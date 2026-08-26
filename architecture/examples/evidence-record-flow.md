# Evidence Record Flow

## Purpose

This example shows how source handles, decoded views, typed records, bounded
retrieval, and trace exports can operate as Architecture records.

## Runtime Shape

```text
source handle -> decoder view -> typed records -> bounded retrieval
  -> evidence trace -> consumer proposal or export
```

## Architecture Responsibilities

- Source evidence remains external and read-only.
- Decoders create bounded views.
- Typed records become retrieval units.
- Parser warnings, coverage, empty output, and truncation are visible state.
- Trace exports preserve refs and bounded summaries.
- Consumers use record refs instead of copying raw evidence.

## Safety Rules

- Evidence refs are handles, not embedded source data.
- Transcript fallback is bounded and secondary to structured records.
- Exports are policy-controlled.
- Record retrieval does not authorize downstream claims by itself.

## Validation Questions

```text
1. Which source handle was decoded?
2. Which view produced the record?
3. Are parser warnings visible?
4. Is retrieval bounded?
5. Can the evidence trace reconstruct the view and record path?
```
