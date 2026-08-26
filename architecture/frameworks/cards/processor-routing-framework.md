# Processor Routing Framework

## Purpose

Use this framework when tasks should route to specialized processors by
declared fit, available evidence, and validation status.

## Reusable Concept

A route registry maps task context to allowed processors. Processor outputs are
bounded records or proposals. A route may be selected, skipped, failed,
deferred, or reviewed.

One global processor should not silently handle every task.

The central rule is fit before score:

```text
task need + evidence availability + view kind + validation status
  -> allowed processors
  -> selected route or abstain/review/defer
```

A processor that removes a quantity through invariance is wrong for a task
where that quantity is the answer. A processor that needs missing evidence is
unavailable, not weak evidence.

## Route States

Routes should record:

```text
allowed
blocked
skipped
unavailable
failed
selected
review
defer
fallback
```

These states keep route choice auditable instead of hiding it inside model
selection.

## Uses CGF Pieces

- execution graph;
- route registry;
- adapters;
- path-conditioned route selection;
- verifier and gate records;
- trace and replay.

## Example Applications

- medical image analysis processor routing;
- feature derivation pipelines;
- robotics perception and control routes;
- ETL and data quality processors;
- search/index update processors.

## When To Use

- Different processors are valid for different task shapes.
- Processor fit depends on invariance, modality, evidence, data quality, or
  policy.
- Missing or failed processors must be visible operational states.
- Route-specific processors may be stronger than a single global processor.
- A robust default should remain available when no validated route wins.

## When Not To Use

- A single deterministic processor is always valid.
- Route choice has no effect on output, risk, or review.
- Processor failures can safely be treated as ordinary absence of evidence.

## Boundary

Processor output is not accepted truth. It becomes evidence, a proposal, or a
bounded derived record that still passes through verifier and commit rules when
action or review state changes.

## Implementation Posture

Future code should keep route decisions deterministic or auditable and should
record skipped, unavailable, failed, and deferred route states.

Validation should prefer a route only when the route has enough evidence over
the default or fallback. Chasing tiny unvalidated score differences should not
be treated as a supported promotion.
