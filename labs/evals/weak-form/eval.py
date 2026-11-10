"""CGF weak form eval.

Two layers live here:

- a discrete weak form on a weighted graph. The strong law is
  (L + mass * I) u = f at every node, where L is the weighted graph Laplacian.
  The weak form tests the same law against a test function phi:
  a(u, phi) = l(phi), with
  a(u, phi) = sum over edges of w (u_i - u_j)(phi_i - phi_j) + mass * sum phi_i u_i
  and l(phi) = sum phi_i f_i. Summation by parts makes the two agree, and a
  Galerkin solve satisfies the weak form on a coarse space without satisfying
  the strong law pointwise;
- the report records that keep an aggregate pass from hiding local failures.

This is a declaration to validate, not a finite-element library.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


Field = Mapping[str, float]


@dataclass(frozen=True)
class GraphLaw:
    nodes: tuple[str, ...]
    edges: tuple[tuple[str, str, float], ...]
    mass: float = 0.0


def validate_law(law: GraphLaw) -> None:
    if not law.nodes or len(set(law.nodes)) != len(law.nodes):
        raise ValueError("law needs distinct nodes")
    known = set(law.nodes)
    for left, right, weight in law.edges:
        if left not in known or right not in known or left == right:
            raise ValueError("edge endpoints must be distinct declared nodes")
        if weight <= 0.0:
            raise ValueError("edge weights must be positive")
    if law.mass < 0.0:
        raise ValueError("mass coefficient must be nonnegative")


def _require(law: GraphLaw, *fields: Field) -> None:
    validate_law(law)
    for values in fields:
        missing = [node for node in law.nodes if node not in values]
        if missing:
            raise ValueError(f"field is missing nodes: {missing}")


def strong_residual(law: GraphLaw, field: Field, source: Field) -> dict[str, float]:
    """Pointwise residual of the local rule at every node."""

    _require(law, field, source)
    residual = {node: law.mass * field[node] - source[node] for node in law.nodes}
    for left, right, weight in law.edges:
        flow = weight * (field[left] - field[right])
        residual[left] += flow
        residual[right] -= flow
    return residual


def bilinear_form(law: GraphLaw, field: Field, test: Field) -> float:
    _require(law, field, test)
    total = law.mass * sum(test[node] * field[node] for node in law.nodes)
    for left, right, weight in law.edges:
        total += weight * (field[left] - field[right]) * (test[left] - test[right])
    return total


def load(law: GraphLaw, source: Field, test: Field) -> float:
    _require(law, source, test)
    return sum(test[node] * source[node] for node in law.nodes)


def tested_residual(law: GraphLaw, field: Field, source: Field, test: Field) -> float:
    """The weak residual a(u, phi) - l(phi) for one test function."""

    return bilinear_form(law, field, test) - load(law, source, test)


def region_balance(law: GraphLaw, field: Field, source: Field, region: frozenset[str]) -> dict[str, float]:
    """Conservation over a region, computed from its boundary edges only.

    Testing with the indicator of a region cancels every interior edge. What is
    left is net outflow through the boundary, plus storage, minus supply.
    """

    _require(law, field, source)
    if not region or not region <= set(law.nodes):
        raise ValueError("region must be a nonempty set of declared nodes")
    outflow = 0.0
    for left, right, weight in law.edges:
        if (left in region) != (right in region):
            inside, outside = (left, right) if left in region else (right, left)
            outflow += weight * (field[inside] - field[outside])
    stored = law.mass * sum(field[node] for node in region)
    supplied = sum(source[node] for node in region)
    return {
        "outflow": outflow,
        "stored": stored,
        "supplied": supplied,
        "residual": outflow + stored - supplied,
    }


def _solve(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    n = len(rhs)
    rows = [row[:] + [value] for row, value in zip(matrix, rhs)]
    for column in range(n):
        pivot = max(range(column, n), key=lambda index: abs(rows[index][column]))
        if abs(rows[pivot][column]) < 1e-13:
            raise ValueError("Galerkin system is singular: add mass or fix the basis")
        rows[column], rows[pivot] = rows[pivot], rows[column]
        scale = rows[column][column]
        rows[column] = [value / scale for value in rows[column]]
        for index in range(n):
            if index != column and rows[index][column]:
                factor = rows[index][column]
                rows[index] = [a - factor * b for a, b in zip(rows[index], rows[column])]
    return [row[n] for row in rows]


def galerkin_solve(law: GraphLaw, source: Field, basis: tuple[Field, ...]) -> dict[str, float]:
    """Best field in the span of `basis`, tested against the same basis."""

    if not basis:
        raise ValueError("basis is required")
    stiffness = [[bilinear_form(law, trial, test) for trial in basis] for test in basis]
    rhs = [load(law, source, test) for test in basis]
    coefficients = _solve(stiffness, rhs)
    return {
        node: sum(coefficient * function[node] for coefficient, function in zip(coefficients, basis))
        for node in law.nodes
    }


def path_law(count: int, *, weight: float = 1.0, mass: float = 1.0) -> GraphLaw:
    nodes = tuple(f"n{index}" for index in range(count))
    edges = tuple((nodes[index], nodes[index + 1], weight) for index in range(count - 1))
    return GraphLaw(nodes, edges, mass)


def hat_basis(law: GraphLaw, centers: tuple[int, ...]) -> tuple[dict[str, float], ...]:
    """Piecewise-linear hats on a path, one per center index. They sum to one."""

    if list(centers) != sorted(set(centers)) or centers[0] != 0 or centers[-1] != len(law.nodes) - 1:
        raise ValueError("centers must be increasing and include both ends of the path")
    basis = []
    for position, center in enumerate(centers):
        function = {}
        for index, node in enumerate(law.nodes):
            value = 0.0
            if index == center:
                value = 1.0
            elif position > 0 and centers[position - 1] < index < center:
                previous = centers[position - 1]
                value = (index - previous) / (center - previous)
            elif position < len(centers) - 1 and center < index < centers[position + 1]:
                following = centers[position + 1]
                value = (following - index) / (following - center)
            function[node] = value
        basis.append(function)
    return tuple(basis)


# --- Report records ----------------------------------------------------------


def weak_residual(observed: dict[str, float], expected: dict[str, float], support: tuple[str, ...], weights: dict[str, float] | None = None) -> float:
    """Normalized tested residual of a pointwise mismatch over declared support."""

    if not support:
        raise ValueError("test support is required")
    if set(support) - set(observed) or set(support) - set(expected):
        raise ValueError("support must resolve to observed and expected values")
    weights = weights or dict.fromkeys(support, 1.0)
    total_weight = sum(weights.get(key, 0.0) for key in support)
    if total_weight <= 0.0:
        raise ValueError("positive total weight is required")
    return sum(weights.get(key, 0.0) * (observed[key] - expected[key]) for key in support) / total_weight


def local_failures(observed: dict[str, float], expected: dict[str, float], support: tuple[str, ...], tolerance: float) -> list[str]:
    if tolerance < 0.0:
        raise ValueError("tolerance must be nonnegative")
    weak_residual(observed, expected, support)
    return [key for key in support if abs(observed[key] - expected[key]) > tolerance]


def weak_form_report(observed: dict[str, float], expected: dict[str, float], support: tuple[str, ...], tolerance: float) -> dict[str, object]:
    residual = weak_residual(observed, expected, support)
    failures = local_failures(observed, expected, support, tolerance)
    return {
        "support": list(support),
        "weak_residual": residual,
        "local_failures": failures,
        "passes_aggregate": abs(residual) <= tolerance,
    }
