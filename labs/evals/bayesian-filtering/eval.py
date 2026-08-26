"""CGF Bayesian filtering eval."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GaussianState:
    mean: float
    covariance: float


def predict(state: GaussianState, velocity: float, dt: float, process_noise: float) -> GaussianState:
    if dt < 0.0 or process_noise < 0.0 or state.covariance < 0.0:
        raise ValueError("invalid prediction parameters")
    return GaussianState(state.mean + velocity * dt, state.covariance + process_noise)


def update(predicted: GaussianState, measurement: float, measurement_noise: float) -> tuple[GaussianState, float, float]:
    if measurement_noise <= 0.0 or predicted.covariance < 0.0:
        raise ValueError("invalid measurement parameters")
    innovation = measurement - predicted.mean
    gain = predicted.covariance / (predicted.covariance + measurement_noise)
    posterior_mean = predicted.mean + gain * innovation
    posterior_covariance = (1.0 - gain) * predicted.covariance
    return GaussianState(posterior_mean, posterior_covariance), innovation, gain


def normalized_innovation(innovation: float, predicted: GaussianState, measurement_noise: float) -> float:
    scale = predicted.covariance + measurement_noise
    if scale <= 0.0:
        raise ValueError("positive innovation scale is required")
    return abs(innovation) / (scale ** 0.5)
