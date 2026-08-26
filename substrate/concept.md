# Substrate Concept

Substrate is the CGF layer for declaring graph-shaped computational subjects as
graph, typed field, placement, state, action, constraint, evolution, readout,
and validation.

It is a problem declaration layer. It is not a graph library, operating
architecture, solver, SDK, or application framework.

Substrate exists so different domains can describe what is being computed before
deciding how to orchestrate work, which model to train, which solver to call, or
which product experience to build.

## Plain-Language Contract

Every Substrate subject should answer:

```text
What is the graph?
What quantities live on it?
Where do they live?
What state do they have now?
What action, cost, law, or objective governs them?
What is constrained?
How does state evolve?
What answer is read out?
How is the result validated?
```

If a subject cannot answer those questions, it is not yet ready to become an
Architecture system, Application, or package.

## Why Graph Alone Is Not Enough

Most graph systems begin with nodes, edges, and features. That is useful, but it
is not enough to define computation.

A graph says where things can relate. It does not by itself say what quantities
exist, where they live, what law or cost governs them, how state changes, what
answer should be returned, or how to trust the result.

Substrate adds the missing structure:

```text
graph
typed field
placement
state
action
constraint
evolution
readout
validation
```

The graph gives support. Fields give meaning. Placement prevents invalid
operations. Action makes the subject computable. Constraints make it admissible.
Evolution changes state. Readout creates the answer. Validation makes the answer
trustworthy.

## The 9 Core Primitives

These primitives are mandatory for every Substrate subject.

| Primitive | Required? | Question | Minimal meaning | Failure if missing |
| --- | --- | --- | --- | --- |
| Graph | Yes | What things exist, and how can they interact? | Nodes, edges, labels, weights, directions, identifiers. | The subject has no declared interaction structure. |
| Typed field | Yes | What quantities live on the graph? | Scalar, vector, tensor, density, probability, feature, phase, risk, or other typed value. | Values become untyped features with unclear meaning. |
| Placement | Yes | Where does each quantity live? | Node, edge, face, cell, path, mode, region, or other support. | Quantities can be combined even when their supports do not match. |
| State | Yes | What values exist now? | Field values at a tick, step, sample, trajectory, or episode. | The subject has a schema but no computable condition. |
| Action | Yes | What behavior is preferred, minimized, preserved, explained, or optimized? | Cost, energy, loss, risk, information, control, law, or transition contribution. | There is no declared reason to score, move, solve, or choose. |
| Constraint | Yes | What must not be violated? | Hard rule, soft penalty, admissibility condition, policy limit, or domain restriction. | Invalid states can look as acceptable as valid ones. |
| Evolution | Yes | How does state change? | Descent, integration, search, message passing, policy step, solver step, or update rule. | The subject can be described but not advanced or solved. |
| Readout | Yes | What answer is extracted? | Score, label, trajectory, action, diagnosis, solution, report, ranking, or decision candidate. | The computation may run but does not produce a domain answer. |
| Validation | Yes | How is the result trusted? | Checks for constraints, stability, reproducibility, declared pass/fail rules, or expected behavior. | Results cannot be distinguished from invalid or unstable outputs. |

For full core primitive explanations, read [primitives.md](primitives.md).

## Progressive Explanation

### 1. Graph alone is not enough

Nodes and edges describe relationships. They do not declare what computation is
supposed to mean.

### 2. Typed fields give graph state meaning

Fields say what quantities live on the graph. A temperature field, phase field,
risk field, belief field, and control field should not be treated as identical
node features.

### 3. Placement prevents invalid computation

Placement says where a field lives. Node-placed values, edge-placed values,
path-placed values, and region-placed values obey different rules.

### 4. Action makes the subject computable

Action is the organizing object. It declares the cost, law, energy, risk, loss,
information objective, or control contribution that tells the system what
behavior is preferred.

### 5. Constraints make it admissible

Constraints say what must not be violated. They separate possible states from
valid states.

### 6. Evolution changes state

Evolution declares how state moves: descent, integration, search, message
passing, solver step, policy step, or another update.

### 7. Readout creates the domain answer

Readout turns state or trajectory into the answer the domain needs.

### 8. Validation makes the result trustworthy

Validation checks that the declared constraints, state changes, readout, and
pass/fail rules hold.

The core contract stops at the 9-core model. Non-core mechanics and optional
components live in [derivatives/README.md](derivatives/README.md) and
[extensions/README.md](extensions/README.md).

## Heat Relaxation Walkthrough

This example shows all 9 core primitives.

| Primitive | Heat relaxation subject |
| --- | --- |
| Graph | A line of connected nodes. |
| Typed field | Temperature as a scalar field. |
| Placement | Temperature is placed on nodes. |
| State | Current temperature value at each node. |
| Action | Neighboring temperatures should be smooth. |
| Constraint | First node fixed hot, last node fixed cold. |
| Evolution | Repeatedly update temperatures to reduce the smoothness action. |
| Readout | Final temperature profile. |
| Validation | Endpoint constraints remain fixed and no step becomes unstable. |

The same pattern can describe other domains by changing the graph, typed field,
placement, state, action, constraint, evolution, readout, and validation.

## Boundary With Other CGF Layers

```text
Substrate = what is computed.
Architecture = how CGF systems operate around it.
Research = deeper theory and reference status.
Labs = experiments and CGF-local evals.
Applications = domain-specific use.
```

Substrate does not own orchestration machinery, adaptive policy state, ordered
activity records, product behavior, or mandatory package structure.

Architecture can use Substrate subjects. Research can study them. Labs can test
them. Applications can use, copy, fork, or ignore CGF patterns.

## Readiness Checklist

A subject is ready to move beyond Substrate when it can answer:

```text
1. What is the graph?
2. What typed field declarations live on it?
3. Where are those fields placed?
4. What is the current state?
5. What action, cost, law, or objective governs it?
6. What constraint rules apply?
7. How does state evolve?
8. What readout produces the answer?
9. What validates the result?
```

If those answers are vague, Architecture and Applications will carry meaning
that belongs in the Substrate.
