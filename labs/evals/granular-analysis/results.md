# Granular Analysis Results

Status: `contract-pass`

Eval layer: `value-over-baseline`

Reviewed date: 2026-11-10

Reviewed command:

```powershell
python -m unittest discover -s labs/evals/granular-analysis -p "test_*.py"
python labs/evals/granular-analysis/comparison.py
```

Reviewed result:

```text
Ran 12 tests
OK
```

## Comparison

Seed 20260105, 4000 cases per regime. Every arm runs the reference
`GranularAnalysisEngine` with commit threshold 0.70 and review threshold 0.45.

Failure mode: one lens decides alone, so its blind spot becomes the outcome.
Metric: wrong commits per case, with the review rate as the cost.

Independent blind spots: each lens reports confident support for the wrong
outcome on 20% of cases, independently of the others.

| Arm | Wrong commits | Sent to review | Precision |
| --- | --- | --- | --- |
| Single lens, best of three (baseline) | 19.6% | 3.3% | 0.798 |
| Three lenses, a proposer per pair | 10.2% | 1.1% | 0.897 |
| Three lenses, one proposer reading all | 0.7% | 52.4% | 0.986 |

Shared blind spot: all three lenses are wrong together on 20% of cases.

| Arm | Wrong commits | Sent to review | Precision |
| --- | --- | --- | --- |
| Single lens, best of three (baseline) | 19.4% | 2.8% | 0.800 |
| Three lenses, a proposer per pair | 20.0% | 0.1% | 0.800 |
| Three lenses, one proposer reading all | 19.3% | 5.5% | 0.796 |

Pass thresholds, checked by `test_comparison.py`: with independent blind
spots, pair proposers keep wrong commits under 60% of the best single lens with
review under 5%, and the unanimous proposer keeps wrong commits under 2%; with
a shared blind spot neither improves on a single lens.

## Where It Does Not Help

More lenses help only as far as their errors are independent. With a shared
blind spot the wrong-commit rate does not move. The unanimous proposer buys its
low error rate by sending half of all cases to review.

Claim boundary: synthetic cases with two outcomes and three lenses whose error
behaviour is set by the generator. The result shows the trade between wrong
commits and review under those assumptions. It does not claim clinical
validity, diagnostic accuracy, model performance, or that real lenses have
independent errors.
