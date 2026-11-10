# Release Notes

For the verification summary of the current snapshot, see
[RELEASE_MANIFEST.md](RELEASE_MANIFEST.md).

## v0.2.0 - 2026-11-10

This snapshot makes the evals carry weight. Every result now says what kind of
evidence it is, six evals measure a concept against a baseline, and the evals
named after mathematical objects implement them.

### Renamed

Four names were replaced by names that say what the thing does. Links to the
old paths no longer resolve.

| v0.1.0 path | v0.2.0 path |
| --- | --- |
| `architecture/cortical-column-world-model.md` | `architecture/local-voting-world-model.md` |
| `architecture/frameworks/cards/cortical-column-world-model-framework.md` | `architecture/frameworks/cards/local-voting-world-model-framework.md` |
| `labs/evals/cortical-column-world-model/` | `labs/evals/local-voting-world-model/` |
| `architecture/engram-spatial-memory.md` | `architecture/cued-recall-memory.md` |
| `architecture/offline-replay-dream-cycles.md` | `architecture/offline-replay-cycles.md` |
| `labs/evals/operator-learning/` | `labs/evals/surrogate-promotion/` |

### Added

- An eval layer on every result record: 19 isolated, 1 integration, and 6
  value-over-baseline.
- A new eval for path-conditioned and path-gated operators, which had none.
- Seeded comparisons against a baseline for six evals, each recording where
  the concept does not help.
- Implementations of the object each of these evals is named after: a
  structural causal model, a linear port-Hamiltonian system, a cellular sheaf,
  a discrete weak form, network renormalization by node elimination, and the
  Fisher metric.
- A memory ablation for the bot example.
- A bibliography of checked public sources, and a References section on every
  extension study and on every Architecture page named after outside work.
- Validator checks for the eval layer, for the comparison files and the
  `Where It Does Not Help` section of a value claim, for references, and for
  release counts that equal the counts in the tree.

### Changed

- The README opens with three results that can be reproduced.
- Status columns in the traversal guide and the connection map show the result
  label and the eval layer. Numbers and claim boundaries live in the result
  records.

### Evidence

| Eval | Baseline | Result under the stated assumptions | Where it does not help |
| --- | --- | --- | --- |
| [Path-gated operators](labs/evals/path-gated-operators/results.md) | Commit the highest score | Wrong commits 65% to 20% | Paths that carry no information |
| [Evidence Graph Triage](labs/evals/evidence-graph-triage/results.md) | Rank by score at equal volume | Wrong commits 313 to 144 | Correlated sources; recall is lower |
| [Granular Analysis](labs/evals/granular-analysis/results.md) | One lens | Wrong commits 20% to 10% | Lenses that share a blind spot |
| [Bayesian filtering](labs/evals/bayesian-filtering/results.md) | Latest raw measurement | Error 2.01 to 0.68 | A wrong motion model, where error is 16.77 |
| [Hyperbolic placement](labs/evals/hyperbolic-placement/results.md) | Same layout in the flat plane | Distortion 124 to 1.4 on a depth-6 binary tree | Grids, and a mismatched radius |
| [Gauge transport](labs/evals/gauge-transport/results.md) | Compare raw coordinates | False alarms per ring 17 to 0 | Aligned frames; wrong declared maps |

The [memory ablation](applications/bots/memory-ablation.md) shows kept memory
reaching the shortest path in a stable maze and failing in a changing one.

### Verification

- 343 Python tests pass: 98 Architecture/application tests and 245 Labs tests
  across 26 eval folders.
- All 93 Python files compile with Python 3.11.
- Local Markdown links are checked as part of the release gate.
- All 26 Labs evals are indexed through the research connection map, and every
  result record has a direct status, an eval layer, and an explicit claim
  boundary.
- The counts above are checked against the tree by
  `scripts/check_public_base.py`.

### Not Included

- No mandatory SDK, top-level package, or package lock-in.
- No result measured on real data, and no production validation.
- No recipe-grounded eval.
- No medical, financial, security, predictive-maintenance, anomaly-detection,
  or reliability claim.

## v0.1.0 - 2026-08-26

This snapshot defined the first CGF public base.

### Included

- MIT-licensed CGF identity and docs-led posture.
- Substrate core primitive contract, derivative mechanics, extension
  components, templates, examples, and primitive implementation guide.
- Architecture execution graph, runtime spine, graph brain/spine, subgraph
  capsules, graph runtime memory, path-conditioned and path-gated operators,
  contracts, examples, and optional reference code.
- Granular Analysis, Multimodal Outcome Stack, Signal Review, and framework
  selection guide.
- Anchor / Lens / Promise, Visual Media Encoding, Hierarchical Execution
  Cycles, Belief State, Bayesian Filtering, and graph memory patterns.
- Applications for bots, medical image analysis review, signal / alert review,
  and industrial robot arm graph control demonstration.
- Labs evals with `contract-pass` result files for small fixtures.
- Publication, support, and security guidance for a standalone public release.

### Verification At Release

- 256 Python tests passed: 92 Architecture/application tests and 164 Labs
  tests in 25 eval folders.
- 71 Python files compiled with Python 3.11.

## How To Use

Start with [README.md](README.md), then use
[FOUNDATION_TRAVERSAL.md](FOUNDATION_TRAVERSAL.md) and
[templates/how-to-use-cgf.md](templates/how-to-use-cgf.md) to choose the right
CGF pieces for a project.

Maintainers should use [PUBLISHING.md](PUBLISHING.md) before tagging or creating
a hosted release.
