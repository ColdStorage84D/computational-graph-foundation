# Public Base Checklist

This checklist defines when the CGF public base can be treated as complete.

Status: the public base is complete for docs-led use when the final checks in
this file pass on the release commit. This does not mean all research,
applications, or optional code directions are finished.

## Public Base Contract

The public base is:

- self-contained;
- MIT-licensed;
- docs-led, not docs-only;
- free of mandatory SDK or package lock-in;
- organized around Substrate, Architecture, Applications, Research, Labs, and
  Archive;
- supported by section-local optional code and Labs evals where claims need a
  runnable check.

## Required Entry Paths

A developer or agent should be able to start from any of these files and find
the correct next step without guessing:

| Entry path | Required answer |
| --- | --- |
| [README.md](README.md) | What is CGF, and where should a new reader start? |
| [FOUNDATION_TRAVERSAL.md](FOUNDATION_TRAVERSAL.md) | Which CGF pieces fit a project shape, and what support exists? |
| [templates/how-to-use-cgf.md](templates/how-to-use-cgf.md) | How can a project apply CGF without adopting a mandatory SDK? |
| [templates/project-intake.md](templates/project-intake.md) | How should a project record its selected CGF mix and claim boundary? |
| [substrate/INDEX.md](substrate/INDEX.md) | How does a reader navigate core primitives, derivatives, extensions, templates, specs, and examples? |
| [architecture/INDEX.md](architecture/INDEX.md) | How does a reader navigate execution graph, spine, memory, contracts, framework cards, and examples? |
| [architecture/frameworks/selection-guide.md](architecture/frameworks/selection-guide.md) | Which reusable framework cards should a project use? |
| [applications/DEMO_GUIDE.md](applications/DEMO_GUIDE.md) | Which forkable application demo should a new developer start from? |
| [research/connection-map.md](research/connection-map.md) | What Research and Labs support exists for a concept? |
| [labs/evals/README.md](labs/evals/README.md) | Which evals are runnable, and what does each result label mean? |
| [ROADMAP.md](ROADMAP.md) | What is done, what is deferred, and what is next? |
| [RELEASE_NOTES.md](RELEASE_NOTES.md) | What changed in each public snapshot? |
| [RELEASE_MANIFEST.md](RELEASE_MANIFEST.md) | What was verified for the current public base snapshot? |
| [PUBLISHING.md](PUBLISHING.md) | How is a candidate prepared, verified, tagged, and published? |
| [agent.md](agent.md) | What standards should agents and contributors follow when editing or applying CGF? |
| [CONTRIBUTING.md](CONTRIBUTING.md) | What are the contribution boundaries? |
| [SUPPORT.md](SUPPORT.md) | Where should usage questions and bug reports go? |
| [SECURITY.md](SECURITY.md) | How should sensitive vulnerability reports be handled? |

## Supported Contract-Pass Claims

Each `contract-pass` claim is limited to the fixture and contract described by
its eval folder. The layer says what kind of contract it was: an isolated or
integration eval shows a concept is implemented as declared, and a
value-over-baseline eval also compares it with a simpler baseline on seeded
synthetic data.

