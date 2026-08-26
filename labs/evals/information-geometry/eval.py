"""CGF information geometry eval."""

from __future__ import annotations

import math


Distribution = dict[str, float]


def validate_distribution(distribution: Distribution) -> None:
    if not distribution:
        raise ValueError("distribution is required")
    if any(value <= 0.0 for value in distribution.values()):
        raise ValueError("probabilities must be positive for this eval")
    if abs(sum(distribution.values()) - 1.0) > 1e-9:
        raise ValueError("distribution must normalize")


def kl_divergence(left: Distribution, right: Distribution) -> float:
    validate_distribution(left)
    validate_distribution(right)
    if set(left) != set(right):
        raise ValueError("distributions must share support")
    return sum(left[key] * math.log(left[key] / right[key]) for key in left)


def entropy(distribution: Distribution) -> float:
    validate_distribution(distribution)
    return -sum(value * math.log(value) for value in distribution.values())


def surprise(distribution: Distribution, observed: str) -> float:
    validate_distribution(distribution)
    if observed not in distribution:
        raise ValueError("observed state missing")
    return -math.log(distribution[observed])


def belief_distance(left: Distribution, right: Distribution) -> float:
    validate_distribution(left)
    validate_distribution(right)
    if set(left) != set(right):
        raise ValueError("distributions must share support")
    return math.sqrt(sum((left[key] - right[key]) ** 2 for key in left))


def information_gain(prior: Distribution, posterior: Distribution) -> float:
    return kl_divergence(posterior, prior)


def calibration_error(predicted: Distribution, observed: str) -> float:
    validate_distribution(predicted)
    if observed not in predicted:
        raise ValueError("observed state missing")
    return 1.0 - predicted[observed]


def tail_risk_mass(distribution: Distribution, risk_states: set[str]) -> float:
    validate_distribution(distribution)
    missing = risk_states - set(distribution)
    if missing:
        raise ValueError("risk states missing from distribution")
    return sum(distribution[state] for state in risk_states)
