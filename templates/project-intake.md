# CGF Project Intake

Use this template when applying Computational Graph Foundation to a real
project, prototype, application, or research direction.

The goal is to record the traversal decision: what CGF pieces apply, why they
apply, what support exists, and what remains unproven or unimplemented.

Primary references:

- [../FOUNDATION_TRAVERSAL.md](../FOUNDATION_TRAVERSAL.md)
- [../substrate/templates/subject-template.md](../substrate/templates/subject-template.md)
- [../substrate/extensions/decision-guide.md](../substrate/extensions/decision-guide.md)
- [../substrate/extensions/registry.md](../substrate/extensions/registry.md)
- [../research/connection-map.md](../research/connection-map.md)
- [../labs/evals/README.md](../labs/evals/README.md)
- [../architecture/README.md](../architecture/README.md)
- [../architecture/INDEX.md](../architecture/INDEX.md)
- [../architecture/frameworks/README.md](../architecture/frameworks/README.md)
- [../architecture/frameworks/selection-guide.md](../architecture/frameworks/selection-guide.md)
- [../architecture/frameworks/registry.md](../architecture/frameworks/registry.md)
- [../architecture/execution-graph.md](../architecture/execution-graph.md)
- [../architecture/granular-analysis.md](../architecture/granular-analysis.md)
- [../architecture/predictive-action-graph.md](../architecture/predictive-action-graph.md)
- [../architecture/multimodal-outcome-stack.md](../architecture/multimodal-outcome-stack.md)
- [../architecture/runtime-spine.md](../architecture/runtime-spine.md)
- [../architecture/graph-brain-and-spine.md](../architecture/graph-brain-and-spine.md)
- [../architecture/subgraph-capsules.md](../architecture/subgraph-capsules.md)
- [../architecture/graph-runtime-memory.md](../architecture/graph-runtime-memory.md)
- [../architecture/path-conditioned-and-path-gated.md](../architecture/path-conditioned-and-path-gated.md)

## 1. Project Snapshot

Project name:

Domain:

Problem statement:

Primary user or system:

Current implementation, if any:

What decision should this intake support?

## 2. Starting Point

Mark the entry point used:

```text
[ ] New project or domain problem
[ ] Existing graph model
[ ] Need computation, equations, or solver path
[ ] Failure mode or domain structure
[ ] Known extension name
[ ] Need extension combination
[ ] Need proof or validation status
[ ] Starting from eval code
[ ] Runtime, bot, workflow, or orchestration problem
[ ] One input, many lenses, many proposers
[ ] Action selection by predicted futures
[ ] Multimodal evidence-to-outcome case
[ ] Reusable framework concept
[ ] Brain/spine, subgraph, or graph memory problem
[ ] Application showcase
```

Why this starting point:

Docs checked:

## 3. Core Substrate Declaration Status

Use [../substrate/templates/subject-template.md](../substrate/templates/subject-template.md)
for the detailed declaration. Summarize it here.

| Core primitive | Declared? | Summary | Gap |
| --- | --- | --- | --- |
| Graph |  |  |  |
| Typed field |  |  |  |
| Placement |  |  |  |
| State |  |  |  |
| Action |  |  |  |
| Constraint |  |  |  |
| Evolution |  |  |  |
| Readout |  |  |  |
| Validation |  |  |  |

Core status:

```text
[ ] Complete enough to evaluate derivatives and extensions
[ ] Incomplete; stay in Substrate drafting
```

Core gaps to resolve:

## 4. Derivative Mechanics Decision

Derivative mechanics are conditional. Use them only when the subject needs more
formal computation, equations, trust checks, or method choice.

| Mechanic | Use / skip | Reason | Support docs | Gap |
| --- | --- | --- | --- | --- |
| Units / dimensions |  |  |  |  |
| Boundary |  |  |  |  |
| Source |  |  |  |  |
| Local action / Lagrangian |  |  |  |  |
| Variation |  |  |  |  |
| Operator assembly |  |  |  |  |
| Invariant |  |  |  |  |
| Residual / error estimator |  |  |  |  |
| Solver selection |  |  |  |  |

