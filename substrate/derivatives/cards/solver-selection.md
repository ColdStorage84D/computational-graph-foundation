# Solver Selection

## Definition

Solver selection declares the method shape that fits the declared Substrate
subject and its derivative mechanics.

## Question it answers

What kind of solving method is justified by the subject declaration?

## Depends on core primitives

Graph, typed field, placement, action, constraint, evolution, validation.

## Minimum declaration

- Method family or solving shape.
- Subject features that justify it.
- Constraints the method must respect.
- Error or stopping rule.
- Validation evidence required after use.

## When to use

- More than one method could plausibly apply.
- A method choice changes accuracy, speed, stability, or validity.
- The implementation needs a documented reason for choosing a method.

## Common failure

A method is selected because it is convenient, even though the declared subject
does not justify its assumptions.
