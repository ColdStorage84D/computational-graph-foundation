# Causal Intervention Eval

Status: `contract-pass`

This eval has two layers.

The model layer is a finite structural causal model solved by exact
enumeration. It answers three different questions about the same system and
shows that they have three different answers:

```text
observe      P(Y | X = 1)                 what we see among units that have X = 1
intervene    P(Y | do(X = 1))             what happens if we set X = 1
counterfact  P(Y had X been 0 | X=1, Y=1) what would have happened to this unit
```

The record layer keeps observation, intervention, and counterfactual records
apart once they leave the model, and refuses to promote a counterfactual.

## Fixture

`Z` causes both `X` and `Y`, and `X` also causes `Y`. The effect of `X` on `Y`
is set to +0.1, 0, or -0.1.

## Contract

- The observed contrast and the interventional contrast differ under
  confounding, and can have opposite signs.
- Backdoor adjustment over `Z` recovers the interventional value from
  observational quantities alone.
- An intervention on `X` leaves the distribution of its cause `Z` unchanged.
- A counterfactual keeps the unit's noise fixed and differs from an
  intervention on a fresh unit.
- Undeclared parents, undeclared intervention targets, and impossible evidence
  are rejected.
- A reported effect is packaged as an intervention record scoped to the
  intervened variable.

## Connections

- Substrate: [causal intervention](../../../substrate/extensions/cards/causal-intervention.md).
- Research: [causal intervention study](../../../research/extension-studies/causal-intervention.md).
- Result record: [results.md](results.md).

## Files

- [eval.py](eval.py): the model and the record functions.
- [test_model.py](test_model.py): tests for the structural causal model.
- [test_eval.py](test_eval.py): tests for the record discipline.
