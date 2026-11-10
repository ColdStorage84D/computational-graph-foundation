# Granular Analysis Eval

Status: `contract-pass`

This eval tests the CGF-local Granular Analysis contract:

```text
one input -> many lenses -> many proposal nodes -> traceable outcome
```

The contract fixture is one synthetic, histology-like sample.

## Comparison

`comparison.py` runs the reference engine on synthetic two-outcome cases. A
lens looking into a blind spot reports confident support for the wrong
outcome. The baseline gives the engine one lens. The variants give it three,
with a proposer per pair of lenses or one proposer reading all three. A second
regime makes all three lenses blind together.

## Connections

- Architecture: [granular-analysis.md](../../../architecture/granular-analysis.md).
- Framework card: [granular-analysis-framework.md](../../../architecture/frameworks/cards/granular-analysis-framework.md).
- Reference code: [Architecture reference Python](../../../architecture/reference/python/README.md).
- Result record: [results.md](results.md).

## Run

```powershell
python -m unittest discover -s labs/evals/granular-analysis -p "test_*.py"
python labs/evals/granular-analysis/comparison.py
```

## Files

- [eval.py](eval.py): the implementation under test.
- [test_eval.py](test_eval.py): contract tests.
- [comparison.py](comparison.py): seeded comparison against the baseline.
- [test_comparison.py](test_comparison.py): thresholds for the comparison.
