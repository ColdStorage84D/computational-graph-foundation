# Bayesian Filtering Results

Status: `contract-pass`

Eval layer: `value-over-baseline`

Reviewed date: 2026-11-10

Reviewed command:

```powershell
python -m unittest discover -s labs/evals/bayesian-filtering -p "test_*.py"
python labs/evals/bayesian-filtering/comparison.py
```

Reviewed result:

```text
Ran 11 tests
OK
```

## Comparison

Seed 20260103, 200 tracks of 200 steps per regime. Measurement noise variance
4.0, process noise variance 0.05.

Failure mode: a noisy measurement is used directly as the state estimate.
Metric: root mean squared error against the true position.

Matched model: the track moves at the velocity the filter assumes.

| Estimator | RMSE |
| --- | --- |
| Latest raw measurement (baseline) | 2.01 |
| Five-step moving average (baseline) | 2.20 |
| Predict/update filter | 0.68 |

Unmodelled maneuver: the true velocity changes from 1.0 to -2.0 halfway
through and the filter is not told.

| Estimator | RMSE |
| --- | --- |
| Latest raw measurement (baseline) | 2.01 |
| Five-step moving average (baseline) | 3.27 |
| Predict/update filter | 16.77 |

Mean normalized innovation is 0.80 with the matched model and 6.54 with the
unmodelled maneuver.

Pass thresholds, checked by `test_comparison.py`: with the matched model the
filter's error is under half of either baseline; with the wrong model it is
more than five times the raw measurement's, and the normalized innovation is
more than five times larger.

## Where It Does Not Help

A filter is only as good as its model. With a confident, wrong motion model it
is eight times worse than not filtering at all. The innovation is the signal
that says so, which is why the contract keeps it visible.

Claim boundary: a scalar linear-Gaussian filter with known velocity on
simulated tracks. The result covers that filter against those two baselines in
those two regimes. It does not claim a general state-estimation library,
adaptive or multi-model filtering, or tracking performance on real data.
