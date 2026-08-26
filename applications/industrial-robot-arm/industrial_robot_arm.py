"""Industrial Robot Arm Graph application.

This app is a self-contained CGF robot-control demonstration. It models a
six-axis industrial arm as graph topology, action candidates, safety gates, and
traceable emitted commands. It does not control a real robot.
"""

from __future__ import annotations

import json
import math
import os
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


APP_DIR = Path(__file__).resolve().parent
WEBOTS_WORLD_PATH = APP_DIR / "main" / "worlds" / "inverse_kinematics.wbt"
AXES = tuple(f"axis_{index}" for index in range(1, 7))
WEBOTS_MOTOR_NAMES = {
    "axis_1": "A motor",
    "axis_2": "B motor",
    "axis_3": "C motor",
    "axis_4": "D motor",
    "axis_5": "E motor",
    "axis_6": "F motor",
}
ABB_IRB_4600_LIMITS_RAD = {
    "axis_1": (-3.1415, 3.1415),
    "axis_2": (-1.5708, 2.61799),
    "axis_3": (-3.1415, 1.309),
    "axis_4": (-6.98132, 6.98132),
    "axis_5": (-2.18166, 2.0944),
    "axis_6": (-6.98132, 6.98132),
}


@dataclass(frozen=True)
class GraphNode:
    node_id: str
    node_type: str
    features: dict[str, Any]

    def to_json(self) -> dict[str, Any]:
        return {"id": self.node_id, "type": self.node_type, "features": dict(self.features)}


@dataclass(frozen=True)
class GraphEdge:
    source: str
    edge_type: str
    to_node: str

    def to_json(self) -> dict[str, str]:
        return {"source": self.source, "type": self.edge_type, "to": self.to_node}


@dataclass(frozen=True)
class ArmRunReport:
    episode_id: str
    seed: int
    ticks: int
    trace_path: Path
    graph_summary: dict[str, int]

    def to_json(self) -> dict[str, Any]:
        return {
            "episode_id": self.episode_id,
            "seed": self.seed,
            "ticks": self.ticks,
            "trace_path": str(self.trace_path),
            "graph_summary": dict(self.graph_summary),
        }


