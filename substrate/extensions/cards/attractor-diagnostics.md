# Attractor Diagnostics

## Definition

Attractor Diagnostics declares dynamical-regime evidence for time-indexed graph
subjects, such as recurrence, cycle signature, local expansion, regime distance,
and escape warning.

## Parent layer

Substrate.

## Problem solved

Time-series or trajectory subjects can look locally stable while their
dynamical regime is drifting, folding, escaping, or becoming unstable.

## Minimum substrate shape

- Complete 9-core subject with time-indexed or step-indexed state.
- Declared state samples or field observations.
- Regime, recurrence, cycle, expansion, or distance evidence derived from the
  declared state.
- Action, readout, or validation that uses the diagnostic.
- Uncertainty or warning record when the diagnostic is weak.

## When to use

- The subject has repeated, cyclic, phase-like, or regime-like behavior.
- A stable-looking local state can hide regime drift.
- A transition, escape, anomaly, or collapse risk matters to readout.
- Delay embedding, recurrence, or local expansion is meaningful for the data.

## When not to use

- The subject is not temporal or sequential.
- A single-step state is enough for validation.
- The diagnostic cannot be tied to declared state and support.
- The result would be treated as a final truth instead of warning evidence.

## Maturity

Research extension. No direct Labs eval yet.

## Validation checks

- Diagnostic inputs resolve to declared state or field support.
- Regime labels or warnings preserve uncertainty.
- Escape warnings are readout evidence, not proof of failure.
- Cycle or recurrence evidence is not forced when the subject is chaotic,
  sparse, or under-sampled.

## Failure modes

- Calling noise an attractor.
- Using under-sampled trajectories without uncertainty.
- Treating a warning score as a hard conclusion.
- Adding dynamical vocabulary when the subject only needs ordinary evolution.
