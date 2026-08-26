# Causal Intervention Results

Status: `contract-pass`

Reviewed command:

```powershell
python -m unittest discover -s labs/evals/causal-intervention -p "test_*.py"
```

Reviewed result:

```text
Ran 5 tests
OK
```

Claim boundary: this result covers explicit intervention records and scoped
attribution on tiny fixtures only. It does not claim causal discovery.
