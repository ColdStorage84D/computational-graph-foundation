# Signal Review Eval

Status: `contract-pass`

This eval tests the CGF-local Signal Review contract:

```text
signals -> feature views -> route-specific processors
  -> proposals -> verifier / review / abstain -> traceable signal decision
```

The fixture is synthetic and domain-neutral. It is not trading data,
maintenance data, fraud data, production telemetry, or anomaly benchmark data.

## Owning Docs

- Framework card:
  [signal-review-framework.md](../../../architecture/frameworks/cards/signal-review-framework.md).
- Selection guide:
  [selection-guide.md](../../../architecture/frameworks/selection-guide.md).
- Granular Analysis:
  [granular-analysis.md](../../../architecture/granular-analysis.md).

## Run

```powershell
python -m unittest discover -s labs/evals/signal-review -p "test_*.py"
```

## Claim Boundary

Passing this eval supports only `contract-pass` for the tiny CGF-local fixture:

- raw signal values do not become authority;
- one signal creates multiple feature views;
- route-specific processors produce competing proposals;
- verifier behavior can review, abstain, or select fallback;
- rejected alternatives remain in trace;
- weak signal support does not auto-commit;
- future labels and outcome fields do not enter lens outputs.

It does not support financial advice, market prediction, production
reliability, anomaly-detection performance, maintenance outcome improvement,
or fraud-detection performance.
