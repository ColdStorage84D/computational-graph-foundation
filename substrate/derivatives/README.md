# Substrate Derivatives

Derivative mechanics explain how a complete Substrate subject can be sharpened
into equations, operators, checks, and implementation choices.

They are not core primitives. A subject is complete when it declares the 9 core
primitives. Derivative mechanics become useful when a subject needs more formal
computational structure.

## Position In Substrate

```text
core primitives -> derivative mechanics -> optional implementation
```

Core primitives answer what is computed. Derivative mechanics answer what extra
declarations are needed to make the computation precise, testable, or ready for
a chosen method.

For the broad framing of computation as constrained graph-state evolution, read
[action-native-computation.md](action-native-computation.md).

## Derivative Mechanics

- [cards/units-dimensions.md](cards/units-dimensions.md): units / dimensions.
- [cards/boundary.md](cards/boundary.md): boundary conditions or boundary
  support.
- [cards/source.md](cards/source.md): injected, removed, or externally supplied
  quantities.
- [cards/local-action-lagrangian.md](cards/local-action-lagrangian.md): local
  action / Lagrangian terms.
- [cards/variation.md](cards/variation.md): allowed changes used to derive a
  condition.
- [cards/operator-assembly.md](cards/operator-assembly.md): operator assembly
  from local declarations.
- [cards/invariant.md](cards/invariant.md): quantities or relations that should
  remain stable.
- [cards/residual-error-estimator.md](cards/residual-error-estimator.md):
  residual / error estimator.
- [cards/solver-selection.md](cards/solver-selection.md): solver selection.

For the full overview, read [mechanics.md](mechanics.md). For light math and
tiny pseudocode, read [implementation.md](implementation.md).

For subjects that ask how a graph calculates from declared actions, laws,
constraints, residuals, and validation, read
[action-native-computation.md](action-native-computation.md).

For subjects that use action principles, least-action language, geodesics,
variational paths, or residual-based stationarity, read
[stationary-path.md](stationary-path.md).

## Rule

Add derivative mechanics only after the 9 core primitives are explicit. Do not
use a derivative mechanic to hide a missing graph, field, placement, state,
action, constraint, evolution, readout, or validation declaration.
