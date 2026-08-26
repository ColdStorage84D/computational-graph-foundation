"""Robot topology and trace example for CGF bot applications."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TopologyNode:
    node_id: str
    node_type: str
    features: dict[str, Any]


@dataclass(frozen=True)
class TopologyEdge:
    source: str
    edge_type: str
    target: str


def build_robot_topology() -> dict[str, Any]:
    nodes = [
        TopologyNode("sensor:range", "sensor", {"kind": "range"}),
        TopologyNode("goal:hold_safe", "goal", {"target": "safe_idle"}),
        TopologyNode("goal:move", "goal", {"target": "bounded_motion"}),
        TopologyNode("action:hold", "action_candidate", {"command": "hold"}),
        TopologyNode("action:move", "action_candidate", {"command": "bounded_move"}),
        TopologyNode("actuator:left", "actuator", {"kind": "wheel"}),
        TopologyNode("actuator:right", "actuator", {"kind": "wheel"}),
        TopologyNode("limit:speed", "safety_limit", {"max": 1.0}),
    ]
    edges = [
        TopologyEdge("sensor:range", "observes", "action:move"),
        TopologyEdge("goal:hold_safe", "supports", "action:hold"),
        TopologyEdge("goal:move", "supports", "action:move"),
        TopologyEdge("action:hold", "commands", "actuator:left"),
        TopologyEdge("action:hold", "commands", "actuator:right"),
        TopologyEdge("action:move", "commands", "actuator:left"),
        TopologyEdge("action:move", "commands", "actuator:right"),
        TopologyEdge("limit:speed", "constrains", "actuator:left"),
        TopologyEdge("limit:speed", "constrains", "actuator:right"),
    ]
    return {
        "graph_id": "robot_topology_example",
        "nodes": [node.__dict__ for node in nodes],
        "edges": [edge.__dict__ for edge in edges],
    }


def build_trace_step(
    *,
    tick: int,
    selected_action: str,
    gate_outcome: str,
    gate_reason: str,
    emitted_command: dict[str, float],
) -> dict[str, Any]:
    return {
        "trace_id": f"trace:robot:{tick}",
        "tick": int(tick),
        "selected_action": selected_action,
        "safety_gate": {
            "outcome": gate_outcome,
            "reason": gate_reason,
        },
        "emitted_command": dict(emitted_command),
        "evidence_paths": [
            ["goal:move", "supports", selected_action, "commands", "actuator:left"],
            ["goal:move", "supports", selected_action, "commands", "actuator:right"],
            ["limit:speed", "constrains", "actuator:left"],
            ["limit:speed", "constrains", "actuator:right"],
        ],
        "outcome": {
            "blocked_before_emit": gate_outcome != "allow",
            "collision": False,
            "limit_violation": gate_outcome != "allow",
        },
    }


def validate_trace_step(trace: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in ("trace_id", "tick", "selected_action", "safety_gate", "evidence_paths", "outcome"):
        if key not in trace:
            errors.append(f"missing {key}")
    selected = str(trace.get("selected_action", ""))
    evidence_text = " ".join(" ".join(str(part) for part in path) for path in trace.get("evidence_paths", []))
    if selected and selected not in evidence_text:
        errors.append("selected action must appear in evidence paths")
    gate = trace.get("safety_gate", {})
    if gate.get("outcome") != "allow" and trace.get("outcome", {}).get("blocked_before_emit") is not True:
        errors.append("blocked gate must be visible as blocked_before_emit")
    if gate.get("outcome") == "allow" and trace.get("outcome", {}).get("blocked_before_emit") is True:
        errors.append("allowed action must not be marked blocked")
    return errors
