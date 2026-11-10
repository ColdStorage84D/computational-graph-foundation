# Geometric Discretization

## Purpose

Geometric discretization studies how a continuous domain becomes a graph-shaped
Substrate subject.

The extension exists because a field must become graph data before CGF can
simulate it, optimize it, learn from it, or validate it. The discretization
choice decides which quantities and invariants survive.

## Failure Mode

A plain graph can look valid while hiding the geometric choices that determine
the computation.

Common failures:

- conservation is lost because all quantities are forced onto nodes;
- intrinsic geometry is replaced by arbitrary adjacency;
- sampling hides boundary layers or localized high variation;
- learned operators appear to transfer, but only across one hidden
  discretization;
- validation cannot tell whether error came from the subject or the
  discretization.

## Minimum Substrate Addition

The extension adds a declared discrete problem:

```text
continuous domain + field requirements
  -> sampling strategy
  -> placement choice
  -> operator choice
  -> discrete problem
  -> Substrate subject
```

Minimum record:

```text
discrete_problem
  graph
  field_types
  placements
  measures_or_weights
  boundary_sets
  source_slots
  operator_basis
  invariant_metadata
```

## DiscreteProblem Contract

Geometric discretization should produce a declared `DiscreteProblem`, not a
hidden preprocessing artifact and not a separate simulator.

The purpose of `DiscreteProblem` is to explain how a continuous, geometric, or
field-like subject became a graph-shaped Substrate subject.

Minimum contract:

```text
DiscreteProblem
  domain_kind
  sampling_strategy
  graph
  field_types
  placements
  measures_or_weights
  boundary_sets
  source_slots
  operator_family
  operator_assembly_metadata
  invariant_metadata
  mismatch_warnings
```

The downstream subject should build its action, residual, learned operator,
evolution, and readout from this declared problem instead of from an
unannotated graph.

`DiscreteProblem` is backend-neutral. It can later feed finite-volume code,
finite-element code, graph operators, differentiable operators, or learned
surrogates, but it is not itself a solver or SDK.

## Sampling Strategies

| Strategy | Use when | Main risk |
| --- | --- | --- |
| Uniform grid | Domain and resolution are simple. | Wasteful in high dimension. |
| Unstructured mesh | Curved geometry or boundaries matter. | Mesh quality controls trust. |
| Quadtree / octree | Multi-scale refinement matters. | Operators become more complex. |
| k-nearest neighbor point cloud | Samples come from data. | Geometric guarantees are weaker. |
| Field-driven adaptive sampling | Local sharp variation matters. | Needs an error indicator. |
| Spherical or radial shells | Source-centered structure dominates. | Weak for non-centered geometry. |
| Surface-wrapped shells | Boundary layers near a surface matter. | Needs normal-frame metadata. |
| Basis-mode graph | Symmetry gives a useful eigenbasis. | Needs a truncation policy. |

## Operator Choices

| Operator family | Best preserves | Use when | Avoid when |
| --- | --- | --- | --- |
| Graph Laplacian | Smoothness on an abstract graph | Exploratory graph diffusion or rough relational data. | Metric geometry, conservation, or physical flux fidelity is required. |
| Cotangent Laplacian | Intrinsic surface geometry | Triangle meshes and surface diffusion. | Mesh quality is poor or the topology changes frequently. |
| Discrete exterior calculus | Differential-form structure | Flux, curl, circulation, and Stokes-style constraints. | The field is not naturally a form or the support has no orientation. |
| Finite volume | Local conservation | Heat, mass, fluid, and transport balances. | Basis accuracy matters more than local conservation. |
| Finite element | Weak-form accuracy | Complex domains and basis-driven PDEs. | A tiny graph-first model is enough and assembled elements add noise. |
| Spectral / basis operator | Symmetry and modal compression | Periodic, spherical, cylindrical, or eigenbasis subjects. | Discontinuities, shocks, or local contacts dominate the result. |

The wrong operator can produce stable-looking output while drifting the
quantity the subject actually cares about. The operator choice should therefore
be explicit in validation and readout.

## Exterior Placement Map

Geometric discretization should place each quantity on the support where it is
valid.

| Quantity | Natural placement |
| --- | --- |
| Scalar potential or local entity state | Node |
| Flow, current, gradient, transition, or relation | Edge |
| Flux, curl, circulation, or surface constraint | Face |
| Mass, charge, volume density, or conserved amount | Cell or volume |
| Harmonic, spectral, or modal coefficient | Mode or mode bundle |

Forcing every quantity onto nodes can hide conservation, flux, boundary, or
modal structure. Exterior placement and weak form are often the first
extensions to check when this failure appears.

## Relationship To Nearby Extensions

- Exterior placement states where quantities live across nodes, edges, faces,
  cells, or modes.
- Weak form handles subjects where pointwise equations are brittle.
- Metric placement adds distance geometry after graph construction.
- Topological rigidity protects cycles or phase-like structure that sampling
  and embedding may collapse.
- Differentiable backend can execute learned or inverse-design versions later.

## Setup Recipe

Use this recipe when the original subject is continuous, geometric, spatial, or
field-like rather than already graph-shaped:

1. Define the domain: point set, curve, surface, volume, manifold, metric
   space, or mode space.
2. Choose the invariant or structure that must survive: conservation, symmetry,
   intrinsic distance, topology, smoothness, flux, boundary behavior, or modal
   sparsity.
3. Pick the sampling strategy, placement map, and operator family that best
   preserve that structure.
4. Build the graph with node, edge, face, cell, region, or mode metadata as
   required by the placement choice.
5. Return a `DiscreteProblem` with measures, boundary sets, source slots,
   operator assembly metadata, invariant metadata, and mismatch warnings.
6. Build the subject's action, constraint, residual, learned operator,
   evolution, and readout from the `DiscreteProblem`.
7. Document which invariant the discretization preserves and which known
   failures remain warnings or hard errors.

## Validation Questions

- Is the graph a faithful support for the declared field?
- Are measures or weights explicit where integration is needed?
- Are boundary sets and source slots declared?
- Does the operator family preserve the invariant the subject cares about?
- Are known mismatch cases warnings or hard errors?
- Can readout state which discretization was used?
- Can a reviewer tell whether error came from the subject, the discretization,
  or the downstream operator?

## Maturity

Status: research-supported.

The decision tables are useful now. Formal schemas and implementation examples
belong in later section-local code.

## Future Implementation Target

A later section-local recipe set may accept a geometry or field description,
sampling choice, placement choice, operator family, and required invariants,
then return a `DiscreteProblem` plus warnings.

That future code should remain optional and section-local. It should not become
a top-level SDK or a mandatory CGF package.

## References

Public sources for placing quantities on discrete structures and for weak formulations.

- [Discrete Exterior Calculus](https://arxiv.org/abs/math/0508341), Desbrun, Hirani, Leok, and Marsden (2005). Placing quantities on nodes, edges, faces, and volumes so that conservation survives discretization.
- [Finite element exterior calculus: from Hodge theory to numerical stability](https://arxiv.org/abs/0906.4325), Arnold, Falk, and Winther (2009). Weak formulations and the conditions under which their discretizations are stable.
