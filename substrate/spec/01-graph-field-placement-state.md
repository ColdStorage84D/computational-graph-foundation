# Graph, Typed Field, Placement, State

This page defines the contract for the descriptive core primitives. These
primitives say what exists before behavior and result are considered.

## Graph

Graph declares the entities and relationships of the subject.

### Required declaration

- Entity identifiers.
- Relationship identifiers or adjacency.
- Relationship direction when direction changes meaning.
- Labels, types, or weights when they affect behavior.
- Domain identifiers needed to read the subject.

### Allowed examples

- A line of connected nodes.
- Worker-to-task candidate edges.
- Account, device, event, and network-address relationships.
- Customer, cart, SKU, inventory, payment, order, shipment, and notification
  dependencies.

### Validation questions

- Can every relationship be named or inspected?
- Are relationship meanings explicit enough for action and constraint rules?
- Are unrelated records being treated as connected without a declared edge?

### Common mistakes

- Treating a table as a graph without declaring relationships.
- Hiding important relationship meaning in free text.
- Assuming node features define the subject by themselves.

## Typed Field

Typed field declares what kind of quantity lives on the graph.

### Required declaration

- Field name.
- Value kind.
- Shape or category when relevant.
- Domain meaning.
- Allowed placement.

### Allowed examples

- Temperature as a scalar.
- Assignment as a binary value.
- Risk score as a scalar.
- Cart status as a category.
- Item quantity as an integer.

### Validation questions

- Is the field meaning clear without reading application code?
- Are unlike quantities kept as separate fields?
- Is placement declared separately instead of hidden in the field name?

### Common mistakes

- Calling every value a feature.
- Mixing unrelated quantities in one field.
- Treating a type name as enough without domain meaning.

## Placement

Placement declares where a typed field lives on the graph.

### Required declaration

- Field being placed.
- Graph support used by the field.
- Placement kind, such as node, edge, path, region, or mode.
- Scope of the placement.

### Allowed examples

- Temperature placed on nodes.
- Assignment placed on candidate edges.
- Risk placed on account and device nodes.
- Item quantity placed on cart-to-SKU edges.

### Validation questions

- Can every field value point to graph support?
- Are values compared only when their placement is compatible?
- Is placement explicit enough for state, action, and readout?

### Common mistakes

- Leaving placement implicit.
- Mixing node-placed and edge-placed values without saying how.
- Using one field across different supports without declaring scope.

## State

State declares the current values of placed fields.

### Required declaration

- Field values.
- Graph support for each value.
- Current step, sample, or condition when relevant.
- Enough context to know what is being evaluated now.

### Allowed examples

- Current temperature value at each node.
- Current selected assignment edges.
- Current account and device risk values.
- Current cart contents, prices, inventory, payment, and order status.

### Validation questions

- Does every state value correspond to a declared field and placement?
- Are values from different steps kept separate?
- Is predicted state separated from accepted current state?

### Common mistakes

- Declaring a field but no current value.
- Mixing old and new values as one state.
- Treating a proposed or predicted value as current state.

## Rule

Graph, typed field, placement, and state must stay separate. This separation is
what lets a subject be checked before behavior and result are declared.

