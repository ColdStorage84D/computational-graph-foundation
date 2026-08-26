# Sheaf Consistency

## Definition

Sheaf consistency declares agreement rules for local assignments over
overlapping graph support.

## Parent layer

Substrate.

## Problem solved

Local field assignments can look valid in isolation but disagree where their
supports overlap.

## Minimum substrate shape

- Local assignments.
- Supports and overlaps.
- Restriction or compatibility rule.
- Constraint or validation condition for agreement.
- Readout behavior when disagreement remains.

## When to use

- Local views, partial observations, or regional declarations overlap.
- Agreement across overlaps matters.
- Validation must detect inconsistent local assignments.

## When not to use

- The subject has one global assignment with no overlap.
- Local disagreement is acceptable.
- The compatibility rule is unclear.

## Maturity

Research extension.

## Substrate-owned declarations

- Local view: partial assignment over a declared support.
- Support: node, edge, region, path, cell, mode, or other graph support where a
  local view is valid.
- Overlap: shared support between two or more local views.
- Restriction map: how a local view is compared on the overlap.
- Consistency residual: mismatch after restrictions are applied.
- Gluing candidate: proposed global assignment built from compatible local
  views.
- Obstruction: reason local views cannot be glued.

## Validation checks

- Every local view declares its support.
- Overlap comparisons use declared restriction maps.
- Residual thresholds are explicit and tied to readout or validation.
- Failed gluing reports an obstruction rather than silently merging.
- A global assignment is accepted only when local consistency is adequate.

## Failure modes

- Merging partial views because each is locally valid.
- Comparing overlapping views without a restriction rule.
- Ignoring small residuals that accumulate into a global contradiction.
- Treating a gluing candidate as truth before validation.
- Using sheaf language when there are no meaningful overlaps.
