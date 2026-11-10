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


def fisher_quadratic_form(base: Distribution, displacement: dict[str, float]) -> float:
    """Squared length of a small displacement in the Fisher information metric.

    On the probability simplex the metric is sum(d_i ** 2 / p_i). A displacement
    is a tangent vector, so its components must sum to zero.
    """

    validate_distribution(base)
    if set(displacement) != set(base):
        raise ValueError("displacement must share support with the base point")
    if abs(sum(displacement.values())) > 1e-9:
        raise ValueError("a tangent displacement must sum to zero")
    return sum(displacement[key] ** 2 / base[key] for key in base)


def fisher_rao_distance(left: Distribution, right: Distribution) -> float:
    """Geodesic distance under the Fisher metric: 2 * arccos(sum sqrt(p q)).

    Unlike `belief_distance`, the same absolute change counts for more where
    probability is scarce.
    """

    validate_distribution(left)
    validate_distribution(right)
    if set(left) != set(right):
        raise ValueError("distributions must share support")
    affinity = sum(math.sqrt(left[key] * right[key]) for key in left)
    return 2.0 * math.acos(max(-1.0, min(1.0, affinity)))


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
