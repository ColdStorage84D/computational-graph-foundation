# Causal Intervention

## Definition

Causal intervention declares an intentional change to part of a subject while
separating it from ordinary observation.

## Parent layer

Substrate.

## Problem solved

Observed association can be mistaken for what would happen under deliberate
change.

## Minimum substrate shape

- State or field being intervened on.
- Intervention value or condition.
- Graph support affected.
- Constraints on admissible intervention.
- Readout and validation rules for intervention results.

## When to use

- The subject asks what changes under an imposed condition.
- Readout should distinguish observation from intervention.
- Validation must check that only declared parts were changed.

## When not to use

- The subject is purely observational.
- There is no declared intervention target.
- Effects cannot be separated from ordinary state change.

## Maturity

Draft extension.

## Substrate-owned declarations

- Observation: state read without imposed change.
- Intervention target: field, node, edge, region, or variable being set or
  forced.
- Intervention value or policy: imposed condition and allowed range.
- Causal graph or dependency support: declared relations relevant to the
  intervention.
- Counterfactual readout: result under an alternate declared condition.
- Attribution path: support used to explain which declared changes affected the
  result.
- Intervention scope: what may change and what must remain fixed.

## Validation checks

- Observation and intervention states are not mixed.
- Non-intervened fields remain within declared allowed change.
- Readout states whether it is observational, interventional, or
  counterfactual.
- Attribution is limited to declared support and evidence.
- Intervention effects respect constraints and admissible state support.

## Failure modes

- Treating correlation as intervention evidence.
- Changing undeclared state while claiming a scoped intervention.
- Reporting counterfactuals without a declared alternate condition.
- Letting attribution extend beyond observed or declared support.
- Using causal language when the subject only declares association.
