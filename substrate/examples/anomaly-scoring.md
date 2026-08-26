# Anomaly Scoring

This is the third teaching example for the 9 core Substrate primitives. It
shows Substrate as a risk and evidence subject rather than a physics or
optimization subject.

## Graph

A small activity graph with accounts, devices, network addresses, and events:

```text
account:a0 -- uses --> device:d0
account:a0 -- login --> event:e0
event:e0   -- from  --> ip:p0
account:a1 -- uses --> device:d1
account:a1 -- login --> event:e1
event:e1   -- from  --> ip:p0
```

## Typed field

Risk score is a scalar typed field. Event count is an integer typed field.
Trust level is a categorical typed field.

## Placement

Risk score is placed on accounts and devices. Event count is placed on login
events. Trust level is placed on accounts.

## State

The current state is the observed activity and current field values:

```text
account:a0 risk: 0.20 trust: known
device:d0  risk: 0.10
event:e0   count: 1

account:a1 risk: 0.70 trust: new
device:d1  risk: 0.60
event:e1   count: 1
```

## Action

Suspicious activity should receive higher risk. Shared network addresses,
new accounts, unfamiliar devices, and unusual event patterns increase the risk
preference.

## Constraint

Missing evidence must not be treated as confirmed behavior. A score can use only
declared graph state and declared typed fields.

## Evolution

Risk changes as new events arrive. A new login event can update account and
device risk when it connects to existing suspicious structure.

## Readout

The domain answer is a ranked anomaly list with the entities that currently
carry the highest risk.

## Validation

Each reported anomaly must trace back to declared graph state, declared typed
fields, and allowed scoring inputs. The example must not use hidden labels or
missing evidence as if they were observed facts.

The purpose is not to build a production detector. The purpose is to show how
graph, typed field, placement, state, action, constraint, evolution, readout,
and validation can describe a risk subject in the same core shape as the other
Substrate examples.

