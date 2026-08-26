# Substrate Subject Template

Use this template to declare one graph-shaped computational subject. Fill every
section before promoting the subject into an example, application, or code.

Keep this document focused on what is computed. Do not use it to define package
layout, service design, or how work is run.

## Subject Name

Fill in:

```text
<short subject name>
```

Minimum standard:

```text
The name should identify the domain object or process being declared.
```

Common failure:

```text
The name describes an implementation technique instead of the subject.
```

## Graph

Purpose:

```text
Declare the entities and relationships that carry the subject.
```

Fill in:

```text
Nodes:
- <node type>
- <node type>

Edges:
- <edge type>: <from> -> <to>
- <edge type>: <from> -> <to>
```

Minimum standard:

```text
The graph names the entities and relationships needed for the computation.
```

Common failure:

```text
The graph is only called "a graph" without naming its nodes and edges.
```

## Typed field

Purpose:

```text
Declare the named quantities that live on the graph and what type each one has.
```

Fill in:

```text
Fields:
- <field name>: <type>, <meaning>
- <field name>: <type>, <meaning>
```

Minimum standard:

```text
Each field has a name, type, and meaning.
```

Common failure:

```text
Values are listed without saying what type they have or what they mean.
```

## Placement

Purpose:

```text
Declare where each typed field is allowed to live on the graph.
```

Fill in:

```text
Placement:
- <field name> lives on <node type or edge type>
- <field name> lives on <node type or edge type>
```

Minimum standard:

```text
Every typed field is assigned to graph support.
```

Common failure:

```text
A field is declared but there is no clear place where it lives.
```

## State

Purpose:

```text
Declare the current values of the typed fields.
```

Fill in:

```text
Current state:
- <field name>: <current value or value rule>
- <field name>: <current value or value rule>
```

Minimum standard:

```text
The subject says what values are known now, even if some are unknown or pending.
```

Common failure:

```text
State is mixed with desired behavior instead of describing current values.
```

## Action

Purpose:

```text
Declare the action, cost, law, or objective that governs the subject.
```

Fill in:

```text
Action:
<one or more sentences describing the preferred behavior>
```

Minimum standard:

```text
The subject states what should be improved, followed, reduced, preserved, or
selected.
```

Common failure:

```text
The action says "compute the answer" without naming what governs the computation.
```

## Constraint

Purpose:

```text
Declare what states, transitions, or outputs are not allowed.
```

Fill in:

```text
Constraints:
- <constraint>
- <constraint>
```

Minimum standard:

```text
Invalid states or outputs are named clearly enough to reject them.
```

Common failure:

```text
The subject describes preferred behavior but never states what is forbidden.
```

## Evolution

Purpose:

```text
Declare how state changes across time, steps, attempts, or updates.
```

Fill in:

```text
Evolution:
- <state change rule or sequence>
- <state change rule or sequence>
```

Minimum standard:

```text
The subject states what can change and what triggers or orders the change.
```

Common failure:

```text
The state changes are assumed but not declared.
```

## Readout

Purpose:

```text
Declare the answer extracted from the subject.
```

Fill in:

```text
Readout:
- <answer name>: <meaning>
- <answer name>: <meaning>
```

Minimum standard:

```text
The result is named in domain language and can be traced back to declared state.
```

Common failure:

```text
The result is a vague score, decision, or output with no declared meaning.
```

## Validation

Purpose:

```text
Declare how the result is checked before it is trusted.
```

Fill in:

```text
Validation:
- <check>
- <check>
```

Minimum standard:

```text
The subject states how success and failure are checked.
```

Common failure:

```text
The subject only describes successful output and never says how the result can
fail.
```

## Completeness Checklist

Before promoting this subject, confirm:

```text
1. Graph is explicit.
2. Typed field is explicit.
3. Placement is explicit.
4. State is explicit.
5. Action is explicit.
6. Constraint is explicit.
7. Evolution is explicit.
8. Readout is explicit.
9. Validation is explicit.
```

If any item is missing, keep the subject in draft form.
