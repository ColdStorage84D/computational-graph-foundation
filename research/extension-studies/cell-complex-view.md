# CellComplexView

## Purpose

CellComplexView studies when a graph-shaped subject needs higher-order support:
not only nodes and edges, but cells, boundaries, regions, surfaces, cycles, and
aggregate support.

Core pattern:

```text
graph support
  -> cells with dimension
  -> boundary relation
  -> fields placed on cells or boundaries
  -> boundary consistency and cell readout
```

## Failure Mode

Some subjects lose meaning when every relation is flattened to edges:

- a closed path should be treated as a boundary of a region;
- a surface or aggregate support carries the field being validated;
- a higher-order interaction cannot be reduced to pairwise edges without
  losing the check;
- boundary inconsistency is hidden by a node-level score.

## Minimum Substrate Addition

```text
cell
  cell_id
  dimension
  support_refs
  boundary_refs
  orientation_or_sign_when_needed
  field_refs
```

The subject must state which action, constraint, readout, or validation uses
the cell view.

## Conceptual Checks

- `C0` cells correspond to point-like support.
- `C1` cells correspond to edge-like support.
- `C2` cells can represent regions, surfaces, or closed path support.
- Higher cells remain optional and must justify their role.
- Boundary records resolve to declared lower-dimensional cells.
- Boundary consistency is visible.

## Relationship To Nearby Extensions

- Higher-dimensional topology studies the broader theory behind cell support.
- Topological rigidity protects selected structures from collapse.
- Weak form can test aggregate residuals over cell support.
- Exterior placement can declare conditions outside the cell support.
- Sheaf consistency can compare local cell views over overlaps.

## Validation Questions

- Which structure cannot be represented by ordinary graph edges?
- Which cell dimensions are actually needed?
- Are boundary references declared and checkable?
- What readout changes if cells are removed?
- Does the cell view add validation, or only vocabulary?

## Maturity

Status: research-supported; CGF-local eval `contract-pass`.

See [../../labs/evals/cell-complex-view/results.md](../../labs/evals/cell-complex-view/results.md).
