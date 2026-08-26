# Gauge Transport

## Definition

Gauge transport declares how field values remain comparable across local frames,
orientations, or coordinate choices.

## Parent layer

Substrate.

## Problem solved

Field values may appear different because their local frames differ, not because
the underlying subject state differs.

## Minimum substrate shape

- Field with local frame dependence.
- Graph support carrying local frames.
- Transport relation between supports.
- Action, constraint, or validation rule using transported values.
- Check for frame-consistent comparison.

## When to use

- Orientation, phase, frame, basis, or coordinate choice affects comparison.
- Evolution moves values across differently framed support.
- Readout depends on frame-consistent field meaning.

## When not to use

- Fields are globally comparable without transport.
- Local frame differences have no domain meaning.
- The transport rule cannot be validated.

## Maturity

Research extension.

## Substrate-owned declarations

- Frame: local basis, orientation, coordinate chart, phase convention, or
  representation context.
- Gauge: allowed transformation between equivalent local descriptions.
- Connection: rule for relating nearby frames.
- Transport map: map that carries field values between supports.
- Holonomy or loop check: accumulated mismatch after transport around a closed
  path.
- Transport residual: disagreement after values are transported into a common
  frame.

## Validation checks

- Field comparison happens only after transport into a compatible frame.
- Transport maps respect declared source and target frames.
- Inverse or round-trip transport errors are bounded where required.
- Holonomy is reported when loop transport is meaningful.
- Residuals separate frame mismatch from true state disagreement.

## Failure modes

- Comparing coordinates from different frames as if they were the same value.
- Hiding unit, orientation, or representation changes inside adapters.
- Treating a large transport residual as field disagreement without checking
  frame mismatch.
- Declaring a connection but not validating round-trip behavior.
- Using transport when the subject has no meaningful local-frame dependence.
