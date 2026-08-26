# Derivative Mechanics Study

## Purpose

This study records the deeper research direction behind Substrate derivative
mechanics.

Core primitives declare the subject. Derivative mechanics explain how a
complete subject can become equations, operators, residuals, solver choices,
or implementation-ready checks without turning Substrate into a solver library.

## Core Thesis

CGF should not make every domain-specific solver a primitive.

It should declare enough structure for computation to be derived:

```text
typed fields + placement + units
+ local action or law
+ constraints + boundaries + sources
+ variation
+ operator assembly
+ invariants + residuals
-> evolution, readout, and validation
```

The result may be implemented later with numerical libraries, learned
surrogates, differentiable frameworks, or hand-written kernels. Those are
execution choices, not the conceptual source of the computation.

## Action-Native Computation

Action-Native Computation is the research framing for computation as
constrained graph-state evolution.

The useful public claim is:

```text
mathematical results are readouts of declared graph-state evolution under
actions, laws, constraints, residuals, and validation
```

This keeps the claim concrete. A graph does not calculate because it is a graph.
It calculates when the subject declares the state, the action or law that drives
change, the allowed changes, the constraints, the residual or error check, and
the validation rule for accepting a readout.

The current calculation families are:

| Family | Research question |
| --- | --- |
| Relaxation / settling | Does repeated evolution reduce or preserve the declared action while constraints remain satisfied? |
| Constraint satisfaction | Can candidate states be accepted only when declared constraints and residual checks pass? |
| Optimization / least-action path | Can admissible paths or state sequences be compared by declared action without hidden scoring? |
| Learned surrogate | Can learned updates remain bounded by visible residuals and validation? |
| Analog or physical realization | Can a physical process realize a declared law without replacing validation? |

Analog or physical computation is treated as a possible realization, not a
required implementation route and not a broad claim.

Current eval support: the CGF-local Action-Native Computation eval has a
tiny-fixture `contract-pass` for relaxation / settling, constraint
satisfaction, and least-action path. The result supports only the local
contract; it does not prove solver quality, physics accuracy, global
optimization, broad mathematical capability, or analog-computing performance.

## Derivative Components

| Component | Research role |
| --- | --- |
| Units / dimensions | Reject invalid equations and incompatible action terms. |
| Boundary | Make the declared subject well-posed at its edge, time start, or interface. |
| Source | Separate external forcing, injection, sinks, and observations from durable state. |
| Local action / Lagrangian | Provide the local law, cost, energy, or objective that can generate dynamics. |
| Variation | State the admissible perturbation or update family used to derive equations. |
| Operator assembly | Convert placement, measures, and local laws into matrices, stencils, kernels, or graph operators. |
| Invariant | State what must be preserved or checked during evolution. |
| Residual / error estimator | Measure how far a state or update is from satisfying the declared law. |
| Solver selection | Choose an execution family after the derived problem is known. |

## What Derivatives Add To Core Primitives

The 9 core primitives can describe a heat-relaxation subject. Derivative
mechanics make the same subject precise:

```text
field: scalar temperature
placement: node samples on a line
units: temperature, length, time, diffusivity
boundary: fixed endpoints
local action: smoothness energy
variation: node-local admissible update
operator assembly: graph Laplacian
residual: update residual and boundary error
solver selection: explicit, implicit, relaxation, or learned surrogate
```

The important point is that solver choice comes last. A subject should not pick
a solver before its fields, placement, action, constraints, and validation are
clear.

## Stationary Path

Stationary Path is the derivative concept for subjects that use stationary
action, least action, geodesics, variational paths, or residual-based
stationarity.

The research shape is:

```text
complete core subject
+ local action or Lagrangian
+ admissible variation
+ constraints, boundaries, and sources when relevant
+ residual / error estimator
-> candidate path, trajectory, state sequence, or field evolution
```

The stationary path condition says that the action has no admissible
first-order improvement under the declared variations. It does not by itself
prove shortest path, global optimum, or broad physical accuracy.

This concept ties together the existing derivative mechanics:

| Mechanic | Stationary Path role |
| --- | --- |
| Local action / Lagrangian | Defines what quantity is stationary. |
| Variation | Defines which changes are admissible. |
| Constraint | Removes invalid changes from the stationarity test. |
| Boundary / source | Explains fixed, exposed, injected, or removed support that affects the condition. |
| Residual / error estimator | Reports how far the candidate is from satisfying stationarity. |
| Solver selection | Comes after the condition is declared; it does not define stationarity. |

Maturity: docs/research-supported. No direct Labs eval exists yet.

## Relationship To Extensions

Derivative mechanics are method-forming. Extensions are gap-naming.

For example:

- weak form is an extension when pointwise equations are not stable enough;
- exterior placement is an extension when node-only placement destroys
  conservation or circulation;
- differentiable backend is an extension when inverse design, learning, or
  gradients must remain attached to the declared subject.

Derivative mechanics explain how those extensions can become computation.

## Validation Questions

Before a derivative study can influence a public spec, it must answer:

- Are all 9 core primitives already explicit?
- Which derivative component is actually needed?
- What invalid computation does the component prevent?
- What minimum record must be declared?
- What check proves the derived artifact still matches the subject?
- What existing implementation family could execute it later?

## Maturity

Status: research-supported.

The component names are stable enough for Substrate v0.2 docs. Their exact
schemas, algorithms, and implementation conventions remain open.
