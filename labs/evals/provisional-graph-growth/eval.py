from __future__ import annotations

from dataclasses import dataclass, field


class GrowthRejectedError(ValueError):
    """Raised when a growth action bypasses required evidence or policy."""


class DurableMutationError(ValueError):
    """Raised when provisional structure mutates durable graph state."""


@dataclass(frozen=True)
class Observation:
    observation_id: str
    pattern_key: str
    evidence_ref: str
    surprise: float
    quality: float
    risk: float
    tick: int


@dataclass
class ActivationState:
    potential: float = 0.0
    last_fired_tick: int | None = None
    observations: list[str] = field(default_factory=list)


@dataclass
class ProvisionalGraph:
    graph_id: str
    pattern_key: str
    evidence_refs: list[str]
    activation: float
    status: str = "provisional"
    allowed_runtime_use: tuple[str, ...] = ("explain", "shadow_score", "review")


@dataclass
class CandidateVariant:
    variant_id: str
    graph_id: str
    strategy: str
    affinity: float
    risk: float
    traffic_weight: float
    status: str = "probation"


@dataclass(frozen=True)
class GrowthPatch:
    patch_id: str
    graph_id: str
    proposed_nodes: tuple[str, ...]
    proposed_edges: tuple[tuple[str, str], ...]
    evidence_refs: tuple[str, ...]
    expected_benefit: float
    cost: float
    risk: float
    baseline_error: float
    candidate_error: float
    rollback_policy: str
    probation_min_observations: int
    temporal_shape: str = "stable"
    baseline_comparison_pass: bool = True
    held_out_pass: bool = True
    safety_review_pass: bool = True


