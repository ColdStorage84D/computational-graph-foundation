# Architecture Status

This page records the current readiness of the Architecture section.

## Current Status

Architecture has a v0.2 documentation and reference-code base for operating
around declared Substrate subjects.

It is ready enough for a developer to:

- understand the execution graph and runtime spine;
- separate brain, spine, surface nodes, and subgraph capsules;
- separate proposals from commits;
- explain Granular Analysis as many lenses, many proposers, one traceable
  outcome;
- explain Predictive Action Graph as action selection by comparing predicted
  futures before committing one first action;
- explain Local-Voting World Model as local sensorimotor predictive
  subgraphs that aggregate proposals, expose prediction error, and keep safety
  gates outside learned preference scoring;
- explain the Multimodal Outcome Stack as evidence records, typed multimodal
  graph, feature views, processor routes, proposals, review, and trace;
- explain Signal Review as signal views, route-specific processors, proposals,
  verifier / review / abstain, and traceable signal decisions;
- explain Anchor / Lens / Promise as stable, replayable view identity for
  external or delayed evidence;
- explain Visual Media Encoding as image and video evidence turned into
  source-bounded graph views;
- explain Hierarchical Execution Cycles as parent/child graph cycles with
  bounded budgets and authority;
- explain Belief State and Bayesian Filtering as traceable state estimates
  under uncertainty;
- explain Offline Replay Cycles, Cognitive Map Memory, and Cued Recall
  Memory as graph-memory patterns with labeled recall and replay
  boundaries;
- explain Provisional Graph Growth as bounded graph adaptation with provisional
  capsules, candidate variants, stability guards, promotion gates, and rollback;
- define event, proposal, commit, outcome, trace, and persistence records;
- choose reusable framework cards without confusing them with applications;
- distinguish path-conditioned computation from path-gated control;
- describe graph runtime memory without confusing it with agent/project memory;
- use example patterns to decide whether Architecture is needed.

It is not a mandatory runtime, SDK, schema package, or product framework. The
reference code is optional and section-local.

## Stable Architecture Ideas

The stable v0.2 ideas are:

```text
execution graph
runtime spine
graph brain and spine
subgraph capsules
path-state graph
proposal / verification / commit
granular analysis
predictive action graph
local-voting world model
multimodal outcome stack
signal review
anchor / lens / promise
visual media encoding
hierarchical execution cycles
belief state / Bayesian filtering
offline replay cycles
cognitive map memory
cued recall memory
provisional graph growth
event log / trace / replay
path-conditioned / path-gated operation
eligibility / outcome / graph runtime memory
action accounting / policy gates
reusable Architecture framework cards
```

## Ready Documents

- [README.md](README.md): short section entry.
- [INDEX.md](INDEX.md): full Architecture map.
- [responsibility-boundary.md](responsibility-boundary.md): layer boundary.
- [execution-graph.md](execution-graph.md): operating graph that acts.
- [runtime-spine.md](runtime-spine.md): central operating path.
- [graph-brain-and-spine.md](graph-brain-and-spine.md): brain/spine pattern.
- [subgraph-capsules.md](subgraph-capsules.md): local graph boundary pattern.
- [graph-runtime-memory.md](graph-runtime-memory.md): memory roles and rules.
- [path-state-graph.md](path-state-graph.md): runtime path representation.
- [granular-analysis.md](granular-analysis.md): multi-lens, multi-proposer
  outcome analysis.
- [predictive-action-graph.md](predictive-action-graph.md): action selection
  through candidate action sequences, predicted futures, gate, trace, and
  outcome-coupled memory.
- [local-voting-world-model.md](local-voting-world-model.md): local
  sensorimotor predictive subgraphs, lateral proposal aggregation, prediction
  error, outcome-coupled memory, and safety gate separation.
- [multimodal-outcome-stack.md](multimodal-outcome-stack.md): reusable
  multimodal evidence-to-outcome framework mix.
- [frameworks/cards/signal-review-framework.md](frameworks/cards/signal-review-framework.md):
  reusable signal, alert, anomaly, risk, and operational review pattern.
