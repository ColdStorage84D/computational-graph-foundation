# Graph Runtime Memory

## Definition

Graph runtime memory is outcome-coupled Architecture state that changes future
operation of an execution graph.

It is not memory merely because it is stored. It is graph runtime memory when
it can affect future scoring, gating, inhibition, uncertainty, recall,
promotion, or replay.

## Core Distinction

```text
agent/project memory = notes, claims, questions, decisions, summaries
graph runtime memory = outcome-backed operating state that changes future graph behavior
```

Agent or project memory may itself be represented as a graph. That does not make
it the execution graph's causal memory. It becomes part of graph runtime memory
only when it enters through a declared memory reader, evidence ref, proposal,
commit, outcome, and memory update path.

## Memory Roles

| Memory role | Meaning | Authority rule |
| --- | --- | --- |
| Event memory | Ordered events used for replay and audit. | Source for replay, not value by itself. |
| Eligibility memory | Pending credit or blame opened by commit. | Only committed paths create eligibility. |
| Outcome/value memory | Reinforcement, inhibition, risk, uncertainty, and sample counts from outcomes. | Only observed outcomes resolve eligibility. |
| Action-functional memory | Learned local weights over raw terms, context, action, and region. | May influence scoring, never hard-gate by itself. |
| Residual action field | Observed residuals for similar context/action regions. | Advisory unless policy promotes it. |
| Place/manifold memory | Local region and transition graph with support, loops, novelty, and expected progress. | Biases proposals or scores through visible evidence. |
| Semantic/procedural projection | Promoted summaries or habits from repeated outcome-backed evidence. | Requires promotion rules and evidence refs. |
| Policy memory | Outcome-backed or reviewed risk rules. | Must remain explicit and reviewable. |
| Quarantine | Contradictory, dangerous, or low-trust memory isolated from promotion. | Blocks or raises review; does not silently vanish. |
| Counterfactual memory | Hypotheses, rejected paths, simulations, or simulated alternatives. | Cannot promote or update value as observed truth. |

## Memory Flow

```text
commit
-> eligibility
-> execution or accepted non-action
-> outcome
-> resolve eligibility
-> update value / inhibition / uncertainty / residual / place field
-> consolidate promoted projections only when allowed
-> replay can rebuild projections
```

## Action-Functional Memory

Action-functional memory keeps raw measurements separate from learned weights.

```text
raw terms + learned local multipliers -> action total
```

The memory record should preserve:

```text
term name
context signature
action signature
optional region
multiplier or weight
support count
prediction error
credit and risk summaries
evidence refs
updated tick or event ref
```

Credits may lower a score. They may not create feasibility or bypass hard
policy.

## Residual And Place Memory

Residual memory answers:

```text
In similar contexts, under similar actions, what residual or action cost was observed?
```

Place or manifold memory answers:

```text
From this local region, which transitions were observed, supported, blocked,
repeated, novel, risky, or productive?
```

These memories are useful for bots, workflows, processors, tools, and review
systems. A place does not have to be physical. It can be a task state, tool
state, document state, cache state, code path state, or dialogue state.

## Promotion And Quarantine

Promotion creates higher-trust memory from repeated or reviewed evidence.

Quarantine isolates memory when:

- evidence contradicts the prediction;
- a low-risk proposal caused a dangerous outcome;
- a source is missing or unreliable;
- a counterfactual is being mistaken for observed evidence;
- a promoted pattern no longer matches outcomes.

Promotion and quarantine must be replayable decisions, not hidden edits.

## Provisional Graph Growth

When repeated evidence suggests that the graph itself may need a new route,
rule, edge, or specialist, use
[provisional-graph-growth.md](provisional-graph-growth.md).

Graph runtime memory may hold activation, support, risk, shadow scores,
probation status, quarantine status, and rollback evidence for candidate graph
structure. It may not silently mutate the durable graph. Durable structure
changes require an explicit growth patch, promotion gate, and rollback policy.

## Counterfactual Rule

Counterfactual records are allowed and useful. They can support review,
simulation, planning, or hypothesis generation.

They cannot:

- resolve eligibility as observed success;
- update value as if executed;
- promote semantic or procedural memory without observed evidence;
- overwrite event history.

## Validation Questions

```text
1. Which committed path opened eligibility?
2. Which observed outcome resolved it?
3. What memory role changed?
4. Does the memory affect future operation, or is it only a stored note?
5. Are raw terms separated from learned weights?
6. Are residual, value, and place/manifold updates evidence-backed?
7. Can promoted memory be traced to repeated or reviewed outcomes?
8. Are counterfactual records blocked from observed-value updates?
9. Can replay rebuild the memory projection?
10. What happens to this memory when the world it describes changes?
```

## Measured Example

[applications/bots/memory-ablation.md](../applications/bots/memory-ablation.md)
removes memory from a small maze controller and measures the difference. Kept
memory reaches the shortest path in a stable maze. In a maze that changes
between episodes, memory that never decays is far worse than no memory.
