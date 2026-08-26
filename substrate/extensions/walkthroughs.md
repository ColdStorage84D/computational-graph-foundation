# Extension Walkthroughs

## Purpose

These walkthroughs show how extensions are added after a complete 9-core
Substrate subject already exists.

They are prose declarations only. They are not code and do not define an SDK.

## Walkthrough 1: Noisy field law

### Core subject

Graph:
  Samples connected by neighborhood edges.

Typed field:
  Scalar field value on sample nodes.

Placement:
  Field values live on nodes; aggregate checks live on regions.

State:
  Current noisy measurements and estimated field values.

Action:
  Prefer a field that agrees with measurements while remaining smooth enough for
  the domain law.

Constraint:
  Field values must remain inside declared admissible bounds.

Evolution:
  Update the estimated field toward lower mismatch and smoother regional
  behavior.

Readout:
  Cleaned field estimate and regions where the law is unreliable.

Validation:
  Bounds hold, aggregate mismatch is reported, and unreliable regions are not
  hidden.

### Extension choice

Use weak form because the law is not reliable point by point. Use exterior
placement when forcing, demand, boundary condition, or environment state affects
the field but should not become internal field state.

### Added declarations

- Test support for aggregate field checks.
- Weak residual over each region.
- Exterior quantity and contact relation.
- Validation that exterior contribution is included only where declared.

### Extension validation

- Aggregate residual stays below the declared tolerance.
- Local outliers are reported when they affect readout.
- Exterior conditions do not become internal state.
- Readout states which regions are trusted and which are not.

## Walkthrough 2: Multi-view catalog or inventory state

### Core subject

Graph:
  Items, locations, records, and relationships between them.

Typed field:
  Quantity, status, identifier, timestamp, and confidence fields.

Placement:
  Quantities live on item-location support; identifiers and confidence live on
  record support.

State:
  Current local records from each view.

Action:
  Prefer a global state that explains local records with minimal disagreement.

Constraint:
  Global state cannot assign impossible quantities, invalid identifiers, or
  contradictory statuses.

Evolution:
  Update the declared global state when local views change.

Readout:
  Accepted inventory state, unresolved conflicts, and confidence by item or
  location.

Validation:
  Every accepted value is supported by declared local records and constraints.

### Extension choice

Use sheaf consistency because local views overlap and may disagree. Use gauge
transport when records use different units, identifiers, coordinate conventions,
or representation frames before comparison.

### Added declarations

- Local views and their supports.
- Overlaps between views.
- Restriction maps for comparing overlap values.
- Transport maps for unit, identifier, or frame conversion.
- Consistency residual and obstruction report.

### Extension validation

- Overlap comparisons happen after the needed transport.
- Residuals are explicit for each unresolved conflict.
- A global state is accepted only when local consistency is adequate.
- Obstructions are reported instead of silently merged.

## Walkthrough 3: Regime-preserving trajectory

### Core subject

Graph:
  Time-indexed states connected by transition edges.

Typed field:
  State vector, regime label, phase-like marker, and transition quality.

Placement:
  State and regime fields live on time nodes; transition quality lives on
  transition edges.

State:
  Current trajectory and inferred regime sequence.

Action:
  Prefer a trajectory that follows observed state while preserving meaningful
  regimes and transitions.

Constraint:
  Regime labels and transition edges must remain admissible.

Evolution:
  Update trajectory estimates as new state samples arrive.

Readout:
  Regime sequence, transition points, and collapse-risk warnings.

Validation:
  Declared transitions are supported by state, constraints, and readout checks.

### Extension choice

Use metric placement when distances between states or regimes matter. Use
topological rigidity when smoothing, compression, or embedding could erase
declared cycles, explicit phase structure, recurrence, rare regimes, or
transition corridors.

### Added declarations

- Metric placement for state or regime distance.
- Protected support for cycles, recurrent paths, or transition corridors.
- Explicitly typed carrier for phase, cycle, or regime structure.
- Reference-relative structure-retention term that resists declared invalid
  collapse.
- Collapse-risk readout tied to declared state and a nondegenerate reference.

### Extension validation

- Metric distances remain valid for the declared support.
- Protected structure remains stable under allowed updates.
- Collapse-risk warnings trace to carrier field and transition support.
- Smoothing does not erase declared rare regimes or transition corridors.

## Walkthrough 4: Symmetry-driven field

### Core subject

Graph:
  Modes connected by allowed coupling edges.

Typed field:
  Coefficient, uncertainty, and residual fields on mode nodes.

