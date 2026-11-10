# Labs Evals

This folder contains CGF-local runnable evals.

Research pages can link to these results, but the result claim lives here.
Every eval is self-contained, uses Python stdlib, and avoids package or SDK
scaffolding.

For the cross-layer map from Substrate cards to Research studies and Labs
results, see [../../research/connection-map.md](../../research/connection-map.md).

For how to design isolated, integration, value-over-baseline, and
recipe-grounded evals, see [evaluation-methodology.md](evaluation-methodology.md).

## Status Labels

| Label | Meaning |
| --- | --- |
| `pending-cgf-eval` | No CGF-local runnable eval exists yet. |
| `cgf-eval-present` | Eval code exists, but no reviewed result has been recorded. |
| `contract-pass` | Eval code exists, tests pass, and a reviewed result is recorded. |
| `contract-fail` | Eval code exists and fails its stated contract. |
| `mixed` | Eval gives partial support or exposes unresolved gaps. |

## Eval Layers

A status says the contract passed. The layer says what kind of contract it was.

| Layer | What it shows | What it needs |
| --- | --- | --- |
| `isolated` | One concept is implemented as declared, on small fixtures. | `eval.py` and its tests. |
| `integration` | A small mix of concepts works together. | `eval.py` and its tests. |
| `value-over-baseline` | The concept beats a simpler baseline on a named failure mode, under stated assumptions. | `comparison.py` with a seeded generator, `test_comparison.py` with pass thresholds, and a result record that names the baseline and has a `Where It Does Not Help` section. |
| `recipe-grounded` | A real application failure mode, rewritten as a self-contained fixture and compared with a baseline. | Everything a value-over-baseline eval needs, plus a stated source for the failure mode. |

No eval is recipe-grounded yet.

Every `results.md` record must contain an H1 title, a direct
`Status: <label>` declaration, an `Eval layer: <layer>` declaration, the
reviewed command or date, the observed result, and an explicit claim boundary.
`scripts/check_public_base.py` enforces this.

Where an eval has both `test_eval.py` and `test_model.py`, the first tests the
record discipline and the second tests the mathematical object the eval is
named after.

## Current Evals

| Eval | Layer |
| --- | --- |
| [action-native-computation/README.md](action-native-computation/README.md) | isolated |
| [anchor-lens-promise/README.md](anchor-lens-promise/README.md) | isolated |
| [basis-mode-representation/README.md](basis-mode-representation/README.md) | isolated |
| [bayesian-filtering/README.md](bayesian-filtering/README.md) | value-over-baseline |
| [causal-intervention/README.md](causal-intervention/README.md) | isolated |
| [cell-complex-view/README.md](cell-complex-view/README.md) | isolated |
| [evidence-graph-triage/README.md](evidence-graph-triage/README.md) | value-over-baseline |
| [exterior-placement/README.md](exterior-placement/README.md) | isolated |
| [gauge-transport/README.md](gauge-transport/README.md) | value-over-baseline |
| [granular-analysis/README.md](granular-analysis/README.md) | value-over-baseline |
| [hierarchical-cycles/README.md](hierarchical-cycles/README.md) | isolated |
| [hyperbolic-placement/README.md](hyperbolic-placement/README.md) | value-over-baseline |
| [information-geometry/README.md](information-geometry/README.md) | isolated |
| [local-voting-world-model/README.md](local-voting-world-model/README.md) | isolated |
| [multimodal-framework-mix/README.md](multimodal-framework-mix/README.md) | integration |
| [path-gated-operators/README.md](path-gated-operators/README.md) | value-over-baseline |
| [port-hamiltonian-flow/README.md](port-hamiltonian-flow/README.md) | isolated |
| [provisional-graph-growth/README.md](provisional-graph-growth/README.md) | isolated |
| [renormalization-coarse-graining/README.md](renormalization-coarse-graining/README.md) | isolated |
| [sheaf-consistency/README.md](sheaf-consistency/README.md) | isolated |
| [signal-review/README.md](signal-review/README.md) | isolated |
| [stochastic-transition/README.md](stochastic-transition/README.md) | isolated |
| [surrogate-promotion/README.md](surrogate-promotion/README.md) | isolated |
| [topological-rigidity/README.md](topological-rigidity/README.md) | isolated |
| [visual-media-encoding/README.md](visual-media-encoding/README.md) | isolated |
| [weak-form/README.md](weak-form/README.md) | isolated |

## Run

Run one eval:

```powershell
python -m unittest discover -s labs/evals/gauge-transport -p "test_*.py"
```

Print the numbers of a value-over-baseline eval:

```powershell
python labs/evals/gauge-transport/comparison.py
```

Run all evals from the repository root:

```powershell
Get-ChildItem labs/evals -Directory |
  ForEach-Object { python -m unittest discover -s $_.FullName -p "test_*.py" }
```
