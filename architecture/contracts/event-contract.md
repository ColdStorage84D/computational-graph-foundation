# Event Contract

## Purpose

An event records that something happened in or around the runtime.

Events are the ordered evidence from which views, traces, projections, and
replay can be built.

## Minimum Record

```text
event id
event type
time or order
actor or emitting role
subject refs
payload summary
evidence refs
correlation id
```

## Validation Questions

```text
1. Is the event ordered?
2. Can it be correlated with later proposals, commits, or outcomes?
3. Does it preserve evidence refs without copying hidden state?
4. Is the event immutable once durable?
```

## Failure Modes

- Events are overwritten.
- Events lack ordering.
- Events cannot be correlated with traces.
- Events copy private data instead of referencing it.

## Boundary

An event is not a proposal, commit, outcome, or memory update by itself.
