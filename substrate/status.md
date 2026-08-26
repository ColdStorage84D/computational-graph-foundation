# Substrate Status

This page records the current readiness of the Substrate section.

## Current Status

Substrate has a stable v0.1 core contract and a v0.2 documentation expansion.

The v0.1 core is stable enough for a developer to:

- understand the purpose of Substrate;
- declare a subject with the 9 core primitives;
- inspect light math and tiny code sketches for the core primitives;
- use the subject template;
- compare a draft against the spec pages;
- read primitive cards as quick references;
- inspect small examples that follow the same structure.

The v0.2 expansion adds derivative mechanics and extension components as
conditional layers. They are useful after the 9 core primitives are explicit.

## Stable Contract

The v0.1 Substrate contract is:

```text
graph
typed field
placement
state
action
constraint
evolution
readout
validation
```

Every complete Substrate subject must declare all 9 primitives explicitly.

## v0.2 Expansion

The v0.2 Substrate expansion adds two conditional tiers:

```text
core primitives
derivative mechanics
extension components
```

Derivative mechanics live in [derivatives/README.md](derivatives/README.md).
They include Action-Native Computation as the broad framing for computation as
constrained graph-state evolution, and cover units / dimensions, boundary,
source, local action / Lagrangian, variation, operator assembly, invariant,
residual / error estimator, Stationary Path, and solver selection.

Extension components live in [extensions/README.md](extensions/README.md). They
cover optional domain-triggered additions such as topological rigidity, exterior
placement, weak form, CellComplexView, Attractor Diagnostics, basis-mode
representation, metric placement, stochastic transition, information geometry,
gauge transport, sheaf consistency, port-Hamiltonian flow, causal intervention,
renormalization / coarse-graining, and differentiable backend.
The extension usage guides explain how to choose, combine, and review those
components without making them mandatory primitives.

## Ready Documents

The current ready set is:

- [README.md](README.md): short section entry.
- [INDEX.md](INDEX.md): full Substrate map.
- [concept.md](concept.md): master concept explanation.
- [primitives.md](primitives.md): full primitive guide.
- [primitive-implementation.md](primitive-implementation.md): primitive-level
  math and tiny code guide.
- [derivatives/README.md](derivatives/README.md): derivative mechanics entry.
- [derivatives/mechanics.md](derivatives/mechanics.md): derivative flow.
- [derivatives/action-native-computation.md](derivatives/action-native-computation.md):
  computation as constrained graph-state evolution.
- [derivatives/implementation.md](derivatives/implementation.md): derivative
  math and tiny pseudocode guide.
- [extensions/README.md](extensions/README.md): extension components entry.
- [extensions/registry.md](extensions/registry.md): extension registry.
- [extensions/topology-guide.md](extensions/topology-guide.md): topology
  meaning and extension choice guide.
- [extensions/decision-guide.md](extensions/decision-guide.md): extension
  choice guide.
- [extensions/composition-patterns.md](extensions/composition-patterns.md):
  common extension combinations.
- [extensions/walkthroughs.md](extensions/walkthroughs.md): prose walkthroughs
  for applying extensions after a complete core subject.
- [templates/README.md](templates/README.md): template entry.
- [templates/subject-template.md](templates/subject-template.md): copyable
  subject declaration form.
- [templates/walkthrough.md](templates/walkthrough.md): blank-to-filled
  template walkthrough.
- [spec/00-overview.md](spec/00-overview.md): complete subject contract.
- [spec/01-graph-field-placement-state.md](spec/01-graph-field-placement-state.md):
  descriptive primitive contract.
- [spec/02-action-constraint-evolution-readout-validation.md](spec/02-action-constraint-evolution-readout-validation.md):
  behavioral and result primitive contract.
- [spec/primitive-cards/README.md](spec/primitive-cards/README.md): primitive
  card index.
- [examples/README.md](examples/README.md): example index.

## Promotion Gate

A new Substrate subject is ready to move into examples, applications, or code
when it can answer:

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

If any answer is vague or only implied, the subject should stay in draft form.

## Not Claimed

Substrate does not claim a required SDK, package, schema, solver, product
design, or implementation style.

Future code can be added section-locally when it is tied to a stable document or
clear example.