- [anchor-lens-promise.md](anchor-lens-promise.md): stable view identity,
  delayed materialization, and promise state.
- [visual-media-encoding.md](visual-media-encoding.md): source frames,
  regions, tracks, encoded features, and graph evidence refs.
- [hierarchical-execution-cycles.md](hierarchical-execution-cycles.md):
  parent/child graph cycles with budget, deferral, and authority boundaries.
- [subgraph-role-registry.md](subgraph-role-registry.md): reusable subgraph
  roles and their authority limits.
- [belief-state.md](belief-state.md): state estimates as evidence instead of
  hidden truth.
- [bayesian-filtering-state-estimation.md](bayesian-filtering-state-estimation.md):
  predict/update filtering, innovation, covariance, and traceable estimates.
- [offline-replay-cycles.md](offline-replay-cycles.md): offline
  replay, simulated alternatives, consolidation, and claim boundaries.
- [provisional-graph-growth.md](provisional-graph-growth.md): bounded graph
  adaptation through provisional structure, shadow scoring, promotion, and
  rollback.
- [cognitive-map-memory.md](cognitive-map-memory.md): place, route, landmark,
  and spatial-context memory roles.
- [cued-recall-memory.md](cued-recall-memory.md): cue-bounded recall and
  spatial memory fragments.
- [path-conditioned-and-path-gated.md](path-conditioned-and-path-gated.md):
  central path-aware Architecture primer.
- [path-conditioned-operators.md](path-conditioned-operators.md): path
  context as an operator input.
- [path-gated-operators.md](path-gated-operators.md): explicit path-evidence
  gates.
- [operating-cycle.md](operating-cycle.md): repeatable decision cycle.
- [contracts/README.md](contracts/README.md): contract card index.
- [frameworks/README.md](frameworks/README.md): reusable framework catalog.
- [frameworks/registry.md](frameworks/registry.md): framework card registry.
- [examples/README.md](examples/README.md): example index.
- [reference/python/README.md](reference/python/README.md): optional
  stdlib-only reference implementation.

## Promotion Gate

An Architecture pattern is ready to guide implementation when it can answer:

```text
1. What Substrate subject does it operate around?
2. What event starts the operating cycle?
3. What view or path is created?
4. Does path context condition any score, threshold, route, message, or readout?
5. Does any path gate allow, block, defer, review, fallback, or abstain?
6. What proposals are allowed?
7. What verifies or rejects proposals?
8. If Granular Analysis is used, which lenses and proposal nodes were considered?
9. If Predictive Action Graph is used, which candidate actions, predicted futures, gate, selected first action, and rejected alternatives are visible?
10. If Local-Voting World Model is used, which local columns, predictions, residuals, aggregation records, safety gates, and memory updates are visible?
11. If the Multimodal Outcome Stack is used, which evidence records, typed graph records, views, routes, proposals, and review states are separated?
12. If Signal Review is used, which signal views, routes, proposals, verifier basis, and abstain or fallback reasons are visible?
13. If Anchor / Lens / Promise is used, what anchor identifies the source, what
    lens materializes the view, and what promise state is visible?
14. If Visual Media Encoding is used, which source frames, regions, tracks,
    features, confidence values, and evidence refs are visible?
15. If Hierarchical Execution Cycles are used, what budget, deferral, failure,
    and final-authority boundaries are declared?
16. If Belief State or Bayesian Filtering is used, what prediction, update,
    uncertainty, innovation, and evidence refs are visible?
17. If offline replay, cognitive map, or cued recall memory is used, how are real
    observed outcomes separated from replayed, simulated, or recalled records?
18. What commit boundary decides accepted action or non-action?
19. What trace reconstructs the decision?
20. What outcome resolves the decision?
21. What memory or value update is allowed?
22. Which reusable framework card is being used, if any?
23. What replay should rebuild?
```

If any answer is missing, keep the pattern in Architecture draft form.

## Not Claimed

Architecture does not claim:

- a required SDK;
- a required database;
- a service bus;
- a runtime package;
- a universal orchestrator;
- production validation.

Future code can be added section-locally when there is a stable contract and a
small eval or example that justifies it.
