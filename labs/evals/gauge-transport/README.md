# Gauge Transport Eval

Status: `contract-pass`

This eval tests frame-aware transport over typed vector state.

## Connections

- Substrate: [gauge transport](../../../substrate/extensions/cards/gauge-transport.md).
- Research: [gauge transport study](../../../research/extension-studies/gauge-transport.md).
- Result record: [results.md](results.md).

## Contract

- Declared frames have explicit bases.
- Transport maps move state between compatible frames.
- Composition matches two-step transport.
- Inverse transport round trips valid square maps.
- Invalid dimensions and singular inverses are rejected.
- Holonomy exposes closed-loop mismatch.
- Source references remain visible through composition.

## Files

- [eval.py](eval.py): tiny implementation under test.
- [test_eval.py](test_eval.py): contract tests.
- [fixtures/README.md](fixtures/README.md): fixture description.
- [results.md](results.md): reviewed result.
