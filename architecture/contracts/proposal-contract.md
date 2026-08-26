# Proposal Contract

## Purpose

A proposal records a candidate path, action, ranking, or non-action option.

It is not authority. It must pass verification and commit before it can create
eligibility or side effects.

## Minimum Record

```text
proposal id
source role
candidate path
expected outcome
confidence
uncertainty
risk
cost
evidence refs
policy requirements
action terms
path context refs, when used
path gate requirements, when used
```

## Validation Questions

```text
1. Is the candidate path explicit?
2. Are confidence and uncertainty both visible when relevant?
3. Are evidence refs present?
4. Are policy requirements declared?
5. If path-conditioned, is the path context visible?
6. If path-gated, are gate requirements visible?
7. Can the proposal be rejected without disappearing?
```

## Failure Modes

- A score is treated as authority.
- Uncertainty is missing.
- Evidence is hidden.
- Policy requirements are implicit.
- Path-conditioned influence is not recorded.
- Path-gated requirements are not declared.
- Rejected candidates are lost.

## Boundary

A proposal can guide commit, but it cannot commit itself.
