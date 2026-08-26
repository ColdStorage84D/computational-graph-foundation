# Event Log, Trace, And Replay

## Purpose

This pattern makes Architecture operation auditable and reconstructable.

## Distinctions

| Concept | Meaning |
| --- | --- |
| Event log | Ordered records of what happened. |
| Trace | A projection that links events, views, proposals, commits, outcomes, and graph runtime memory updates. |
| Replay | Rebuilding projections from durable records. |
| Persistence | The storage discipline that keeps replay possible. |

## Rules

- Durable state should be reconstructable from events or explicit persisted
  records.
- Trace is evidence of operation, not graph runtime memory by itself.
- Replay should not silently rewrite history.
- Projections are derived views, not hidden truth.
- Large artifacts should be referenced, not copied into every trace.

## Minimal Trace

```text
input event
runtime view
proposals considered
path context refs, when used
path gate weight or result, when used
verification result
commit decision
execution result, if any
outcome
eligibility resolution
memory update
replay projection
```

## Validation Questions

```text
1. Can the trace reconstruct why the decision happened?
2. Are rejected proposals visible when needed?
3. Can path-conditioned effects and path-gated weights or decisions be reconstructed?
4. Can replay rebuild the same projection?
5. Are references stable enough for audit?
6. Are failures represented as events or outcomes?
```
