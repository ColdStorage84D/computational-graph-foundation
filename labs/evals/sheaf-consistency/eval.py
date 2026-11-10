"""CGF sheaf consistency eval.

Two layers live here:

- a cellular sheaf on a graph: a vector space (stalk) on every node and edge,
  and a linear restriction map from each node into each incident edge. The
  coboundary measures disagreement on edges, its kernel is the space of global
  sections, and the sheaf Laplacian drives diffusion toward the nearest one;
- the view records that carry restriction, comparison, and gluing out of the
  model without letting a merged summary hide a conflict.

The fixture supplies every restriction map. Nothing here learns a sheaf.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Mapping


Vector = tuple[float, ...]
Matrix = tuple[tuple[float, ...], ...]
Assignment = Mapping[str, Vector]


# --- Cellular sheaf ----------------------------------------------------------


@dataclass(frozen=True)
class SheafEdge:
    edge_id: str
    tail: str
    head: str


@dataclass(frozen=True)
class CellularSheaf:
    node_dimensions: Mapping[str, int]
    edge_dimensions: Mapping[str, int]
    edges: tuple[SheafEdge, ...]
    restrictions: Mapping[tuple[str, str], Matrix]  # (node, edge) -> edge_dim x node_dim


def validate_sheaf(sheaf: CellularSheaf) -> None:
    if not sheaf.node_dimensions:
        raise ValueError("sheaf needs at least one node stalk")
    seen: set[str] = set()
    for edge in sheaf.edges:
        if edge.edge_id in seen:
            raise ValueError(f"duplicate edge: {edge.edge_id}")
        seen.add(edge.edge_id)
        if edge.edge_id not in sheaf.edge_dimensions:
            raise ValueError(f"edge stalk is undeclared: {edge.edge_id}")
        for node in (edge.tail, edge.head):
            if node not in sheaf.node_dimensions:
                raise ValueError(f"edge endpoint is undeclared: {node}")
            matrix = sheaf.restrictions.get((node, edge.edge_id))
            if matrix is None:
                raise ValueError(f"restriction map is missing: {node} -> {edge.edge_id}")
            rows, columns = sheaf.edge_dimensions[edge.edge_id], sheaf.node_dimensions[node]
            if len(matrix) != rows or any(len(row) != columns for row in matrix):
                raise ValueError(f"restriction map has the wrong shape: {node} -> {edge.edge_id}")


def _apply(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(sum(a * b for a, b in zip(row, vector)) for row in matrix)


def _check_assignment(sheaf: CellularSheaf, assignment: Assignment) -> None:
    for node, dimension in sheaf.node_dimensions.items():
        if node not in assignment:
            raise ValueError(f"assignment is missing node: {node}")
        if len(assignment[node]) != dimension:
            raise ValueError(f"assignment has the wrong dimension at node: {node}")


def coboundary(sheaf: CellularSheaf, assignment: Assignment) -> dict[str, Vector]:
    """Disagreement on each edge after both endpoints are restricted to it."""

    validate_sheaf(sheaf)
    _check_assignment(sheaf, assignment)
    result = {}
    for edge in sheaf.edges:
        head = _apply(sheaf.restrictions[(edge.head, edge.edge_id)], assignment[edge.head])
        tail = _apply(sheaf.restrictions[(edge.tail, edge.edge_id)], assignment[edge.tail])
        result[edge.edge_id] = tuple(a - b for a, b in zip(head, tail))
    return result


def edge_residuals(sheaf: CellularSheaf, assignment: Assignment) -> dict[str, float]:
    return {
        edge_id: math.sqrt(sum(value * value for value in difference))
        for edge_id, difference in coboundary(sheaf, assignment).items()
    }


def consistency_energy(sheaf: CellularSheaf, assignment: Assignment) -> float:
    """The quadratic form of the sheaf Laplacian: squared coboundary norm."""

    return sum(value * value for value in edge_residuals(sheaf, assignment).values())


def is_global_section(sheaf: CellularSheaf, assignment: Assignment, tolerance: float = 1e-9) -> bool:
    return all(value <= tolerance for value in edge_residuals(sheaf, assignment).values())


def _node_offsets(sheaf: CellularSheaf) -> tuple[dict[str, int], int]:
    offsets = {}
    total = 0
    for node in sorted(sheaf.node_dimensions):
        offsets[node] = total
        total += sheaf.node_dimensions[node]
    return offsets, total


def coboundary_matrix(sheaf: CellularSheaf) -> Matrix:
    validate_sheaf(sheaf)
    offsets, columns = _node_offsets(sheaf)
    rows: list[list[float]] = []
    for edge in sheaf.edges:
        for row_index in range(sheaf.edge_dimensions[edge.edge_id]):
            row = [0.0] * columns
            for node, sign in ((edge.head, 1.0), (edge.tail, -1.0)):
                source = sheaf.restrictions[(node, edge.edge_id)][row_index]
                for column, value in enumerate(source):
                    row[offsets[node] + column] += sign * value
            rows.append(row)
    return tuple(tuple(row) for row in rows)


def _rank(matrix: Matrix, tolerance: float = 1e-9) -> int:
    rows = [list(row) for row in matrix]
    if not rows:
        return 0
    rank = 0
    for column in range(len(rows[0])):
        pivot = max(range(rank, len(rows)), key=lambda index: abs(rows[index][column]), default=None)
        if pivot is None or abs(rows[pivot][column]) <= tolerance:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [value / scale for value in rows[rank]]
        for index in range(len(rows)):
            if index != rank and rows[index][column]:
                factor = rows[index][column]
                rows[index] = [a - factor * b for a, b in zip(rows[index], rows[rank])]
        rank += 1
        if rank == len(rows):
            break
    return rank


def global_section_dimension(sheaf: CellularSheaf) -> int:
    """Dimension of the kernel of the coboundary: how many ways views can agree."""

    _, columns = _node_offsets(sheaf)
    return columns - _rank(coboundary_matrix(sheaf))


def diffuse(
    sheaf: CellularSheaf, assignment: Assignment, *, step_size: float, iterations: int
) -> dict[str, Vector]:
    """Gradient descent on the consistency energy: x <- x - step * L x.

    For a small enough step the energy never increases and the limit is the
    orthogonal projection of the start onto the global sections.
    """

    if step_size <= 0.0 or iterations < 0:
        raise ValueError("step size must be positive and iterations nonnegative")
    current = {node: tuple(assignment[node]) for node in sheaf.node_dimensions}
    _check_assignment(sheaf, current)
    for _ in range(iterations):
        difference = coboundary(sheaf, current)
        gradient = {node: [0.0] * dim for node, dim in sheaf.node_dimensions.items()}
        for edge in sheaf.edges:
            for node, sign in ((edge.head, 1.0), (edge.tail, -1.0)):
                matrix = sheaf.restrictions[(node, edge.edge_id)]
                for row_index, value in enumerate(difference[edge.edge_id]):
                    for column, weight in enumerate(matrix[row_index]):
                        gradient[node][column] += sign * weight * value
        current = {
            node: tuple(value - step_size * slope for value, slope in zip(current[node], gradient[node]))
            for node in current
        }
    return current


def _identity(size: int, scale: float = 1.0) -> Matrix:
    return tuple(tuple(scale if a == b else 0.0 for b in range(size)) for a in range(size))


def cycle_sheaf(stalk_dimension: int, *, twisted: bool) -> CellularSheaf:
    """Three nodes in a cycle with identity restrictions.

    With `twisted`, one restriction is negated. Every single edge can still be
    satisfied, but going around the cycle flips the sign, so only the zero
    assignment agrees everywhere.
    """

    nodes = ("a", "b", "c")
    edges = (SheafEdge("ab", "a", "b"), SheafEdge("bc", "b", "c"), SheafEdge("ca", "c", "a"))
    restrictions = {}
    for edge in edges:
        restrictions[(edge.tail, edge.edge_id)] = _identity(stalk_dimension)
        restrictions[(edge.head, edge.edge_id)] = _identity(stalk_dimension)
    if twisted:
        restrictions[("a", "ca")] = _identity(stalk_dimension, -1.0)
    return CellularSheaf(
        node_dimensions={node: stalk_dimension for node in nodes},
        edge_dimensions={edge.edge_id: stalk_dimension for edge in edges},
        edges=edges,
        restrictions=restrictions,
    )


def shared_coordinate_sheaf() -> CellularSheaf:
    """Two views with two coordinates each that overlap on the first only."""

    edge = SheafEdge("overlap", "left", "right")
    return CellularSheaf(
        node_dimensions={"left": 2, "right": 2},
        edge_dimensions={"overlap": 1},
        edges=(edge,),
        restrictions={("left", "overlap"): ((1.0, 0.0),), ("right", "overlap"): ((1.0, 0.0),)},
    )


# --- View records ------------------------------------------------------------


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
