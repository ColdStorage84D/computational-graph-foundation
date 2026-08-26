# Metric Placement

## Definition

Metric placement adds distance, scale, angle, similarity, or geometry to graph
support.

## Parent layer

Substrate.

## Problem solved

Graph adjacency alone may not say how far, close, aligned, scaled, or comparable
two supported quantities are.

## Minimum substrate shape

- Graph support.
- Metric or geometric relation.
- Fields affected by the relation.
- Action, constraint, or validation rule using the metric.
- Scope where the metric is valid.

## When to use

- Distance or scale affects action or evolution.
- Neighboring graph parts are not equally related.
- Readout needs geometry-aware interpretation.

## When not to use

- Adjacency is the only relation that matters.
- The metric cannot be validated or justified.
- Geometry is used only for display.

## Maturity

Draft extension.

## Substrate-owned declarations

- Metric space: Euclidean, spherical, hyperbolic, graph-geodesic, learned
  metric, or domain-specific distance relation.
- Coordinate or embedding field: values that carry placement.
- Distance function: how two placed values are compared.
- Projection or validity rule: how placement stays inside the allowed geometry.
- Metric action term: distance-aware cost, smoothness, recall, neighborhood,
  or scale relation.

## Validation checks

- Distances are finite and meaningful inside the declared valid domain.
- Projection or normalization preserves placement validity.
- Metric-based edges or weights are traceable to declared placement.
- Readout changes are justified by metric structure, not display geometry.
- Scale and curvature assumptions are stated when they affect the result.

## Failure modes

- Treating an embedding vector as meaningful without declaring the metric.
- Using geometry only for visualization while action secretly depends on it.
- Comparing values across incompatible coordinate charts.
- Letting learned placement drift outside the valid metric domain.
- Assuming graph adjacency and metric closeness are the same relation.
