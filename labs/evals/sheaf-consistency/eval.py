"""CGF sheaf consistency eval."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LocalView:
    view_id: str
    support: str
    payload: dict[str, object]
    status: str = "observed"


@dataclass(frozen=True)
class RestrictionMap:
    map_id: str
    source_support: str
    target_support: str
    keys: tuple[str, ...]


def restrict_view(view: LocalView, restriction: RestrictionMap) -> LocalView:
    if view.support != restriction.source_support:
        raise ValueError("restriction source does not match view support")
    return LocalView(
        view_id=f"{view.view_id}:{restriction.map_id}",
        support=restriction.target_support,
        payload={key: view.payload[key] for key in restriction.keys if key in view.payload},
        status=view.status,
    )


def compare_overlap(left: LocalView, right: LocalView) -> dict[str, object]:
    if left.support != right.support:
        raise ValueError("views must share support")
    keys = sorted(set(left.payload) | set(right.payload))
    conflicts = tuple(
        key for key in keys
        if left.payload.get(key) != right.payload.get(key)
    )
    return {
        "support": left.support,
        "residual": len(conflicts),
        "conflicts": conflicts,
        "statuses": (left.status, right.status),
    }


def glue_views(left: LocalView, right: LocalView, comparison: dict[str, object]) -> dict[str, object]:
    if comparison["residual"]:
        return {
            "kind": "obstruction",
            "support": comparison["support"],
            "obstruction_refs": comparison["conflicts"],
            "merged_payload": {},
            "status": "counterfactual" if "counterfactual" in comparison["statuses"] else "observed",
        }
    payload = dict(left.payload)
    payload.update(right.payload)
    return {
        "kind": "gluing_candidate",
        "support": comparison["support"],
        "merged_payload": payload,
        "status": "counterfactual" if "counterfactual" in comparison["statuses"] else "observed",
    }