Derivative decision:

```text
[ ] No derivative mechanics needed now
[ ] Some derivative mechanics needed
[ ] Derivative mechanics are central to this project
```

Notes:

## 5. Extension Decision

Use [../substrate/extensions/decision-guide.md](../substrate/extensions/decision-guide.md)
and [../substrate/extensions/registry.md](../substrate/extensions/registry.md).

For each extension considered, mark it as required, optional, wrong, or deferred.

| Extension | Decision | Failure mode solved | Depends on | Research support | Labs result | Claim boundary |
| --- | --- | --- | --- | --- | --- | --- |
| Topological rigidity |  |  |  |  |  |  |
| Exterior placement |  |  |  |  |  |  |
| Weak form |  |  |  |  |  |  |
| Metric placement |  |  |  |  |  |  |
| Stochastic transition |  |  |  |  |  |  |
| Information geometry |  |  |  |  |  |  |
| Gauge transport |  |  |  |  |  |  |
| Sheaf consistency |  |  |  |  |  |  |
| Port-Hamiltonian flow |  |  |  |  |  |  |
| Causal intervention |  |  |  |  |  |  |
| Renormalization / coarse-graining |  |  |  |  |  |  |
| Differentiable backend |  |  |  |  |  |  |

Selected extension mix:

Extensions explicitly rejected:

Extension gaps:

## 6. Composition Pattern

Use [../substrate/extensions/composition-patterns.md](../substrate/extensions/composition-patterns.md).

Chosen pattern:

```text
[ ] No extension composition needed
[ ] Weak form + exterior placement
[ ] Metric placement + gauge transport
[ ] Sheaf consistency + gauge transport
[ ] Stochastic transition + information geometry
[ ] Causal intervention + stochastic transition
[ ] Renormalization / coarse-graining + differentiable backend
[ ] Topological rigidity + metric placement
[ ] Other:
```

Why this mix works:

What the mix makes easier to validate:

What the mix could hide or confuse:

## 7. Research Support

Use [../research/connection-map.md](../research/connection-map.md).

| Chosen CGF piece | Research page checked | Reference status | Open research risk |
| --- | --- | --- | --- |
|  |  |  |  |

Research summary:

Unresolved research questions:

## 8. Labs Eval Status

Use [../labs/evals/README.md](../labs/evals/README.md).

| Chosen CGF piece | Eval folder / result | Status label | Exact supported claim | Not supported |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

Eval status:

```text
[ ] No Labs eval applies
[ ] Labs eval exists but is only a tiny fixture
[ ] Labs eval should be created before making claims
[ ] Existing eval is enough for this intake's limited claim
```

Eval gaps:

## 9. Architecture Decision

Architecture is optional. Use it only when the project needs system operation
around a declared subject.

Architecture needed?

```text
[ ] No
[ ] Yes
[ ] Later
```

If yes or later, mark likely areas:

```text
[ ] Reusable Architecture framework cards
[ ] Granular Analysis
[ ] Predictive Action Graph
[ ] Multimodal Outcome Stack
[ ] Execution graph
[ ] Graph brain and spine
[ ] Subgraph capsules
[ ] Runtime graph views
[ ] Runtime node roles
[ ] Runtime spine
[ ] Path-state graphs
[ ] Operating cycle
[ ] Proposal / verifier / commit
[ ] Event log / trace / replay
[ ] Graph runtime memory / outcome feedback
[ ] Action accounting / policy gates
[ ] Evaluation discipline
[ ] Path-conditioned operators
[ ] Path-gated operators
[ ] Section-local Architecture reference code
```

Architecture reason:

Architecture gaps:

Reusable framework cards selected:

Framework selection record:

```text
project shape:
selected framework mix:
skipped framework cards:
eval / claim boundary:
reason this mix is enough:
```

```text
[ ] Bot graph
[ ] Evidence record
[ ] Typed multimodal graph
[ ] Feature view
[ ] Granular Analysis
[ ] Multimodal Outcome Stack
[ ] Proposer / verifier
[ ] Processor routing
[ ] Human review
[ ] Cache invalidation
[ ] Code security graph
[ ] Sensor ingestion
[ ] Signal Review
[ ] Other:
```

