# State

## One Sentence

State declares the current values of placed fields.

## Question It Answers

What values does the subject have now?

## Required Status

Core. Required for every Substrate subject.

## Minimum Declaration

- Field values.
- Graph parts carrying those values.
- Current step, sample, or condition when relevant.
- Enough context to know what is being evaluated.

## Allowed Examples

- Current temperature at each node.
- Current selected assignment edges.
- Current account and device risk values.
- Current cart contents, prices, payment status, and order status.

## Validation Questions

- Does every state value correspond to a declared field?
- Does every state value have declared placement?
- Are values from different steps kept separate?
- Is predicted state separated from accepted current state?

## Common Mistakes

- Declaring fields but no actual values.
- Mixing old and new values as one state.
- Treating predicted values as accepted state.
- Omitting the current condition being evaluated.

## Heat Example

Each node has a current temperature:

```text
n0: 100
n1:  60
n2:  40
n3:   0
```

## Related Core Primitives

Typed field, placement, action, evolution, readout, validation.

