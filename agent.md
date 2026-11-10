# Agent Editing Standards

This file defines the working rules for agents and contributors editing CGF.
Use it before creating, moving, rewriting, or expanding project material.

CGF should stay easy to read, copy, fork, and implement independently.

## Required Operating References

Before analyzing, editing, or applying CGF to a project, use these files as the
main navigation surface:

| File | Use it for |
| --- | --- |
| [FOUNDATION_TRAVERSAL.md](FOUNDATION_TRAVERSAL.md) | Start here when choosing the right CGF mix for a project or tracing support from Substrate to Research and Labs. |
| [README.md](README.md) | Confirm project identity, public ladder, repo posture, and section responsibilities. |
| [PUBLIC_BASE_CHECKLIST.md](PUBLIC_BASE_CHECKLIST.md) | Use as the release gate for public-base status, supported claims, known gaps, and final checks. |
| [ROADMAP.md](ROADMAP.md) | Confirm what is done for the public base, what is intentionally deferred, and what comes next. |
| [RELEASE_NOTES.md](RELEASE_NOTES.md) | Confirm the current public base snapshot contents and boundaries. |
| [PUBLISHING.md](PUBLISHING.md) | Prepare a verified candidate for a standalone or deliberate monorepo release. |
| [SECURITY.md](SECURITY.md) | Route sensitive vulnerability reports without public disclosure. |
| [SUPPORT.md](SUPPORT.md) | Route usage questions, defects, and scope-limited support requests. |
| [templates/project-intake.md](templates/project-intake.md) | Record a project-level CGF traversal decision before proposing implementation. |
| [substrate/INDEX.md](substrate/INDEX.md) | Navigate the full Substrate section and find the right core, derivative, extension, template, spec, or example document. |
| [substrate/templates/subject-template.md](substrate/templates/subject-template.md) | Draft a complete 9-core Substrate declaration for a new subject. |
| [substrate/extensions/decision-guide.md](substrate/extensions/decision-guide.md) | Decide whether an extension is required, optional, or wrong. |
| [substrate/extensions/topology-guide.md](substrate/extensions/topology-guide.md) | Use when topology appears so graph topology, higher-dimensional topology, topological rigidity, and application graph topology are not mixed together. |
| [substrate/extensions/registry.md](substrate/extensions/registry.md) | See current extension cards, research support, Labs eval links, and maturity labels. |
| [substrate/extensions/cards/cell-complex-view.md](substrate/extensions/cards/cell-complex-view.md) | Use when cells, boundaries, regions, surfaces, volumes, or episode support must be declared above node-edge graph support. |
| [substrate/extensions/cards/attractor-diagnostics.md](substrate/extensions/cards/attractor-diagnostics.md) | Use when recurrence, basins, traps, regime persistence, or escape warnings matter for a dynamical subject. |
| [substrate/extensions/cards/basis-mode-representation.md](substrate/extensions/cards/basis-mode-representation.md) | Use when symmetry, modes, selection rules, or eigenbasis structure may make the graph a graph of modes rather than samples. |
| [substrate/derivatives/action-native-computation.md](substrate/derivatives/action-native-computation.md) | Use when a project frames calculation as graph-state evolution under an action, law, energy, loss, objective, constraint, or residual. |
| [substrate/derivatives/stationary-path.md](substrate/derivatives/stationary-path.md) | Use when stationary action, least action, geodesic, variational path, admissible variation, or residual-based stationarity appears. |
| [research/connection-map.md](research/connection-map.md) | Trace each supported topic through Substrate surface, Research support, Labs result, and claim boundary. |
| [labs/evals/README.md](labs/evals/README.md) | Find runnable evals and understand result labels such as `contract-pass` and eval layers such as value-over-baseline. |
| [research/references.md](research/references.md) | Find the checked public sources behind a concept, and the topics that still have none. |
| [labs/evals/evaluation-methodology.md](labs/evals/evaluation-methodology.md) | Use when deciding whether a result is isolated, integration, value-over-baseline, recipe-grounded, or ready for promotion. |
| [architecture/README.md](architecture/README.md) | Check whether a problem belongs to Architecture instead of Substrate. |
| [architecture/INDEX.md](architecture/INDEX.md) | Navigate Architecture runtime spine, patterns, contracts, and examples. |
| [architecture/frameworks/README.md](architecture/frameworks/README.md) | Use when a reusable Architecture framework concept must be separated from an application. |
| [architecture/frameworks/selection-guide.md](architecture/frameworks/selection-guide.md) | Start here when choosing framework cards from a project shape. |
| [architecture/frameworks/registry.md](architecture/frameworks/registry.md) | Choose framework cards such as bot graph, evidence record, multimodal graph, Provisional Graph Growth, routing, review, cache, security, and sensor ingestion. |
| [architecture/execution-graph.md](architecture/execution-graph.md) | Start here for bots, workflows, processors, graph runtimes, and systems that act. |
| [architecture/granular-analysis.md](architecture/granular-analysis.md) | Use when one input fans out through many lenses, proposal nodes, and outcome candidates. |
| [architecture/predictive-action-graph.md](architecture/predictive-action-graph.md) | Use when actions are selected by comparing candidate action sequences through predicted futures. |
| [architecture/multimodal-outcome-stack.md](architecture/multimodal-outcome-stack.md) | Use when external evidence, typed records, feature views, processor routes, proposals, review, and trace must stay separated. |
| [architecture/runtime-spine.md](architecture/runtime-spine.md) | Use the central Architecture chain for routing, authority, replay, audit, and outcome coupling. |
| [architecture/anchor-lens-promise.md](architecture/anchor-lens-promise.md) | Use when external records need stable view identity, delayed materialization, or replayable lens outputs. |
| [architecture/visual-media-encoding.md](architecture/visual-media-encoding.md) | Use when image or video evidence must become graph evidence through frames, regions, tracks, and evidence refs. |
| [architecture/hierarchical-execution-cycles.md](architecture/hierarchical-execution-cycles.md) | Use when parent graphs delegate bounded work to specialist child cycles. |
| [architecture/subgraph-role-registry.md](architecture/subgraph-role-registry.md) | Use when subgraphs need clear roles such as worker, verifier, memory, route, adapter, or sandbox. |
| [architecture/belief-state.md](architecture/belief-state.md) | Use when an Architecture layer holds a noisy estimate rather than directly observed truth. |
| [architecture/bayesian-filtering-state-estimation.md](architecture/bayesian-filtering-state-estimation.md) | Use when predict/update filtering, innovation, gain, or covariance should be traceable. |
| [architecture/offline-replay-cycles.md](architecture/offline-replay-cycles.md) | Use when offline replay, simulated alternatives, or consolidation cycles appear. |
| [architecture/cognitive-map-memory.md](architecture/cognitive-map-memory.md) | Use when place, route, landmark, or spatial-context recall must be graph memory instead of notes. |
| [architecture/cued-recall-memory.md](architecture/cued-recall-memory.md) | Use when episode fragments, cues, and spatial recall need bounded reactivation rules. |
| [architecture/graph-brain-and-spine.md](architecture/graph-brain-and-spine.md) | Separate brain coordination, spine routing, surface nodes, child graphs, and the core cycle. |
| [architecture/subgraph-capsules.md](architecture/subgraph-capsules.md) | Use when local graph detail should be routeable without hiding evidence or authority. |
| [architecture/graph-runtime-memory.md](architecture/graph-runtime-memory.md) | Distinguish graph runtime memory from agent/project memory and define memory roles. |
| [architecture/provisional-graph-growth.md](architecture/provisional-graph-growth.md) | Use when recurring evidence may justify new graph routes, rules, edges, specialists, or local graph structure. |
| [architecture/frameworks/cards/provisional-graph-growth-framework.md](architecture/frameworks/cards/provisional-graph-growth-framework.md) | Use when Provisional Graph Growth should be selected as a reusable framework card for bots, workflows, routes, triage, or controllers. |
| [architecture/path-conditioned-and-path-gated.md](architecture/path-conditioned-and-path-gated.md) | Decide whether path influence is conditioning, gating, or both. |
| [architecture/path-conditioned-operators.md](architecture/path-conditioned-operators.md) | Use when path context changes score, threshold, route, message, ranking, or readout. |
| [architecture/path-gated-operators.md](architecture/path-gated-operators.md) | Use when a gate controls path influence or proposal advancement. |
| [architecture/reference/python/README.md](architecture/reference/python/README.md) | Inspect optional stdlib-only Architecture reference contracts and tests. |
| [applications/DEMO_GUIDE.md](applications/DEMO_GUIDE.md) | Use the recommended forkable demo path: Signal Review -> Medical Image Analysis -> Graph Memory Bot. |
| [applications/bots/README.md](applications/bots/README.md) | Inspect Graph Memory Bot for execution graph, trace, topology, candidate actions, gates, and graph runtime memory. |
| [applications/maze-graph-memory-bot/README.md](applications/maze-graph-memory-bot/README.md) | Inspect the shipped Webots maze app for Graph Memory Bot action, trace, and memory in a simulator fixture. |
| [applications/industrial-robot-arm/README.md](applications/industrial-robot-arm/README.md) | Inspect the shipped Webots Industrial Robot Arm Graph app for topology, safety gates, emitted commands, evidence paths, and trace. |
| [applications/industrial-robot-arm/claim-boundary.md](applications/industrial-robot-arm/claim-boundary.md) | Check robot-arm safety, manufacturing, benchmark, and autonomy claim limits. |
| [applications/medical-image-analysis/README.md](applications/medical-image-analysis/README.md) | Inspect Medical Image Analysis as an application example composed from reusable framework cards. |
| [applications/medical-image-analysis/walkthrough.md](applications/medical-image-analysis/walkthrough.md) | Use when drafting a medical image analysis review workflow from reusable Architecture patterns. |
| [applications/medical-image-analysis/claim-boundary.md](applications/medical-image-analysis/claim-boundary.md) | Check what the Medical Image Analysis application can and cannot claim. |

