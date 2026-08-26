# Foundation Traversal

## Purpose

This guide is the public path through CGF.

Use it when you are a developer, agent, or reviewer trying to decide which CGF
parts apply to a project without guessing whether a better fit exists somewhere
else in the repo.

CGF is not a mandatory framework. This guide helps you inspect the available
pieces, choose a useful mix, and trace each choice to its Substrate definition,
Research support, Labs eval status, and claim boundary.

When applying CGF to a real project, record the decision in
[templates/project-intake.md](templates/project-intake.md).

When preparing or reviewing a public base snapshot, use
[PUBLIC_BASE_CHECKLIST.md](PUBLIC_BASE_CHECKLIST.md) as the release gate.

## No-Guess Rule

Do not choose an extension, derivative mechanic, Architecture pattern, or code
direction until you can answer:

```text
1. What is the subject being computed?
2. Which CGF layer owns the thing I am using?
3. What problem or failure mode does it solve?
4. What other CGF pieces does it depend on?
5. Is there Research support?
6. Is there a Labs eval result?
7. What claim is actually supported?
```

If any answer is unclear, use the maps below before adding the concept to a
project.

## Fast Entry Points

| Starting point | First read | Then check | Output |
| --- | --- | --- | --- |
| Public base readiness review | [PUBLIC_BASE_CHECKLIST.md](PUBLIC_BASE_CHECKLIST.md) | [ROADMAP.md](ROADMAP.md) and [RELEASE_NOTES.md](RELEASE_NOTES.md) | Release gate, supported claims, known gaps, and final checks. |
| New project or domain problem | [substrate/templates/subject-template.md](substrate/templates/subject-template.md) | [substrate/primitives.md](substrate/primitives.md) | Complete 9-core Substrate subject. |
| Existing graph model | [substrate/spec/00-overview.md](substrate/spec/00-overview.md) | [substrate/spec/primitive-cards/README.md](substrate/spec/primitive-cards/README.md) | Gap list for missing primitives. |
| Need computation, equations, or solver path | [substrate/derivatives/README.md](substrate/derivatives/README.md) | [research/derivative-mechanics-study.md](research/derivative-mechanics-study.md) | Conditional derivative mechanics. |
| Computation as graph-state evolution under action or law | [substrate/derivatives/action-native-computation.md](substrate/derivatives/action-native-computation.md) | [research/derivative-mechanics-study.md](research/derivative-mechanics-study.md) and [labs/evals/action-native-computation/README.md](labs/evals/action-native-computation/README.md) | Action-Native Computation framing and its current tiny-fixture eval claim; not a universal calculator. |
| Stationary action, least action, geodesic, or variational path | [substrate/derivatives/stationary-path.md](substrate/derivatives/stationary-path.md) | [research/derivative-mechanics-study.md](research/derivative-mechanics-study.md) | Stationary Path as a Substrate derivative condition, not an Architecture path. |
| Failure mode or domain structure | [substrate/extensions/decision-guide.md](substrate/extensions/decision-guide.md) | [substrate/extensions/registry.md](substrate/extensions/registry.md) | Required, optional, or wrong extension choice. |
| Topology question | [substrate/extensions/topology-guide.md](substrate/extensions/topology-guide.md) | [substrate/extensions/cards/topological-rigidity.md](substrate/extensions/cards/topological-rigidity.md) and [research/extension-studies/higher-dimensional-topology.md](research/extension-studies/higher-dimensional-topology.md) | Decide whether this is graph topology, higher-dimensional topology, topological rigidity, or application graph topology. |
| Cells, boundaries, regions, surfaces, or episodes | [substrate/extensions/cards/cell-complex-view.md](substrate/extensions/cards/cell-complex-view.md) | [research/extension-studies/cell-complex-view.md](research/extension-studies/cell-complex-view.md) and [labs/evals/cell-complex-view/README.md](labs/evals/cell-complex-view/README.md) | Decide whether the subject needs a CellComplexView instead of only node-edge support. |
| Recurrence, basin, regime, or escape warning | [substrate/extensions/cards/attractor-diagnostics.md](substrate/extensions/cards/attractor-diagnostics.md) | [research/extension-studies/attractor-diagnostics.md](research/extension-studies/attractor-diagnostics.md) | Attractor Diagnostics as a research-supported extension with no direct Labs eval yet. |
| Symmetry, modes, or selection rules | [substrate/extensions/cards/basis-mode-representation.md](substrate/extensions/cards/basis-mode-representation.md) | [research/extension-studies/basis-mode-representation.md](research/extension-studies/basis-mode-representation.md) and [labs/evals/basis-mode-representation/README.md](labs/evals/basis-mode-representation/README.md) | Basis-mode subject check and current local eval claim. |
| Known extension name | [substrate/extensions/cards/README.md](substrate/extensions/cards/README.md) | [research/connection-map.md](research/connection-map.md) | Card, research study, eval status, and claim boundary. |
| Need extension combinations | [substrate/extensions/composition-patterns.md](substrate/extensions/composition-patterns.md) | [substrate/extensions/walkthroughs.md](substrate/extensions/walkthroughs.md) | Candidate mix of extensions. |
| Need proof or validation status | [research/connection-map.md](research/connection-map.md) | [labs/evals/README.md](labs/evals/README.md) | Current result label and supported claim. |
| Starting from eval code | [labs/evals/README.md](labs/evals/README.md) | Eval folder `README.md` and `results.md` | Exact contract tested and owning docs. |
| Runtime, bot, workflow, or orchestration problem | [architecture/execution-graph.md](architecture/execution-graph.md) | [architecture/INDEX.md](architecture/INDEX.md) and [architecture/runtime-spine.md](architecture/runtime-spine.md) | Architecture-owned execution graph and operating pattern. |
| One input, many lenses, many proposers | [architecture/granular-analysis.md](architecture/granular-analysis.md) | [architecture/frameworks/cards/granular-analysis-framework.md](architecture/frameworks/cards/granular-analysis-framework.md) and [labs/evals/granular-analysis/README.md](labs/evals/granular-analysis/README.md) | Granular Analysis mix and current local eval claim. |
| Action selection by predicted futures | [architecture/predictive-action-graph.md](architecture/predictive-action-graph.md) | [architecture/path-conditioned-and-path-gated.md](architecture/path-conditioned-and-path-gated.md), [architecture/proposal-verifier-commit.md](architecture/proposal-verifier-commit.md), and [architecture/graph-runtime-memory.md](architecture/graph-runtime-memory.md) | Predictive Action Graph mix with candidate futures, gate, selected first action, trace, and memory. |
| Sensorimotor world-model controller | [architecture/cortical-column-world-model.md](architecture/cortical-column-world-model.md) | [architecture/frameworks/cards/cortical-column-world-model-framework.md](architecture/frameworks/cards/cortical-column-world-model-framework.md), [architecture/predictive-action-graph.md](architecture/predictive-action-graph.md), and [labs/evals/cortical-column-world-model/README.md](labs/evals/cortical-column-world-model/README.md) | Local predictive subgraphs, lateral proposal aggregation, prediction error, explicit gates, outcome-coupled memory, and the current tiny-fixture eval claim. |
| Multimodal evidence-to-outcome case | [architecture/multimodal-outcome-stack.md](architecture/multimodal-outcome-stack.md) | [architecture/examples/multimodal-review-flow.md](architecture/examples/multimodal-review-flow.md) and [labs/evals/multimodal-framework-mix/README.md](labs/evals/multimodal-framework-mix/README.md) | Framework mix for evidence records, typed graph, views, routes, proposals, review, and trace. |
| Reusable framework concept | [architecture/frameworks/README.md](architecture/frameworks/README.md) | [architecture/frameworks/selection-guide.md](architecture/frameworks/selection-guide.md), [architecture/frameworks/registry.md](architecture/frameworks/registry.md), and [architecture/frameworks/cards/README.md](architecture/frameworks/cards/README.md) | Framework mix that can be reused outside one application. |
| Brain/spine, subgraph, or graph memory problem | [architecture/graph-brain-and-spine.md](architecture/graph-brain-and-spine.md) | [architecture/subgraph-capsules.md](architecture/subgraph-capsules.md) and [architecture/graph-runtime-memory.md](architecture/graph-runtime-memory.md) | Brain coordination, spine routing, local graph boundary, and graph runtime memory decision. |
| Path context, evidence paths, or gates affect decisions | [architecture/path-conditioned-and-path-gated.md](architecture/path-conditioned-and-path-gated.md) | [architecture/path-conditioned-operators.md](architecture/path-conditioned-operators.md) and [architecture/path-gated-operators.md](architecture/path-gated-operators.md) | Path-conditioned influence, path-gated control, or both. |
| External data must become a stable graph view | [architecture/anchor-lens-promise.md](architecture/anchor-lens-promise.md) | [labs/evals/anchor-lens-promise/README.md](labs/evals/anchor-lens-promise/README.md) | Anchor, lens, and promise identity for replayable view materialization. |
| Image or video evidence must become graph evidence | [architecture/visual-media-encoding.md](architecture/visual-media-encoding.md) | [labs/evals/visual-media-encoding/README.md](labs/evals/visual-media-encoding/README.md) | Regions, tracks, frame refs, and graph views from visual media. |
| Parent graph delegates to specialist cycles | [architecture/hierarchical-execution-cycles.md](architecture/hierarchical-execution-cycles.md) | [labs/evals/hierarchical-cycles/README.md](labs/evals/hierarchical-cycles/README.md) | Parent/child graph cycles with budget, deferral, and authority boundaries. |
| Noisy hidden state or belief estimate | [architecture/belief-state.md](architecture/belief-state.md) | [architecture/bayesian-filtering-state-estimation.md](architecture/bayesian-filtering-state-estimation.md) and [labs/evals/bayesian-filtering/README.md](labs/evals/bayesian-filtering/README.md) | Belief-state evidence and Bayesian filtering as traceable estimates, not hidden truth. |
| Offline replay, dream, cognitive map, or engram memory | [architecture/offline-replay-dream-cycles.md](architecture/offline-replay-dream-cycles.md) | [architecture/cognitive-map-memory.md](architecture/cognitive-map-memory.md), [architecture/engram-spatial-memory.md](architecture/engram-spatial-memory.md), and [architecture/graph-runtime-memory.md](architecture/graph-runtime-memory.md) | Replay, recall, and spatial memory roles without giving them commit authority. |
| Recurring evidence suggests the graph should grow | [architecture/provisional-graph-growth.md](architecture/provisional-graph-growth.md) | [architecture/frameworks/cards/provisional-graph-growth-framework.md](architecture/frameworks/cards/provisional-graph-growth-framework.md), [labs/evals/provisional-graph-growth/README.md](labs/evals/provisional-graph-growth/README.md), and [research/connection-map.md](research/connection-map.md) | Provisional capsules, candidate variants, stability guards, promotion gates, rollback, and current local eval claim. |
| Need copyable Architecture contracts | [architecture/reference/python/README.md](architecture/reference/python/README.md) | [applications/bots/README.md](applications/bots/README.md) when the system is bot-shaped | Optional section-local reference code and tests. |
| Forkable application demos | [applications/DEMO_GUIDE.md](applications/DEMO_GUIDE.md) | [applications/signal-review/README.md](applications/signal-review/README.md), [applications/medical-image-analysis/README.md](applications/medical-image-analysis/README.md), [applications/bots/README.md](applications/bots/README.md), [applications/maze-graph-memory-bot/README.md](applications/maze-graph-memory-bot/README.md), and [applications/industrial-robot-arm/README.md](applications/industrial-robot-arm/README.md) | Start with Signal Review, then Medical Image Analysis, then Graph Memory Bot; use the maze and industrial arm Webots apps for simulator fixtures. |
| Application showcase | [applications/README.md](applications/README.md) | [research/application-class-studies.md](research/application-class-studies.md) | Domain-facing example candidate. |

