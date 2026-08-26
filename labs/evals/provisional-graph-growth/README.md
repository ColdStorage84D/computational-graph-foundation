# Provisional Graph Growth Eval

This eval checks a tiny CGF-local contract for
[Provisional Graph Growth](../../../architecture/provisional-graph-growth.md).

It tests that repeated evidence can create provisional graph structure while
durable graph mutation remains blocked until an explicit promotion gate passes.

## Contract Tested

- repeated observations create a provisional graph capsule;
- one-off or burst evidence is held instead of promoted;
- candidate variants are bounded;
- risky variants are quarantined;
- shadow scoring has no commit authority;
- low-affinity variants can be retired;
- growth patches require evidence and probation status;
- durable graph state cannot change before promotion;
- promotion requires stable temporal support, baseline comparison, held-out
  check, safety check, risk limit, and rollback policy;
- regression after promotion can restore the fallback route.

## Claim Boundary

Status: `contract-pass`.

This eval does not prove autonomous self-improvement, production graph safety,
broad learning performance, or domain usefulness. It only verifies the local
fixture contract.

## Run

```powershell
python -m unittest discover -s labs/evals/provisional-graph-growth -p "test_*.py"
```
