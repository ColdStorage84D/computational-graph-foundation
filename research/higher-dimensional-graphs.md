# Higher-Dimensional Graphs

## Purpose

This page defines higher-dimensional graphs as a CGF research direction.

The goal is to represent subjects whose meaningful structure is not only nodes
and edges, but also higher-order relations, faces, volumes, boundaries, loops,
fluxes, and cell-supported signals.

## Short definition

A higher-dimensional graph is a cell-based relational structure with signals on
vertices, edges, faces, volumes, and higher cells, connected by oriented
boundary maps.

## Why ordinary graphs are limited

An ordinary graph represents:

```text
vertices + edges
```

This is enough for pairwise relations. It is not enough when the subject needs:

- group interactions;
- loops;
- faces;
- surfaces;
- volumes;
- cavities;
- flux;
- circulation;
- divergence;
- conservation laws;
- higher-order message passing;
- topological summaries.

## Topological domain choices

Different higher-dimensional supports solve different problems.

| Domain | Use when |
| --- | --- |
| Graph | Pairwise relations are enough. |
| Hypergraph | Group membership matters more than geometry. |
| Simplicial complex | Triangles, tetrahedra, closure rules, and topology matter. |
| Cell complex | General faces, volumes, mixed cells, and engineering meshes matter. |
| Combinatorial complex | Flexible higher-order relations and topological-domain learning matter. |
| Sheaf over support | Local assignments need restriction maps and consistency checks. |

The choice is part of the Substrate declaration. It should not be hidden inside
an implementation.

## Cell dimensions

```text
0-cells = vertices / points / nodes
1-cells = edges / links / directed relations
2-cells = faces / polygons / surfaces
3-cells = volumes / regions / cells
k-cells = higher-dimensional support
```

Signals may live on any dimension:

| Signal | Natural support |
| --- | --- |
| pressure or potential | node or volume |
| directed flow or current | edge |
| flux or circulation | face |
| mass, density, energy | volume |
| group state | hyperedge or higher cell |

This is the key Substrate idea: fields should live where their meaning belongs.

## Orientation and boundary maps

Higher-dimensional subjects often need orientation.

Examples:

```text
boundary(edge) = end vertex - start vertex
boundary(face) = signed sum of boundary edges
boundary(volume) = signed sum of boundary faces
```

Boundary maps connect dimensions:

```text
C0 <- B1 <- C1 <- B2 <- C2 <- B3 <- C3
```

The core consistency rule is:

```text
boundary of boundary = 0
```

This matters for conservation, circulation, flux, and topology-aware
validation.

## Hodge-style structure

The Hodge Laplacian generalizes graph Laplacian behavior to signals on higher
cell dimensions.

For edge signals, a Hodge-style operator separates:

```text
gradient-like behavior
curl-like behavior
harmonic / loop behavior
```

This makes higher-dimensional support useful for:

- flow fields;
- electrical networks;
- mesh-based simulation;
- molecular rings and cavities;
- circulation and divergence checks;
- topology-aware smoothing.

## Relationship to Substrate

Higher-dimensional graphs affect several Substrate pieces:

| CGF piece | Effect |
| --- | --- |
| Graph | Support may include cells, not only nodes and edges. |
| Typed field | Fields can live on vertices, edges, faces, volumes, or higher cells. |
| Placement | Placement must name the cell dimension and valid support. |
| State | State may be split by dimension. |
| Action | Action can include boundary, coboundary, flux, circulation, or conservation terms. |
| Constraint | Closure, orientation, and conservation conditions become admissibility checks. |
| Evolution | Updates may move information across boundary and coboundary relations. |
| Readout | Answers may include loops, cavities, fluxes, divergence, or cell-level summaries. |
| Validation | Boundary consistency, Hodge-style decomposition, and topology stability can be checked. |

## Relationship to extensions

Higher-dimensional support interacts with existing extensions:

- topological rigidity protects declared topological features from invalid
  collapse or smoothing;
- weak form supports aggregate laws over cells or regions;
- exterior placement declares boundary-side or environment-side quantities;
- sheaf consistency checks local assignments over overlapping support;
- gauge transport keeps cell signals comparable across frames;
- renormalization / coarse-graining relates fine and coarse cell structures.

## Current topology expectation

Topology in CGF should be based on current topological learning practice:

- treat topology as declared support and validation structure, not a magic
  feature;
- distinguish graphs, hypergraphs, simplicial complexes, cell complexes, and
  combinatorial complexes;
- make topological liftings explicit when graph data is moved to a richer
  domain;
- validate which features are preserved, lost, or unstable;
- keep expressivity limits visible.

Topological rigidity should therefore protect declared topological structure.
It should not merely add a cycle score or preserve a visually interesting loop.

## When to use

Use higher-dimensional graph support when:

- fields naturally live on edges, faces, volumes, or groups;
- loops, holes, cavities, or boundaries matter;
- conservation, flux, curl, or divergence is part of validation;
- a higher-order interaction cannot be represented honestly as pairwise edges;
- readout depends on topological or geometric structure.

## When not to use

Do not use higher-dimensional support when:

- pairwise graph structure is enough;
- topology does not affect validation or readout;
- the higher-dimensional lift cannot be justified;
- the added structure only makes the subject harder to inspect;
- a simpler graph declaration gives the same trusted result.

## Promotion path

This research can become public Substrate material only when it has:

- a clear minimum declaration for higher-dimensional support;
- one or more small examples;
- validation checks for boundary, placement, and topology;
- a decision guide for choosing graph, hypergraph, simplicial, cell, or
  combinatorial support;
- no dependency on a specific implementation.
