# Action, Constraint, Evolution, Readout, Validation

This page defines the contract for the behavioral and result core primitives.
These primitives say what the subject prefers, what is invalid, how state
changes, what answer is returned, and how the answer is checked.

## Action

Action declares the cost, law, objective, risk, preference, or rule of behavior
that governs the subject.

### Required declaration

- Behavior being preferred or minimized.
- Field values involved.
- Graph support involved.
- Direction of preference.
- Domain meaning.

### Allowed examples

- Neighboring temperatures should become smoother.
- Lower-cost valid assignments are preferred.
- Suspicious activity should receive higher risk.
- A valid checkout path should create an order while preserving customer safety.

### Validation questions

- Is the preferred behavior stated explicitly?
- Can the action be evaluated from declared graph state?
- Is the action separate from the final readout?

### Common mistakes

- Running updates without naming what they serve.
- Treating a score as meaningful without declaring what it means.
- Mixing unrelated preferences without naming their relationship.

## Constraint

Constraint declares what must not be violated.

### Required declaration

- Rule being enforced.
- Scope of the rule.
- Whether failure rejects the subject, rejects a state, or rejects a result.
- Meaning of failure.

### Allowed examples

- Endpoint temperatures must remain fixed.
- Each task can be assigned at most once.
- Missing evidence cannot be treated as confirmed behavior.
- An order cannot be created from an invalid cart.

### Validation questions

- Is every invalid condition explicit?
- Can each rule be checked against declared state?
- Are hard rules separated from preferred behavior?

### Common mistakes

- Encoding a hard rule as a preference.
- Declaring rules but never checking them.
- Allowing a readout that violates a rule.

## Evolution

Evolution declares how state changes.

### Required declaration

- Starting state.
- Allowed state change.
- Inputs used by the state change.
- Resulting state.
- Checks that must hold after state changes.

### Allowed examples

- Interior temperatures move toward neighboring temperatures.
- Assignment state changes by trying a different valid edge selection.
- Risk state updates when new events arrive.
- Checkout state moves from submitted to priced, authorized, ordered, or failed.

### Validation questions

- Is the state change rule explicit?
- Does the resulting state still satisfy constraints?
- Is one step separated from final readout?

### Common mistakes

- Mutating state without declaring the change.
- Letting state changes bypass constraints.
- Treating a state change as a final answer.

## Readout

Readout declares the domain answer extracted from state or a sequence of states.

### Required declaration

- Input state or sequence.
- Output kind.
- Domain interpretation.
- How the answer should be consumed.

### Allowed examples

- Final temperature profile.
- Best valid assignment and score.
- Ranked anomaly list.
- Checkout decision and customer-visible status.

### Validation questions

- Is the answer useful to the domain?
- Does the answer come from declared state?
- Is readout separate from state mutation?

### Common mistakes

- Returning internal state with no domain interpretation.
- Returning a number without explaining what it means.
- Changing state during readout.

## Validation

Validation declares how the subject and result are checked.

### Required declaration

- What is checked.
- When it is checked.
- What passes.
- What fails.
- What evidence is shown.

### Allowed examples

- Endpoint values remain fixed.
- Assignment rules hold and score matches selected edges.
- Anomaly score uses only declared observed state.
- Checkout success has valid cart, valid inventory, valid payment, and created
  order state.

### Validation questions

- Are pass and fail conditions explicit?
- Can validation be checked from declared graph state?
- Does validation catch invalid state, invalid change, and invalid readout?

### Common mistakes

- Treating output as valid because a process finished.
- Checking only the final answer.
- Using vague success language instead of pass/fail checks.

## Rule

Action, constraint, evolution, readout, and validation must be declared before a
subject is treated as complete.

