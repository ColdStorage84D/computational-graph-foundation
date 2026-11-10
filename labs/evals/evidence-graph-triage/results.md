# Evidence Graph Triage Results

Status: `contract-pass`

Eval layer: `value-over-baseline`

Reviewed date: 2026-11-10

Reviewed command:

```powershell
python -m unittest discover -s labs/evals/evidence-graph-triage -p "test_*.py"
python labs/evals/evidence-graph-triage/comparison.py
```

Reviewed result:

```text
Ran 19 tests
OK
```

## Contract Result

Observed queue movement, with every status unchanged between the two cycles:

```text
before                        after
finding:single-source-high    finding:single-source-high
finding:unsupported           finding:unsupported
finding:multi-record          finding:corroborated
finding:corroborated          finding:multi-record
```

- status is a function of evidence corroboration alone;
- the status function cannot receive a score, so ranking cannot influence it;
- the highest scoring candidate is still deferred when only one source supports it;
- a recorded outcome changes rank order without changing any status;
- a candidate that was never committed cannot update value memory;
- a resolved eligibility trace cannot be resolved a second time;
- a replayed outcome id applies nothing;
- inconclusive and expired outcomes raise uncertainty and never register as
  success.

## Comparison

Seed 20260102, 5000 findings per regime, 25% of them real.

Failure modes, both named on the framework card: a high score from one source
is treated as confirmation, and repeated records from one source are counted
as corroboration. Metric: wrong commits and precision. The score-ranked arm
commits the same number of findings as the corroborated arm, so the two are
compared at equal review volume.

Independent sources: each source records a real finding 70% of the time and a
false one 15% of the time. A source that fires emits one to three records, and
the score rises with record count.

| Arm | Commits | Wrong commits | Precision | Recall |
| --- | --- | --- | --- | --- |
| Score ranked (baseline) | 924 | 313 | 0.661 | 0.507 |
| Two or more records (baseline) | 2155 | 1047 | 0.514 | 0.920 |
| Corroborated by a declared source pair | 924 | 144 | 0.844 | 0.647 |

Correlated sources: `source_b` repeats `source_a` 95% of the time.

| Arm | Commits | Wrong commits | Precision | Recall |
| --- | --- | --- | --- | --- |
| Score ranked (baseline) | 1376 | 636 | 0.538 | 0.609 |
| Two or more records (baseline) | 1916 | 896 | 0.532 | 0.840 |
| Corroborated by a declared source pair | 1376 | 539 | 0.608 | 0.689 |

Pass thresholds, checked by `test_comparison.py`: with independent sources,
corroboration has under half the wrong commits of score ranking and precision
above 0.80; with correlated sources its precision advantage is less than half
as large.

## Where It Does Not Help

Corroboration gives up recall: it commits 65% of real findings where counting
records commits 92%. When two sources are copies of each other the precision
advantage shrinks from 0.18 to 0.07, because the pair no longer carries two
independent observations. The contract counts distinct source categories; it
cannot tell whether they are independent.

## Not Supported

This result does not support detection accuracy, malware or threat
identification, triage-quality improvement on real queues, analyst workload
reduction, calibrated probability or risk scoring, evidence-collection
completeness, or any security, audit, compliance, or moderation claim.

Claim boundary: the contract fixture is four synthetic candidates. The
comparison uses synthetic findings from a generator whose assumptions are its
parameters. Neither is a measured corpus, and the value-key scheme and decay
behavior have not been validated against real review volume.
