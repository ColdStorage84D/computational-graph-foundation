# Substrate Core Primitives

This guide explains only the 9 mandatory Substrate primitives:

```text
graph
typed field
placement
state
action
constraint
evolution
readout
validation
```

A complete Substrate subject must declare all 9. Other mechanics and optional
concepts are left for later documents.

## Graph

### Definition

Graph declares the entities and relationships of the subject.

### Question it answers

What things exist, and how can they affect each other?

### Minimum declaration

- Node identities.
- Edge identities or adjacency.
- Labels or types when they change meaning.
- Weights or directions when they affect behavior.
- Connectivity structure needed by the subject.

### Heat-relaxation example

A line of connected nodes:

```text
n0 -- n1 -- n2 -- n3
```

### Common mistakes

- Treating an arbitrary table as a graph without declaring relationships.
- Hiding important relationship types in unstructured labels.
- Assuming node features are enough to define the subject.

### Related core primitives

Typed field, placement, constraint, evolution, readout.

## Typed Field

### Definition

Typed field declares what kind of quantity lives on the graph.

### Question it answers

What values exist on the subject?

### Minimum declaration

- Field name.
- Value kind.
- Shape or rank when relevant.
- Meaning in the domain.
- Allowed placement.

### Heat-relaxation example

Temperature is a scalar typed field.

### Common mistakes

- Calling every value a feature without explaining its meaning.
- Mixing unlike quantities as if they had the same type.
- Letting a field imply placement instead of declaring placement separately.

### Related core primitives

Graph, placement, state, action, readout, validation.

## Placement

### Definition

Placement declares where a typed field lives on the graph.

### Question it answers

Where does each quantity live?

### Minimum declaration

- Field being placed.
- Graph support.
- Placement kind, such as node, edge, path, region, or mode.
- Scope of the placement.

### Heat-relaxation example

Temperature is node-placed: each node carries one temperature value.

### Common mistakes

- Treating node-placed and edge-placed values as interchangeable.
- Leaving placement implicit in field names.
- Combining values whose supports do not match.

### Related core primitives

Graph, typed field, state, action, validation.

## State

### Definition

State declares the current values of placed fields.

### Question it answers

What values does the subject have now?

### Minimum declaration

- Field values.
- The graph support for those values.
- A step, tick, sample, or episode marker when needed.
- The current condition being evaluated.

### Heat-relaxation example

Each node has a current temperature:

```text
n0: 100
n1:  60
n2:  40
n3:   0
```

### Common mistakes

- Declaring fields but no actual values.
- Mixing values from different steps as one state.
- Treating predicted values as accepted state without validation.

### Related core primitives

Typed field, placement, action, evolution, readout, validation.

## Action

### Definition

Action declares the cost, law, objective, loss, risk, or preference that governs
the subject.

### Question it answers

What behavior is preferred, minimized, preserved, explained, or optimized?

### Minimum declaration

- Terms being evaluated.
- Fields involved.
- Graph support involved.
- Direction of preference.
- Domain meaning of the action.

### Heat-relaxation example

Neighboring temperatures should become smoother.

### Common mistakes

- Running updates without saying what behavior they serve.
- Treating a score as meaningful without explaining what it measures.
- Mixing unrelated objectives without declaring how they interact.

### Related core primitives

State, constraint, evolution, readout, validation.

## Constraint

### Definition

Constraint declares what must not be violated.

### Question it answers

What states, changes, or answers are invalid?

### Minimum declaration

- Rule being enforced.
- Scope of the rule.
- Whether it rejects or penalizes.
- What failure means.

### Heat-relaxation example

The first node remains hot and the last node remains cold.

### Common mistakes

- Encoding a hard rule as an ordinary preference.
- Declaring constraints but never checking them.
- Letting constraints conflict without naming the conflict.

### Related core primitives

Graph, state, action, evolution, validation.

## Evolution

### Definition

Evolution declares how state changes.

### Question it answers

How does the subject move from one state to another?

### Minimum declaration

- Current state.
- Update rule.
- Inputs used by the update.
- Resulting state.
- Checks that must hold after the update.

### Heat-relaxation example

Interior node temperatures move toward neighboring temperatures while endpoint
constraints remain fixed.

### Common mistakes

- Changing state without declaring the rule.
- Allowing updates to violate constraints.
- Confusing one update step with the final answer.

### Related core primitives

State, action, constraint, readout, validation.

## Readout

### Definition

Readout declares the answer extracted from state or a sequence of states.

### Question it answers

What result does the domain need?

### Minimum declaration

- Input state or sequence.
- Output type.
- Domain interpretation.
- How the answer should be consumed.

### Heat-relaxation example

The final temperature profile is the readout.

### Common mistakes

- Producing internal state without a domain answer.
- Returning a number without explaining what it means.
- Letting readout logic change the subject after evolution.

### Related core primitives

State, evolution, validation.

## Validation

### Definition

Validation declares how the subject and result are checked.

### Question it answers

How do we know the result is acceptable?

### Minimum declaration

- What is checked.
- When it is checked.
- What passes.
- What fails.
- What evidence is reported.

### Heat-relaxation example

The fixed endpoint temperatures remain unchanged, the update remains stable, and
the final profile is readable as a temperature value at each node.

### Common mistakes

- Treating output as valid just because a process finished.
- Checking only the final answer and ignoring invalid intermediate states.
- Using vague success language instead of explicit pass/fail checks.

### Related core primitives

Constraint, state, evolution, readout.
