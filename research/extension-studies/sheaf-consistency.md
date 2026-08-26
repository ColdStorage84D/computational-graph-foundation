# Sheaf Consistency

## Purpose

Sheaf consistency studies local-to-global agreement across partial views.

Core pattern:

```text
local views + restriction maps + overlaps
  -> consistency residuals
  -> gluing candidate or obstruction
```

## Failure Mode

Multiple local views may each be valid while disagreeing on their overlap.

Common failures:

- views are compared without a declared overlap;
- restriction maps are implicit or inconsistent;
- conflicts are hidden by a merged summary;
- a local view is promoted to a global view without gluing checks;
- disagreement is treated as failure when it should be uncertainty.

## Minimum Substrate Addition

Minimum records:

```text
local_view
  view_kind
  support_ref
  typed_payload_ref
  evidence_refs
  confidence
  uncertainty

restriction_map
  source_view_kind
  source_support_kind
  target_support_kind
  operator_ref
  deterministic_or_frozen

overlap
  support_ref
  participating_view_refs
  restriction_map_refs
```

Derived records may include consistency residuals, gluing candidates, global
sections, obstructions, or cosheaf flows.

## Conceptual Checks

- Views are restricted before comparison.
- Overlap support is explicit.
- Residual type and tolerance are declared.
- Gluing candidates preserve evidence refs.
- Obstructions remain visible.
- Upward aggregation preserves uncertainty.

## Relationship To Nearby Extensions

- Gauge transport may align frames before views can be compared.
- Metric placement provides distance, not local-to-global agreement.
- Higher-dimensional topology can supply shared boundaries as overlaps.
- Information geometry can compare probabilistic local views.

## Validation Questions

- Is there a declared support for every local view?
- Is the restriction map deterministic or frozen enough to review?
- Are residual values interpretable for the payload type?
- Does a global section remain evidence rather than assumed truth?
- Are unresolved conflicts visible in readout?
- Is sheaf consistency solving a real overlap problem?

## Maturity

Status: research-supported; CGF-local eval `contract-pass`.

The extension is ready for cards and decision guides. Domain-specific
restriction maps remain the main future work.

## CGF Eval Result

See [../../labs/evals/sheaf-consistency/results.md](../../labs/evals/sheaf-consistency/results.md).
