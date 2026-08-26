# Outcome Contract

## Purpose

An outcome records the observed result of a committed path or deliberate
non-action.

Outcomes resolve eligibility into value, inhibition, uncertainty, or no update.

## Minimum Record

```text
outcome id
commit id
observed result
result status
evidence refs
time or order
resolution target
quality or error signal
```

## Validation Questions

```text
1. Which commit does this outcome resolve?
2. Is the result observed, delayed, expired, or unknown?
3. What evidence supports the result?
4. Does the outcome create value, inhibition, or uncertainty?
```

## Failure Modes

- Outcome is attached to an uncommitted proposal.
- Missing outcomes are treated as success.
- Evidence refs are absent.
- Ambiguous outcomes update value as if certain.

## Boundary

Outcome is evidence for update. It should not rewrite the original event or
commit.
