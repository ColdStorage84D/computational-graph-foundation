# Derivative Mechanics

Derivative mechanics are conditional Substrate components. They are used when a
complete core subject needs a more formal route from declaration to computation.

They do not replace the 9 core primitives:

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

Instead, they refine a complete subject by answering questions such as:

```text
Are units compatible?
What is fixed at the edge of the subject?
What enters or leaves the subject?
What local law or cost is being accumulated?
What changes are allowed?
What operator is assembled from local parts?
What should remain stable?
How is error measured?
Which solving method fits the declared shape?
```

Action-Native Computation is the broad derivative framing for computation as
constrained graph-state evolution. Use
[action-native-computation.md](action-native-computation.md) when the question
is how a graph subject calculates from declared actions, laws, constraints,
evolution, residuals, and validation.

## Mechanics Table

| Mechanic | Question | Typical trigger |
| --- | --- | --- |
| Units / dimensions | Are quantities compatible? | Values from different sources or scales must be combined. |
| Boundary | What is fixed, exposed, or limited at the subject edge? | A subject has endpoints, walls, interfaces, clamps, or external conditions. |
| Source | What quantity enters, leaves, or is externally supplied? | State changes because something is injected, removed, emitted, or observed. |
| Local action / Lagrangian | What local contribution defines the action? | A global action should be built from graph-local terms. |
| Variation | What changes are allowed when deriving behavior? | The action should imply an update, equilibrium, or admissible direction. |
| Operator assembly | How are local declarations composed? | Local rules must become a matrix, transform, update map, or evaluator. |
| Invariant | What should remain stable? | A quantity, relation, or admissibility condition must survive evolution. |
| Residual / error estimator | How far is the current state from satisfying the declared condition? | Approximation, iteration, or incomplete update needs a quality measure. |
| Solver selection | Which method shape fits the declared subject? | Multiple methods could apply and the subject must justify one. |

Action-Native Computation is not a separate mechanic card. It is the review
frame that checks whether the needed mechanics compose into a visible
calculation path.

Stationary Path is a guide that combines local action / Lagrangian, admissible
variation, constraints, and residual checks into one stationarity condition. Use
[stationary-path.md](stationary-path.md) when the subject uses stationary
action, least action, geodesic, variational path, or first-order stationarity
language.

## Derivation Flow

A typical derivative pass is:

```text
1. Start with a complete core subject.
2. Use Action-Native Computation when the subject needs a visible route from
   action, law, constraint, and evolution to readout.
3. Check units / dimensions when quantities interact.
4. Declare boundary and source terms when the subject has external contact.
5. Refine action into local action / Lagrangian terms when needed.
6. Declare variation to define admissible changes.
7. Declare Stationary Path when action, variation, and constraints define a
   first-order stationarity condition.
8. Assemble an operator when local declarations must act globally.
9. Declare invariants that should remain stable.
10. Add residual / error estimation for approximate or iterative work.
11. Select a solver shape only after the subject and checks justify it.
```

Not every subject needs every step. The point is to name the extra structure
honestly instead of forcing it into a core primitive.
