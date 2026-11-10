# Stochastic Transition

## Purpose

Stochastic transition studies transitions whose result is a distribution rather
than one deterministic next state.

Core pattern:

```text
state + context + optional action
  -> transition kernel
  -> distribution over next states or outcomes
```

## Failure Mode

Deterministic evolution hides uncertainty when the subject is probabilistic.

Common failures:

- an average next state hides risk mass;
- a sampled possible future is treated as an observed result;
- source and target state spaces are incompatible;
- kernel uncertainty disappears after composition;
- transition probability is mistaken for causality.

## Minimum Substrate Addition

Minimum records:

```text
state_space
  support_kind
  state_kind
  shape
  type_or_measure_basis

transition_kernel
  source_space_ref
  target_space_ref
  context_refs
  action_refs
  distribution_family
  parameter_refs
  uncertainty
  evidence_refs
```

A deterministic transition is the degenerate case where the distribution puts
all mass on one next state.

## Conceptual Checks

- Kernel outputs normalize.
- Source and target state spaces are compatible.
- Degenerate deterministic kernels are represented correctly.
- Kernel composition preserves uncertainty.
- Risk scoring exposes bad probability mass.
- Samples remain possible outcomes until observed.

## Relationship To Nearby Extensions

- Information geometry compares distributions.
- Causal intervention distinguishes prediction from intervention and
  attribution.
- Port-Hamiltonian flow can use stochastic exchange or loss models.
- Renormalization / coarse-graining can summarize state spaces before kernels
  are estimated.

## Validation Questions

- What source and target state spaces are declared?
- What distribution family is used?
- Does the distribution normalize?
- What risk region should readout expose?
- What uncertainty remains after composition?
- What evidence would update or reject the kernel?

## Maturity

Status: research-supported; CGF-local eval `contract-pass`.

The extension is ready as a card and study. Stronger examples should separate
prediction, sampling, and observed results very clearly.

## CGF Eval Result

See [../../labs/evals/stochastic-transition/results.md](../../labs/evals/stochastic-transition/results.md).

## References

Public source for finite-state transition kernels.

- [Markov Chains](https://doi.org/10.1017/CBO9780511810633), Norris (1997). Transition matrices, composition of kernels, and how a distribution is pushed forward.
