# Trace Contract

## Purpose

A trace reconstructs the operating path from event to view to proposal to
commit to outcome and memory update.

Trace is the explanation surface for audit and review.

## Minimum Record

```text
trace id
input event refs
view refs
route trace path, when a spine is used
subgraph capsule refs, when used
proposal refs
path context refs, when used
path-conditioned effect, when used
path gate weight or decision, when used
path gate blocked reasons, when used
verification refs
verifier basis
commit ref
execution refs
outcome refs
memory update refs
memory role, when known
promotion or quarantine refs, when used
counterfactual proposal refs
```

## Validation Questions

```text
1. Can the trace reconstruct the accepted path?
2. Can it show rejected alternatives when needed?
3. Can it show path context, gate weight or decision, and blocked reasons when used?
4. Can it resolve outcome attribution?
5. Can it be rebuilt from durable records?
```

## Failure Modes

- Trace is hand-written and not reconstructable.
- Trace hides rejected proposals.
- Trace hides path-conditioned influence or path-gated blocking.
- Trace copies large artifacts instead of referencing them.
- Outcome cannot be attributed to a committed path.

## Boundary

Trace is evidence of operation. It is not value memory by itself.
