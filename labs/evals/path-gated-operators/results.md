# Path-Gated Operators Results

Status: `contract-pass`

Eval layer: `value-over-baseline`

Reviewed date: 2026-11-10

Reviewed command:

```powershell
python -m unittest discover -s labs/evals/path-gated-operators -p "test_*.py"
python labs/evals/path-gated-operators/comparison.py
```

Reviewed result:

```text
Ran 12 tests
OK
```

## Comparison

Seed 20260101, 4000 cases per regime, four candidates per case.

Failure mode: the highest score commits although its cited path was never
recorded. Metric: wrong commits per case.

Paths carry information: a chain is recorded for 85% of correct candidates and
15% of wrong ones, and correct chains are usually one hop.

| Arm | Wrong commits | Correct commits | Abstained | Precision |
| --- | --- | --- | --- | --- |
| Score only (baseline) | 64.9% | 35.1% | 0.0% | 0.351 |
| Path gated | 20.3% | 70.4% | 9.4% | 0.777 |
| Path gated and conditioned | 16.0% | 74.7% | 9.4% | 0.824 |

Paths carry no information: a chain is recorded for 50% of candidates whether
correct or not, and chain length is unrelated to correctness.

| Arm | Wrong commits | Correct commits | Abstained | Precision |
| --- | --- | --- | --- | --- |
| Score only (baseline) | 66.3% | 33.7% | 0.0% | 0.337 |
| Path gated | 67.2% | 27.0% | 5.8% | 0.287 |
| Path gated and conditioned | 67.9% | 26.4% | 5.8% | 0.280 |

Pass thresholds, checked by `test_comparison.py`: in the first regime the gate
keeps wrong commits under 25% and more than doubles precision; in the second
it is no better than the baseline. Across seeds 1 to 3 the gate at least halves
wrong commits in the first regime.

## Where It Does Not Help

The gate is worth exactly as much as the link between a recorded path and
correctness. When that link is absent the gate removes candidates at random,
abstains on 5.8% of cases, and lowers precision from 0.337 to 0.287. It also
costs abstentions in the regime where it helps.

Claim boundary: synthetic cases from a generator whose assumptions are its
parameters. The result shows the size of the effect under those assumptions
and its absence without them. It does not measure how informative evidence
paths are in any real system, and it supports no accuracy claim for one.
