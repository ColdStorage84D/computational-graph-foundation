"""CGF topology-preservation diagnostics for tiny geometric fixtures.

These functions implement a representational diagnostic contract. They do not
model or validate a microscopic physical theory.
"""

from __future__ import annotations

import math


Vector = tuple[float, ...]
Point2D = tuple[float, float]


def _validate_vectors(*vectors: Vector) -> None:
    if not vectors or len(vectors[0]) < 2:
        raise ValueError("vectors must have dimension at least 2")
    dimension = len(vectors[0])
    if any(len(vector) != dimension for vector in vectors):
        raise ValueError("vectors must have the same dimension")
    if any(not math.isfinite(value) for vector in vectors for value in vector):
        raise ValueError("vectors must contain finite values")


def validate_unit_vector(vector: Vector, tolerance: float = 1e-6) -> None:
    """Require an explicitly declared unit carrier."""

    if not math.isfinite(tolerance) or tolerance <= 0.0:
        raise ValueError("tolerance must be positive and finite")
    _validate_vectors(vector)
    norm = math.sqrt(sum(value * value for value in vector))
    if abs(norm - 1.0) > tolerance:
        raise ValueError("unit field vector must have norm 1")


def triangle_structure(
    a: Vector,
    b: Vector,
    c: Vector,
    *,
    degeneracy_threshold: float = 1e-12,
) -> dict[str, float | bool | None]:
    """Return dimension-independent area and angular diagnostics.

    ``area_squared`` is the Gram determinant. ``non_collinearity`` is its
    normalization by the squared edge norms and lies in ``[0, 1]`` when the
    two reference edges are nondegenerate.
    """

    if not math.isfinite(degeneracy_threshold) or degeneracy_threshold <= 0.0:
        raise ValueError("degeneracy threshold must be positive and finite")
    _validate_vectors(a, b, c)
    left = tuple(b_i - a_i for a_i, b_i in zip(a, b))
    right = tuple(c_i - a_i for a_i, c_i in zip(a, c))
    left_norm2 = sum(value * value for value in left)
    right_norm2 = sum(value * value for value in right)
    dot = sum(left_i * right_i for left_i, right_i in zip(left, right))
    scale = left_norm2 * right_norm2
    area_squared = max(0.0, scale - dot * dot)
    valid = scale > degeneracy_threshold
    non_collinearity = min(1.0, area_squared / scale) if valid else None
    return {
        "area_squared": area_squared,
        "non_collinearity": non_collinearity,
        "valid": valid,
    }


def retention_metrics(
    reference: tuple[Vector, Vector, Vector],
    observed: tuple[Vector, Vector, Vector],
    *,
    angular_weight: float = 1.0,
    degeneracy_threshold: float = 1e-12,
) -> dict[str, float | bool]:
    """Compare observed structure with a declared nondegenerate reference."""

    if not math.isfinite(angular_weight) or angular_weight < 0.0:
        raise ValueError("angular weight must be nonnegative and finite")
    reference_structure = triangle_structure(
        *reference, degeneracy_threshold=degeneracy_threshold
    )
    observed_structure = triangle_structure(
        *observed, degeneracy_threshold=degeneracy_threshold
    )
    reference_area = float(reference_structure["area_squared"])
    if reference_area <= degeneracy_threshold:
        raise ValueError("reference triangle must have nonzero structural area")

    observed_area = float(observed_structure["area_squared"])
    area_retention_ratio = observed_area / reference_area
    area_deficit = max(0.0, 1.0 - area_retention_ratio)
    reference_angle = float(reference_structure["non_collinearity"])
    observed_angle_value = observed_structure["non_collinearity"]
    observed_angle = 0.0 if observed_angle_value is None else float(observed_angle_value)
    angular_deficit = max(0.0, reference_angle - observed_angle)
    retention_loss = area_deficit**2 + angular_weight * angular_deficit**2
    retention_deficit = area_deficit + angular_weight * angular_deficit
    return {
        "area_retention_ratio": area_retention_ratio,
        "area_deficit": area_deficit,
        "angular_deficit": angular_deficit,
        "retention_loss": retention_loss,
        "retention_deficit": retention_deficit,
        "observed_valid": bool(observed_structure["valid"]),
    }