| Area | Layer | Result |
| --- | --- | --- |
| Action-native computation | isolated | [labs/evals/action-native-computation/results.md](labs/evals/action-native-computation/results.md) |
| Anchor / Lens / Promise | isolated | [labs/evals/anchor-lens-promise/results.md](labs/evals/anchor-lens-promise/results.md) |
| Basis-mode representation | isolated | [labs/evals/basis-mode-representation/results.md](labs/evals/basis-mode-representation/results.md) |
| Bayesian filtering / state estimation | value-over-baseline | [labs/evals/bayesian-filtering/results.md](labs/evals/bayesian-filtering/results.md) |
| Causal intervention | isolated | [labs/evals/causal-intervention/results.md](labs/evals/causal-intervention/results.md) |
| CellComplexView | isolated | [labs/evals/cell-complex-view/results.md](labs/evals/cell-complex-view/results.md) |
| Evidence Graph Triage | value-over-baseline | [labs/evals/evidence-graph-triage/results.md](labs/evals/evidence-graph-triage/results.md) |
| Exterior placement | isolated | [labs/evals/exterior-placement/results.md](labs/evals/exterior-placement/results.md) |
| Gauge transport | value-over-baseline | [labs/evals/gauge-transport/results.md](labs/evals/gauge-transport/results.md) |
| Granular Analysis | value-over-baseline | [labs/evals/granular-analysis/results.md](labs/evals/granular-analysis/results.md) |
| Hierarchical execution cycles | isolated | [labs/evals/hierarchical-cycles/results.md](labs/evals/hierarchical-cycles/results.md) |
| Hyperbolic / metric placement | value-over-baseline | [labs/evals/hyperbolic-placement/results.md](labs/evals/hyperbolic-placement/results.md) |
| Information geometry | isolated | [labs/evals/information-geometry/results.md](labs/evals/information-geometry/results.md) |
| Local-Voting World Model | isolated | [labs/evals/local-voting-world-model/results.md](labs/evals/local-voting-world-model/results.md) |
| Multimodal Outcome Stack | integration | [labs/evals/multimodal-framework-mix/results.md](labs/evals/multimodal-framework-mix/results.md) |
| Path-conditioned and path-gated operators | value-over-baseline | [labs/evals/path-gated-operators/results.md](labs/evals/path-gated-operators/results.md) |
| Port-Hamiltonian flow | isolated | [labs/evals/port-hamiltonian-flow/results.md](labs/evals/port-hamiltonian-flow/results.md) |
| Provisional Graph Growth | isolated | [labs/evals/provisional-graph-growth/results.md](labs/evals/provisional-graph-growth/results.md) |
| Renormalization / coarse-graining | isolated | [labs/evals/renormalization-coarse-graining/results.md](labs/evals/renormalization-coarse-graining/results.md) |
| Sheaf consistency | isolated | [labs/evals/sheaf-consistency/results.md](labs/evals/sheaf-consistency/results.md) |
| Signal Review | isolated | [labs/evals/signal-review/results.md](labs/evals/signal-review/results.md) |
| Stochastic transition | isolated | [labs/evals/stochastic-transition/results.md](labs/evals/stochastic-transition/results.md) |
| Surrogate promotion | isolated | [labs/evals/surrogate-promotion/results.md](labs/evals/surrogate-promotion/results.md) |
| Topological rigidity | isolated | [labs/evals/topological-rigidity/results.md](labs/evals/topological-rigidity/results.md) |
| Visual Media Encoding | isolated | [labs/evals/visual-media-encoding/results.md](labs/evals/visual-media-encoding/results.md) |
| Weak form | isolated | [labs/evals/weak-form/results.md](labs/evals/weak-form/results.md) |

## Known Non-Blocking Gaps

These gaps do not block the public base when they remain clearly marked:

- action-native computation has a direct eval, but derivative mechanics as a
  whole still need broader direct evaluation;
- Attractor Diagnostics remains research-supported with no direct Labs eval yet;
- higher-dimensional topology remains research-only until narrowed into a
  card, example, or eval;
- offline replay cycles, cognitive map memory, and cued recall memory remain
  Architecture patterns without direct Labs evals yet;
- Architecture framework cards without direct evals must keep their claim
  boundary visible;
- applications remain examples, not proof that a domain is solved;
- no eval is recipe-grounded, and no result is measured on real data;
- the topics listed as still unreferenced in
  [research/references.md](research/references.md) have no checked public
  source yet.

## Final Checks

Run these checks from the directory containing this file before calling a
snapshot done:

```powershell
python scripts/check_public_base.py
python -m unittest discover -s architecture/reference/python/tests -p "test_*.py"
python -m unittest discover -s applications/bots -p "test_*.py"
python -m unittest discover -s applications/maze-graph-memory-bot -p "test_*.py"
python -m unittest discover -s applications/medical-image-analysis -p "test_*.py"
python -m unittest discover -s applications/industrial-robot-arm -p "test_*.py"
Get-ChildItem labs/evals -Directory |
  ForEach-Object { python -m unittest discover -s $_.FullName -p "test_*.py" }
```

After exporting CGF as the dedicated repository root, run the stricter
publication check on a clean candidate commit:

```powershell
python scripts/check_public_base.py --publication-candidate
```

Also verify, using the current release scan patterns:

```text
1. The automated public-base validator passes.
2. No Architecture operation terms appear in Substrate.
3. The CGF directory is the publication root, or the host repository has a
   deliberate root landing page and root-level automation.
4. The release commit has no unintended changes and has a documented version or
   snapshot identifier.
5. When history is preserved, no removed generated artifact, private draft, or
   unrelated project history remains reachable.
```

Expected results:

- all tests pass;
- no stale project-history wording appears;
- no Architecture operation terms appear in Substrate;
- no top-level package or SDK scaffolding appears;
- all local Markdown links resolve;
- the release tree is free of tracked generated artifacts;
- repository-root publishing metadata and automation are in the location used
  by the publishing host;
- all Labs result records and cross-layer evidence links agree;
- every result record declares a status, an eval layer, and a claim boundary;
- every value-over-baseline record has a runnable comparison, names its
  baseline, and says where the concept does not help;
- every extension study has a References section with an external source;
- the counts in the release notes and manifest equal the counts in the tree.
