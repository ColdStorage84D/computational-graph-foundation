# Port-Hamiltonian Flow

## Purpose

Port-Hamiltonian flow studies open systems with storage, exchange,
dissipation, and control.

Core pattern:

```text
storage state + ports + control + dissipation
  -> open-system flow
  -> storage balance, supply, loss, and residual
```

## Failure Mode

Closed-system modeling hides the cost and exchange structure of many subjects.

Common failures:

- external input is treated as internal state;
- dissipation is hidden by aggregate success;
- storage changes have no balance check;
- incompatible ports are composed;
- control effects are not separated from ordinary evolution.

## Minimum Substrate Addition

Minimum records:

```text
storage_state
  support_ref
  state_ref
  storage_function_ref
  units_or_type_basis
  evidence_refs

port
  port_id
  boundary_ref
  quantity_type
  direction
  compatibility_basis

flow_balance
  storage_change
  supply
  dissipation
  residual
```

The extension can also declare effort, flow, Hamiltonian, supply rate, control
input, and open-system boundary.

## Conceptual Checks

- Storage change balances declared supply and dissipation.
- Port input is typed and evidence-backed.
- Port composition checks compatible quantity types.
- Dissipation remains visible.
- Undeclared external input raises uncertainty.
- Flow balance does not replace validation.

## Relationship To Nearby Extensions

- Causal intervention marks that an action was taken; port-Hamiltonian flow
  accounts how it enters the open system.
- Stochastic transition can model uncertain flow outcomes.
- Information geometry can score uncertainty in storage or outcome beliefs.
- Exterior placement can place flows on edges, faces, or cells.

## Validation Questions

- What quantity is stored?
- Where can it enter or leave?
- What is dissipated or lost?
- What control input is declared?
- Does the balance residual stay visible?
- Are incompatible ports rejected?

## Maturity

Status: research-supported; CGF-local eval `contract-pass`.

The extension is ready as a card and study. Domain-specific flow laws and
port-compatibility records need concrete examples.

## CGF Eval Result

See [../../labs/evals/port-hamiltonian-flow/results.md](../../labs/evals/port-hamiltonian-flow/results.md).

## References

Public source for port-Hamiltonian systems. The eval implements the linear input-state-output form with dissipation described there.

- [Port-Hamiltonian Systems Theory: An Introductory Overview](https://doi.org/10.1561/2600000002), van der Schaft and Jeltsema (2014). Interconnection, dissipation, and port structure, the power balance, and why interconnections of port-Hamiltonian systems are again port-Hamiltonian.
