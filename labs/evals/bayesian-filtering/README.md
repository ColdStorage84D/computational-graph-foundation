# Bayesian Filtering Eval

Status: `contract-pass`

This eval tests a tiny one-dimensional linear-Gaussian state estimator:
prediction advances state and uncertainty, measurement update lowers
uncertainty, and innovation remains visible.

## Connections

- Architecture: [Bayesian Filtering / State Estimation](../../../architecture/bayesian-filtering-state-estimation.md).
- Substrate support: [stochastic transition](../../../substrate/extensions/cards/stochastic-transition.md) and [information geometry](../../../substrate/extensions/cards/information-geometry.md).
- Result record: [results.md](results.md).
