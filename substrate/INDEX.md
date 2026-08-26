# Substrate Index

This index is the map for the Substrate section. Use it when you need to know
which document to read, what each document is responsible for, and what signal
to look for before declaring a Substrate subject complete.

Substrate has one active responsibility:

```text
Declare the graph-shaped computational subject using the 9 core primitives.
```

Those primitives are:

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

## What To Look For

When reading or writing any Substrate document, look for these signals:

- The subject is declared before any implementation style is chosen.
- All 9 core primitives are explicit, not implied.
- Every field has a type and a placement.
- State is separated from action, constraint, evolution, and readout.
- Validation explains how a result can fail, not only how it succeeds.
- Examples stay small enough that the primitive mapping is visible.

Avoid treating Substrate as an operating layer, product framework, solver, SDK,
or application architecture. Those choices can come later, after the subject is
clear.

## Reading Paths

Use this order if you are deciding which CGF pieces fit a project:

```text
../FOUNDATION_TRAVERSAL.md -> templates/subject-template.md
-> extensions/decision-guide.md -> ../research/connection-map.md
```

Use this order if you are new to the section:

```text
README.md -> concept.md -> primitives.md -> primitive-implementation.md
-> spec/00-overview.md -> examples/heat-relaxation.md
```

Use this order if you are declaring a new subject:

```text
primitives.md -> templates/subject-template.md -> templates/walkthrough.md
-> spec/00-overview.md -> spec/01-graph-field-placement-state.md
-> spec/02-action-constraint-evolution-readout-validation.md
-> primitive-implementation.md -> derivatives/README.md
-> extensions/README.md -> extensions/cards/README.md
-> extensions/decision-guide.md -> extensions/composition-patterns.md
-> extensions/walkthroughs.md -> examples/
```

Use this order if you are reviewing a contribution:

```text
status.md -> spec/00-overview.md -> spec/primitive-cards/ -> examples/README.md
```

## Root Documents

| Document | Purpose | What to look for |
| --- | --- | --- |
| [README.md](README.md) | The short Substrate landing page. | The layer definition, the 9 core primitives, and the main reading order. |
| [status.md](status.md) | The current v0.1 readiness marker. | The stable contract, ready document set, and promotion gate. |
| [concept.md](concept.md) | The master explanation of what Substrate is. | The plain-language contract, why graph alone is not enough, and the boundary with other CGF layers. |
| [primitives.md](primitives.md) | The full teaching guide for the 9 core primitives. | Definition, question, minimum declaration, heat example, mistakes, and related primitives for each core primitive. |
| [primitive-implementation.md](primitive-implementation.md) | Light math and tiny code sketches for the core primitives. | How the heat relaxation subject maps to minimal representations, checks, and illustrative snippets. |
| [vision.md](vision.md) | The public reason Substrate exists. | The promise of a shared declaration layer and the limits of what Substrate should claim. |
| [research-notes.md](research-notes.md) | Self-contained exploratory notes growing from Substrate. | Questions that are not ready for the spec but still belong to CGF. |

## Derivative Mechanics

Derivative mechanics are the v0.2 layer for making a complete Substrate subject
more formal, computable, or method-ready. They do not replace the 9 core
primitives.

| Document | Purpose | What to look for |
| --- | --- | --- |
| [derivatives/README.md](derivatives/README.md) | Entry point for derivative mechanics. | The rule that derivative mechanics require a complete core subject first. |
| [derivatives/mechanics.md](derivatives/mechanics.md) | Overview of the derivative flow. | How units, boundaries, sources, local action, variation, operator assembly, invariants, residuals, and solver selection fit together. |
| [derivatives/action-native-computation.md](derivatives/action-native-computation.md) | Frames computation as constrained graph-state evolution. | Whether action, law, constraints, evolution, residual, and validation visibly support the readout. |
| [derivatives/implementation.md](derivatives/implementation.md) | Light math and tiny pseudocode for derivative mechanics. | How the heat relaxation subject becomes more formal and method-ready. |
| [derivatives/cards/README.md](derivatives/cards/README.md) | Index of derivative cards. | The standard card format for conditional mechanics. |

## Extension Components

Extension components are the v0.2 layer for optional domain-triggered structure.
They are not mandatory primitives.

| Document | Purpose | What to look for |
| --- | --- | --- |
| [extensions/README.md](extensions/README.md) | Entry point for Substrate extensions. | The rule that extensions solve specific modeling failure modes. |
| [extensions/registry.md](extensions/registry.md) | Registry of current extension components. | The named extension set and maturity labels. |
| [extensions/topology-guide.md](extensions/topology-guide.md) | Guide to topology meanings in CGF. | Whether graph topology, higher-dimensional topology, topological rigidity, or application graph topology is meant. |
| [extensions/cards/README.md](extensions/cards/README.md) | Index of extension cards. | The standard card format for optional components. |
| [extensions/decision-guide.md](extensions/decision-guide.md) | Usage guide for choosing extensions. | The extension gate, decision table, and required/optional/wrong distinction. |
| [extensions/composition-patterns.md](extensions/composition-patterns.md) | Guide for combining extensions. | Common extension clusters and how each combination affects validation. |
| [extensions/walkthroughs.md](extensions/walkthroughs.md) | Short prose walkthroughs for extension use. | How extensions are added only after a complete 9-core subject exists. |
| [../research/connection-map.md](../research/connection-map.md) | Cross-layer connection map. | Which extension cards have deeper studies, Labs evals, and scoped result claims. |

