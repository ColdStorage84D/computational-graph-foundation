# Architecture Index

This index maps the Architecture section. Use it when a project already has a
Substrate subject and needs operating structure around it.

Architecture has one active responsibility:

```text
Define how CGF systems operate around declared Substrate subjects.
```

## What To Look For

When reading or writing Architecture material, look for these signals:

- The Substrate subject already exists.
- The system needs an execution graph rather than a static subject declaration.
- Runtime views do not redefine Substrate primitives.
- Brain, spine, surface nodes, and subgraph capsules stay separate.
- Subgraph roles are routeable capsules, not separate foundations.
- Anchor / Lens / Promise records preserve source identity and replayable view
  identity.
- Visual media encoding preserves source frames, regions, tracks, and evidence
  refs.
- Proposals are separated from commits.
- Trace and replay can reconstruct why a decision happened.
- Graph runtime memory updates are coupled to observed outcomes.
- Hierarchical cycles keep child responses bounded by budget and authority.
- Offline replay cycles separate real outcome-backed replay from
  counterfactual hypotheses.
- Provisional Graph Growth separates candidate graph adaptation from durable
  graph mutation.
- Belief state and Bayesian filtering preserve uncertainty and innovation as
  evidence, not durable truth.
- Cognitive map and cued recall memory organize recall without bypassing outcomes.
- Granular Analysis is visible when one input fans out through multiple lenses,
  encoders, proposal nodes, and outcome candidates.
- Predictive Action Graph is visible when action selection compares candidate
  action sequences through predicted futures before committing one first action.
- The Local-Voting World Model is visible when local sensorimotor subgraphs
  predict outcomes, report prediction error, and aggregate proposals before a
  gated commit.
- The Multimodal Outcome Stack is visible when source evidence, typed records,
  feature views, processor routes, proposals, review, and trace all need to stay
  separated.
- Path-conditioned and path-gated behavior is explicit when paths affect
  computation, influence, or advancement.
- Policy gates can block action even when a score is high.
- Operators and adapters cannot bypass the commit boundary.

## Reading Paths

Use this order if you are new to Architecture:

```text
README.md -> responsibility-boundary.md -> execution-graph.md
-> runtime-spine.md -> graph-brain-and-spine.md
-> subgraph-capsules.md -> subgraph-role-registry.md
-> anchor-lens-promise.md -> visual-media-encoding.md
-> graph-runtime-memory.md -> belief-state.md
-> path-state-graph.md -> hierarchical-execution-cycles.md
-> offline-replay-cycles.md -> provisional-graph-growth.md
-> granular-analysis.md
-> predictive-action-graph.md
-> local-voting-world-model.md
-> multimodal-outcome-stack.md
-> path-conditioned-and-path-gated.md
-> operating-cycle.md
```

Use this order if you are designing an operating system around a subject:

```text
execution-graph.md -> runtime-spine.md -> contracts/README.md
-> path-conditioned-and-path-gated.md -> proposal-verifier-commit.md
-> event-log-trace-replay.md
-> memory-outcome-feedback.md -> action-accounting-policy.md
-> examples/README.md
```

Use this order if you are choosing reusable framework concepts:

```text
frameworks/README.md -> frameworks/registry.md -> frameworks/cards/README.md
-> execution-graph.md -> contracts/README.md
```

Use this order if you are reviewing a contribution:

```text
status.md -> responsibility-boundary.md -> execution-graph.md -> runtime-spine.md
-> path-conditioned-and-path-gated.md -> contracts/README.md
-> examples/README.md
```

## Core Documents

