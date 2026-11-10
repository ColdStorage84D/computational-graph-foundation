# Evidence Graph Triage Eval

Status: `contract-pass`

This eval tests the CGF-local Evidence Graph Triage contract:

```text
evidence records -> status from evidence diversity, never from score
  -> commit -> eligibility -> observed outcome
  -> value memory -> rank only
```

The fixture is synthetic and domain-neutral. Source categories are `source_a`,
`source_b`, and `source_c` rather than any domain vocabulary, because the contract
under test is the reusable pattern and not one application of it. It is not
incident data, security data, audit data, or any measured corpus.

## Owning Docs

- Framework card:
  [evidence-graph-triage-framework.md](../../../architecture/frameworks/cards/evidence-graph-triage-framework.md).
- Graph runtime memory:
  [graph-runtime-memory.md](../../../architecture/graph-runtime-memory.md).
- Memory and outcome feedback:
  [memory-outcome-feedback.md](../../../architecture/memory-outcome-feedback.md).

## Fixture

Four candidates, one per status branch:

```text
finding:corroborated        two sources, a declared gate pair  -> confirmed / commit
finding:single-source-high  one record, the highest raw score  -> inferred / defer
finding:multi-record        two records, one source            -> review / review
finding:unsupported         no records                         -> needs_more_evidence / defer
```

`finding:multi-record` is scored just above `finding:corroborated`, so one recorded
outcome on the corroborated item is enough to swap them. That swap, with every
status unchanged, is what the eval observes.

## Comparison

`comparison.py` generates synthetic findings, each recorded by zero to three
sources, and compares three ways of deciding what to commit:

- the highest scores, at the same volume the corroboration arm commits;
- any finding with two or more records;
- `decide_status` from this eval, which needs a declared pair of distinct
  source categories.

A second regime makes two of the sources copies of each other. The numbers
are in [results.md](results.md).

## Run

```powershell
python -m unittest discover -s labs/evals/evidence-graph-triage -p "test_*.py"
```

To print the contract result and the comparison:

```powershell
python labs/evals/evidence-graph-triage/eval.py
python labs/evals/evidence-graph-triage/comparison.py
```

## Claim Boundary

Passing the contract tests supports `contract-pass` for the four-candidate
fixture:

- status is a function of evidence corroboration alone;
- the highest scoring candidate is still deferred when one source supports it;
- an outcome changes rank order without changing any status;
- a candidate that was never committed cannot update value memory;
- a resolved eligibility trace cannot be resolved a second time;
- a replayed outcome id applies nothing;
- inconclusive and expired outcomes raise uncertainty and never register as
  success.

The comparison adds a measured effect on synthetic findings under the
generator's stated assumptions. Neither part supports detection accuracy,
triage-quality improvement on real queues, analyst workload reduction,
calibrated probability or risk scoring, or any security, audit, or moderation
claim.
