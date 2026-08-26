# Execution Graph

## Definition

An execution graph is the Architecture surface that lets a CGF system operate
around a declared Substrate subject through views, paths, proposals, gates,
commits, outcomes, memory updates, and replay.

It is the graph that acts.

## What It Is For

Use an execution graph when a project needs to answer:

```text
What runtime view was used?
Which paths or actions were proposed?
Which gates or verifiers applied?
What became committed?
What outcome was observed?
What memory changed future behavior?
Can the decision be replayed?
```

The execution graph can operate around a physical system, service workflow,
agent graph, model pipeline, cache invalidation path, security finding flow, or
review process. The domain changes; the operating contract stays visible.

It also supports Granular Analysis, where one input fans out through many lenses
or encoders, many proposal nodes, and one traceable outcome.

## What It Is Not

The execution graph is not:

- the Substrate subject itself;
- a graph database;
- a required SDK;
- a service bus;
- a hidden controller;
- a place to hardcode every domain rule.

Substrate declares what is computed. The execution graph declares how operating
state moves through authority, trace, outcome, and memory.

## Core Operating Shape

```text
event
-> graph/path view
-> proposal set
-> path-conditioned or path-gated operators, when used
-> verification
-> commit
-> execution or accepted non-action
-> outcome
-> eligibility resolution
-> graph runtime memory update
-> replayable projection
```

Path-conditioned and path-gated operators are important execution-graph
patterns. They are not the whole execution graph. They sit inside the operating
path where path context may change computation or where a gate controls
influence or advancement.

## Granular Analysis Shape

```text
input
-> many lenses / encoders
-> many proposal nodes
-> verifier or gate
-> commit, review, defer, fallback, or abstain
-> traceable outcome
```

Granular Analysis makes the proposal set visible. A selected outcome can be
reviewed with the lens outputs that supported it and the rejected proposals that
competed with it.

## Required Separation

| Thing | Role | Must not do |
| --- | --- | --- |
| View | Freezes the operating graph or path state used for a decision. | Mutate hidden state after proposal. |
| Proposal | Carries candidate action, path, score, risk, uncertainty, and evidence. | Become authority by itself. |
| Verifier or gate | Checks evidence, policy, shape, and admissibility. | Hide blocked reasons. |
| Commit | Decides accepted action or accepted non-action. | Learn without outcome. |
| Trace | Reconstructs the operating path. | Become the source of value memory. |
| Outcome | Records observed result. | Rewrite proposal history. |
| Memory update | Changes future scoring, inhibition, uncertainty, or promotion. | Bypass verifier or commit. |
| Replay | Rebuilds projections from durable records. | Depend on hidden process state. |

## Validation Questions

```text
1. Does every proposal reference a declared view or path?
2. Are rejected proposals separated from committed decisions?
3. Can a hard gate block a high-scoring proposal?
4. Are path-conditioned effects visible when used?
5. Are path-gated decisions visible when used?
6. Does only commit create eligibility?
7. Does only outcome resolve eligibility into memory?
8. Can replay rebuild the trace and memory projection?
```

## Reading Path

Read this with:

- [runtime-spine.md](runtime-spine.md)
- [graph-brain-and-spine.md](graph-brain-and-spine.md)
- [subgraph-capsules.md](subgraph-capsules.md)
- [graph-runtime-memory.md](graph-runtime-memory.md)
- [proposal-verifier-commit.md](proposal-verifier-commit.md)
- [event-log-trace-replay.md](event-log-trace-replay.md)
