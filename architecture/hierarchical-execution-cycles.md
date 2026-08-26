# Hierarchical Execution Cycles

Hierarchical Execution Cycles let a parent operating cycle ask bounded child
cycles for evidence, proposals, uncertainty, or deferral without giving those
children unbounded authority.

## Definition

```text
parent cycle
  -> child cycle requests with budgets
  -> child responses
  -> parent proposal set
  -> parent verification and commit
```

Child cycles can be specialists. They may inspect local evidence, run a local
view, or return a candidate, but parent authority remains explicit unless a
scope says otherwise.

## Response Types

```text
evidence
proposal
uncertainty
deferred
failed
no_bid
```

## Minimum Record

```text
parent_cycle_id
child_cycle_id
budget
request_kind
response_status
evidence_refs
proposal_refs
uncertainty
failure_reason
trace_refs
```

## When To Use

- A system has specialists with different budgets or cadences.
- Some work may be deferred.
- Parent and child authority must remain separate.
- Local graph detail should be routeable without becoming global truth.

## Boundary

Child cycles produce bounded evidence or candidates. They do not erase parent
trace, skip verification, or silently commit external action.

## Claim Boundary

CGF has a tiny local eval for budgeted child responses and authority separation.
It does not claim a scheduler or distributed execution runtime.