def build_industrial_arm_topology(profile: str = "abb_irb_4600_demo") -> dict[str, Any]:
    """Build a six-axis arm topology with joints, actuators, goals, and limits."""

    nodes: list[GraphNode] = [
        GraphNode("body:base", "body_part", {"role": "fixed_base", "profile": profile}),
        GraphNode("body:link_1", "body_part", {"role": "arm_link", "index": 1}),
        GraphNode("body:link_2", "body_part", {"role": "arm_link", "index": 2}),
        GraphNode("body:link_3", "body_part", {"role": "arm_link", "index": 3}),
        GraphNode("body:link_4", "body_part", {"role": "arm_link", "index": 4}),
        GraphNode("body:link_5", "body_part", {"role": "arm_link", "index": 5}),
        GraphNode("body:link_6", "body_part", {"role": "arm_link", "index": 6}),
        GraphNode("body:flange", "body_part", {"role": "flange"}),
        GraphNode("body:tool", "body_part", {"role": "end_effector"}),
        GraphNode("sensor:joint_state", "sensor", {"kind": "joint_encoder_bundle"}),
        GraphNode("sensor:tool_pose", "sensor", {"kind": "tool_pose"}),
        GraphNode("sensor:workcell_proximity", "sensor", {"kind": "proximity"}),
        GraphNode("goal:hold_safe", "task_goal", {"goal": "bounded_stationary_state"}),
        GraphNode("goal:reach_pose", "task_goal", {"goal": "tool_frame"}),
        GraphNode("action:hold", "action_candidate", {"command_family": "hold"}),
        GraphNode("action:bounded_joint_delta", "action_candidate", {"command_family": "joint_delta"}),
        GraphNode("action:retreat", "action_candidate", {"command_family": "retreat"}),
    ]
    edges: list[GraphEdge] = [
        GraphEdge("body:link_1", "attached_to", "body:base"),
        GraphEdge("body:link_2", "attached_to", "body:link_1"),
        GraphEdge("body:link_3", "attached_to", "body:link_2"),
        GraphEdge("body:link_4", "attached_to", "body:link_3"),
        GraphEdge("body:link_5", "attached_to", "body:link_4"),
        GraphEdge("body:link_6", "attached_to", "body:link_5"),
        GraphEdge("body:flange", "attached_to", "body:link_6"),
        GraphEdge("body:tool", "attached_to", "body:flange"),
        GraphEdge("sensor:joint_state", "observes", "body:link_1"),
        GraphEdge("sensor:joint_state", "observes", "body:link_6"),
        GraphEdge("sensor:tool_pose", "observes", "body:tool"),
        GraphEdge("sensor:workcell_proximity", "observes", "body:tool"),
        GraphEdge("goal:hold_safe", "supports", "action:hold"),
        GraphEdge("goal:reach_pose", "supports", "action:bounded_joint_delta"),
        GraphEdge("goal:reach_pose", "supports", "action:retreat"),
    ]

    previous_body = "body:base"
    for index, axis in enumerate(AXES, start=1):
        lower, upper = ABB_IRB_4600_LIMITS_RAD[axis]
        joint_id = f"joint:{axis}"
        actuator_id = f"actuator:{axis}"
        limit_id = f"limit:{axis}_range"
        body_id = f"body:link_{index}"
        nodes.extend(
            [
                GraphNode(joint_id, "joint", {"dof": 1, "axis": axis}),
                GraphNode(
                    actuator_id,
                    "actuator",
                    {
                        "command": "bounded_position_delta",
                        "axis": axis,
                        "webots_device": WEBOTS_MOTOR_NAMES[axis],
                    },
                ),
                GraphNode(limit_id, "safety_limit", {"min_rad": lower, "max_rad": upper}),
            ]
        )
        edges.extend(
            [
                GraphEdge(joint_id, "attached_to", previous_body),
                GraphEdge(body_id, "attached_to", joint_id),
                GraphEdge(actuator_id, "drives", joint_id),
                GraphEdge(limit_id, "constrains", joint_id),
                GraphEdge(limit_id, "constrains", actuator_id),
                GraphEdge("action:bounded_joint_delta", "commands", actuator_id),
                GraphEdge("action:hold", "commands", actuator_id),
                GraphEdge("action:retreat", "commands", actuator_id),
            ]
        )
        previous_body = body_id

    return {
        "schema": "cgf.industrial_robot_arm.topology.v1",
        "profile": profile,
        "graph_id": "industrial_robot_arm_six_axis_topology",
        "nodes": [node.to_json() for node in nodes],
        "edges": [edge.to_json() for edge in edges],
    }


def summarize_topology(graph: dict[str, Any]) -> dict[str, int]:
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    return {
        "nodes": len(nodes),
        "edges": len(edges),
        "joints": sum(1 for node in nodes if node.get("type") == "joint"),
        "actuators": sum(1 for node in nodes if node.get("type") == "actuator"),
        "limits": sum(1 for node in nodes if node.get("type") == "safety_limit"),
    }


def zero_command() -> dict[str, float]:
    return {axis: 0.0 for axis in AXES}


def safety_gate_command(
    command: dict[str, float],
    *,
    previous: dict[str, float] | None = None,
    max_joint_step_rad: float = 0.15,
) -> dict[str, Any]:
    """Validate and rate-limit a six-axis command before it can be emitted."""

    previous = previous or zero_command()
    if set(command) != set(AXES):
        return {
            "outcome": "block",
            "reason": "command_axes_do_not_match_topology",
            "original_command": dict(command),
            "emitted_command": zero_command(),
        }

    emitted: dict[str, float] = {}
    clamped = False
    for axis, value in command.items():
        if not isinstance(value, (int, float)) or not math.isfinite(float(value)):
            return {
                "outcome": "block",
                "reason": "command_contains_non_finite_value",
                "original_command": dict(command),
                "emitted_command": zero_command(),
            }
        lower, upper = ABB_IRB_4600_LIMITS_RAD[axis]
        bounded = min(upper, max(lower, float(value)))
        delta = bounded - float(previous.get(axis, 0.0))
        if abs(delta) > max_joint_step_rad:
            bounded = float(previous.get(axis, 0.0)) + math.copysign(max_joint_step_rad, delta)
            clamped = True
        if bounded != float(value):
            clamped = True
        emitted[axis] = bounded

    return {
        "outcome": "clamp" if clamped else "allow",
        "reason": "joint_step_or_range_limit" if clamped else "command_within_declared_limits",
        "original_command": dict(command),
        "emitted_command": emitted,
    }


