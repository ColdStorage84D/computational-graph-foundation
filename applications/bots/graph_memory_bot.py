"""Generalized Graph Memory Bot example for CGF applications.

This module is a dependency-free bot/controller skeleton. It is not a MazeBot
or a simulator adapter. It shows the reusable CGF action loop:

input state -> candidate actions -> predicted outcomes -> gate -> selected
action -> trace -> observed outcome -> graph runtime memory update.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
import random
from typing import Any

from provisional_route_growth import run_route_growth_demo


def _clamp(value: float, low: float = -1.0, high: float = 1.0) -> float:
    return max(low, min(high, float(value)))


@dataclass(frozen=True)
class BotInputState:
    input_id: str
    tick: int
    kind: str
    signal_quality: float
    obstacle_risk: float
    uncertainty: float
    goal_pressure: float
    pattern_key: str


@dataclass(frozen=True)
class PredictedOutcome:
    progress: float
    risk: float
    uncertainty_after: float
    expected_error: float
    rationale: str


@dataclass(frozen=True)
class CandidateAction:
    action_id: str
    label: str
    strategy: str
    command: dict[str, float]
    base_score: float
    predicted_outcome: PredictedOutcome


@dataclass(frozen=True)
class GateResult:
    outcome: str
    reason: str
    score_multiplier: float
    blocked: bool


@dataclass(frozen=True)
class CandidateEvaluation:
    candidate: CandidateAction
    gate: GateResult
    memory_before: float
    score_before_gate: float
    score_after_gate: float


@dataclass(frozen=True)
class ObservedOutcome:
    observed_progress: float
    observed_risk: float
    observed_uncertainty: float
    prediction_error: float


@dataclass(frozen=True)
class MemoryUpdate:
    memory_key: str
    before: float
    after: float
    reason: str


@dataclass(frozen=True)
class GraphMemoryTraceStep:
    trace_id: str
    input_state: BotInputState
    candidates: tuple[CandidateEvaluation, ...]
    selected_action_id: str
    selected_command: dict[str, float]
    rejected_action_ids: tuple[str, ...]
    observed_outcome: ObservedOutcome
    memory_updates: tuple[MemoryUpdate, ...]
    decision_path: tuple[str, ...]


@dataclass(frozen=True)
class GraphMemoryBotRun:
    run_id: str
    steps: tuple[GraphMemoryTraceStep, ...]
    final_memory: dict[str, float]
    route_growth_summary: dict[str, Any]
    claim_boundary: tuple[str, ...] = (
        "graph-action and memory skeleton only",
        "no autonomous bot performance claim",
        "no guaranteed maze solving",
        "no robotics benchmark",
        "no production safety claim",
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class GraphMemoryBot:
    seed: int = 0
    memory: dict[str, float] = field(default_factory=lambda: {
        "strategy:advance": 0.0,
        "strategy:probe": 0.0,
        "strategy:reroute": 0.0,
        "strategy:hold_review": 0.0,
    })
    trace: list[GraphMemoryTraceStep] = field(default_factory=list)

    def input_state(self, tick: int) -> BotInputState:
        rng = random.Random(self.seed + tick)
        return BotInputState(
            input_id=f"input:generic:{tick}",
            tick=tick,
            kind="generic_task_state",
            signal_quality=round(0.78 + 0.08 * rng.random(), 3),
            obstacle_risk=round(0.86 if tick == 0 else 0.44 + 0.08 * rng.random(), 3),
            uncertainty=round(0.42 if tick == 0 else 0.30 + 0.12 * rng.random(), 3),
            goal_pressure=round(0.72 + 0.08 * rng.random(), 3),
            pattern_key="unknown:c" if tick == 1 else "known:generic",
        )

    def candidate_actions(self, state: BotInputState) -> tuple[CandidateAction, ...]:
        advance_risk = _clamp(state.obstacle_risk + 0.08, 0.0, 1.0)
        probe_risk = _clamp(state.obstacle_risk - 0.34, 0.0, 1.0)
        reroute_risk = _clamp(state.obstacle_risk - 0.48, 0.0, 1.0)
        return (
            CandidateAction(
                action_id="action:advance",
                label="Advance toward goal",
                strategy="advance",
                command={"throttle": _clamp(0.78), "turn": _clamp(0.0)},
                base_score=0.55,
                predicted_outcome=PredictedOutcome(
                    progress=_clamp(0.78 * state.goal_pressure, 0.0, 1.0),
                    risk=advance_risk,
                    uncertainty_after=_clamp(state.uncertainty + 0.10, 0.0, 1.0),
                    expected_error=0.22,
                    rationale="fastest progress if the path is clear",
                ),
            ),
            CandidateAction(
                action_id="action:probe",
                label="Probe and correct",
                strategy="probe",
                command={"throttle": _clamp(0.32), "turn": _clamp(0.24)},
                base_score=0.52,
                predicted_outcome=PredictedOutcome(
                    progress=_clamp(0.48 * state.goal_pressure, 0.0, 1.0),
                    risk=probe_risk,
                    uncertainty_after=_clamp(state.uncertainty - 0.08, 0.0, 1.0),
                    expected_error=0.11,
                    rationale="small move to reduce uncertainty before committing",
                ),
            ),
            CandidateAction(
                action_id="action:reroute",
                label="Reroute around risk",
                strategy="reroute",
                command={"throttle": _clamp(0.20), "turn": _clamp(-0.58)},
                base_score=0.45,
                predicted_outcome=PredictedOutcome(
                    progress=_clamp(0.32 * state.goal_pressure, 0.0, 1.0),
                    risk=reroute_risk,
                    uncertainty_after=_clamp(state.uncertainty + 0.02, 0.0, 1.0),
                    expected_error=0.15,
                    rationale="lower immediate risk at the cost of slower progress",
                ),
            ),
            CandidateAction(
                action_id="action:hold_review",
                label="Hold for review",
                strategy="hold_review",
                command={"throttle": 0.0, "turn": 0.0},
                base_score=0.20,
                predicted_outcome=PredictedOutcome(
                    progress=0.0,
                    risk=0.02,
                    uncertainty_after=state.uncertainty,
                    expected_error=0.05,
                    rationale="safe fallback when the graph should not act",
                ),
            ),
        )

    def gate_candidate(self, state: BotInputState, candidate: CandidateAction) -> GateResult:
        if candidate.strategy == "advance" and candidate.predicted_outcome.risk >= 0.80:
            return GateResult(
                outcome="block",
                reason="predicted_risk_above_limit",
                score_multiplier=0.0,
                blocked=True,
            )
        if candidate.strategy == "reroute" and state.uncertainty >= 0.35:
            return GateResult(
                outcome="downgrade",
                reason="reroute_uncertainty_requires_review_margin",
                score_multiplier=0.70,
                blocked=False,
            )
        if candidate.strategy == "hold_review" and state.goal_pressure < 0.40:
            return GateResult(
                outcome="allow",
                reason="low_goal_pressure_safe_hold",
                score_multiplier=1.0,
                blocked=False,
            )
        return GateResult(
            outcome="allow",
            reason="within_declared_limits",
            score_multiplier=1.0,
            blocked=False,
        )

    def evaluate_candidates(self, state: BotInputState) -> tuple[CandidateEvaluation, ...]:
        evaluations: list[CandidateEvaluation] = []
        for candidate in self.candidate_actions(state):
            key = f"strategy:{candidate.strategy}"
            memory_before = self.memory.get(key, 0.0)
            prediction = candidate.predicted_outcome
            score_before_gate = (
                candidate.base_score
                + 0.80 * prediction.progress
                - 0.60 * prediction.risk
                - 0.70 * prediction.expected_error
                - 0.10 * state.uncertainty
                + 0.35 * memory_before
            )
            gate = self.gate_candidate(state, candidate)
            score_after_gate = -1.0 if gate.blocked else score_before_gate * gate.score_multiplier
            evaluations.append(
                CandidateEvaluation(
                    candidate=candidate,
                    gate=gate,
                    memory_before=round(memory_before, 4),
                    score_before_gate=round(score_before_gate, 4),
                    score_after_gate=round(score_after_gate, 4),
                )
            )
        return tuple(evaluations)

    def observe_outcome(self, state: BotInputState, selected: CandidateAction) -> ObservedOutcome:
        predicted = selected.predicted_outcome
        drag = 0.07 if selected.strategy == "probe" else 0.13
        if selected.strategy == "hold_review":
            drag = 0.0
        observed_progress = _clamp(predicted.progress - drag, 0.0, 1.0)
        observed_risk = _clamp(predicted.risk + (0.04 if state.obstacle_risk > 0.5 else -0.02), 0.0, 1.0)
        observed_uncertainty = _clamp(predicted.uncertainty_after + 0.03, 0.0, 1.0)
        prediction_error = (
            abs(predicted.progress - observed_progress)
            + abs(predicted.risk - observed_risk)
            + abs(predicted.uncertainty_after - observed_uncertainty)
        ) / 3.0
        return ObservedOutcome(
            observed_progress=round(observed_progress, 4),
            observed_risk=round(observed_risk, 4),
            observed_uncertainty=round(observed_uncertainty, 4),
            prediction_error=round(prediction_error, 4),
        )

    def update_memory(self, selected: CandidateAction, outcome: ObservedOutcome) -> tuple[MemoryUpdate, ...]:
        key = f"strategy:{selected.strategy}"
        before = self.memory.get(key, 0.0)
        if outcome.prediction_error <= 0.10 and outcome.observed_progress > 0.0:
            after = _clamp(before + 0.22, -1.0, 1.0)
            reason = "prediction_error_low_and_progress_observed"
        elif outcome.observed_progress <= 0.0:
            after = _clamp(before - 0.18, -1.0, 1.0)
            reason = "no_progress_observed"
        else:
            after = _clamp(before - 0.08, -1.0, 1.0)
            reason = "prediction_error_above_memory_margin"
        self.memory[key] = round(after, 4)
        return (MemoryUpdate(memory_key=key, before=round(before, 4), after=round(after, 4), reason=reason),)

    def run_tick(self, tick: int) -> GraphMemoryTraceStep:
        state = self.input_state(tick)
        evaluations = self.evaluate_candidates(state)
        selected_eval = max(evaluations, key=lambda item: item.score_after_gate)
        selected = selected_eval.candidate
        rejected_ids = tuple(
            item.candidate.action_id for item in evaluations if item.candidate.action_id != selected.action_id
        )
        observed = self.observe_outcome(state, selected)
        updates = self.update_memory(selected, observed)
        step = GraphMemoryTraceStep(
            trace_id=f"trace:graph-memory-bot:{tick}",
            input_state=state,
            candidates=evaluations,
            selected_action_id=selected.action_id,
            selected_command=dict(selected.command),
            rejected_action_ids=rejected_ids,
            observed_outcome=observed,
            memory_updates=updates,
            decision_path=(
                "input / sensor state",
                f"{len(evaluations)} candidate actions",
                "predicted outcomes",
                "safety / policy gate",
                selected.action_id,
                "observed outcome",
                "graph runtime memory update",
            ),
        )
        self.trace.append(step)
        return step

    def run(self, *, max_ticks: int = 3) -> GraphMemoryBotRun:
        for tick in range(max_ticks):
            self.run_tick(tick)
        route_growth = run_route_growth_demo()
        return GraphMemoryBotRun(
            run_id=f"graph-memory-bot:seed:{self.seed}",
            steps=tuple(self.trace),
            final_memory=dict(self.memory),
            route_growth_summary={
                "provisional_route_id": route_growth.provisional_route_id,
                "candidate_count": route_growth.candidate_count,
                "promoted_route": route_growth.promoted_route,
                "route_after_rollback": route_growth.route_after_rollback,
                "trace": list(route_growth.trace),
            },
        )


def build_graph_memory_bot(seed: int = 0) -> GraphMemoryBot:
    return GraphMemoryBot(seed=seed)


def run_graph_memory_bot_demo(seed: int = 0, max_ticks: int = 3) -> GraphMemoryBotRun:
    return build_graph_memory_bot(seed=seed).run(max_ticks=max_ticks)


if __name__ == "__main__":
    print(json.dumps(run_graph_memory_bot_demo().to_dict(), indent=2))