| Document | Purpose | What to look for |
| --- | --- | --- |
| [README.md](README.md) | Short Architecture landing page. | Layer ownership and reading order. |
| [status.md](status.md) | Current Architecture readiness and gaps. | What is stable, draft, and deferred. |
| [responsibility-boundary.md](responsibility-boundary.md) | Boundary with Substrate and Applications. | What Architecture owns and does not own. |
| [execution-graph.md](execution-graph.md) | Operating graph that acts around a declared subject. | View, proposal, gate, commit, outcome, memory, and replay separation. |
| [runtime-spine.md](runtime-spine.md) | Central operating path. | Event log, graph/path view, proposal, verification, commit, trace, eligibility, outcome, value/memory update, replay. |
| [graph-brain-and-spine.md](graph-brain-and-spine.md) | Brain, spine, surface-node, and route boundary pattern. | Brain coordinates phases, spine routes messages, surface nodes own local transforms. |
| [subgraph-capsules.md](subgraph-capsules.md) | Local graph detail as traceable routeable capsules. | Capsule inputs, outputs, evidence, memory boundary, and failure modes. |
| [subgraph-role-registry.md](subgraph-role-registry.md) | Current subgraph role catalog. | Role ownership, inputs, outputs, authority boundary, and trace obligations. |
| [anchor-lens-promise.md](anchor-lens-promise.md) | Replayable source-to-view identity pattern. | Anchor identity, lens application identity, promise status, output refs, and evidence refs. |
| [visual-media-encoding.md](visual-media-encoding.md) | Image/video evidence to traceable graph views. | Source frames, regions, tracks, events, lens refs, and claim boundary. |
| [graph-runtime-memory.md](graph-runtime-memory.md) | Memory that changes future execution-graph behavior. | Eligibility, value, residual, action-functional, place/manifold, promotion, quarantine, and counterfactual rules. |
| [belief-state.md](belief-state.md) | Operating belief and uncertainty records. | Confidence, uncertainty, evidence weight, distribution refs, and calibration. |
| [bayesian-filtering-state-estimation.md](bayesian-filtering-state-estimation.md) | Belief prediction and measurement correction. | Prior, process model, measurement, posterior, innovation, and uncertainty. |
| [path-state-graph.md](path-state-graph.md) | Runtime representation of active, candidate, committed, and historical paths. | How facts, relations, workflows, decisions, and subgraph routes can be represented as paths. |
| [hierarchical-execution-cycles.md](hierarchical-execution-cycles.md) | Parent and child operating cycles. | Child budgets, response statuses, deferrals, and parent authority. |
| [offline-replay-cycles.md](offline-replay-cycles.md) | Offline resolve, replay, simulation, and promotion review cycles. | Real outcome-backed replay versus counterfactual hypotheses. |
| [provisional-graph-growth.md](provisional-graph-growth.md) | Bounded graph adaptation. | Provisional capsules, candidate variants, shadow scoring, stability guards, promotion gates, and rollback. |
| [cognitive-map-memory.md](cognitive-map-memory.md) | Relational recall structure. | Physical, conceptual, or latent task maps used as proposal evidence. |
| [cued-recall-memory.md](cued-recall-memory.md) | Sparse episode recall traces. | Where, what, action, outcome bindings and partial cue reactivation. |
| [granular-analysis.md](granular-analysis.md) | Multi-lens, multi-proposer, outcome-oriented graph analysis. | Many lenses, many proposers, one traceable outcome. |
| [predictive-action-graph.md](predictive-action-graph.md) | Action selection through traceable predicted futures. | Current evidence, goal evidence, candidate sequences, prediction, gate, selected first action, trace, and memory. |
| [local-voting-world-model.md](local-voting-world-model.md) | Local sensorimotor predictive subgraphs composed as an Architecture foundation. | Columns as evidence/prediction/memory surfaces, lateral proposal aggregation, prediction error, outcome-coupled memory, and safety gates. |
| [multimodal-outcome-stack.md](multimodal-outcome-stack.md) | Reusable evidence-to-outcome stack for multimodal and multi-view cases. | Evidence refs, typed graph records, feature views, processor routes, proposals, review, and trace. |
| [path-conditioned-and-path-gated.md](path-conditioned-and-path-gated.md) | Central path-aware Architecture primer. | Difference between conditioning, gating, and combined use. |
| [operating-cycle.md](operating-cycle.md) | Repeatable decision cycle. | Encode, propose, verify, commit, execute, observe, resolve, consolidate. |

## Frameworks

Framework cards are reusable Architecture patterns. Applications such as bots
and medical image analysis compose them; they do not own them.

