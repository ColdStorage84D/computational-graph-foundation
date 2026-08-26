# Sheaf Consistency Eval

Status: `contract-pass`

This eval tests local-to-global agreement using declared supports, restriction
maps, overlap residuals, gluing candidates, and obstructions.

## Connections

- Substrate: [sheaf consistency](../../../substrate/extensions/cards/sheaf-consistency.md).
- Research: [sheaf consistency study](../../../research/extension-studies/sheaf-consistency.md).
- Result record: [results.md](results.md).

## Contract

- Views must be restricted before comparison.
- Agreeing restricted views can glue.
- Conflicting restricted views produce obstruction records.
- Counterfactual status survives comparison.
- No merged view may hide a conflict.

## Files

- [eval.py](eval.py)
- [test_eval.py](test_eval.py)
- [fixtures/README.md](fixtures/README.md)
- [results.md](results.md)
