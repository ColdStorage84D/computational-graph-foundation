# Substrate Extensions

Substrate extensions are optional components used when a domain has structure
that the 9 core primitives can name but not fully protect or express.

They are not mandatory primitives. They are domain-triggered additions.

## Position In Substrate

```text
core primitives -> optional extension components -> domain-specific use
```

Use an extension only when a real failure mode appears in the subject. Do not
add extensions because they sound general or advanced.

## Extension Components

The current extension registry is [registry.md](registry.md).

Recommended reading order:

```text
registry.md -> topology-guide.md -> cards/README.md -> decision-guide.md
-> composition-patterns.md -> walkthroughs.md
-> ../../research/connection-map.md
-> ../../research/extension-studies/README.md
```

Cards:

- [cards/topological-rigidity.md](cards/topological-rigidity.md)
- [cards/basis-mode-representation.md](cards/basis-mode-representation.md)
- [cards/cell-complex-view.md](cards/cell-complex-view.md)
- [cards/attractor-diagnostics.md](cards/attractor-diagnostics.md)
- [cards/exterior-placement.md](cards/exterior-placement.md)
- [cards/weak-form.md](cards/weak-form.md)
- [cards/metric-placement.md](cards/metric-placement.md)
- [cards/stochastic-transition.md](cards/stochastic-transition.md)
- [cards/information-geometry.md](cards/information-geometry.md)
- [cards/gauge-transport.md](cards/gauge-transport.md)
- [cards/sheaf-consistency.md](cards/sheaf-consistency.md)
- [cards/port-hamiltonian-flow.md](cards/port-hamiltonian-flow.md)
- [cards/causal-intervention.md](cards/causal-intervention.md)
- [cards/renormalization-coarse-graining.md](cards/renormalization-coarse-graining.md)
- [cards/differentiable-backend.md](cards/differentiable-backend.md)

Usage guides:

- [topology-guide.md](topology-guide.md): separates graph topology,
  higher-dimensional topology, topological rigidity, and application graph
  topology.
- [decision-guide.md](decision-guide.md): when an extension is required,
  optional, or wrong.
- [composition-patterns.md](composition-patterns.md): common extension
  combinations and their boundaries.
- [walkthroughs.md](walkthroughs.md): short prose examples that apply
  extension choices after the 9 core primitives are complete.
- [../../research/connection-map.md](../../research/connection-map.md):
  card-to-study-to-eval map for extension support and claim boundaries.
- [../../research/extension-studies/README.md](../../research/extension-studies/README.md):
  deeper research notes for extension theory, validation questions, and
  maturity without making cards too large.

## Rule

Every extension must state its parent layer, problem solved, minimum substrate
shape, when to use it, when not to use it, and maturity.

Extension cards may also include Substrate-owned declarations, validation
checks, and failure modes. Those details should sharpen the subject
declaration without turning the extension into a system design or SDK.
