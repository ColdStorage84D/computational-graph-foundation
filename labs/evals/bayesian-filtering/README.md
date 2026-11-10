# Bayesian Filtering Eval

Status: `contract-pass`

This eval tests a one-dimensional linear-Gaussian state estimator: prediction
advances state and uncertainty, a measurement update lowers uncertainty, and
the innovation stays visible.

## Comparison

`comparison.py` simulates noisy position tracks and compares three estimators
by root mean squared error: the latest raw measurement, a five-step moving
average, and the filter. One regime matches the filter's motion model. The
other changes the true velocity halfway through without telling the filter.

## Connections

- Architecture: [Bayesian Filtering / State Estimation](../../../architecture/bayesian-filtering-state-estimation.md).
- Substrate support: [stochastic transition](../../../substrate/extensions/cards/stochastic-transition.md) and [information geometry](../../../substrate/extensions/cards/information-geometry.md).
- Result record: [results.md](results.md).

## Files

- [eval.py](eval.py): the implementation under test.
- [test_eval.py](test_eval.py): contract tests.
- [comparison.py](comparison.py): seeded comparison against the baseline.
- [test_comparison.py](test_comparison.py): thresholds for the comparison.
