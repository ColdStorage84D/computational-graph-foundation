# Renormalization / Coarse-Graining Results

Status: `contract-pass`

Reviewed command:

```powershell
python -m unittest discover -s labs/evals/renormalization-coarse-graining -p "test_*.py"
```

Reviewed result:

```text
Ran 4 tests
OK
```

Claim boundary: this result covers tiny coarse-graining fixtures only. It does
not claim learned clustering, real data performance, or universal robustness.
