"""CGF stochastic transition eval."""

from __future__ import annotations


Distribution = dict[str, float]
Kernel = dict[str, Distribution]


def validate_distribution(distribution: Distribution, tolerance: float = 1e-9) -> None:
    if not distribution:
        raise ValueError("distribution is required")
    if any(value < 0.0 for value in distribution.values()):
        raise ValueError("probabilities must be nonnegative")
    if abs(sum(distribution.values()) - 1.0) > tolerance:
        raise ValueError("distribution must normalize")


def validate_kernel(kernel: Kernel) -> None:
    if not kernel:
        raise ValueError("kernel is required")
    for distribution in kernel.values():
        validate_distribution(distribution)


def predict_distribution(state: str, kernel: Kernel) -> Distribution:
    validate_kernel(kernel)
    if state not in kernel:
        raise ValueError("state missing from kernel")
    return dict(kernel[state])


def push_forward_belief(prior: Distribution, kernel: Kernel) -> Distribution:
    validate_distribution(prior)
    validate_kernel(kernel)
    result: Distribution = {}
    for source, mass in prior.items():
        if source not in kernel:
            raise ValueError("prior state missing from kernel")
        for target, probability in kernel[source].items():
            result[target] = result.get(target, 0.0) + mass * probability
    validate_distribution(result)
    return result


def compose_kernels(first: Kernel, second: Kernel) -> Kernel:
    validate_kernel(first)
    validate_kernel(second)
    composed: Kernel = {}
    for source, middle_distribution in first.items():
        result: Distribution = {}
        for middle, mass in middle_distribution.items():
            if middle not in second:
                raise ValueError("kernel target/source mismatch")
            for target, probability in second[middle].items():
                result[target] = result.get(target, 0.0) + mass * probability
        validate_distribution(result)
        composed[source] = result
    return composed


def score_risk(distribution: Distribution, risk_states: set[str]) -> float:
    validate_distribution(distribution)
    return sum(probability for state, probability in distribution.items() if state in risk_states)


def sample_record(state: str, distribution: Distribution, observed: bool = False) -> dict[str, object]:
    validate_distribution(distribution)
    return {
        "source_state": state,
        "distribution": distribution,
        "status": "observed" if observed else "counterfactual",
    }
