"""CGF Hierarchical Cycles eval."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChildResponse:
    child_cycle_id: str
    status: str
    used_budget: int
    budget: int
    evidence_refs: tuple[str, ...] = ()
    proposal_refs: tuple[str, ...] = ()
    final_authority: bool = False


def validate_child_response(response: ChildResponse) -> None:
    allowed = {"evidence", "proposal", "uncertainty", "deferred", "failed", "no_bid"}
    if response.status not in allowed:
        raise ValueError("invalid child response status")
    if response.used_budget > response.budget:
        raise ValueError("child exceeded budget")
    if response.final_authority:
        raise ValueError("child response cannot carry final authority")
    if response.status == "proposal" and not response.proposal_refs:
        raise ValueError("proposal response requires proposal refs")
    if response.status == "evidence" and not response.evidence_refs:
        raise ValueError("evidence response requires evidence refs")


def parent_trace(parent_cycle_id: str, responses: tuple[ChildResponse, ...]) -> dict[str, object]:
    if not parent_cycle_id:
        raise ValueError("parent cycle id is required")
    for response in responses:
        validate_child_response(response)
    return {
        "parent_cycle_id": parent_cycle_id,
        "child_cycle_ids": [response.child_cycle_id for response in responses],
        "deferred": [response.child_cycle_id for response in responses if response.status == "deferred"],
        "proposal_refs": [ref for response in responses for ref in response.proposal_refs],
        "evidence_refs": [ref for response in responses for ref in response.evidence_refs],
    }
