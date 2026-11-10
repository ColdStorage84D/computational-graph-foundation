# Sheaf Consistency Results

Status: `contract-pass`

Eval layer: `isolated`

Reviewed date: 2026-11-10

Reviewed command:

```powershell
python -m unittest discover -s labs/evals/sheaf-consistency -p "test_*.py"
```

Reviewed result:

```text
Ran 12 tests
OK
```

## Observed Values

| Fixture | Dimension of global sections |
| --- | --- |
| Plain cycle, two-dimensional stalks | 2 |
| Plain cycle, one-dimensional stalks | 1 |
| Twisted cycle, one-dimensional stalks | 0 |
| Two views sharing one of two coordinates | 3 |

On the twisted cycle the all-ones assignment has consistency energy 4, carried
entirely by the twisted edge. Diffusion from (0, 3, 6) on the plain cycle
converges to (3, 3, 3).

Claim boundary: sheaves with three nodes, stalks of dimension one or two, and
restriction maps supplied by the fixture. The result covers the coboundary,
global sections, the local-versus-global obstruction, and diffusion on those
fixtures. It does not cover learned restriction maps, higher cohomology, or a
production view system.
