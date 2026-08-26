# Application-Class Studies

## Purpose

Application-class studies test whether the same CGF Substrate vocabulary can
describe very different computational families.

They are not applications yet. They are pressure tests for the declaration
layer, derivative mechanics, and extension components.

## Basis-Mode Representation

Basis-mode representation applies when symmetry gives a natural eigenbasis.
Instead of sampling state at spatial points, the subject represents fields as
coefficients over mode labels.

Basis-mode is now also a Substrate extension:

- [../substrate/extensions/cards/basis-mode-representation.md](../substrate/extensions/cards/basis-mode-representation.md)
- [extension-studies/basis-mode-representation.md](extension-studies/basis-mode-representation.md)
- [../labs/evals/basis-mode-representation/results.md](../labs/evals/basis-mode-representation/results.md)

Typical fit:

- rotational, translational, cylindrical, toroidal, gauge, or crystallographic
  symmetry;
- operators that become diagonal, sparse, block-diagonal, or selection-rule
  limited in the chosen basis;
- readout that reconstructs field values at query points.

Substrate value:

- equivariance becomes structural;
- smooth fields compress into fewer coefficients;
- invariants and forbidden couplings become validation checks;
- spatial discretization is replaced by a mode graph when appropriate.

Open issue: continuous or non-compact symmetries still need a sampling or
truncation policy for modes before broad domain claims are made.

## Field-Theoretic Graph Subjects

Field-theoretic graph subjects apply when many placed fields share a common
domain.

Typical fit:

- scalar, vector, spinor, tensor, or matrix-valued fields;
- local action or Lagrangian terms;
- constraints such as conservation, divergence, gauge, or boundary
  conditions;
- evolution derived from action and variation.

Substrate value:

- adding a field means adding a typed placed quantity, not a separate model;
- interactions become action contributions;
- validation can check conservation, admissibility, and residual drift;
- geometric discretization controls which physical invariants survive.

Open issue: tensor and representation-indexed fields need a clearer minimum
record before they become examples.

Promotion criteria:

- all placed fields declare support and type;
- local action or law terms state their field dependencies;
- boundary, source, exterior placement, or weak-form needs are explicit;
- residuals and invariants are visible before any solver or learned surrogate
  is selected.

## Operator Learning

Operator learning applies when the forward law, action, or propagator is
unknown, partially known, expensive, or learned from data.

Typical fit:

- state evolves over time or maps input functions to output functions;
- data exists for transitions or input-output pairs;
- first-principles information is partial but still provides residual,
  boundary, conservation, or action checks.

Substrate value:

- learned operators become surrogates for declared or derived operators;
- graph, placement, boundary, residual, and invariant metadata remain visible;
- learned readouts can be compared across discretizations;
- validation stays attached to the subject rather than the model architecture.

Open issue: CGF needs examples that distinguish learned surrogates from core
Substrate primitives.

Promotion criteria:

- the learned component is a surrogate for a declared operator, action, or
  readout;
- baseline comparison is explicit;
- residual, uncertainty, or invariant checks remain visible;
- policy, review, or validation boundaries are not replaced by model score.

CGF eval result:

[../labs/evals/operator-learning/results.md](../labs/evals/operator-learning/results.md)
records a `contract-pass` result for the tiny CGF-local promotion-discipline
eval. The claim is limited to that fixture.

## Physical Computation Patterns

Physical computation studies the patterns CGF can describe before domain
details are attached.

Common patterns:

- linear systems;
- eigenvalue problems;
- optimization;
- probabilistic inference;
- combinatorial search;
- optimal control;
- information optimization;
- neural-network forward passes;
- diffusion, smoothing, waves, and oscillation.

Substrate value:

- each pattern can be expressed as graph state plus action, operator, update,
  constraints, readout, and validation;
- applications can start from a known pattern instead of inventing vocabulary;
- missing fits become evidence for a derivative mechanic or extension.

Open issue: the first pattern catalog should be prose-first and code-light,
then section-local examples can follow.

Promotion criteria:

- each pattern maps to the 9 core primitives;
- derivative mechanics are selected only when needed;
- extension choices name a real failure mode;
- claim strength stays tied to a local eval or clearly marked research status.

## Promotion Rule

An application-class study can become an Application page when it has:

- a complete 9-core Substrate declaration;
- the derivative mechanics it needs;
- any extension choices justified by failure modes;
- a small example that does not require a mandatory SDK;
- validation checks that make failure visible.
