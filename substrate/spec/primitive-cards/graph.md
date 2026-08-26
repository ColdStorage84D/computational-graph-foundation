# Graph

## One Sentence

Graph declares the entities and relationships of the computational subject.

## Question It Answers

What things exist, and how can they affect each other?

## Required Status

Core. Required for every Substrate subject.

## Minimum Declaration

- Entity identifiers.
- Relationship identifiers or adjacency.
- Relationship direction when direction changes meaning.
- Labels, types, or weights when they affect behavior.
- Domain identifiers needed to read the subject.

## Allowed Examples

- Nodes connected in a line.
- Worker-to-task candidate edges.
- Accounts connected to devices and activity records.
- Customer, cart, item, payment, order, and shipment dependencies.

## Validation Questions

- Can every entity be identified?
- Can every relationship be inspected?
- Is relationship meaning explicit enough for action and constraint rules?
- Are unrelated records kept separate unless a relationship is declared?

## Common Mistakes

- Treating a table as a graph without declaring relationships.
- Hiding relationship meaning in free text.
- Assuming values alone define the subject.
- Using edges without saying what they mean.

## Heat Example

The graph is a line of connected nodes:

```text
n0 -- n1 -- n2 -- n3
```

## Related Core Primitives

Typed field, placement, constraint, evolution, readout.

