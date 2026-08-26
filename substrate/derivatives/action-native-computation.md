# Action-Native Computation

Action-Native Computation is the Substrate derivative framing for computation
as constrained graph-state evolution.

The public claim is:

```text
mathematical results are readouts of declared graph-state evolution under
actions, laws, constraints, residuals, and validation.
```

This is stronger and cleaner than saying that mathematics simply appears from a
graph. The graph does not compute by itself. A CGF subject computes only after
it declares what state exists, what action or law governs change, what changes
are allowed, what is constrained, what residual or error is visible, and what
validation accepts the readout.

## Why This Exists

Many projects start by asking for a formula, solver, model, or calculator. CGF
starts earlier:

```text
complete Substrate subject
+ declared action, law, or objective
+ constraints and admissible changes
+ evolution rule
+ residual or error check
+ validation
-> readout
```

Action-Native Computation names that pattern. It lets a developer describe a
calculation as graph-state evolution before choosing a numerical method,
symbolic method, learned surrogate, or physical realization.

## Required Ingredients

Start with the 9 core primitives:

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

Then add only the derivative mechanics that are needed:

| Ingredient | Role |
| --- | --- |
| Action or law | Defines what drives change or what should be reduced, preserved, satisfied, or optimized. |
| Constraints | Declare invalid states, invalid transitions, fixed values, or admissibility limits. |
| Evolution | Applies the declared action or law to update graph state. |
| Variation | Defines which changes are allowed when deriving a direction or condition. |
| Operator assembly | Builds a global update, evaluator, or transform from local declarations when needed. |
| Invariant | States what must remain stable during evolution. |
| Residual / error estimator | Reports how far the current state or readout is from satisfying the declared law. |
| Solver selection | Comes after the subject and checks justify a method family. |

## Calculation Families

Action-Native Computation can describe several calculation styles without
turning any one style into a CGF requirement.

| Family | Shape | Example readout |
| --- | --- | --- |
| Relaxation / settling | Repeated evolution reduces or preserves a declared action. | A smoothed field that passes residual and boundary checks. |
| Constraint satisfaction | Candidate state changes are accepted only if constraints and residual checks pass. | A valid assignment, labeling, schedule, or layout. |
| Optimization / least-action path | Candidate paths or state sequences are compared by declared action under constraints. | A lowest declared-action path among admissible candidates. |
| Learned surrogate | A learned component proposes or approximates an update while residual and validation remain visible. | A predicted update accepted only inside declared error limits. |
| Analog or physical realization | A physical process realizes the evolution rule, but the declared law and validation still define the computation. | A measured final state accepted only if checks pass. |

Analog or physical computation is an implementation example, not a requirement
and not a special CGF promise.

## Relation To Stationary Path

[Stationary Path](stationary-path.md) is one specific derivative condition
inside Action-Native Computation.

Use Stationary Path when the subject says a path, trajectory, state sequence, or
field evolution should have no admissible first-order improvement under the
declared action and variation.

Use Action-Native Computation when the broader question is:

```text
How does this graph subject calculate anything from its declared action, law,
constraints, residual, and validation?
```

## What It Is Not

Action-Native Computation is not:

- a new core primitive;
- a universal calculator;
- a hidden solver;
- a hidden physical law;
- a theory-of-everything claim;
- a proof that any graph will produce valid mathematics;
- a reason to accept a readout without residual and validation.

## Minimum Declaration

A subject using this framing should state:

- the complete 9-core Substrate declaration;
- the action, law, cost, energy, or objective that drives computation;
- which changes are admissible;
- which constraints block invalid state or invalid evolution;
- the evolution step or comparison rule;
- the residual or error check;
- the validation rule for accepting the readout;
- what implementation family is being used, if one is chosen.

## Common Failures

- The graph structure is declared, but no action or law drives computation.
- A solver is named before the subject declares fields, placement, constraints,
  residuals, and validation.
- A hidden force, source, label, or scoring rule changes the result without
  being declared.
- A readout is accepted because it looks plausible, without a residual or
  validation check.
- A learned or physical process is treated as self-validating.
- A least-action or stationary result is overclaimed as global optimality.

## Maturity

Status: tiny-fixture `contract-pass`.

The CGF-local eval covers relaxation / settling, constraint satisfaction, and
least-action path fixtures. It supports the local contract that computation
needs declared action or law, constraints, evolution, residual/error,
validation, and readout.

It does not prove physics accuracy, solver quality, global optimization, broad
mathematical capability, autonomous reasoning, or analog-computing performance.
