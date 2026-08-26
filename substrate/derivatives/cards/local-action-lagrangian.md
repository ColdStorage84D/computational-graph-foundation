# Local Action / Lagrangian

## Definition

Local action / Lagrangian declares graph-local contributions that combine into
the subject action.

## Question it answers

What local terms define the law, cost, energy, loss, or objective?

## Depends on core primitives

Graph, typed field, placement, state, action, constraint.

## Minimum declaration

- Local support for each term.
- Fields used by each term.
- Term meaning and sign.
- How local terms combine.
- Constraints that affect the terms.

## When to use

- A global action should be built from node, edge, cell, region, or interaction
  terms.
- Local contributions need to be inspected independently.
- Evolution or validation depends on local contribution size.
- A stationary path or least-action condition needs local terms before
  admissible variation can be checked.

## Common failure

The action is named globally, but no local contributions explain where the
behavior comes from.
