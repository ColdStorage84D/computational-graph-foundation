# Signal / Alert Review Application

This application shows Signal Review as a reusable CGF shape.

It is not a trading system, predictive-maintenance system, fraud system,
monitoring product, financial advice tool, anomaly detector, or production
reliability claim.

## Reusable Framework Mix

Use these Architecture docs:

- [../../architecture/frameworks/cards/signal-review-framework.md](../../architecture/frameworks/cards/signal-review-framework.md)
- [../../architecture/frameworks/cards/feature-view-framework.md](../../architecture/frameworks/cards/feature-view-framework.md)
- [../../architecture/frameworks/cards/granular-analysis-framework.md](../../architecture/frameworks/cards/granular-analysis-framework.md)
- [../../architecture/frameworks/cards/processor-routing-framework.md](../../architecture/frameworks/cards/processor-routing-framework.md)
- [../../architecture/frameworks/cards/proposer-verifier-framework.md](../../architecture/frameworks/cards/proposer-verifier-framework.md)
- [../../architecture/frameworks/cards/evidence-record-framework.md](../../architecture/frameworks/cards/evidence-record-framework.md), when signals come from external sources
- [../../architecture/frameworks/cards/human-review-framework.md](../../architecture/frameworks/cards/human-review-framework.md), when a person or policy must accept the result

## Application Shape

```text
signal packet
-> bounded signal record
-> feature views
-> route-specific processors
-> candidate proposals
-> verifier / review / fallback / abstain
-> traceable signal decision
```

## Synthetic Example

A synthetic signal packet can expose:

```text
level view
trend view
regime view
source-quality view
```

Different processors can propose:

```text
level-supported review
trend-supported review
regime-supported review
fallback review
abstain
```

The selected decision is not truth because a signal was high. It advances only
through verifier, review, fallback, or abstain rules.

## Claim Boundary

The direct CGF eval is:
[../../labs/evals/signal-review/results.md](../../labs/evals/signal-review/results.md).

That eval supports only a tiny local contract. It does not support:

- financial advice;
- market prediction;
- production reliability;
- anomaly-detection performance;
- maintenance outcome improvement;
- fraud-detection performance;
- broad domain generalization.

## Current Status

This is an application note backed by the synthetic Signal Review eval. It is a
showcase of CGF separation rules, not a domain implementation.
