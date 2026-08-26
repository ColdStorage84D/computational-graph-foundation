# Information Geometry

## Purpose

Information geometry studies typed belief distributions as geometric objects.

Core pattern:

```text
belief distribution
  -> statistical manifold
  -> divergence, metric, entropy, or surprise
  -> belief validation and action terms
```

The study is subject-neutral. The distribution can describe risk, classification
state, next-state uncertainty, sensor interpretation, model disagreement,
expected outcome, or any other declared support. Information geometry only
defines how those belief fields are compared, moved, and validated.

## Failure Mode

Scalar confidence is often too weak to describe uncertainty.

Common failures:

- two beliefs with the same confidence have very different distributional
  shape;
- rare tail risk is hidden by an average score;
- belief updates depend on parameter coordinates rather than the distribution;
- information gain is confused with truth;
- surprise is treated as causality.
- a natural-gradient update is claimed without declaring the distribution
  family or metric basis.

## Minimum Substrate Addition

Minimum records:

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

The extension may also declare divergence, entropy, surprise, Fisher metric,
natural-gradient direction, or information distance.

## Core Concepts

| Concept | Meaning |
| --- | --- |
| Belief distribution | Normalized distribution, calibrated score family, interval family, density, or other declared probabilistic representation. |
| Statistical manifold | Parameter space and metric basis for a family of belief distributions. |
| Divergence | Directed or symmetric separation between two belief distributions. |
| Fisher metric | Local metric basis for a distribution family. |
| Natural-gradient direction | Optional update direction corrected by the information metric instead of raw coordinates. |
| Entropy | Spread or uncertainty in the belief distribution. |
| Surprise | Unexpectedness of observed evidence or outcome under a prior belief. |
| Information distance | Distance-like readout that preserves which divergence or metric was used. |
| Information gain | Amount of belief movement caused by new evidence, scoped as evidence rather than truth. |
| Calibration error | Mismatch between repeated predictions and observed outcomes. |

## Conceptual Operators

| Operator | Meaning |
| --- | --- |
| `kl_divergence` | Directed information difference between two beliefs on shared support. |
| `symmetric_divergence` | Symmetric comparison when direction is not the point of the readout. |
| `entropy_score` | Distributional uncertainty. |
| `surprise_score` | Evidence or outcome surprise under a prior belief. |
| `information_distance` | Distance-like readout over declared support and metric basis. |
| `information_gain` | Belief movement after evidence, usually a divergence from prior to posterior. |
| `calibration_error` | Forecast mismatch over repeated observed outcomes. |
| `fisher_metric_ref` | Declared local metric basis for a distribution family. |
| `natural_gradient_direction` | Optional metric-aware update direction for adaptive belief updates. |

These operators are declarations or readouts. They do not force one numerical
library, solver, or backend.

## Mapping To Core Primitives

| Core primitive | Information geometry interpretation |
| --- | --- |
| Graph | Belief support, states, outcomes, regions, modes, or evidence groups. |
| Typed field | Probability, belief, entropy, surprise, uncertainty, or divergence field. |
| Placement | Declared support where each belief field lives. |
| State | Current belief distribution and evidence references. |
| Action | Belief action terms such as information gain, surprise, divergence, calibration, or complexity. |
| Constraint | Normalization, positivity, support compatibility, and valid parameter region. |
| Evolution | Belief update, distribution movement, stochastic transition, or adaptive parameter update. |
| Readout | Entropy, divergence, surprise, distance, calibration, tail risk, or information gain. |
| Validation | Distribution validity, finite divergence, support match, calibration, and tail-risk visibility. |

## Example Shape

```text
prior belief over outcomes
  -> new evidence
  -> posterior belief over the same support
  -> divergence and information gain
  -> surprise if an observed outcome arrives
  -> calibration and tail-risk report
```

This can help decide whether evidence changed the declared belief enough to
matter, but it does not decide truth, causality, or authority by itself.

## Conceptual Checks

- Identical beliefs have near-zero declared divergence.
- Shifted beliefs produce larger divergence.
- Broader distributions have higher entropy when the family supports it.
- Unlikely observations produce high surprise.
- Infinite or unstable divergence is reported rather than hidden.
- Tail risk remains separately visible.
- Information gain is separated from correctness.
- Natural-gradient claims include a declared metric basis.

## Relationship To Nearby Extensions

- Stochastic transition maps distributions forward.
- Information geometry compares distributions and update paths.
- Causal intervention decides whether a belief change can be attributed to an
  intervention.
- Sheaf consistency can use belief residuals when local views are
  probabilistic.
- Differentiable backend can implement metric-aware updates when gradients are
  part of the declared subject.
- Basis-mode representation can place belief or uncertainty fields on mode
  nodes, while information geometry compares their distributions.

## When It Is The Right Extension

Use Information Geometry when:

- two beliefs with the same confidence can mean different things;
- a subject compares prior and posterior distributions;
- uncertainty shape affects action, readout, or validation;
- rare outcomes or tail risk must stay visible;
- calibration matters after repeated forecasts;
- a learned or adaptive update claims to move through belief space.

Do not use it when:

- the subject has no probability, belief, density, or uncertainty field;
- the distribution support cannot be declared;
- scalar confidence is enough and no distribution comparison is needed;
- information terms would bypass constraints or validation;
- the metric basis is invented only to make the method sound more formal.

## Validation Questions

- Is the distribution family declared?
- Is the metric or divergence basis declared?
- Are invalid parameter regions handled?
- Does entropy hide or expose risk?
- Are surprise and information gain scoped as evidence?
- Can readout explain which information measure was used?
- Is tail risk preserved when it matters?
- Does natural-gradient language have a declared metric basis?

## Maturity

Status: research-supported; CGF-local eval `contract-pass`.

The concept is ready as an extension card. Concrete numerical choices should
stay subject-specific until more examples exist.

## CGF Eval Result

See [../../labs/evals/information-geometry/results.md](../../labs/evals/information-geometry/results.md).
