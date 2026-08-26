# Provisional Graph Growth Framework

## Purpose

Use this framework when a runtime graph sees recurring evidence that may justify
a new route, rule, edge, specialist, or local graph structure, but durable graph
mutation must stay bounded, reviewable, and reversible.

## Reusable Concept

```text
recurring evidence
-> provisional graph capsule
-> bounded candidate variants
-> shadow scoring
-> stability guard
-> growth patch
-> promotion gate
-> probation / promote / quarantine / retire / reject
-> rollback on regression
```

The reusable idea is not that the graph changes itself freely. The reusable
idea is that candidate structure can exist provisionally while durable graph
state remains protected by explicit promotion and rollback rules.

## Uses CGF Pieces

- [Provisional Graph Growth](../../provisional-graph-growth.md)
- [Execution graph](../../execution-graph.md)
- [Subgraph capsules](../../subgraph-capsules.md)
- [Graph runtime memory](../../graph-runtime-memory.md)
- [Offline replay / dream cycles](../../offline-replay-dream-cycles.md)
- [Proposer-verifier](proposer-verifier-framework.md)
- [Trace contract](../../contracts/trace-contract.md)

## Example Applications

- bot route growth;
- recurring workflow exception handling;
- processor route discovery;
- signal or alert triage route refinement;
- security finding triage rules;
- cache or derived-view dependency repair;
- robot or tool-controller fallback refinement.

## When To Use

Use this framework when:

- the same unknown pattern appears repeatedly;
- the current graph keeps falling back to review or a generic route;
- candidate graph structure should be tested before it becomes durable;
- shadow scoring and rejected variants should remain visible;
- burst, one-off, or low-quality evidence must not create durable graph state;
- promotion requires baseline comparison, held-out review, safety or policy
  review, risk limits, and rollback.

## When Not To Use

Do not use this framework when:

- a developer is making a normal authored release change;
- the evidence is one event or a short spike;
- the graph has no trace or outcome evidence;
- there is no review, promotion, or rollback path;
- the project only needs a static Substrate declaration;
- the intended claim is autonomous self-improvement or production safety.

## Boundary

Provisional Graph Growth is an Architecture framework. It is not a Substrate
primitive, not a mandatory runtime, not a package surface, not a solver, and
not a broad learning method.

Candidate variants cannot commit themselves. A provisional capsule can explain,
shadow-score, route to review, or propose a growth patch. Durable graph changes
require an explicit promotion gate.

## Implementation Posture

Keep implementations section-local and inspectable. The minimum useful runtime
records are:

```text
observation
provisional graph capsule
candidate variant
shadow score
stability guard
growth patch
promotion decision
rollback record
```

Do not hide promotion inside a model score, cache write, or background job.

## Eval Support

Current support:

- [provisional-graph-growth/results.md](../../../labs/evals/provisional-graph-growth/results.md)

Supported claim: tiny-fixture `contract-pass` for provisional capsules,
bounded candidate variants, stability guards, promotion gates, and rollback.

Unsupported claims: autonomous self-improvement, production safety, broad
learning performance, domain adaptation, or better performance than a
hand-authored graph.
