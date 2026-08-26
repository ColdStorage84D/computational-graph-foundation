# Renormalization / Coarse-Graining

## Definition

Renormalization / coarse-graining declares how a fine subject maps to a coarser
subject while preserving selected meaning.

## Parent layer

Substrate.

## Problem solved

Large or multiscale subjects can lose important behavior when simplified unless
the fine-to-coarse relation is explicit.

## Minimum substrate shape

- Fine graph support.
- Coarse graph support.
- Field aggregation or projection rule.
- Action, constraint, readout, or validation relation to preserve.
- Error or loss check for simplification.

## When to use

- A subject has multiple useful scales.
- Simplification is needed for inspection or computation.
- Readout must remain meaningful after aggregation.

## When not to use

- The original scale is already small enough.
- Coarsening destroys the property being studied.
- There is no validation check for coarse behavior.

## Maturity

Research extension.

## Substrate-owned declarations

- Fine support: detailed graph, fields, action, constraints, and readout.
- Coarse support: aggregated graph or lower-resolution subject.
- Projection rule: how fine state maps to coarse state.
- Lift or reconstruction rule: optional route from coarse state back to fine
  support.
- Effective action or operator: coarse rule meant to preserve selected fine
  behavior.
- Scale residual: mismatch between fine and coarse readouts, actions, or
  invariants.

## Validation checks

- Coarse readout agrees with the fine readout within declared tolerance.
- Preserved invariants remain valid after projection.
- Coarse evolution approximates projected fine evolution where claimed.
- Repeated coarse-graining does not produce uncontrolled drift.
- Lost detail is named instead of hidden.

## Failure modes

- Aggregating graph structure while pretending no behavior changed.
- Preserving average behavior while losing the rare state that matters.
- Comparing fine and coarse subjects with no projection rule.
- Reusing a coarse operator outside its scale validity.
- Treating coarse-graining as compression only, without validation.
