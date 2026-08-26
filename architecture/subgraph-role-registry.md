# Subgraph Role Registry

Subgraph roles are bounded graph capsules used inside an execution graph. They
are roles, not separate foundations.

## Role Rule

Each subgraph role should declare:

```text
role name
owned local state
input records
output records
authority boundary
trace obligations
failure modes
```

## Current Roles

| Role | Purpose | Boundary |
| --- | --- | --- |
| Execution subgraph | Runs a bounded operating loop. | Returns evidence, candidates, uncertainty, or deferral. |
| Decision subgraph | Owns local verification and decision support. | Final authority remains explicit in the parent operating path. |
| Memory subgraph | Maintains outcome-backed operating memory projections. | No durable update without resolved outcome support. |
| Operator subgraph | Hosts transforms, scorers, projectors, or learned operators. | Cannot bypass verification and trace. |
| Channel adapter subgraph | Translates between channels, formats, or external systems. | Must preserve source refs and adapter basis. |
| Tool subgraph | Wraps tool calls, permissions, and tool results. | Tool output is evidence, not final authority. |
| Artifact subgraph | Tracks files, reports, generated outputs, and versions. | Artifacts preserve refs; they do not prove claims. |
| Model subgraph | Holds model interface, checkpoint, head, or evaluation state. | Model output remains proposal evidence. |
| Path evidence subgraph | Materializes explicit evidence paths when path shape matters. | Evidence paths support decisions but do not decide alone. |
| Lens registry subgraph | Tracks lens ids, versions, parameters, and application records. | Lens identity supports replay; it does not validate output by itself. |

## When To Use

Use this registry when a local specialist graph should be routeable, testable,
and bounded without becoming a separate CGF layer.

## Claim Boundary

This is a docs-led registry. Use Architecture contracts and section-local tests
before making implementation claims.
