"""Import-safe maze policy for the Webots Maze Graph Memory Bot.

The controller uses this small graph policy to turn sensor-derived maze state
into candidate wheel commands. It is deliberately local to the Webots app: the
general Graph Memory Bot remains reusable, while this module adapts the pattern
to a Pioneer-style maze world.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import math
from typing import Any, Mapping


GOAL_ATTRACTOR_RADIUS = 2.60
GOAL_HOLD_RADIUS = 0.42
DEFAULT_SENSOR_GOAL = (0.0, 0.0)


def _clamp(value: float, low: float = -1.0, high: float = 1.0) -> float:
    return max(low, min(high, float(value)))


def _wrap_angle(value: float) -> float:
    return (float(value) + math.pi) % (2.0 * math.pi) - math.pi


@dataclass(frozen=True)
class MazeSensorState:
    tick: int
    pose: tuple[float, float, float]
    goal: tuple[float, float]
    distance_to_goal: float
    goal_bearing_error: float
    front_clearance: float
    left_clearance: float
    right_clearance: float
    nearest_clearance: float
    spin_streak: int = 0


@dataclass(frozen=True)
class MazeCandidate:
    action_id: str
    label: str
    command: dict[str, float]
    predicted_progress: float
    risk: float
    gate: str
    reason: str
    score: float


@dataclass(frozen=True)
class MazeDecision:
    selected_action_id: str
    selected_command: dict[str, float]
    candidates: tuple[MazeCandidate, ...]
    rejected_action_ids: tuple[str, ...]
    decision_path: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class MazeActionOutcomeMemory:
    """In-run and persisted sensor-context memory for Maze action outcomes."""

    def __init__(self, *, outcomes: dict[str, Any] | None = None) -> None:
        self.outcomes: dict[str, dict[str, dict[str, Any]]] = {}
        if outcomes:
            for key, action_rows in outcomes.items():
                if not isinstance(action_rows, dict):
                    continue
                self.outcomes[str(key)] = {}
                for action_id, row in action_rows.items():
                    if not isinstance(row, dict):
                        continue
                    self.outcomes[str(key)][str(action_id)] = {
                        "attempts": int(row.get("attempts", 0)),
                        "successes": int(row.get("successes", 0)),
                        "failures": int(row.get("failures", 0)),
                        "neutral": int(row.get("neutral", 0)),
                        "last_reason": str(row.get("last_reason", "")),
                    }

    @staticmethod
    def _band(value: float, cuts: tuple[float, ...], labels: tuple[str, ...]) -> str:
        for cut, label in zip(cuts, labels):
            if value <= cut:
                return label
        return labels[-1]

    @classmethod
    def context_key(cls, state: MazeSensorState) -> str:
        """Build a memory key from live sensors only, not from a maze map."""

        distance_band = cls._band(
            state.distance_to_goal,
            (GOAL_HOLD_RADIUS, GOAL_ATTRACTOR_RADIUS, 7.5, 14.0),
            ("goal", "near", "mid", "far", "very_far"),
        )
        bearing = state.goal_bearing_error
        if abs(bearing) <= 0.35:
            bearing_band = "ahead"
        elif bearing > 2.35 or bearing < -2.35:
            bearing_band = "behind"
        elif bearing > 0.0:
            bearing_band = "left"
        else:
            bearing_band = "right"

        def clearance_band(value: float) -> str:
            return cls._band(value, (0.08, 0.18, 0.36, 0.66), ("blocked", "tight", "near", "open", "wide"))

        spin_band = "spinning" if state.spin_streak >= 5 else "stable"
        return (
            "sensor:"
            f"goal:{distance_band}:{bearing_band}:"
            f"front:{clearance_band(state.front_clearance)}:"
            f"left:{clearance_band(state.left_clearance)}:"
            f"right:{clearance_band(state.right_clearance)}:"
            f"nearest:{clearance_band(state.nearest_clearance)}:"
            f"{spin_band}"
        )

    def record_outcome(
        self,
        *,
        context_key: str,
        action_id: str,
        movement_delta: float,
        previous_goal_distance: float,
        current_goal_distance: float,
        contact_active: bool,
        no_progress: bool,
    ) -> dict[str, Any]:
        action_id = str(action_id)
        progress_delta = float(previous_goal_distance) - float(current_goal_distance)
        ignored = action_id == "action:hold" or action_id.startswith("action:recovery_")
        no_effect = float(movement_delta) < 0.003
        worsened = progress_delta < -0.050
        success = progress_delta > 0.035 and float(movement_delta) >= 0.010 and not contact_active
        failure = bool(contact_active or no_progress or no_effect or worsened)
        if ignored:
            status = "ignored"
            reason = "non_learning_action"
        elif failure:
            status = "failure"
            if contact_active:
                reason = "contact_after_action"
            elif no_progress or no_effect:
                reason = "no_effect_after_action"
            else:
                reason = "distance_to_goal_worsened"
        elif success:
            status = "success"
            reason = "distance_to_goal_improved"
        else:
            status = "neutral"
            reason = "weak_or_ambiguous_effect"

        key = str(context_key)
        if not ignored:
            row = self.outcomes.setdefault(key, {}).setdefault(
                action_id,
                {"attempts": 0, "successes": 0, "failures": 0, "neutral": 0, "last_reason": ""},
            )
            row["attempts"] = int(row.get("attempts", 0)) + 1
            counter = "successes" if status == "success" else ("failures" if status == "failure" else "neutral")
            row[counter] = int(row.get(counter, 0)) + 1
            row["last_reason"] = reason

        return {
            "key": key,
            "action_id": action_id,
            "status": status,
            "reason": reason,
            "movement_delta": round(float(movement_delta), 5),
            "progress_delta": round(progress_delta, 5),
            "biases": self.biases_for(context_key=key),
        }

    def biases_for(self, *, context_key: str) -> dict[str, float]:
        action_rows = self.outcomes.get(str(context_key), {})
        biases: dict[str, float] = {}
        repeated_failures = 0
        for action_id, row in action_rows.items():
            failures = int(row.get("failures", 0))
            successes = int(row.get("successes", 0))
            if failures <= 0 and successes <= 0:
                continue
            repeated_failures += failures
            failure_penalty = 0.18 if failures == 1 else min(1.80, 0.44 * failures)
            success_bonus = min(0.50, 0.12 * successes)
            bias = success_bonus - failure_penalty
            if abs(bias) > 0.0001:
                biases[action_id] = round(bias, 4)

        if repeated_failures >= 2:
            biases["action:reverse"] = round(biases.get("action:reverse", 0.0) + 0.22, 4)
            biases["action:arc_left"] = round(biases.get("action:arc_left", 0.0) + 0.16, 4)
            biases["action:arc_right"] = round(biases.get("action:arc_right", 0.0) + 0.16, 4)
            biases["action:escape_left"] = round(biases.get("action:escape_left", 0.0) + 0.12, 4)
            biases["action:escape_right"] = round(biases.get("action:escape_right", 0.0) + 0.12, 4)
        return biases

    def biases_for_state(self, state: MazeSensorState) -> dict[str, float]:
        return self.biases_for(context_key=self.context_key(state))

    def summary_for(self, *, context_key: str) -> dict[str, Any]:
        key = str(context_key)
        return {
            "key": key,
            "actions": self.outcomes.get(key, {}),
            "biases": self.biases_for(context_key=key),
        }

    def summary_for_state(self, state: MazeSensorState) -> dict[str, Any]:
        return self.summary_for(context_key=self.context_key(state))

    def to_dict(self) -> dict[str, Any]:
        return {"outcomes": self.outcomes}

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "MazeActionOutcomeMemory":
        return cls(outcomes=dict(payload.get("outcomes", {})))


def recovery_decision(
    state: MazeSensorState,
    *,
    action_id: str,
    command: dict[str, float],
    reason: str,
) -> MazeDecision:
    selected = _candidate(
        action_id,
        "Contact recovery command",
        command.get("throttle", 0.0),
        command.get("turn", 0.0),
        0.0,
        1.0 - state.nearest_clearance,
        "allow",
        reason,
        2.0,
    )
    rejected = tuple(
        item.action_id for item in evaluate_maze_candidates(state)
        if item.action_id != selected.action_id
    )
    return MazeDecision(
        selected_action_id=selected.action_id,
        selected_command=dict(selected.command),
        candidates=(selected, *evaluate_maze_candidates(state)),
        rejected_action_ids=rejected,
        decision_path=(
            "webots sensors",
            "gps no-progress / contact detection",
            "recovery gate",
            selected.action_id,
            "wheel command",
            "trace",
        ),
    )


def tight_corner_trap(state: MazeSensorState) -> bool:
    return (
        state.front_clearance < 0.12
        and state.nearest_clearance < 0.10
        and max(state.left_clearance, state.right_clearance) < 0.13
    )


def recovery_turn_direction(state: MazeSensorState) -> float:
    if tight_corner_trap(state):
        return 1.0 if state.goal_bearing_error >= 0.0 else -1.0
    return -1.0 if state.right_clearance >= state.left_clearance else 1.0


def build_recovery_plan(state: MazeSensorState) -> list[dict[str, object]]:
    turn_direction = recovery_turn_direction(state)
    if tight_corner_trap(state):
        return (
            [{"action_id": "action:recovery_deep_reverse", "command": {"throttle": -0.38, "turn": 0.0}, "reason": "deep_reverse_from_tight_corner"}] * 28
            + [{"action_id": "action:recovery_rotate_clear", "command": {"throttle": 0.0, "turn": 0.70 * turn_direction}, "reason": "rotate_toward_clearer_side_after_corner_reverse"}] * 18
        )
    return (
        [{"action_id": "action:recovery_reverse", "command": {"throttle": -0.36, "turn": 0.0}, "reason": "back_out_from_contact"}] * 14
        + [{"action_id": "action:recovery_rotate_clear", "command": {"throttle": 0.0, "turn": 0.70 * turn_direction}, "reason": "rotate_toward_clearer_side"}] * 12
        + [{"action_id": "action:recovery_probe_forward", "command": {"throttle": 0.24, "turn": 0.12 * turn_direction}, "reason": "probe_after_contact_recovery"}] * 8
    )


def guard_recovery_item(state: MazeSensorState, item: Mapping[str, object]) -> dict[str, object]:
    action_id = str(item.get("action_id", ""))
    front_still_blocked = state.front_clearance < 0.14 or state.nearest_clearance < 0.10
    if action_id == "action:recovery_probe_forward" and front_still_blocked:
        return {
            "action_id": "action:recovery_probe_blocked_reverse",
            "command": {"throttle": -0.34, "turn": 0.0},
            "reason": "probe_blocked_by_lidar_reverse_again",
        }
    return dict(item)


def goal_bearing_error(pose: tuple[float, float, float], goal: tuple[float, float]) -> float:
    x, y, yaw = pose
    bearing = math.atan2(goal[1] - y, goal[0] - x)
    return _wrap_angle(bearing - yaw)


def _distance_to_point(pose: tuple[float, float, float], point: tuple[float, float]) -> float:
    return math.hypot(point[0] - pose[0], point[1] - pose[1])


def goal_sensor_reading(state: MazeSensorState) -> dict[str, Any]:
    distance = max(0.0, float(state.distance_to_goal))
    attractor_span = max(0.001, GOAL_ATTRACTOR_RADIUS - GOAL_HOLD_RADIUS)
    attractor_strength = _clamp(1.0 - max(0.0, distance - GOAL_HOLD_RADIUS) / attractor_span, 0.0, 1.0)
    return {
        "target": {"x": state.goal[0], "y": state.goal[1]},
        "distance": round(distance, 5),
        "bearing_error": round(state.goal_bearing_error, 5),
        "alignment": round(max(0.0, math.cos(state.goal_bearing_error)), 5),
        "attractor_strength": round(attractor_strength, 5),
        "inside_attractor_radius": distance <= GOAL_ATTRACTOR_RADIUS,
        "inside_goal_radius": distance <= GOAL_HOLD_RADIUS,
    }


def navigation_sensor_record(state: MazeSensorState) -> dict[str, Any]:
    return {
        "source": "gps_compass_lidar_goal_marker",
        "target": {"x": round(float(state.goal[0]), 5), "y": round(float(state.goal[1]), 5)},
        "distance_to_goal": round(float(state.distance_to_goal), 5),
        "goal_bearing_error": round(float(state.goal_bearing_error), 5),
        "clearance": {
            "front": round(float(state.front_clearance), 5),
            "left": round(float(state.left_clearance), 5),
            "right": round(float(state.right_clearance), 5),
            "nearest": round(float(state.nearest_clearance), 5),
        },
        "memory_context_key": MazeActionOutcomeMemory.context_key(state),
        "maze_map_known": False,
    }


def build_sensor_state(
    *,
    tick: int,
    pose: tuple[float, float, float],
    goal: tuple[float, float] = DEFAULT_SENSOR_GOAL,
    clearances: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0),
    spin_streak: int = 0,
) -> MazeSensorState:
    x, y, _yaw = pose
    front, left, right, nearest = (_clamp(item, 0.0, 1.0) for item in clearances)
    return MazeSensorState(
        tick=tick,
        pose=pose,
        goal=goal,
        distance_to_goal=math.hypot(goal[0] - x, goal[1] - y),
        goal_bearing_error=goal_bearing_error(pose, goal),
        front_clearance=front,
        left_clearance=left,
        right_clearance=right,
        nearest_clearance=nearest,
        spin_streak=spin_streak,
    )


def _candidate(
    action_id: str,
    label: str,
    throttle: float,
    turn: float,
    predicted_progress: float,
    risk: float,
    gate: str,
    reason: str,
    score: float,
) -> MazeCandidate:
    return MazeCandidate(
        action_id=action_id,
        label=label,
        command={"throttle": round(_clamp(throttle), 4), "turn": round(_clamp(turn), 4)},
        predicted_progress=round(_clamp(predicted_progress, 0.0, 1.0), 4),
        risk=round(_clamp(risk, 0.0, 1.0), 4),
        gate=gate,
        reason=reason,
        score=round(score, 4) if math.isfinite(score) else -1.0,
    )


def _apply_memory_biases(
    candidates: tuple[MazeCandidate, ...],
    memory_biases: Mapping[str, float] | None,
) -> tuple[MazeCandidate, ...]:
    if not memory_biases:
        return candidates
    adjusted: list[MazeCandidate] = []
    for candidate in candidates:
        bias = float(memory_biases.get(candidate.action_id, 0.0))
        if abs(bias) <= 0.0001:
            adjusted.append(candidate)
            continue
        reason = f"{candidate.reason}; memory_bias={bias:+.2f}"
        adjusted.append(replace(candidate, score=round(candidate.score + bias, 4), reason=reason))
    return tuple(adjusted)


def evaluate_maze_candidates(
    state: MazeSensorState,
    memory_biases: Mapping[str, float] | None = None,
) -> tuple[MazeCandidate, ...]:
    error = state.goal_bearing_error
    abs_error = abs(error)
    front = state.front_clearance
    left = state.left_clearance
    right = state.right_clearance
    nearest = state.nearest_clearance
    goal_alignment = max(0.0, math.cos(error))
    turn_to_goal = _clamp(error / 5.0, -0.16, 0.16)
    obstacle_risk = 1.0 - min(front, nearest)
    blocked_front = front < 0.08 or nearest < 0.06
    reverse_needed = front < 0.05 or nearest < 0.05
    clear_side = "left" if left >= right else "right"
    side_clearance_gap = abs(left - right)
    clear_side_margin = max(left, right) - nearest
    wall_hugging = nearest < 0.22 and side_clearance_gap > 0.015 and clear_side_margin > 0.015
    corner_risk = front < 0.18 and nearest < 0.16
    side_escape_needed = nearest < 0.18 and side_clearance_gap > 0.015 and clear_side_margin > 0.015
    goal_sensor = goal_sensor_reading(state)
    final_attractor_zone = goal_sensor["inside_attractor_radius"]
    attractor_has_clearance = final_attractor_zone and front > 0.12 and nearest > 0.07
    effective_wall_hugging = False if attractor_has_clearance else wall_hugging
    effective_corner_risk = False if attractor_has_clearance else corner_risk
    effective_side_escape_needed = False if attractor_has_clearance else side_escape_needed
    straight_wall_risk = effective_wall_hugging or effective_corner_risk or effective_side_escape_needed
    alignment_needed = abs_error > 0.80 and front > 0.10
    at_goal = goal_sensor["inside_goal_radius"]

    candidates: list[MazeCandidate] = []

    attractor_throttle = _clamp(0.12 + 0.26 * min(1.0, max(0.0, state.distance_to_goal - GOAL_HOLD_RADIUS)), 0.0, 0.38)
    attractor_turn = _clamp(error / 2.0, -0.52, 0.52)
    candidates.append(
        _candidate(
            "action:goal_attractor",
            "Final goal attractor",
            0.0 if at_goal else attractor_throttle,
            0.0 if at_goal else attractor_turn,
            max(0.0, goal_alignment),
            obstacle_risk,
            "allow" if final_attractor_zone and not blocked_front else "block",
            "inside_final_goal_radius" if at_goal else "final_goal_attractor",
            3.2 if at_goal else (2.15 + 0.55 * goal_sensor["attractor_strength"] + 0.30 * goal_alignment - 0.10 * obstacle_risk),
        )
    )

    advance_blocked = blocked_front or effective_side_escape_needed or (effective_corner_risk and max(left, right) > 0.16)
    advance_downgraded = alignment_needed or straight_wall_risk
    advance_gate = "block" if advance_blocked else ("downgrade" if advance_downgraded else "allow")
    advance_score = (
        -1.0 if advance_blocked
        else -0.35 if alignment_needed
        else -0.20 if straight_wall_risk
        else 0.80 * goal_alignment + 0.45 * front - 0.35 * obstacle_risk
    )
    advance_reason = "front_clearance_below_limit"
    if not blocked_front and (effective_side_escape_needed or effective_corner_risk):
        advance_reason = "side_wall_escape_required"
    elif not blocked_front and effective_wall_hugging:
        advance_reason = "wall_hugging_downgrade"
    elif alignment_needed:
        advance_reason = "align_to_navigation_goal_first"
    elif not blocked_front:
        advance_reason = "goal_aligned_forward_progress"
    candidates.append(
        _candidate(
            "action:advance",
            "Advance with goal correction",
            0.56,
            turn_to_goal,
            goal_alignment * front,
            obstacle_risk,
            advance_gate,
            advance_reason,
            advance_score,
        )
    )

    contact_penalty = 0.50 if reverse_needed else 0.0
    alignment_arc_penalty = 0.0 if straight_wall_risk else (0.35 if alignment_needed else 0.0)
    escape_left_bonus = 0.78 if straight_wall_risk and clear_side == "left" else 0.0
    escape_right_bonus = 0.78 if straight_wall_risk and clear_side == "right" else 0.0
    into_left_wall_penalty = 0.40 if straight_wall_risk and clear_side == "right" else 0.0
    into_right_wall_penalty = 0.40 if straight_wall_risk and clear_side == "left" else 0.0
    left_score = (
        0.45 * left
        + 0.22 * max(0.0, error)
        + 0.20 * front
        - 0.12 * abs_error
        - contact_penalty
        - alignment_arc_penalty
        + escape_left_bonus
        - into_left_wall_penalty
    )
    right_score = (
        0.45 * right
        + 0.22 * max(0.0, -error)
        + 0.20 * front
        - 0.12 * abs_error
        - contact_penalty
        - alignment_arc_penalty
        + escape_right_bonus
        - into_right_wall_penalty
    )
    escape_gate_enabled = straight_wall_risk and not reverse_needed and front > 0.09
    candidates.append(
        _candidate(
            "action:escape_left",
            "Pivot away from a tight right-side wall",
            0.18,
            0.58,
            0.18 * left,
            1.0 - left,
            "allow" if escape_gate_enabled and clear_side == "left" else "block",
            "side_wall_escape_left" if clear_side == "left" else "left_escape_not_clearer",
            1.15 + 0.35 * left if escape_gate_enabled and clear_side == "left" else -1.0,
        )
    )
    candidates.append(
        _candidate(
            "action:escape_right",
            "Pivot away from a tight left-side wall",
            0.18,
            -0.58,
            0.18 * right,
            1.0 - right,
            "allow" if escape_gate_enabled and clear_side == "right" else "block",
            "side_wall_escape_right" if clear_side == "right" else "right_escape_not_clearer",
            1.15 + 0.35 * right if escape_gate_enabled and clear_side == "right" else -1.0,
        )
    )
    candidates.append(
        _candidate(
            "action:arc_left",
            "Arc left around obstacle or toward goal",
            0.34,
            0.30,
            0.35 * left,
            1.0 - left,
            "allow" if left > 0.16 else "downgrade",
            "left_side_clearance_and_goal_bearing",
            left_score,
        )
    )
    candidates.append(
        _candidate(
            "action:arc_right",
            "Arc right around obstacle or toward goal",
            0.34,
            -0.30,
            0.35 * right,
            1.0 - right,
            "allow" if right > 0.16 else "downgrade",
            "right_side_clearance_and_goal_bearing",
            right_score,
        )
    )

    corridor_rotation_blocked = nearest < 0.24 and front > 0.25
    rotate_left_blocked = (state.spin_streak >= 5 and front > 0.30) or corridor_rotation_blocked
    rotate_right_blocked = (state.spin_streak >= 5 and front > 0.30) or corridor_rotation_blocked
    align_bonus = 0.0 if straight_wall_risk else (0.45 if alignment_needed else 0.0)
    rotate_left_escape_bonus = 0.25 if straight_wall_risk and clear_side == "left" else 0.0
    rotate_right_escape_bonus = 0.25 if straight_wall_risk and clear_side == "right" else 0.0
    rotate_left_wall_penalty = 0.45 if straight_wall_risk and clear_side == "right" else 0.0
    rotate_right_wall_penalty = 0.45 if straight_wall_risk and clear_side == "left" else 0.0
    rotate_left_score = (
        -1.0 if rotate_left_blocked
        else 0.34 * left
        + 0.30 * max(0.0, error)
        - 0.18 * front
        + (align_bonus if error > 0.0 else 0.0)
        + rotate_left_escape_bonus
        - rotate_left_wall_penalty
    )
    rotate_right_score = (
        -1.0 if rotate_right_blocked
        else 0.34 * right
        + 0.30 * max(0.0, -error)
        - 0.18 * front
        + (align_bonus if error <= 0.0 else 0.0)
        + rotate_right_escape_bonus
        - rotate_right_wall_penalty
    )
    candidates.append(
        _candidate(
            "action:rotate_left",
            "Rotate left only when translation is unsafe",
            0.06,
            0.62,
            0.05,
            1.0 - left,
            "block" if rotate_left_blocked else "allow",
            "corridor_centering_guard"
            if corridor_rotation_blocked
            else ("anti_spin_guard" if rotate_left_blocked else "reorient_when_left_is_clearer"),
            rotate_left_score,
        )
    )
    candidates.append(
        _candidate(
            "action:rotate_right",
            "Rotate right only when translation is unsafe",
            0.06,
            -0.62,
            0.05,
            1.0 - right,
            "block" if rotate_right_blocked else "allow",
            "corridor_centering_guard"
            if corridor_rotation_blocked
            else ("anti_spin_guard" if rotate_right_blocked else "reorient_when_right_is_clearer"),
            rotate_right_score,
        )
    )

    reverse_score = 0.75 if reverse_needed else (-0.05 if blocked_front else -0.2)
    candidates.append(
        _candidate(
            "action:reverse",
            "Reverse from contact risk",
            -0.24,
            0.0,
            0.0,
            min(1.0, 1.0 - nearest),
            "allow" if blocked_front else "downgrade",
            "escape_contact_or_wedge" if reverse_needed else ("make_space_before_turn" if blocked_front else "reverse_not_needed"),
            reverse_score,
        )
    )

    candidates.append(
        _candidate(
            "action:hold",
            "Hold at goal or when no safe command exists",
            0.0,
            0.0,
            0.0,
            0.0,
            "allow",
            "at_goal" if at_goal else "fallback_only",
            3.4 if at_goal else -0.5,
        )
    )

    return _apply_memory_biases(tuple(candidates), memory_biases)


def select_maze_action(
    state: MazeSensorState,
    memory_biases: Mapping[str, float] | None = None,
) -> MazeDecision:
    candidates = evaluate_maze_candidates(state, memory_biases=memory_biases)
    selectable = [
        item for item in candidates
        if item.gate != "block" and (item.action_id != "action:hold" or item.reason == "at_goal")
    ]
    selected = max(selectable or list(candidates), key=lambda item: item.score)
    rejected = tuple(item.action_id for item in candidates if item.action_id != selected.action_id)
    return MazeDecision(
        selected_action_id=selected.action_id,
        selected_command=dict(selected.command),
        candidates=candidates,
        rejected_action_ids=rejected,
        decision_path=(
            "webots sensors",
            "sensor graph state",
            f"{len(candidates)} candidate actions",
            "clearance / anti-spin gate",
            "action-outcome memory",
            selected.action_id,
            "wheel command",
            "trace",
        ),
    )
