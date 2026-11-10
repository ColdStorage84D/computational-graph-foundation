# Local-Voting World Model Eval Results

Status: `contract-pass`

Eval layer: `isolated`

Reviewed date: 2026-06-10

## Result

The local eval passes its stated contract:

- a column binds feature input to path-integrated reference-frame location;
- single-column observations produce ambiguous hypotheses;
- lateral voting reinforces the object hypothesis shared across columns;
- unsupported hypotheses decay and remain visible as rejected alternatives;
- the selected object model predicts the next feature after an action.

## Claim Boundary

This is a tiny synthetic fixture. It supports only the claim that CGF can
represent and run a toy feature-location / voting / prediction mechanism as a
graph-shaped computation.

It does not support a general world-model claim or a real-world performance
claim.
