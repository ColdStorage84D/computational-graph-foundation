# Information Geometry Eval

Status: `contract-pass`

This eval tests discrete belief quantities: divergence, entropy, surprise,
information gain, tail-risk mass, calibration error, and two distances.

The geometric part is the Fisher information metric on the probability
simplex, `sum(d_i ** 2 / p_i)`, and its geodesic distance, the Fisher-Rao
distance `2 * arccos(sum sqrt(p_i q_i))`.

## Contract

- Fisher-Rao distance is symmetric, zero on identical beliefs, and satisfies
  the triangle inequality on the fixture.
- For a small shift, KL divergence is half the squared Fisher length and the
  Fisher-Rao distance is the Fisher length.
- Two shifts of the same flat size are not the same size in the Fisher
  geometry: a rare state becoming six times likelier is the larger change.
- A displacement that leaves the simplex, and beliefs over different supports,
  are rejected.

## Connections

- Substrate: [information geometry](../../../substrate/extensions/cards/information-geometry.md).
- Research: [information geometry study](../../../research/extension-studies/information-geometry.md).
- Result record: [results.md](results.md).

## Files

- [eval.py](eval.py): the belief quantities.
- [test_model.py](test_model.py): tests for the Fisher metric and distance.
- [test_eval.py](test_eval.py): tests for the other belief quantities.
