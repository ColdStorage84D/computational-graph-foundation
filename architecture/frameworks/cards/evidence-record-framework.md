# Evidence Record Framework

## Purpose

Use this framework when source evidence should stay external while decoded
views, typed records, retrieval, exports, and traces remain bounded.

## Reusable Concept

Source evidence is represented by stable handles. Decoders produce bounded
views. Views produce typed records. Consumers retrieve records through scoped
queries, summaries, pages, and exports.

The framework prevents raw evidence from being copied into every graph,
answer, prompt, or trace.

In a multimodal outcome stack, evidence records are the first boundary:

```text
source evidence -> evidence ref -> decoded record -> typed graph node or field
```

The graph can cite evidence refs and decoded records without becoming the
source system.

## Minimum Record Shape

An evidence record should name:

```text
evidence ref
record id
record type
decoder or adapter id
bounded content or summary
coverage or truncation status
warnings or failure state
source timestamp or version, when known
```

The record should not silently include training labels, future outcomes, or
review decisions unless the record is explicitly a later-derived review record.

## Uses CGF Pieces

- evidence refs;
- adapters and lenses;
- typed record views;
- trace contract;
- persistence contract;
- bounded retrieval;
- replayable exports.

## Example Applications

- medical image analysis evidence review;
- code and security analysis;
- audit systems;
- legal or compliance review;
- research curation;
- enterprise knowledge systems.

## When To Use

- Source material is large, sensitive, external, or read-only.
- Decoders can fail, truncate, warn, or produce partial coverage.
- Retrieval must be bounded and traceable.
- Structured records should be preferred over free transcript fallback.
- One case should combine image, document, sensor, metadata, or human-entered
  surfaces without copying all raw material into the graph.

## When Not To Use

- The project has no source evidence boundary.
- Raw evidence can safely be represented directly in the Substrate subject.
- The project does not need bounded retrieval or traceable exports.

## Boundary

Typed records are retrieval units, not final claims. Evidence refs identify
support; they do not make unsupported conclusions true.

Evidence records do not own feature derivation, processor routing, review, or
commit authority. They supply bounded support for those later Architecture
steps.

## Implementation Posture

This is a reusable Architecture pattern. Projects choose their own source
systems, decoders, transports, and storage.
