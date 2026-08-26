# Stationary Path

Stationary Path is a Substrate derivative guide for subjects where a path,
trajectory, state sequence, or field evolution is judged by whether the
declared action has no admissible first-order improvement under the allowed
variations and constraints.

It is not a core primitive, a shortest-path rule, a solver, an operating path,
or a guarantee of global optimality.

## Definition

A stationary path is a candidate path whose action does not change to first
order under the variations that the subject declares as admissible.

In plain language:

```text
action + admissible variation + constraints
-> no local first-order improvement
-> residual or stationarity check
```

The path can be a geometric path, a time-indexed trajectory, an iterative state
sequence, or a field evolution. The important point is not that it is shortest
or best overall. The important point is that the subject has declared what may
change and the path passes the local stationarity check for those changes.

## Required Ingredients

Start with a complete core subject:

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

Then add the derivative mechanics needed for stationarity:

| Ingredient | Meaning |
| --- | --- |
| Local action / Lagrangian | The cost, law, energy, loss, or objective being tested. |
| Variation | The admissible changes used to ask whether the action can improve locally. |
| Constraint | The restrictions that make some changes invalid. |
| Boundary / source, when needed | External support, endpoints, forcing, or fixed values that affect admissible changes. |
| Residual / error estimator | The visible mismatch from the declared stationarity condition. |
| Validation | The rule that says whether the residual and constraints are acceptable. |

## Minimum Declaration

A Stationary Path declaration should state:

- the candidate path, trajectory, state sequence, or field evolution;
- the action being tested;
- the field or state components that may vary;
- the support where variation is allowed;
- constraints that restrict the variation;
- boundary or source terms when they affect the path;
- the stationarity condition or residual being checked;
- the threshold, comparison rule, or validation record used for acceptance.

## Examples

### Heat Relaxation

- Path: a sequence of temperature fields on a graph.
- Action: smoothness energy over neighboring nodes.
- Variation: node-local changes on non-fixed nodes.
- Constraint: fixed endpoint values remain fixed.
- Stationarity check: interior values stop improving under allowed local
  changes.
- Residual: mismatch between each interior value and the neighbor-supported
  condition.

The stationary result is not "the only possible computation." It is the field
state that satisfies the declared smoothness condition under the declared fixed
endpoints.

### Graph Optimization

- Path: a sequence of graph states or assignments.
- Action: declared objective over nodes, edges, or regions.
- Variation: allowed local edits to the assignment.
- Constraint: invalid labels, capacities, or compatibility rules are excluded.
- Stationarity check: no allowed local edit gives a first-order improvement.
- Residual: remaining local objective violation or blocked-improvement report.

This may still be a local stationary point. It should not be described as a
global optimum unless a separate global check is declared.

### Trajectory Or Control Subject

- Path: a time-indexed state and action sequence.
- Action: effort, tracking cost, safety cost, or physical action integral.
- Variation: small admissible changes to state or action along the sequence.
- Constraint: action limits, endpoint conditions, obstacle exclusions, or
  admissible dynamics.
- Stationarity check: the candidate sequence satisfies the declared local
  optimality or least-action condition.
- Residual: violation of the local condition, constraints, or endpoint terms.

The stationary path is not the same as an operating path through a software
system. It is a mathematical candidate inside the declared subject.

### Field Evolution

- Path: a field evolving across graph support, cells, regions, or mode nodes.
- Action: field law, energy, or loss accumulated over the support.
- Variation: admissible changes to the field, coefficients, or local values.
- Constraint: conservation, compatibility, boundary, or mode-coupling rules.
- Stationarity check: first-order change vanishes under allowed field
  variations.
- Residual: field-law mismatch, conservation error, or reconstruction error.

Stationarity can be useful even when the final implementation uses an
iterative method, a learned surrogate, or a hand-written evaluator.

## What It Is Not

| Confusion | Correction |
| --- | --- |
| Shortest path | A stationary path need not minimize distance or hop count. |
| Global optimum | Stationarity is usually local unless a stronger proof is declared. |
| Any equilibrium | Equilibrium may be static for many reasons; Stationary Path requires an action and admissible variation. |
| A solver | Solver selection comes after the stationary condition is declared. |
| A system-operation path | Stationary Path belongs to Substrate derivative mechanics, not Architecture operation. |

## Common Failure Modes

- The action is named, but the allowed variation is not declared.
- Every change is treated as admissible even when constraints forbid it.
- Boundary or source terms are omitted even though they affect stationarity.
- A local stationary condition is described as a global optimum.
- The result is accepted without a residual, error estimator, or validation
  record.
- The path is mixed with system-operation, evidence-routing, or application UI
  flow instead of staying inside the declared computational subject.

## Maturity

Status: docs/research-supported.

No direct Labs eval exists yet. Use Stationary Path as a declaration and
review guide until a section-local eval or implementation is added.
