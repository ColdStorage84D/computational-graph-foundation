# Hyperbolic Placement Eval

Status: `contract-pass`

This eval tests Poincare-ball placement validity and hierarchy-aware distance.

## Comparison

`comparison.py` places complete trees with one layout rule and measures how
well embedded distance matches tree distance, once in the flat plane and once
in the Poincare ball. It also places a square grid, which has no hierarchy, to
show where the flat plane is the better geometry.

## Connections

- Substrate: [metric placement](../../../substrate/extensions/cards/metric-placement.md).
- Research: [hyperbolic metric placement study](../../../research/extension-studies/hyperbolic-metric-placement.md).
- Result record: [results.md](results.md).

## Files

- [eval.py](eval.py): the implementation under test.
- [test_eval.py](test_eval.py): contract tests.
- [comparison.py](comparison.py): seeded comparison against the baseline.
- [test_comparison.py](test_comparison.py): thresholds for the comparison.