Placement:
  Coefficients live on mode support rather than sampled spatial support.

State:
  Current coefficient vector and truncation scope.

Action:
  Prefer coefficient states that satisfy the declared operator, law, or objective.

Constraint:
  Forbidden couplings and inadmissible mode labels are not allowed.

Evolution:
  Update coefficients through a diagonal, sparse, block, or
  selection-rule-limited operator.

Readout:
  Reconstructed field, projected query values, or modal summary.

Validation:
  Coupling validity, reconstruction error, truncation residual, and declared
  invariant checks are visible.

### Extension choice

Use basis-mode representation because the subject has a known symmetry,
eigenbasis, or mode decomposition. Add differentiable backend only when
coefficient operators or readouts need gradients. Add topological rigidity only
when modal dynamics have protected cycles, explicit phase structure, regimes,
or reference-relative collapse risk.

### Added declarations

- Basis family and mode labels.
- Coefficient fields on mode nodes.
- Selection-rule edges and forbidden coupling checks.
- Operator support: diagonal, sparse, block-diagonal, or selection-rule-limited.
- Readout map and truncation policy.

### Extension validation

- Every coefficient resolves to a declared mode node.
- Operators do not write outside their declared support.
- Forbidden couplings are rejected or reported as residuals.
- Dropped modes contribute to a visible truncation residual.
- Readout states whether it reconstructs, projects, or summarizes the field.

## Walkthrough 5: Region-supported field

### Core subject

Graph:
  Samples, edges, region cells, and boundary relations.

Typed field:
  Sample value, region aggregate, boundary marker, and residual fields.

Placement:
  Sample values live on nodes; flux or transition values live on edges; region
  aggregates live on cells.

State:
  Current sample values, declared region support, and boundary assignments.

Action:
  Prefer states whose region aggregates and boundary relations agree with the
  declared law.

Constraint:
  Region cells must have valid boundaries, and values cannot be assigned to
  undeclared support.

Evolution:
  Update sample and region fields while preserving declared boundary relations.

Readout:
  Accepted region summaries, boundary conflicts, and unsupported regions.

Validation:
  Every region readout traces to declared cell support and boundary checks.

### Extension choice

Use CellComplexView because node-edge graph support is not enough to declare
regions, surfaces, or volumes. Add weak form when the declared law is checked
over those higher-order supports.

### Added declarations

- Cell labels and dimensions.
- Boundary relations between cells.
- Region support for aggregate fields.
- Validation for missing, open, or inconsistent boundaries.

### Extension validation

- Every cell has declared lower-dimensional support.
- Boundary checks fail visibly when a region is incomplete.
- Aggregate laws are attached to declared cells, not hidden collections.
- Readout reports unsupported or invalid regions.

## Walkthrough 6: Regime diagnostic

### Core subject

Graph:
  State samples connected by transition edges.

Typed field:
  State marker, transition quality, regime label, recurrence score, and escape
  warning.

Placement:
  State markers live on state nodes; transition quality lives on transition
  edges; regime diagnostics live on declared regime support.

State:
  Current sequence of observed or estimated states.

Action:
  Prefer regime summaries that explain recurrence, trapping, and transition
  evidence without hiding uncertainty.

Constraint:
  Regime labels must be supported by declared state and transition evidence.

Evolution:
  Update the regime diagnostic as new transition evidence appears.

Readout:
  Regime label, recurrence warning, basin or trap warning, and escape warning.

Validation:
  Warnings must cite declared state and transition evidence, and uncertainty is
  not hidden.

### Extension choice

Use Attractor Diagnostics because the subject needs warnings about recurrence,
basins, traps, oscillation, or regime escape. Add stochastic transition when
transition uncertainty is part of the declared subject. Add topological
rigidity only when cycles, phase, or rare transition support must be protected.

### Added declarations

- Regime or basin support.
- Recurrence or trap diagnostic.
- Escape or transition warning.
- Validation that diagnostics are warnings, not proof of a global attractor.

### Extension validation

- Recurrence warnings cite transition evidence.
- Escape warnings cite state and transition changes.
- Diagnostics do not replace the declared readout.
- The document does not claim prediction or solver success from diagnostics
  alone.

## Walkthrough review

For every extension walkthrough, check:

```text
1. The 9 core primitives are complete before the extension appears.
2. The extension solves a named failure mode.
3. The extension adds a declaration, not just terminology.
4. The extension changes validation or readout.
5. The extension remains optional for subjects that do not have that failure mode.
```
