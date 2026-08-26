"""Webots-only IK adapter for the ABB IRB 4600 sample world.

The adapter is optional. When Webots runs with `ikpy` available, it computes
sample-style target IK from the `DEF TARGET` node and emits bounded joint
commands. The CGF controller can fall back to bounded graph commands when
`ikpy` is not installed.
"""

from __future__ import annotations

import math
import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from industrial_robot_arm import ABB_IRB_4600_LIMITS_RAD


IKPY_MAX_ITERATIONS = 4
POSITION_TOLERANCE_M = 0.03
ACTIVE_LINKS_MASK = [False, True, True, True, True, True, True, False]
DEFAULT_MAX_JOINT_STEP_RAD = 0.15
DEFAULT_MAX_JOINT_ACCEL_STEP_RAD = 0.04
DEFAULT_TARGET_DEADBAND_M = 0.01
DEFAULT_REPLAN_INTERVAL = 8
DEFAULT_COMMAND_SMOOTHING_ALPHA = 0.35


def _ikpy_major_version(value: object) -> int:
    match = re.match(r"^\s*(\d+)(?:\.|$)", str(value))
    if match is None:
        raise RuntimeError(f'Cannot determine the installed "ikpy" version from {value!r}.')
    return int(match.group(1))


@dataclass(frozen=True)
class RelativeTarget:
    x: float
    y: float
    z: float

    def as_list(self) -> list[float]:
        return [self.x, self.y, self.z]


def target_relative_to_arm(target_position: list[float], arm_position: list[float]) -> RelativeTarget:
    return RelativeTarget(
        x=-(target_position[1] - arm_position[1]),
        y=target_position[0] - arm_position[0],
        z=target_position[2] - arm_position[2],
    )


def squared_tool_error(forward_kinematics: Any, target: RelativeTarget) -> float:
    return (
        (forward_kinematics[0, 3] - target.x) ** 2
        + (forward_kinematics[1, 3] - target.y) ** 2
        + (forward_kinematics[2, 3] - target.z) ** 2
    )


