# Heat Relaxation

This is the first teaching example for the 9 core Substrate primitives.

## Graph

A line of connected nodes:

```text
n0 -- n1 -- n2 -- n3
```

## Typed field

Temperature is a scalar typed field.

## Placement

Temperature is placed on nodes. Each node carries one temperature value.

## State

The current state is one temperature value per node:

```text
n0: 100
n1:  60
n2:  40
n3:   0
```

## Action

Neighboring temperatures should become smoother.

## Constraint

The first node remains hot and the last node remains cold.

## Evolution

Interior node temperatures move toward neighboring temperatures while endpoint
constraints remain fixed.

## Readout

The final temperature profile is the domain answer.

## Validation

The endpoint temperatures remain unchanged, the update remains stable, and the
final profile is readable as a temperature value at each node.

The purpose is not to build a full physics engine. The purpose is to show how a
graph, typed field, placement, state, action, constraint, evolution, readout,
and validation can be declared in one place.
