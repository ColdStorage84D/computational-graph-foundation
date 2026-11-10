# Weak Form Results

Status: `contract-pass`

Eval layer: `isolated`

Reviewed date: 2026-11-10

Reviewed command:

```powershell
python -m unittest discover -s labs/evals/weak-form -p "test_*.py"
```

Reviewed result:

```text
Ran 12 tests
OK
```

## Observed Values

| Check | Observed |
| --- | --- |
| Tested residual against the summed pointwise residual, five random test functions | equal to 10 decimal places |
| Tested residual of the three-hat Galerkin solution, each hat | below 1e-9 |
| Largest pointwise residual of the same solution | above 0.5 |
| Largest pointwise residual with the full nodal space | below 1e-9 |

Claim boundary: a symmetric positive-definite law on a nine-node path with a
piecewise-linear test space. The result covers the weak and strong forms of
that law and how they relate. It does not cover a finite-element library, mesh
geometry, convergence rates, or any physical accuracy.
