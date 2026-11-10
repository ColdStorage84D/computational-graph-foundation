# Port-Hamiltonian Flow Eval

Status: `contract-pass`

This eval has two layers.

The model layer is a linear port-Hamiltonian system:

```text
x' = (J - R) grad H(x) + G u        y = G^T grad H(x)        H(x) = 1/2 x^T Q x
J skew-symmetric    moves energy between states without creating it
R positive semidef  can only remove energy
G                   the ports, the only way energy enters or leaves
```

It is stepped with the implicit midpoint rule, for which the discrete power
balance `H(next) - H(now) = supplied - dissipated` holds to rounding error.

The record layer carries storage, supply, work, and dissipation out of the
model and reports whatever does not add up as a residual.

## Fixture

A mass-spring-damper with state (position, momentum). The port is force in,
velocity out. Two of them are interconnected through their ports.

## Contract

- With no damping and no input, energy is conserved over 2000 steps.
- With damping, energy never increases and the loss equals the accumulated
  dissipation.
- With a driven port, the change in energy equals supply minus dissipation.
- A non-skew `J`, a negative damping, and a non-positive storage matrix are
  rejected.
- A power-conserving interconnection of two systems is again port-Hamiltonian
  and conserves total energy while energy moves between the parts.
- A loss that the accounting does not declare shows up as a residual of
  exactly that size.

## Connections

- Substrate: [port-Hamiltonian flow](../../../substrate/extensions/cards/port-hamiltonian-flow.md).
- Research: [port-Hamiltonian flow study](../../../research/extension-studies/port-hamiltonian-flow.md).
- Result record: [results.md](results.md).

## Files

- [eval.py](eval.py): the system, the integrator, and the accounting records.
- [test_model.py](test_model.py): tests for the port-Hamiltonian structure.
- [test_eval.py](test_eval.py): tests for the accounting records.
