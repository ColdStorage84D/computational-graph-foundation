# Substrate Research Map

## Purpose

This page maps the Substrate-owned research threads in CGF language.

It is not the Substrate spec. It is the research map behind the current
Substrate docs.

## Core Research Claim

Substrate is the CGF layer for declaring graph-shaped computational subjects.

The stable public contract uses 9 core primitives:

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

Research then asks what extra mechanics or extension components are needed
when that declaration must become a precise computation.

## Extracted Threads

### 1. Subject Declaration

The first research thread is the declaration of a computational subject.

CGF keeps this as the stable core:

```text
graph + typed fields + placement + state
+ action + constraints + evolution + readout + validation
```

This thread belongs to Substrate core docs and examples.

### 2. Action-Derived Computation

The second research thread is the path from action to computation.

The central idea is:

```text
declared subject
  -> action or local law
  -> allowed variation or update rule
  -> operator, residual, or evolution step
  -> readout
  -> validation
```

This thread belongs to Substrate derivative mechanics, not to the core
primitive list.

### 3. Derivative Mechanics

Derivative mechanics are conditional declarations that make a subject more
formal, testable, or implementable.

Current mechanics:

- units / dimensions;
- boundary;
- source;
- local action / Lagrangian;
- variation;
- operator assembly;
- invariant;
- residual / error estimator;
- solver selection.

These are not mandatory core primitives. They become relevant when the subject
needs equations, operators, solver choice, trust checks, or a clearer bridge to
implementation.

### 4. Geometric And Discrete Placement

Some subjects need more than node-only state.

This research thread covers:

- placement on nodes, edges, faces, cells, or modes;
- CellComplexView as the narrowed public extension for cells, boundaries,
  regions, surfaces, and episode-shaped support;
- higher-dimensional graph support with oriented cell boundaries;
- topological domains such as hypergraphs, simplicial complexes, cell
  complexes, and combinatorial complexes;
- graph discretization of continuous domains;
- exterior placement for conservation-heavy subjects;
- weak-form support when pointwise equations are too brittle.

This belongs mostly to extension and derivative research.

### 5. Extension Components

Extension components name domain-triggered gaps that the core primitives can
point to but not fully express.

Current extension tracks include:

- topological rigidity;
- CellComplexView;
- Attractor Diagnostics;
- basis-mode representation;
- higher-dimensional / topological-domain support;
- exterior placement;
- weak form;
- metric placement;
- stochastic transition;
- information geometry;
- gauge transport;
- sheaf consistency;
- port-Hamiltonian flow;
- causal intervention;
- renormalization / coarse-graining;
- differentiable backend.

Each extension must state its parent layer, problem solved, minimum substrate
shape, when to use it, when not to use it, and maturity.

### 6. Application-Class Pressure Tests

Application-class research asks whether the same Substrate shape can describe
very different problem families.

Current pressure-test families include:

- basis-mode representation;
- field-theoretic graph subjects;
- operator learning;
- physical computation;
- ecommerce checkout;
- graph optimization;
- anomaly scoring.

Application-class material is useful only when it clarifies the common
Substrate declaration or exposes a precise extension gap.

### 7. Honest Limits

CGF should avoid claiming that Substrate replaces every solver, graph library,
physics engine, database, or machine-learning framework.

The research posture is:

```text
Use Substrate to declare the subject clearly.
Use derivative mechanics when computation must be derived.
Use extensions only when the domain exposes a real gap.
Use existing tools when they are the right implementation target.
```

## What Moves Into Public Substrate

The public Substrate section should receive only:

- clear definitions;
- small examples;
- reusable primitive vocabulary;
- derivative mechanics that explain computation;
- extension cards with maturity labels;
- validation checks;
- implementation notes tied to stable docs.

## What Stays In Research

Research keeps:

- broad theory;
- literature references;
- unpublished drafts;
- speculative synthesis;
- novelty and claim boundaries;
- unresolved questions;
- CGF-local eval links and claim boundaries.

## Reference Needs

Before this research is promoted into stronger public claims, the public
reference pass must cover:

- spectral methods and basis-mode representations;
- graph Laplacians and spectral graph theory;
- action principles and variational calculus;
- weak forms and discretization methods;
- discrete exterior calculus and exterior placement;
- cell complexes and Hodge-style operators;
- sheaf theory;
- gauge transport;
- information geometry;
- stochastic processes and Bayesian filtering;
- causal inference;
- port-Hamiltonian systems;
- renormalization and coarse-graining;
- operator learning.

The current page is a research map, not a bibliography.

## Related Research Pages

- [coverage-map.md](coverage-map.md): layer ownership and maturity map for CGF
  research.
- [geometric-multimodal-framework.md](geometric-multimodal-framework.md):
  research direction for geometric and physics-inspired multimodal structure.
- [higher-dimensional-graphs.md](higher-dimensional-graphs.md): research
  direction for cell-based, topological, and higher-order graph support.
- [derivative-mechanics-study.md](derivative-mechanics-study.md): deeper
  research behind the v0.2 derivative mechanics.
- [extension-studies/README.md](extension-studies/README.md): deeper studies
  behind optional Substrate extension components.
- [application-class-studies.md](application-class-studies.md): pressure-test
  families that show where Substrate, derivatives, and extensions need more
  work.
