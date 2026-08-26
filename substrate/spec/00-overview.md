# Substrate Spec Overview

The Substrate spec defines the required contract for graph-shaped computational
subjects.

For the full explanation, start with [../concept.md](../concept.md). For a
teaching guide, read [../primitives.md](../primitives.md). For short reference
cards, use [primitive-cards/README.md](primitive-cards/README.md). For concrete
subjects, see [../examples/README.md](../examples/README.md).

## Definition

```text
Substrate is the CGF layer for declaring graph-shaped computational subjects as
graph, typed field, placement, state, action, constraint, evolution, readout,
and validation.
```

## Complete Substrate Subject

A Complete Substrate subject declares all 9 core primitives:

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

All 9 core primitives are required. A subject may be simple, but it is not
complete if any primitive is missing or only implied.

## Spec Pages

Each contract page uses required declaration, allowed examples, validation questions, and common mistakes sections.

- [01-graph-field-placement-state.md](01-graph-field-placement-state.md):
  graph, typed field, placement, and state.
- [02-action-constraint-evolution-readout-validation.md](02-action-constraint-evolution-readout-validation.md):
  action, constraint, evolution, readout, and validation.

## Completion Checklist

Use this checklist before moving a subject into examples, implementations, or
higher CGF layers:

```text
1. Graph: Are entities and relationships declared?
2. Typed field: Are quantities named and typed?
3. Placement: Is every field placed on graph support?
4. State: Are current values declared?
5. Action: Is preferred behavior declared?
6. Constraint: Are invalid states or transitions declared?
7. Evolution: Is state change declared?
8. Readout: Is the domain answer declared?
9. Validation: Are pass/fail checks declared?
```

If the answer to any item is no, the subject is incomplete.
