# Code Security Graph Framework

## Purpose

Use this framework when source code needs typed graph evidence for findings,
control flow, data flow, verification, and exports.

## Reusable Concept

Represent a codebase as a typed evidence graph. Parsers create syntax and
semantic nodes. Local passes add conservative control and data flow. Rules or
models propose findings. Verifiers preserve evidence paths and status.

## Uses CGF Pieces

- typed graph subject;
- evidence paths;
- proposal / verifier / commit;
- path-gated findings;
- traceable exports;
- bounded source refs.

## Example Applications

- static security analysis;
- code review assistants;
- supply-chain inspection;
- policy linting;
- secure refactoring tools.

## When To Use

- Findings need source location and evidence paths.
- Control-flow or data-flow context matters.
- Proposed findings can be verified, reviewed, suppressed, or exported.
- Raw source should be referenced carefully rather than copied everywhere.

## When Not To Use

- The project only needs text search.
- Findings do not need evidence paths.
- Parser or language support is too incomplete for useful claims.

## Boundary

This framework can create candidate findings and verification records. It does
not prove security completeness without a dedicated evaluation suite.

## Implementation Posture

Start with one language, conservative rules, deterministic exports, and tests
that prove evidence paths and finding status are stable.
