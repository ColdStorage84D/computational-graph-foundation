# Architecture Framework Registry

This registry lists reusable Architecture frameworks and the application shapes
they can support.

Use [selection-guide.md](selection-guide.md) first when starting from a project
shape and choosing a framework mix.

| Framework | Problem solved | Main CGF pieces | Example applications |
| --- | --- | --- | --- |
| [Bot graph](cards/bot-graph-framework.md) | A system needs sensing, proposing, gating, acting, observing, and learning as a traceable graph. | Execution graph, brain/spine, subgraph capsules, proposals, gates, graph runtime memory. | Robotics, tools, assistants, automation, games, process control. |
| [Evidence record](cards/evidence-record-framework.md) | Source evidence must stay external while decoded views, typed records, retrieval, and traces stay bounded. | Execution graph, evidence refs, record views, trace, replay, persistence contracts. | Health, security, incident evidence triage, legal review, audits, research curation, enterprise search. |
| [Typed multimodal graph](cards/typed-multimodal-graph-framework.md) | A case has heterogeneous parts, relations, labels, and leakage risks. | Substrate subject, typed graph views, feature nodes, training-only labels, deterministic export. | Health, documents, images, sensor fusion, product catalogs, education. |
| [Feature view](cards/feature-view-framework.md) | Different feature encodings should be named, filtered, routed, and evaluated rather than blindly stacked. | Lenses, operators, projectors, validation, evaluation discipline. | Multimodal inference, robotics, security scoring, scientific data. |
| [Granular Analysis](cards/granular-analysis-framework.md) | One input fans out through many lenses and proposal nodes before a traceable outcome. | Execution graph, lenses, proposals, verifier/commit, trace, evaluation discipline. | Histology-like analysis, medical image analysis, robotics, security, trading, predictive maintenance, documents. |
| [Local-Voting World Model](cards/local-voting-world-model-framework.md) | Local sensorimotor subgraphs predict outcomes, aggregate proposals, and update memory from prediction error. | Bot graph, sensor ingestion, Predictive Action Graph, subgraph capsules, graph runtime memory, safety gates. | Stochastic robot controllers, Webots agents, sensorimotor learning demos, tool or game controllers. |
| [Provisional Graph Growth](cards/provisional-graph-growth-framework.md) | Recurring evidence may justify candidate graph structure, but durable mutation must be bounded, reviewed, and reversible. | Provisional Graph Growth, subgraph capsules, graph runtime memory, replay, proposer-verifier, trace contract. | Bots, workflow routing, processor route discovery, signal triage, security triage, cache repair, robot fallback refinement. |
| [Proposer-verifier](cards/proposer-verifier-framework.md) | Candidate answers or actions need a validated connection before commit. | Proposal, verifier, commit, abstain/review, audit trace. | Classification, routing, findings, recommendations, actions. |
| [Processor routing](cards/processor-routing-framework.md) | Tasks should route to processors by declared fit and validation, not by one global encoder. | Route registry, path-conditioned routing, processor records, verifier gates. | Health processors, model selection, ETL, robotics, data products. |
| [Human review](cards/human-review-framework.md) | Model or processor output must remain proposal state until reviewed or explicitly accepted. | Proposal, verifier, review gate, commit, trace, outcome, later label derivation. | Health, security triage, compliance, editorial review, QA. |
| [Cache invalidation](cards/cache-invalidation-framework.md) | Derived views must update or invalidate from source dependency paths. | Execution graph, event log, dependency graph, commit, replay. | Caches, data products, feature stores, search indexes. |
| [Code security graph](cards/code-security-graph-framework.md) | Code needs graph evidence for findings, control/data flow, verification, and export. | Typed graph, evidence paths, verifier gates, finding records, trace exports. | Static analysis, supply chain review, secure coding assistants. |
| [Sensor ingestion](cards/sensor-ingestion-framework.md) | Raw observations must become bounded frames, views, and processor-ready records. | Adapters, lenses, typed views, trace, failure records. | Robots, IoT, health devices, industrial monitoring, simulation. |
| [Signal review](cards/signal-review-framework.md) | Noisy, partial, or regime-dependent signals need reviewable proposals instead of direct authority. | Feature views, Granular Analysis, processor routing, proposer/verifier, trace, optional human review. | Trading signals, predictive maintenance, risk alerts, anomaly review, operational monitoring. |
| [Evidence graph triage](cards/evidence-graph-triage-framework.md) | More findings compete for review than can be reviewed, and score must not be mistaken for corroboration. | Evidence records, typed graph, evidence paths, corroboration gates, eligibility, outcome, value memory, coverage and belief. | Incident evidence triage, alert and case triage, audit finding review, moderation queues, quality inspection. |

## Selection Rule

Select a framework only when it prevents a real failure mode:

```text
hidden authority
unbounded evidence
leakage
invalid processor fit
unsupported model output
missing review boundary
untraceable cache update
unverifiable finding
unbounded sensor state
unreviewed graph mutation
```

If a framework only adds vocabulary, skip it.
