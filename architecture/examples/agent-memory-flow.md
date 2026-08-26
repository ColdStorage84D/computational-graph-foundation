# Agent Memory Flow

## Purpose

This example shows agent memory as outcome-coupled Architecture state, not as
evidence or truth by itself.

## Runtime Shape

```text
evidence refs -> durable note -> committed claim -> self-audit
  -> eligibility -> resolved outcome -> value memory -> reusable template
```

## Architecture Responsibilities

- Notes and claims are separate from source evidence.
- Evidence refs must be resolvable by the adopting project.
- Self-audit creates questions or checks for material claims.
- Eligibility traces track delayed resolution.
- Value memory records calibration after outcome.
- Templates can reuse memory summaries without granting hidden access.

## Safety Rules

- Memory is not evidence.
- Claims are committed beliefs, not truth.
- Unsupported, stale, contradicted, or uncited claims remain visible states.
- Eligibility resolves once.
- Value memory is deterministic calibration, not hidden training.

## Validation Questions

```text
1. Which evidence refs support the claim?
2. What audit questions remain open?
3. Which committed claim created eligibility?
4. What outcome resolved the trace?
5. What value update changed future behavior?
```
