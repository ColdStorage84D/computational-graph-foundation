"""CGF operator learning eval."""

from __future__ import annotations


Pair = tuple[float, float]


def fit_affine(samples: tuple[Pair, ...]) -> tuple[float, float]:
    if len(samples) < 2:
        raise ValueError("at least two samples are required")
    xs = [x for x, _ in samples]
    ys = [y for _, y in samples]
    x_mean = sum(xs) / len(xs)
    y_mean = sum(ys) / len(ys)
    denom = sum((x - x_mean) ** 2 for x in xs)
    if denom == 0.0:
        raise ValueError("x values must vary")
    slope = sum((x - x_mean) * (y - y_mean) for x, y in samples) / denom
    intercept = y_mean - slope * x_mean
    return slope, intercept


def fit_constant(samples: tuple[Pair, ...]) -> float:
    return sum(y for _, y in samples) / len(samples)


def mse_affine(model: tuple[float, float], samples: tuple[Pair, ...]) -> float:
    slope, intercept = model
    return sum((slope * x + intercept - y) ** 2 for x, y in samples) / len(samples)


def mse_constant(value: float, samples: tuple[Pair, ...]) -> float:
    return sum((value - y) ** 2 for _, y in samples) / len(samples)


def residual(model: tuple[float, float], expected: tuple[float, float]) -> float:
    return abs(model[0] - expected[0]) + abs(model[1] - expected[1])


def uncertainty(train_count: int, heldout_error: float, out_of_domain: bool = False) -> float:
    value = min(1.0, heldout_error + (0.5 if train_count < 3 else 0.0) + (0.5 if out_of_domain else 0.0))
    return value


def promotion_gate(
    candidate_error: float,
    baseline_error: float,
    residual_error: float,
    uncertainty_value: float,
    policy_allowed: bool,
) -> str:
    if not policy_allowed:
        return "reject"
    if residual_error > 0.1:
        return "hold: residual too high"
    if uncertainty_value > 0.4:
        return "hold: uncertainty too high"
    if candidate_error >= baseline_error:
        return "hold: no baseline improvement"
    return "promote_candidate"
