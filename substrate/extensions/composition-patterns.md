# Extension Composition Patterns

## Purpose

Some subjects need more than one extension. This guide names common
combinations and explains why they fit together.

## Composition patterns

Composition should start from a complete 9-core subject. Add the smallest
extension set that protects the failure mode.

## Weak form + exterior placement

Use when the subject has a law that is best checked over aggregate support and
is affected by boundary-side, environment, forcing, demand, or control-like
conditions.

Typical shape:

```text
core subject
+ exterior quantity and contact relation
+ aggregate test support
+ weak residual
+ validation for boundary or exchange contribution
```

Good fit:

- noisy measurement over a physical or operational field;
- boundary forcing that should not become internal state;
- regional conservation or balance checked over support.

Wrong fit:

- the local rule is clean and complete;
- the exterior condition does not affect action, evolution, or readout;
- the aggregate hides failures that the readout depends on.

## CellComplexView + weak form

Use when aggregate laws live on declared cells, regions, surfaces, or volumes
instead of only individual nodes or edges.

Typical shape:

```text
core subject
+ cell support and boundary relations
+ aggregate test support on cells
+ weak residual over each declared support
+ validation that residuals resolve to declared boundaries
```

Good fit:

- regional balance laws;
- surface or volume support;
- image, mesh, or map regions with boundary-sensitive readouts;
- laws that are invalid if the region boundary is ambiguous.

Wrong fit:

- node-edge support already declares the needed computation;
- the cell boundary cannot be checked;
- aggregate support hides local failure without reporting a residual.

## Metric placement + gauge transport

Use when distance matters and values must be compared across local frames,
charts, orientations, or bases.

Typical shape:

```text
core subject
+ metric or coordinate placement
+ local frame declaration
+ transport map
+ distance or residual after transport
```

Good fit:

- geometry-aware field comparison;
- multi-frame sensor or map alignment;
- movement across coordinate contexts.

Wrong fit:

- all fields are globally comparable;
- distance has no action or validation role;
- the frame relation cannot be checked.

## Sheaf consistency + gauge transport

Use when partial local views overlap, but the values must be transported before
they can be compared.

Typical shape:

```text
core subject
+ local views and supports
+ overlap declarations
+ frame or representation context
+ restriction after transport
+ consistency residual
```

Good fit:

- regional records that use different conventions;
- inventory or catalog state assembled from partial views;
- local assignments that need compatibility before global readout.

Wrong fit:

- there are no overlaps;
- values already share one frame;
- disagreement is acceptable and does not affect validation.

## Stochastic transition + information geometry

Use when evolution produces distributions and the subject needs to compare,
update, or validate those distributions as structured fields.

Typical shape:

```text
core subject
+ transition kernel
+ distribution field
+ divergence or information term
+ calibration or uncertainty validation
```

Good fit:

- uncertain next-state prediction;
- belief update;
- risk-sensitive readout;
- distribution drift or calibration checks.

Wrong fit:

- the subject has deterministic evolution;
- uncertainty has no validation path;
- scalar scores are enough for the readout.

## Causal intervention + stochastic transition

Use when the subject asks what distribution of outcomes follows from an imposed
condition.

Typical shape:

```text
core subject
+ intervention target and scope
+ transition kernel under imposed condition
+ admissible next-state support
+ validation that non-target state changes remain scoped
```

Good fit:

- controlled what-if analysis;
- intervention-sensitive risk;
- comparison between observed and imposed conditions.

Wrong fit:

- the subject is purely observational;
- the intervention target is vague;
- stochastic output is used as causal proof without scoped validation.

## Renormalization + differentiable backend

Use when fine and coarse subjects must be related while parameters or operators
are tuned by gradient-based methods.

Typical shape:

```text
core subject
+ fine-to-coarse projection
+ effective coarse action or readout
+ differentiable parameters
+ scale residual and gradient checks
```

Good fit:

- multiscale approximation;
- learned coarse operator;
- inverse design over coarse parameters.

Wrong fit:

