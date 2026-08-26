# Placement

## One Sentence

Placement declares where a typed field lives on the graph.

## Question It Answers

Where does each quantity live?

## Required Status

Core. Required for every Substrate subject.

## Minimum Declaration

- Field being placed.
- Graph part that carries the field.
- Placement kind, such as node, edge, path, region, or mode.
- Scope of the placement.

## Allowed Examples

- Temperature placed on nodes.
- Assignment placed on candidate edges.
- Risk placed on account and device nodes.
- Item quantity placed on cart-to-item edges.
- Status placed on order nodes.

## Validation Questions

- Can every field value point to a graph part?
- Are values compared only when placement is compatible?
- Is placement explicit enough for state, action, and readout?
- Is the placement scope clear?

## Common Mistakes

- Leaving placement implicit.
- Mixing node-placed and edge-placed values without saying how.
- Reusing one field across different graph parts without scope.
- Treating placement as a display detail.

## Heat Example

Temperature is node-placed. Each node carries one temperature value.

## Related Core Primitives

Graph, typed field, state, action, validation.

