# Port-Hamiltonian Flow

## Definition

Port-Hamiltonian flow declares energy-like state, exchange ports, and structured
flows between parts of a subject.

## Parent layer

Substrate.

## Problem solved

Some subjects need energy exchange and interconnection structure to be explicit
so evolution does not violate physical or control meaning.

## Minimum substrate shape

- Energy-like state field.
- Flow and effort quantities.
- Ports or interfaces on graph support.
- Action or constraint expressing exchange structure.
- Validation check for admissible exchange.

## When to use

- Energy, effort, flow, or exchange structure matters.
- Interconnection should preserve a physical or control condition.
- Readout depends on admissible transfer.

## When not to use

- The subject has no energy-like exchange.
- Ordinary action and constraint declarations are enough.
- The exchange structure cannot be validated.

## Maturity

Research extension.

## Substrate-owned declarations

- Storage state: quantity that stores energy-like value.
- Hamiltonian: scalar storage or energy-like function of state.
- Flow: rate-like quantity changing storage.
- Effort: conjugate quantity paired with flow.
- Port: declared interface where exchange enters or leaves.
- Supply rate: exchange contribution through a port.
- Dissipation: loss term or inequality.
- Control input: selectable input that affects flow or supply.

## Validation checks

- Storage change matches declared flow, supply, and dissipation terms.
- Port signs and directions are explicit.
- Dissipation has the expected sign or bound.
- Control inputs stay within declared admissible support.
- Interconnected ports preserve the intended balance relation.

## Failure modes

- Treating open exchange as closed-system evolution.
- Omitting dissipation or supply from validation.
- Mixing effort and flow quantities without declaring conjugacy.
- Allowing controls that violate storage or port constraints.
- Reporting stable behavior while balance is drifting.
