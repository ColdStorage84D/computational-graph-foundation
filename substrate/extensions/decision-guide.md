# Extension Decision Guide

## Purpose

This guide helps decide when a Substrate subject should use an extension.

Extensions are optional. They are added only when the 9 core primitives can name
the subject but cannot fully protect, express, or validate an important domain
structure.

## Extension gate

Do not choose an extension until the subject can answer all 9 core questions:

```text
1. What is the graph?
2. What typed fields live on it?
3. Where is each field placed?
4. What is the current state?
5. What action, law, cost, or objective governs the subject?
6. What is constrained?
7. How does state evolve?
8. What answer is read out?
9. How is the result validated?
```

If one of those answers is missing, finish the core subject first. An extension
must never hide a missing core primitive.

## Decision table

| Extension | Required when | Optional when | Wrong when |
| --- | --- | --- | --- |
| Topological rigidity | A declared cycle, explicit phase degree, or named twist or regime diagnostic must survive smoothing, compression, or learning. | Reference-relative collapse risk is useful evidence but not central to the readout. | The subject has no protected recurrent or topological structure, or no valid reference exists for the claimed collapse score. |
| CellComplexView | Regions, surfaces, closed boundaries, or higher-order support affect action, readout, or validation. | Cell support improves explanation but edge support remains adequate. | Cells are only visual labels and no boundary check exists. |
| Attractor Diagnostics | Regime drift, recurrence, cycle behavior, or escape warning affects readout or validation. | Dynamical evidence improves warning quality but a simpler evolution check still works. | The subject is not sequential or the diagnostic cannot be tied to declared state. |
| Basis-mode representation | A known symmetry or eigenbasis makes mode coefficients, selection rules, and structured operators the valid subject representation. | A mode view improves compression, readout, or invariant checks but the sampled graph remains usable. | No meaningful basis exists, or the subject is better represented by ordinary graph nodes or the system-operation layer. |
| Exterior placement | A condition affects the subject but should not be treated as internal graph state. | Context affects readout but does not drive evolution. | The quantity naturally lives on the declared graph. |
| Weak form | Pointwise rules are invalid, too noisy, or unavailable, but aggregate tested conditions are meaningful. | The local law is clear but aggregate checks improve validation. | Aggregate checks would hide local failures that matter. |
| Metric placement | Distance, scale, curvature, or coordinate validity changes action, evolution, or readout. | Geometry is useful for interpretation but not decisive. | Geometry is only for display. |
| Stochastic transition | The subject declares distributions over possible next states. | Uncertainty improves risk or quality readout. | A deterministic evolution is adequate and uncertainty cannot be checked. |
| Information geometry | Probability, belief, or distribution fields require divergence, entropy, calibration, or metric structure. | Distribution comparison is useful but not central. | The subject only uses ordinary scalar or vector fields. |
| Gauge transport | Field comparison depends on frame, orientation, basis, phase, or coordinate context. | Transport residuals improve validation. | Fields are already globally comparable. |
| Sheaf consistency | Local assignments overlap and must agree before a global assignment is trusted. | Partial views may conflict and need diagnostics. | There is one global assignment with no meaningful overlaps. |
| Port-Hamiltonian flow | Storage, effort, flow, ports, supply, dissipation, or control balance defines validity. | Exchange accounting improves validation. | The subject has no energy-like or balance-like exchange. |
| Causal intervention | The readout asks what changes under an imposed condition. | Intervention status helps separate observed and imposed state. | The subject is only observational. |
| Renormalization / coarse-graining | Fine and coarse descriptions must preserve selected action, readout, or invariant behavior. | Coarse views help inspect or approximate a large subject. | Coarsening destroys the property being studied and no residual is checked. |
| Differentiable backend | Gradients or sensitivities are part of optimization, learning, or validation. | Gradient checks help tune parameters. | No gradient is needed, or non-smooth logic dominates the subject. |

## Required, optional, or wrong

Use this rule:

```text
required:
  Without the extension, the subject gives a misleading or invalid answer.

optional:
  The extension improves validation or clarity, but the core subject remains
  usable without it.

wrong:
  The extension adds vocabulary without preventing a real failure mode.
```

## Validation questions before promotion

Before using an extension in an example, application, or code note, answer:

```text
1. Which failure mode does this extension prevent?
2. Which core primitives does it depend on?
3. What new declaration does it add?
4. What validation check becomes possible?
5. What readout changes if the extension is removed?
6. What makes the extension invalid or out of scope?
```

If those answers are unclear, keep the subject in draft form.
