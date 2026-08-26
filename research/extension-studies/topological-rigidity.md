# Topological Rigidity

## Purpose

Topological rigidity studies how a graph subject protects declared cycles,
explicit phase structure, rare regimes, and transition regions from collapse
during smoothing, compression, embedding, or learning. This is an independent
CGF research study: its public claims stand on its own declarations, public
references, and evals rather than on an unpublished physical analogy.

## Failure Mode

A model can preserve local similarity while destroying global structure.

Common failures:

- dimension reduction turns a loop into a line;
- rare branches collapse into common clusters;
- periodic regimes lose phase information;
- transition states merge with endpoints;
- learned operators do not preserve declared cycle or phase diagnostics;
- summaries erase cycles that matter to validation.

## Minimum Substrate Addition

The extension can add a typed carrier placement and declared topology
diagnostics:

```text
unit_field_placement
  field_space
  sphere_dimension
  coordinates
  normalization_status
  field_version
  evidence_refs
  rigidity_confidence
  rigidity_uncertainty

topology_diagnostic
  support_ref
  estimator_kind
  cycle_value
  explicit_phase_degree
  exactness_status
  evidence_refs
  uncertainty
```

The graph remains the declared support. Carrier and diagnostic records are
additional placed quantities and validation terms. A generic unit vector or
orientation does not define an integer winding. An integer phase degree
requires a declared, nonvanishing $U(1)$-valued field on a closed support
cycle.

## Conceptual Checks

- Unit-field coordinates stay normalized; near-zero raw fields are rejected or
  handled by a declared fallback rather than silently called unit vectors.
- Cycle candidates and estimator kinds are declared before diagnostics are
  computed.
- Integer phase degree is used only for a sufficiently sampled nonvanishing
  $U(1)$ phase; other cycle, orientation, and twist values remain diagnostics.
- Collapse risk is surfaced in readout.
- Structure-retention terms remain optional and reference-relative.
- Topological claims are rejected when evidence is too weak.

## Reference-based structure retention

For a triangle $(i,j,k)$ on the declared representation, let

$$
a_{ijk}=y_j-y_i,
\qquad
b_{ijk}=y_k-y_i.
$$

Here $y_i$ is the declared representation coordinate or state vector. It is
separate from an optional unit or phase carrier and need not itself be a unit
vector.

The dimension-independent squared-area diagnostic is the Gram determinant

$$
A_{ijk}
=
\|a_{ijk}\|^2\|b_{ijk}\|^2
-
(a_{ijk}\cdot b_{ijk})^2.
$$

The normalized non-collinearity score is

$$
r_{ijk}
=
\frac{A_{ijk}}
{\|a_{ijk}\|^2\|b_{ijk}\|^2},
\qquad
\|a_{ijk}\|^2\|b_{ijk}\|^2>\delta.
$$

The raw $A_{ijk}$ is a diagnostic, not a positive loss to minimize: minimizing
it would favor collinearity. Given a declared nondegenerate reference on the
same indexed cell, define

$$
\rho_{ijk}
=
\frac{A_{ijk}}{A^{\mathrm{ref}}_{ijk}},
\qquad
A^{\mathrm{ref}}_{ijk}>\delta
$$

and

$$
\ell^{\mathrm{retain}}_{ijk}
=
\left[\max(0,1-\rho_{ijk})\right]^2
+
\eta
\left[
\max\left(0,r^{\mathrm{ref}}_{ijk}-r_{ijk}\right)
\right]^2.
$$

This separates scale-sensitive area loss from angular non-collinearity loss.
The corresponding unsquared deficit is

$$
d_{ijk}
=
\max(0,1-\rho_{ijk})
+
\eta
\max\left(0,r^{\mathrm{ref}}_{ijk}-r_{ijk}\right).
$$

For a dimensionless compression ratio $\chi_i$, a local diagnostic may combine
compression and the weighted neighborhood mean $\bar d_i$ as

$$
C_i=\chi_i\bar d_i.
$$

Degenerate references must be excluded or flagged. Without a reference,
$A_{ijk}$ and $r_{ijk}$ remain diagnostics and must not be promoted to a
validated collapse-risk score.

## Relationship To Nearby Extensions

- Higher-dimensional topology can provide cells and cycles as support.
- Metric placement can represent distances while reference-based retention
  protects declared cycles.
- Gauge transport may be needed when phase-like fields cross frames.
- Operator learning can use structure retention as a validation or
  regularization term.
- Stochastic transition can describe regime uncertainty near transitions.

## Attractor Specialization

Dynamical subjects may use attractor diagnostics as a specialization:

- delay embedding for reconstructing state from time series;
- Lyapunov-style diagnostics for sensitivity;
- attractor-distance loss for forecasting;
- escape warnings for explicit-phase discontinuities or regime shifts.

These remain research tools until examples show they improve validation beyond
simpler baselines.

Use “phase slip” only when a domain supplies an explicit phase whose loss or
discontinuity is measurable.

## Validation Questions

- What cycle, explicit phase, regime, or transition structure is at risk?
- Which graph support carries the topology?
- Is the protected value an exact invariant or a named diagnostic, and what
  mathematical conditions justify that status?
- What nondegenerate reference defines structural retention?
- What baseline collapse should the extension beat?
- Does structure retention improve validation without hiding ordinary error?
- What claim is still unsupported?

## Maturity

Status: active research; CGF-local eval `contract-pass`.

The pass covers a tiny diagnostic contract: unit-carrier validation,
reference-relative structural retention, sampled explicit-phase degree,
cycle-score labeling, collapse-risk composition, and evidence-only output.
The card is public, but stronger claims need continued reference work and
larger evals.

## CGF Eval Result

See [../../labs/evals/topological-rigidity/results.md](../../labs/evals/topological-rigidity/results.md).
