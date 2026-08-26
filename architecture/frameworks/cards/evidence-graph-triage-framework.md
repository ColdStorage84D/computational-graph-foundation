# Evidence Graph Triage Framework

## Purpose

Use this framework when many candidate findings compete for limited review
attention, and the system must separate what the evidence supports from what is
worth looking at first.

## Reusable Concept

Corroboration decides truth; outcomes decide priority.

Typed records become a graph. Rules propose findings with measured, named score
components. Status comes from how many independent sources support a finding, not
from how high its score is. Committed findings open eligibility, observed outcomes
resolve it, and the resulting memory changes ordering only.

```text
evidence records -> typed graph -> proposals
  -> status from evidence diversity, never from score
  -> commit -> eligibility -> observed outcome
  -> value memory -> rank only
```

The framework also declares an authority ordering, which is the part most often
lost when the pattern is reused:

```text
reasoning layer   notes, hypotheses, questions, corrections
                  authority: none
     |  the only bridge: a recorded outcome against a committed proposal
value memory      which rules have proven worth surfacing
                  authority: ordering only
     |  never
status            what the evidence supports
                  authority: truth
```

The failure mode this prevents is specific and common. A reasoning or notes layer
that runs its own eligibility and value loop looks structurally identical to graph
runtime memory, so the two get conflated and speculation quietly gains authority
over findings. Declaring the bridge is what keeps them apart. See
[../../graph-runtime-memory.md](../../graph-runtime-memory.md) for the underlying
distinction between agent or project memory and graph runtime memory.

## Uses CGF Pieces

- evidence records and evidence refs;
- typed graph nodes, edges, and evidence paths;
- proposer / verifier / commit;
- gates, as declared corroboration pairs;
- eligibility, outcome, and value memory;
- coverage and belief state as reported evidence, not as authority;
- trace and replay;
- human review, when a person supplies the outcome.

## Example Applications

- incident evidence triage;
- alert and case triage queues;
- audit and compliance finding review;
- content moderation queues;
- quality-inspection triage;
- code security finding review, when findings need corroboration rather than one
  analyzer's verdict.

## When To Use

- More candidate findings exist than can be reviewed, so ordering matters.
- Several independent sources can support or fail to support the same claim.
- A high score on one source should not be treated as confirmation.
- Reviewers produce dispositions that should influence future ordering.
- Gaps in collection must be distinguishable from clean results.
- A reasoning or notes surface exists that must not gain authority.

## When Not To Use

- One source is authoritative, so corroboration adds nothing.
- Every finding is reviewed, so ordering carries no cost.
- No outcome is ever observed, so memory has nothing to learn from.
- The project needs detection performance rather than review discipline; this
  framework organises triage, it does not improve a detector.

## Boundary

This framework is not a detection method, a scoring model, a risk quantification,
or a claim that corroborated findings are correct. Corroboration across sources
raises support; it does not establish truth, and correlated sources can agree while
both being wrong.

Coverage and belief are reported evidence about the collection, not calibrated
probability. A belief value produced under this framework has no frequency
interpretation unless a project separately validates one.

It is distinct from
[code-security-graph-framework.md](code-security-graph-framework.md), which is
scoped to static code analysis: parsers, control and data flow, and findings over
source. This card is about any finding surface where independent corroboration
decides status and observed outcomes decide ordering, whatever produced the
findings.

## Implementation Posture

Keep the status decision structurally unable to see a score. A status function that
accepts only records cannot be influenced by ranking, and that is easier to defend
than a convention. Keep raw measured components separate from any learned weight in
both storage and output, so a reader can see which half moved.

Treat an unresolved outcome as uncertainty rather than success, and make value keys
carry no case-specific detail, or they accumulate one sample each and never
generalise.

The current direct Labs result is a tiny-fixture `contract-pass`:
[../../../labs/evals/evidence-graph-triage/results.md](../../../labs/evals/evidence-graph-triage/results.md).
Use it only as support for the local contract, not as a validated triage-quality
claim. No application example currently ships for this card; the eval is the
only worked implementation.
