# Weak Form

## Definition

Weak form declares a law through tested aggregate conditions instead of direct
pointwise rules.

## Parent layer

Substrate.

## Problem solved

Some subjects cannot reliably declare behavior at every point, sample, or graph
part, but can declare how behavior should hold when tested over support.

## Minimum substrate shape

- Typed field being tested.
- Placement support for the test.
- Test quantity or aggregate condition.
- Action or constraint expressed through the test.
- Validation check for the aggregate condition.

## When to use

- Pointwise rules are too strict, noisy, or unavailable.
- The domain law is naturally expressed over regions or aggregates.
- Approximation quality should be judged by tested conditions.

## When not to use

- Direct local rules are clear and sufficient.
- The test condition is not tied to the subject action or validation.
- The aggregate hides failures that matter locally.

## Maturity

Draft extension.

## Substrate-owned declarations

- Trial field: the typed field being tested.
- Test support: graph region, cell, edge set, basis mode, or aggregate support
  where the law is checked.
- Test function or weight: how local values are aggregated.
- Weak residual: aggregate mismatch that replaces a brittle pointwise rule.
- Boundary and source contribution: terms that enter the tested condition when
  the subject has contact or forcing.

## Validation checks

- The weak residual is computed on declared test support.
- Aggregate satisfaction does not hide local failures that matter to readout.
- Boundary and source terms are included when they affect the tested law.
- Refinement or alternate test supports do not change the result
  unexpectedly.
- The weak form reduces to the local rule when the local rule is valid.

## Failure modes

- Using an aggregate test to hide invalid local behavior.
- Omitting boundary or source terms from the tested condition.
- Choosing test support that has no domain meaning.
- Treating a weak residual as a solver instead of a declaration to validate.
- Failing to state what approximation quality is acceptable.
