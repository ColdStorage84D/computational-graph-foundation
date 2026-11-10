# Causal Intervention Results

Status: `contract-pass`

Eval layer: `isolated`

Reviewed date: 2026-11-10

Reviewed command:

```powershell
python -m unittest discover -s labs/evals/causal-intervention -p "test_*.py"
```

Reviewed result:

```text
Ran 13 tests
OK
```

## Observed Values

Effect of `X` on `Y` set to +0.1:

| Query | Value |
| --- | --- |
| `P(Y=1 | X=1) - P(Y=1 | X=0)` | 0.58 |
| `P(Y=1 | do(X=1)) - P(Y=1 | do(X=0))` | 0.10 |
| Backdoor adjustment over `Z` for `do(X=1)` | 0.60, equal to `P(Y=1 | do(X=1))` |
| `P(Z=1 | X=1)` and `P(Z=1 | do(X=1))` | 0.90 and 0.50 |
| `P(Y=1 had X been 0 | X=1, Y=1)` | 0.881, against 0.50 for `do(X=0)` |

With the effect set to -0.1 the observed contrast is +0.38 while the
interventional contrast is -0.10. With the effect set to 0 the observed
contrast is +0.48.

Claim boundary: the graph and mechanisms are declared by the fixture and
solved by enumeration over a few dozen noise settings. The result covers
intervention semantics on that fixture and the record separation. It does not
cover causal discovery, estimation from samples, or identification when the
graph is unknown.