Use the shortest path that answers the task, but do not skip the connection map
when making support, maturity, or validation claims.

## Project Identity

Use the public project name:

```text
Computational Graph Foundation
```

Use `CGF` only when a short form improves readability.

Do not use stale umbrella names. Do not rename the project around one technique,
operator, runtime idea, or implementation style.

The public ladder is:

```text
CGF -> Substrate -> Architecture -> Applications
```

## Layer Responsibilities

Keep each layer responsible for one kind of work:

| Layer | Responsibility |
| --- | --- |
| `substrate/` | Declares the graph-shaped computational subject. |
| `architecture/` | Describes how systems operate around declared subjects. |
| `applications/` | Holds domain-specific uses and showcases. |
| `research/` | Holds self-contained theory, references, and claim boundaries. |
| `labs/` | Holds active experiments. |
| `archive/` | Holds historical or deprecated material. |

Do not move runtime machinery, service orchestration, product behavior, or
implementation choices into Substrate.

## Substrate Standard

Substrate is the first technical layer. It declares what is being computed
before choosing a runtime, solver, package, or application design.

Every complete Substrate subject must declare the 9 core primitives:

```text
graph
typed field
placement
state
action
constraint
evolution
readout
validation
```

Substrate has three tiers:

```text
core primitives
derivative mechanics
extension components
```

