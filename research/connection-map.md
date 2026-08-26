# Substrate Research Labs Connection Map

## Purpose

This page connects the three CGF layers that carry technical claims:

- Substrate defines the public declaration surface.
- Research holds deeper theory, reference needs, and claim boundaries.
- Labs holds runnable evals and reviewed result records.

Use this page when deciding whether a Substrate card is only a named extension,
has deeper research support, or has a CGF-local eval result.

For the full project traversal path, start with
[../FOUNDATION_TRAVERSAL.md](../FOUNDATION_TRAVERSAL.md).

## Connection Rule

A Substrate page can name a concept before it has an eval, but it must not make
a pass claim without a Labs result.

Research can explain theory and claim boundaries. Labs owns runnable checks and
result labels. Substrate should stay concise and point outward when the reader
needs deeper support.

## Current Connections

| Topic | Substrate surface | Research support | Labs result | Claim boundary |
| --- | --- | --- | --- | --- |
| 9-core primitives | [primitives.md](../substrate/primitives.md) and [spec/00-overview.md](../substrate/spec/00-overview.md) | [substrate-research-map.md](substrate-research-map.md) | None | Stable declaration contract, not a solver claim. |
| Primitive implementation bridge | [primitive-implementation.md](../substrate/primitive-implementation.md) | [substrate-research-map.md](substrate-research-map.md) | None | Teaching math and pseudocode only. |
| Derivative mechanics | [derivatives/README.md](../substrate/derivatives/README.md) | [derivative-mechanics-study.md](derivative-mechanics-study.md) | None | v0.2 mechanics docs, not full numerical method validation. |
| Action-Native Computation | [action-native-computation.md](../substrate/derivatives/action-native-computation.md) | [derivative-mechanics-study.md](derivative-mechanics-study.md) | [action-native-computation/results.md](../labs/evals/action-native-computation/results.md) | Tiny-fixture `contract-pass` for relaxation, constraint satisfaction, and least-action path; no solver, physics, broad optimization, or analog-computing performance claim. |
| Geometric discretization | [exterior placement](../substrate/extensions/cards/exterior-placement.md), [weak form](../substrate/extensions/cards/weak-form.md) | [extension-studies/geometric-discretization.md](extension-studies/geometric-discretization.md) | [exterior-placement/results.md](../labs/evals/exterior-placement/results.md), [weak-form/results.md](../labs/evals/weak-form/results.md) | Tiny-fixture checks exist for exterior contact support and weak aggregate residuals; broader discretization claims still need reference and eval passes. |
| CellComplexView | [cell-complex-view.md](../substrate/extensions/cards/cell-complex-view.md) | [extension-studies/cell-complex-view.md](extension-studies/cell-complex-view.md) | [cell-complex-view/results.md](../labs/evals/cell-complex-view/results.md) | Tiny-fixture `contract-pass` for cells, boundaries, path lift, and episode lift. |
| Attractor Diagnostics | [attractor-diagnostics.md](../substrate/extensions/cards/attractor-diagnostics.md) | [extension-studies/attractor-diagnostics.md](extension-studies/attractor-diagnostics.md) | None | Research-supported warning and regime evidence only; no direct Labs eval yet. |
| Topology in CGF | [topology-guide.md](../substrate/extensions/topology-guide.md) | [extension-studies/topological-rigidity.md](extension-studies/topological-rigidity.md), [extension-studies/higher-dimensional-topology.md](extension-studies/higher-dimensional-topology.md), and [higher-dimensional-graphs.md](higher-dimensional-graphs.md) | Specific eval depends on selected topology concept. | Guide only; it separates topology meanings and does not create a new pass claim. |
| Higher-dimensional topology | Extension study only | [extension-studies/higher-dimensional-topology.md](extension-studies/higher-dimensional-topology.md), [higher-dimensional-graphs.md](higher-dimensional-graphs.md) | None | Research-only until narrowed into cards, examples, or evals. |
| Topological rigidity | [topological-rigidity.md](../substrate/extensions/cards/topological-rigidity.md) | [extension-studies/topological-rigidity.md](extension-studies/topological-rigidity.md) | [topological-rigidity/results.md](../labs/evals/topological-rigidity/results.md) | Independently defined CGF extension; tiny-fixture `contract-pass` for derivative diagnostics only, with no physical-theory validation claim. |
| Basis-mode representation | [basis-mode-representation.md](../substrate/extensions/cards/basis-mode-representation.md) | [extension-studies/basis-mode-representation.md](extension-studies/basis-mode-representation.md) | [basis-mode-representation/results.md](../labs/evals/basis-mode-representation/results.md) | Tiny-fixture `contract-pass` for mode labels, coefficient placement, selection rules, operator support, readout, and truncation residuals. |
| Metric placement / hyperbolic placement | [metric-placement.md](../substrate/extensions/cards/metric-placement.md) | [extension-studies/hyperbolic-metric-placement.md](extension-studies/hyperbolic-metric-placement.md) | [hyperbolic-placement/results.md](../labs/evals/hyperbolic-placement/results.md) | Tiny-fixture `contract-pass` for placement validity and hierarchy-aware distance. |
| Stochastic transition | [stochastic-transition.md](../substrate/extensions/cards/stochastic-transition.md) | [extension-studies/stochastic-transition.md](extension-studies/stochastic-transition.md) | [stochastic-transition/results.md](../labs/evals/stochastic-transition/results.md) | Tiny-fixture `contract-pass` for finite-state transition checks. |
| Information geometry | [information-geometry.md](../substrate/extensions/cards/information-geometry.md) | [extension-studies/information-geometry.md](extension-studies/information-geometry.md) | [information-geometry/results.md](../labs/evals/information-geometry/results.md) | Tiny-fixture `contract-pass` for discrete belief metrics. |
| Gauge transport | [gauge-transport.md](../substrate/extensions/cards/gauge-transport.md) | [extension-studies/gauge-transport.md](extension-studies/gauge-transport.md) | [gauge-transport/results.md](../labs/evals/gauge-transport/results.md) | Tiny-fixture `contract-pass` for frame-aware transport checks. |
| Sheaf consistency | [sheaf-consistency.md](../substrate/extensions/cards/sheaf-consistency.md) | [extension-studies/sheaf-consistency.md](extension-studies/sheaf-consistency.md) | [sheaf-consistency/results.md](../labs/evals/sheaf-consistency/results.md) | Tiny-fixture `contract-pass` for restriction, gluing, and obstruction checks. |
| Port-Hamiltonian flow | [port-hamiltonian-flow.md](../substrate/extensions/cards/port-hamiltonian-flow.md) | [extension-studies/port-hamiltonian-flow.md](extension-studies/port-hamiltonian-flow.md) | [port-hamiltonian-flow/results.md](../labs/evals/port-hamiltonian-flow/results.md) | Tiny-fixture `contract-pass` for storage, ports, dissipation, and residual visibility. |
| Causal intervention | [causal-intervention.md](../substrate/extensions/cards/causal-intervention.md) | [extension-studies/causal-intervention.md](extension-studies/causal-intervention.md) | [causal-intervention/results.md](../labs/evals/causal-intervention/results.md) | Tiny-fixture `contract-pass` for observation, intervention, counterfactual, and attribution separation. |
| Renormalization / coarse-graining | [renormalization-coarse-graining.md](../substrate/extensions/cards/renormalization-coarse-graining.md) | [extension-studies/renormalization-coarse-graining.md](extension-studies/renormalization-coarse-graining.md) | [renormalization-coarse-graining/results.md](../labs/evals/renormalization-coarse-graining/results.md) | Tiny-fixture `contract-pass` for fine/coarse source and residual visibility. |
| Differentiable backend / operator learning | [differentiable-backend.md](../substrate/extensions/cards/differentiable-backend.md) | [application-class-studies.md](application-class-studies.md) | [operator-learning/results.md](../labs/evals/operator-learning/results.md) | Tiny-fixture `contract-pass` for learned-surrogate promotion discipline. |