| Document | Purpose | What to look for |
| --- | --- | --- |
| [frameworks/README.md](frameworks/README.md) | Framework catalog entry. | The rule that framework means reusable pattern, not mandatory SDK. |
| [frameworks/registry.md](frameworks/registry.md) | Current framework registry. | Which pattern solves which failure mode and which applications can use it. |
| [frameworks/cards/README.md](frameworks/cards/README.md) | Framework card index. | Compact cards for bot graph, evidence record, multimodal graph, feature view, Granular Analysis, Local-Voting World Model, proposer/verifier, routing, review, cache, security, and sensor ingestion. |

## Operating Patterns

| Document | Purpose | What to look for |
| --- | --- | --- |
| [lenses-adapters-operators.md](lenses-adapters-operators.md) | Typed views and specialist operation boundaries. | Lenses create views, adapters translate, operators produce results, scorers rank, projectors summarize. |
| [proposal-verifier-commit.md](proposal-verifier-commit.md) | Decision authority pattern. | Candidate generation stays separate from accepted state change. |
| [event-log-trace-replay.md](event-log-trace-replay.md) | Audit and reconstruction pattern. | Append-only event record, trace projection, replay equality. |
| [memory-outcome-feedback.md](memory-outcome-feedback.md) | Outcome-coupled memory pattern. | Eligibility before outcome, value after outcome, promotion after evidence. |
| [provisional-graph-growth.md](provisional-graph-growth.md) | Candidate graph growth pattern. | Recurring evidence can create provisional structure, but durable graph mutation requires promotion and rollback rules. |
| [action-accounting-policy.md](action-accounting-policy.md) | Auditable selection and blocking. | Soft action terms, hard policy gates, explicit tradeoffs. |
| [path-conditioned-operators.md](path-conditioned-operators.md) | Path context as an operator input. | Ranking, thresholds, routing, scoring, message passing, or readout changes caused by declared path context. |
| [path-gated-operators.md](path-gated-operators.md) | Explicit path-evidence gate pattern. | Learned or deterministic gates that control influence or advancement. |

## Contracts

Contract cards define the minimum record shape for Architecture operation.

| Contract | Purpose |
| --- | --- |
| [contracts/README.md](contracts/README.md) | Contract card index and rules. |
| [contracts/event-contract.md](contracts/event-contract.md) | Records that something happened. |
| [contracts/proposal-contract.md](contracts/proposal-contract.md) | Records a candidate path or action. |
| [contracts/commit-contract.md](contracts/commit-contract.md) | Records the decision boundary where a candidate becomes accepted. |
| [contracts/outcome-contract.md](contracts/outcome-contract.md) | Records observed result after committed action or non-action. |
| [contracts/trace-contract.md](contracts/trace-contract.md) | Reconstructs the path from event to decision to outcome. |
| [contracts/persistence-contract.md](contracts/persistence-contract.md) | Defines replayable storage expectations without choosing a database. |

## Examples

Examples are prose operating patterns. They are not SDKs or required
implementations.

| Example | Purpose |
| --- | --- |
| [examples/README.md](examples/README.md) | Example index and rules. |
| [examples/ecommerce-runtime-path.md](examples/ecommerce-runtime-path.md) | Checkout-like service workflow through proposal, commit, trace, and outcome. |
| [examples/agent-graph-harness.md](examples/agent-graph-harness.md) | Agent, model, tool, and memory nodes operating under commit authority. |
| [examples/evidence-record-flow.md](examples/evidence-record-flow.md) | Source handles, decoded views, records, bounded retrieval, and trace exports. |
| [examples/agent-memory-flow.md](examples/agent-memory-flow.md) | Notes, claims, audit questions, eligibility, and value memory. |
| [examples/path-aware-verifier-flow.md](examples/path-aware-verifier-flow.md) | Evidence path, path-conditioned effect, path gate, verifier, commit, and trace. |
| [examples/bot-execution-graph.md](examples/bot-execution-graph.md) | Bot-shaped execution graph with brain/spine routing, path-aware scoring, gates, and graph runtime memory. |
| [examples/multimodal-review-flow.md](examples/multimodal-review-flow.md) | Reusable source evidence, typed graph, lenses, routes, proposals, review, and trace flow. |

## Reference Code

Reference code is optional and section-local. It exists to make the contracts
inspectable and testable without becoming a required SDK.

| Reference | Purpose |
| --- | --- |
| [reference/python/README.md](reference/python/README.md) | Stdlib-only execution graph, graph memory, and bot graph reference tests. |
