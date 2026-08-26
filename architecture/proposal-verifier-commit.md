# Proposal, Verifier, And Commit

## Purpose

This pattern separates candidate generation from accepted state change.

It protects a CGF system from treating a high score, confident model output, or
service suggestion as authority.

In an execution graph, proposals can come from surface nodes, operators,
subgraph capsules, or graph runtime memory projections. The commit boundary
still owns accepted action or accepted non-action.

## Roles

| Role | Responsibility |
| --- | --- |
| Proposal | Candidate path, action, ranking, or non-action option. |
| Verifier | Checks shape, evidence, uncertainty, constraints, and policy. |
| Commit | Accepted action or non-action decision. |

## Proposal Requirements

A proposal should expose:

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

## Path-Aware Proposals

A proposal may be path-conditioned, path-gated, or both.

Path-conditioned proposals expose the path context that influenced a score,
threshold, route, rank, message, or readout.

Path-gated proposals expose any gate requirement that must be checked before
the candidate can advance.

Neither form commits itself. The verifier and commit boundary still decide
accepted action or non-action.

## Commit Decisions

Commit may choose:

- accept;
- reject;
- review;
- defer;
- ask;
- fallback;
- abort.

Only accepted committed paths create eligibility. Rejected proposals may remain
as counterfactual trace evidence, but they do not update graph runtime memory.

## Validation Questions

```text
1. Can a proposal be rejected without losing trace evidence?
2. Can policy block a high-scoring proposal?
3. Can a path gate block, defer, review, fallback, or abstain?
4. Can commit choose non-action?
5. Is eligibility created only for committed paths?
6. Are rejected paths barred from causal value updates?
```
