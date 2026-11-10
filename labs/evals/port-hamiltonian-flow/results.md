# Port-Hamiltonian Flow Results

Status: `contract-pass`

Eval layer: `isolated`

Reviewed date: 2026-11-10

Reviewed command:

```powershell
python -m unittest discover -s labs/evals/port-hamiltonian-flow -p "test_*.py"
```

Reviewed result:

```text
Ran 11 tests
OK
```

## Observed Values

| Check | Observed |
| --- | --- |
| Energy drift, lossless, 2000 steps | below 1e-10 |
| Worst per-step balance residual, damped | below 1e-12 |
| Worst per-step balance residual, driven | below 1e-12 |
| Total energy drift, two interconnected lossless systems | below 1e-10 |
| Accounting residual when damping is left undeclared | equal to the true dissipation |

Claim boundary: linear systems with quadratic storage and two to four states,
integrated with one scheme. The result covers the structural properties and the
power balance on those fixtures. It does not cover nonlinear storage, a general
simulator, a scheduler, or any physical device.
