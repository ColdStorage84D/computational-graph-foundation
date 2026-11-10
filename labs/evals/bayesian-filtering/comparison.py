"""Value-over-baseline comparison for scalar Bayesian filtering.

Failure mode: a noisy measurement is used directly as the state estimate.

Baselines: the latest raw measurement, and a short moving average. Variant: the
predict/update filter from `eval.py`.

Two regimes. In the first the filter's model matches the process. In the
second the true velocity jumps part-way through and the filter is not told; a
filter with a confident, wrong model should lose, and its innovation should
say so.
"""

from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path
import random
import sys


def _load_eval():
    name = "cgf_bayesian_filtering_eval"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name("eval.py"))
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ev = _load_eval()

DT = 1.0
STEPS = 200
MEASUREMENT_NOISE = 4.0  # variance
PROCESS_NOISE = 0.05  # variance per step
ASSUMED_VELOCITY = 1.0
WINDOW = 5


def simulate_track(rng: random.Random, *, maneuver: bool):
    position = 0.0
    truth, measurements = [], []
    for step in range(STEPS):
        velocity = ASSUMED_VELOCITY
        if maneuver and step >= STEPS // 2:
            velocity = -2.0
        position += velocity * DT + rng.gauss(0.0, math.sqrt(PROCESS_NOISE))
        truth.append(position)
        measurements.append(position + rng.gauss(0.0, math.sqrt(MEASUREMENT_NOISE)))
    return truth, measurements


def run_track(truth: list[float], measurements: list[float]) -> dict[str, float]:
    state = ev.GaussianState(0.0, 10.0)
    squared = {"raw_measurement": 0.0, "moving_average": 0.0, "filter": 0.0}
    innovation_total = 0.0
    for step, (actual, measured) in enumerate(zip(truth, measurements)):
        predicted = ev.predict(state, velocity=ASSUMED_VELOCITY, dt=DT, process_noise=PROCESS_NOISE)
        state, innovation, _ = ev.update(predicted, measured, MEASUREMENT_NOISE)
        innovation_total += ev.normalized_innovation(innovation, predicted, MEASUREMENT_NOISE)
        window = measurements[max(0, step - WINDOW + 1) : step + 1]
        squared["raw_measurement"] += (measured - actual) ** 2
        squared["moving_average"] += (sum(window) / len(window) - actual) ** 2
        squared["filter"] += (state.mean - actual) ** 2
    result = {name: total / len(truth) for name, total in squared.items()}
    result["mean_normalized_innovation"] = innovation_total / len(truth)
    return result


def run_regime(*, maneuver: bool, seed: int = 20260103, tracks: int = 200) -> dict[str, float]:
    rng = random.Random(seed)
    totals: dict[str, float] = {}
    for _ in range(tracks):
        truth, measurements = simulate_track(rng, maneuver=maneuver)
        for name, value in run_track(truth, measurements).items():
            totals[name] = totals.get(name, 0.0) + value
    report = {}
    for name, total in totals.items():
        mean = total / tracks
        key = name if name == "mean_normalized_innovation" else f"rmse_{name}"
        report[key] = round(mean if name == "mean_normalized_innovation" else math.sqrt(mean), 4)
    return report


def run_comparison(*, seed: int = 20260103, tracks: int = 200) -> dict[str, object]:
    return {
        "seed": seed,
        "tracks_per_regime": tracks,
        "steps_per_track": STEPS,
        "matched_model": run_regime(maneuver=False, seed=seed, tracks=tracks),
        "unmodelled_maneuver": run_regime(maneuver=True, seed=seed, tracks=tracks),
    }


if __name__ == "__main__":
    print(json.dumps(run_comparison(), indent=2))
