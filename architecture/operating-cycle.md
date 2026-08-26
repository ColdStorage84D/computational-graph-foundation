# Operating Cycle

## Definition

The operating cycle is the repeatable Architecture loop that moves a CGF system
from event to decision to outcome-backed learning.

## Cycle Shape

```text
encode -> propose -> verify -> commit -> execute -> observe -> resolve
  -> consolidate
```

## Phases

| Phase | Responsibility | Output |
| --- | --- | --- |
| Encode | Turn an event into a typed runtime view. | Graph/path view. |
| Propose | Generate candidate paths or actions; optionally use path-conditioned or softly path-gated operators. | Proposal records. |
| Verify | Check evidence, path gates, policy, constraints, uncertainty, and shape. | Verification result. |
| Commit | Select accepted action, non-action, review, defer, fallback, or abort. | Commit record. |
| Execute | Run only approved side effects or internal actions. | Execution result. |
| Observe | Record outcome evidence. | Outcome record. |
| Resolve | Attach outcome to eligibility. | Value, inhibition, or uncertainty update. |
| Consolidate | Update projections, summaries, or promoted graph runtime memory when allowed. | Replayable graph runtime memory projection. |

## Rules

- Propose is not commit.
- Path-conditioned proposals are still proposals.
- Soft path gates control influence, not authority.
- Hard path gates can block, defer, review, fallback, or abstain before commit.
- Verify can reject or defer.
- Commit is the only authority boundary.
- Non-action can be a valid committed decision.
- Eligibility is created only from committed paths.
- Outcome resolves eligibility.
- Consolidation must be replayable.

## Validation Questions

```text
1. Which event starts the cycle?
2. Which view is used by proposals?
3. What can propose?
4. Does path context condition any operator?
5. Does a path gate control influence or advancement?
6. What verifies?
7. What can commit?
8. What action or non-action was accepted?
9. What outcome resolved it?
10. What replay projection changed?
```
