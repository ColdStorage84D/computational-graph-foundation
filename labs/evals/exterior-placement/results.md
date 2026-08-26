# Exterior Placement Results

Status: `contract-pass`

Reviewed command:

```powershell
python -m unittest discover -s labs/evals/exterior-placement -p "test_*.py"
```

Reviewed result:

```text
Ran 5 tests
OK
```

Claim boundary: this result covers tiny exterior contact fixtures only. It does
not claim a general boundary-condition or external-environment solver.
