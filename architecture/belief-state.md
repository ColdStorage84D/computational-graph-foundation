# Belief State

Belief State is the Architecture pattern for carrying uncertainty, confidence,
calibration, evidence weight, and distribution references through operating
records.

## Definition

```text
evidence -> belief state -> proposal evidence -> outcome comparison
```

A belief state is not just a number. It may include confidence, uncertainty,
source weight, calibration status, distribution reference, and update basis.

## Minimum Record

```text
belief_id
subject_ref
support_ref
confidence
uncertainty
evidence_refs
distribution_ref
calibration_ref
updated_from_refs
```

## When To Use

- A proposal relies on uncertain evidence.
- Several processors or lenses disagree.
- Later outcomes should calibrate earlier forecasts.
- Distribution structure is important enough to use the Information Geometry
  extension.

## Boundary

Belief state is evidence. It cannot replace verification, policy gates, commit
authority, or observed outcomes.

## Claim Boundary

CGF has Substrate support through stochastic transition and information
geometry evals. This Architecture guide defines operating use only.
