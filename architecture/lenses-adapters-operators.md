# Lenses, Adapters, Operators, Scorers, And Projectors

## Purpose

This pattern defines how execution graphs produce typed views, translate
between specialized components, run operations, score candidates, and project
results without bypassing Architecture authority.

## Responsibilities

| Role | Responsibility | Must not do |
| --- | --- | --- |
| Lens | Creates a typed view from declared state or evidence. | Mutate source state or commit action. |
| Adapter | Translates between a specialist component and shared runtime records. | Hide unsupported fields or bypass policy. |
| Operator | Transforms a view into a candidate, score, readout, or projection. | Treat output as committed truth. |
| Scorer | Ranks, weighs, or compares proposals. | Override hard policy gates. |
| Projector | Builds a derived view from event, trace, or memory records. | Become the source of truth. |

## Path-Aware Operators

Some operators are path-conditioned, path-gated, or both.

| Form | Responsibility | Must preserve |
| --- | --- | --- |
| Path-conditioned operator | Uses path context to change score, threshold, route, message, ranking, or readout. | Path context, effect surface, evidence refs, and evaluation boundary. |
| Path-gated operator | Uses a gate to control path influence or proposal advancement. | Gate basis, gate weight or outcome, blocked reasons, unknown-path behavior, and trace refs. |

Path-conditioned output is still an operator result. Path-gated output is still
subject to verifier, commit, trace, and replay inside the execution graph.

## Minimal Declaration

Each role should declare:

```text
input view
output record
evidence refs
path context refs, when used
uncertainty or confidence
failure mode
policy relevance
replay behavior
```

## Rule

Specialists propose or transform. The execution graph routes them through the
runtime spine, and accepted state changes still require verification and
commit.

## Validation Questions

```text
1. Is every output tied to an input view?
2. Are evidence refs preserved?
3. Is path context or gate basis preserved when used?
4. Can failures be represented as records?
5. Can the role be replayed or frozen when needed?
6. Can policy still block the result?
```
