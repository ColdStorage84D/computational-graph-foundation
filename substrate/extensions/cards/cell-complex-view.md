# CellComplexView

## Definition

CellComplexView declares higher-order support over a graph using cells, their
dimensions, boundaries, and validation checks.

## Parent layer

Substrate.

## Problem solved

Ordinary nodes and edges can hide surfaces, closed boundaries, higher-order
relations, and episode-like support that matter to the subject's action,
readout, or validation.

## Minimum substrate shape

- Complete 9-core subject.
- Cell records with stable ids and dimensions.
- Boundary references from each cell to lower-dimensional support.
- Typed fields placed on cells or boundaries.
- Action, constraint, readout, or validation that uses the cell structure.

## When to use

- A path, loop, surface, volume, region, or higher-order relation is part of
  the subject.
- Boundary consistency matters.
- Evidence should be checked over cells rather than only over node or edge
  support.
- A graph view needs explicit support for cycles, regions, surfaces, or
  episode-shaped structure.

## When not to use

- Nodes and edges already express the subject completely.
- Higher-order cells would only decorate the graph without changing validation.
- The boundary relation cannot be declared or checked.
- A product workflow or operating trace is being modeled; that belongs outside
  Substrate unless it is being declared as the computational subject itself.

## Maturity

Research extension with CGF-local tiny eval `contract-pass`.

## Validation checks

- Every boundary reference resolves to declared lower-dimensional support.
- A valid closed boundary satisfies the declared boundary consistency rule.
- Fields placed on cells do not silently move to unrelated graph support.
- Readout states whether it uses nodes, edges, cells, boundaries, or aggregate
  cell support.

## Failure modes

- Treating a cycle or surface as a visual annotation instead of declared
  support.
- Adding cells without boundary records.
- Letting a cell view override the 9-core subject declaration.
- Hiding boundary inconsistency inside a successful aggregate score.