## Missing Eval Signals

The current Substrate extension areas without CGF-local eval results are:

- higher-dimensional topology as a standalone extension direction;
- Attractor Diagnostics;
- derivative mechanics as a whole.

These topics can remain in Substrate or Research with draft or research status,
but they should not be described as validated until Labs contains a runnable
eval and a reviewed result.

## Architecture Connections

Architecture concepts are not Substrate primitives, but they can still have
Labs evals and claim boundaries.

| Topic | Architecture surface | Research support | Labs result | Claim boundary |
| --- | --- | --- | --- | --- |
| Granular Analysis | [granular-analysis.md](../architecture/granular-analysis.md) and [framework card](../architecture/frameworks/cards/granular-analysis-framework.md) | [research-program.md](research-program.md) | [granular-analysis/results.md](../labs/evals/granular-analysis/results.md) | Tiny-fixture `contract-pass` for many lenses, many proposers, one traceable outcome; no medical or domain performance claim. |
| Anchor / Lens / Promise | [anchor-lens-promise.md](../architecture/anchor-lens-promise.md) | [research-program.md](research-program.md) | [anchor-lens-promise/results.md](../labs/evals/anchor-lens-promise/results.md) | Tiny-fixture `contract-pass` for stable lens identity and promise status only. |
| Visual Media Encoding | [visual-media-encoding.md](../architecture/visual-media-encoding.md) | [research-program.md](research-program.md) | [visual-media-encoding/results.md](../labs/evals/visual-media-encoding/results.md) | Tiny-fixture `contract-pass` for source, frame, region, track, and graph-view evidence records; no perception-performance claim. |
| Hierarchical execution cycles | [hierarchical-execution-cycles.md](../architecture/hierarchical-execution-cycles.md) | [research-program.md](research-program.md) | [hierarchical-cycles/results.md](../labs/evals/hierarchical-cycles/results.md) | Tiny-fixture `contract-pass` for child budgets, bounded responses, deferrals, and authority separation. |
| Cortical-Column World Model | [cortical-column-world-model.md](../architecture/cortical-column-world-model.md) and [framework card](../architecture/frameworks/cards/cortical-column-world-model-framework.md) | [research-program.md](research-program.md) | [cortical-column-world-model/results.md](../labs/evals/cortical-column-world-model/results.md) | Tiny-fixture `contract-pass` for feature-location memory, lateral voting, rejected alternatives, and next-feature prediction; no biological, AGI, benchmark, or real-world performance claim. |
| Bayesian filtering / state estimation | [bayesian-filtering-state-estimation.md](../architecture/bayesian-filtering-state-estimation.md) | [research-program.md](research-program.md) | [bayesian-filtering/results.md](../labs/evals/bayesian-filtering/results.md) | Tiny-fixture `contract-pass` for scalar linear-Gaussian prediction, update, and innovation only. |
| Provisional Graph Growth | [provisional-graph-growth.md](../architecture/provisional-graph-growth.md) | [research-program.md](research-program.md) | [provisional-graph-growth/results.md](../labs/evals/provisional-graph-growth/results.md) | Tiny-fixture `contract-pass` for provisional capsules, bounded candidate variants, stability guards, promotion gates, and rollback; no autonomous self-improvement, production safety, or broad learning-performance claim. |
| Multimodal Outcome Stack | [multimodal-outcome-stack.md](../architecture/multimodal-outcome-stack.md), [review flow](../architecture/examples/multimodal-review-flow.md), and framework cards | [research-program.md](research-program.md) and [application-class-studies.md](application-class-studies.md) | [multimodal-framework-mix/results.md](../labs/evals/multimodal-framework-mix/results.md) | Tiny-fixture `contract-pass` for evidence, typed graph, view, route, proposal, review, and trace separation; no domain performance claim. |
| Signal Review | [signal-review-framework.md](../architecture/frameworks/cards/signal-review-framework.md) and [selection guide](../architecture/frameworks/selection-guide.md) | [research-program.md](research-program.md) | [signal-review/results.md](../labs/evals/signal-review/results.md) | Tiny-fixture `contract-pass` for signal views, route-specific proposals, review/abstain/fallback, and trace; no financial, prediction, reliability, anomaly-performance, or maintenance claim. |
| Evidence Graph Triage | [evidence-graph-triage-framework.md](../architecture/frameworks/cards/evidence-graph-triage-framework.md), [graph-runtime-memory.md](../architecture/graph-runtime-memory.md), and [memory-outcome-feedback.md](../architecture/memory-outcome-feedback.md) | [research-program.md](research-program.md) | [evidence-graph-triage/results.md](../labs/evals/evidence-graph-triage/results.md) | Tiny-fixture `contract-pass` for evidence-set status, rank-only memory, and outcomes that never register as success when unresolved; no detection, triage-quality, or security claim. |
