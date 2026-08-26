# Runtime Spine

## Definition

The runtime spine is the minimal Architecture path inside an execution graph
that makes a CGF system replayable, auditable, and outcome-coupled.

It is the operating contract for routing, authority, replay, and audit:

```text
event log -> graph/path view -> proposal -> verification -> commit
  -> trace -> eligibility -> outcome -> value/memory update -> replay
```

## What It Is

The runtime spine defines what must be visible when a system acts around a
declared Substrate subject.

It answers:

```text
What happened?
What view was used?
What was proposed?
What checked the proposal?
What was committed?
What trace explains it?
What outcome resolved it?
What memory or value changed?
Can the path be replayed?
```

## What It Is Not

The spine is not:

- a global object;
- a database;
- a service bus;
- an SDK;
- a package layout;
- a graph database;
- a product workflow.

It is an Architecture contract. Implementations can realize it with files,
databases, queues, services, in-memory objects, or external systems.

## Spine Stages

| Stage | Responsibility | Failure if missing |
| --- | --- | --- |
| Event log | Records ordered things that happened. | State cannot be replayed or audited. |
| Graph/path view | Builds the operational view used for a decision. | Proposals act on hidden or ambiguous state. |
| Proposal | Carries a candidate path, action, score, risk, uncertainty, and evidence refs. | Candidate generation is confused with authority. |
| Verification | Checks shape, policy, constraints, evidence, and admissibility. | Invalid proposals can reach commit. |
| Commit | Decides accepted action, non-action, review, defer, fallback, or abort. | Side effects happen without a decision boundary. |
| Trace | Links event, view, proposal, verification, commit, and later outcome. | Attribution is lost. |
| Eligibility | Opens delayed credit or blame only for committed paths. | Rejected or uncommitted candidates can update memory. |
| Outcome | Records observed result. | Learning becomes speculation. |
| Value / memory update | Updates future ranking, inhibition, uncertainty, or promotion. | The system cannot learn from outcomes. |
| Replay | Rebuilds projections and traces from durable records. | Audit and recovery depend on hidden state. |

## Place In The Execution Graph

The execution graph is the larger operating surface. The spine is the authority
and routing path through that surface. Brain, surface nodes, subgraph capsules,
operators, and memory projections can be arranged around it, but committed
state still flows through the spine.

## Path-Aware Operation

Path-conditioned and path-gated operation can appear between the graph/path
view, proposal, verification, and commit stages.

```text
graph/path view -> path context -> path-conditioned operator
  -> path gate -> verification -> commit
```

Path-conditioned operation may change a score, threshold, route, message, or
readout. Soft path-gated operation may change a weight, confidence, or blend.
Hard path-gated operation may allow, deny, defer, review, fallback, or abstain.
Neither replaces verification, commit, trace, replay, or outcome resolution.

## Minimal Spine Record

A minimal Architecture design should name:

```text
event type
view id
path context refs, when used
proposal id
verification result
path gate weight or result, when used
commit id
trace id
eligibility status
outcome id
memory update id
replay projection
```

These names do not require a schema yet. They are the minimum identifiers a
future implementation must preserve.

## Boundary With Substrate

Substrate defines what is computed. The runtime spine defines how operation
around that subject becomes ordered, reviewable, and outcome-coupled.

The spine may use Substrate graph, typed fields, placement, state, action,
constraint, evolution, readout, and validation, but it must not redefine those
primitives.

## Validation Questions

Before using the runtime spine in an example or implementation plan, check:

```text
1. Can every committed decision be traced to an event and view?
2. Are proposals visible even when rejected?
3. Can hard policy block high-scoring proposals?
4. Is path-conditioned influence visible when path context changes computation?
5. Is path-gated control visible when a path influences computation or blocks advancement?
6. Does only commit create eligibility?
7. Does memory update only after outcome?
8. Can replay rebuild the trace without hidden state?
```
