# Basis-Mode Representation

## Definition

Basis-mode representation declares a computational subject in a natural
symmetry or eigenbasis, so graph nodes are modes and typed fields are
coefficients on those modes.

## Parent layer

Substrate.

## Problem solved

Point-sampled graphs can hide symmetry, create dense operators, and make
selection rules or forbidden couplings difficult to validate. A basis-mode
subject makes the basis explicit so operators can be diagonal, sparse,
block-diagonal, or selection-rule-limited when the domain supports that
structure.

## Minimum substrate shape

- A declared basis family such as Fourier, spherical harmonic, wavelet,
  Laplace-Beltrami, radial/angular, Bloch, or another eigenbasis.
- Mode labels that identify each graph node.
- Coefficient fields placed on mode nodes.
- Selection rules or allowed coupling edges between modes.
- Action, constraint, or evolution terms that operate on coefficients.
- Readout that reconstructs, projects, or summarizes the subject from mode
  coefficients.
- Validation for forbidden couplings, truncation residual, reconstruction
  error, or conserved quantities.

## When to use

- The subject has known translation, rotation, cylindrical, toroidal, gauge,
  crystallographic, periodic, or other symmetry.
- A known eigenbasis makes the operator diagonal, sparse, block-diagonal, or
  selection-rule-limited.
- Smooth or structured fields can be represented by fewer coefficients than
  dense samples.
- The readout can report reconstruction error, truncation residual, or
  forbidden coupling checks.

## When not to use

- There is no meaningful basis, symmetry, or eigenproblem.
- The basis is invented only to make an ordinary representation look stronger.
- Ordinary graph nodes already match the domain better than mode labels.
- The readout cannot validate reconstruction or truncation error.
- The problem is system coordination, audit history, or workflow operation
  rather than subject declaration.

## Maturity

Research extension.

## Validation checks

- Every coefficient is placed on a declared mode node.
- Mode labels include the basis family and enough indices to resolve support.
- Selection-rule edges are explicit, and forbidden couplings are rejected or
  surfaced as residuals.
- Diagonal and block-diagonal operators do not write outside their declared
  support.
- Truncation reports dropped-mode residual or uncertainty.
- Readout states whether it reconstructs, projects, or summarizes the field.

## Failure modes

- Treating learned vector embeddings as basis modes without a declared basis.
- Keeping dense point-sampled computation while claiming mode sparsity.
- Hiding coupling terms that violate declared selection rules.
- Truncating high-frequency or high-order modes without residual reporting.
- Using basis-mode vocabulary when topology, metric placement, weak form, or
  gauge transport is the actual missing structure.
