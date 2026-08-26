# Causal Intervention

## Purpose

Causal intervention studies how a Substrate subject separates observation,
intervention, counterfactuals, causal claims, and attribution.

Core pattern:

```text
observe evidence
  -> mark intervention when action changes the subject
  -> observe outcome
  -> keep unacted alternatives counterfactual
  -> score attribution under declared assumptions
```

## Failure Mode

Without causal status, a subject can confuse correlation, prediction,
intervention, and imagined alternatives.

Common failures:

- observation is treated as an action;
- unacted alternatives are treated as outcomes;
- correlated variables receive causal credit;
- intervention scope is missing;
- attribution ignores uncertainty.

## Minimum Substrate Addition

Minimum records:

```text
observation
  subject_ref
  observed_value_ref
  context_refs
  evidence_refs
  observed_at

intervention
  intervention_scope
  action_ref
  actor_or_operator_ref
  assumption_refs

causal_claim
  cause_ref
  outcome_ref
  assumption_refs
  attribution_score
  uncertainty
```

Counterfactual records mark paths, states, or outcomes that did not happen but
remain useful for comparison.

## Conceptual Checks

- Observations do not create intervention status.
- Interventions have declared scope.
- Counterfactuals cannot become observed outcomes.
- Attribution follows the acted path, not merely correlated evidence.
- Causal claims carry assumptions and uncertainty.
- High-risk attribution requires stronger validation.

## Relationship To Nearby Extensions

- Stochastic transition predicts possible outcomes; causal intervention marks
  acted changes and attribution.
- Information geometry scores belief change; causal intervention decides
  whether the change can support a causal claim.
- Sheaf consistency can expose conflicting views, but it does not establish
  causality.
- Port-Hamiltonian flow accounts exchange and control effects; causal
  intervention marks the act.

## Validation Questions

- What was observed?
- What was intervened on?
- What was only counterfactual?
- What scope was the intervention allowed to affect?
- What assumptions support the causal claim?
- What evidence would reject the attribution?

## Maturity

Status: research-supported; CGF-local eval `contract-pass`.

The extension is ready as a card and study. Strong public claims require a
reference pass and careful examples.

## CGF Eval Result

See [../../labs/evals/causal-intervention/results.md](../../labs/evals/causal-intervention/results.md).
