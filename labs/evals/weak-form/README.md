# Weak Form Eval

Status: `contract-pass`

This eval has two layers.

The model layer is a discrete weak form on a weighted graph. The local rule is
`(L + mass * I) u = f` at every node, with `L` the weighted graph Laplacian.
The weak form tests the same law against a test function `phi`:

```text
a(u, phi) = sum over edges of w (u_i - u_j)(phi_i - phi_j) + mass * sum phi_i u_i
l(phi)    = sum phi_i f_i
tested residual = a(u, phi) - l(phi)
```

The record layer reports an aggregate residual together with the local
failures it would otherwise hide.

## Fixture

A nine-node path with a quadratic source, tested with piecewise-linear hat
functions at three, five, and nine nodes.

## Contract

- Summation by parts: the tested residual equals the test function applied to
  the pointwise residual.
- Testing with a single-node indicator recovers the local rule at that node.
- Testing with a region indicator is a balance over the region computed from
  its boundary edges only.
- A Galerkin solution on three hats passes every coarse test while its
  pointwise residual stays large and visible.
- Refining the test space shrinks the pointwise residual, and the full nodal
  space reduces the weak form to the local rule.
- Leaving the source out of the tested condition changes the residual by the
  total source in the region.
- Missing field values, non-positive weights, and a singular system are
  rejected.

## Connections

- Substrate: [weak form](../../../substrate/extensions/cards/weak-form.md).
- Research: [geometric discretization](../../../research/extension-studies/geometric-discretization.md).
- Result record: [results.md](results.md).

## Files

- [eval.py](eval.py): the discrete weak form and the report records.
- [test_model.py](test_model.py): tests for the discrete weak form.
- [test_eval.py](test_eval.py): tests for the report records.
- [fixtures/README.md](fixtures/README.md)
