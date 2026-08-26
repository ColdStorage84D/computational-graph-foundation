# Typed Multimodal Graph Framework

## Purpose

Use this framework when a case is made of heterogeneous parts such as images,
regions, questions, options, documents, sensor frames, entities, or concepts.

## Reusable Concept

Represent each item as a typed graph with domain-supplied node and edge types.
Labels and supervision are marked separately from feature-bearing nodes so
training-only information cannot leak into inference.

The typed multimodal graph is a strong base for Granular Analysis because one
input can expose many analysis surfaces: image regions, text, measurements,
metadata, source quality, priors, or task context.

The graph should hold typed parts and relations, not one undifferentiated
feature row:

```text
case
image / document / sensor / record node
region / span / frame / component node
measurement / metadata / quality node
candidate or review node, when later derived
training-only label, kept out of feature paths
```

## Minimum Declaration

A typed multimodal graph should declare:

```text
graph id
node types
edge types
field names and field types
evidence refs for sourced nodes
training-only labels or later-derived labels
feature-bearing nodes
non-feature nodes
export or replay identity, when used
```

This makes leakage and replay reviewable before any model, processor, or
runtime is chosen.

## Uses CGF Pieces

- Substrate graph, typed field, placement, state, readout, and validation;
- Architecture graph/path views;
- Granular Analysis;
- feature nodes;
- label boundaries;
- deterministic export and replay checks.

## Example Applications

- medical image analysis review;
- visual question answering;
- document analysis;
- sensor fusion;
- product catalog reasoning;
- multimodal education tools.

## When To Use

- A single item has several evidence surfaces.
- Relations between parts matter.
- Labels exist during training or evaluation but must not become inference
  features.
- Deterministic export and reload matter.
- One input will feed Granular Analysis through many lens or processor
  branches.

## When Not To Use

- The subject is already a simple single-field graph.
- The project does not need multimodal parts or leakage separation.
- A table is enough and relationships do not matter.

## Boundary

The typed multimodal graph is a container and contract. It does not decide
which processor, model, route, or reviewer should be trusted.

It also does not require all modalities to be present. Missing, unavailable, or
failed modalities should remain explicit graph or record state.

## Implementation Posture

Code can be added section-locally later when a CGF-native contract is stable.
No mandatory multimodal package is implied.
