# Attractor Diagnostics

## Purpose

Attractor Diagnostics studies dynamical-regime evidence for sequential
Substrate subjects.

Core pattern:

```text
time-indexed state
  -> recurrence or regime evidence
  -> cycle, expansion, distance, or escape warning
  -> readout and validation with uncertainty
```

## Failure Mode

A subject can pass local state checks while the underlying regime is changing.
Examples include drift away from a stable cycle, transition into a risky regime,
folding or expansion in state space, or escape from a known operating region.

## Minimum Substrate Addition

```text
dynamical_diagnostic
  state_support_ref
  sample_window
  regime_or_cycle_evidence
  local_expansion_or_distance
  warning_score
  uncertainty
```

The diagnostic is useful only when the subject's action, readout, or validation
depends on dynamical regime structure.

## Conceptual Checks

- Inputs resolve to declared state or field observations.
- Warnings state their sample window and uncertainty.
- Cycle or recurrence signals are not forced when data is under-sampled.
- Escape evidence remains a warning unless independently validated.

## Relationship To Nearby Extensions

- Topological rigidity can preserve cycle or phase-like structure.
- Metric placement can measure distance to regimes or transition corridors.
- Stochastic transition can represent uncertain next-regime predictions.
- Information geometry can compare distributions over regimes.
- CellComplexView can make cycle or episode support explicit.

## Validation Questions

- What regime structure is being protected or detected?
- Is the diagnostic tied to declared state and placement?
- What baseline would produce the same warning without attractor language?
- Does the warning change readout or validation?
- Is uncertainty visible?

## Maturity

Status: research-supported. No direct Labs eval yet.
