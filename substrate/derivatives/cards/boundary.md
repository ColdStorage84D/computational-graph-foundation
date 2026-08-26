# Boundary

## Definition

Boundary declares the fixed, exposed, constrained, or externally contacted parts
of a Substrate subject.

## Question it answers

What part of the subject is held, limited, opened, closed, or connected to
outside conditions?

## Depends on core primitives

Graph, placement, state, constraint, evolution, validation.

## Minimum declaration

- Boundary support on the graph.
- Field values or relations affected by the boundary.
- Whether the boundary is fixed, open, absorbing, reflective, or constrained.
- How evolution treats the boundary.
- Validation checks for boundary violation.

## When to use

- Endpoints, walls, interfaces, clamps, surfaces, or external contact matter.
- State changes differently at the edge of the subject.
- A result is invalid if edge conditions are ignored.

## Common failure

The subject evolves interior state correctly but silently changes values that
were supposed to remain fixed or externally constrained.
