# Basis-Mode Representation

## Purpose

Basis-mode representation is the Substrate extension for subjects where the
natural graph is a graph of modes rather than a graph of sampled points.

The core move is:

```text
field -> mode coefficients -> mode graph
  -> sparse / diagonal / block operators
  -> validated readout
```

Use it when a symmetry, eigenbasis, or mode decomposition gives the subject a
more compact and more valid computational shape than point samples.

## Failure mode

Point-sampled graphs can make a structured subject look dense. They often hide
known symmetry, blur conserved quantities, and turn simple operators into large
stencils. They can also make forbidden couplings hard to detect because every
sample may appear able to influence every nearby sample.

Basis-mode representation prevents this failure by declaring the basis, mode
labels, coefficient fields, and allowed mode couplings directly.

## Minimum Substrate addition

A basis-mode subject starts from a complete 9-core Substrate subject and adds:

- `basis_family`: Fourier, spherical harmonic, wavelet, Laplace-Beltrami,
  radial/angular, Bloch, point-group irrep, or another declared family.
- `mode_label`: explicit indices for each mode node, such as `k`, `(l, m)`,
  `(n, l, m)`, band index, radial index, or representation label.
- `coefficient_field`: typed values placed on mode nodes.
- `selection_rule`: allowed couplings between modes.
- `basis_operator_shape`: diagonal, sparse, block-diagonal, or
  selection-rule-limited.
- `readout_map`: reconstruction, projection, or summary from coefficients.
- `truncation_policy`: which modes are kept and how dropped support is reported.

## Mapping to the 9 core primitives

| Primitive | Basis-mode declaration |
| --- | --- |
| Graph | Nodes are basis modes; edges are allowed mode couplings. |
| Typed field | Coefficients, uncertainty, residual, or conserved quantities on modes. |
| Placement | Fields live on mode support, not spatial sample support. |
| State | Current coefficient vector and truncation scope. |
| Action | Law, cost, Hamiltonian, energy, smoothing, or objective in coefficient form. |
| Constraint | Selection rules, forbidden couplings, symmetry constraints, bounds, or conserved quantities. |
| Evolution | Coefficient update under diagonal, sparse, block, or learned operator. |
| Readout | Reconstruct field values, project to query support, or summarize modal content. |
| Validation | Coupling validity, residual, reconstruction error, truncation error, and invariant checks. |

## Mode graph

A mode graph is not a hidden vector embedding. Each node has a declared basis
meaning.

Examples:

| Domain shape | Mode labels |
| --- | --- |
| Periodic signal | Fourier index `k` and sine/cosine component. |
| Spherical field | Spherical harmonic label `(l, m)` plus radial index. |
| Curved manifold | Laplace-Beltrami eigenfunction index. |
| Crystal or lattice | Bloch wave vector, band, or irreducible representation label. |
| Reduced-order model | Proper mode index with source and truncation policy. |

Edges should mean allowed coupling, not visual proximity. If a declared rule
says only neighboring Fourier modes can couple, the graph should not quietly
connect every mode to every other mode.

## Operator shapes

Basis-mode representation is valuable because many operators become structured.

| Shape | Meaning | Example |
| --- | --- | --- |
| Diagonal | Each mode evolves independently. | Fourier Laplacian multiplies each mode by a scalar. |
| Sparse | Only a small set of mode pairs interact. | Local forcing couples nearby mode indices. |
| Block-diagonal | Modes mix only within declared blocks. | Rotation mixes components inside a fixed angular degree. |
| Selection-rule-limited | Couplings are allowed only when labels satisfy a rule. | A transition changes one angular index while preserving another. |

The implementation can be a matrix, function, learned surrogate, or external
solver. The Substrate contract only requires that the support and validation
rules are explicit.

## Basis-mode versus sampled spatial graph

A sampled spatial graph is best when locality in physical space is the main
structure. Nodes represent points, cells, regions, or measured entities.

A basis-mode graph is best when the field is more naturally represented by
coefficients. Nodes represent functions, harmonics, modes, or representation
components.

Use sampled support when:

- boundaries, contacts, local discontinuities, or geometry dominate;
- the basis is unknown or unstable;
- readout depends on local values that cannot be reconstructed safely.

Use mode support when:

