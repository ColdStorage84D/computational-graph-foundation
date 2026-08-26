# Readout

## One Sentence

Readout declares the domain answer extracted from state or a sequence of states.

## Question It Answers

What result does the domain need?

## Required Status

Core. Required for every Substrate subject.

## Minimum Declaration

- Input state or sequence.
- Output kind.
- Domain interpretation.
- How the answer should be consumed.

## Allowed Examples

- Final temperature profile.
- Best valid assignment and score.
- Ranked anomaly list.
- Checkout decision and customer-visible status.

## Validation Questions

- Is the answer useful to the domain?
- Does the answer come from declared state?
- Is readout separate from state change?
- Is the output meaning clear?

## Common Mistakes

- Returning internal state with no domain interpretation.
- Returning a number without explaining what it means.
- Changing state during readout.
- Producing multiple answers without naming which one the domain needs.

## Heat Example

The final temperature profile is the readout.

## Related Core Primitives

State, evolution, validation.

