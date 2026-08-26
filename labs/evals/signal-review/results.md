# Signal Review Results

Status: `contract-pass`

## Reviewed Command

```powershell
python -m unittest discover -s labs/evals/signal-review -p "test_*.py"
```

## Result

```text
Ran 7 tests
OK
```

## Claim Boundary

This result supports only the CGF-local Signal Review contract on a tiny
synthetic fixture:

- raw signal values do not become authority;
- one signal creates multiple feature views;
- route-specific processors create competing proposals;
- review, abstain, and fallback behavior are visible;
- rejected alternatives remain in trace;
- weak signal support does not auto-commit;
- future labels and outcome fields are excluded from lens outputs.

## Not Supported

This result does not support financial advice, market prediction, production
reliability, anomaly-detection performance, maintenance outcome improvement,
fraud-detection performance, or broad domain generalization.
