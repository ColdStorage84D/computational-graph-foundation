# Residual / Error Estimator

## Definition

Residual / error estimator declares how far a state, update, or result is from
satisfying the declared condition.

## Question it answers

How wrong, incomplete, unstable, or unresolved is the current result?

## Depends on core primitives

State, action, constraint, evolution, readout, validation.

## Minimum declaration

- Condition being tested.
- Quantity used to measure mismatch.
- Support where mismatch is measured.
- Acceptable threshold or comparison rule.
- Reported evidence.

## When to use

- Evolution is iterative or approximate.
- A readout needs a quality signal.
- Validation needs more than pass/fail.
- A method should stop only when mismatch is small enough.
- A stationary path claim needs a residual or error record that shows how far
  the candidate is from the declared stationarity condition.

## Common failure

A result is accepted because the process ended, not because the remaining error
was declared and checked.
