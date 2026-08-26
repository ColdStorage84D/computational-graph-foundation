# Source

## Definition

Source declares a quantity that is injected, removed, emitted, observed, or
externally supplied to the subject.

## Question it answers

What enters or leaves the subject, and where does it affect state?

## Depends on core primitives

Typed field, placement, state, action, evolution, validation.

## Minimum declaration

- Source field or quantity.
- Graph support where it enters or leaves.
- Sign or direction of contribution.
- Rate, amount, schedule, or condition.
- Validation check for source accounting.

## When to use

- State changes because of injection, removal, demand, supply, observation, or
  forcing.
- Action depends on external contribution.
- Validation must account for conservation or accounting rules.

## Common failure

State changes are attributed to evolution even though an external quantity was
never declared.
