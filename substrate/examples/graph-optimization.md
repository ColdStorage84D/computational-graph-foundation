# Graph Optimization

This is the second teaching example for the 9 core Substrate primitives. It
shows that Substrate is not limited to physical smoothing problems.

## Graph

A small assignment graph with tasks and workers:

```text
workers: w0, w1
tasks:   t0, t1, t2

candidate edges:
  w0 -> t0
  w0 -> t1
  w1 -> t1
  w1 -> t2
```

## Typed field

Assignment is a binary typed field. A candidate edge is either selected or not
selected.

## Placement

Assignment is placed on candidate edges. Each candidate edge carries one
assignment value.

## State

The current state is one assignment value per candidate edge:

```text
w0 -> t0: 1
w0 -> t1: 0
w1 -> t1: 1
w1 -> t2: 0
```

## Action

Lower-cost assignments are preferred. A selected edge contributes its assignment
cost to the total score.

## Constraint

Each task can be assigned at most once, and each worker can receive only allowed
tasks.

## Evolution

The state changes by trying a different valid edge selection and keeping a
candidate when it improves the score without violating constraints.

## Readout

The domain answer is the best valid assignment and its score.

## Validation

Every selected edge must be allowed, each task must appear at most once, and the
reported score must match the selected edges.

The purpose is not to define a full optimizer. The purpose is to show how graph,
typed field, placement, state, action, constraint, evolution, readout, and
validation can describe an optimization subject in the same shape as the heat
example.