def u1_phase_degree(phases: tuple[float, ...], tolerance: float = 1e-6) -> int:
    """Estimate the integer degree of a sampled, nonvanishing U(1) phase.

    Samples must follow one closed support cycle densely enough that every
    wrapped phase increment is unambiguous (strictly smaller than pi).
    """

    if not math.isfinite(tolerance) or tolerance <= 0.0:
        raise ValueError("tolerance must be positive and finite")
    if len(phases) < 3:
        raise ValueError("a phase cycle needs at least three samples")
    if any(not math.isfinite(phase) for phase in phases):
        raise ValueError("phase samples must be finite")

    total = 0.0
    for left, right in zip(phases, phases[1:] + phases[:1]):
        delta = math.atan2(math.sin(right - left), math.cos(right - left))
        if abs(abs(delta) - math.pi) <= tolerance:
            raise ValueError("phase sampling is ambiguous at a pi-sized step")
        total += delta

    degree_value = total / (2.0 * math.pi)
    degree = round(degree_value)
    if abs(degree_value - degree) > tolerance:
        raise ValueError("phase samples do not close to an integer degree")
    return degree


def closed_area_cycle_diagnostic(
    points: tuple[Point2D, ...], tolerance: float = 1e-9
) -> dict[str, float | int | bool | str]:
    """Report a closed-area cycle score, explicitly not a winding number."""

    if not math.isfinite(tolerance) or tolerance <= 0.0:
        raise ValueError("tolerance must be positive and finite")
    if any(len(point) != 2 for point in points):
        raise ValueError("cycle diagnostic requires two-dimensional points")
    if any(not math.isfinite(value) for point in points for value in point):
        raise ValueError("points must contain finite values")
    closed = (
        len(points) >= 4
        and math.dist(points[0], points[-1]) <= tolerance
    )
    signed_area = 0.0
    if closed:
        for left, right in zip(points, points[1:]):
            signed_area += left[0] * right[1] - right[0] * left[1]
        signed_area *= 0.5
    return {
        "estimator": "closed_area_cycle",
        "value": int(closed and abs(signed_area) > tolerance),
        "signed_area": signed_area,
        "closed": closed,
        "exact_topological_invariant": False,
    }


def collapse_risk(
    original_distance: float,
    embedded_distance: float,
    retention_deficit: float,
) -> float:
    """Combine dimensionless compression with reference-relative deficit."""

    if not all(
        math.isfinite(value)
        for value in (original_distance, embedded_distance, retention_deficit)
    ):
        raise ValueError("collapse-risk inputs must be finite")
    if original_distance <= 0.0 or embedded_distance <= 0.0:
        raise ValueError("distances must be positive")
    if retention_deficit < 0.0:
        raise ValueError("retention deficit must be nonnegative")
    compression_ratio = original_distance / embedded_distance
    return compression_ratio * retention_deficit


def topology_evidence_report(
    risk: float,
    n_data_expected: int,
    n_data_observed: int,
    *,
    m_data_expected: int | None = None,
    m_data_observed: int | None = None,
) -> dict[str, object]:
    """Build a bounded evidence record for derivative diagnostics."""

    if not math.isfinite(risk) or risk < 0.0:
        raise ValueError("collapse risk must be nonnegative and finite")
    report: dict[str, object] = {
        "kind": "topology_evidence",
        "collapse_risk": risk,
        "n_data": {
            "estimator": "closed_area_cycle",
            "expected": n_data_expected,
            "observed": n_data_observed,
            "mismatch": abs(n_data_expected - n_data_observed),
            "status": "diagnostic",
            "exact_topological_invariant": False,
        },
        "authority": False,
        "validates_physical_theory": False,
    }
    if (m_data_expected is None) != (m_data_observed is None):
        raise ValueError("m_data expected and observed values must be provided together")
    if m_data_expected is not None and m_data_observed is not None:
        report["m_data"] = {
            "estimator": "sampled_explicit_u1_phase_degree",
            "expected": m_data_expected,
            "observed": m_data_observed,
            "mismatch": abs(m_data_expected - m_data_observed),
            "status": "integer-degree-under-sampling-contract",
        }
    return report
