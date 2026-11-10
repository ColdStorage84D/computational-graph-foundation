# Higher-Dimensional Topology

## Purpose

Higher-dimensional topology studies when a graph subject needs cells,
boundaries, and higher-order relations instead of only nodes and edges.

The extension exists because some computational objects are naturally bounded
paths, surfaces, volumes, cycles, or higher-order interactions.

## Failure Mode

Node-edge graphs can hide structure that is essential to validation:

- a loop is treated as repeated edges instead of a closed object;
- an evidence chain has no explicit boundary;
- a surface interaction is flattened into pairwise edges;
- circulation, flux, or higher-order consistency cannot be checked;
- readout misses whether a higher-order object was valid or orphaned.

## Minimum Substrate Addition

The extension adds a higher-dimensional support view:

```text
cellular_view
  support_scope
  max_dimension
  cells_by_dimension
  boundary_maps
  evidence_refs
  confidence
  uncertainty
```

Minimum cell record:

```text
cell
  cell_id
  dimension
  kind
  boundary_cell_ids
  boundary_signs
  support_refs
  evidence_refs
  confidence
  uncertainty
```

The core invariant is:

```text
boundary(boundary(cell)) = 0
```

## Cell Dimensions

| Dimension | Substrate meaning |
| --- | --- |
| 0-cell | Individual object, state point, sample, entity, or anchor. |
| 1-cell | Typed transition, relation, edge, or interval. |
| 2-cell | Bounded path, cycle, surface, comparison region, or local patch. |
| 3-cell | Volume, episode-like region, or higher-order aggregate with a boundary. |

The exact interpretation belongs to the subject. The extension only requires
that boundaries and supports are explicit.

## Operators And Checks

Useful conceptual operators include:

- lift selected paths or cycles into cells;
- build a signed boundary matrix;
- build Hodge-style operators over a chosen dimension;
- detect cycles or orphaned cells;
- pass messages across boundary and coboundary adjacency;
- score boundary consistency and cell uncertainty.

These are operator ideas, not mandatory APIs.

## Relationship To Nearby Extensions

- Exterior placement decides which quantities live on cells of each dimension.
- Weak form can use cells and basis functions to express integral laws.
- Sheaf consistency can compare local views on shared boundaries.
- Topological rigidity can use cycles and cells as support for invariant
  checks.
- Metric placement can add geometry to the higher-dimensional support.

## Validation Questions

- Does every cell have a declared boundary?
- Are boundary signs preserved when orientation matters?
- Does boundary-of-boundary vanish for valid cells?
- Are orphaned or unsupported cells detected?
- Does readout distinguish graph facts from higher-dimensional derived views?
- Is the higher-dimensional structure actually needed by the subject?

## Maturity

Status: active research.

The conceptual boundary model is strong enough for research pages and future
examples. It needs narrower examples before becoming a dedicated extension
card beyond the existing topological and placement cards.

## References

Public sources for computation on domains above graphs.

- [Topological Deep Learning: Going Beyond Graph Data](https://arxiv.org/abs/2206.00606), Hajij et al. (2022). Simplicial, cell, and combinatorial complexes as domains for computation.
- [Hodge Laplacians on Graphs](https://doi.org/10.1137/18M1223101), Lim (2020). Hodge Laplacians and higher-order boundary structure on graphs.
- [Weisfeiler and Lehman Go Cellular: CW Networks](https://arxiv.org/abs/2106.12575), Bodnar et al. (2021). A worked lifting from graphs to cell complexes.
