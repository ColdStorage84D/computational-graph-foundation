"""Webots controller for the ABB IRB 4600 CGF graph app."""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import traceback

try:
    from controller import Supervisor
except ImportError as exc:  # pragma: no cover - executed only inside Webots
    raise SystemExit("This controller must be run by Webots.") from exc


APP_DIR = Path(__file__).resolve().parents[3]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from industrial_robot_arm import (  # noqa: E402
    WEBOTS_MOTOR_NAMES,
    build_hold_trace_step,
    build_industrial_arm_topology,
    build_reach_trace_step,
    safety_gate_command,
    summarize_topology,
    zero_command,
)


def _trace_dir() -> Path:
    configured = os.environ.get("CGF_ABB_IRB_4600_TRACE_DIR")
    path = Path(configured) if configured else APP_DIR / "main" / "runtime"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _env_flag(name: str, default: str = "0") -> bool:
    return os.environ.get(name, default).strip().lower() in {"1", "true", "yes", "on"}


def _fallback_motors(supervisor: Supervisor, timestep: int) -> dict[str, object]:
    motors: dict[str, object] = {}
    for axis, name in WEBOTS_MOTOR_NAMES.items():
        try:
            motor = supervisor.getDevice(name)
            motor.setVelocity(1.0)
            sensor = motor.getPositionSensor()
            sensor.enable(timestep)
            motors[axis] = motor
        except Exception:
            pass
    return motors


def _fallback_command(tick: int) -> dict[str, float]:
    if tick == 0:
        return zero_command()
    return {
        "axis_1": 0.35,
        "axis_2": 0.60,
        "axis_3": 0.18,
        "axis_4": 0.25,
        "axis_5": 0.48,
        "axis_6": 0.0,
    }


def _apply_command(motors: dict[str, object], command: dict[str, float]) -> None:
    for axis, motor in motors.items():
        try:
            motor.setPosition(float(command[axis]))
        except Exception:
            pass


def main() -> int:
    supervisor = Supervisor()
    graph_summary = summarize_topology(build_industrial_arm_topology())
    max_ticks = int(os.environ.get("CGF_ABB_IRB_4600_MAX_TICKS", "0"))
    auto_quit = _env_flag("CGF_WEBOTS_AUTO_QUIT")
    seed = int(os.environ.get("CGF_ABB_IRB_4600_SEED", "0"))
    trace_path = _trace_dir() / f"abb-irb-4600-webots-seed-{seed}.jsonl"
    error_path = _trace_dir() / "abb_irb_4600_controller_error.log"
    timestep = int(4 * supervisor.getBasicTimeStep())
    previous = zero_command()
    fallback_motors = _fallback_motors(supervisor, timestep)

    adapter = None
    adapter_error = None
    if os.environ.get("CGF_ABB_IRB_4600_WEBOTS_IK", "1") == "1":
        try:
            from abb_webots_ik_adapter import WebotsIkAdapter

            adapter = WebotsIkAdapter(supervisor)
            timestep = adapter.time_step
        except Exception as exc:
            adapter_error = str(exc)

    tick = 0
    try:
        with trace_path.open("w", encoding="utf-8") as handle:
            while (max_ticks <= 0 or tick < max_ticks) and supervisor.step(timestep) != -1:
                adapter_metadata = None
                if adapter is not None:
                    try:
                        result = adapter.step_to_target()
                        gate = {
                            "outcome": result["safety_outcome"],
                            "reason": result["safety_reason"],
                            "original_command": result["original_command"],
                            "emitted_command": result["emitted_command"],
                        }
                        target = result["target"]
                        adapter_metadata = {
                            "mode": "ik_temporal_coherence",
                            "replanned": result["replanned"],
                            "ticks_since_replan": result["ticks_since_replan"],
                            "target_deadband_m": result["target_deadband_m"],
                            "replan_interval": result["replan_interval"],
                        }
                    except Exception as exc:
                        adapter_error = f"ik_runtime_error: {exc}"
                        adapter = None
                        gate = safety_gate_command(_fallback_command(tick), previous=previous)
                        target = {"x": 0.0, "y": 0.0, "z": 0.0, "mode": "fallback_after_ik_error"}
                        _apply_command(fallback_motors, gate["emitted_command"])
                elif tick == 0:
                    step = build_hold_trace_step(
                        episode_id=f"abb-irb-4600-webots-seed-{seed}",
                        seed=seed,
                        tick=tick,
                        graph_summary=graph_summary,
                    )
                    handle.write(json.dumps(step, sort_keys=True) + "\n")
                    tick += 1
                    continue
                else:
                    gate = safety_gate_command(_fallback_command(tick), previous=previous)
                    target = {"x": 0.0, "y": 0.0, "z": 0.0, "mode": "fallback_no_ikpy"}
                    _apply_command(fallback_motors, gate["emitted_command"])

                previous = dict(gate["emitted_command"])
                step = build_reach_trace_step(
                    episode_id=f"abb-irb-4600-webots-seed-{seed}",
                    seed=seed,
                    tick=tick,
                    graph_summary=graph_summary,
                    destination_pose=target,
                    safety_gate=gate,
                )
                if adapter_error:
                    step["webots_adapter"] = {
                        "mode": "fallback_bounded_joint_command",
                        "reason": adapter_error,
                    }
                elif adapter_metadata:
                    step["webots_adapter"] = adapter_metadata
                handle.write(json.dumps(step, sort_keys=True) + "\n")
                tick += 1
    except BaseException:
        error_path.write_text(traceback.format_exc(), encoding="utf-8")
        raise
    finally:
        if auto_quit:
            supervisor.simulationQuit(0)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