class ProvisionalGraphGrowthRuntime:
    """Tiny eval fixture, not a public API."""

    def __init__(
        self,
        *,
        activation_threshold: float = 1.0,
        decay: float = 0.8,
        refractory_ticks: int = 2,
        max_variants: int = 3,
        risk_limit: float = 0.6,
    ) -> None:
        self.activation_threshold = activation_threshold
        self.decay = decay
        self.refractory_ticks = refractory_ticks
        self.max_variants = max_variants
        self.risk_limit = risk_limit
        self.activations: dict[str, ActivationState] = {}
        self.provisional_graphs: dict[str, ProvisionalGraph] = {}
        self.variants: dict[str, CandidateVariant] = {}
        self.durable_nodes = {"source", "verifier", "sink"}
        self.durable_edges = {("source", "verifier"), ("verifier", "sink")}

    def observe(self, observation: Observation) -> ProvisionalGraph | None:
        state = self.activations.setdefault(observation.pattern_key, ActivationState())
        state.potential *= self.decay
        state.potential += observation.surprise * observation.quality
        state.observations.append(observation.evidence_ref)

        if state.last_fired_tick is not None:
            if observation.tick - state.last_fired_tick <= self.refractory_ticks:
                return None

        if state.potential < self.activation_threshold:
            return None

        graph_id = f"provisional:{observation.pattern_key}"
        graph = self.provisional_graphs.get(graph_id)
        if graph is None:
            graph = ProvisionalGraph(
                graph_id=graph_id,
                pattern_key=observation.pattern_key,
                evidence_refs=list(state.observations),
                activation=state.potential,
            )
            self.provisional_graphs[graph_id] = graph
        else:
            graph.evidence_refs = list(dict.fromkeys(graph.evidence_refs + state.observations))
            graph.activation = state.potential

        state.last_fired_tick = observation.tick
        return graph

    def spawn_variants(self, graph: ProvisionalGraph, observations: list[Observation]) -> list[CandidateVariant]:
        if graph.status not in {"provisional", "shadow", "probation"}:
            raise GrowthRejectedError("variants require a provisional graph under review")

        variants: list[CandidateVariant] = []
        strategies = ("new_edge", "new_rule", "new_route", "new_specialist")
        average_quality = sum(obs.quality for obs in observations) / max(1, len(observations))
        average_risk = sum(obs.risk for obs in observations) / max(1, len(observations))

        for strategy in strategies[: self.max_variants]:
            affinity = max(0.0, min(1.0, average_quality - 0.05 * len(variants)))
            risk = min(1.0, average_risk + 0.1 * len(variants))
            status = "quarantine" if risk > self.risk_limit else "probation"
            traffic_weight = 0.0 if status == "quarantine" else round(1.0 / self.max_variants, 3)
            variant = CandidateVariant(
                variant_id=f"{graph.graph_id}:{strategy}",
                graph_id=graph.graph_id,
                strategy=strategy,
                affinity=affinity,
                risk=risk,
                traffic_weight=traffic_weight,
                status=status,
            )
            self.variants[variant.variant_id] = variant
            variants.append(variant)
        return variants

    def stability_guard(self, observations: list[Observation]) -> dict[str, object]:
        if not observations:
            return {"temporal_shape": "empty", "accepted": False, "reason": "no_observations"}

        ticks = sorted({obs.tick for obs in observations})
        span = ticks[-1] - ticks[0] if len(ticks) > 1 else 0
        average_quality = sum(obs.quality for obs in observations) / len(observations)

        if len(observations) < 2:
            return {"temporal_shape": "one_off", "accepted": False, "reason": "insufficient_recurrence"}
        if span <= 1 and len(observations) >= 2:
            return {"temporal_shape": "burst", "accepted": False, "reason": "burst_pattern"}
        if average_quality < 0.5:
            return {"temporal_shape": "unstable", "accepted": False, "reason": "low_quality"}
        return {"temporal_shape": "stable", "accepted": True, "reason": "recurring_stable_support"}

    def shadow_score(self, variant: CandidateVariant, observation: Observation) -> dict[str, object]:
        score = max(0.0, min(1.0, variant.affinity * observation.quality - variant.risk))
        return {
            "variant_id": variant.variant_id,
            "score": score,
            "authority": "shadow_only",
            "can_commit": False,
            "evidence_ref": observation.evidence_ref,
        }

    def retire_variants(self, *, min_affinity: float = 0.35, max_risk: float | None = None) -> list[str]:
        retired: list[str] = []
        risk_limit = self.risk_limit if max_risk is None else max_risk
        for variant in self.variants.values():
            if variant.affinity < min_affinity or variant.risk > risk_limit:
                variant.status = "retired"
                variant.traffic_weight = 0.0
                retired.append(variant.variant_id)
        return retired

    def make_growth_patch(
        self,
        variant: CandidateVariant,
        evidence_refs: list[str],
        *,
        temporal_shape: str = "stable",
        baseline_comparison_pass: bool = True,
        held_out_pass: bool = True,
        safety_review_pass: bool = True,
    ) -> GrowthPatch:
        if not evidence_refs:
            raise GrowthRejectedError("growth patch requires evidence refs")
        if variant.status != "probation":
            raise GrowthRejectedError("only probation variants can produce growth patches")
        return GrowthPatch(
            patch_id=f"patch:{variant.variant_id}",
            graph_id=variant.graph_id,
            proposed_nodes=(f"node:{variant.strategy}",),
            proposed_edges=(("source", f"node:{variant.strategy}"), (f"node:{variant.strategy}", "verifier")),
            evidence_refs=tuple(evidence_refs),
            expected_benefit=variant.affinity,
            cost=0.15,
            risk=variant.risk,
            baseline_error=0.4,
            candidate_error=max(0.0, 0.4 - 0.25 * variant.affinity),
            rollback_policy="quality_below_baseline",
            probation_min_observations=10,
            temporal_shape=temporal_shape,
            baseline_comparison_pass=baseline_comparison_pass,
            held_out_pass=held_out_pass,
            safety_review_pass=safety_review_pass,
        )

    def should_promote(self, patch: GrowthPatch) -> bool:
        if not patch.evidence_refs:
            return False
        if not patch.rollback_policy:
            return False
        if patch.temporal_shape != "stable":
            return False
        if not (patch.baseline_comparison_pass and patch.held_out_pass and patch.safety_review_pass):
            return False
        if patch.risk > self.risk_limit:
            return False
        current = patch.baseline_error
        candidate = patch.candidate_error + patch.cost + patch.risk
        return current > candidate

    def apply_patch(self, patch: GrowthPatch, *, promoted: bool) -> None:
        if not promoted:
            raise DurableMutationError("durable graph can change only after promotion")
        if not self.should_promote(patch):
            raise GrowthRejectedError("patch failed promotion criteria")
        self.durable_nodes.update(patch.proposed_nodes)
        self.durable_edges.update(patch.proposed_edges)
        graph = self.provisional_graphs.get(patch.graph_id)
        if graph is not None:
            graph.status = "promoted"

    def durable_snapshot(self) -> dict[str, object]:
        return {
            "nodes": tuple(sorted(self.durable_nodes)),
            "edges": tuple(sorted(self.durable_edges)),
        }


@dataclass(frozen=True)
class GrowthScenarioRun:
    known_route: str
    unknown_before_route: str
    provisional_graph_id: str
    candidate_variant_count: int
    promoted_route: str
    burst_temporal_shape: str
    burst_promoted: bool
    route_after_rollback: str
    durable_changed_after_promotion: bool
    durable_restored_after_rollback: bool
    events: tuple[str, ...]


