# Signal Review Framework

## Purpose

Use this framework when time-varying or event-like signals should become
reviewable decisions instead of direct authority.

## Reusable Concept

Signal Review turns raw signals, alerts, forecasts, anomalies, or health scores
into traceable proposal sets.

The reusable pattern is:

```text
signals -> feature views -> route-specific processors
  -> proposals -> verifier / review / abstain -> traceable signal decision
```

The framework prevents a raw signal from silently becoming action. A signal can
support a proposal, trigger review, defer to fallback, or produce an abstain
decision when support is weak.

## Uses CGF Pieces

- evidence records, when signals come from external sources;
- feature views;
- Granular Analysis;
- processor routing;
- proposer / verifier / commit;
- path-conditioned and path-gated operators, when path or regime changes
  influence routing or advancement;
- trace and replay;
- human review, when the decision needs qualified acceptance.

## Example Applications

- trading signals;
- predictive maintenance;
- risk alerts;
- anomaly review;
- operational monitoring;
- fraud or abuse signal triage.

## When To Use

- Signals are noisy, delayed, partial, or regime-dependent.
- Several processors or views can interpret the same signal differently.
- A route-specific processor may be valid in one regime and wrong in another.
- Rejected alternatives matter for audit, learning, or later review.
- The system needs review, fallback, or abstain instead of automatic action.

## When Not To Use

- A deterministic rule already produces the only valid output.
- No signal branch can be rejected, reviewed, deferred, or abstained.
- The project does not need traceable alternatives or route state.
- The framework would imply prediction authority without eval support.

## Boundary

Signal Review is not financial advice, market prediction, production
reliability validation, anomaly-detection performance, maintenance outcome
improvement, or fraud-detection proof.

It describes how signal-derived proposals move through Architecture boundaries.
It does not prove that the signal, processor, model, or action is correct.

## Implementation Posture

Future implementations should keep signal source refs, feature view ids,
processor route states, proposal ids, verifier basis, review decisions, and
abstain/fallback reasons visible.

The current direct Labs result is a tiny-fixture `contract-pass`:
[../../../labs/evals/signal-review/results.md](../../../labs/evals/signal-review/results.md).
Use it only as support for the local Signal Review contract, not as a validated
performance claim.
