# Path-Gated Operators Eval

Status: `contract-pass`

This eval tests path-gated and path-conditioned decisions, and compares them
with a baseline that never reads the path.

```text
candidates, each with a score and a cited evidence path
  -> hard path gate: does the path resolve from evidence to this claim?
  -> optional conditioning: discount long chains
  -> commit the best survivor, or abstain
```

## Contract

- A path that resolves from an evidence node to the candidate's own claim
  passes the gate.
- The gate fails closed on a missing path, a missing edge, a missing node, an
  edge that does not connect, and a wrong edge count.
- A path that starts somewhere other than evidence, or reaches a different
  claim, does not pass.
- The highest score does not commit without a resolvable path.
- When nothing passes, the decision is to abstain, and every rejection keeps
  its reason.
- Conditioning can change which surviving candidate ranks first. It cannot
  admit a candidate the gate rejected.

## Comparison

`comparison.py` generates cases with four candidate claims, one of them
correct. Every candidate cites a chain. Whether the chain was really recorded
depends on whether the candidate is correct, with probabilities that are
parameters of the run. Scores favour the correct candidate only slightly.

- Baseline: commit the highest score.
- Variant: gate, then commit the highest score that survived.
- Variant: gate, then commit the highest path-conditioned score.

A second regime sets the probabilities so that a recorded chain says nothing
about correctness.

## Connections

- Architecture: [path-conditioned and path-gated](../../../architecture/path-conditioned-and-path-gated.md),
  [path-gated operators](../../../architecture/path-gated-operators.md), and
  [path-conditioned operators](../../../architecture/path-conditioned-operators.md).
- Reference code: [Architecture reference Python](../../../architecture/reference/python/README.md).
- Result record: [results.md](results.md).

## Files

- [eval.py](eval.py): path validation, the gate, conditioning, and decisions.
- [test_eval.py](test_eval.py): contract tests.
- [comparison.py](comparison.py): seeded comparison against the baseline.
- [test_comparison.py](test_comparison.py): thresholds for the comparison.
