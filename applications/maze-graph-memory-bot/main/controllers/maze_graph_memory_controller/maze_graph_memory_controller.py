"""Webots controller for Maze Graph Memory Bot."""

from __future__ import annotations

from dataclasses import asdict
import json
import math
import os
from pathlib import Path
import sys

try:
    from controller import Supervisor as Robot
except ImportError as exc:  # pragma: no cover - executed only inside Webots
    raise SystemExit("This controller must be run by Webots.") from exc


APP_DIR = Path(__file__).resolve().parents[3]
CGF_ROOT = APP_DIR.parents[1]
BOTS_DIR = CGF_ROOT / "applications" / "bots"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))
if str(BOTS_DIR) not in sys.path:
    sys.path.insert(0, str(BOTS_DIR))

from maze_webots_graph_policy import (  # noqa: E402
    MazeActionOutcomeMemory,
    build_recovery_plan,
    build_sensor_state,
    goal_sensor_reading,
    guard_recovery_item,
    navigation_sensor_record,
    recovery_decision,
    select_maze_action,
)
from maze_failure_diagnostics import diagnostic_record, is_failure_point  # noqa: E402


def _env_flag(name: str, default: str = "0") -> bool:
    return os.environ.get(name, default).strip().lower() in {"1", "true", "yes", "on"}


def _safe_device(robot: Robot, name: str):
    try:
        return robot.getDevice(name)
    except Exception:
        return None


def _csv_names(name: str, default: tuple[str, ...]) -> tuple[str, ...]:
    configured = os.environ.get(name)
    if not configured:
        return default
    return tuple(part.strip() for part in configured.split(",") if part.strip())


def _safe_devices(robot: Robot, names: tuple[str, ...]) -> list[object]:
    devices = []
    for name in names:
        device = _safe_device(robot, name)
        if device is not None:
            devices.append(device)
    return devices


def _set_wheel_velocity(motors: list[object], velocity: float) -> None:
    for motor in motors:
        try:
            motor.setVelocity(velocity)
        except Exception:
            pass


def _enable_device(device: object | None, timestep: int) -> None:
    if device is None:
        return
    try:
        device.enable(timestep)
    except Exception:
        pass


def _wrap_angle(value: float) -> float:
    return (float(value) + math.pi) % (2.0 * math.pi) - math.pi


def _compass_yaw(compass: object | None, fallback: float = 0.0) -> float:
    if compass is None or not hasattr(compass, "getValues"):
        return fallback
    try:
        values = compass.getValues()
    except Exception:
        return fallback
    if len(values) < 2:
        return fallback
    x = float(values[0])
    y = float(values[1])
    if not (math.isfinite(x) and math.isfinite(y)):
        return fallback
    return _wrap_angle(-math.atan2(y, x))


def _robot_pose(
    gps: object | None,
    compass: object | None,
    fallback: tuple[float, float, float],
    yaw_offset: float,
) -> tuple[float, float, float]:
    x, y, yaw = fallback
    if gps is not None and hasattr(gps, "getValues"):
        try:
            values = gps.getValues()
        except Exception:
            values = ()
        if len(values) >= 2:
            gx = float(values[0])
            gy = float(values[1])
            if math.isfinite(gx) and math.isfinite(gy):
                x, y = gx, gy
    yaw = _wrap_angle(_compass_yaw(compass, yaw) + yaw_offset)
    return (x, y, yaw)


def _goal_target(robot: Robot, def_name: str, fallback: tuple[float, float]) -> tuple[float, float]:
    try:
        node = robot.getFromDef(def_name)
    except Exception:
        node = None
    if node is not None:
        try:
            field = node.getField("translation")
            values = field.getSFVec3f()
        except Exception:
            values = ()
        if len(values) >= 2:
            x = float(values[0])
            y = float(values[1])
            if math.isfinite(x) and math.isfinite(y):
                return (x, y)
    return fallback


