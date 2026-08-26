# Validation

## One Sentence

Validation declares how the subject and result are checked.

## Question It Answers

How do we know the result is acceptable?

## Required Status

Core. Required for every Substrate subject.

## Minimum Declaration

- What is checked.
- When it is checked.
- What passes.
- What fails.
- What evidence is shown.

## Allowed Examples

- Endpoint values remain fixed.
- Assignment rules hold and score matches selected edges.
- Anomaly score uses only declared observed state.
- Checkout success has valid cart, valid payment, and created order state.

## Validation Questions

- Are pass and fail conditions explicit?
- Can checks be performed from declared state?
- Does validation catch invalid state, invalid state change, and invalid readout?
- Is failure evidence clear enough to inspect?

## Common Mistakes

- Treating output as valid because a process finished.
- Checking only the final answer.
- Using vague success language instead of pass/fail checks.
- Letting validation depend on hidden state.

## Heat Example

Endpoint temperatures remain unchanged, the update remains stable, and the final
profile is readable as one temperature value per node.

## Related Core Primitives

Constraint, state, evolution, readout.

