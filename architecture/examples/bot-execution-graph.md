# Bot Execution Graph

This example shows a bot-shaped Architecture without making CGF an agent
framework.

The useful split is:

```text
Substrate subject = what the bot is acting over
execution graph = how the bot routes, proposes, gates, commits, observes, and learns
```

## Surface

A small bot execution graph may contain:

```text
intake node
state encoder
path view builder
proposal node
path-conditioned scorer
path gate
verifier
commit node
action adapter
outcome reader
memory update projection
replay projection
```

The brain coordinates the phases. The spine routes records between nodes. Local
specialists can be wrapped as subgraph capsules when they need their own graph
detail.

## Operating Path

```text
event
-> path view
-> candidate actions
-> path-conditioned score
-> path gate
-> verifier
-> commit or review
-> action adapter
-> observed outcome
-> eligibility resolution
-> value, residual, inhibition, or uncertainty memory update
-> replayable trace
```

## Path-Conditioned Use

The scorer may use path context such as:

- recent route;
- evidence chain;
- place or task region;
- outcome-backed failure context;
- support count;
- uncertainty.

This can change action ranking or verifier threshold. It does not authorize the
action.

## Path-Gated Use

A gate may block, defer, review, fallback, or abstain when:

- the path is unknown;
- required evidence is absent;
- the action previously failed in a similar path;
- the proposal crosses a policy boundary;
- the local subgraph capsule reports contradiction.

The gate basis and blocked reason must appear in trace.

## Graph Runtime Memory

The bot may carry agent/project notes, but those notes are not graph runtime
memory by default.

Graph runtime memory updates only after:

```text
commit -> eligibility -> observed outcome -> memory update
```

The update may affect future operation as value, inhibition, residual,
place/manifold, semantic/procedural, quarantine, or counterfactual memory,
depending on the declared role.

## Validation Questions

```text
1. Which Substrate subject is the bot operating around?
2. Which node owns each local transform?
3. Does the spine route records without hiding authority?
4. Does path conditioning influence only declared effect surfaces?
5. Does a gate preserve basis, result, and blocked reason?
6. Does commit create eligibility before memory update?
7. Can replay rebuild the trace without hidden process state?
```
