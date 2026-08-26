# Granular Analysis Eval

Status: `contract-pass`

This eval tests the CGF-local Granular Analysis contract:

```text
one input -> many lenses -> many proposal nodes -> traceable outcome
```

The fixture is synthetic and histology-like only. It is not clinical data, does
not validate diagnosis, and does not claim medical performance.

## Connections

- Architecture: [granular-analysis.md](../../../architecture/granular-analysis.md).
- Framework card: [granular-analysis-framework.md](../../../architecture/frameworks/cards/granular-analysis-framework.md).
- Reference code: [Architecture reference Python](../../../architecture/reference/python/README.md).
- Result record: [results.md](results.md).

## Run

```powershell
python -m unittest discover -s labs/evals/granular-analysis -p "test_*.py"
```
