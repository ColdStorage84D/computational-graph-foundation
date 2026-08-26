# Evidence Graph Triage Results

Status: `contract-pass`

## Reviewed Command

```powershell
python -m unittest discover -s labs/evals/evidence-graph-triage -p "test_*.py"
```

## Result

```text
Ran 12 tests
OK
```

Observed queue movement, with every status unchanged between the two cycles:

```text
before                        after
finding:single-source-high    finding:single-source-high
finding:unsupported           finding:unsupported
finding:multi-record          finding:corroborated
finding:corroborated          finding:multi-record
```

## Claim Boundary

This result supports only the CGF-local Evidence Graph Triage contract on a tiny
synthetic fixture:

- status is a function of evidence corroboration alone;
- the status function cannot receive a score, so ranking cannot influence it;
- the highest scoring candidate is still deferred when only one source supports it;
- a recorded outcome changes rank order without changing any status;
- a candidate that was never committed cannot update value memory;
- a resolved eligibility trace cannot be resolved a second time;
- a replayed outcome id applies nothing;
- inconclusive and expired outcomes raise uncertainty and never register as
  success.

## Not Supported

This result does not support detection accuracy, malware or threat
identification, triage-quality improvement, analyst workload reduction,
calibrated probability or risk scoring, evidence-collection completeness, or any
security, audit, compliance, or moderation claim.

The fixture is four synthetic candidates with neutral source labels. It is not a
measured corpus, and the value-key scheme and decay behavior have not been
validated against real review volume.
