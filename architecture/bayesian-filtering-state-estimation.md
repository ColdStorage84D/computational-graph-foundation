# Bayesian Filtering / State Estimation

Bayesian Filtering / State Estimation is the Architecture pattern for advancing
a prior belief through a process model and correcting it with measurement
evidence.

## Definition

```text
prior belief
  -> process prediction
  -> measurement update
  -> posterior belief + innovation
  -> proposal evidence
```

The posterior is working belief evidence. It is not durable truth until resolved
through observed outcomes and the normal memory path.

## Minimum Record

```text
prior_ref
process_model_ref
measurement_ref
predicted_state
posterior_state
covariance_or_uncertainty
innovation
evidence_refs
```

## When To Use

- A hidden or noisy state must be estimated over time.
- Measurements arrive with known uncertainty.
- Innovation or residual should affect review, fallback, or proposal quality.
- Stochastic transition and information geometry are already relevant.

## Boundary

Filtering updates belief. It does not prove causality, commit action, or update
durable value by itself.

## Claim Boundary

CGF has a tiny local eval for a one-dimensional linear-Gaussian filter. It does
not claim a general filtering library.

## References

Public sources for the filter the eval implements.

- [A New Approach to Linear Filtering and Prediction Problems](https://doi.org/10.1115/1.3662552), Kalman (1960). The predict and update recursion for linear-Gaussian systems.
- [Bayesian Filtering and Smoothing](https://doi.org/10.1017/CBO9781139344203), Sarkka (2013). A modern treatment of Bayesian filtering, including innovation and consistency checks.
