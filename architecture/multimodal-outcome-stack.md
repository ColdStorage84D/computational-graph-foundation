# Multimodal Outcome Stack

The Multimodal Outcome Stack is the CGF Architecture guide for projects where
one case contains several evidence surfaces and the final answer must stay
traceable.

Use it when a project needs this reusable chain:

```text
external evidence
-> bounded evidence records
-> typed multimodal graph
-> feature views and lenses
-> processor routes
-> proposals
-> verifier / review / commit
-> traceable outcome
```

This is not a health-only pattern. It can support image review, document
analysis, robotics perception, security triage, product catalog reasoning,
sensor fusion, trading signal review, and predictive maintenance.

## Core Rule

A multimodal outcome is not produced by blindly stacking every available
feature. It is produced by naming the evidence surfaces, choosing valid views,
routing work to processors that fit the task, preserving competing proposals,
and committing only through a visible authority boundary.

## Why This Exists

Many multimodal systems fail in the same ways:

- source evidence is copied into every record;
- labels leak into inference features;
- raw coordinates dilute the signal;
- one global encoder is used for tasks with different invariance needs;
- the winning prediction hides the views and proposals that competed;
- review state is mixed into source evidence;
- later labels are treated as if they were available at inference time.

The stack makes those failure modes explicit.

## Reusable Pieces

| Piece | Responsibility | Main document |
| --- | --- | --- |
| Evidence record | Keep source evidence external and expose bounded decoded records. | [frameworks/cards/evidence-record-framework.md](frameworks/cards/evidence-record-framework.md) |
| Typed multimodal graph | Represent one case as typed nodes, edges, fields, and labels. | [frameworks/cards/typed-multimodal-graph-framework.md](frameworks/cards/typed-multimodal-graph-framework.md) |
| Feature view | Name the lens or encoding used by a branch. | [frameworks/cards/feature-view-framework.md](frameworks/cards/feature-view-framework.md) |
| Processor routing | Select valid processors by task fit, evidence, and validation. | [frameworks/cards/processor-routing-framework.md](frameworks/cards/processor-routing-framework.md) |
| Granular Analysis | Fan one input through many lenses and proposers. | [granular-analysis.md](granular-analysis.md) |
| Proposer-verifier | Let candidates compete and advance only with visible support. | [frameworks/cards/proposer-verifier-framework.md](frameworks/cards/proposer-verifier-framework.md) |
| Human review | Keep sensitive outputs in proposal state until review accepts them. | [frameworks/cards/human-review-framework.md](frameworks/cards/human-review-framework.md) |
| Trace and replay | Reconstruct which evidence, views, processors, proposals, and gates operated. | [event-log-trace-replay.md](event-log-trace-replay.md) |

## Minimum Declaration

A project using this stack should declare:

```text
case id
source evidence refs
decoded record types
typed graph node and edge types
training-only labels or future outcomes
lenses / feature views
processor route candidates
proposal nodes
verifier or review gate
commit or abstain rule
trace fields
claim boundary
```

If any item is missing, the project can still be useful, but it should not be
described as a complete multimodal CGF outcome stack.

## Feature And Processor Discipline

Feature views should declare what kind of information they carry:

```text
raw
invariant
aligned
domain-specific
aggregate
```

Raw views are useful when position, pose, order, or orientation is signal.
Invariant views are useful when those quantities are nuisance. Aligned views
are useful when different modalities or frames must be compared.

Do not use one invariant or aligned processor globally. A processor that removes
a quantity is invalid for a task where that quantity is the answer.

## Outcome Discipline

The outcome record should be able to answer:

```text
Which evidence refs were read?
Which typed records were created?
Which graph nodes and fields were used?
Which lenses produced outputs?
Which processors were allowed, skipped, failed, or blocked?
Which proposals competed?
Which proposal was selected, reviewed, deferred, or rejected?
Which verifier basis or review gate applied?
Which labels were training-only and excluded?
What claim is actually supported?
```

## When To Use

Use the stack when:

- one case has multiple modalities, regions, documents, sensors, or metadata
  surfaces;
- different tasks need different valid encoders or processors;
- one input can support many proposals;
- rejected alternatives matter for audit or later review;
- labels, review outcomes, or future observations must be excluded from live
  inference.

## When Not To Use

Do not use the stack when:

- the subject has one deterministic view;
- there are no competing views, processors, or proposals;
- source evidence can be represented directly without bounded records;
- trace and review do not matter;
- the vocabulary would add ceremony without preventing a real failure mode.

## Boundary

The Multimodal Outcome Stack is an Architecture mix. It does not replace the
Substrate declaration. It does not make a domain claim by itself. It does not
require a CGF SDK, graph database, model framework, or package.

## Current Support

The current CGF-local support is a tiny contract eval for the framework mix:
[../labs/evals/multimodal-framework-mix/results.md](../labs/evals/multimodal-framework-mix/results.md).

That result only supports the local contract tested by the fixture. It does not
prove domain performance, medical validity, model quality, or production safety.
