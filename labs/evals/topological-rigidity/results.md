# Topological Rigidity Results

Status: `contract-pass`

Eval layer: `isolated`

Reviewed command:

```powershell
python -m unittest discover -s labs/evals/topological-rigidity -p "test_*.py"
```

Reviewed result:

```text
Ran 8 tests
OK
```

The passing checks cover unit-carrier validation, Gram-area and normalized
non-collinearity separation, reference-relative area and angular retention,
rescaling consistency, signed and multiple sampled $U(1)$ phase degree,
explicit non-invariant labeling of a closed-area cycle score, collapse-risk
composition, and evidence-only reporting.

Claim boundary: this result covers tiny deterministic geometry fixtures only.
It does not claim persistent homology, learned topology preservation, broad
empirical performance, physical winding, localized-carrier existence, soliton
stability, or validation of any microscopic physical theory.
