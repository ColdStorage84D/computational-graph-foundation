"""Small bot route-growth example for CGF bot applications.

The example is intentionally dependency-free. It shows Provisional Graph
Growth as application behavior: recurring unknown patterns may create a
candidate route, but durable route changes require stable evidence, a promotion
gate, and rollback.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RouteObservation:
    observation_id: str
    pattern_key: str
    evidence_ref: str
    surprise: float
    quality: float
    risk: float
    tick: int


@dataclass
class ProvisionalRoute:
    route_id: str
    pattern_key: str
    evidence_refs: list[str]
    activation: float
    status: str = "provisional"
    allowed_use: tuple[str, ...] = ("explain", "shadow_score", "review")


@dataclass(frozen=True)
class RouteCandidate:
    candidate_id: str
    provisional_route_id: str
    strategy: str
    affinity: float
    risk: float
    can_commit: bool = False


@dataclass(frozen=True)
class PromotionGate:
    accepted: bool
    temporal_shape: str
    reason: str
    baseline_error: float
    candidate_error: float
    risk: float
    rollback_policy: str


@dataclass(frozen=True)
class RouteGrowthRun:
    known_route: str
    unknown_before_route: str
    provisional_route_id: str
    candidate_count: int
    promoted_route: str
    burst_temporal_shape: str
    burst_promoted: bool
    route_after_rollback: str
    trace: tuple[str, ...]


@dataclass
class ProvisionalRouteGrowthBot:
    activation_threshold: float = 0.8
    risk_limit: float = 0.6
    max_candidates: int = 3
    known_routes: dict[str, str] = field(default_factory=lambda: {
        "known:a": "route:known_a",
        "known:b": "route:known_b",
    })
    promoted_routes: dict[str, str] = field(default_factory=dict)
    observations_by_pattern: dict[str, list[RouteObservation]] = field(default_factory=dict)
    provisional_routes: dict[str, ProvisionalRoute] = field(default_factory=dict)
    promoted_gates: dict[str, PromotionGate] = field(default_factory=dict)
    trace: list[str] = field(default_factory=list)

    def route_for(self, pattern_key: str) -> str:
        if pattern_key in self.known_routes:
            return self.known_routes[pattern_key]
        if pattern_key in self.promoted_routes:
            return self.promoted_routes[pattern_key]
        return "route:review_fallback"

    def observe(self, observation: RouteObservation) -> ProvisionalRoute | None:
        observations = self.observations_by_pattern.setdefault(observation.pattern_key, [])
        observations.append(observation)
        activation = sum(item.surprise * item.quality for item in observations) / max(1, len(observations))
        if activation < self.activation_threshold or len(observations) < 2:
            self.trace.append(f"{observation.pattern_key}:observed:insufficient_support")
            return None

        route_id = f"provisional:{observation.pattern_key}"
        provisional = self.provisional_routes.get(route_id)
        evidence_refs = [item.evidence_ref for item in observations]
        if provisional is None:
            provisional = ProvisionalRoute(
                route_id=route_id,
                pattern_key=observation.pattern_key,
                evidence_refs=evidence_refs,
                activation=activation,
            )
            self.provisional_routes[route_id] = provisional
            self.trace.append(f"{observation.pattern_key}:provisional_created")
            return provisional

        provisional.evidence_refs = list(dict.fromkeys(provisional.evidence_refs + evidence_refs))
        provisional.activation = activation
        self.trace.append(f"{observation.pattern_key}:provisional_updated")
        return provisional

    def stability_guard(self, observations: list[RouteObservation]) -> dict[str, object]:
        if len(observations) < 2:
            return {"accepted": False, "temporal_shape": "one_off", "reason": "insufficient_recurrence"}

        ticks = sorted({item.tick for item in observations})
        span = ticks[-1] - ticks[0]
        average_quality = sum(item.quality for item in observations) / len(observations)
        average_risk = sum(item.risk for item in observations) / len(observations)

        if span <= 1:
            return {"accepted": False, "temporal_shape": "burst", "reason": "burst_pattern"}
        if average_quality < 0.6:
            return {"accepted": False, "temporal_shape": "unstable", "reason": "low_quality"}
        if average_risk > self.risk_limit:
            return {"accepted": False, "temporal_shape": "unstable", "reason": "risk_above_limit"}
        return {"accepted": True, "temporal_shape": "stable", "reason": "recurring_stable_support"}

    def candidate_routes(self, provisional: ProvisionalRoute) -> tuple[RouteCandidate, ...]:
        observations = self.observations_by_pattern[provisional.pattern_key]
        average_quality = sum(item.quality for item in observations) / len(observations)
        average_risk = sum(item.risk for item in observations) / len(observations)
        strategies = ("new_route", "new_rule", "new_specialist")
        candidates = []
        for index, strategy in enumerate(strategies[: self.max_candidates]):
            candidates.append(
                RouteCandidate(
                    candidate_id=f"{provisional.route_id}:{strategy}",
                    provisional_route_id=provisional.route_id,
                    strategy=strategy,
                    affinity=max(0.0, min(1.0, average_quality - 0.05 * index)),
                    risk=min(1.0, average_risk + 0.1 * index),
                )
            )
        return tuple(candidates)

    def shadow_score(self, candidate: RouteCandidate, observation: RouteObservation) -> dict[str, object]:
        return {
            "candidate_id": candidate.candidate_id,
            "score": max(0.0, min(1.0, candidate.affinity * observation.quality - candidate.risk)),
            "authority": "shadow_only",
            "can_commit": False,
            "evidence_ref": observation.evidence_ref,
        }

    def promotion_gate(self, candidate: RouteCandidate, observations: list[RouteObservation]) -> PromotionGate:
        guard = self.stability_guard(observations)
        baseline_error = 0.4
        candidate_error = max(0.0, baseline_error - 0.25 * candidate.affinity)
        accepted = bool(guard["accepted"]) and candidate.risk <= self.risk_limit
        accepted = accepted and baseline_error > candidate_error + candidate.risk + 0.1
        return PromotionGate(
            accepted=accepted,
            temporal_shape=str(guard["temporal_shape"]),
            reason=str(guard["reason"]) if not accepted else "promotion_gate_passed",
            baseline_error=baseline_error,
            candidate_error=candidate_error,
            risk=candidate.risk,
            rollback_policy="observed_error_above_baseline",
        )

    def try_promote(self, provisional: ProvisionalRoute) -> str:
        observations = self.observations_by_pattern[provisional.pattern_key]
        candidates = self.candidate_routes(provisional)
        scored = [
            (self.shadow_score(candidate, observations[-1])["score"], candidate)
            for candidate in candidates
        ]
        best = max(scored, key=lambda item: item[0])[1]
        gate = self.promotion_gate(best, observations)
        if not gate.accepted:
            self.trace.append(f"{provisional.pattern_key}:held:{gate.reason}")
            return self.route_for(provisional.pattern_key)

        route = f"route:{best.strategy}"
        self.promoted_routes[provisional.pattern_key] = route
        self.promoted_gates[provisional.pattern_key] = gate
        provisional.status = "promoted"
        self.trace.append(f"{provisional.pattern_key}:promoted:{best.strategy}")
        return route

    def rollback_if_regressed(self, pattern_key: str, *, observed_error: float) -> bool:
        gate = self.promoted_gates.get(pattern_key)
        if gate is None or observed_error <= gate.baseline_error:
            return False
        self.promoted_routes.pop(pattern_key, None)
        for provisional in self.provisional_routes.values():
            if provisional.pattern_key == pattern_key:
                provisional.status = "rolled_back"
        self.trace.append(f"{pattern_key}:rolled_back")
        return True


def observation(index: int, pattern_key: str, *, tick: int, quality: float = 0.9, risk: float = 0.05) -> RouteObservation:
    return RouteObservation(
        observation_id=f"obs:{pattern_key}:{index}",
        pattern_key=pattern_key,
        evidence_ref=f"trace:{pattern_key}:{index}",
        surprise=1.0,
        quality=quality,
        risk=risk,
        tick=tick,
    )


def run_route_growth_demo() -> RouteGrowthRun:
    bot = ProvisionalRouteGrowthBot()

    known_route = bot.route_for("known:a")
    unknown_before_route = bot.route_for("unknown:c")

    recurring = [
        observation(1, "unknown:c", tick=1, quality=0.92, risk=0.05),
        observation(2, "unknown:c", tick=5, quality=0.95, risk=0.05),
        observation(3, "unknown:c", tick=11, quality=0.90, risk=0.08),
    ]
    provisional = None
    for item in recurring:
        provisional = bot.observe(item) or provisional
    if provisional is None:
        raise AssertionError("demo expected recurring unknown pattern to create a provisional route")

    candidates = bot.candidate_routes(provisional)
    promoted_route = bot.try_promote(provisional)

    burst = [
        observation(1, "unknown:d", tick=20, quality=0.95, risk=0.05),
        observation(2, "unknown:d", tick=21, quality=0.95, risk=0.05),
    ]
    burst_provisional = None
    for item in burst:
        burst_provisional = bot.observe(item) or burst_provisional
    burst_guard = bot.stability_guard(burst)
    burst_promoted = False
    if burst_provisional is not None:
        before = bot.route_for("unknown:d")
        after = bot.try_promote(burst_provisional)
        burst_promoted = before != after

    bot.rollback_if_regressed("unknown:c", observed_error=0.7)

    return RouteGrowthRun(
        known_route=known_route,
        unknown_before_route=unknown_before_route,
        provisional_route_id=provisional.route_id,
        candidate_count=len(candidates),
        promoted_route=promoted_route,
        burst_temporal_shape=str(burst_guard["temporal_shape"]),
        burst_promoted=burst_promoted,
        route_after_rollback=bot.route_for("unknown:c"),
        trace=tuple(bot.trace),
    )
