"""Diagnostics helpers for Maze Graph Memory Bot Webots runs."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any


def _round(value: float, digits: int = 5) -> float:
    return round(float(value), digits)


def _selected_candidate(decision: Any) -> Any | None:
    for candidate in decision.candidates:
        if candidate.action_id == decision.selected_action_id:
            return candidate
    return None


def _candidate_rows(decision: Any) -> list[dict[str, Any]]:
    rows = [
        {
            "action_id": candidate.action_id,
            "score": candidate.score,
            "gate": candidate.gate,
            "reason": candidate.reason,
            "command": dict(candidate.command),
            "risk": candidate.risk,
            "predicted_progress": candidate.predicted_progress,
        }
        for candidate in decision.candidates
    ]
    return sorted(rows, key=lambda item: float(item["score"]), reverse=True)


def failure_flags(
    state: Any,
    decision: Any,
    *,
    movement_delta: float,
    contact_streak: int,
    no_progress_streak: int,
    recovery_queue_remaining: int,
) -> dict[str, bool]:
    command = decision.selected_command
    throttle = abs(float(command.get("throttle", 0.0)))
    turn = abs(float(command.get("turn", 0.0)))
    front_blocked = state.front_clearance < 0.08 or state.nearest_clearance < 0.06
    side_clearance_gap = abs(state.left_clearance - state.right_clearance)
    clear_side_margin = max(state.left_clearance, state.right_clearance) - state.nearest_clearance
    wall_hugging = (
        state.nearest_clearance < 0.22
        and side_clearance_gap > 0.015
        and clear_side_margin > 0.015
        and state.front_clearance >= 0.08
    )
    corner_risk = state.front_clearance < 0.18 and state.nearest_clearance < 0.16
    no_progress = (throttle > 0.05 or turn > 0.05) and movement_delta < 0.003
    spin_risk = turn >= 0.55 and throttle <= 0.08
    recovery_active = (
        recovery_queue_remaining > 0
        or str(decision.selected_action_id).startswith("action:recovery_")
    )
    return {
        "front_blocked": front_blocked,
        "wall_hugging": wall_hugging,
        "corner_risk": corner_risk,
        "no_progress": no_progress,
        "spin_risk": spin_risk,
        "contact_streak_active": contact_streak > 0,
        "no_progress_streak_active": no_progress_streak > 0,
        "recovery_active": recovery_active,
    }


def failure_label(flags: dict[str, bool]) -> str:
    for label in (
        "recovery_active",
        "corner_risk",
        "front_blocked",
        "wall_hugging",
        "no_progress_streak_active",
        "no_progress",
        "spin_risk",
        "contact_streak_active",
    ):
        if flags.get(label):
            return label
    return "nominal"


def diagnostic_record(
    *,
    state: Any,
    decision: Any,
    movement_delta: float,
    contact_streak: int,
    no_progress_streak: int,
    recovery_queue_remaining: int,
    emitted_wheel_velocity: dict[str, float],
    navigation_sensor: dict[str, Any] | None = None,
    goal_sensor: dict[str, Any] | None = None,
    learning_outcome: dict[str, Any] | None = None,
    learning_memory: dict[str, Any] | None = None,
) -> dict[str, Any]:
    selected = _selected_candidate(decision)
    flags = failure_flags(
        state,
        decision,
        movement_delta=movement_delta,
        contact_streak=contact_streak,
        no_progress_streak=no_progress_streak,
        recovery_queue_remaining=recovery_queue_remaining,
    )
    return {
        "schema": "cgf.maze_graph_memory.failure_diagnostics.v1",
        "tick": state.tick,
        "failure_label": failure_label(flags),
        "flags": flags,
        "pose": {
            "x": _round(state.pose[0]),
            "y": _round(state.pose[1]),
            "yaw": _round(state.pose[2]),
        },
        "goal": {"x": _round(state.goal[0]), "y": _round(state.goal[1])},
        "distance_to_goal": _round(state.distance_to_goal),
        "goal_bearing_error": _round(state.goal_bearing_error),
        "clearance": {
            "front": _round(state.front_clearance),
            "left": _round(state.left_clearance),
            "right": _round(state.right_clearance),
            "nearest": _round(state.nearest_clearance),
        },
        "movement_delta": _round(movement_delta),
        "contact_streak": contact_streak,
        "no_progress_streak": no_progress_streak,
        "recovery_queue_remaining": recovery_queue_remaining,
        "selected": {
            "action_id": decision.selected_action_id,
            "command": dict(decision.selected_command),
            "score": None if selected is None else selected.score,
            "gate": None if selected is None else selected.gate,
            "reason": None if selected is None else selected.reason,
        },
        "emitted_wheel_velocity": dict(emitted_wheel_velocity),
        "navigation_sensor": navigation_sensor,
        "goal_sensor": goal_sensor,
        "learning_outcome": learning_outcome,
        "learning_memory": learning_memory,
        "candidate_ranking": _candidate_rows(decision),
        "decision_path": tuple(decision.decision_path),
        "raw_state": asdict(state),
    }


def is_failure_point(record: dict[str, Any]) -> bool:
    return record["failure_label"] != "nominal"
