# Research Coverage Map

This page tracks how CGF research areas are carried by the public project
structure.

It is not a spec. It is the map that keeps theory, eval results, and future
implementation pressure from being mixed into one section.

## Coverage Rule

Every research area should have one current home:

- Substrate when it changes how a computational subject is declared.
- Architecture when it changes how CGF systems operate around a subject.
- Labs when it is runnable evals, prototypes, or unfinished experiments.
- Applications when it becomes a domain-facing pattern.
- Research when it needs deeper theory, references, or validation notes.
- Archive when it is retained for history but should not guide new work.

Public CGF docs should be self-contained. They should explain the idea in CGF
terms and should not require external project history to be understood.

## Current Coverage

| Research area | Primary home | Current status | Next destination |
| --- | --- | --- | --- |
| 9-core Substrate primitives | Substrate | Stable v0.1 contract | Examples and future section-local code |
| Primitive computation bridge | Substrate | Teaching guide exists | More examples after contracts settle |
| Derivative mechanics | Substrate + Research | v0.2 docs exist; deeper study added | More math and validation notes |
| Action-Native Computation | Substrate derivatives + Research + Labs | CGF-local eval `contract-pass` | Larger examples only after claim boundaries stay clear |
| Domain-agnostic substrate charter | Research + Substrate | Public posture exists across README and Substrate docs | Sharper examples and release narrative |
| Geometric discretization | Research extension study | Exterior placement and weak form now have tiny CGF-local evals | Substrate derivative and extension examples |
| Topology in CGF | Substrate extension guide + Research | Guide added; claims depend on selected topology concept | Narrower examples and evals later |
| Higher-dimensional graphs | Research extension study | Public research page exists | Extension cards and examples when narrower |
| CellComplexView | Substrate extension + Research | CGF-local eval `contract-pass` | Examples and topology guide refinements later |
| Attractor Diagnostics | Substrate extension + Research | Research-supported; no direct Labs eval yet | Tiny dynamical-regime eval later |
| Basis-mode representation | Research extension study | CGF-local eval `contract-pass` | Symmetry and mode-graph examples later |
| Gauge transport | Research extension study | CGF-local eval `contract-pass` | Domain examples later |
| Information geometry | Research extension study | CGF-local eval `contract-pass` | Belief-state examples later |
| Sheaf consistency | Research extension study | CGF-local eval `contract-pass` | Multi-view example later |
| Causal intervention | Research extension study | CGF-local eval `contract-pass` | Architecture bridge later |
| Hyperbolic / metric placement | Research extension study | CGF-local eval `contract-pass` | Metric placement examples later |
| Port-Hamiltonian flow | Research extension study | CGF-local eval `contract-pass` | Open-system examples later |
| Stochastic transition | Research extension study | CGF-local eval `contract-pass` | Probabilistic examples later |
| Topological rigidity | Independent research extension study | CGF-local derivative-diagnostic eval `contract-pass` | Reference and larger evals later |
| Renormalization / coarse-graining | Research extension study | CGF-local eval `contract-pass` | Scale-change examples later |
| Bayesian filtering / state estimation | Architecture + Labs | CGF-local eval `contract-pass` | Deeper belief-state examples later |
| Field-theoretic graph subjects | Research application class | Study added | Derivative examples later |
| Operator learning | Research application class | CGF-local eval `contract-pass` | Differentiable backend examples later |
| Physical computation patterns | Research application class | Study added | Pattern catalog later |
| Anchor / Lens / Promise | Architecture + Labs | CGF-local eval `contract-pass` | More ingestion examples later |
| Visual media encoding | Architecture + Labs | CGF-local eval `contract-pass` | Better media application examples later |
| Hierarchical execution cycles | Architecture + Labs | CGF-local eval `contract-pass` | Integration examples later |
| Cortical-Column World Model | Architecture + Labs | CGF-local eval `contract-pass` | Larger sensorimotor examples only within the documented claim boundary |
| Provisional Graph Growth | Architecture + Labs | CGF-local eval `contract-pass` | Application examples only after promotion and rollback boundaries stay clear |
| Offline replay / dream cycles | Architecture | Docs-led; no direct Labs eval yet | Eval once claim becomes public |
| Cognitive map memory | Architecture | Docs-led; no direct Labs eval yet | Recall examples later |
| Engram / spatial memory | Architecture | Docs-led; no direct Labs eval yet | Recall examples later |
| Evidence Graph Triage | Architecture + Applications + Labs | CGF-local eval `contract-pass` | Larger triage examples only after value-key and decay behavior are reviewed against real review volume |
| Value-over-baseline / recipe-grounded eval discipline | Labs | Methodology page added | First recipe-grounded CGF-local eval later |
| Evaluation backlog | Labs | Methodology exists; gaps remain explicit | Add CGF-local eval code before claims |
| Path-state and operating contracts | Architecture | Bridge added | Architecture spec pass later |
| Retired execution-graph material | Archive | Not promoted | Archive only if still useful |

## Reading Map

Use this order when deciding where a research idea belongs:

```text
coverage-map.md
-> connection-map.md
-> substrate-research-map.md
-> extension-studies/README.md
-> derivative-mechanics-study.md
-> application-class-studies.md
-> ../labs/evals/README.md
-> ../labs/evaluation-backlog/README.md
-> ../architecture/research-bridge.md
```

## Promotion Gate

A research idea can move into a public contract only when it has:

- a clear parent CGF layer;
- a one-sentence definition;
- the failure mode it solves;
- the minimum Substrate or Architecture shape it requires;
- at least one small example;
- a maturity label;
- reference status or CGF-local evaluation status.

If any item is missing, keep the idea in Research or Labs.
