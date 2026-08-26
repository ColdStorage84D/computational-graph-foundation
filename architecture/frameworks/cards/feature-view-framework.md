# Feature View Framework

## Purpose

Use this framework when different feature encodings need to be named, filtered,
compared, and evaluated rather than blindly stacked.

## Reusable Concept

A lens creates a typed feature surface. In Granular Analysis, each lens is also
an analysis branch that can feed one or more proposal nodes. A feature view
selects a named subset of features with declared kind requirements such as raw,
invariant, aligned, or domain-specific.

The point is to make encoding choice visible and testable.

The stronger pattern is:

```text
one input -> many feature views -> many proposals -> traceable outcome
```

## View Kinds

Common view kinds:

| Kind | Meaning | Failure if misused |
| --- | --- | --- |
| `raw` | Keeps pose, position, order, coordinates, or direct measurements. | Can dilute signal when those quantities are nuisance. |
| `invariant` | Removes a declared nuisance such as rotation, translation, or order. | Invalid when the removed quantity is the target. |
| `aligned` | Places different sources or modalities in a shared frame. | Misleads if the frame or residual is hidden. |
| `domain-specific` | Encodes a task-owned process or specialized measurement. | Becomes brittle when treated as universal. |
| `aggregate` | Summarizes many local records into a compact view. | Hides failures if coverage is not recorded. |

The main discipline is that better views often matter more than more columns.
Adding raw features to an incompatible view can make the system worse while
making the trace harder to audit.

## Uses CGF Pieces

- lenses;
- projectors;
- typed views;
- Granular Analysis;
- validation checks;
- path-conditioned operator effects, when view choice depends on path context;
- evaluation discipline.

## Example Applications

- multimodal inference;
- image or sensor processing;
- robotics state views;
- security feature derivation;
- scientific or engineering datasets.

## When To Use

- Raw coordinates or raw features can dilute the useful signal.
- Invariance or alignment matters for a task.
- A model should train on one declared view, not hidden mixed columns.
- View choice needs validation.
- Several proposal nodes should consume different views from the same input.

## When Not To Use

- Features are already declared and there is only one valid view.
- The project cannot define what a feature kind means.
- View selection would hide unsupported assumptions.

## Boundary

A feature view can influence scoring, ranking, or routing. It does not create
commit authority by itself.

A feature view is also not a processor. The processor consumes a view; the view
declares what evidence surface is being offered.

## Implementation Posture

Framework code should stay small, inspectable, and tied to explicit view and
validation contracts.