## Required Traversal

Every serious use of CGF should follow this path:

```text
Substrate core
-> derivative need check
-> extension need check
-> composition check
-> research support check
-> Labs eval check
-> Architecture check, only if system operation is needed
-> Application or section-local implementation
```

### 1. Start With The Core Subject

Use [substrate/primitives.md](substrate/primitives.md) and
[substrate/templates/subject-template.md](substrate/templates/subject-template.md).

Do not move on until the subject declares:

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

### 2. Decide Whether Derivatives Are Needed

Use [substrate/derivatives/README.md](substrate/derivatives/README.md).

Derivative mechanics are useful when the subject needs equations, units,
boundaries, sources, action-derived updates, residuals, invariants, or solver
selection. They are not mandatory for every subject.

### 3. Decide Whether Extensions Are Needed

Use [substrate/extensions/decision-guide.md](substrate/extensions/decision-guide.md).

An extension is required only when leaving it out would make the subject
misleading or invalid. It is optional when it improves validation or clarity.
It is wrong when it adds vocabulary without preventing a real failure mode.

### 4. Check How Pieces Work Together

Use [substrate/extensions/composition-patterns.md](substrate/extensions/composition-patterns.md).

Extension combinations should make validation clearer, not broader. If the mix
creates hidden assumptions, reduce it or move the unresolved part to Research.

