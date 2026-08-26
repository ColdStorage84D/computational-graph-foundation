# Evolution

## One Sentence

Evolution declares how state changes.

## Question It Answers

How does the subject move from one state to another?

## Required Status

Core. Required for every Substrate subject.

## Minimum Declaration

- Starting state.
- Allowed state change.
- Inputs used by the state change.
- Resulting state.
- Checks that must hold after state changes.

## Allowed Examples

- Interior temperatures move toward neighboring temperatures.
- Assignment state changes by trying a different valid edge selection.
- Risk state updates when new activity arrives.
- Checkout state moves from submitted to priced, ordered, or failed.

## Validation Questions

- Is the state change rule explicit?
- Does the resulting state still satisfy constraints?
- Is one step separated from final readout?
- Can invalid state changes be rejected?

## Common Mistakes

- Changing state without declaring the rule.
- Letting state changes bypass constraints.
- Treating a state change as the final answer.
- Omitting checks after state changes.

## Heat Example

Interior node temperatures move toward neighboring temperatures while endpoint
constraints remain fixed.

## Related Core Primitives

State, action, constraint, readout, validation.

