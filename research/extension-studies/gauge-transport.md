# Gauge Transport

## Purpose

Gauge transport studies how typed state moves across local frames or
representation contexts.

Core pattern:

```text
state in frame A
  -> declared connection or transport map
  -> state in frame B
  -> residual or holonomy check
```

## Failure Mode

Without gauge transport, two values may be compared as if they share the same
basis when they do not.

Common failures:

- local coordinate frames are ignored;
- a non-invertible transform is treated as reversible;
- transported state loses evidence refs;
- round-trip mismatch is hidden;
- closed-path mismatch is mistaken for ordinary noise.

## Minimum Substrate Addition

Minimum records:

```text
frame
  frame_id
  support_ref
  basis_kind
  basis_ref
  evidence_refs
  uncertainty

connection
  connection_id
  source_frame_ref
  target_frame_ref
  transport_rule_ref
  parameters
  uncertainty
```

The state remains a typed field. Gauge transport declares how that field is
represented and moved across frames.

## Conceptual Checks

- Identity transport preserves state.
- Composed transport matches direct transport when both are valid.
- Round-trip transport exposes residual.
- Missing frame declaration blocks comparison.
- Closed-path transport can expose holonomy.
- Residuals remain visible after transport.

## Relationship To Nearby Extensions

- Metric placement gives distances; gauge transport gives frame changes.
- Sheaf consistency compares overlaps; gauge transport may be required before
  comparison.
- Higher-dimensional topology can provide the paths or cycles used for
  holonomy checks.
- Information geometry can measure belief changes after transported evidence
  is aligned.

## Validation Questions

- Is each local frame declared before transport?
- Is the transport rule versioned and typed?
- Are source and target supports compatible?
- Are lossy transforms marked as lossy?
- Is residual surfaced instead of hidden?
- Is holonomy treated as diagnostic evidence, not automatic failure?

## Maturity

Status: research-supported; CGF-local eval `contract-pass`.

The concept is mature enough for an extension card and deeper research study.
Production-quality construction of correspondences and calibration remains
future work.

## CGF Eval Result

See [../../labs/evals/gauge-transport/results.md](../../labs/evals/gauge-transport/results.md).

## References

Public sources for local frames, transport, and holonomy on discrete structures.

- [Geometric Deep Learning: Grids, Groups, Graphs, Geodesics, and Gauges](https://arxiv.org/abs/2104.13478), Bronstein, Bruna, Cohen, and Velickovic (2021). Gauges and frame choices as a design principle for computation on manifolds and graphs.
- [Gauge Equivariant Convolutional Networks and the Icosahedral CNN](https://arxiv.org/abs/1902.04615), Cohen, Weiler, Kicanaoglu, and Welling (2019). Transporting features between local frames before combining them.
- [Vector Diffusion Maps and the Connection Laplacian](https://arxiv.org/abs/1102.0075), Singer and Wu (2011). The connection Laplacian: comparing vectors across nodes through orthogonal transport maps.