### 5. Trace Support

Use [research/connection-map.md](research/connection-map.md).

This is the support chain:

```text
Substrate card or contract
-> Research study or reference queue
-> Labs eval result, when one exists
-> claim boundary
```

No Labs eval means no pass claim. A `contract-pass` result means the tiny
CGF-local fixture passed its stated contract; it does not prove broad domain
performance.

### 6. Add Architecture Only When Needed

Use [architecture/README.md](architecture/README.md).

Architecture is for operating around a declared subject: execution graph,
graph brain/spine, subgraph capsules, runtime graph views, runtime spine,
path-state, proposals, verification, commit, event logs, trace, replay, graph
runtime memory, action accounting, policy, path-conditioned operators,
path-gated operators, and evaluation discipline. It is not required for someone
who only wants to copy a Substrate idea.

Use [architecture/frameworks/selection-guide.md](architecture/frameworks/selection-guide.md)
when starting from a project shape and choosing a reusable Architecture
framework mix. Applications such as bots and medical image analysis should compose framework
cards instead of owning reusable concepts.

## Capability Selection Map

| Need | Use | Support path | Current status |
| --- | --- | --- | --- |
| Declare any graph-shaped subject | 9-core primitives | [Substrate spec](substrate/spec/00-overview.md) -> [research map](research/substrate-research-map.md) | Stable v0.1 contract. |
| Teach minimal computation | Primitive implementation bridge | [primitive-implementation.md](substrate/primitive-implementation.md) -> [research map](research/substrate-research-map.md) | Teaching guide, not API. |
| Derive equations or operators | Derivative mechanics | [derivatives](substrate/derivatives/README.md) -> [derivative study](research/derivative-mechanics-study.md) | v0.2 docs; no Labs eval yet. |
| Treat calculation as constrained graph-state evolution | Action-Native Computation | [guide](substrate/derivatives/action-native-computation.md) -> [derivative study](research/derivative-mechanics-study.md) -> [eval](labs/evals/action-native-computation/results.md) | Tiny-fixture `contract-pass`; no solver, physics, broad optimization, or analog-computing performance claim. |
| Declare least-action or variational stationarity | Stationary Path | [guide](substrate/derivatives/stationary-path.md) -> [derivative study](research/derivative-mechanics-study.md) | Docs/research-supported; no direct Labs eval yet. |
| Handle external conditions | Exterior placement | [card](substrate/extensions/cards/exterior-placement.md) -> [geometric discretization](research/extension-studies/geometric-discretization.md) -> [eval](labs/evals/exterior-placement/results.md) | Tiny-fixture `contract-pass`; no production coupling or domain-performance claim. |
| Use weak or aggregate laws | Weak form | [card](substrate/extensions/cards/weak-form.md) -> [geometric discretization](research/extension-studies/geometric-discretization.md) -> [eval](labs/evals/weak-form/results.md) | Tiny-fixture `contract-pass`; no PDE, physics, or solver-accuracy claim. |
| Decide what topology means | Topology guide | [guide](substrate/extensions/topology-guide.md) -> [topological rigidity card](substrate/extensions/cards/topological-rigidity.md) or [higher-dimensional topology study](research/extension-studies/higher-dimensional-topology.md) | Guide only; specific claims come from the selected card, study, or eval. |
| Use cells, boundaries, regions, surfaces, or episode support | CellComplexView | [card](substrate/extensions/cards/cell-complex-view.md) -> [study](research/extension-studies/cell-complex-view.md) -> [eval](labs/evals/cell-complex-view/results.md) | Tiny-fixture `contract-pass`; no mesh solver, topology inference, or geometric accuracy claim. |
| Use symmetry, modes, or selection rules | Basis-mode representation | [card](substrate/extensions/cards/basis-mode-representation.md) -> [study](research/extension-studies/basis-mode-representation.md) -> [eval](labs/evals/basis-mode-representation/results.md) | Tiny-fixture `contract-pass`; no physics, chemistry, solver, or model-performance claim. |
| Add distance, hierarchy, or geometry | Metric placement | [card](substrate/extensions/cards/metric-placement.md) -> [study](research/extension-studies/hyperbolic-metric-placement.md) -> [eval](labs/evals/hyperbolic-placement/results.md) | Tiny-fixture `contract-pass`. |
| Preserve declared cycles, regimes, explicit phase degree, or reference-relative collapse evidence | Topological rigidity | [card](substrate/extensions/cards/topological-rigidity.md) -> [study](research/extension-studies/topological-rigidity.md) -> [eval](labs/evals/topological-rigidity/results.md) | Tiny-fixture derivative-diagnostic `contract-pass`; broad and physical claims remain research-bound. |
| Diagnose recurrence, basins, traps, or regime escape | Attractor Diagnostics | [card](substrate/extensions/cards/attractor-diagnostics.md) -> [study](research/extension-studies/attractor-diagnostics.md) | Research-supported; no direct Labs eval yet. |
| Represent uncertain transitions | Stochastic transition | [card](substrate/extensions/cards/stochastic-transition.md) -> [study](research/extension-studies/stochastic-transition.md) -> [eval](labs/evals/stochastic-transition/results.md) | Tiny-fixture `contract-pass`. |
| Compare belief or probability fields | Information geometry | [card](substrate/extensions/cards/information-geometry.md) -> [study](research/extension-studies/information-geometry.md) -> [eval](labs/evals/information-geometry/results.md) | Tiny-fixture `contract-pass`. |
| Compare fields across local frames | Gauge transport | [card](substrate/extensions/cards/gauge-transport.md) -> [study](research/extension-studies/gauge-transport.md) -> [eval](labs/evals/gauge-transport/results.md) | Tiny-fixture `contract-pass`. |
| Check local-to-global agreement | Sheaf consistency | [card](substrate/extensions/cards/sheaf-consistency.md) -> [study](research/extension-studies/sheaf-consistency.md) -> [eval](labs/evals/sheaf-consistency/results.md) | Tiny-fixture `contract-pass`. |
| Model storage, flow, ports, and dissipation | Port-Hamiltonian flow | [card](substrate/extensions/cards/port-hamiltonian-flow.md) -> [study](research/extension-studies/port-hamiltonian-flow.md) -> [eval](labs/evals/port-hamiltonian-flow/results.md) | Tiny-fixture `contract-pass`. |
| Separate observation from intervention | Causal intervention | [card](substrate/extensions/cards/causal-intervention.md) -> [study](research/extension-studies/causal-intervention.md) -> [eval](labs/evals/causal-intervention/results.md) | Tiny-fixture `contract-pass`. |
| Relate fine and coarse descriptions | Renormalization / coarse-graining | [card](substrate/extensions/cards/renormalization-coarse-graining.md) -> [study](research/extension-studies/renormalization-coarse-graining.md) -> [eval](labs/evals/renormalization-coarse-graining/results.md) | Tiny-fixture `contract-pass`. |
| Use gradients or learned surrogates | Differentiable backend + operator learning | [card](substrate/extensions/cards/differentiable-backend.md) -> [application study](research/application-class-studies.md) -> [eval](labs/evals/operator-learning/results.md) | Tiny-fixture `contract-pass`. |
| Operate a system around the subject | Execution graph + Architecture patterns | [execution graph](architecture/execution-graph.md) -> [runtime spine](architecture/runtime-spine.md) -> [contracts](architecture/contracts/README.md) | Docs-led Architecture contract and optional reference code exist. |
| Turn external records into stable views | Anchor / Lens / Promise | [guide](architecture/anchor-lens-promise.md) -> [eval](labs/evals/anchor-lens-promise/results.md) | Tiny-fixture `contract-pass` for stable identity and promise fulfillment boundaries. |
| Turn image or video into graph evidence | Visual Media Encoding | [guide](architecture/visual-media-encoding.md) -> [eval](labs/evals/visual-media-encoding/results.md) | Tiny-fixture `contract-pass` for bounded regions, tracks, frame refs, and graph-view evidence. |
| Delegate work to specialist cycles | Hierarchical Execution Cycles | [guide](architecture/hierarchical-execution-cycles.md) -> [subgraph roles](architecture/subgraph-role-registry.md) -> [eval](labs/evals/hierarchical-cycles/results.md) | Tiny-fixture `contract-pass`; child cycles cannot commit final authority. |
| Estimate hidden or noisy state | Belief State + Bayesian Filtering | [belief state](architecture/belief-state.md) -> [filtering guide](architecture/bayesian-filtering-state-estimation.md) -> [eval](labs/evals/bayesian-filtering/results.md) | Tiny-fixture `contract-pass`; no broad tracking or forecasting claim. |
| Consolidate traces offline | Offline Replay / Dream Cycles | [guide](architecture/offline-replay-dream-cycles.md) -> [graph memory](architecture/graph-runtime-memory.md) | Draft Architecture pattern; no direct Labs eval yet. |
| Recall spatial or episodic structure | Cognitive Map + Engram / Spatial Memory | [cognitive map](architecture/cognitive-map-memory.md) -> [engram memory](architecture/engram-spatial-memory.md) -> [graph memory](architecture/graph-runtime-memory.md) | Draft Architecture pattern; no direct Labs eval yet. |
| Grow graph structure from recurring evidence | Provisional Graph Growth | [guide](architecture/provisional-graph-growth.md) -> [framework card](architecture/frameworks/cards/provisional-graph-growth-framework.md) -> [bot example](applications/bots/provisional-growth-example.md) -> [eval](labs/evals/provisional-graph-growth/results.md) | Tiny-fixture `contract-pass`; no autonomous self-improvement, production safety, or broad learning-performance claim. |
| Choose reusable Architecture concepts | Architecture framework cards | [framework catalog](architecture/frameworks/README.md) -> [selection guide](architecture/frameworks/selection-guide.md) -> [registry](architecture/frameworks/registry.md) -> [cards](architecture/frameworks/cards/README.md) | Reusable patterns; not SDKs or application ownership. |
| Build a local sensorimotor world-model controller | Cortical-Column World Model | [world-model guide](architecture/cortical-column-world-model.md) -> [framework card](architecture/frameworks/cards/cortical-column-world-model-framework.md) -> [eval](labs/evals/cortical-column-world-model/results.md) -> [Maze Graph Memory Bot Webots app](applications/maze-graph-memory-bot/README.md) | Tiny-fixture `contract-pass` plus a Webots fixture; no benchmark, autonomous-control, guaranteed-solving, AGI, or biological-cortex claim. |
| Review signals, alerts, or anomalies | Signal Review | [framework card](architecture/frameworks/cards/signal-review-framework.md) -> [selection guide](architecture/frameworks/selection-guide.md) -> [eval](labs/evals/signal-review/results.md) | Tiny-fixture `contract-pass`; no financial, prediction, reliability, anomaly-performance, or maintenance claim. |
| Analyze one input through many branches | Granular Analysis | [Granular Analysis](architecture/granular-analysis.md) -> [framework card](architecture/frameworks/cards/granular-analysis-framework.md) -> [eval](labs/evals/granular-analysis/results.md) | Tiny-fixture `contract-pass` after eval passes; no domain performance claim. |
| Select actions by predicted futures | Predictive Action Graph | [Predictive Action Graph](architecture/predictive-action-graph.md) -> [Graph Memory Bot](applications/bots/README.md) -> [Maze Graph Memory Bot Webots app](applications/maze-graph-memory-bot/README.md) -> [Cortical-Column World Model](architecture/cortical-column-world-model.md) | Graph action and memory concept; no benchmark, autonomous-control, guaranteed solving, AGI, or biological-cortex claim. |
| Demonstrate safety-gated manipulator commands | Industrial Robot Arm Graph | [Industrial Robot Arm app](applications/industrial-robot-arm/README.md) -> [Webots world](applications/industrial-robot-arm/main/worlds/inverse_kinematics.wbt) -> [claim boundary](applications/industrial-robot-arm/claim-boundary.md) | ABB IRB 4600 Webots graph-control demo; no real robot safety, manufacturing, benchmark, vendor-accuracy, or autonomy claim. |
| Aggregate local predictive sensorimotor columns | Cortical-Column World Model | [Cortical-Column World Model](architecture/cortical-column-world-model.md) -> [framework card](architecture/frameworks/cards/cortical-column-world-model-framework.md) -> [eval](labs/evals/cortical-column-world-model/results.md) -> [Maze Graph Memory Bot Webots app](applications/maze-graph-memory-bot/README.md) | Tiny-fixture `contract-pass` plus a Webots maze fixture; no AGI, biological cortex, benchmark, or guaranteed-solving claim. |
| Keep multimodal evidence and outcome trace separated | Multimodal Outcome Stack | [stack guide](architecture/multimodal-outcome-stack.md) -> [review flow](architecture/examples/multimodal-review-flow.md) -> [eval](labs/evals/multimodal-framework-mix/results.md) | Tiny-fixture `contract-pass` for framework-mix separation; no domain performance claim. |
| Coordinate bot-like processing | Graph brain and spine | [brain/spine](architecture/graph-brain-and-spine.md) -> [subgraph capsules](architecture/subgraph-capsules.md) -> [bot example](architecture/examples/bot-execution-graph.md) | Architecture pattern with small application examples. |
| Keep local graph detail routeable | Subgraph capsules | [subgraph capsules](architecture/subgraph-capsules.md) -> [trace contract](architecture/contracts/trace-contract.md) | Architecture contract; capsule cannot commit by itself. |
| Separate graph memory from notes | Graph runtime memory | [graph runtime memory](architecture/graph-runtime-memory.md) -> [memory flow](architecture/memory-outcome-feedback.md) -> [bot examples](applications/bots/README.md) | Outcome-coupled Architecture pattern; notes become graph runtime memory only through declared evidence, commit, and outcome paths. |
| Triage findings by corroboration and outcome | Evidence Graph Triage | [framework card](architecture/frameworks/cards/evidence-graph-triage-framework.md) -> [eval](labs/evals/evidence-graph-triage/results.md) | Tiny-fixture `contract-pass` for evidence-set status and rank-only memory; no detection, triage-quality, or security claim. No shipped application example. |
| Let path context change scoring, thresholds, routes, messages, or readout | Path-conditioned operators | [primer](architecture/path-conditioned-and-path-gated.md) -> [operator guide](architecture/path-conditioned-operators.md) -> [trace contract](architecture/contracts/trace-contract.md) | Core Architecture pattern; no broad performance claim without eval. |
| Let path evidence control model influence or proposal advancement | Path-gated operators | [primer](architecture/path-conditioned-and-path-gated.md) -> [gate guide](architecture/path-gated-operators.md) -> [commit contract](architecture/contracts/commit-contract.md) | Core Architecture pattern; no broad performance claim without eval. |
| Inspect copyable Architecture code | Section-local Architecture reference | [reference code](architecture/reference/python/README.md) -> [reference tests](architecture/reference/python/tests/test_architecture_reference.py) | Optional stdlib-only contracts, not an SDK. |
| Build medical image analysis evidence review | Evidence + multimodal + routing + review frameworks | [Medical Image Analysis application](applications/medical-image-analysis/README.md) -> [framework registry](architecture/frameworks/registry.md) | Application example; reusable concepts remain in Architecture. |

