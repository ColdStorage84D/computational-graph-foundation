"""CGF renormalization and coarse-graining eval."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FineNode:
    node_id: str
    group: str
    signal: str
    source_refs: tuple[str, ...]


def coarse_grain(nodes: tuple[FineNode, ...]) -> dict[str, dict[str, object]]:
    coarse: dict[str, dict[str, object]] = {}
    for node in nodes:
        entry = coarse.setdefault(node.group, {"signals": set(), "source_refs": []})
        entry["signals"].add(node.signal)
        entry["source_refs"].extend(node.source_refs)
    return {
        key: {"signals": tuple(sorted(value["signals"])), "source_refs": tuple(value["source_refs"])}
        for key, value in coarse.items()
    }


def relevant_law_score(coarse: dict[str, dict[str, object]], edges: tuple[tuple[str, str], ...]) -> int:
    required_groups = {"source", "bridge", "sink"}
    if not required_groups.issubset(set(coarse)):
        return 0
    return int(("source", "bridge") in edges) + int(("bridge", "sink") in edges)


def distractor_baseline(nodes: tuple[FineNode, ...]) -> int:
    return sum(1 for node in nodes if node.signal == "distractor")


def consistency_residual(fine_signal_count: int, coarse_signal_count: int) -> int:
    return abs(fine_signal_count - coarse_signal_count)