When editing Substrate:

- Keep all 9 primitives explicit.
- Do not imply a primitive through prose if it should be declared directly.
- Keep examples small enough that the primitive mapping is visible.
- Keep derivative mechanics in `substrate/derivatives/`.
- Keep extension components in `substrate/extensions/`.
- Keep `substrate/primitives.md` and `substrate/spec/primitive-cards/`
  core-only.
- When symmetry, eigenbasis, modes, or selection rules appear, ask whether the
  graph is a graph of samples or a graph of modes before choosing basis-mode
  representation.
- When cells, boundaries, regions, surfaces, volumes, or episode support appear,
  ask whether CellComplexView is needed before forcing the subject into only
  node-edge support.
- When recurrence, basins, traps, regime persistence, or escape warnings
  appear, use Attractor Diagnostics as a Substrate extension candidate and keep
  it separate from solver or controller claims.
- When a project says computation follows from action, law, energy, loss,
  objective, constraints, or residuals, use
  `substrate/derivatives/action-native-computation.md`. Require a declared
  action or law, admissible changes, constraints, evolution, residual, readout,
  and validation before making a calculation claim.
- When stationary action, least action, geodesic, variational path,
  Euler-Lagrange style reasoning, or residual-based stationarity appears, use
  `substrate/derivatives/stationary-path.md`. Keep this separate from
  Architecture path-conditioned or path-gated operation.
