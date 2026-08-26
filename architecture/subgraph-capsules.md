# Subgraph Capsules

## Definition

A subgraph capsule is a named Architecture boundary around local graph detail.
It lets an execution graph treat a specialized graph as one routeable unit
without hiding its inputs, outputs, evidence, or authority limits.

## Why Use It

Use a subgraph capsule when a project has local structure that is meaningful
but too detailed for the top-level execution graph.

Examples:

- a sensor-processing graph;
- a robot topology graph;
- a cache dependency subgraph;
- a processor graph for one task class;
- a verifier graph;
- an evidence-record graph;
- an agent worker graph;
- a place or manifold memory neighborhood.

## Minimum Capsule Declaration

```text
capsule id
owner layer or domain
input channels
output records
local nodes and static relations
runtime routes, if any
evidence refs
allowed side effects
policy or gate requirements
memory read/write boundary
trace summary
failure modes
```

## Runtime Contract

A capsule can produce:

- evidence;
- proposals;
- verifier results;
- gate results;
- bounded summaries;
- action adapter results;
- outcome conversions;
- memory recall summaries.

A capsule cannot make a proposal committed by itself. It must return to the
execution graph authority path.

```text
capsule output -> proposal or evidence -> verifier/gate -> commit
```

## Provisional Capsules

A provisional graph capsule is a stricter capsule used by
[Provisional Graph Growth](provisional-graph-growth.md). It represents a
candidate new route, rule, edge, or specialist before the durable graph accepts
it.

Provisional capsules can explain, shadow-score, route to review, or produce a
growth patch. They cannot commit themselves or mutate durable graph state.

## Compression Without Hiding

Subgraph capsules are allowed to summarize local detail, but the summary must
preserve enough information to review or replay the decision.

Good summaries include:

- capsule id and version;
- source view refs;
- selected path refs;
- gate results;
- rejected or unavailable routes when relevant;
- evidence refs;
- uncertainty and failure reasons.

Bad summaries hide:

- which local path was used;
- which gate blocked;
- whether the capsule used missing evidence;
- whether output was observed, inferred, or counterfactual.

## Validation Questions

```text
1. What local graph detail does the capsule own?
2. What can enter and leave the capsule?
3. Does the capsule emit evidence or proposals instead of hidden authority?
4. Can the capsule output be traced and replayed?
5. Are memory reads separated from memory writes?
6. Is a failed capsule represented as a structured state?
```
