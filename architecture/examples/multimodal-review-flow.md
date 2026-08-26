# Multimodal Review Flow

This example shows how the Multimodal Outcome Stack can be used without making
the pattern belong to any one domain.

## Flow

```text
source packet
-> evidence refs
-> decoded records
-> typed graph case
-> texture lens
-> layout lens
-> metadata lens
-> route-specific processors
-> candidate proposals
-> verifier / review gate
-> traceable outcome or abstain
```

## Evidence Records

The source packet stays outside the graph. The graph keeps handles such as:

```text
evidence:image-region-a
evidence:metadata-sheet
evidence:operator-note
```

Decoded records can summarize bounded facts:

```text
record:region-texture
record:layout-measurement
record:metadata-quality
```

The raw source material is not copied into every proposal or trace.

## Typed Multimodal Graph

The case graph may contain:

```text
case
image
region
measurement
metadata
question
candidate
review
```

Labels, future outcomes, reviewer decisions, or training annotations are marked
as training-only or later-derived records. They cannot enter live lens outputs.

## Lenses And Views

The same case can expose several views:

```text
texture view       invariant or aggregate signal
layout view        raw or orientation-sensitive signal
metadata view      context and quality signal
combined view      selected fields from several lens outputs
```

The view choice is part of the trace. It is not hidden inside a single feature
matrix.

## Processor Routes

Processors are selected by declared fit:

```text
texture processor      allowed for texture-like tasks
layout processor       allowed when orientation or position matters
metadata processor     allowed for context and source-quality checks
combined processor     allowed only when its input views are present
```

Unavailable, invalid, skipped, failed, reviewed, or deferred routes remain
visible states.

## Proposals And Review

Each processor output becomes evidence, a proposal, or a derived record.

```text
proposal:texture-supported-candidate
proposal:layout-supported-candidate
proposal:combined-supported-candidate
proposal:abstain
```

The verifier can commit a supported candidate, send it to review, defer for
more evidence, fall back to a robust default, or abstain.

## Trace

The trace should preserve:

```text
input id
evidence refs
decoded records
typed graph version
lens outputs
processor routes
selected and rejected proposals
verifier basis
review status, if any
commit or abstain reason
hidden labels excluded
```

This is the reusable value: the outcome is not just a prediction. It is an
auditable graph of how the prediction, review item, or abstain decision was
assembled.