- When topology appears, use `substrate/extensions/topology-guide.md` before
  choosing topological rigidity or a higher-dimensional topology research path.
- When an encoder converts structured input into vectors, features, regions, or
  graph views, check whether topology-aware encoding should protect arrangement,
  boundaries, loops, rare transitions, phase-like structure, or connectivity.
  Treat improvement claims as hypotheses until a local or documented benchmark
  supports them.
- Use `substrate/primitive-implementation.md` for tiny inline code and light
  math that explains primitive representation.
- Use `substrate/derivatives/implementation.md` for tiny inline code and light
  math that explains derivative mechanics.
- Keep deeper algorithms, solver choice, papers, and method-specific math in
  derivatives, extensions, research, or future section-local implementation
  docs.
- Keep Architecture terms out of Substrate examples unless the document is
  explicitly about crossing the layer boundary.

## Architecture Standard

Architecture explains how CGF systems operate around declared subjects.

Architecture may discuss runtime graph views, runtime node roles, path-state
graphs, execution graphs, graph brain/spine coordination, subgraph capsules,
path-conditioned or path-gated operators, proposal and commit flows, event
logs, replay, graph runtime memory, feedback, and evaluation discipline.

The execution graph is the operating surface that acts. It keeps view,
proposal, gate, verifier, commit, trace, outcome, memory update, and replay
separate.

The graph brain coordinates phases. The spine routes records. Surface nodes own
local transforms. Subgraph capsules own local detail. Commit and outcome
coupling remain the authority path.

Graph runtime memory is not the same as agent/project memory. Notes,
summaries, claims, or user preferences become graph runtime memory only when
they enter through declared evidence, proposal, commit, outcome, and memory
update paths.

Provisional Graph Growth is the Architecture pattern for bounded graph
adaptation. Use it when repeated evidence suggests a new route, rule, edge,
specialist, or local graph structure. Require a provisional capsule, bounded
candidate variants, shadow scoring, stability guard, promotion gate, and
rollback policy. One-off events, bursts, and low-quality trends must not mutate
durable graph state.

When this pattern can be reused outside one app, select the
[Provisional Graph Growth framework card](architecture/frameworks/cards/provisional-graph-growth-framework.md)
and record the claim boundary from
[labs/evals/provisional-graph-growth/results.md](labs/evals/provisional-graph-growth/results.md).

Anchor / Lens / Promise is the Architecture pattern for stable view identity.
Use it when external records, delayed features, or derived views must be
addressable and replayable before they are used by proposal or verifier logic.

Visual Media Encoding is the Architecture pattern for turning image or video
evidence into graph evidence. Use it when a system needs source frames,
regions, tracks, encoded features, confidence, and evidence refs instead of a
hidden visual vector.

Hierarchical Execution Cycles are the Architecture pattern for parent graphs
that delegate bounded work to specialist child cycles. Child cycles may return
evidence, proposals, deferrals, or failure records; they do not silently own
final commit authority.

Belief State and Bayesian Filtering are Architecture patterns for traceable
state estimates under uncertainty. Use them when prediction, update,
innovation, covariance, or confidence should be visible and bounded rather
than treated as hidden truth.

Offline Replay Cycles, Cognitive Map Memory, and Cued Recall Memory are
Architecture memory patterns. They may organize replayed,
simulated, spatial, or cued recall records, but real observed outcomes,
counterfactuals, and recalled material must remain labeled separately.

Architecture framework cards are reusable operating patterns. They belong in
`architecture/frameworks/` when they can be used outside one application.
Applications such as bots and medical image analysis compose those cards; they do not own the
reusable concepts.

Use [architecture/frameworks/selection-guide.md](architecture/frameworks/selection-guide.md)
before choosing framework cards from a project shape. The guide maps project
shape to failure mode, framework mix, owning Architecture docs, and current
eval or claim boundary.

