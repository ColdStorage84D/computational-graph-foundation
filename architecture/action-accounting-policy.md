# Action Accounting And Policy Gates

## Purpose

Action accounting makes proposal selection auditable. Policy gates make hard
constraints explicit.

## Distinction

| Mechanism | Meaning |
| --- | --- |
| Action accounting | Soft terms used to compare cost, risk, uncertainty, latency, information gain, memory impact, and task fit. |
| Policy gate | Hard rule that can block or force review regardless of score. |

## Common Action Terms

- task error;
- prediction error;
- uncertainty;
- risk;
- latency;
- control cost;
- constraint penalty;
- complexity;
- memory impact;
- information gain.

## Rules

- Hard constraints are gates, not giant soft costs.
- Soft terms must be visible in the proposal or trace.
- Policy can require review, defer, fallback, or abort.
- Optional evidence fields cannot authorize policy by themselves.
- Explanation should show which terms mattered.

## Validation Questions

```text
1. Which terms were compared?
2. Which policy gates applied?
3. Did any hard gate block commit?
4. Can the selected decision be explained from the ledger?
5. Are optional signals prevented from bypassing policy?
```
