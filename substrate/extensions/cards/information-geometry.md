# Information Geometry

## Definition

Information geometry treats probability, belief, or distribution fields as
structured objects with their own geometry.

## Parent layer

Substrate.

## Problem solved

Probability-like fields can be invalidly compared or updated when their
geometry is ignored.

The extension prevents a common shortcut: replacing a full belief distribution
with one scalar confidence score. Scalar confidence can hide tail risk,
distribution shift, unstable support, or a belief update that moved in the wrong
geometry.

## Minimum substrate shape

- Probability, belief, or distribution field.
- Placement support.
- Geometric relation or divergence.
- Action, constraint, or readout using that relation.
- Validation check for valid distribution behavior.

## When to use

- Belief or probability fields drive action or readout.
- Comparing distributions matters.
- Updates must preserve distribution validity.
- Surprise, entropy, calibration, information gain, or tail risk must remain
  visible.
- A learned or adaptive update needs a declared metric basis instead of raw
  coordinate movement.

## When not to use

- The subject uses ordinary scalar fields only.
- A simple distance or score is sufficient.
- Distribution validity is not checked.
- The distribution family, support, or evidence basis cannot be declared.
- Information terms would be used as authority instead of evidence inside the
  declared subject.

## Maturity

Research extension.

## Substrate-owned declarations

- Distribution field: belief, probability, density, categorical state, or
  uncertainty field.
- Statistical support: valid sample space and placement.
- Divergence: KL-like, symmetric, task-specific, or other declared comparison.
- Metric structure: Fisher-style, natural-gradient, or declared local geometry.
- Information terms: entropy, surprise, calibration, information gain, or
  complexity contribution to action/readout.

## Conceptual records

```text
belief_distribution
  support_ref
  distribution_family
  parameters_ref
  evidence_refs
  confidence
  uncertainty

statistical_manifold
  distribution_family
  parameter_basis
  metric_basis
  valid_region
```

## Typical operators and readouts

| Item | Role |
| --- | --- |
| Divergence | Measures directed or symmetric separation between beliefs. |
| Entropy | Measures spread or uncertainty in the belief distribution. |
| Surprise | Measures how unexpected observed evidence is under a prior belief. |
| Information distance | Reports a distance-like readout with its declared basis. |
| Fisher metric | Declares local distribution geometry for a family. |
| Natural-gradient direction | Optional update direction adjusted by declared information geometry. |
| Calibration error | Reports repeated mismatch between belief and observed outcome. |
| Information gain | Measures how much evidence changed the belief state. |

Natural-gradient direction and Fisher metric are optional. They should be used
only when the distribution family and metric basis are explicit.

## Mapping to core primitives

| Core primitive | Information geometry shape |
| --- | --- |
| Graph | Nodes, regions, states, outcomes, or supports that carry beliefs. |
| Typed field | Probability, belief, density, uncertainty, entropy, or divergence fields. |
| Placement | Support where the distribution is valid. |
| State | Current belief distribution and evidence references. |
| Action | Belief action terms such as divergence, surprise, information gain, or calibration cost. |
| Constraint | Normalization, positivity, support compatibility, valid parameter region. |
| Evolution | Belief update, distribution transport, or stochastic transition comparison. |
| Readout | Divergence, entropy, surprise, information distance, tail risk, or calibration report. |
| Validation | Distribution validity, support match, finite divergence, calibration, and visible risk checks. |

## Validation checks

- Distribution fields remain normalized and nonnegative where required.
- Divergence direction and support assumptions are explicit.
- Metric or natural-gradient use is tied to declared distribution geometry.
- Entropy, surprise, or information gain is computed from declared state.
- Updates preserve distribution validity and calibration requirements.
- Tail-risk mass remains visible when the subject has risk states.
- Infinite or unstable divergence is reported instead of hidden.

## Failure modes

- Comparing distributions with an ordinary vector distance when support matters.
- Reporting confidence without a declared belief field.
- Mixing incompatible distribution families.
- Treating surprise or entropy as a generic score with no action role.
- Letting information terms override hard constraints.
- Using natural-gradient language without a declared metric basis.
- Hiding rare but important outcomes inside an average confidence score.
