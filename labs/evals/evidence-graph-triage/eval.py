"""Evidence Graph Triage eval: evidence sets status, outcomes set order.

Self-contained and domain-neutral. Source categories are `source_a`, `source_b`,
and `source_c` rather than any domain vocabulary, because this eval tests the
reusable contract rather than one application of it.

The fixture is synthetic. It is not incident data, security data, audit data, or
any measured corpus, and it supports no detection or triage-quality claim.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

REFERENCE = Path(__file__).resolve().parents[3] / "architecture" / "reference" / "python"
if str(REFERENCE) not in sys.path:
    sys.path.insert(0, str(REFERENCE))

from cgf_architecture import EligibilityStore, GateDecision, Proposal  # noqa: E402

SOURCE_CATEGORIES = ("source_a", "source_b", "source_c")
VERDICTS = ("true_positive", "false_positive", "benign", "inconclusive")

GATES = (
    ("gate:a-b", "source_a", "source_b"),
    ("gate:b-c", "source_b", "source_c"),
)

SUPPORT_DELTA = {
    "true_positive": 1.0,
    "false_positive": -1.0,
    "benign": -0.5,
    "inconclusive": 0.0,
}
UNCERTAINTY_DELTA = {
    "true_positive": -0.30,
    "false_positive": -0.30,
    "benign": -0.15,
    "inconclusive": 0.20,
}
MULTIPLIER_GAIN = 0.15
MULTIPLIER_MIN = 0.60
MULTIPLIER_MAX = 1.40
UNCERTAINTY_FLOOR = 0.15


@dataclass(frozen=True)
class Record:
    record_id: str
    source_category: str


@dataclass(frozen=True)
class Candidate:
    finding_id: str
    rule_id: str
    raw_score: float
    records: tuple[Record, ...]


@dataclass(frozen=True)
class Decision:
    status: str
    action: str
    reason: str
    matched_gate_id: str | None
    categories: tuple[str, ...]
    gates: tuple[GateDecision, ...]


@dataclass(frozen=True)
class ValueRecord:
    key: str
    support: float = 0.0
    uncertainty: float = 1.0
    sample_count: int = 0
    expired_count: int = 0


@dataclass(frozen=True)
class Ranked:
    candidate: Candidate
    decision: Decision
    multiplier: float
    rank_score: float
    trace_id: str | None


def decide_status(records: tuple[Record, ...]) -> Decision:
    """Status from evidence corroboration alone.

    This signature is the contract: no score, weight, or memory value can reach it.
    """

    categories = tuple(sorted({record.source_category for record in records}))
    present = set(categories)
    gates = tuple(
        GateDecision(
            gate_id=gate_id,
            passed=left in present and right in present,
            reason=f"{left} corroborated by {right}",
            hard=False,
        )
        for gate_id, left, right in GATES
    )

    if not records:
        return Decision("needs_more_evidence", "defer", "no_records", None, (), gates)
    for gate in gates:
        if gate.passed:
            return Decision(
                "confirmed", "commit", "gate_matched", gate.gate_id, categories, gates
            )
    if len(categories) >= 2:
        return Decision("review", "review", "multi_source_no_gate", None, categories, gates)
    if len(records) >= 2:
        return Decision(
            "review", "review", "multi_record_single_source", None, categories, gates
        )
    return Decision("inferred", "defer", "single_record", None, categories, gates)


class ValueMemory:
    """Outcome-backed weighting that reaches ordering and nothing else."""

    def __init__(self) -> None:
        self._records: dict[str, ValueRecord] = {}

    def get(self, key: str) -> ValueRecord:
        return self._records.get(key, ValueRecord(key))

    def multiplier(self, key: str) -> float:
        record = self.get(key)
        if record.sample_count == 0:
            return 1.0
        weight = 1.0 - record.uncertainty
        raw = 1.0 + MULTIPLIER_GAIN * record.support * weight
        return max(MULTIPLIER_MIN, min(MULTIPLIER_MAX, raw))

    def apply(self, key: str, verdict: str) -> ValueRecord:
        if verdict not in VERDICTS:
            raise ValueError(f"unknown verdict: {verdict}")
        before = self.get(key)
        after = replace(
            before,
            support=before.support + SUPPORT_DELTA[verdict],
            uncertainty=max(
                UNCERTAINTY_FLOOR, min(1.0, before.uncertainty + UNCERTAINTY_DELTA[verdict])
            ),
            sample_count=before.sample_count + 1,
        )
        self._records[key] = after
        return after

    def expire(self, key: str) -> ValueRecord:
        before = self.get(key)
        after = replace(
            before,
            uncertainty=min(1.0, before.uncertainty + 0.25),
            expired_count=before.expired_count + 1,
        )
        self._records[key] = after
        return after


class TriageRun:
    """One pass over candidates, plus the outcome bridge."""

    def __init__(self) -> None:
        self.values = ValueMemory()
        self.eligibility = EligibilityStore()
        self._finding_trace: dict[str, str] = {}
        self._trace_key: dict[str, str] = {}
        self._seen_verdicts: set[str] = set()

    def value_key(self, candidate: Candidate, decision: Decision) -> str:
        signature = "+".join(decision.categories) if decision.categories else "none"
        return f"{candidate.rule_id}|{decision.status}|{signature}"

    def rank(self, candidates: tuple[Candidate, ...], *, cycle_id: str) -> tuple[Ranked, ...]:
        ranked: list[Ranked] = []
        for candidate in candidates:
            decision = decide_status(candidate.records)
            key = self.value_key(candidate, decision)
            multiplier = self.values.multiplier(key)
            trace_id = None
            if decision.action == "commit":
                trace_id = f"eligibility:{candidate.finding_id}:{cycle_id}"
                if self.eligibility.get(trace_id) is None:
                    self.eligibility.create(
                        trace_id,
                        proposal=Proposal(
                            proposal_id=candidate.finding_id,
                            action_ref=f"triage:{candidate.finding_id}",
                        ),
                        cycle_id=cycle_id,
                    )
                self._finding_trace[candidate.finding_id] = trace_id
                self._trace_key[trace_id] = key
            ranked.append(
                Ranked(
                    candidate=candidate,
                    decision=decision,
                    multiplier=multiplier,
                    rank_score=round(candidate.raw_score * multiplier, 6),
                    trace_id=trace_id,
                )
            )
        return tuple(sorted(ranked, key=lambda item: (-item.rank_score, item.candidate.finding_id)))

    def record_outcome(self, verdict_id: str, finding_id: str, verdict: str) -> str:
        """The bridge. Only a committed finding can produce a value update."""

        if verdict_id in self._seen_verdicts:
            return "duplicate_ignored"
        trace_id = self._finding_trace.get(finding_id)
        if trace_id is None:
            raise ValueError(f"finding was never committed: {finding_id}")
        trace = self.eligibility.get(trace_id)
        if trace is None or trace.status != "pending":
            raise ValueError(f"eligibility is not pending: {trace_id}")
        succeeded = {"true_positive": True, "false_positive": False, "benign": False}.get(
            verdict
        )
        self.eligibility.resolve(trace_id, succeeded)
        self.values.apply(self._trace_key[trace_id], verdict)
        self._seen_verdicts.add(verdict_id)
        return "applied"

    def expire(self, finding_id: str) -> str:
        trace_id = self._finding_trace[finding_id]
        self.eligibility.expire(trace_id)
        self.values.expire(self._trace_key[trace_id])
        return "expired"


def fixture_candidates() -> tuple[Candidate, ...]:
    """Four candidates covering each status branch, with the top score deferred."""

    return (
        Candidate(
            "finding:corroborated",
            "rule-one",
            0.60,
            (Record("record:1", "source_a"), Record("record:2", "source_b")),
        ),
        Candidate(
            "finding:single-source-high",
            "rule-one",
            0.95,
            (Record("record:3", "source_a"),),
        ),
        # Scored just above `finding:corroborated`, so a single outcome on the
        # corroborated item is enough to swap them. The swap is the observable.
        Candidate(
            "finding:multi-record",
            "rule-two",
            0.62,
            (Record("record:4", "source_c"), Record("record:5", "source_c")),
        ),
        Candidate(
            "finding:unsupported",
            "rule-two",
            0.80,
            (),
        ),
    )


def run_eval() -> dict[str, Any]:
    """Run two cycles with an outcome between them and report the contract results."""

    run = TriageRun()
    candidates = fixture_candidates()

    first = run.rank(candidates, cycle_id="cycle-1")
    statuses_before = {item.candidate.finding_id: item.decision.status for item in first}
    order_before = tuple(item.candidate.finding_id for item in first)

    run.record_outcome("verdict:1", "finding:corroborated", "true_positive")

    second = run.rank(candidates, cycle_id="cycle-2")
    statuses_after = {item.candidate.finding_id: item.decision.status for item in second}
    order_after = tuple(item.candidate.finding_id for item in second)

    top_raw = max(second, key=lambda item: item.candidate.raw_score)

    return {
        "statuses": statuses_before,
        "statuses_unchanged": statuses_before == statuses_after,
        "order_before": order_before,
        "order_after": order_after,
        "order_changed": order_before != order_after,
        "top_raw_finding": top_raw.candidate.finding_id,
        "top_raw_action": top_raw.decision.action,
        "multiplier_after_true_positive": run.values.multiplier(
            "rule-one|confirmed|source_a+source_b"
        ),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run_eval(), indent=2, default=str))
