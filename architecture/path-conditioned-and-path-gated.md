# Path-Conditioned And Path-Gated

Path-conditioned and path-gated operation is a core CGF Architecture operator
concept inside the execution graph for systems where the path used to reach a
state, claim, proposal, or action matters.

## Definitions

| Concept | Plain meaning | What it controls |
| --- | --- | --- |
| Path-conditioned | Path context changes scoring, thresholds, routing, ranking, message passing, readout, or operator behavior. | Computation. It does not authorize action by itself. |
| Path-gated | An explicit gate controls how much path evidence can influence computation, or whether a proposal can advance. | Influence or advancement. Hard gates can allow, deny, defer, review, fallback, or abstain. |

## Why They Matter

A CGF system often operates over paths:

```text
local fact
relation
evidence chain
workflow route
candidate plan
tool call
memory recall
committed action
```

The same node or score can mean different things depending on the path that
produced it. Architecture makes that path visible so a system can use it
without turning path history into hidden state.

Path-conditioned and path-gated operation is first-class because it affects:

- what evidence is considered relevant;
- how an operator scores or routes a candidate;
- how a learned operator blends path context with graph context;
- whether a proposal is trusted enough to reach commit;
- whether an unknown or blocked path fails closed, defers, or falls back;
- what trace must preserve for audit and replay.

It is not the whole execution graph. The broader operating model is defined in
[execution-graph.md](execution-graph.md), [runtime-spine.md](runtime-spine.md),
and [graph-runtime-memory.md](graph-runtime-memory.md).

## Conditioning Versus Gating

Path-conditioned operation changes an operator's behavior.

```text
path context + input view -> adjusted score, threshold, route, rank, or message
```

Path-gated operation controls influence or advancement.

```text
path evidence + gate basis -> gate weight or gate outcome
```

They solve different problems.

| Need | Use |
| --- | --- |
| "This path should change the score or threshold." | Path-conditioned operator. |
| "This model should blend path context with graph context." | Soft path-gated operator. |
| "This path is not trusted enough to affect the decision." | Hard path-gated operator. |
| "This path is unknown, unsafe, contradictory, or unsupported." | Hard path gate with explicit unknown or blocked behavior. |
| "This path is useful but not authoritative." | Path-conditioned ranking behind normal verification and commit. |
| "This path improves decisions only after evaluation." | Path-conditioned operator with an evaluation check and claim boundary. |

## Three Recurring Forms

CGF treats these as one Architecture family with different control strength:

| Form | Meaning | Typical result |
| --- | --- | --- |
| Path-conditioned feature use | Path context is an input feature or context key. | Adjusted score, threshold, route, rank, message, or readout. |
| Soft path gate | A gate weight controls how strongly path context affects an operator. | Blended path context and graph context, weighted message passing, or adjusted confidence. |
| Hard path gate | A gate decision controls whether a proposal or path influence can advance. | Allow, deny, defer, review, fallback, or abstain. |

This distinction matters because "path-gated model" language can mean a learned
soft gate, while verifier and policy language often means a hard gate. CGF
names both forms and requires the document to say which one is being used.

## Path Evidence Versus Neighborhood Context

Do not treat every nearby graph fact as proof.

Architecture should distinguish:

| Surface | Purpose | Typical use |
| --- | --- | --- |
| Evidence path | Ordered, resolvable support chain. | Verification, explanation, gate basis, commit trace. |
| Graph neighborhood | Bounded surrounding context. | Exploration, retrieval, review support, next-question discovery. |
| Path context | The path-derived signal used by an operator. | Conditioning scores, thresholds, routes, messages, or readouts. |

An evidence path can support a gate or verifier because its steps are explicit
and resolvable. A neighborhood can provide context, but it should not be treated
as authority unless a bounded evidence path is declared from it.

## Combined Use

The common combined pattern is:

```text
event
-> graph/path view
-> path context
-> path-conditioned operator
-> path gate
-> verifier
-> commit / review / defer / fallback
-> trace
```

In this pattern, conditioning can improve a score, threshold, or route. A soft
gate can control how much path context affects an operator. A hard gate and
verifier can decide whether the result can advance. Commit remains the
authority boundary.

## What They Do Not Replace

Path-conditioned and path-gated operation do not replace:

- Substrate primitives;
- proposal, verifier, and commit separation;
- event log, trace, and replay;
- policy gates;
- outcome-coupled memory;
- evaluation discipline.

They are Architecture patterns for making path influence explicit, bounded,
traceable, and reviewable.

## Minimum Design Questions

Before using either concept, answer:

```text
1. What path context or path evidence is being used?
2. Which operator, score, threshold, route, or proposal is affected?
3. Is the path influence conditioning, gating, or both?
4. What happens when the path is unknown, weak, blocked, or contradictory?
5. What trace fields preserve the path context, gate basis, and decision?
6. What evaluation or ablation is needed before making an improvement claim?
```

Use [path-conditioned-operators.md](path-conditioned-operators.md) when path
context changes computation. Use [path-gated-operators.md](path-gated-operators.md)
when path evidence controls influence or advancement.

## Eval Support

[labs/evals/path-gated-operators](../labs/evals/path-gated-operators/README.md)
tests the hard gate and hop-discount conditioning, and compares both with a
baseline that commits the highest score. On seeded synthetic cases where a
recorded path is informative, the gate cuts wrong commits from 65% to 20% and
abstains on 9%; conditioning takes them to 16%. Where a recorded path says
nothing about correctness, the gate lowers precision. The
[result record](../labs/evals/path-gated-operators/results.md) has the
assumptions and the numbers.