def _evidence_paths_for_action(selected_action: str) -> list[list[str]]:
    goal = "goal:hold_safe" if selected_action == "action:hold" else "goal:reach_pose"
    return [
        [goal, "supports", selected_action, "commands", f"actuator:{axis}"]
        for axis in AXES
    ] + [[f"limit:{axis}_range", "constrains", f"actuator:{axis}"] for axis in AXES]


def build_hold_trace_step(
    *,
    episode_id: str,
    seed: int,
    tick: int,
    graph_summary: dict[str, int],
) -> dict[str, Any]:
    return {
        "schema": "cgf.industrial_robot_arm.trace_step.v1",
        "episode_id": episode_id,
        "seed": seed,
        "tick": tick,
        "task": "hold_safe",
        "selected_action": "action:hold",
        "graph_summary": dict(graph_summary),
        "model_scores": {"action:hold": 1.0, "action:bounded_joint_delta": 0.0, "action:retreat": 0.0},
        "safety_gate": {
            "outcome": "allow",
            "reason": "hold_command_within_declared_limits",
            "original_command": zero_command(),
            "emitted_command": zero_command(),
        },
        "evidence_paths": _evidence_paths_for_action("action:hold"),
        "outcome": {
            "blocked_before_emit": False,
            "collision": False,
            "limit_violation": False,
            "unsafe_action_emitted": False,
        },
        "training_labels": {
            "training_only": True,
            "task_progress_delta": 0.0,
            "limit_violation": False,
        },
    }


def build_reach_trace_step(
    *,
    episode_id: str,
    seed: int,
    tick: int,
    graph_summary: dict[str, int],
    destination_pose: dict[str, float],
    safety_gate: dict[str, Any],
) -> dict[str, Any]:
    blocked = safety_gate["outcome"] == "block"
    return {
        "schema": "cgf.industrial_robot_arm.trace_step.v1",
        "episode_id": episode_id,
        "seed": seed,
        "tick": tick,
        "task": "reach_pose",
        "selected_action": "action:bounded_joint_delta",
        "graph_summary": dict(graph_summary),
        "model_scores": {"action:bounded_joint_delta": 1.0, "action:hold": 0.2, "action:retreat": 0.1},
        "safety_gate": dict(safety_gate),
        "evidence_paths": _evidence_paths_for_action("action:bounded_joint_delta"),
        "outcome": {
            "blocked_before_emit": blocked,
            "collision": False,
            "limit_violation": safety_gate["outcome"] != "allow",
            "unsafe_action_emitted": False,
            "destination_pose": dict(destination_pose),
        },
        "training_labels": {
            "training_only": True,
            "task_progress_delta": 0.0,
            "limit_violation": safety_gate["outcome"] != "allow",
        },
    }


