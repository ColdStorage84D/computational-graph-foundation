# Renormalization / Coarse-Graining Results

Status: `contract-pass`

Eval layer: `isolated`

Reviewed date: 2026-11-10

Reviewed command:

```powershell
python -m unittest discover -s labs/evals/renormalization-coarse-graining -p "test_*.py"
```

Reviewed result:

```text
Ran 11 tests
OK
```

## Observed Values

| Check | Observed |
| --- | --- |
| Coarse against fine potentials on kept nodes, five-rung ladder | equal to 10 decimal places |
| End-to-end coupling over five rounds, 32-edge disordered chain | equal to 10 decimal places at every round |
| Uniform chain, coupling 4.0 on 16 edges | 2.0, 1.0, 0.5, 0.25 after each round |
| Naive coarse network, three-rung ladder | under 80% of the true coupling |

Claim boundary: linear response of conductance networks with up to 33 nodes.
The result covers exact node elimination, the flow of couplings on a chain, and
the renormalization of sources on those fixtures. It does not cover learned
clustering, approximate coarse-graining, nonlinear systems, or a
renormalization group for any other kind of model.