- coarse behavior is not validated against fine behavior;
- gradients optimize a surrogate that does not match the declared readout;
- the original subject is already small enough.

## Topological rigidity + metric placement

Use when geometry is needed but must not erase declared cycles, explicit phase
degree, named twist diagnostics, or regime structure.

Typical shape:

```text
core subject
+ metric placement
+ protected cycle or regime support
+ explicitly typed carrier field
+ reference-relative structure-retention term
+ reference-relative collapse-risk or topology-preservation validation
```

Good fit:

- cyclic trajectories;
- regime-preserving embeddings;
- compression that must protect rare transitions;
- explicit-phase-degree or named cycle-diagnostic readout.

Wrong fit:

- geometry is only visual;
- no protected structure is declared;
- rigidity preserves noise rather than domain meaning.

## Attractor diagnostics + stochastic transition

Use when the subject has uncertain dynamics and needs to report whether state
is settling into, escaping from, or oscillating around a declared regime.

Typical shape:

```text
core subject
+ transition uncertainty
+ regime or basin field
+ recurrence, escape, or trapping diagnostic
+ validation that diagnostics are warnings, not solver authority
```

Good fit:

- noisy regime tracking;
- trap or oscillation warnings;
- distributional transitions where recurrence matters;
- early warning before a readout declares a regime change.

Wrong fit:

- there is no sequence, transition, or recurrence signal;
- a diagnostic is treated as proof of an attractor;
- the subject needs a controller rather than a declared diagnostic.

## Attractor diagnostics + topological rigidity

Use when dynamical regimes also have protected cycles, loops, explicit phase
structure, or rare transitions that should not collapse under smoothing or
compression.

Typical shape:

```text
core subject
+ recurrent support or basin declaration
+ protected cycle, explicit-phase, or rare-transition support
+ collapse-risk and escape diagnostics
+ validation that separates recurrence warnings from topology preservation
```

Good fit:

- cyclic or phase-sensitive regime dynamics;
- rare transition corridors;
- compressed trajectories where regime collapse would invalidate readout.

Wrong fit:

- recurrence alone is enough and no protected topology is declared;
- topology preservation is used without a measurable carrier field;
- diagnostic warnings are described as guaranteed prediction.

## Basis-mode representation + differentiable backend

Use when a symmetry or eigenbasis gives a coefficient graph and the coefficients,
operator weights, or readout parameters need gradient-based tuning.

Typical shape:

```text
core subject
+ basis family and mode labels
+ coefficient fields on mode nodes
+ diagonal, sparse, block, or selection-rule operator support
+ differentiable parameters or readout
+ residual, truncation, and forbidden-coupling validation
```

Good fit:

- Fourier, spherical, manifold, or reduced-order coefficient models;
- learned operator surrogates that should preserve declared mode support;
- inverse design or fitting over coefficient-space parameters.

Wrong fit:

- the basis has no domain meaning;
- gradients optimize a hidden model output rather than the declared readout;
- the implementation writes outside allowed mode support without reporting a
  residual.

## Basis-mode representation + topological rigidity

Use when the subject has a useful mode basis and the mode dynamics also carry
declared cycles, explicit phase degree, regimes, or reference-relative
collapse-risk structure that should survive compression or learning.

Typical shape:

```text
core subject
+ mode graph and coefficient fields
+ selection-rule edges
+ protected cyclic, phase, or regime support in mode dynamics
+ topology-preservation validation
```

Good fit:

- phase-bearing modal trajectories;
- regime changes expressed in coefficient space;
- reduced-order dynamics where truncation may erase rare transitions.

Wrong fit:

- basis-mode alone already gives the needed invariants and validation;
- the protected topology is not declared or cannot be checked;
- topological rigidity is used as a substitute for a missing basis declaration.

## Composition rule

When combining extensions, each one must earn its place:

```text
extension A declares one missing structure
extension B declares a different missing structure
validation explains how both affect the readout
```

If two extensions solve the same failure mode, keep the simpler one.