def validate_trace_step(trace: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = (
        "schema",
        "episode_id",
        "seed",
        "tick",
        "selected_action",
        "graph_summary",
        "model_scores",
        "safety_gate",
        "evidence_paths",
        "outcome",
        "training_labels",
    )
    for key in required:
        if key not in trace:
            errors.append(f"missing {key}")
    selected = str(trace.get("selected_action", ""))
    if selected and selected not in trace.get("model_scores", {}):
        errors.append("selected action must have a model score")
    evidence_text = " ".join(" ".join(str(part) for part in path) for path in trace.get("evidence_paths", []))
    if selected and selected not in evidence_text:
        errors.append("selected action must appear in evidence paths")
    gate = trace.get("safety_gate", {})
    emitted = gate.get("emitted_command", {})
    if set(emitted) != set(AXES):
        errors.append("emitted command must cover every axis")
    if trace.get("training_labels", {}).get("training_only") is not True:
        errors.append("training labels must be marked training_only")
    if trace.get("outcome", {}).get("unsafe_action_emitted") is True:
        errors.append("trace must not emit unsafe actions")
    if gate.get("outcome") == "block" and trace.get("outcome", {}).get("blocked_before_emit") is not True:
        errors.append("blocked gate must be visible in outcome")
    return errors


def _demo_command_for_tick(tick: int) -> dict[str, float]:
    if tick % 3 == 1:
        return {
            "axis_1": 0.05,
            "axis_2": 0.08,
            "axis_3": -0.04,
            "axis_4": 0.06,
            "axis_5": -0.03,
            "axis_6": 0.02,
        }
    return {
        "axis_1": 0.70,
        "axis_2": 0.42,
        "axis_3": -0.35,
        "axis_4": 0.80,
        "axis_5": -0.40,
        "axis_6": 0.30,
    }


def run_offline_demo(
    seed: int = 0,
    max_ticks: int = 3,
    trace_dir: str | Path | None = None,
) -> ArmRunReport:
    """Run an offline graph-control episode and write JSONL trace steps."""

    graph = build_industrial_arm_topology()
    graph_summary = summarize_topology(graph)
    episode_id = f"industrial-arm-offline-seed-{seed}"
    output_dir = Path(trace_dir) if trace_dir is not None else Path(tempfile.mkdtemp(prefix="cgf-industrial-arm-"))
    output_dir.mkdir(parents=True, exist_ok=True)
    trace_path = output_dir / f"{episode_id}.jsonl"
    previous = zero_command()
    destination_pose = {"x": 1.0, "y": 0.2, "z": 0.8}
    with trace_path.open("w", encoding="utf-8") as handle:
        for tick in range(max_ticks):
            if tick == 0:
                step = build_hold_trace_step(
                    episode_id=episode_id,
                    seed=seed,
                    tick=tick,
                    graph_summary=graph_summary,
                )
            else:
                gate = safety_gate_command(_demo_command_for_tick(tick), previous=previous)
                previous = dict(gate["emitted_command"])
                step = build_reach_trace_step(
                    episode_id=episode_id,
                    seed=seed,
                    tick=tick,
                    graph_summary=graph_summary,
                    destination_pose=destination_pose,
                    safety_gate=gate,
                )
            handle.write(json.dumps(step, sort_keys=True) + "\n")
    return ArmRunReport(
        episode_id=episode_id,
        seed=seed,
        ticks=max_ticks,
        trace_path=trace_path,
        graph_summary=graph_summary,
    )


def _find_webots_executable() -> str | None:
    webots_home = os.environ.get("WEBOTS_HOME")
    if webots_home:
        candidate = Path(webots_home) / "msys64" / "mingw64" / "bin" / "webots.exe"
        if candidate.exists():
            return str(candidate)
        candidate = Path(webots_home) / "webots.exe"
        if candidate.exists():
            return str(candidate)
    return shutil.which("webots")


def webots_world_path() -> Path:
    return WEBOTS_WORLD_PATH


def build_webots_launch_info(seed: int = 0, max_ticks: int = 120) -> dict[str, Any]:
    executable = _find_webots_executable()
    command = None
    if executable:
        command = [executable, "--mode=fast", str(WEBOTS_WORLD_PATH)]
    return {
        "app": "Industrial Robot Arm Graph",
        "world": str(WEBOTS_WORLD_PATH),
        "controller": "abb_irb_4600_controller",
        "seed": seed,
        "max_ticks": max_ticks,
        "webots_executable": executable,
        "command": command,
        "claim": "Webots graph-control demonstration only; no real robot safety claim",
    }


def run_webots_app(seed: int = 0, max_ticks: int = 120) -> dict[str, Any]:
    """Report whether the shipped Webots app can be launched locally."""

    if not WEBOTS_WORLD_PATH.exists():
        return {
            "status": "skipped",
            "reason": "missing_webots_world",
            "world": str(WEBOTS_WORLD_PATH),
        }
    info = build_webots_launch_info(seed=seed, max_ticks=max_ticks)
    if info["webots_executable"] is None:
        return {
            "status": "skipped",
            "reason": "missing_webots_executable",
            **info,
        }
    return {
        "status": "available",
        "reason": "webots_executable_found",
        **info,
    }


def _read_trace(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


if __name__ == "__main__":
    print(json.dumps(run_webots_app(), indent=2, sort_keys=True))
