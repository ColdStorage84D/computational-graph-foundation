# Template Walkthrough

This walkthrough shows how to move from a blank Substrate subject template to a
complete 9-primitive declaration.

The example subject is heat relaxation on a small line graph. The goal is not to
build an implementation. The goal is to show how each template section becomes a
clear Substrate declaration.

## Starting Point

Begin with [subject-template.md](subject-template.md). The template asks for:

```text
Graph
Typed field
Placement
State
Action
Constraint
Evolution
Readout
Validation
```

Do not skip sections. A short answer is acceptable. An implied answer is not.

## 1. Name The Subject

Decision:

```text
Heat Relaxation
```

Why:

```text
The name identifies the physical process being declared, not a tool or method.
```

## 2. Fill Graph

Template question:

```text
What entities and relationships carry the subject?
```

Decision:

```text
Nodes are sample points in a line.
Edges connect neighboring sample points.
```

Filled declaration:

```text
Nodes:
- sample point n0
- sample point n1
- sample point n2
- sample point n3

Edges:
- neighbor: n0 -> n1
- neighbor: n1 -> n2
- neighbor: n2 -> n3
```

Why this is enough:

```text
The graph names the entities and relationships needed to carry temperature.
```

## 3. Fill Typed Field

Template question:

```text
What named quantities live on the graph, and what type does each one have?
```

Decision:

```text
Temperature is the only field.
```

Filled declaration:

```text
Fields:
- temperature: scalar number, heat value at a sample point
```

Why this is enough:

```text
The field has a name, type, and meaning.
```

## 4. Fill Placement

Template question:

```text
Where is each typed field allowed to live?
```

Decision:

```text
Temperature lives on sample point nodes.
```

Filled declaration:

```text
Placement:
- temperature lives on sample point nodes
```

Why this is enough:

```text
Every temperature value has graph support.
```

## 5. Fill State

Template question:

```text
What values are known now?
```

Decision:

```text
Each node starts with one temperature value.
```

Filled declaration:

```text
Current state:
- n0.temperature: 100
- n1.temperature: 60
- n2.temperature: 40
- n3.temperature: 0
```

Why this is enough:

```text
The current values are separated from the desired behavior.
```

## 6. Fill Action

Template question:

```text
What action, cost, law, or objective governs the subject?
```

Decision:

```text
Neighboring temperatures should become smoother.
```

Filled declaration:

```text
Action:
Reduce sharp temperature differences between neighboring sample points.
```

Why this is enough:

```text
The action names what should be reduced.
```

## 7. Fill Constraint

Template question:

```text
What states, transitions, or outputs are not allowed?
```

Decision:

```text
The endpoint temperatures must remain fixed.
```

Filled declaration:

```text
Constraints:
- n0.temperature must remain 100
- n3.temperature must remain 0
```

Why this is enough:

```text
The subject names values that cannot change.
```

## 8. Fill Evolution

Template question:

```text
How does state change across time, steps, attempts, or updates?
```

Decision:

```text
Interior temperatures move toward neighboring temperatures while endpoints stay
fixed.
```

Filled declaration:

```text
Evolution:
- n1.temperature moves toward the temperatures at n0 and n2
- n2.temperature moves toward the temperatures at n1 and n3
- n0.temperature remains fixed
- n3.temperature remains fixed
```

Why this is enough:

```text
The subject states what can change and what cannot change.
```

## 9. Fill Readout

Template question:

```text
What answer is extracted from the subject?
```

Decision:

```text
The answer is the final temperature profile.
```

Filled declaration:

```text
Readout:
- temperature profile: final temperature value at each sample point
```

Why this is enough:

```text
The result is named in domain language and traces back to declared state.
```

## 10. Fill Validation

Template question:

```text
How is the result checked before it is trusted?
```

Decision:

```text
Check fixed endpoints, readable values, and smoother neighboring temperatures.
```

Filled declaration:

```text
Validation:
- n0.temperature is still 100
- n3.temperature is still 0
- every sample point has one readable temperature value
- neighboring temperature differences are not sharper than the starting profile
```

Why this is enough:

```text
The checks describe how the result can pass or fail.
```

## Completed Declaration

The completed Substrate subject can now be written as:

## Graph

Nodes are sample points in a line:

```text
n0 -- n1 -- n2 -- n3
```

Edges connect neighboring sample points.

## Typed field

Temperature is a scalar number that means heat value at a sample point.

## Placement

Temperature lives on sample point nodes.

## State

The current state is:

```text
n0.temperature: 100
n1.temperature: 60
n2.temperature: 40
n3.temperature: 0
```

## Action

Reduce sharp temperature differences between neighboring sample points.

## Constraint

The endpoint temperatures remain fixed:

```text
n0.temperature: 100
n3.temperature: 0
```

## Evolution

Interior temperatures move toward neighboring temperatures while endpoint
temperatures remain fixed.

## Readout

The temperature profile is the final temperature value at each sample point.

## Validation

The result is valid when:

```text
n0.temperature is still 100
n3.temperature is still 0
every sample point has one readable temperature value
neighboring temperature differences are not sharper than the starting profile
```

## Final Check

This subject is complete because it declares:

```text
1. Graph: line of sample points.
2. Typed field: temperature as scalar number.
3. Placement: temperature on nodes.
4. State: current temperature at each node.
5. Action: reduce sharp neighbor differences.
6. Constraint: fixed endpoint temperatures.
7. Evolution: interior values move toward neighbors.
8. Readout: final temperature profile.
9. Validation: endpoint, readability, and smoothness checks.
```
