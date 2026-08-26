# Predictive Action Graph

Predictive Action Graph is the CGF Architecture pattern for choosing an action
by comparing predicted futures instead of committing directly from a single
opaque model output.

It is useful when a system can observe a current state, propose candidate
actions, predict what each action is expected to change, and commit only the
first action from the best traceable candidate path.

## Operating Shape

```text
current evidence + goal evidence
-> lenses / encoders
-> generic hypergraph evidence encode, when structure matters
-> candidate action sequences
-> predicted futures
-> path-conditioned scoring
-> gate / verifier
-> selected first action
-> outcome observation
-> trace + graph runtime memory
```

The prediction step may be a deterministic proxy, a learned model, a simulator,
or another declared predictor. The Architecture requirement is not a specific
algorithm. The requirement is that the predictor input, candidate futures,
selected action, rejected alternatives, gate reason, outcome, and memory update
remain traceable.

## What It Solves

Predictive Action Graph prevents these failure modes:

- treating one direct model action as authority;
- hiding the alternatives that were considered;
- mixing live evidence with later outcome labels;
- using goal or simulator truth without saying which path observed it;
- committing an action without a gate, verifier, or abstain path;
- updating memory before the outcome is observed.

## Minimum Declaration

A Predictive Action Graph should declare:

```text
input evidence
goal or target evidence
lenses / encoders
generic hypergraph evidence encode, if used
proposal nodes
candidate action sequences
predictor
predicted future representation
path-conditioned score basis
gate / verifier
selected first action
rejected alternatives
outcome observation
memory update
claim boundary
```

## Relationship To Other Architecture Concepts

Predictive Action Graph builds on existing CGF Architecture concepts:

| Concept | Role |
| --- | --- |
| Granular Analysis | One input can fan out through many lenses and proposal nodes. |
| Path-conditioned operators | Path context changes scores, thresholds, ranking, or routing. |
| Path-gated operators | A gate controls whether a candidate action can advance. |
| Proposal / verifier / commit | Prediction remains a proposal until accepted. |
| Trace / replay | The selected action and rejected futures can be inspected. |
| Graph runtime memory | Outcome-coupled updates change future behavior only after observation. |

## Image-Only Action Rule

For visual control examples, image-only means the action graph receives RGB
frames or image-derived features. It must not use simulator-provided object
position, angle, contact count, distance, hidden success, or other privileged
state as action evidence.

Image-derived geometry can be used when it is computed from the pixels and
labeled as visual evidence. It is not simulator truth.

When spatial structure matters, prefer a generic hypergraph evidence encode
over a flat feature vector. The encoder should preserve typed evidence nodes,
n-ary relations, features, confidence, and source refs without owning
task-specific semantics. A robot app can bind generic image components to task
roles later; the encoder itself should stay reusable.

## When To Use

Use Predictive Action Graph when:

- actions should be selected by comparing possible futures;
- one input can produce several visual, sensor, or context lenses;
- multiple proposal nodes should compete;
- rejected action paths should remain visible;
- outcome memory should improve future selection;
- the system needs an abstain, review, or fallback path.

## When Not To Use

Do not use it when:

- there is only one deterministic action and no competing future;
- the predictor cannot expose its candidate futures;
- action selection does not need trace, gate, verifier, or memory;
- the project is only declaring a Substrate subject and not operating a system.

## Current CGF Example

[../applications/bots/README.md](../applications/bots/README.md) uses the same
shape in Graph Memory Bot, and
[../applications/maze-graph-memory-bot/README.md](../applications/maze-graph-memory-bot/README.md)
runs that action loop as a Webots maze fixture. The app compares candidate
actions through predicted outcomes, gates unsafe or weak choices, selects one
action, preserves rejected alternatives in the trace, and updates graph runtime
memory from observed prediction error.

[../applications/bots/README.md](../applications/bots/README.md) provides
smaller dependency-light examples for topology, trace, action gates, and graph
runtime memory.

Claim boundary: these examples demonstrate graph action and memory concepts.
They do not claim autonomous robot performance, benchmark success, guaranteed
maze solving, AGI, or biological cortex.