## Templates

Templates are the drafting layer. Use them when you want to declare a new
subject before rewriting it as a polished example, application note, or code
example.

| Document | Purpose | What to look for |
| --- | --- | --- |
| [templates/README.md](templates/README.md) | Explains how Substrate templates should be used. | The rule that all 9 primitives must be explicit before promotion. |
| [templates/subject-template.md](templates/subject-template.md) | A copyable form for declaring a complete Substrate subject. | The 9 primitive sections, fill-in prompts, minimum standards, and final checklist. |
| [templates/walkthrough.md](templates/walkthrough.md) | Shows a blank-to-filled pass through the subject template. | How each primitive decision becomes a complete heat relaxation declaration. |

## Spec Documents

The spec is the contract layer. Use it when a Substrate subject needs to be
reviewed, stabilized, or reused by examples and future code.

| Document | Purpose | What to look for |
| --- | --- | --- |
| [spec/00-overview.md](spec/00-overview.md) | Defines a complete Substrate subject. | The requirement that all 9 core primitives are declared and the completion checklist. |
| [spec/01-graph-field-placement-state.md](spec/01-graph-field-placement-state.md) | Contract for descriptive primitives. | Required declarations for graph, typed field, placement, and state. |
| [spec/02-action-constraint-evolution-readout-validation.md](spec/02-action-constraint-evolution-readout-validation.md) | Contract for behavioral and result primitives. | Required declarations for action, constraint, evolution, readout, and validation. |

## Primitive Cards

Primitive cards are the quick-reference layer. Use them when you need a compact
definition for one primitive without rereading the full guide.

| Card | Summary |
| --- | --- |
| [spec/primitive-cards/README.md](spec/primitive-cards/README.md) | Explains the card format and links all 9 core cards. |
| [spec/primitive-cards/graph.md](spec/primitive-cards/graph.md) | Defines the entities and relationships that carry the subject. |
| [spec/primitive-cards/typed-field.md](spec/primitive-cards/typed-field.md) | Defines the named, typed quantities that live on the graph. |
| [spec/primitive-cards/placement.md](spec/primitive-cards/placement.md) | Defines where each field is allowed to live. |
| [spec/primitive-cards/state.md](spec/primitive-cards/state.md) | Defines the current values of declared fields. |
| [spec/primitive-cards/action.md](spec/primitive-cards/action.md) | Defines the action, cost, law, or objective that governs the subject. |
| [spec/primitive-cards/constraint.md](spec/primitive-cards/constraint.md) | Defines what states, transitions, or results are not allowed. |
| [spec/primitive-cards/evolution.md](spec/primitive-cards/evolution.md) | Defines how state changes over time, steps, events, or iterations. |
| [spec/primitive-cards/readout.md](spec/primitive-cards/readout.md) | Defines the answer extracted from the subject. |
| [spec/primitive-cards/validation.md](spec/primitive-cards/validation.md) | Defines the checks that decide whether a result should be trusted. |

## Examples

Examples are small prose declarations. They show how the same 9 primitives apply
across different domains before any code structure is required.

| Example | Summary | What to look for |
| --- | --- | --- |
| [examples/README.md](examples/README.md) | Lists the current Substrate examples. | The expectation that every example uses the same 9-section mapping. |
| [examples/heat-relaxation.md](examples/heat-relaxation.md) | A minimal physical relaxation subject. | The clearest first pass through all 9 primitives. |
| [examples/graph-optimization.md](examples/graph-optimization.md) | A subject for improving graph assignments under constraints. | How action and constraint shape an optimization subject without choosing a solver. |
| [examples/anomaly-scoring.md](examples/anomaly-scoring.md) | A subject for scoring unusual graph-local behavior. | How readout and validation keep scores tied to declared state. |
| [examples/ecommerce-checkout.md](examples/ecommerce-checkout.md) | A checkout subject declared as cart, inventory, payment, order, shipment, and notification dependencies. | How a product workflow can be described as a Substrate subject without operational machinery. |

## Completion Review

A Substrate subject is ready to leave this layer when it can answer:

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

If any answer is missing, the subject should stay in Substrate until the
declaration is clearer.

After the core subject is complete, use derivative mechanics when it needs
formal computational structure and extension components when a domain-specific
failure mode needs an explicit name.
