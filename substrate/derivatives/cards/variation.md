# Variation

## Definition

Variation declares the allowed changes to fields or state used to derive a
condition, direction, or update.

## Question it answers

What may change when asking how the action responds?

## Depends on core primitives

Typed field, placement, state, action, constraint, evolution.

## Minimum declaration

- Field or state component being varied.
- Allowed support for the change.
- Constraints that restrict the change.
- Quantity being tested against the change.
- Expected condition or direction.

## When to use

- An action should imply an equilibrium, gradient, update direction, or
  admissible change.
- A stationary path or least-action condition needs a clear admissible
  variation before any first-order claim is meaningful.
- Constraints limit which changes are allowed.
- Validation needs to know whether a change was legitimate.

## Common failure

Every field is treated as freely changeable even when placement or constraints
make some changes invalid.
