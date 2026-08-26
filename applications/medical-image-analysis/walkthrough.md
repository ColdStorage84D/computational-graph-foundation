# Medical Image Analysis Review Walkthrough

This walkthrough shows how a medical image analysis review application can use
CGF without making medical image analysis the owner of the reusable framework
concepts.

The same pattern can be reused for any high-separation review problem:
security findings, document review, robotics perception, industrial monitoring,
or audit workflows.

## Application Goal

Build a reviewable graph workflow where one case can contain multiple evidence
surfaces, multiple lens outputs, multiple proposals, and one traceable review
outcome.

The application shape is:

```text
medical image evidence
-> bounded records
-> typed multimodal graph
-> lenses and feature views
-> processor routes
-> proposals
-> verifier / review gate
-> reviewable outcome
-> later label derivation, only after accepted review
```

## Step 1. Source Evidence

Source evidence remains external. The graph stores handles:

```text
evidence:sample-image
evidence:region-summary
evidence:metadata-sheet
evidence:review-note
```

The source payload is not copied into every graph node, proposal, prompt, or
trace. Decoders may produce bounded records with coverage and warning fields.

Owning concept: [../../architecture/frameworks/cards/evidence-record-framework.md](../../architecture/frameworks/cards/evidence-record-framework.md).

## Step 2. Typed Multimodal Graph

The case becomes a typed graph:

```text
case
sample
image
region
measurement
metadata
candidate
review
```

Edges declare relations such as:

```text
case -> sample
sample -> image
image -> region
region -> measurement
candidate -> supporting region
review -> candidate
```

Training labels, future outcomes, accepted review decisions, or later
annotations are not live features. They are separate records.

Owning concept: [../../architecture/frameworks/cards/typed-multimodal-graph-framework.md](../../architecture/frameworks/cards/typed-multimodal-graph-framework.md).

## Step 3. Lenses And Feature Views

One case can expose several views:

```text
texture lens
morphology lens
context / metadata lens
quality lens
combined evidence view
```

Each lens should declare whether it is raw, invariant, aligned,
domain-specific, or aggregate. A view that removes orientation, position, or
scale is only valid when the task does not depend on what was removed.

Owning concept: [../../architecture/frameworks/cards/feature-view-framework.md](../../architecture/frameworks/cards/feature-view-framework.md).

## Step 4. Processor Routes

Processors should be route-specific:

```text
texture processor
morphology processor
context processor
quality processor
combined review processor
```

Routes can be:

```text
allowed
blocked
skipped
unavailable
failed
selected
review
defer
fallback
```

One global processor should not silently handle every task.

Owning concept: [../../architecture/frameworks/cards/processor-routing-framework.md](../../architecture/frameworks/cards/processor-routing-framework.md).

## Step 5. Granular Analysis

The case can fan out:

```text
one case
-> texture lens
-> morphology lens
-> context lens
-> texture proposal
-> morphology proposal
-> combined proposal
-> verifier / review gate
-> traceable review outcome
```

The selected outcome should preserve rejected alternatives. That is the point:
the review item is not a single opaque model answer.

Owning concept: [../../architecture/granular-analysis.md](../../architecture/granular-analysis.md).

## Step 6. Verifier And Review Gate

Processor output is proposal state.

The verifier or review gate can:

```text
commit
review
defer
fallback
abstain
deny
```

In a medical image analysis application, the default safe posture is review or
abstain unless a domain-specific policy says otherwise. CGF does not provide
medical authority.

Owning concepts:
[../../architecture/frameworks/cards/proposer-verifier-framework.md](../../architecture/frameworks/cards/proposer-verifier-framework.md)
and
[../../architecture/frameworks/cards/human-review-framework.md](../../architecture/frameworks/cards/human-review-framework.md).

## Step 7. Trace

The trace should preserve:

```text
case id
source evidence refs
decoded records
typed graph version
lens outputs
route states
proposals considered
selected proposal, if any
rejected proposals
verifier basis
review state
excluded training-only fields
claim boundary
```

Trace is what lets a reviewer or developer inspect the full path behind the
review item.

## Step 8. Later Labels

Later labels can be derived only from accepted outcomes or reviewed records
under an explicit derivation rule.

They must not be treated as live input evidence.

## Minimal Implementation Slice

A first implementation can be tiny:

```text
one synthetic case
three evidence records
three lenses
three proposal nodes
one review gate
one trace
tests for separation and rejected alternatives
```

See [synthetic_review.py](synthetic_review.py) for a small section-local
example.
