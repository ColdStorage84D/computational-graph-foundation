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

This eval does not claim physics accuracy, solver quality, global optimization,
autonomous reasoning, benchmark performance, analog-computing performance, or a
general mathematical engine.

It only checks that the local CGF contract exposes action or law, constraints,
evolution, residual/error, validation, and readout before accepting a result.
