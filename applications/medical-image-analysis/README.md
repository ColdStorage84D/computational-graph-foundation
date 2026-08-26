# Medical Image Analysis Application

Medical Image Analysis is an application example for CGF. It is not the owner
of the reusable framework concepts it uses.

The same concepts can be used in projects that have nothing to do with medical
image analysis: evidence review, multimodal records, feature views, processor
routing, proposer/verifier boundaries, human review, trace, replay, and graph
runtime memory.

## Reusable Framework Mix

This application should be built from reusable Architecture framework cards:

- [../../architecture/frameworks/cards/evidence-record-framework.md](../../architecture/frameworks/cards/evidence-record-framework.md)
- [../../architecture/frameworks/cards/typed-multimodal-graph-framework.md](../../architecture/frameworks/cards/typed-multimodal-graph-framework.md)
- [../../architecture/frameworks/cards/feature-view-framework.md](../../architecture/frameworks/cards/feature-view-framework.md)
- [../../architecture/frameworks/cards/granular-analysis-framework.md](../../architecture/frameworks/cards/granular-analysis-framework.md)
- [../../architecture/multimodal-outcome-stack.md](../../architecture/multimodal-outcome-stack.md)
- [../../architecture/frameworks/cards/processor-routing-framework.md](../../architecture/frameworks/cards/processor-routing-framework.md)
- [../../architecture/frameworks/cards/proposer-verifier-framework.md](../../architecture/frameworks/cards/proposer-verifier-framework.md)
- [../../architecture/frameworks/cards/human-review-framework.md](../../architecture/frameworks/cards/human-review-framework.md)
- [../../architecture/execution-graph.md](../../architecture/execution-graph.md)
- [../../architecture/graph-runtime-memory.md](../../architecture/graph-runtime-memory.md)

## Medical Image Analysis Docs

- [INDEX.md](INDEX.md): medical image analysis application map.
- [walkthrough.md](walkthrough.md): step-by-step review flow.
- [review-template.md](review-template.md): copyable review declaration.
- [claim-boundary.md](claim-boundary.md): supported and unsupported claims.
- [synthetic_review.py](synthetic_review.py): tiny synthetic example.
- [index.html](index.html): static fixture demo for browser testing.
- [BENCHMARK_RESOURCES.md](BENCHMARK_RESOURCES.md): optional external benchmark setup.

## Application Shape

A medical image analysis review application can use this flow:

```text
source evidence
-> evidence records
-> typed multimodal graph
-> Multimodal Outcome Stack
-> Granular Analysis
-> feature views and processor routes
-> candidate proposals
-> verifier gates
-> ranked review queue
-> grounded explanation or draft
-> reviewer action
-> later outcome or label derivation
```

The exact domain can change. The reusable structure remains:

```text
external source evidence
bounded decoded records
typed graph facts
processor proposals
visible verifier basis
review gate
traceable final state
```

## Histology-Style Granular Analysis

A histology-like application can use Granular Analysis without making medical
image analysis the owner of the concept:

```text
one sample
-> texture lens
-> morphology lens
-> context / metadata lens
-> texture proposal
-> morphology proposal
-> combined-evidence proposal
-> verifier
-> review, defer, fallback, abstain, or traceable outcome
```

The value is not a single opaque model answer. The value is that the selected
outcome can show which lens branches supported it, which proposals competed,
and which alternatives were rejected or deferred.

## What Medical Image Analysis Adds

Medical image analysis adds domain-specific decisions:

- source evidence types;
- modality and record vocabularies;
- allowed processors;
- review roles;
- safety policy;
- report or communication surfaces;
- domain-specific evaluation.

Those decisions belong in this application, not in the reusable framework
cards.

## Reusable Lessons Applied Here

Medical image analysis projects are useful examples because they force strict
separation:

- source evidence remains external;
- decoded records are bounded;
- labels and later outcomes are not live features;
- one global processor is not assumed valid for every task;
- route-specific processors need declared fit and validation;
- processor output is proposal state;
- review state is distinct from source evidence;
- final claims require a trace, verifier basis, and review or policy boundary.

The same lessons apply to non-medical domains such as security findings,
document analysis, robotics perception, and industrial monitoring.

## What Medical Image Analysis Must Not Add

Medical image analysis must not make CGF claim:

- diagnosis authority;
- clinical safety;
- replacement of professional judgment;
- replacement of source systems;
- broad model performance;
- validated medical workflow behavior without domain-specific evidence.

## Boundary

Source evidence remains external and read-only by default. Processor outputs
are proposals. Review state is separate from source evidence. Later labels or
training signals require explicit derivation from accepted outcomes or review
records.

## Try The Fixture Demo

The committed browser demo uses only CGF-native fixture images and generated
trace data:

```text
index.html
```

The page shows one fixture case at a time:

```text
fixture image
-> visual lens outputs
-> competing proposals
-> verifier decision
-> rejected alternatives
-> trace
```

The fixture data is for workflow testing only. It is not benchmark data and it
does not support medical or model-performance claims.

## Optional Benchmark Testing

Benchmark data is not committed to CGF. Developers who want to test with a
local benchmark copy should follow [BENCHMARK_RESOURCES.md](BENCHMARK_RESOURCES.md)
and set `CGF_MEDICAL_BENCHMARK_DIR`.

The optional benchmark path is a local smoke-test path. It verifies that records
can flow through the CGF graph/lens/proposal/review pipeline. It does not create
a clinical, diagnostic, benchmark-performance, or dataset-representativeness
claim.

## Current Status

This is an application example with docs, a CGF-native fixture dataset, a static
browser demo, and optional local benchmark-resource support. It does not include
benchmark data, clinical integration, safety claim, or medical claim.