Granular Analysis is a first-class Architecture concept and sales-pitch pillar:
many lenses, many proposers, one traceable outcome. Use it when one input can
produce multiple lens outputs, those outputs can feed multiple proposal nodes,
and one outcome should preserve selected and rejected proposals.

Predictive Action Graph is a first-class Architecture concept for action
selection through predicted futures. Use it when a system should compare
candidate action sequences, predict their expected future evidence, gate the
best candidate, commit one first action, preserve rejected alternatives, and
update graph runtime memory only after outcome observation.

For image-control examples, keep the action path image-only unless a document
explicitly declares privileged state. RGB frames and image-derived visual
features may drive the graph. Simulator-provided object position, angle,
contact count, distance, hidden success, or other privileged state must not
drive action selection.

When the image contains structure, prefer the generic hypergraph encoder over a
task-specific flat vector. The encoder should expose typed evidence nodes,
hyperedges, features, confidence, and evidence refs. Application role binding
can map encoded evidence to task roles, but the encoder itself should remain
domain-neutral.

The Multimodal Outcome Stack is the Architecture mix for cases that need
external evidence records, typed multimodal graph records, feature views,
processor routes, proposals, review state, and traceable outcomes. Use it when
one case has several evidence surfaces and when labels, later outcomes, or
review decisions must be kept out of live feature paths.

Path-conditioned and path-gated operation are first-class Architecture
concepts:

- Path-conditioned means path context changes scoring, thresholds, routing,
  ranking, message passing, readout, or operator behavior.
- Path-gated means an explicit gate controls how much path evidence influences
  computation or whether a proposal can advance.
- They can compose, but neither replaces proposal, verifier, commit, trace,
  replay, outcome memory, or evaluation discipline.

Do not make Architecture required for a developer who only wants to copy a
Substrate idea and implement it independently.

Do not trap reusable framework concepts inside an application example. If a
concept could support unrelated projects, create or update a framework card and
let applications link to it.

## Creating Documents

When adding a document:

- Put it in the section that owns the responsibility.
- Add a short title and a clear first paragraph.
- State what the document is for.
- State what the document is not for when the boundary matters.
- Link it from the nearest `README.md` or index when it should be discoverable.
- Keep the document self-contained. Do not depend on private history or old
  research folders for meaning.
- Prefer concise tables and checklists when they clarify responsibilities.

New folders should include a `README.md` unless they are intentionally temporary
and local to an experiment.

## Editing Documents

When editing existing material:

- Preserve the public ladder and section responsibilities.
- Prefer direct definitions over broad claims.
- Keep public language stable once a term is chosen.
- Remove stale names instead of explaining around them.
- Do not add unrelated refactors during a focused pass.
- Avoid duplicating the same explanation across many files; link to the owner
  document instead.
- Keep examples readable before making them exhaustive.

Use ASCII punctuation and plain Markdown unless the existing file clearly needs
something else.

## Code Standard

CGF is docs-led first, not docs-only.

Future code is expected, but it should be section-local by default:

```text
substrate/examples/        small teaching implementations
architecture/reference/    section-local Architecture contract references
labs/evals/                experimental contract evals
applications/<domain>/     domain-specific implementations
```

Do not add a top-level SDK, package, or lock-in structure unless there is a
clear project decision and a stable contract that justifies it.

When adding code later:

- Tie it to a stable document or clear example.
- Keep dependencies minimal and explained.
- Prefer small, inspectable implementations over framework-heavy demos.
- Keep generated artifacts out of the docs unless they are part of the example.

## Eval Standard

Labs evals follow [labs/evals/README.md](labs/evals/README.md) and
[labs/evals/evaluation-methodology.md](labs/evals/evaluation-methodology.md).

- Every result record declares a status, an eval layer, the reviewed command
  or date, and a claim boundary.
- An isolated eval shows that a concept is implemented as declared. Do not
  describe it as evidence that the concept helps.
- A claim that a concept helps needs a value-over-baseline eval: a seeded
  `comparison.py`, thresholds in `test_comparison.py`, a named baseline, and a
  `Where It Does Not Help` section in the result record.
