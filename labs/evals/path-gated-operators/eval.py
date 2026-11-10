"""CGF path-conditioned and path-gated operators eval.

The contract under test:

- an evidence path is an ordered chain of declared edges that must resolve
  against the graph, start at evidence, and end at the claim it supports;
- a hard path gate decides whether a proposal may advance, and fails closed
  when the path is missing, broken, or points somewhere else;
- path conditioning changes a score using the path, and never authorizes
  anything by itself;
- a decision keeps every rejected candidate and the reason it was rejected.

The functions are self-contained. They mirror the Architecture reference but do
not import it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class EvidenceGraph:
    node_types: Mapping[str, str]  # node_id -> "evidence" | "intermediate" | "claim"
    edges: Mapping[str, tuple[str, str]]  # edge_id -> (source, target)


@dataclass(frozen=True)
class EvidencePath:
    node_ids: tuple[str, ...]
    edge_ids: tuple[str, ...]


@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    claim_node: str
    score: float
    path: EvidencePath | None


@dataclass(frozen=True)
class GateOutcome:
    candidate_id: str
    allowed: bool
    reason: str


@dataclass(frozen=True)
class Decision:
    action: str  # "commit" or "abstain"
    selected_id: str | None
    reason: str
    rejected: tuple[GateOutcome, ...] = ()


def path_errors(graph: EvidenceGraph, path: EvidencePath) -> tuple[str, ...]:
    """Every reason the path does not resolve. Empty means it resolves."""

    errors = []
    for node_id in path.node_ids:
        if node_id not in graph.node_types:
            errors.append(f"missing node {node_id}")
    if len(path.node_ids) < 2:
        errors.append("a support path needs at least two nodes")
        return tuple(errors)
    if len(path.edge_ids) != len(path.node_ids) - 1:
        errors.append("edge count must equal node count minus one")
        return tuple(errors)
    for index, edge_id in enumerate(path.edge_ids):
        edge = graph.edges.get(edge_id)
        if edge is None:
            errors.append(f"missing edge {edge_id}")
        elif edge != (path.node_ids[index], path.node_ids[index + 1]):
            errors.append(f"edge {edge_id} does not connect path step {index}")
    return tuple(errors)


def hard_gate(graph: EvidenceGraph, candidate: Candidate) -> GateOutcome:
    """Allow only a candidate whose path resolves from evidence to its claim."""

    if candidate.path is None:
        return GateOutcome(candidate.candidate_id, False, "no_path")
    errors = path_errors(graph, candidate.path)
    if errors:
        return GateOutcome(candidate.candidate_id, False, "unresolved_path: " + "; ".join(errors))
    if graph.node_types[candidate.path.node_ids[0]] != "evidence":
        return GateOutcome(candidate.candidate_id, False, "path_does_not_start_at_evidence")
    if candidate.path.node_ids[-1] != candidate.claim_node:
        return GateOutcome(candidate.candidate_id, False, "path_does_not_reach_claim")
    return GateOutcome(candidate.candidate_id, True, "path_resolved")


def path_conditioned_score(candidate: Candidate, *, hop_discount: float) -> float:
    """Discount a score by the length of the chain that supports it.

    Conditioning changes the number. It does not decide whether the candidate
    may advance; `hard_gate` does that.
    """

    if not 0.0 < hop_discount <= 1.0:
        raise ValueError("hop discount must be in (0, 1]")
    if candidate.path is None:
        return candidate.score
    extra_hops = max(0, len(candidate.path.edge_ids) - 1)
    return candidate.score * hop_discount**extra_hops


def _best(candidates: tuple[Candidate, ...], scores: Mapping[str, float]) -> Candidate:
    return max(candidates, key=lambda item: (scores[item.candidate_id], item.candidate_id))


def decide_score_only(candidates: tuple[Candidate, ...]) -> Decision:
    """Baseline: the highest score commits. The path is never read."""

    if not candidates:
        return Decision("abstain", None, "no_candidates")
    scores = {item.candidate_id: item.score for item in candidates}
    return Decision("commit", _best(candidates, scores).candidate_id, "highest_score")


def decide_path_gated(
    graph: EvidenceGraph,
    candidates: tuple[Candidate, ...],
    *,
    hop_discount: float | None = None,
) -> Decision:
    """Gate first, then rank what survived. Abstain when nothing survives."""

    outcomes = tuple(hard_gate(graph, candidate) for candidate in candidates)
    allowed = tuple(
        candidate for candidate, outcome in zip(candidates, outcomes) if outcome.allowed
    )
    rejected = tuple(outcome for outcome in outcomes if not outcome.allowed)
    if not allowed:
        return Decision("abstain", None, "no_candidate_passed_the_path_gate", rejected)
    if hop_discount is None:
        scores = {item.candidate_id: item.score for item in allowed}
        reason = "highest_score_among_gated"
    else:
        scores = {
            item.candidate_id: path_conditioned_score(item, hop_discount=hop_discount)
            for item in allowed
        }
        reason = "highest_path_conditioned_score_among_gated"
    return Decision("commit", _best(allowed, scores).candidate_id, reason, rejected)
