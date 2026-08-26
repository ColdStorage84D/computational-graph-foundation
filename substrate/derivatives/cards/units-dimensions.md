# Units / Dimensions

## Definition

Units / dimensions declare the measurement scale and dimensional compatibility
of typed fields.

## Question it answers

Can these quantities be compared, combined, accumulated, or transformed without
losing meaning?

## Depends on core primitives

Typed field, placement, state, action, validation.

## Minimum declaration

- Field being measured.
- Unit or dimension family.
- Conversion rule when multiple scales appear.
- Compatibility rule for operations.
- Validation check for invalid combinations.

## When to use

- Fields come from different instruments, systems, or scales.
- Action combines unlike quantities.
- Readout depends on comparable magnitudes.
- Validation must catch unit mistakes.

## Common failure

Numbers are combined because their shapes match, even though their units or
dimensions do not.
