# References And Research Status

## Purpose

This page separates internal CGF research from public concepts that need
public references.

It is a research-status and reference queue, not a final bibliography.

## Research Status Types

| Type | Meaning |
| --- | --- |
| `internal-cgf` | Created inside this CGF research line. |
| `internal-unpublished` | Internal research draft, not published public prior art. |
| `public-theory` | Established mathematical or scientific concept. |
| `public-tool` | Established method, library, benchmark, or implementation family. |
| `cgf-local-eval` | Local eval result, scoped to its stated fixture and contract. |

## Reference Rule

Public concepts need public references before they support public CGF
claims.

Prefer:

- primary papers;
- official documentation;
- stable technical books;
- project or dataset pages;
- source repositories with clear licenses.

Avoid using Wikipedia as an authoritative citation. It may be useful for
orientation, but CGF should cite stronger sources.

## Public Reference Queue

These topics need verified public references before stronger claims are made.

### Substrate Foundations

- graph Laplacian;
- spectral graph theory;
- graph diffusion;
- action principles;
- variational calculus;
- optimization and gradient flow;
- constrained optimization;
- numerical stability and validation.

### Derivative Mechanics

- units and dimensional analysis;
- boundary conditions;
- source terms;
- local action and Lagrangian mechanics;
- functional variation;
- operator assembly;
- residual and error estimation;
- solver selection.

### Discretization And Placement

- finite difference methods;
- finite element methods;
- finite volume methods;
- weak form;
- discrete exterior calculus;
- cell complexes;
- CellComplexView;
- simplicial complexes;
- combinatorial complexes;
- hypergraphs as topological domains;
- Hodge Laplacian;
- exterior placement of quantities.

### Extension Components

- topological invariants, winding, and rigidity;
- topological deep learning;
- persistent homology and persistence diagrams;
- PCA, t-SNE, UMAP, and diffusion maps;
- delay-coordinate reconstruction and attractor analysis;
- Lyapunov-exponent estimation and standard chaos benchmarks;
- topological liftings from graphs to higher-dimensional domains;
- hyperbolic geometry and Poincare-style embeddings;
- stochastic processes and Markov kernels;
- Bayesian filtering;
- Kalman filtering and state estimation;
- information geometry, Fisher metric, entropy, and divergences;
- gauge theory, connections, transport, and holonomy;
- sheaf theory and local-to-global consistency;
- port-Hamiltonian systems;
- causal inference, intervention, and counterfactuals;
- renormalization and coarse-graining;
- differentiable programming and autodiff backends.

### Architecture Research

- data lineage and provenance;
- media metadata and visual evidence records;
- hierarchical control and task decomposition;
- replay, counterfactual simulation, and offline consolidation;
- cognitive maps and spatial memory;
- episodic or engram-like recall;
- calibration and uncertainty management in operating systems.

### Future Implementation Methods

- NumPy;
- SciPy;
- PyTorch;
- Fourier Neural Operator;
- DeepONet;
- Graph Neural Operator;
- graph ML libraries if used by future examples.

## Current Reference Anchors

These public references are the current anchors for topology, higher-dimensional
graphs, and geometric representation work:

- [Geometric Deep Learning: Grids, Groups, Graphs, Geodesics, and Gauges](https://arxiv.org/abs/2104.13478)
- [Topological Deep Learning: Going Beyond Graph Data](https://arxiv.org/abs/2206.00606)
- [Topological deep learning: a review of an emerging paradigm](https://link.springer.com/article/10.1007/s10462-024-10710-9)
- [ICML Topological Deep Learning Challenge 2024: Beyond the Graph Domain](https://arxiv.org/abs/2409.05211)
- [Cell Complex Neural Networks](https://arxiv.org/abs/2010.00743)
- [Simplicial Neural Networks](https://arxiv.org/abs/2010.03633)
- [Weisfeiler and Lehman Go Cellular: CW Networks](https://arxiv.org/abs/2106.12575)
- [Neural Sheaf Diffusion: A Topological Perspective on Heterophily and Oversmoothing in GNNs](https://arxiv.org/abs/2202.04579)
- [Hodge Laplacians on Graphs](https://epubs.siam.org/doi/10.1137/18M1223101)
- [Topological Blindspots: Understanding and Extending Topological Deep Learning Through the Lens of Expressivity](https://research.nvidia.com/labs/par/publication/topological_blind_spots.html)

## Promotion Checklist

Before promoting a research page into a public Substrate, Architecture,
extension, or Application page:

```text
1. Is every internal idea labeled as internal when needed?
2. Are public concepts backed by public references?
3. Are local evals treated as scoped checks, not production proof?
4. Are claims scoped to what the references and local evals support?
```
