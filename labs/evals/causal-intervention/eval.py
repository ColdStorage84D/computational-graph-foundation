"""CGF causal intervention eval."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Record:
    record_id: str
    kind: str
    subject: str
    value: object
    scope: tuple[str, ...] = ()
    source_refs: tuple[str, ...] = ()


def observe(record_id: str, subject: str, value: object, source_refs: tuple[str, ...] = ()) -> Record:
    return Record(record_id, "observation", subject, value, (), source_refs)


def intervene(record_id: str, subject: str, value: object, scope: tuple[str, ...], source_refs: tuple[str, ...] = ()) -> Record:
    if not scope:
        raise ValueError("intervention scope is required")
    return Record(record_id, "intervention", subject, value, scope, source_refs)


def mark_counterfactual(record_id: str, subject: str, value: object) -> Record:
    return Record(record_id, "counterfactual", subject, value)


def block_counterfactual_promotion(record: Record) -> bool:
    return record.kind == "counterfactual"


def score_attribution(candidate: Record, outcome: Record, causal_scope: tuple[str, ...]) -> float:
    if candidate.kind != "intervention":
        return 0.0
    if candidate.subject != outcome.subject:
        return 0.0
    return 1.0 if set(candidate.scope) == set(causal_scope) else 0.0


def trace_attribution(candidate: Record, outcome: Record, causal_scope: tuple[str, ...]) -> dict[str, object]:
    score = score_attribution(candidate, outcome, causal_scope)
    return {
        "candidate_ref": candidate.record_id,
        "outcome_ref": outcome.record_id,
        "score": score,
        "allowed": score > 0.0,
    }
