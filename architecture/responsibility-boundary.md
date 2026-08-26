# Architecture Responsibility Boundary

Architecture starts after a Substrate subject exists.

## Architecture Question

```text
How do CGF systems operate around this subject?
```

## Owns

- Execution graph.
- Graph brain and spine.
- Runtime spine.
- Runtime graph views.
- Runtime node roles: task, choice, proposal, commit, operator, policy,
  artifact, memory anchor, outcome, tool, and subgraph capsule.
- Subgraph capsules.
- Path-state graphs.
- Operating cycle.
- Path-conditioned operators: path context changes scoring, thresholds,
  routing, ranking, message passing, readout, or operator behavior.
- Path-gated operators: explicit gates decide whether path evidence can
  influence computation or whether a proposal can advance.
- Evidence paths.
- Predictive Action Graph: current evidence, goal evidence, candidate action
  sequences, predicted futures, gate / verifier, selected first action, trace,
  and outcome memory.
- Proposal, verifier, and commit.
- Event log, trace, replay, and persistence.
- Eligibility, graph runtime memory, outcome feedback, and value feedback.
- Action accounting and policy gates.
- Evaluation discipline.

## Does Not Own

- Base Substrate primitive definitions.
- Domain product behavior.
- Mandatory implementation style.
- Large datasets or private application material.
- Database, service bus, or SDK requirements.

## Rule

```text
Substrate defines what is computed.
Architecture defines how a CGF system operates around it.
```

The execution graph is the broad operating surface. The runtime spine is the
authority and routing path inside that surface.
