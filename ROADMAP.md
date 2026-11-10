# Roadmap

CGF is a docs-led, self-contained, MIT-licensed public base for graph-shaped
computational systems. It is not a mandatory SDK, package lock-in, graph
database, solver, or product framework.

The public base is considered ready when a developer or agent can enter from
the README, pick the right layer, choose a framework mix, understand claim
boundaries, run local checks, and build independently.

Use [PUBLIC_BASE_CHECKLIST.md](PUBLIC_BASE_CHECKLIST.md) as the release gate for
entry paths, supported `contract-pass` claims, known gaps, and final checks.
Use [RELEASE_MANIFEST.md](RELEASE_MANIFEST.md) for the current snapshot's
verification summary.

## Done For Public Base

The public base includes:

- stable Substrate core contract for graph-shaped computational subjects;
- Substrate derivative mechanics and extension components as conditional
  documentation layers;
- Architecture docs for execution graph, runtime spine, graph brain/spine,
  subgraph capsules, graph runtime memory, path-conditioned operation,
  path-gated control, proposal / verifier / commit, trace, replay, and
  evaluation discipline;
- first-class Granular Analysis, Multimodal Outcome Stack, Signal Review,
  Anchor / Lens / Promise, Visual Media Encoding, Hierarchical Execution
  Cycles, Belief State, Bayesian Filtering, and graph memory patterns;
- framework selection guide for choosing reusable Architecture cards;
- Applications for bot / agent systems, medical image analysis review, signal /
  alert review, and industrial robot arm graph control demonstration;
- Labs evals with a declared layer: 19 isolated, 1 integration, and 6
  value-over-baseline;
- a memory ablation for the bot example;
- checked public references for every extension study;
- section-local optional code only.
- standalone publication, support, and security guidance.

## Known Research And Eval Gaps

These gaps are intentional and do not block the public base:

- action-native computation has a direct eval, but derivative mechanics as a
  whole still need broader direct evaluation;
- Attractor Diagnostics remains research-supported with no direct Labs eval yet;
- higher-dimensional topology remains research-only until narrowed into
  cards, examples, or evals;
- offline replay cycles, cognitive map memory, and cued recall memory remain
  Architecture patterns without direct Labs evals yet;
- Architecture framework cards without direct evals must continue to say so;
- no eval is recipe-grounded, and no result is measured on real data.

Missing evals do not block release when docs clearly mark them as
`no direct Labs eval yet`, `research-only`, or `draft`.

## Next Research

- Public references for the topics listed as still unreferenced in
  [research/references.md](research/references.md).
- A recipe-grounded eval built from a real application failure mode.
- Value-over-baseline comparisons for the evals that are still isolated.
- Larger evals for topological rigidity, CellComplexView, weak form, exterior
  placement, and derivative mechanics.
- A narrowed Attractor Diagnostics eval.
- Clearer examples for field-theoretic, physical-computation, and
  operator-learning subjects.

## Next Applications

- Keep adding small, self-contained application notes only when they demonstrate
  reusable CGF patterns.
- Do not add real financial, medical, security, maintenance, or production
  claims without domain-specific validation.
- Candidate future examples: ecommerce/service workflow, sensor ingestion,
  predictive maintenance, and security or audit finding review as application
  notes. The Evidence Graph Triage card and its Labs eval already carry the
  reusable pattern for the last of these; no application example ships for it.

## Future Optional Code

Future code should stay section-local:

```text
substrate/examples/        small teaching implementations
architecture/reference/    Architecture contract references
labs/evals/                experimental contract evals
applications/<domain>/     domain-specific examples
```

Do not add a top-level SDK, package metadata, or package lock-in unless a later
project decision creates a clear reason.

## Final Acceptance Checklist

Before calling a snapshot done:

```text
README, traversal, agent standards, and project intake agree.
The public base checklist is current.
Substrate and Architecture boundaries are clean.
Labs claims are traceable to result files.
Every result record declares its eval layer.
Every extension study carries checked references.
Release counts equal the counts in the tree.
Applications are examples, not owners of reusable concepts.
No stale project-history wording appears.
No top-level SDK/package surface exists.
All local tests pass.
All local Markdown links resolve.
```
