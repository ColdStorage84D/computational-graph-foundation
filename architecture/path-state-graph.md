# Path-State Graph

## Definition

A path-state graph is an Architecture view that represents facts, relations,
candidate decisions, committed decisions, workflows, and subgraph routes as
paths through runtime state.

## Purpose

The path-state graph gives the execution graph and runtime spine a common
operating surface.

It avoids splitting operation into unrelated graph families:

```text
local fact = zero-step path
relation = one-edge path
workflow = multi-step path
decision = candidate or committed path
subgraph route = path through role capsules
```

Path-conditioned and path-gated Architecture use this surface. The path-state
graph exposes the path context; path-conditioned operators may use that context
to change computation, and path-gated operators may control path influence or
advancement.

## Runtime Path Kinds

| Path kind | Meaning | Example |
| --- | --- | --- |
| Fact path | A single declared state point. | Current cart status. |
| Relation path | A direct relation between two runtime nodes. | Cart depends on inventory reservation. |
| Workflow path | Ordered steps across roles or services. | Submit cart, reserve inventory, authorize payment, create order. |
| Proposal path | Candidate route not yet accepted. | Ship from warehouse A. |
| Commit path | Accepted route or non-action. | Create order and reserve inventory. |
| Outcome path | Observed result of committed work. | Payment failed after authorization attempt. |
| Memory path | Outcome-backed value or inhibition route. | Carrier and region path became riskier. |

## Node Roles

Runtime nodes can represent:

- tasks;
- choices;
- proposals;
- commits;
- operators;
- policies;
- artifacts;
- tools;
- outcomes;
- memory anchors;
- subgraph capsules.

These are Architecture roles. They do not replace Substrate graph entities.

## Validation Questions

```text
1. Is the path built from declared runtime nodes and edges?
2. Is candidate state separate from committed state?
3. Are rejected paths preserved as counterfactual evidence when useful?
4. Is path context explicit when it conditions an operator?
5. Is gate basis explicit when a path gate controls influence or advancement?
6. Can the path be serialized into a trace?
7. Does the path preserve evidence references?
```
