"""CGF weak form eval."""

from __future__ import annotations


def weak_residual(observed: dict[str, float], expected: dict[str, float], support: tuple[str, ...], weights: dict[str, float] | None = None) -> float:
    if not support:
        raise ValueError("test support is required")
    if set(support) - set(observed) or set(support) - set(expected):
        raise ValueError("support must resolve to observed and expected values")
    weights = weights or {key: 1.0 for key in support}
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