Framework cards explicitly skipped:

Framework mix risk:

Granular Analysis decision:

```text
[ ] Not needed
[ ] Needed: one input has many lenses / encoders
[ ] Needed: lens outputs feed multiple proposal nodes
[ ] Needed: one outcome should preserve competing proposals
[ ] Deferred
```

Granular Analysis trace requirements:

Predictive Action Graph decision:

```text
[ ] Not needed
[ ] Needed: current evidence and goal evidence produce candidate actions
[ ] Needed: action sequences are scored through predicted futures
[ ] Needed: one first action is committed from the selected future
[ ] Needed: rejected future paths remain in trace
[ ] Deferred
```

Predictive Action Graph trace requirements:

```text
current evidence:
goal evidence:
lenses / encoders:
proposal nodes:
candidate action sequences:
predictor:
predicted future representation:
gate / verifier:
selected first action:
rejected alternatives:
outcome observation:
memory update:
claim boundary:
```

Multimodal Outcome Stack decision:

```text
[ ] Not needed
[ ] Needed: source evidence must stay external
[ ] Needed: decoded records must stay bounded
[ ] Needed: typed graph nodes / edges / labels must be separated
[ ] Needed: labels, later outcomes, or review records must stay out of live features
[ ] Needed: feature views and processor routes must be explicit
[ ] Needed: proposals and review state must be traceable
[ ] Deferred
```

Multimodal Outcome Stack trace requirements:

```text
source evidence refs:
decoded record types:
typed graph node / edge types:
training-only or later-derived labels:
feature views:
processor routes:
proposal nodes:
review / verifier gate:
trace fields:
claim boundary:
```

Execution graph decision:

```text
[ ] Not needed
[ ] Needed for operating path
[ ] Needed for bot/agent/process graph
[ ] Deferred
```

Brain/spine decision:

```text
[ ] Not needed
[ ] Brain coordinates phases
[ ] Spine routes between surface nodes
[ ] Child graphs are subgraph capsules
[ ] Deferred
```

Graph runtime memory decision:

```text
[ ] No graph runtime memory
[ ] Eligibility/value memory
[ ] Residual/action-functional memory
[ ] Place/manifold memory
[ ] Semantic/procedural projection
[ ] Quarantine or counterfactual memory
[ ] Deferred
```

Agent/project memory distinction:

Path-conditioned decision:

```text
[ ] Not used
[ ] Used for score, threshold, route, message, ranking, or readout
[ ] Deferred
```

Path-gated decision:

```text
[ ] Not used
[ ] Used as soft influence control
[ ] Used as hard advancement control
[ ] Used as both soft influence and hard advancement control
[ ] Deferred
```

Path-aware trace requirements:

## 10. Application Or Implementation Direction

Target destination:

```text
[ ] Substrate example
[ ] Research study
[ ] Labs eval
[ ] Architecture note
[ ] Application page
[ ] Section-local code example
[ ] External implementation
```

Implementation posture:

```text
[ ] Docs only for now
[ ] Inline pseudocode only
[ ] Section-local implementation later
[ ] Runnable eval needed first
[ ] Application implementation can start
```

No-lock-in note:

## 11. Final Traversal Record

Summarize the chosen path:

```text
Starting point:
Core Substrate status:
Derivative mechanics:
Extensions:
Composition:
Research support:
Labs eval status:
Architecture:
Destination:
```

## 12. Remaining Gaps Before Use

-

## 13. Reviewer Checklist

```text
[ ] The 9-core Substrate declaration is explicit or gaps are named.
[ ] Derivative mechanics are selected only when needed.
[ ] Extensions are required, optional, wrong, or deferred with reasons.
[ ] Research support is linked.
[ ] Labs eval status is linked or the absence of evals is explicit.
[ ] Claim boundaries are stated.
[ ] Architecture is included only if system operation is needed.
[ ] The destination is clear.
[ ] No mandatory SDK or package lock-in is implied.
```
