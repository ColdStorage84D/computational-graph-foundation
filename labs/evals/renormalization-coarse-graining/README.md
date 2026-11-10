# Renormalization / Coarse-Graining Eval

Status: `contract-pass`

This eval has two layers.

The model layer is real-space renormalization of a conductance network.
Eliminating a node replaces it with renormalized couplings among its
neighbours:

```text
new coupling between neighbours i and j:   w_i * w_j / (sum of all w at the node)
current injected at the eliminated node:   shared to neighbours in proportion to w
```

This is the Schur complement of the graph Laplacian. The coarse network
reproduces the fine network's response at every kept node.

The record layer keeps source references and a fine/coarse residual visible
when a coarse summary is reported.

## Fixtures

Chains with uniform and with seeded random couplings, and ladders of three to
five rungs.

## Contract

- Eliminating the middle of a two-edge chain gives the series coupling.
- A coarse ladder reproduces the fine response on the kept nodes, and gains
  couplings the fine ladder never had.
- Dropping eliminated nodes without renormalizing gives a different answer.
- On a uniform chain the coupling halves at every step while coupling times
  segment length stays fixed.
- On a disordered chain five rounds of coarse-graining leave the end-to-end
  response unchanged.
- A source on an eliminated node must be renormalized too. Ignoring it changes
  the response.
- Unknown kept nodes, fewer than two kept nodes, non-positive couplings, and
  odd chains are rejected.

## Connections

- Substrate: [renormalization / coarse-graining](../../../substrate/extensions/cards/renormalization-coarse-graining.md).
- Research: [renormalization / coarse-graining study](../../../research/extension-studies/renormalization-coarse-graining.md).
- Result record: [results.md](results.md).

## Files

- [eval.py](eval.py): network renormalization and the summary records.
- [test_model.py](test_model.py): tests for network renormalization.
- [test_eval.py](test_eval.py): tests for the summary records.