class WebotsIkAdapter:
    def __init__(
        self,
        supervisor: Any,
        *,
        velocity: float = 1.0,
        max_joint_step_rad: float | None = None,
        max_joint_accel_step_rad: float | None = None,
        target_deadband_m: float | None = None,
        replan_interval: int | None = None,
        command_smoothing_alpha: float | None = None,
    ) -> None:
        self.supervisor = supervisor
        self.time_step = int(4 * supervisor.getBasicTimeStep())
        self.velocity = velocity
        configured_step = os.environ.get("CGF_ABB_IRB_4600_MAX_JOINT_STEP_RAD")
        configured_accel = os.environ.get("CGF_ABB_IRB_4600_MAX_JOINT_ACCEL_STEP_RAD")
        configured_deadband = os.environ.get("CGF_ABB_IRB_4600_TARGET_DEADBAND_M")
        configured_replan = os.environ.get("CGF_ABB_IRB_4600_REPLAN_INTERVAL")
        configured_smoothing = os.environ.get("CGF_ABB_IRB_4600_COMMAND_SMOOTHING_ALPHA")
        if max_joint_step_rad is not None:
            self.max_joint_step_rad = max_joint_step_rad
        elif configured_step:
            self.max_joint_step_rad = float(configured_step)
        else:
            self.max_joint_step_rad = DEFAULT_MAX_JOINT_STEP_RAD
        if max_joint_accel_step_rad is not None:
            self.max_joint_accel_step_rad = max_joint_accel_step_rad
        elif configured_accel:
            self.max_joint_accel_step_rad = float(configured_accel)
        else:
            self.max_joint_accel_step_rad = DEFAULT_MAX_JOINT_ACCEL_STEP_RAD
        if target_deadband_m is not None:
            self.target_deadband_m = target_deadband_m
        elif configured_deadband:
            self.target_deadband_m = float(configured_deadband)
        else:
            self.target_deadband_m = DEFAULT_TARGET_DEADBAND_M
        if replan_interval is not None:
            self.replan_interval = max(1, int(replan_interval))
        elif configured_replan:
            self.replan_interval = max(1, int(configured_replan))
        else:
            self.replan_interval = DEFAULT_REPLAN_INTERVAL
        if command_smoothing_alpha is not None:
            self.command_smoothing_alpha = min(1.0, max(0.0, float(command_smoothing_alpha)))
        elif configured_smoothing:
            self.command_smoothing_alpha = min(1.0, max(0.0, float(configured_smoothing)))
        else:
            self.command_smoothing_alpha = DEFAULT_COMMAND_SMOOTHING_ALPHA
        self.last_command: dict[str, float] | None = None
        self.last_command_delta: dict[str, float] = {f"axis_{index}": 0.0 for index in range(1, 7)}
        self.last_target: RelativeTarget | None = None
        self.cached_goal_command: dict[str, float] | None = None
        self.ticks_since_replan = self.replan_interval
        self.arm_chain = self._chain_from_supervisor_urdf()
        self.motors = self._collect_motors()
        self.target = supervisor.getFromDef("TARGET")
        self.arm = supervisor.getSelf()
        if self.target is None:
            raise RuntimeError('World is missing a DEF TARGET node.')

    def _chain_from_supervisor_urdf(self) -> Any:
        try:
            import ikpy
            from ikpy.chain import Chain
        except ImportError as exc:
            raise RuntimeError('The "ikpy" Python module is required for ABB IK mode.') from exc
        if _ikpy_major_version(getattr(ikpy, "__version__", "")) < 3:
            raise RuntimeError('The "ikpy" Python module must be version 3.0 or newer.')
        with tempfile.NamedTemporaryFile(suffix=".urdf", delete=False) as file:
            file.write(self.supervisor.getUrdf().encode("utf-8"))
            urdf_path = Path(file.name)
        try:
            return Chain.from_urdf_file(str(urdf_path), active_links_mask=ACTIVE_LINKS_MASK)
        finally:
            urdf_path.unlink(missing_ok=True)

    def _collect_motors(self) -> list[Any]:
        motors = []
        for link in self.arm_chain.links:
            if "motor" not in link.name:
                continue
            motor = self.supervisor.getDevice(link.name)
            motor.setVelocity(self.velocity)
            sensor = motor.getPositionSensor()
            sensor.enable(self.time_step)
            motors.append(motor)
        if len(motors) < 6:
            raise RuntimeError(f"Expected at least 6 ABB arm motors, found {len(motors)}.")
        return motors

    def current_joint_position(self) -> list[float]:
        return [0.0] + [motor.getPositionSensor().getValue() for motor in self.motors] + [0.0]

    def current_command_map(self) -> dict[str, float]:
        return {f"axis_{index + 1}": motor.getPositionSensor().getValue() for index, motor in enumerate(self.motors[:6])}

    def solve_target(self, target: RelativeTarget) -> Any:
        initial_position = self.current_joint_position()
        result = self.arm_chain.inverse_kinematics(
            target.as_list(),
            max_iter=IKPY_MAX_ITERATIONS,
            initial_position=initial_position,
        )
        position = self.arm_chain.forward_kinematics(result)
        if math.sqrt(squared_tool_error(position, target)) > POSITION_TOLERANCE_M:
            result = self.arm_chain.inverse_kinematics(target.as_list())
        return result

    @staticmethod
    def _nearest_equivalent_angle(value: float, reference: float, lower: float, upper: float) -> float:
        candidates = [value + (2.0 * math.pi * offset) for offset in range(-2, 3)]
        valid = [candidate for candidate in candidates if lower <= candidate <= upper]
        if not valid:
            valid = [min(max(value, lower), upper)]
        return min(valid, key=lambda candidate: abs(candidate - reference))

    def _continuous_command(self, raw_command: dict[str, float], previous: dict[str, float]) -> dict[str, float]:
        continuous: dict[str, float] = {}
        for index in range(1, 7):
            axis = f"axis_{index}"
            lower, upper = ABB_IRB_4600_LIMITS_RAD[axis]
            continuous[axis] = self._nearest_equivalent_angle(raw_command[axis], previous[axis], lower, upper)
        return continuous

    def _rate_limited_command(
        self,
        command: dict[str, float],
        previous: dict[str, float],
    ) -> tuple[dict[str, float], bool]:
        emitted: dict[str, float] = {}
        clamped = False
        for index in range(1, 7):
            axis = f"axis_{index}"
            delta = command[axis] - previous[axis]
            if abs(delta) > self.max_joint_step_rad:
                clamped = True
                delta = math.copysign(self.max_joint_step_rad, delta)
            lower, upper = ABB_IRB_4600_LIMITS_RAD[axis]
            emitted[axis] = min(max(previous[axis] + delta, lower), upper)
        return emitted, clamped

    @staticmethod
    def _target_distance(a: RelativeTarget, b: RelativeTarget) -> float:
        return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)

    def _should_replan(self, target: RelativeTarget) -> bool:
        if self.cached_goal_command is None or self.last_target is None:
            return True
        if self._target_distance(target, self.last_target) >= self.target_deadband_m:
            return True
        return self.ticks_since_replan >= self.replan_interval

    def _smooth_goal_command(self, command: dict[str, float], previous: dict[str, float]) -> dict[str, float]:
        continuous = self._continuous_command(command, previous)
        if self.cached_goal_command is None:
            return continuous
        alpha = self.command_smoothing_alpha
        return {
            axis: alpha * continuous[axis] + (1.0 - alpha) * self.cached_goal_command[axis]
            for axis in continuous
        }

    def _smooth_rate_limited_command(
        self,
        command: dict[str, float],
        previous: dict[str, float],
    ) -> tuple[dict[str, float], bool]:
        emitted: dict[str, float] = {}
        clamped = False
        for axis, value in command.items():
            if not isinstance(value, (int, float)) or not math.isfinite(float(value)):
                raise ValueError(f"non-finite command for {axis}")
            lower, upper = ABB_IRB_4600_LIMITS_RAD[axis]
            target = min(max(float(value), lower), upper)
            desired_delta = target - previous[axis]
            if abs(desired_delta) > self.max_joint_step_rad:
                clamped = True
                desired_delta = math.copysign(self.max_joint_step_rad, desired_delta)
            prior_delta = self.last_command_delta.get(axis, 0.0)
            delta_change = desired_delta - prior_delta
            if abs(delta_change) > self.max_joint_accel_step_rad:
                clamped = True
                desired_delta = prior_delta + math.copysign(self.max_joint_accel_step_rad, delta_change)
            emitted[axis] = min(max(previous[axis] + desired_delta, lower), upper)
            self.last_command_delta[axis] = emitted[axis] - previous[axis]
        return emitted, clamped

    def step_to_target(self) -> dict[str, Any]:
        target = target_relative_to_arm(self.target.getPosition(), self.arm.getPosition())
        previous = self.last_command or self.current_command_map()
        replanned = self._should_replan(target)
        if replanned:
            result = self.solve_target(target)
            raw_command = {f"axis_{index + 1}": float(result[index + 1]) for index in range(6)}
            self.cached_goal_command = self._smooth_goal_command(raw_command, previous)
            self.last_target = target
            self.ticks_since_replan = 0
        elif self.cached_goal_command is not None:
            raw_command = dict(self.cached_goal_command)
            self.ticks_since_replan += 1
        else:
            raise RuntimeError("IK adapter has no cached command")
        emitted, clamped = self._smooth_rate_limited_command(self.cached_goal_command, previous)
        for index, motor in enumerate(self.motors[:6]):
            motor.setPosition(emitted[f"axis_{index + 1}"])
        self.last_command = emitted
        safety_reason = "joint_step_or_accel_limit" if clamped else "webots_ik_command_with_graph_trace"
        if not replanned and not clamped:
            safety_reason = "reused_cached_ik_command"
        return {
            "target": {"x": target.x, "y": target.y, "z": target.z},
            "original_command": raw_command,
            "emitted_command": emitted,
            "safety_outcome": "clamp" if clamped else "allow",
            "safety_reason": safety_reason,
            "replanned": replanned,
            "ticks_since_replan": self.ticks_since_replan,
            "target_deadband_m": self.target_deadband_m,
            "replan_interval": self.replan_interval,
        }
