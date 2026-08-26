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

Every `results.md` record must contain an H1 title, a direct
`Status: <label>` declaration, the reviewed command or date, the observed
result, and an explicit claim boundary.

## Current Evals

- [action-native-computation/README.md](action-native-computation/README.md)
- [gauge-transport/README.md](gauge-transport/README.md)
- [cell-complex-view/README.md](cell-complex-view/README.md)
- [exterior-placement/README.md](exterior-placement/README.md)
- [weak-form/README.md](weak-form/README.md)
- [sheaf-consistency/README.md](sheaf-consistency/README.md)
- [stochastic-transition/README.md](stochastic-transition/README.md)
- [information-geometry/README.md](information-geometry/README.md)
- [bayesian-filtering/README.md](bayesian-filtering/README.md)
- [causal-intervention/README.md](causal-intervention/README.md)
- [port-hamiltonian-flow/README.md](port-hamiltonian-flow/README.md)
- [topological-rigidity/README.md](topological-rigidity/README.md)
- [basis-mode-representation/README.md](basis-mode-representation/README.md)
- [hyperbolic-placement/README.md](hyperbolic-placement/README.md)
- [renormalization-coarse-graining/README.md](renormalization-coarse-graining/README.md)
- [operator-learning/README.md](operator-learning/README.md)
- [granular-analysis/README.md](granular-analysis/README.md)
- [multimodal-framework-mix/README.md](multimodal-framework-mix/README.md)
- [signal-review/README.md](signal-review/README.md)
- [cortical-column-world-model/README.md](cortical-column-world-model/README.md)
- [anchor-lens-promise/README.md](anchor-lens-promise/README.md)
- [visual-media-encoding/README.md](visual-media-encoding/README.md)
- [hierarchical-cycles/README.md](hierarchical-cycles/README.md)
- [provisional-graph-growth/README.md](provisional-graph-growth/README.md)
- [evidence-graph-triage/README.md](evidence-graph-triage/README.md)

## Run

Run one eval:

```powershell
python -m unittest discover -s labs/evals/gauge-transport -p "test_*.py"
```

Run all evals from the repository root:

```powershell
Get-ChildItem labs/evals -Directory |
  ForEach-Object { python -m unittest discover -s $_.FullName -p "test_*.py" }
```
