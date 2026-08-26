# Operator Learning Results

Status: `contract-pass`

Reviewed command:

```powershell
python -m unittest discover -s labs/evals/operator-learning -p "test_*.py"
```

Reviewed result:

```text
Ran 5 tests
OK
```

Claim boundary: this result covers a tiny affine surrogate and promotion gate
only. It does not claim neural-operator performance or a required backend.
