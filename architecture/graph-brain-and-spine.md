# Graph Brain And Spine

## Definition

Graph brain and spine is the Architecture pattern for coordinating a system
made of surface nodes, child graphs, gates, actions, and memory projections
without turning the coordinator into a hidden global controller.

```text
surface nodes -> spine -> surface nodes
brain -> spine-routed phases -> execution graph cycle
```

## Responsibilities

| Part | Responsibility |
| --- | --- |
| Brain | Coordinates phases and asks the execution graph to encode, propose, commit, execute, observe, resolve, and consolidate. |
| Spine | Routes messages, preserves authority boundaries, and keeps node communication traceable. |
| Surface node | Owns a local transform, gate, proposer, verifier, action adapter, memory read, or outcome conversion. |
| Child graph | Owns local detail as a subgraph capsule. |
| Core cycle | Owns commit, outcome coupling, memory update, and replay discipline. |

## Safe Rule

```text
surface nodes own local transforms
child graphs own local detail
spine routes messages
brain coordinates phases
execution graph owns commit/outcome learning
```

This prevents the spine from becoming a giant object where domain behavior,
policy, and memory are hardcoded.

## Node Roles

Execution graphs may use nodes such as:

- sensing or intake nodes;
- processing nodes;
- proposer nodes;
- verifier nodes;
- gate nodes;
- action nodes;
- memory reader nodes;
- outcome nodes;
- review nodes;
- child graph nodes;
- brain and spine nodes.

These are Architecture roles. They do not replace Substrate primitives.

## Runtime Routes And Static Relations

Runtime messages should route through the spine:

```text
surface node -> spine -> surface node
```

Static relations should not masquerade as runtime authority. A robot body
topology, source dependency graph, image region graph, or code AST graph can be
represented as relations, but those relations do not execute side effects by
themselves.

Examples of static relations:

```text
sensor observes body part
limit constrains actuator
source record feeds derived view
finding cites evidence record
cache entry depends on source entity
```

Examples of runtime routes:

```text
observation -> encode node
state -> proposer node
proposal -> verifier node
committed proposal -> action node
execution result -> outcome node
outcome -> memory update projection
```

## Boundary

The brain may coordinate. It may not bypass commit.

The spine may route. It may not decide hidden policy.

Surface nodes may compute. They may not mutate durable memory unless an
outcome-resolved memory update authorizes that mutation.

## Validation Questions

```text
1. Is there one visible routing boundary?
2. Are local transforms owned by named nodes?
3. Are static relations separated from runtime routes?
4. Can child graphs be traced as subgraph capsules?
5. Does commit remain the authority boundary?
6. Can memory updates be traced to committed outcomes?
```
