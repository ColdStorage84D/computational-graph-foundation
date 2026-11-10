# References And Research Status

## Purpose

This page is the CGF bibliography. It separates internal CGF research from
public concepts and lists the public sources those concepts rest on.

Every source below was checked against the arXiv listing or the DOI registry on
2026-11-10: the identifier resolves, and the title, authors, and year match.

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

Every page in `research/extension-studies/`, and every Architecture page named
after outside work, carries its own `References` section.
`scripts/check_public_base.py` fails when one is missing.

## Bibliography

### Graphs, Spectra, And Modes

- [Spectral Graph Theory](https://doi.org/10.1090/cbms/092), Chung (1996).
- [The Emerging Field of Signal Processing on Graphs](https://arxiv.org/abs/1211.0053), Shuman, Narang, Frossard, Ortega, and Vandergheynst (2012).
- [Hodge Laplacians on Graphs](https://doi.org/10.1137/18M1223101), Lim (2020).

### Discretization, Cells, And Higher-Order Domains

- [Discrete Exterior Calculus](https://arxiv.org/abs/math/0508341), Desbrun, Hirani, Leok, and Marsden (2005).
- [Finite element exterior calculus: from Hodge theory to numerical stability](https://arxiv.org/abs/0906.4325), Arnold, Falk, and Winther (2009).
- [Topological Deep Learning: Going Beyond Graph Data](https://arxiv.org/abs/2206.00606), Hajij et al. (2022).
- [Cell Complex Neural Networks](https://arxiv.org/abs/2010.00743), Hajij, Istvan, and Zamzmi (2020).
- [Weisfeiler and Lehman Go Cellular: CW Networks](https://arxiv.org/abs/2106.12575), Bodnar et al. (2021).
- [Topological deep learning: a review of an emerging paradigm](https://link.springer.com/article/10.1007/s10462-024-10710-9).
- [ICML Topological Deep Learning Challenge 2024: Beyond the Graph Domain](https://arxiv.org/abs/2409.05211).
- [Simplicial Neural Networks](https://arxiv.org/abs/2010.03633).
- [Topological Blindspots: Understanding and Extending Topological Deep Learning Through the Lens of Expressivity](https://research.nvidia.com/labs/par/publication/topological_blind_spots.html).

### Topology Of Data And Dynamics

- [Topology and data](https://doi.org/10.1090/S0273-0979-09-01249-X), Carlsson (2009).
- [Detecting strange attractors in turbulence](https://doi.org/10.1007/BFb0091924), Takens (1981).
- [Measuring the strangeness of strange attractors](https://doi.org/10.1016/0167-2789%2883%2990298-1), Grassberger and Procaccia (1983).
- [Determining Lyapunov exponents from a time series](https://doi.org/10.1016/0167-2789%2885%2990011-9), Wolf, Swift, Swinney, and Vastano (1985).

### Geometry, Frames, And Sheaves

- [Geometric Deep Learning: Grids, Groups, Graphs, Geodesics, and Gauges](https://arxiv.org/abs/2104.13478), Bronstein, Bruna, Cohen, and Velickovic (2021).
- [Gauge Equivariant Convolutional Networks and the Icosahedral CNN](https://arxiv.org/abs/1902.04615), Cohen, Weiler, Kicanaoglu, and Welling (2019).
- [Vector Diffusion Maps and the Connection Laplacian](https://arxiv.org/abs/1102.0075), Singer and Wu (2011).
- [Toward a Spectral Theory of Cellular Sheaves](https://arxiv.org/abs/1808.01513), Hansen and Ghrist (2018).
- [Sheaves, Cosheaves and Applications](https://arxiv.org/abs/1303.3255), Curry (2013).
- [Neural Sheaf Diffusion: A Topological Perspective on Heterophily and Oversmoothing in GNNs](https://arxiv.org/abs/2202.04579), Bodnar et al. (2022).
- [Poincare Embeddings for Learning Hierarchical Representations](https://arxiv.org/abs/1705.08039), Nickel and Kiela (2017).
- [Low Distortion Delaunay Embedding of Trees in Hyperbolic Plane](https://doi.org/10.1007/978-3-642-25878-7_34), Sarkar (2012).
- [Representation Tradeoffs for Hyperbolic Embeddings](https://arxiv.org/abs/1804.03329), De Sa, Gu, Re, and Sala (2018).

### Probability, Information, And Estimation

- [Markov Chains](https://doi.org/10.1017/CBO9780511810633), Norris (1997).
- [Information Geometry and Its Applications](https://doi.org/10.1007/978-4-431-55978-8), Amari (2016).
- [An elementary introduction to information geometry](https://arxiv.org/abs/1808.08271), Nielsen (2018).
- [A New Approach to Linear Filtering and Prediction Problems](https://doi.org/10.1115/1.3662552), Kalman (1960).
- [Bayesian Filtering and Smoothing](https://doi.org/10.1017/CBO9781139344203), Sarkka (2013).

### Causality

- [Causal inference in statistics: An overview](https://doi.org/10.1214/09-SS057), Pearl (2009).
- [Causality](https://doi.org/10.1017/CBO9780511803161), Pearl, second edition (2009).

### Energy, Flow, And Scale

- [Port-Hamiltonian Systems Theory: An Introductory Overview](https://doi.org/10.1561/2600000002), van der Schaft and Jeltsema (2014).
- [Kron Reduction of Graphs With Applications to Electrical Networks](https://doi.org/10.1109/TCSI.2012.2215780), Dorfler and Bullo (2013).
- [The renormalization group: Critical phenomena and the Kondo problem](https://doi.org/10.1103/RevModPhys.47.773), Wilson (1975).
- [Graph reduction with spectral and cut guarantees](https://arxiv.org/abs/1808.10650), Loukas (2018).

### Learned Operators

- [DeepONet: Learning nonlinear operators](https://arxiv.org/abs/1910.03193), Lu, Jin, and Karniadakis (2019).
- [Fourier Neural Operator for Parametric Partial Differential Equations](https://arxiv.org/abs/2010.08895), Li et al. (2020).

### Memory, Replay, And World Models

- [A Theory of How Columns in the Neocortex Enable Learning the Structure of the World](https://doi.org/10.3389/fncir.2017.00081), Hawkins, Ahmad, and Cui (2017).
- [A Framework for Intelligence and Cortical Function Based on Grid Cells in the Neocortex](https://doi.org/10.3389/fncir.2018.00121), Hawkins, Lewis, Klukas, Purdy, and Ahmad (2019).
- [Memory engrams: Recalling the past and imagining the future](https://doi.org/10.1126/science.aaw4325), Josselyn and Tonegawa (2020).
- [Cognitive maps in rats and men](https://doi.org/10.1037/h0061626), Tolman (1948).
- [Reactivation of Hippocampal Ensemble Memories During Sleep](https://doi.org/10.1126/science.8036517), Wilson and McNaughton (1994).
- [Self-improving reactive agents based on reinforcement learning, planning and teaching](https://doi.org/10.1007/BF00992699), Lin (1992).
- [Human-level control through deep reinforcement learning](https://doi.org/10.1038/nature14236), Mnih et al. (2015).
- [Dream to Control: Learning Behaviors by Latent Imagination](https://arxiv.org/abs/1912.01603), Hafner, Lillicrap, Ba, and Norouzi (2019).

## Still Without A Public Reference

These topics appear in CGF and do not yet have a checked source on this page.
Do not make a stronger claim about them until they do.

- action principles, variational calculus, and Lagrangian mechanics;
- gradient flow and constrained optimization;
- numerical stability and error estimation;
- units and dimensional analysis;
- boundary conditions and source terms;
- finite difference and finite volume methods;
- persistent homology and persistence diagrams;
- PCA, t-SNE, UMAP, and diffusion maps;
- differentiable programming and autodiff backends;
- data lineage and provenance;
- hierarchical control and task decomposition;
- calibration and uncertainty management in operating systems;
- NumPy, SciPy, PyTorch, and graph ML libraries, if future examples use them.

## Promotion Checklist

Before promoting a research page into a public Substrate, Architecture,
extension, or Application page:

```text
1. Is every internal idea labeled as internal when needed?
2. Are public concepts backed by public references?
3. Are local evals treated as scoped checks, not production proof?
4. Are claims scoped to what the references and local evals support?
```
