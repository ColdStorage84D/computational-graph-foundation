# Differentiable Backend

## Definition

Differentiable backend declares that a Substrate subject should be represented
so automatic differentiation can compute sensitivities.

## Parent layer

Substrate.

## Problem solved

Some implementations need gradients or sensitivities, but differentiability is
often assumed without declaring which fields, actions, and readouts support it.

## Minimum substrate shape

- Differentiable fields.
- Differentiable action or readout.
- Constraints that affect differentiability.
- Non-differentiable parts, if any.
- Validation check for gradient meaning.

## When to use

- Optimization or learning depends on gradients.
- Sensitivity analysis is part of readout or validation.
- The subject must state which parts are differentiable.

## When not to use

- No gradient or sensitivity is needed.
- Non-differentiable logic dominates the subject.
- Gradient values cannot be validated or interpreted.

## Maturity

Draft extension.

## Substrate-owned declarations

- Differentiable fields: fields represented in a gradient-capable form.
- Differentiable parameters: values intended for optimization or sensitivity.
- Differentiable action, residual, or readout: exact expression that gradients
  apply to.
- Non-differentiable parts: constraints, projections, discrete choices, clamps,
  or validation checks that break or stop gradients.
- Gradient target: what variable is optimized, explained, or measured.
- Backend assumptions: tensor shape, dtype, device, precision, and allowed
  approximation.

## Validation checks

- Gradients are finite and tied to declared fields and parameters.
- Finite-difference or perturbation checks agree where practical.
- Constraint handling does not create misleading gradients.
- Detached or non-differentiable parts are explicit.
- Optimization readout still satisfies Substrate validation.

## Failure modes

- Assuming differentiability because code uses tensors.
- Taking gradients through invalid projections or hidden state changes.
- Optimizing a surrogate action while reporting a different readout.
- Ignoring constraints that make the gradient meaningless.
- Treating backend choice as part of the conceptual Substrate contract.
