# Memory And Outcome Feedback

## Purpose

This pattern keeps graph runtime memory tied to observed outcomes instead of
choices alone.

## Core Rule

```text
choice alone is not learning
committed choice + observed outcome can update value
```

## Memory Flow

```text
commit -> eligibility -> outcome -> value / inhibition / uncertainty
  -> possible promotion
```

For the fuller memory taxonomy, see
[graph-runtime-memory.md](graph-runtime-memory.md).

## Memory Roles

| Role | Meaning |
| --- | --- |
| Eligibility | Pending credit or blame opened by a committed path. |
| Outcome | Observed result that resolves eligibility. |
| Value memory | Outcome-weighted future guidance. |
| Inhibition | Outcome-backed warning against a path or condition. |
| Uncertainty | Result of unresolved, expired, or ambiguous outcomes. |
| Residual memory | Observed mismatch between expected and actual action or state. |
| Action-functional memory | Learned local weights over raw terms, context, action, and region. |
| Place/manifold memory | Local region and transition graph with support, loops, novelty, and expected progress. |
| Promotion | Higher-trust memory created only after policy allows it. |
| Quarantine | Isolated memory for contradictory, dangerous, or low-trust evidence. |
| Counterfactual memory | Rejected, simulated, or hypothetical paths that cannot count as observed outcomes. |

## Rules

- Rejected proposals do not create eligibility.
- Uncommitted observations can be evidence, but not causal value updates.
- Expired eligibility becomes uncertainty, not success.
- Memory is advisory unless a policy explicitly promotes it.
- Memory must preserve evidence references and sample counts when possible.
- Agent/project notes are not causal graph runtime memory unless they enter
  through declared evidence, proposal, commit, outcome, and memory update paths.
- Counterfactual records cannot update value as if observed.

## Validation Questions

```text
1. Which committed path opened eligibility?
2. What observed outcome resolved it?
3. Did the update reinforce, inhibit, or increase uncertainty?
4. Can the update be traced back to events and commit?
5. Is promoted memory separated from temporary state?
```
