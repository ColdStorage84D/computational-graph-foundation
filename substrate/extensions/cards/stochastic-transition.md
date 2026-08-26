# Stochastic Transition

## Definition

Stochastic transition declares uncertain state change.

## Parent layer

Substrate.

## Problem solved

Some subjects cannot declare a single deterministic next state, but still need
state change to be typed, placed, constrained, and validated.

## Minimum substrate shape

- State being changed.
- Possible next states or distribution family.
- Conditions affecting transition likelihood.
- Constraints that all possible changes must respect.
- Validation check for uncertainty quality.

## When to use

- Randomness, uncertainty, risk, noise, or sampling is part of the subject.
- Readout depends on probability, expectation, or uncertainty.
- Validation must check calibration or admissible uncertainty.

## When not to use

- A deterministic transition is adequate.
- Uncertainty is only a missing-data excuse.
- There is no way to validate the uncertainty claim.

## Maturity

Draft extension.

## Substrate-owned declarations

- State space: valid current and next-state support.
- Transition kernel: distribution over next state given current state,
  condition, action, or context.
- Kernel source and target: where the transition starts and where probability
  mass may land.
- Pushforward rule: how a distribution over current state becomes a
  distribution over next state.
- Uncertainty metadata: confidence, variance, calibration status, sampling
  rule, or known model limits.

## Validation checks

- Transition probabilities are normalized and nonnegative where required.
- Samples or next-state distributions respect graph support and constraints.
- Deterministic transitions appear as a valid special case.
- Calibration, likelihood, or held-out transition checks are stated when
  probability is used for readout.
- Composed kernels keep the source and target spaces compatible.

## Failure modes

- Using probability to disguise missing state declarations.
- Predicting impossible next states.
- Treating uncertainty as causal authority.
- Mixing state spaces without an explicit target support.
- Reporting expected readout without preserving risk or tail behavior.