## Common Mixes

| Project shape | Likely CGF mix | First validation question |
| --- | --- | --- |
| Calculation from declared law, energy, loss, or objective | Core primitives + Action-Native Computation + derivative mechanics as needed. | Is the readout produced from declared action, constraints, evolution, residual, and validation instead of hidden scoring? |
| Simple graph optimization | Core primitives + derivative mechanics if an update rule is needed. | Can the action, constraint, evolution, readout, and validation be stated without choosing a solver first? |
| Least-action, geodesic, or variational-path subject | Core primitives + local action / Lagrangian + variation + constraints + Stationary Path + residual. | Is the path stationary under declared admissible changes, and is it not being overclaimed as a global optimum? |
| Noisy physical law | Core primitives + derivatives + weak form + exterior placement. | Does the weak aggregate check expose failure instead of hiding local errors? |
| Region, surface, or episode-support subject | Core primitives + CellComplexView; add weak form when aggregate laws live on cells and topological rigidity only when protected cycles or regimes can collapse. | Does every higher-order support have declared boundary relations and validation? |
| Multi-view catalog, inventory, or knowledge state | Core primitives + sheaf consistency + gauge transport when views use different frames. | Do overlapping views restrict to comparable support before being merged? |
| Dynamical regime or attractor warning | Core primitives + Attractor Diagnostics; add stochastic transition, metric placement, or topological rigidity only when the regime evidence requires them. | Is recurrence, basin, trap, or escape evidence visible without treating the diagnostic as a solver? |
| Belief-state or risk system | Core primitives + stochastic transition + information geometry. | Are uncertainty and information gain declared as fields, not hidden scoring logic? |
| Intervention or policy comparison | Core primitives + causal intervention + stochastic transition when outcomes are uncertain. | Is the readout explicitly observational, interventional, or counterfactual? |
| Hierarchical or geometric placement | Core primitives + metric placement; add topological rigidity only when collapse risk matters. | Does geometry affect action, evolution, readout, or validation rather than display only? |
| Topology-sensitive subject | Core primitives + topology guide; use graph topology only unless cells, boundaries, protected cycles, explicit phase degree, named regime diagnostics, or reference-relative collapse risk require more. | Which topology meaning is being used, and what validation detects topology loss? |
| Structure-sensitive encoding | Core primitives + topology guide; consider topological rigidity when an encoder could collapse loops, boundaries, compartments, rare transitions, phase-like structure, or meaningful connectivity. | What arrangement would the encoder lose, and is there an eval before claiming improvement? |
| Regime-preserving trajectory | Core primitives + metric placement + topological rigidity. | What protected structure would make the result invalid if it collapsed? |
| Open energy or flow system | Core primitives + port-Hamiltonian flow + exterior placement when ports touch external conditions. | Are storage, supply, dissipation, and residual visibility all declared? |
| Learned surrogate or differentiable model | Core primitives + derivatives + differentiable backend + operator-learning promotion checks. | Does the learned component preserve residual, uncertainty, and policy-blocking checks? |
| Symmetry or eigenbasis field | Core primitives + basis-mode representation; add differentiable backend when coefficients or operators are tuned, and add topological rigidity only when mode dynamics have protected cycles, phases, regimes, or collapse risk. | Is the graph a graph of samples or a graph of modes, and can readout report reconstruction or truncation error? |
| Large system summarized at multiple scales | Core primitives + renormalization / coarse-graining. | What fine-level source, action, readout, or residual must remain visible at the coarse level? |
| Path-aware verifier or ranker | Core primitives + Architecture path-conditioned and path-gated operators. | Is the path influence visible, gateable, traceable, and still below commit authority? |
| External records become reusable views | Architecture Anchor / Lens / Promise + evidence records + trace contract. | Is lens identity stable enough for replay, and are promised views visibly pending, fulfilled, or failed? |
| Image or video analysis | Architecture Visual Media Encoding + Granular Analysis + feature views + proposer/verifier; add CellComplexView when regions, boundaries, or surfaces need declared support. | Can every region, track, and derived graph view trace back to a source frame and evidence ref? |
| Parent graph with specialist subgraphs | Architecture Hierarchical Execution Cycles + Subgraph Role Registry + proposal/verifier/commit. | Can child cycles propose, defer, or report failure without silently committing final authority? |
| Runtime graph that may need new routes or specialists | Provisional Graph Growth framework + graph runtime memory + replay. | Is the evidence stable rather than a spike, and is durable mutation blocked until promotion and rollback are explicit? |
| Noisy state estimate in an operating system | Architecture Belief State + Bayesian Filtering + trace contract; add information geometry when distribution comparison matters. | Is the belief estimate labeled as evidence with covariance, innovation, or uncertainty instead of truth? |
| Offline consolidation or recall | Architecture Offline Replay / Dream Cycles + Cognitive Map Memory or Engram / Spatial Memory + graph runtime memory. | Are replayed, simulated, recalled, and real observed outcomes kept separate? |
| Trading, predictive maintenance, risk, or anomaly signal review | Core primitives + Signal Review + feature views + Granular Analysis + processor routing + proposer/verifier; add evidence record or human review when needed. | Can the trace show which signal view, processor route, proposal, verifier basis, and abstain/fallback reason supported the decision? |
| Bot, processor, or tool-use system | Core primitives + execution graph + graph brain/spine + graph runtime memory; add path-conditioned or path-gated operators only where path influence matters. | Can the spine route without hiding authority, and can memory update only after committed outcomes? |
| Sensorimotor world-model controller | Core primitives + execution graph + cortical-column world model + sensor ingestion + Predictive Action Graph + graph runtime memory + explicit safety gates. | Can the trace show bounded sensory frames, local predictions, lateral aggregation, selected action, blocked unsafe actions, observed outcome, and prediction-error memory update? |
| Bot or sensorimotor action-memory showcase | Core primitives + execution graph + Predictive Action Graph + path-conditioned scoring + path-gated proposal advancement + graph runtime memory. | Can the trace show bounded sensory evidence, candidate actions, predicted futures, selected action, blocked unsafe actions, observed outcome, and memory update? Start with [applications/DEMO_GUIDE.md](applications/DEMO_GUIDE.md), then [applications/bots/README.md](applications/bots/README.md) and [applications/maze-graph-memory-bot/README.md](applications/maze-graph-memory-bot/README.md). |
| Local specialist graph inside a larger runtime | Core primitives + Architecture execution graph + subgraph capsule. | Does the capsule return evidence or proposals without committing hidden state? |
| Histology-like or multimodal analysis | Core primitives + Multimodal Outcome Stack + typed multimodal graph + Granular Analysis + feature views + processor routing + proposer/verifier + human review when needed. | Can the trace show which evidence refs, lens branches, routes, and proposal nodes supported the selected outcome? |
| Medical image analysis review system | Core primitives + evidence record + typed multimodal graph + Multimodal Outcome Stack + Granular Analysis + processor routing + proposer/verifier + human review. | Are source evidence, processor output, review state, final state, and later labels separated? Start with [applications/medical-image-analysis/walkthrough.md](applications/medical-image-analysis/walkthrough.md). |
| Security or audit evidence system | Core primitives + evidence record + code/security graph or domain graph + proposer/verifier + human review if needed. | Can every finding or claim resolve through bounded evidence paths? |
| Finding triage queue with limited review attention | Core primitives + Evidence Graph Triage + evidence record + proposer/verifier + graph runtime memory; add human review when a person supplies the outcome. | Is status set by corroboration rather than score, and can memory change ordering without changing what the evidence says? Start with [architecture/frameworks/cards/evidence-graph-triage-framework.md](architecture/frameworks/cards/evidence-graph-triage-framework.md). |

