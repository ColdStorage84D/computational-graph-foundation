# Renormalization / Coarse-Graining

## Purpose

Renormalization / coarse-graining studies how a Substrate subject can change
scale while preserving the behavior that matters.

The extension exists because some subjects contain fine detail that should be
summarized, but the summary must not erase the law, invariant, interaction, or
failure mode the subject cares about.

## Failure Mode

A summary can look simpler while destroying the relevant computation.

Common failures:

- coarse nodes lose source references;
- distractor features dominate local scoring;
- the relevant interaction only appears at a larger scale;
- fine/coarse residuals are hidden;
- a learned coarse model improves one metric while losing the declared law.

## Minimum Substrate Addition

Minimum records:

```text
coarse_graining
  fine_support_refs
  coarse_support_ref
  aggregation_rule_ref
  preserved_quantity_refs
  discarded_quantity_refs
  consistency_residual
  evidence_refs

coarse_operator
  coarse_support_ref
  operator_basis
  relevant_interaction_refs
  uncertainty
```

The extension should state exactly what survives scale change and what is
allowed to be discarded.

## Conceptual Checks

- Coarse supports preserve source refs.
- The declared relevant law survives coarse-graining.
- Fine/coarse consistency residual is visible.
- Distractor suppression does not erase true positives.
- The same coarse law transfers across comparable regimes.
- Readout reports the scale at which the answer was produced.

## Relationship To Nearby Extensions

- Metric placement can define neighborhoods or hierarchy before
  coarse-graining.
- Gauge transport handles frame change; coarse-graining handles scale change.
- Operator learning can learn coarse operators, but validation still belongs
  to the declared subject.
- Differentiable backend can support learned or inverse coarse-graining later.

## Validation Questions

- What quantity or law must survive the scale change?
- What fine details are allowed to be discarded?
- Does the coarse record preserve source references?
- Does the residual expose lost structure?
- Does coarse-graining beat the baseline failure mode?
- Does it improve the target failure without claiming universal predictor
  superiority?

## Maturity

Status: research-supported; CGF-local eval `contract-pass`.

The extension is ready as a card and study. Future work should add examples
that make the preserved law explicit.

## CGF Eval Result

See [../../labs/evals/renormalization-coarse-graining/results.md](../../labs/evals/renormalization-coarse-graining/results.md).
