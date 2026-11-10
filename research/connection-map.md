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

The last column names the eval layer and what the result covers. An isolated
eval shows a concept is implemented as declared. A value-over-baseline eval
also compares it with a simpler baseline and records where it does not help.
Each result record states its own numbers and claim boundary.

## Current Connections

| Topic | Substrate surface | Research support | Labs result | What the result covers |
| --- | --- | --- | --- | --- |
| 9-core primitives | [primitives.md](../substrate/primitives.md) and [spec/00-overview.md](../substrate/spec/00-overview.md) | [substrate-research-map.md](substrate-research-map.md) | None | Stable declaration contract. |
| Primitive implementation bridge | [primitive-implementation.md](../substrate/primitive-implementation.md) | [substrate-research-map.md](substrate-research-map.md) | None | Teaching math and pseudocode. |
| Derivative mechanics | [derivatives/README.md](../substrate/derivatives/README.md) | [derivative-mechanics-study.md](derivative-mechanics-study.md) | None | v0.2 mechanics docs. |
| Action-Native Computation | [action-native-computation.md](../substrate/derivatives/action-native-computation.md) | [derivative-mechanics-study.md](derivative-mechanics-study.md) | [action-native-computation/results.md](../labs/evals/action-native-computation/results.md) | Isolated. Relaxation, constraint satisfaction, and least-action path on small fixtures. |
| Geometric discretization | [exterior placement](../substrate/extensions/cards/exterior-placement.md), [weak form](../substrate/extensions/cards/weak-form.md) | [extension-studies/geometric-discretization.md](extension-studies/geometric-discretization.md) | [exterior-placement/results.md](../labs/evals/exterior-placement/results.md), [weak-form/results.md](../labs/evals/weak-form/results.md) | Isolated. Exterior contact support, and a discrete weak form on a nine-node path: weak and strong residuals, region balance, and Galerkin refinement. |
| CellComplexView | [cell-complex-view.md](../substrate/extensions/cards/cell-complex-view.md) | [extension-studies/cell-complex-view.md](extension-studies/cell-complex-view.md) | [cell-complex-view/results.md](../labs/evals/cell-complex-view/results.md) | Isolated. Cells, boundaries, path lift, and episode lift. |
| Attractor Diagnostics | [attractor-diagnostics.md](../substrate/extensions/cards/attractor-diagnostics.md) | [extension-studies/attractor-diagnostics.md](extension-studies/attractor-diagnostics.md) | None | Research-supported warning and regime evidence. |
| Topology in CGF | [topology-guide.md](../substrate/extensions/topology-guide.md) | [extension-studies/topological-rigidity.md](extension-studies/topological-rigidity.md), [extension-studies/higher-dimensional-topology.md](extension-studies/higher-dimensional-topology.md), and [higher-dimensional-graphs.md](higher-dimensional-graphs.md) | Specific eval depends on selected topology concept. | Guide only. It separates the meanings of topology. |
| Higher-dimensional topology | Extension study only | [extension-studies/higher-dimensional-topology.md](extension-studies/higher-dimensional-topology.md), [higher-dimensional-graphs.md](higher-dimensional-graphs.md) | None | Research-only until narrowed into cards, examples, or evals. |
| Topological rigidity | [topological-rigidity.md](../substrate/extensions/cards/topological-rigidity.md) | [extension-studies/topological-rigidity.md](extension-studies/topological-rigidity.md) | [topological-rigidity/results.md](../labs/evals/topological-rigidity/results.md) | Isolated. Derivative diagnostics defined by CGF. |
| Basis-mode representation | [basis-mode-representation.md](../substrate/extensions/cards/basis-mode-representation.md) | [extension-studies/basis-mode-representation.md](extension-studies/basis-mode-representation.md) | [basis-mode-representation/results.md](../labs/evals/basis-mode-representation/results.md) | Isolated. Mode labels, coefficient placement, selection rules, operator support, readout, and truncation residuals. |
| Metric placement / hyperbolic placement | [metric-placement.md](../substrate/extensions/cards/metric-placement.md) | [extension-studies/hyperbolic-metric-placement.md](extension-studies/hyperbolic-metric-placement.md) | [hyperbolic-placement/results.md](../labs/evals/hyperbolic-placement/results.md) | Value-over-baseline. Tree distortion in the Poincare ball against the flat plane, and a grid where the flat plane wins. |
| Stochastic transition | [stochastic-transition.md](../substrate/extensions/cards/stochastic-transition.md) | [extension-studies/stochastic-transition.md](extension-studies/stochastic-transition.md) | [stochastic-transition/results.md](../labs/evals/stochastic-transition/results.md) | Isolated. Finite-state kernels: push-forward, composition, and risk mass. |
| Information geometry | [information-geometry.md](../substrate/extensions/cards/information-geometry.md) | [extension-studies/information-geometry.md](extension-studies/information-geometry.md) | [information-geometry/results.md](../labs/evals/information-geometry/results.md) | Isolated. Fisher metric, Fisher-Rao distance, divergence, and entropy on small distributions. |
| Gauge transport | [gauge-transport.md](../substrate/extensions/cards/gauge-transport.md) | [extension-studies/gauge-transport.md](extension-studies/gauge-transport.md) | [gauge-transport/results.md](../labs/evals/gauge-transport/results.md) | Value-over-baseline. Flagging real disagreements across rotated frames with and without transport, and with wrong maps. |
| Sheaf consistency | [sheaf-consistency.md](../substrate/extensions/cards/sheaf-consistency.md) | [extension-studies/sheaf-consistency.md](extension-studies/sheaf-consistency.md) | [sheaf-consistency/results.md](../labs/evals/sheaf-consistency/results.md) | Isolated. Cellular sheaf coboundary, global sections, a local-versus-global obstruction, and diffusion. |
| Port-Hamiltonian flow | [port-hamiltonian-flow.md](../substrate/extensions/cards/port-hamiltonian-flow.md) | [extension-studies/port-hamiltonian-flow.md](extension-studies/port-hamiltonian-flow.md) | [port-hamiltonian-flow/results.md](../labs/evals/port-hamiltonian-flow/results.md) | Isolated. Structure checks, exact power balance for linear systems, and interconnection. |
| Causal intervention | [causal-intervention.md](../substrate/extensions/cards/causal-intervention.md) | [extension-studies/causal-intervention.md](extension-studies/causal-intervention.md) | [causal-intervention/results.md](../labs/evals/causal-intervention/results.md) | Isolated. Observation, intervention, backdoor adjustment, and counterfactuals on a confounded structural model. |
| Renormalization / coarse-graining | [renormalization-coarse-graining.md](../substrate/extensions/cards/renormalization-coarse-graining.md) | [extension-studies/renormalization-coarse-graining.md](extension-studies/renormalization-coarse-graining.md) | [renormalization-coarse-graining/results.md](../labs/evals/renormalization-coarse-graining/results.md) | Isolated. Exact node elimination for conductance networks, coupling flow on chains, and source renormalization. |
| Differentiable backend / surrogate promotion | [differentiable-backend.md](../substrate/extensions/cards/differentiable-backend.md) | [application-class-studies.md](application-class-studies.md) | [surrogate-promotion/results.md](../labs/evals/surrogate-promotion/results.md) | Isolated. Promotion gate for a learned surrogate. |

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