- When an eval is named after a mathematical object, `eval.py` must implement
  that object and the owning study must cite a public source for it.
- Counts written in release documents must equal the counts in the tree.

`scripts/check_public_base.py` enforces these rules.

## Usage Standard

CGF material should support three usage modes:

- Read the docs and apply the ideas independently.
- Copy or fork examples and adapt them.
- Build section-local implementations without adopting a mandatory SDK.

Do not write docs as if users must follow every recommendation. CGF should make
the structure clear without becoming a rulebook for independent developers.

## Traversal Standard

When using CGF to analyze a project, start from
[FOUNDATION_TRAVERSAL.md](FOUNDATION_TRAVERSAL.md) unless the user has already
chosen a narrower entry point.

Use [templates/project-intake.md](templates/project-intake.md) when the task is
to apply CGF to a project, compare possible CGF mixes, or prepare an
implementation plan.

Every agent or contributor should make the path explicit:

- starting point;
- complete 9-core Substrate status;
- derivative mechanics selected or skipped;
- extensions selected, with required / optional / wrong reasoning;
- topology meaning selected or skipped when topology vocabulary appears;
- topology-aware encoding assumption checked when an encoder could collapse
  meaningful structure;
- CellComplexView selected or skipped when cells, boundaries, regions,
  surfaces, volumes, or episode support are present;
- Attractor Diagnostics selected or skipped when recurrence, basin, trap,
  regime persistence, or escape-warning language is present;
- basis-mode selected or skipped when symmetry, modes, or selection rules are
  present;
- Stationary Path selected or skipped when stationary action, least action,
  geodesic, variational path, admissible variation, or residual-based
  stationarity is present;
- composition pattern used, if any;
- Research links checked;
- Labs eval links checked and exact claim boundary;
- Architecture patterns selected or skipped;
- Architecture framework cards selected or skipped;
- Anchor / Lens / Promise selected or skipped when external records become
  stable graph views;
- Visual Media Encoding selected or skipped when image or video evidence
  becomes graph evidence;
- Hierarchical Execution Cycles and Subgraph Role Registry selected or skipped
  when parent graphs delegate work to specialist graph cycles;
- Belief State and Bayesian Filtering selected or skipped when noisy hidden
  state is estimated;
- Offline Replay, Cognitive Map, and Cued Recall Memory selected
  or skipped when replay, simulated consolidation, spatial recall, or cue-based
  recall appears;
- Granular Analysis selected or skipped when one input can fan out through
  multiple lenses, encoders, processors, or proposal nodes;
- Predictive Action Graph selected or skipped when action selection compares
  candidate action sequences through predicted futures;
- Multimodal Outcome Stack selected or skipped when one case has external
  evidence, typed records, feature views, route choices, review state, or later
  labels;
- execution graph, brain/spine, subgraph capsule, and graph runtime memory
  choices when system operation is needed;
- path-conditioned and path-gated use selected, composed, or skipped;
- remaining gaps before implementation.

When adding or promoting docs, preserve a visible chain when applicable:

```text
Substrate surface
-> Research support
-> Labs eval result
-> claim boundary
```

Do not make readers infer whether a better CGF option exists elsewhere. Link to
the owning guide, registry, connection map, or eval result.

## Review Checklist

Before finishing an edit, check:

```text
1. Does the document use the current project identity?
2. Does it fit the owning section?
3. Does it keep Substrate, Architecture, Research, Labs, and Applications separate?
4. Does it avoid stale names and old project history?
5. Does it avoid implying a mandatory SDK or package?
6. Are new links valid?
7. Are examples small and self-contained?
8. Are future-code statements section-local by default?
9. Can a reader traverse from this doc to related Substrate, Research, Labs,
   or Architecture material without guessing?
10. If the edit affects public-base readiness, is PUBLIC_BASE_CHECKLIST.md
    still accurate?
```

For Substrate-specific edits, also check:

```text
1. Are all 9 core primitives explicit when a complete subject is claimed?
2. Are derivative mechanics kept in the derivatives section?
3. Are extension components kept out of core primitive docs?
4. Are runtime and orchestration terms kept out of core examples?
```