def _pose_distance(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _range_clearances(lidar: object | None, max_range: float = 8.0) -> tuple[float, float, float, float]:
    if lidar is None or not hasattr(lidar, "getRangeImage"):
        return (1.0, 1.0, 1.0, 1.0)
    try:
        values = [float(value) for value in lidar.getRangeImage()]
    except Exception:
        return (1.0, 1.0, 1.0, 1.0)
    values = [value for value in values if math.isfinite(value) and value >= 0.0]
    if not values:
        return (1.0, 1.0, 1.0, 1.0)
    normalized = [max(0.0, min(1.0, value / max_range)) for value in values]
    count = len(normalized)
    third = max(1, count // 3)
    center = count // 2
    window = max(1, count // 10)
    left = min(normalized[:third])
    right = min(normalized[-third:])
    front = min(normalized[max(0, center - window): min(count, center + window + 1)])
    nearest = min(normalized)
    return (front, left, right, nearest)


def _load_learning_memory(path: Path) -> MazeActionOutcomeMemory:
    if not path.exists():
        return MazeActionOutcomeMemory()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return MazeActionOutcomeMemory()
    if not isinstance(payload, dict):
        return MazeActionOutcomeMemory()
    return MazeActionOutcomeMemory.from_dict(payload)


def _save_learning_memory(path: Path, memory: MazeActionOutcomeMemory) -> None:
    path.write_text(json.dumps(memory.to_dict(), sort_keys=True, indent=2), encoding="utf-8")


def main() -> int:
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())
    max_ticks = int(os.environ.get("CGF_MAZE_GRAPH_MEMORY_MAX_TICKS", "0"))
    auto_quit = _env_flag("CGF_WEBOTS_AUTO_QUIT")
    yaw_offset = float(os.environ.get("CGF_MAZE_GRAPH_MEMORY_YAW_OFFSET_RAD", str(math.pi / 2.0)))
    left_motor_names = _csv_names(
        "CGF_MAZE_GRAPH_MEMORY_LEFT_MOTORS",
        ("front left wheel", "back left wheel"),
    )
    right_motor_names = _csv_names(
        "CGF_MAZE_GRAPH_MEMORY_RIGHT_MOTORS",
        ("front right wheel", "back right wheel"),
    )
    left_motors = _safe_devices(robot, left_motor_names)
    right_motors = _safe_devices(robot, right_motor_names)
    gps = _safe_device(robot, os.environ.get("CGF_MAZE_GRAPH_MEMORY_GPS", "gps"))
    compass = _safe_device(robot, os.environ.get("CGF_MAZE_GRAPH_MEMORY_COMPASS", "compass"))
    lidar = _safe_device(robot, os.environ.get("CGF_MAZE_GRAPH_MEMORY_LIDAR", "Sick LMS 291"))
    _enable_device(gps, timestep)
    _enable_device(compass, timestep)
    _enable_device(lidar, timestep)
    if lidar is not None and hasattr(lidar, "enablePointCloud"):
        try:
            lidar.enablePointCloud()
        except Exception:
            pass
    for motor in (*left_motors, *right_motors):
        try:
            motor.setPosition(float("inf"))
            motor.setVelocity(0.0)
        except Exception:
            pass

    runtime_dir = Path(
        os.environ.get(
            "CGF_MAZE_GRAPH_MEMORY_RUNTIME_DIR",
            str(APP_DIR / "main" / "runtime"),
        )
    ).expanduser()
    runtime_dir.mkdir(parents=True, exist_ok=True)
    trace_path = runtime_dir / "maze_graph_memory_webots_trace.jsonl"
    diagnostics_path = runtime_dir / "maze_graph_memory_diagnostics.jsonl"
    failure_points_path = runtime_dir / "maze_graph_memory_failure_points.jsonl"
    learning_memory_path = runtime_dir / "maze_graph_memory_learning.json"
    persist_learning = _env_flag("CGF_MAZE_GRAPH_MEMORY_PERSIST_LEARNING")
    learning_memory = _load_learning_memory(learning_memory_path) if persist_learning else MazeActionOutcomeMemory()

    tick = 0
    spin_streak = 0
    pose = (16.0, -16.0, 0.0)
    previous_pose = pose
    previous_command_active = False
    no_progress_streak = 0
    contact_streak = 0
    goal_def = os.environ.get("CGF_MAZE_GRAPH_MEMORY_GOAL_DEF", "MAZEBOT_GOAL")
    fallback_goal = tuple(
        float(part.strip())
        for part in os.environ.get("CGF_MAZE_GRAPH_MEMORY_GOAL_XY", "-16,16").split(",", 1)
    )
    recovery_queue: list[dict[str, object]] = []
    pending_learning: dict[str, object] | None = None
    with (
        trace_path.open("w", encoding="utf-8") as handle,
        diagnostics_path.open("w", encoding="utf-8") as diagnostics_handle,
        failure_points_path.open("w", encoding="utf-8") as failure_handle,
    ):
        while robot.step(timestep) != -1 and (max_ticks <= 0 or tick < max_ticks):
            pose = _robot_pose(gps, compass, pose, yaw_offset)
            navigation_goal = _goal_target(robot, goal_def, fallback_goal)
            state = build_sensor_state(
                tick=tick,
                pose=pose,
                goal=navigation_goal,
                clearances=_range_clearances(lidar),
                spin_streak=spin_streak,
            )
            goal_sensor = goal_sensor_reading(state)
            navigation_sensor = navigation_sensor_record(state)
            memory_context_key = navigation_sensor["memory_context_key"]
            movement_delta = _pose_distance(pose, previous_pose)
            contact_active = state.front_clearance < 0.08 or state.nearest_clearance < 0.06
            action_no_progress = previous_command_active and movement_delta < 0.008
            learning_outcome = None
            if pending_learning is not None:
                pending_goal = tuple(pending_learning["goal"])
                current_pending_distance = math.hypot(float(pending_goal[0]) - pose[0], float(pending_goal[1]) - pose[1])
                learning_outcome = learning_memory.record_outcome(
                    context_key=str(pending_learning["context_key"]),
                    action_id=str(pending_learning["action_id"]),
                    movement_delta=movement_delta,
                    previous_goal_distance=float(pending_learning["previous_goal_distance"]),
                    current_goal_distance=current_pending_distance,
                    contact_active=contact_active,
                    no_progress=action_no_progress,
                )
                _save_learning_memory(learning_memory_path, learning_memory)
            if contact_active:
                contact_streak += 1
            else:
                contact_streak = 0
            if previous_command_active and contact_active and movement_delta < 0.008:
                no_progress_streak += 1
            elif movement_delta > 0.020 or not contact_active:
                no_progress_streak = 0
            if not recovery_queue and (contact_streak >= 10 or no_progress_streak >= 4):
                recovery_queue = build_recovery_plan(state)
                contact_streak = 0
                no_progress_streak = 0

            recovery_item = guard_recovery_item(state, recovery_queue.pop(0)) if recovery_queue else None
            if recovery_item is not None:
                decision = recovery_decision(
                    state,
                    action_id=str(recovery_item["action_id"]),
                    command=dict(recovery_item["command"]),
                    reason=str(recovery_item["reason"]),
                )
            else:
                decision = select_maze_action(
                    state,
                    memory_biases=learning_memory.biases_for(context_key=memory_context_key),
                )
            command = decision.selected_command
            throttle = float(command.get("throttle", 0.0))
            turn = float(command.get("turn", 0.0))
            left_velocity = max(-4.0, min(4.0, 4.0 * (throttle - turn)))
            right_velocity = max(-4.0, min(4.0, 4.0 * (throttle + turn)))
            emitted_wheel_velocity = {
                "left": round(left_velocity, 4),
                "right": round(right_velocity, 4),
            }
            _set_wheel_velocity(left_motors, left_velocity)
            _set_wheel_velocity(right_motors, right_velocity)
            if abs(turn) >= 0.55 and abs(throttle) <= 0.08:
                spin_streak += 1
            else:
                spin_streak = 0
            learning_summary = learning_memory.summary_for(context_key=memory_context_key)
            trace_step = {
                "schema": "cgf.maze_graph_memory.webots_trace_step.v1",
                "tick": tick,
                "sensor_state": asdict(state),
                "movement_delta": round(movement_delta, 5),
                "persistent_learning_enabled": persist_learning,
                "learning_outcome": learning_outcome,
                "learning_memory": learning_summary,
                "goal_sensor": goal_sensor,
                "navigation_sensor": navigation_sensor,
                "contact_streak": contact_streak,
                "no_progress_streak": no_progress_streak,
                "recovery_queue_remaining": len(recovery_queue),
                "decision": decision.to_dict(),
                "emitted_wheel_velocity": emitted_wheel_velocity,
            }
            diagnostic = diagnostic_record(
                state=state,
                decision=decision,
                movement_delta=movement_delta,
                contact_streak=contact_streak,
                no_progress_streak=no_progress_streak,
                recovery_queue_remaining=len(recovery_queue),
                emitted_wheel_velocity=emitted_wheel_velocity,
                navigation_sensor=navigation_sensor,
                goal_sensor=goal_sensor,
                learning_outcome=learning_outcome,
                learning_memory=learning_summary,
            )
            handle.write(json.dumps(trace_step, sort_keys=True) + "\n")
            diagnostics_handle.write(json.dumps(diagnostic, sort_keys=True) + "\n")
            if is_failure_point(diagnostic):
                failure_handle.write(json.dumps(diagnostic, sort_keys=True) + "\n")
            previous_pose = pose
            previous_command_active = abs(throttle) > 0.05 or abs(turn) > 0.05
            pending_learning = {
                "context_key": memory_context_key,
                "goal": navigation_goal,
                "action_id": decision.selected_action_id,
                "previous_goal_distance": state.distance_to_goal,
            }
            tick += 1
    if auto_quit:
        robot.simulationQuit(0)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
