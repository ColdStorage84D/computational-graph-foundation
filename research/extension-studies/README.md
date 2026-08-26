# Extension Studies

Extension studies are deeper research notes for optional Substrate extension
components.

Extension cards stay concise. These studies keep the extra theory, record
shape, operator ideas, validation questions, failure modes, and reference needs
that are too large for cards.

For the public decision path across graph topology, higher-dimensional topology,
topological rigidity, and application graph topology, start with
[../../substrate/extensions/topology-guide.md](../../substrate/extensions/topology-guide.md).

## Rule

An extension study must not make the extension mandatory.

Every study assumes a complete 9-core Substrate subject already exists:

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

The extension is added only when the subject exposes a real modeling failure.

## Current Studies

| Study | Substrate surface | Labs result |
| --- | --- | --- |
| [geometric-discretization.md](geometric-discretization.md) | [exterior placement](../../substrate/extensions/cards/exterior-placement.md), [weak form](../../substrate/extensions/cards/weak-form.md) | [exterior placement](../../labs/evals/exterior-placement/results.md), [weak form](../../labs/evals/weak-form/results.md) |
| [higher-dimensional-topology.md](higher-dimensional-topology.md) | Research-only direction | None yet. |
| [cell-complex-view.md](cell-complex-view.md) | [CellComplexView](../../substrate/extensions/cards/cell-complex-view.md) | [contract-pass](../../labs/evals/cell-complex-view/results.md) |
| [attractor-diagnostics.md](attractor-diagnostics.md) | [Attractor Diagnostics](../../substrate/extensions/cards/attractor-diagnostics.md) | None yet. |
| [basis-mode-representation.md](basis-mode-representation.md) | [basis-mode representation](../../substrate/extensions/cards/basis-mode-representation.md) | [contract-pass](../../labs/evals/basis-mode-representation/results.md) |
| [gauge-transport.md](gauge-transport.md) | [gauge transport](../../substrate/extensions/cards/gauge-transport.md) | [contract-pass](../../labs/evals/gauge-transport/results.md) |
| [information-geometry.md](information-geometry.md) | [information geometry](../../substrate/extensions/cards/information-geometry.md) | [contract-pass](../../labs/evals/information-geometry/results.md) |
| [sheaf-consistency.md](sheaf-consistency.md) | [sheaf consistency](../../substrate/extensions/cards/sheaf-consistency.md) | [contract-pass](../../labs/evals/sheaf-consistency/results.md) |
| [causal-intervention.md](causal-intervention.md) | [causal intervention](../../substrate/extensions/cards/causal-intervention.md) | [contract-pass](../../labs/evals/causal-intervention/results.md) |
| [hyperbolic-metric-placement.md](hyperbolic-metric-placement.md) | [metric placement](../../substrate/extensions/cards/metric-placement.md) | [contract-pass](../../labs/evals/hyperbolic-placement/results.md) |
| [port-hamiltonian-flow.md](port-hamiltonian-flow.md) | [port-Hamiltonian flow](../../substrate/extensions/cards/port-hamiltonian-flow.md) | [contract-pass](../../labs/evals/port-hamiltonian-flow/results.md) |
| [stochastic-transition.md](stochastic-transition.md) | [stochastic transition](../../substrate/extensions/cards/stochastic-transition.md) | [contract-pass](../../labs/evals/stochastic-transition/results.md) |
| [topological-rigidity.md](topological-rigidity.md) | [topological rigidity](../../substrate/extensions/cards/topological-rigidity.md) | [contract-pass](../../labs/evals/topological-rigidity/results.md) |
| [renormalization-coarse-graining.md](renormalization-coarse-graining.md) | [renormalization / coarse-graining](../../substrate/extensions/cards/renormalization-coarse-graining.md) | [contract-pass](../../labs/evals/renormalization-coarse-graining/results.md) |

For the full cross-layer view, see
[../connection-map.md](../connection-map.md).

## Standard Shape

Each study should cover:

- purpose;
- failure mode;
- minimum Substrate addition;
- conceptual records;
- operators or checks;
- relationship to nearby extensions;
- validation questions;
- maturity.

If a note needs system operation, scheduling, durable state, or event handling,
move that part to Architecture.
