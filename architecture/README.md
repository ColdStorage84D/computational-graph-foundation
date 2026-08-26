# Architecture

Architecture defines how CGF systems operate around Substrate subjects.

It owns runtime organization:

- execution graphs;
- runtime spine;
- graph brain and spine coordination;
- runtime graph views;
- runtime node roles;
- subgraph capsules;
- subgraph role registry;
- path-state graphs;
- anchor / lens / promise records;
- visual media encoding;
- operating cycle;
- hierarchical execution cycles;
- offline replay / dream cycles;
- provisional graph growth;
- operators, lenses, adapters, scorers, and projectors;
- belief state and Bayesian filtering / state estimation;
- granular analysis: many lenses, many proposers, one traceable outcome;
- predictive action graph: candidate action sequences, predicted futures,
  gate / verifier, trace, and outcome-coupled memory;
- cortical-column world model: local sensorimotor predictive subgraphs,
  lateral proposal aggregation, prediction error, and safety gate separation;
- multimodal outcome stack: evidence records, typed multimodal graph, feature
  views, processor routes, proposals, review, and traceable outcome;
- signal review: signals, feature views, route-specific processors, proposals,
  verifier / review / abstain, and traceable signal decision;
- reusable Architecture framework cards;
- path-conditioned and path-gated operators;
- proposal, verifier, and commit patterns;
- event log, trace, replay, and persistence;
- eligibility, graph runtime memory, outcome feedback, and value feedback;
- cognitive map memory and engram / spatial memory;
- action accounting and policy gates;
- evaluation discipline.

Architecture may use Substrate primitives. It must not redefine them.

Start with [../FOUNDATION_TRAVERSAL.md](../FOUNDATION_TRAVERSAL.md) when you
need to decide whether Architecture is required. Start with
[INDEX.md](INDEX.md) when you already know the problem is operational.

Core Architecture docs:

- [execution-graph.md](execution-graph.md): the operating graph that acts
  around a declared subject.
- [runtime-spine.md](runtime-spine.md): the minimal operating path that makes a
  CGF system replayable, auditable, and outcome-coupled.
- [graph-brain-and-spine.md](graph-brain-and-spine.md): brain, spine,
  surface-node, and route boundary pattern.
- [responsibility-boundary.md](responsibility-boundary.md): what Architecture
  owns and what remains outside it.
- [subgraph-capsules.md](subgraph-capsules.md): local graph detail as a
  traceable capsule.
- [subgraph-role-registry.md](subgraph-role-registry.md): current subgraph
  roles and authority boundaries.
- [anchor-lens-promise.md](anchor-lens-promise.md): stable source identity,
  lens application identity, and promise status.
- [visual-media-encoding.md](visual-media-encoding.md): traceable image and
  video records as fields, regions, tracks, events, and graph views.
- [path-state-graph.md](path-state-graph.md): active, candidate, committed,
  and historical paths through runtime state.
- [hierarchical-execution-cycles.md](hierarchical-execution-cycles.md):
  parent/child cycles, budgets, deferrals, and authority boundaries.
- [offline-replay-dream-cycles.md](offline-replay-dream-cycles.md): late
  outcome resolution, real-trace replay, and counterfactual hypothesis cycles.
- [provisional-graph-growth.md](provisional-graph-growth.md): bounded graph
  adaptation through provisional capsules, candidate variants, promotion gates,
  and rollback.
- [belief-state.md](belief-state.md): uncertainty, confidence, calibration,
  evidence weight, and belief refs.
- [bayesian-filtering-state-estimation.md](bayesian-filtering-state-estimation.md):
  process prediction, measurement update, posterior belief, and innovation.
- [graph-runtime-memory.md](graph-runtime-memory.md): graph memory versus
  agent/project memory.
- [cognitive-map-memory.md](cognitive-map-memory.md): relational recall
  structure over physical, conceptual, or latent task spaces.
- [engram-spatial-memory.md](engram-spatial-memory.md): sparse reactivatable
  episode traces.
- [operating-cycle.md](operating-cycle.md): encode, propose, verify, commit,
  execute, observe, resolve, and consolidate.
- [granular-analysis.md](granular-analysis.md): one input fan-out through
  many lenses and proposers into one traceable outcome.
- [predictive-action-graph.md](predictive-action-graph.md): action selection
  by comparing traceable predicted futures.
- [cortical-column-world-model.md](cortical-column-world-model.md): local
  sensorimotor predictive subgraphs, lateral aggregation, prediction error,
  and outcome-coupled memory.
- [multimodal-outcome-stack.md](multimodal-outcome-stack.md): reusable
  evidence-to-outcome stack for multimodal and multi-view cases.
- [path-conditioned-and-path-gated.md](path-conditioned-and-path-gated.md):
  central primer for CGF path-aware Architecture.
- [contracts/README.md](contracts/README.md): event, proposal, commit,
  outcome, trace, and persistence contract cards.
- [frameworks/README.md](frameworks/README.md): reusable Architecture
  framework cards for bots, evidence records, multimodal graphs, routing,
  review, cache, security, and sensor ingestion.
- [examples/README.md](examples/README.md): self-contained Architecture
  examples.

Research bridge:

- [research-bridge.md](research-bridge.md): Architecture bridge for path-state,
  contracts, proposal / verification / commit, event log, trace, replay,
  memory, path-aware operators, and evaluation discipline.
- [path-conditioned-operators.md](path-conditioned-operators.md):
  Architecture operator pattern for using path context as an explicit input.
- [path-gated-operators.md](path-gated-operators.md): Architecture operator
  pattern for explicit path-evidence gates.

Framework catalog:

- [frameworks/registry.md](frameworks/registry.md): reusable Architecture
  framework registry.
- [frameworks/cards/README.md](frameworks/cards/README.md): compact framework
  cards, including the cortical-column world-model framework. Applications
  should compose these cards instead of owning reusable concepts.

Reference code:

- [reference/python/README.md](reference/python/README.md): optional
  stdlib-only Architecture reference implementation and tests.
