# Action-Native Computation Results

Status: `contract-pass`

Eval layer: `isolated`

Reviewed command:

```powershell
python -m unittest discover -s labs/evals/action-native-computation -p "test_*.py"
```

Reviewed result:

```text
Ran 14 tests
OK
```

Claim boundary: this result covers only tiny local fixtures for relaxation,
constraint satisfaction, and least-action path. It proves that the CGF contract
can require declared action or law, visible constraints, residual/error,
validation, and readout before accepting a result. It does not prove physics
accuracy, solver quality, global optimization, broad mathematical capability,
or analog-computing performance.
