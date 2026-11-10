"""CGF renormalization and coarse-graining eval.

Two layers live here:

- real-space renormalization of a conductance network. Eliminating a node and
  replacing it by renormalized couplings among its neighbours (the star-mesh
  rule, which is the Schur complement of the graph Laplacian) gives a coarse
  network that reproduces the fine network's response at every kept node. The
  couplings flow under repeated coarse-graining, and sources on eliminated
  nodes must be renormalized too;
- the summary records that keep source references and fine/coarse residuals
  visible when a coarse description is reported.

The law preserved is the linear response of a resistor-like network. Nothing
here claims a renormalization group for any other system.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


Coupling = tuple[str, str]
Network = Mapping[Coupling, float]


def _key(left: str, right: str) -> Coupling:
    if left == right:
        raise ValueError("self-couplings are not allowed")
    return (left, right) if left < right else (right, left)


def make_network(edges: tuple[tuple[str, str, float], ...]) -> dict[Coupling, float]:
    network: dict[Coupling, float] = {}
    for left, right, weight in edges:
        if weight <= 0.0:
            raise ValueError("couplings must be positive")
        key = _key(left, right)
        network[key] = network.get(key, 0.0) + weight
    return network


def nodes_of(network: Network) -> tuple[str, ...]:
    return tuple(sorted({node for pair in network for node in pair}))


def eliminate(
    network: Network,
    node: str,
    injections: Mapping[str, float] | None = None,
) -> tuple[dict[Coupling, float], dict[str, float]]:
    """Remove one node and renormalize what touches it.

    Every pair of its neighbours gains w_i * w_j / (sum of w), and any current
    injected at the node is shared out to the neighbours in proportion to w.
    """

    injections = dict(injections or {})
    neighbours = {}
    remaining: dict[Coupling, float] = {}
    for (left, right), weight in network.items():
        if node == left:
            neighbours[right] = weight
        elif node == right:
            neighbours[left] = weight
        else:
            remaining[(left, right)] = weight
    if not neighbours:
        raise ValueError(f"cannot eliminate a node with no couplings: {node}")
    total = sum(neighbours.values())
    names = sorted(neighbours)
    for index, first in enumerate(names):
        for second in names[index + 1 :]:
            key = _key(first, second)
            remaining[key] = remaining.get(key, 0.0) + neighbours[first] * neighbours[second] / total
    lost = injections.pop(node, 0.0)
    if lost:
        for name in names:
            injections[name] = injections.get(name, 0.0) + lost * neighbours[name] / total
    return remaining, injections


def renormalize(
    network: Network,
    keep: tuple[str, ...],
    injections: Mapping[str, float] | None = None,
) -> tuple[dict[Coupling, float], dict[str, float]]:
    """Coarse network and coarse sources on the kept nodes."""

    present = set(nodes_of(network))
    missing = set(keep) - present
    if missing:
        raise ValueError(f"kept nodes are not in the network: {sorted(missing)}")
    if len(keep) < 2:
        raise ValueError("keep at least two nodes")
    coarse: dict[Coupling, float] = dict(network)
    sources = dict(injections or {})
    for node in sorted(present - set(keep)):
        coarse, sources = eliminate(coarse, node, sources)
    return coarse, sources


def naive_coarse_grain(network: Network, keep: tuple[str, ...]) -> dict[Coupling, float]:
    """Baseline: drop eliminated nodes and keep the surviving direct couplings."""

    kept = set(keep)
    return {pair: weight for pair, weight in network.items() if pair[0] in kept and pair[1] in kept}


def potentials(network: Network, injections: Mapping[str, float], ground: str) -> dict[str, float]:
    """Solve the network equations with one grounded node."""

    names = [node for node in nodes_of(network) if node != ground]
    if ground not in nodes_of(network):
        raise ValueError("ground node is not in the network")
    index = {node: position for position, node in enumerate(names)}
    size = len(names)
    rows = [[0.0] * (size + 1) for _ in range(size)]
    for (left, right), weight in network.items():
        for here, there in ((left, right), (right, left)):
            if here == ground:
                continue
            rows[index[here]][index[here]] += weight
            if there != ground:
                rows[index[here]][index[there]] -= weight
    for node, current in injections.items():
        if node != ground:
            if node not in index:
                raise ValueError(f"injection at a node outside the network: {node}")
            rows[index[node]][size] += current
    for column in range(size):
        pivot = max(range(column, size), key=lambda position: abs(rows[position][column]))
        if abs(rows[pivot][column]) < 1e-13:
            raise ValueError("network is disconnected from ground")
        rows[column], rows[pivot] = rows[pivot], rows[column]
        scale = rows[column][column]
        rows[column] = [value / scale for value in rows[column]]
        for position in range(size):
            if position != column and rows[position][column]:
                factor = rows[position][column]
                rows[position] = [a - factor * b for a, b in zip(rows[position], rows[column])]
    solution = {node: rows[index[node]][size] for node in names}
    solution[ground] = 0.0
    return solution


def effective_coupling(network: Network, left: str, right: str) -> float:
    """Coupling a single direct edge would need to give the same response."""

    return 1.0 / potentials(network, {left: 1.0}, right)[left]


def decimate_chain(couplings: tuple[float, ...]) -> tuple[float, ...]:
    """One renormalization step on a chain: merge consecutive pairs in series."""

    if len(couplings) % 2:
        raise ValueError("chain length must be even to decimate")
    return tuple(
        first * second / (first + second)
        for first, second in zip(couplings[0::2], couplings[1::2])
    )


def chain_network(couplings: tuple[float, ...]) -> dict[Coupling, float]:
    return make_network(
        tuple((f"n{index:03d}", f"n{index + 1:03d}", weight) for index, weight in enumerate(couplings))
    )


def ladder_network(rungs: int, rail: float, rung: float) -> dict[Coupling, float]:
    edges = []
    for index in range(rungs):
        edges.append((f"t{index}", f"b{index}", rung * (1.0 + 0.1 * index)))
        if index + 1 < rungs:
            edges.append((f"t{index}", f"t{index + 1}", rail))
            edges.append((f"b{index}", f"b{index + 1}", rail * 1.5))
    return make_network(tuple(edges))


# --- Summary records ---------------------------------------------------------


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