## How To Read Claim Strength

| Signal | Meaning |
| --- | --- |
| Substrate card only | Named optional component with a public declaration shape. |
| Research study | Deeper theory, unresolved questions, references, and claim limits. |
| Labs eval present | Runnable code exists for a small stated contract. |
| `contract-pass` | The local eval passed; the claim is limited to that fixture and contract. |
| No Labs result | Do not describe the topic as validated. |
| Architecture bridge | System-operation direction, not a Substrate primitive. |

## Agent Checklist

When an agent uses CGF for a project, it should report:

```text
1. Starting point used.
2. Complete 9-core Substrate declaration status.
3. Derivative mechanics selected or explicitly skipped.
4. Extensions selected, with required / optional / wrong reasoning.
5. Composition pattern used, if any.
6. Research links checked.
7. Labs eval links checked and exact claim boundary.
8. Architecture patterns selected or explicitly skipped.
9. Architecture framework cards selected or explicitly skipped.
10. Execution graph, brain/spine, subgraph capsule, and graph runtime memory choices when Architecture is used.
11. Granular Analysis or Multimodal Outcome Stack selected, composed, or explicitly skipped when one case has many views or evidence surfaces.
12. Basis-mode representation selected or skipped when symmetry, modes, or selection rules appear.
13. Stationary Path selected or skipped when stationary action, least action,
    geodesic, variational path, or residual-based stationarity appears.
14. CellComplexView selected or skipped when cells, boundaries, regions,
    surfaces, or episode support appear.
15. Attractor Diagnostics selected or skipped when recurrence, basin, regime,
    trap, or escape-warning language appears.
16. Anchor / Lens / Promise selected or skipped when external records become
    reusable graph views.
17. Visual Media Encoding selected or skipped when image or video evidence
    becomes graph evidence.
18. Hierarchical Execution Cycles and Subgraph Role Registry selected or
    skipped when parent graphs delegate to specialist cycles.
19. Belief State and Bayesian Filtering selected or skipped when noisy hidden
    state is estimated.
20. Offline Replay / Dream, Cognitive Map, and Engram / Spatial Memory selected
    or skipped when recall, consolidation, spatial maps, or simulated replay
    appear.
21. Predictive Action Graph selected or skipped when action selection compares candidate futures.
22. Cortical-Column World Model selected or skipped when local sensorimotor predictive subgraphs drive proposals.
23. Path-conditioned or path-gated use selected, composed, or explicitly skipped.
24. Remaining gaps before implementation.
```

This report is the traversal record. It prevents hidden assumptions and makes
the chosen CGF mix reviewable.

Use [templates/project-intake.md](templates/project-intake.md) as the copyable
record for that report.
