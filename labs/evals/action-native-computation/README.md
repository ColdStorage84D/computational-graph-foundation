# Action-Native Computation Eval

Status: `contract-pass`

This eval tests the tiny local contract for Action-Native Computation:
computation as constrained graph-state evolution.

The fixture covers three calculation families:

- relaxation / settling;
- constraint satisfaction;
- least-action path.

## Connections

- Substrate: [Action-Native Computation](../../../substrate/derivatives/action-native-computation.md).
- Research: [derivative mechanics study](../../../research/derivative-mechanics-study.md).
- Result record: [results.md](results.md).

## Boundary

The claim boundary is in [results.md](results.md).

The eval checks that the local CGF contract exposes action or law, constraints,
evolution, residual/error, validation, and readout before accepting a result.