- symmetry makes the basis meaningful;
- operators are simpler in coefficient space;
- compression and invariant checks matter;
- readout can validate reconstruction or truncation.

## Basis-mode versus vector embedding

Vector embeddings are usually learned coordinates. They are useful for
similarity, retrieval, clustering, or downstream model features, but individual
coordinates often do not have declared scientific meaning.

Basis modes are declared coordinates. A coefficient means "how much of this
known basis function is present." The basis, support, coupling rules, and
readout are part of the subject contract.

The distinction:

```text
embedding dimension = learned feature coordinate
basis mode = declared function / symmetry component
```

A learned model may produce coefficients, but it does not make them basis-mode
coefficients unless the basis family, mode labels, readout map, and validation
checks are declared.

## Basis-mode versus topological rigidity

Basis-mode representation and topological rigidity are complementary.

Use basis-mode when symmetry or an eigenbasis is known. Use topological
rigidity when cycles, phases, winding, regimes, rare branches, or transition
structure may collapse under smoothing, compression, embedding, or learning.

Rule of thumb:

```text
exact or useful global symmetry -> basis-mode
local / broken / partial cyclic structure -> topological rigidity
both present -> basis-mode first, topological rigidity only for protected
                cycle, phase, or regime behavior in the mode dynamics
```

Basis-mode prevents invalid dense computation in a structured basis.
Topological rigidity prevents collapse of protected topology. They should not
be used as substitutes for each other.

## Relationship to nearby extensions

| Nearby CGF piece | Relationship |
| --- | --- |
| Gauge transport | Use when coefficients or fields must be compared across local frames, bases, phases, or charts. |
| Weak form | Use when laws are validated by tested aggregate residuals rather than pointwise updates. |
| Differentiable backend | Use when coefficient operators, parameters, or readouts need gradients. |
| Renormalization / coarse-graining | Use when high-order modes are compressed into lower-order effective descriptions. |
| Metric placement | Use when the basis or readout also depends on declared distance, curvature, or coordinate validity. |
| Topological rigidity | Use only when mode dynamics carry protected cycles, phases, winding, regimes, or collapse risk. |

## Validation questions

Before promoting a basis-mode subject, ask:

1. What is the declared basis family?
2. What does each mode label mean?
3. Which coefficients live on which mode nodes?
4. What coupling edges are allowed by selection rules?
5. Which couplings are forbidden?
6. Which operator is diagonal, sparse, block-diagonal, or selection-rule-limited?
7. What modes are dropped by truncation?
8. How does readout reconstruct, project, or summarize the field?
9. What residual, reconstruction error, invariant, or forbidden-coupling check is reported?

## Example declarations

Fourier signal:

```text
graph: Fourier modes k = 0..K with sine/cosine components
typed field: coefficient amplitude per mode
placement: mode support
action: prefer low residual under a diagonal frequency operator
constraint: forbidden coupling beyond declared neighbor rules
readout: reconstruct signal at query points
validation: dropped-mode residual and forbidden-coupling check
```

Spherical field:

```text
graph: radial/angular modes (n, l, m)
typed field: coefficient per mode
placement: radial/angular mode support
action: operator that is diagonal or block structured by mode label
constraint: allowed angular and radial couplings
readout: evaluate field at selected spatial queries
validation: selection-rule violations and reconstruction residual
```

Reduced-order field:

```text
graph: retained modes from an identified basis
typed field: coefficient and uncertainty per mode
placement: reduced mode support
action: effective operator over retained modes
constraint: truncation scope and admissible coefficient range
readout: coarse field reconstruction or task-relevant summary
validation: residual against held-out support or known invariants
```

## Maturity

Status: research extension; CGF-local eval `contract-pass` after the
basis-mode tiny fixture passes.

The result should remain bounded. A tiny eval can validate the declaration
contract, but it does not prove physics accuracy, chemistry accuracy,
production solver quality, or learned model performance.

## References

Public sources for mode decompositions on graphs.

- [Spectral Graph Theory](https://doi.org/10.1090/cbms/092), Chung (1996). Eigenvalues and eigenvectors of the graph Laplacian.
- [The Emerging Field of Signal Processing on Graphs](https://arxiv.org/abs/1211.0053), Shuman, Narang, Frossard, Ortega, and Vandergheynst (2012). The graph Fourier transform and operators that are diagonal in it.
