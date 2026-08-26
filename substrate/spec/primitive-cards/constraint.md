# Constraint

## One Sentence

Constraint declares what must not be violated.

## Question It Answers

What states, changes, or answers are invalid?

## Required Status

Core. Required for every Substrate subject.

## Minimum Declaration

- Rule being enforced.
- Scope of the rule.
- Whether failure rejects the subject, state, or result.
- Meaning of failure.

## Allowed Examples

- Endpoint temperatures must remain fixed.
- Each task can be assigned at most once.
- Missing evidence cannot be treated as confirmed behavior.
- An order cannot be created from an invalid cart.

## Validation Questions

- Is every invalid condition explicit?
- Can each rule be checked against declared state?
- Are hard rules separated from preferred behavior?
- Is failure meaning clear?

## Common Mistakes

- Encoding a hard rule as a preference.
- Declaring rules but never checking them.
- Allowing a readout that violates a rule.
- Treating a warning as a rule without saying so.

## Heat Example

The first node remains hot and the last node remains cold.

## Related Core Primitives

Graph, state, action, evolution, validation.

