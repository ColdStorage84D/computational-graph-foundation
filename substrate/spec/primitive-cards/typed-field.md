# Typed Field

## One Sentence

Typed field declares what kind of quantity lives on the graph.

## Question It Answers

What values exist on the subject?

## Required Status

Core. Required for every Substrate subject.

## Minimum Declaration

- Field name.
- Value kind.
- Shape, category, or range when relevant.
- Domain meaning.
- Allowed placement.

## Allowed Examples

- Temperature as a scalar.
- Assignment as a binary value.
- Risk score as a scalar.
- Cart status as a category.
- Item quantity as an integer.

## Validation Questions

- Is the field meaning clear without application code?
- Are unlike quantities declared as separate fields?
- Is the value kind specific enough to reject invalid values?
- Is allowed placement named separately?

## Common Mistakes

- Calling every value a feature.
- Mixing unrelated quantities in one field.
- Letting a field name imply placement.
- Declaring a value type without domain meaning.

## Heat Example

Temperature is a scalar typed field.

## Related Core Primitives

Graph, placement, state, action, readout, validation.

