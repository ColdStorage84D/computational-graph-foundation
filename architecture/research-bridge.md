# Architecture Research Bridge

## Purpose

This Architecture bridge records research areas that belong to system
operation rather than Substrate declaration.

Substrate defines what is computed. Architecture defines how a CGF system
operates around declared subjects.

## Architecture-Owned Research Areas

| Area | Architecture responsibility |
| --- | --- |
| Execution graph | Define the operating graph that acts around a declared subject. |
| Graph brain and spine | Separate phase coordination, record routing, surface nodes, child graphs, and authority boundaries. |
| Runtime spine | Preserve routing, authority, replay, audit, and outcome coupling across the operating path. |
| Path-state graph | Represent active, candidate, and historical paths through system state. |
| Runtime graph views | Build operational views over declared subjects without redefining the subject. |
| Node roles | Distinguish task, choice, operator, policy, artifact, outcome, memory anchor, and subgraph capsule roles. |
| Subgraph capsules | Keep local graph detail routeable, traceable, and below commit authority. |
| Subgraph role registry | Keep specialist graph roles named, bounded, and reusable without becoming separate foundations. |
| Anchor / Lens / Promise | Preserve stable source identity, replayable lens application identity, and pending or fulfilled view status. |
| Visual media encoding | Preserve image/video source refs, frames, regions, tracks, events, and graph-view evidence. |
| Hierarchical execution cycles | Coordinate parent/child cycles, budgets, response statuses, deferrals, and authority boundaries. |
| Offline replay cycles | Separate late outcome resolution and real-trace replay from counterfactual hypothesis generation. |
| Belief state | Carry confidence, uncertainty, calibration, evidence weight, and distribution refs through operating records. |
| Bayesian filtering / state estimation | Use process prediction and measurement update as working belief evidence without durable-truth promotion. |
| Cognitive map memory | Organize relational recall over physical, conceptual, or latent task spaces. |
| Cued recall memory | Preserve sparse reactivatable episode traces as recall evidence. |
| Contracts | Define what each operational step must preserve, expose, or reject. |
| Proposal / verification / commit | Separate candidate generation, checking, and accepted state change. |
| Granular Analysis | Preserve many lens branches, many proposal nodes, and one traceable outcome. |
| Event log, trace, and replay | Preserve ordered evidence for audit and repeatable review. |
| Graph runtime memory and outcome feedback | Store outcome-backed operating memory separately from notes, summaries, and temporary state. |
| Framework cards | Separate reusable Architecture concepts from application examples. |
| Lenses, adapters, scorers, projectors | Produce and transform typed views while keeping evidence refs visible. |
| Path-conditioned operators | Use path context to change scores, thresholds, routes, messages, ranking, or readout without creating authority by itself. |
| Path-gated operators | Use explicit gates to control path influence or proposal advancement. |
| Action accounting and policy gates | Make tradeoffs explicit and keep hard gates separate from scores. |
| Evaluation discipline | Decide whether an operating pattern improves reliability, traceability, or validation. |

## Boundary With Substrate

Substrate may declare:

- graph;
- typed fields;
- placement;
- state;
- action;
- constraints;
- evolution;
- readout;
- validation;
- derivative mechanics;
- extension components.

Architecture may use those declarations, but it does not redefine them.

## Carry-Forward Rule

When research material contains both Substrate and Architecture content:

- keep field, placement, action, constraint, evolution, readout, validation,
  derivative, and extension content in Substrate or Research;
- move execution graph, graph brain/spine, subgraph capsule, proposal,
  verification, commit, granular analysis, event log, trace, replay, graph
  runtime memory, anchor/lens/promise, visual media encoding, hierarchical
  cycles, offline replay cycles, belief state, Bayesian filtering,
  cognitive map, cued recall, lens, adapter, framework-card,
  path-conditioned, path-gated, policy, and operating-contract content into
  Architecture;
- keep runnable evals, prototypes, and unfinished experiments in Labs until
  they have clean result records and maturity labels.

## Current Architecture Pass

The current Architecture pass defines:

- an execution graph explainer;
- a graph brain/spine explainer;
- a subgraph capsule explainer;
- a runtime spine explainer;
- a path-state graph explainer;
- an operating-cycle guide;
- contract cards;
- reusable framework cards;
- Granular Analysis guidance;
- proposal / verification / commit guidance;
- event log, trace, and replay guidance;
- graph runtime memory and outcome-feedback guidance;
- action accounting and policy guidance;
- path-conditioned and path-gated guidance;
- self-contained example patterns.

Those docs should remain optional and docs-led. They should not create a
mandatory SDK or package surface.
