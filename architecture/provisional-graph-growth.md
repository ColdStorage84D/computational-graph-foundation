# Provisional Graph Growth

Provisional Graph Growth is a CGF Architecture pattern for bounded graph
adaptation: runtime evidence may create provisional graph capsules and bounded
candidate variants, but durable graph state changes only after stability
checks, validation, risk review, promotion, and rollback policy.

It is the Architecture answer to this question:

```text
When repeated evidence suggests the graph needs a new route, rule, specialist,
or local structure, how can the system test that possibility without silently
mutating the durable graph?
```

## What It Solves

Execution graphs need room to adapt. A bot, review system, signal pipeline, or
controller may see a recurring pattern that existing routes handle poorly.
Without a bounded growth pattern, the system tends to choose one of two bad
options:

- ignore the recurring pattern and keep falling back to review;
- add new structure too quickly and let one spike or noisy cluster reshape the
  graph.

Provisional Graph Growth creates a middle path. The graph can represent a
possible new structure, score it in shadow mode, collect outcome evidence, and
then either promote, quarantine, retire, reject, or roll it back.

## Operating Shape

```text
trace
-> observation
-> novelty / surprise signal
-> provisional graph capsule
-> bounded candidate variants
-> shadow scoring
-> stability guard
-> growth patch
-> probation
-> promote / quarantine / retire / reject
-> rollback when promoted behavior regresses
```

The key rule is that provisional structure has no durable authority. It can
explain, score, route to review, or produce a candidate growth patch. It cannot
commit itself into the durable graph.

## Core Records

| Record | Meaning | Minimum fields |
| --- | --- | --- |
| Observation | Evidence that a pattern appeared. | Pattern key, evidence ref, surprise, quality, risk, tick. |
| Provisional graph capsule | Temporary local graph around the recurring pattern. | Capsule id, pattern key, evidence refs, activation, allowed use. |
| Candidate variant | Bounded possible route, rule, edge, or specialist. | Variant id, strategy, affinity, risk, traffic weight, status. |
| Shadow score | Non-authoritative score for a candidate. | Variant ref, score, evidence ref, `shadow_only` authority. |
| Stability guard | Temporal and quality check before promotion. | Temporal shape, accepted flag, reason. |
| Growth patch | Proposed durable graph change. | Nodes, edges, evidence refs, benefit, cost, risk, rollback policy. |
| Promotion decision | Explicit review of whether the patch may become durable. | Baseline comparison, held-out check, safety check, risk limit. |
| Rollback record | Removal or deactivation after regression. | Patch ref, trigger, restored route, trace refs. |

## Stability Guard

The stability guard keeps the graph from growing on spikes.

| Temporal shape | Meaning | Durable growth allowed? |
| --- | --- | --- |
| One-off | A single unsupported observation. | No. |
| Burst | Multiple observations in a tight spike. | No. |
| Unstable trend | Repeated evidence with weak or inconsistent quality. | No. |
| Stable recurring support | Repeated evidence over enough time with acceptable quality and risk. | Only after the rest of the promotion gate passes. |

This matters because bursts can look important without being durable. CGF
should keep burst evidence visible, but it should not let the burst create a
permanent route by itself.

## Promotion Gate

A growth patch may be promoted only when all of these are true:

```text
evidence refs exist
temporal support is stable
candidate beats baseline after cost and risk
held-out or delayed check passes
safety / policy review passes
rollback policy exists
trace can explain the decision
```

If any item fails, the candidate remains provisional, moves to review, enters
quarantine, or is retired.

## Relationship To Nearby Architecture

| Concept | Relationship |
| --- | --- |
| Execution graph | Provides the operating surface where observations, proposals, gates, and commits occur. |
| Subgraph capsules | Provisional structures are a special kind of capsule with stricter authority limits. |
| Graph runtime memory | Stores activation, support, risk, outcomes, quarantine, and rollback evidence. |
| Offline replay / dream cycles | Can replay real traces or generate hypotheses, but promotion still requires resolved evidence. |
| Path-conditioned / path-gated operators | May influence candidate scoring or advancement, but cannot replace the promotion gate. |

## When To Use

Use Provisional Graph Growth when:

- repeated evidence suggests a new graph route, rule, edge, or specialist;
- an existing fallback path is handling the same unknown pattern repeatedly;
- a candidate should be tested without becoming durable;
- shadow scoring, probation, quarantine, retirement, and rollback need to be
  visible;
- graph adaptation must be traceable.

## When Not To Use

Do not use it when:

- a developer can make a normal authored graph change;
- the evidence is a one-off spike or burst;
- there is no trace or outcome evidence;
- the system has no promotion, review, or rollback path;
- the document is only declaring a Substrate subject;
- the project wants to claim autonomous self-improvement without eval support.

## Claim Boundary

This is an Architecture pattern, not a Substrate primitive, not a solver, not a
production safety system, and not a broad learning-performance claim.

The current CGF-local eval supports only a tiny fixture contract: recurring
stable evidence can create provisional structure, bounded candidate variants
can be shadow-scored, burst evidence is held, durable mutation requires an
explicit promotion gate, and regression can roll back promoted structure.

See [../labs/evals/provisional-graph-growth/results.md](../labs/evals/provisional-graph-growth/results.md).
