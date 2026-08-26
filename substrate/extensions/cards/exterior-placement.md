# Exterior Placement

## Definition

Exterior placement declares quantities that live outside the main graph support
but still affect the subject.

## Parent layer

Substrate.

## Problem solved

Some important fields are not naturally node, edge, region, or mode values
inside the declared graph, but treating them as ordinary internal state hides
their role.

## Minimum substrate shape

- Internal graph support.
- Exterior quantity and type.
- Contact point or relation to internal support.
- Constraint or action term affected by the exterior quantity.
- Validation check that exterior values are not confused with internal state.

## When to use

- Environment, demand, control input, observation, or context affects a subject.
- The exterior quantity should be declared but not internalized.
- Readout needs to distinguish internal state from external condition.

## When not to use

- The quantity naturally lives on the declared graph.
- The outside condition has no effect on action, evolution, readout, or
  validation.
- The distinction adds vocabulary without preventing an actual mistake.

## Maturity

Draft extension.

## Substrate-owned declarations

- Exterior quantity: demand, forcing, control input, environment state,
  observation, context, or boundary-side value.
- Contact relation: where the exterior quantity touches node, edge, face, cell,
  region, mode, or boundary support.
- Exchange rule: how the exterior quantity affects action, constraint,
  evolution, readout, or validation.
- Scope: whether the exterior quantity is fixed, time-varying, measured,
  imposed, sampled, or uncertain.
- Separation rule: what remains internal state and what remains an exterior
  condition.

## Natural placement guide

Use this guide when a geometric or field-like subject risks forcing every
quantity onto nodes:

| Quantity | Natural support |
| --- | --- |
| Scalar potential or local entity state | Node |
| Flow, current, gradient, transition, or relation | Edge |
| Flux, curl, circulation, or surface constraint | Face |
| Mass, charge, volume density, or conserved amount | Cell or volume |
| Harmonic, spectral, or modal coefficient | Mode or mode bundle |

If the quantity lives at a boundary, contact surface, exterior condition, or
source term, declare the contact relation instead of hiding it as ordinary node
state.

## Validation checks

- Exterior values are not silently promoted into durable internal state.
- Effects enter only through declared contact relations or exchange terms.
- Conservation, balance, or admissibility checks include exterior exchange when
  relevant.
- Readout reports whether it depends on interior state, exterior condition, or
  both.
- Missing exterior values produce explicit uncertainty or invalidity.

## Failure modes

- Treating environment or control as ordinary graph state.
- Hiding boundary forcing inside evolution without declaring contact support.
- Forgetting that an observed exterior value may be stale or uncertain.
- Making the exterior quantity so broad that every dependency becomes
  "context."
- Failing to validate whether the exterior quantity actually affects the
  subject.
