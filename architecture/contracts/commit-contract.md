# Commit Contract

## Purpose

A commit records the decision boundary where a proposal becomes accepted action
or a deliberate non-action.

## Minimum Record

```text
commit id
proposal refs
decision
accepted path or non-action
verification basis
policy basis
path gate basis, when used
path gate decision, when a hard gate is used
action ledger summary
trace id
eligibility rule
```

## Validation Questions

```text
1. Which proposal or proposals were considered?
2. What decision was made?
3. Which policy gates applied?
4. Which path gates applied, if any?
5. Did commit create eligibility?
6. Can rejected proposals remain counterfactual evidence?
```

## Failure Modes

- Side effects happen before commit.
- Hard policy is represented only as a soft score.
- Path gate failure is hidden inside a score.
- Non-action decisions are not recorded.
- Rejected proposals create value updates.

## Boundary

Commit is the authority boundary. It is still not outcome or memory by itself.