| Topic | Architecture surface | Research support | Labs result | What the result covers |
| --- | --- | --- | --- | --- |
| Granular Analysis | [granular-analysis.md](../architecture/granular-analysis.md) and [framework card](../architecture/frameworks/cards/granular-analysis-framework.md) | [research-program.md](research-program.md) | [granular-analysis/results.md](../labs/evals/granular-analysis/results.md) | Value-over-baseline. One lens against three, with independent and with shared blind spots. |
| Anchor / Lens / Promise | [anchor-lens-promise.md](../architecture/anchor-lens-promise.md) | [research-program.md](research-program.md) | [anchor-lens-promise/results.md](../labs/evals/anchor-lens-promise/results.md) | Isolated. Stable lens identity and promise status. |
| Visual Media Encoding | [visual-media-encoding.md](../architecture/visual-media-encoding.md) | [research-program.md](research-program.md) | [visual-media-encoding/results.md](../labs/evals/visual-media-encoding/results.md) | Isolated. Source, frame, region, track, and graph-view evidence records. |
| Hierarchical execution cycles | [hierarchical-execution-cycles.md](../architecture/hierarchical-execution-cycles.md) | [research-program.md](research-program.md) | [hierarchical-cycles/results.md](../labs/evals/hierarchical-cycles/results.md) | Isolated. Child budgets, bounded responses, deferrals, and authority separation. |
| Local-Voting World Model | [local-voting-world-model.md](../architecture/local-voting-world-model.md) and [framework card](../architecture/frameworks/cards/local-voting-world-model-framework.md) | [research-program.md](research-program.md) | [local-voting-world-model/results.md](../labs/evals/local-voting-world-model/results.md) | Isolated. Feature-location memory, lateral voting, rejected alternatives, and next-feature prediction. |
| Bayesian filtering / state estimation | [bayesian-filtering-state-estimation.md](../architecture/bayesian-filtering-state-estimation.md) | [research-program.md](research-program.md) | [bayesian-filtering/results.md](../labs/evals/bayesian-filtering/results.md) | Value-over-baseline. Scalar filter against raw measurement and moving average, with a matched and with a wrong motion model. |
| Provisional Graph Growth | [provisional-graph-growth.md](../architecture/provisional-graph-growth.md) | [research-program.md](research-program.md) | [provisional-graph-growth/results.md](../labs/evals/provisional-graph-growth/results.md) | Isolated. Provisional capsules, bounded candidate variants, stability guards, promotion gates, and rollback. |
| Multimodal Outcome Stack | [multimodal-outcome-stack.md](../architecture/multimodal-outcome-stack.md), [review flow](../architecture/examples/multimodal-review-flow.md), and framework cards | [research-program.md](research-program.md) and [application-class-studies.md](application-class-studies.md) | [multimodal-framework-mix/results.md](../labs/evals/multimodal-framework-mix/results.md) | Integration. Evidence, typed graph, view, route, proposal, review, and trace separation. |
| Signal Review | [signal-review-framework.md](../architecture/frameworks/cards/signal-review-framework.md) and [selection guide](../architecture/frameworks/selection-guide.md) | [research-program.md](research-program.md) | [signal-review/results.md](../labs/evals/signal-review/results.md) | Isolated. Signal views, route-specific proposals, review, abstain, fallback, and trace. |
| Evidence Graph Triage | [evidence-graph-triage-framework.md](../architecture/frameworks/cards/evidence-graph-triage-framework.md), [graph-runtime-memory.md](../architecture/graph-runtime-memory.md), and [memory-outcome-feedback.md](../architecture/memory-outcome-feedback.md) | [research-program.md](research-program.md) | [evidence-graph-triage/results.md](../labs/evals/evidence-graph-triage/results.md) | Value-over-baseline. Evidence-set status and rank-only memory; corroboration against score ranking and record counting, with independent and with correlated sources. |
| Path-conditioned and path-gated operators | [path-conditioned-and-path-gated.md](../architecture/path-conditioned-and-path-gated.md), [path-gated-operators.md](../architecture/path-gated-operators.md), and [path-conditioned-operators.md](../architecture/path-conditioned-operators.md) | [research-program.md](research-program.md) | [path-gated-operators/results.md](../labs/evals/path-gated-operators/results.md) | Value-over-baseline. Path gate and path conditioning against score-only commit, with informative and with uninformative paths. |
