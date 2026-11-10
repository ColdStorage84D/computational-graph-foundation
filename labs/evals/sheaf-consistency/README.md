# Sheaf Consistency Eval

Status: `contract-pass`

This eval has two layers.

The model layer is a cellular sheaf on a graph: a vector space on every node
and edge, and a linear restriction map from each node into each incident edge.

```text
coboundary        (delta x)_e = F_head x_head - F_tail x_tail
global section    delta x = 0, every pair of views agrees where they overlap
energy            |delta x|^2, the quadratic form of the sheaf Laplacian
```

The record layer restricts, compares, and glues keyed views, and returns an
obstruction record instead of a merged view when they conflict.

## Fixtures

- A three-node cycle with identity restrictions.
- The same cycle with one restriction negated.
- Two views with two coordinates each that overlap on the first only.

## Contract

- On the plain cycle the global sections are exactly the constant
  assignments.
- A disagreement at one node appears on its two edges and nowhere else.
- On the twisted cycle every single edge can be satisfied, yet the only
  assignment that satisfies all three is zero. Local agreement does not imply
  global agreement.
- Views need to agree only on the coordinates they share.
- Diffusion never raises the consistency energy and converges to the nearest
  global section. On the twisted cycle it can only converge to zero.
- Missing restriction maps and assignments of the wrong shape are rejected.

## Connections

- Substrate: [sheaf consistency](../../../substrate/extensions/cards/sheaf-consistency.md).
- Research: [sheaf consistency study](../../../research/extension-studies/sheaf-consistency.md).
- Result record: [results.md](results.md).

## Files

- [eval.py](eval.py): the cellular sheaf and the view records.
- [test_model.py](test_model.py): tests for the cellular sheaf.
- [test_eval.py](test_eval.py): tests for the view records.
- [fixtures/README.md](fixtures/README.md)
