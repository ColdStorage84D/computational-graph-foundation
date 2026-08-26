# Agent Graph Harness

## Purpose

This example shows how agents, tools, models, memory readers, verifiers, and
evaluators can operate as runtime graph roles without owning final authority.

## Runtime Shape

```text
task event -> agent graph view -> model/tool proposals
  -> verification and policy -> commit -> approved execution
  -> trace -> outcome -> memory update
```

## Architecture Responsibilities

- Agent nodes deliberate and propose.
- Tool and model adapters expose bounded capabilities.
- Policy controls side effects.
- Commit authorizes approved execution.
- Trace records model calls, tool calls, selected proposal, rejected
  alternatives, and outcome.
- Memory updates only after outcome.

## Safety Rules

- Agents are graph roles, not authority.
- Tools are registered capabilities, not arbitrary execution.
- Side effects require committed paths.
- Rejected proposals remain counterfactual.
- Model provider adapters must be swappable.

## Validation Questions

```text
1. Which agent node proposed the action?
2. Which tool or model adapter was used?
3. What policy allowed or blocked execution?
4. Can trace reconstruct the full node path?
5. Did outcome-backed memory update exactly once?
```
