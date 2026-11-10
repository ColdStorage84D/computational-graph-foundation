# Gauge Transport Eval

Status: `contract-pass`

This eval tests frame-aware transport over typed vector state.

## Contract

- Declared frames have explicit bases.
- Transport maps move state between compatible frames.
- Composition matches two-step transport.
- Inverse transport round trips valid square maps.
- Invalid dimensions and singular inverses are rejected.
- Holonomy exposes closed-loop mismatch.
- Source references remain visible through composition.

## Comparison

`comparison.py` builds rings of nodes that report a shared quantity in their
own rotated frames, plants a few genuine disagreements, and asks each arm to
flag the disagreeing edges. The baseline compares raw coordinates. The variant
transports along the declared map first. Further regimes align all frames,
and corrupt the declared maps in two different ways.

## Connections

- Substrate: [gauge transport](../../../substrate/extensions/cards/gauge-transport.md).
- Research: [gauge transport study](../../../research/extension-studies/gauge-transport.md).
- Result record: [results.md](results.md).

## Files

- [eval.py](eval.py): the implementation under test.
- [test_eval.py](test_eval.py): contract tests.
- [comparison.py](comparison.py): seeded comparison against the baseline.
- [test_comparison.py](test_comparison.py): thresholds for the comparison.
- [fixtures/README.md](fixtures/README.md): fixture description.