class GrowthScenarioHarness:
    """Scenario fixture for end-to-end provisional growth behavior."""

    def __init__(self) -> None:
        self.runtime = ProvisionalGraphGrowthRuntime(
            activation_threshold=0.8,
            decay=0.85,
            refractory_ticks=2,
            max_variants=3,
            risk_limit=0.6,
        )
        self.known_routes = {
            "known:a": "route:known_a",
            "known:b": "route:known_b",
        }
        self.promoted_routes: dict[str, str] = {}
        self.promoted_patches: dict[str, GrowthPatch] = {}
        self.events: list[str] = []

    def route(self, pattern_key: str) -> str:
        if pattern_key in self.known_routes:
            return self.known_routes[pattern_key]
        if pattern_key in self.promoted_routes:
            return self.promoted_routes[pattern_key]
        return "route:review_fallback"

    def learn_from_observations(self, pattern_key: str, observations: list[Observation]) -> GrowthPatch | None:
        graph: ProvisionalGraph | None = None
        for item in observations:
            graph = self.runtime.observe(item) or graph

        guard = self.runtime.stability_guard(observations)
        if graph is None:
            self.events.append(f"{pattern_key}:held:no_provisional_graph")
            return None
        if not guard["accepted"]:
            self.events.append(f"{pattern_key}:held:{guard['reason']}")
            return None

        variants = self.runtime.spawn_variants(graph, observations)
        eligible = [variant for variant in variants if variant.status == "probation"]
        if not eligible:
            self.events.append(f"{pattern_key}:held:no_probation_variant")
            return None

        scored = [
            (self.runtime.shadow_score(variant, observations[-1])["score"], variant)
            for variant in eligible
        ]
        best_variant = max(scored, key=lambda item: item[0])[1]
        patch = self.runtime.make_growth_patch(
            best_variant,
            graph.evidence_refs,
            temporal_shape=str(guard["temporal_shape"]),
        )
        if not self.runtime.should_promote(patch):
            self.events.append(f"{pattern_key}:held:promotion_gate")
            return None

        self.runtime.apply_patch(patch, promoted=True)
        self.promoted_routes[pattern_key] = f"route:{best_variant.strategy}"
        self.promoted_patches[pattern_key] = patch
        self.events.append(f"{pattern_key}:promoted:{best_variant.strategy}")
        return patch

    def rollback_if_regressed(self, pattern_key: str, *, observed_error: float) -> bool:
        patch = self.promoted_patches.get(pattern_key)
        if patch is None:
            return False
        if observed_error <= patch.baseline_error:
            return False

        for node in patch.proposed_nodes:
            self.runtime.durable_nodes.discard(node)
        for edge in patch.proposed_edges:
            self.runtime.durable_edges.discard(edge)
        self.promoted_routes.pop(pattern_key, None)
        graph = self.runtime.provisional_graphs.get(patch.graph_id)
        if graph is not None:
            graph.status = "rolled_back"
        self.events.append(f"{pattern_key}:rolled_back")
        return True


def run_provisional_growth_scenario() -> GrowthScenarioRun:
    harness = GrowthScenarioHarness()
    initial_durable = harness.runtime.durable_snapshot()

    known_route = harness.route("known:a")
    unknown_before_route = harness.route("unknown:c")

    recurring_c = [
        Observation("c-1", "unknown:c", "trace:c:1", surprise=1.0, quality=0.92, risk=0.05, tick=1),
        Observation("c-2", "unknown:c", "trace:c:2", surprise=0.9, quality=0.95, risk=0.05, tick=5),
        Observation("c-3", "unknown:c", "trace:c:3", surprise=0.8, quality=0.90, risk=0.08, tick=11),
    ]
    patch_c = harness.learn_from_observations("unknown:c", recurring_c)
    if patch_c is None:
        raise AssertionError("scenario fixture expected recurring pattern C to promote")

    after_promotion_durable = harness.runtime.durable_snapshot()
    graph_c = harness.runtime.provisional_graphs[patch_c.graph_id]
    promoted_route = harness.route("unknown:c")

    burst_d = [
        Observation("d-1", "unknown:d", "trace:d:1", surprise=1.0, quality=0.95, risk=0.05, tick=20),
        Observation("d-2", "unknown:d", "trace:d:2", surprise=1.0, quality=0.95, risk=0.05, tick=21),
    ]
    burst_guard = harness.runtime.stability_guard(burst_d)
    patch_d = harness.learn_from_observations("unknown:d", burst_d)

    harness.rollback_if_regressed("unknown:c", observed_error=0.7)
    after_rollback_durable = harness.runtime.durable_snapshot()

    return GrowthScenarioRun(
        known_route=known_route,
        unknown_before_route=unknown_before_route,
        provisional_graph_id=graph_c.graph_id,
        candidate_variant_count=len([variant for variant in harness.runtime.variants.values() if variant.graph_id == graph_c.graph_id]),
        promoted_route=promoted_route,
        burst_temporal_shape=str(burst_guard["temporal_shape"]),
        burst_promoted=patch_d is not None,
        route_after_rollback=harness.route("unknown:c"),
        durable_changed_after_promotion=after_promotion_durable != initial_durable,
        durable_restored_after_rollback=after_rollback_durable == initial_durable,
        events=tuple(harness.events),
    )
