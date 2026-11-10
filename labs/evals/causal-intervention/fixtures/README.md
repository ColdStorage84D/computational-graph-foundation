# Fixtures

Inline records cover observations, interventions, counterfactuals, outcome
records, causal scope, and attribution traces.

The structural causal model tests use `confounded_model`, where `Z` causes both
`X` and `Y` and the effect of `X` on `Y` is set by the caller.
