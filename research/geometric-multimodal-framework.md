# Geometric Multimodal Framework

## Purpose

This research page frames multimodal representation as a graph-shaped,
geometric, topological, and dynamical subject.

It is not a product architecture. It is a research direction for deciding which
Substrate declarations and extensions are needed when data cannot be treated as
flat vectors.

## Core thesis

Multimodal data is not only a point in a vector space.

For many subjects, data is better treated as:

```text
relational structure
+ metric placement
+ transformation behavior
+ local frame choices
+ topological support
+ dynamics
+ information state
```

The research claim is:

```text
meaning is the structure that remains coherent under valid transformations.
```

## Why flat vectors are not enough

Flat vector representations can work well when a task only needs similarity in
one feature space. They become brittle when the subject depends on:

- hierarchy;
- compositional semantics;
- transformations across views or modalities;
- relational reasoning;
- manifold continuity;
- scale transitions;
- topology;
- temporal evolution;
- uncertainty.

CGF should not reject vector embeddings. It should declare what the vectors
mean, where they live, what transformations preserve meaning, and what
validation checks are required.

## Research components

### Graph support

Multimodal subjects need a graph or graph-like support before geometry is
useful.

Examples:

- scene regions, objects, parts, and relations;
- text spans, entities, claims, and dependencies;
- sensor readings, tracks, and temporal transitions;
- domain entities and typed relations.

Substrate relation:

```text
graph + typed field + placement
```

### Metric placement

Some subjects need declared geometry:

- Euclidean placement for local measurements;
- hyperbolic placement for hierarchy or scale-free structure;
- spherical or angular placement for direction and phase;
- learned metric placement when the metric is part of the subject.

Metric placement should affect action, evolution, readout, or validation. If it
only affects display, it should not be promoted as a Substrate extension.

Substrate relation:

```text
metric placement extension
```

### Symmetry and transformation orbits

A concept may remain the same under valid transformations:

- rotation;
- scale;
- lighting;
- style;
- coordinate change;
- modality projection;
- temporal deformation.

Instead of treating a concept as one point, this research treats it as an orbit
or family under allowed transformations.

Substrate relation:

```text
typed field + constraint + validation
```

### Gauge transport

Different local views may use different frames, units, bases, coordinate
systems, or conventions.

Gauge transport is needed when values are not comparable until they are moved
into a compatible frame.

Substrate relation:

```text
gauge transport extension
```

### Topological support

Some subjects depend on loops, holes, cycles, higher-order relations, cell
structure, or persistent features across scale.

Topology should be declared only when it changes validation or readout.

Substrate relation:

```text
topological rigidity
higher-dimensional graph support
sheaf consistency
```

### Renormalization and abstraction

Multimodal representation often needs scale transitions:

```text
fine detail -> coarse structure -> stable concept
```

Coarse views are valid only when the preserved action, readout, or validation
relation is explicit.

Substrate relation:

```text
renormalization / coarse-graining extension
```

### Dynamics

Many multimodal subjects are not static:

- video;
- sensor streams;
- market regimes;
- biological processes;
- language generation;
- interaction traces.

State should evolve on declared graph support. If the next state is uncertain,
the subject may need stochastic transition and information geometry.

Substrate relation:

```text
state + evolution + readout + validation
stochastic transition extension
information geometry extension
```

## Alignment with current public work

Current public work supports a restrained framing:

- geometric deep learning provides the broad geometric unification lens;
- topological deep learning moves beyond ordinary graphs into topological
  domains such as hypergraphs, simplicial complexes, cell complexes, and
  combinatorial complexes;
- sheaf-based models show why local compatibility and transport matter;
- recent topological learning work also warns that topology does not
  automatically solve expressivity or validation limits.

CGF should use those ideas as research anchors, not as a claim that every
multimodal subject needs every extension.

## CGF mapping

| Research idea | CGF layer |
| --- | --- |
| Relational multimodal support | Substrate graph |
| Typed modality quantities | Substrate typed field |
| Where values live | Substrate placement |
| Geometry and hierarchy | Metric placement |
| Local frames and cross-view comparison | Gauge transport |
| Local-to-global agreement | Sheaf consistency |
| Loops, cells, persistence, or topological features | Topological rigidity and higher-dimensional support |
| Scale transition | Renormalization / coarse-graining |
| Belief, uncertainty, entropy, divergence | Information geometry |
| Time and state change | Evolution and stochastic transition |

## What not to claim

Do not claim that:

- every modality needs hyperbolic geometry;
- every transformation needs gauge transport;
- every graph should be lifted to a topological domain;
- topology is automatically more truthful than ordinary graph structure;
- a learned embedding is meaningful without declared metric, support, and
  validation;
- geometric language replaces domain evidence.

## Open questions

- Which multimodal subjects need ordinary graph support only?
- Which need metric placement before topology?
- Which topological features are stable enough to validate?
- When does a learned metric become part of the subject instead of an
  implementation detail?
- How should local-frame transport and sheaf consistency be taught without
  overloading core Substrate?
