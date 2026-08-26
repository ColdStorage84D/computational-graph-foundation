# Operator Assembly

## Definition

Operator assembly declares how local graph declarations become a global
transform, matrix, update map, evaluator, or rule application.

## Question it answers

How are local contributions connected into something that can act on state?

## Depends on core primitives

Graph, typed field, placement, action, constraint, evolution, validation.

## Minimum declaration

- Local pieces being assembled.
- Graph supports they attach to.
- Input and output fields.
- Composition rule.
- Checks for placement and constraint compatibility.

## When to use

- Local rules must act together across the graph.
- A method needs a matrix, transform, update map, evaluator, or similar object.
- Validation must inspect assembly errors.

## Common failure

Local rules are applied globally without declaring how their supports, signs,
weights, or field types combine.
