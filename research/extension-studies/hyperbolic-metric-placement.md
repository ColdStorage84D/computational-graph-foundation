# Hyperbolic Metric Placement

## Purpose

Hyperbolic metric placement studies negative-curvature geometry as an optional
placement for graph objects with hierarchical, tree-like, scale-free, or
branching structure.

The extension does not replace the graph. It adds a metric field over selected
graph objects so distance, abstraction depth, sibling separation, and path
coherence can be measured.

## Failure Mode

Flat embeddings can crowd hierarchical structure.

Common failures:

- many specialized leaves collapse into one region;
- hierarchy depth is not visible in distance;
- sibling branches overlap;
- abstraction and specialization are not distinguishable;
- a learned coordinate becomes trusted without geometry validity checks.

## Minimum Substrate Addition

Minimum record:

```text
metric_placement
  metric_model
  curvature
  coordinates
  placement_version
  evidence_refs
  geometry_confidence
  geometry_uncertainty
  valid_context
```

For a Poincare-ball-style placement:

```text
||coordinates|| < 1 - epsilon
```

Projection back into the valid ball is a geometry guard, not a claim that the
placement is correct.

## Interpretation

| Quantity | Substrate meaning |
| --- | --- |
| Radius near center | General, root-like, abstract, reusable state. |
| Radius near boundary | Specific, leaf-like, narrow state. |
| Angle | Branch, sibling family, topic, or route family. |
| Geodesic distance | Hierarchy-aware dissimilarity. |
| Outward movement | Specialization or refinement. |
| Inward movement | Generalization or summary. |

## Relationship To Nearby Extensions

- Metric placement supplies distance geometry.
- Gauge transport supplies frame changes.
- Topological rigidity protects cycles and phase-like structure.
- Renormalization / coarse-graining can summarize metric neighborhoods.
- Sheaf consistency can compare local metric views on overlaps.

## Validation Questions

- Why is ordinary graph distance not enough?
- What graph objects receive metric placement?
- Is the metric model declared?
- Are coordinates inside the valid region?
- Are confidence and uncertainty explicit?
- Does readout say how metric distance influenced the answer?

## Maturity

Status: research-supported; CGF-local eval `contract-pass`.

The extension is ready as metric-placement research. More examples are needed
before CGF should recommend one metric model as a default.

## CGF Eval Result

See [../../labs/evals/hyperbolic-placement/results.md](../../labs/evals/hyperbolic-placement/results.md).

## References

Public sources for placing hierarchies in hyperbolic space. The comparison in the eval follows the construction idea in Sarkar: match radial growth to the branching factor.

- [Low Distortion Delaunay Embedding of Trees in Hyperbolic Plane](https://doi.org/10.1007/978-3-642-25878-7_34), Sarkar (2012). A constructive embedding of trees in the hyperbolic plane with distortion as close to one as desired.
- [Poincare Embeddings for Learning Hierarchical Representations](https://arxiv.org/abs/1705.08039), Nickel and Kiela (2017). Hierarchies embedded in the Poincare ball, and the distance formula the eval uses.
- [Representation Tradeoffs for Hyperbolic Embeddings](https://arxiv.org/abs/1804.03329), De Sa, Gu, Re, and Sala (2018). The trade between distortion, dimension, and numerical precision.
