# Computational Graph Foundation (CGF)

CGF is an MIT-licensed set of patterns, written contracts, and small runnable
examples for systems that compute over graphs and have to show how they reached
a result.

It is documentation first, with stdlib-only Python wherever a contract is clear
enough to run. There is nothing to install. Read it, copy from it, or fork it.

## What You Get

Three results you can reproduce in a few minutes. Run them from the directory
containing this README, with Python 3.11 and no dependencies.

**A commit boundary the highest score cannot cross.** A proposal advances only
when its cited evidence path resolves.

```powershell
python labs/evals/path-gated-operators/comparison.py
```

On 4000 seeded cases, gating on a resolvable path cuts wrong commits from 65%
to 20% and abstains on 9%. When paths carry no information about correctness
the gate does not help.
[Result record](labs/evals/path-gated-operators/results.md).

**Status set by corroboration, never by score.** A finding is confirmed only
when a declared pair of distinct sources supports it.

```powershell
python labs/evals/evidence-graph-triage/comparison.py
```

On 5000 seeded findings, at equal review volume, corroboration makes 144 wrong
commits where score ranking makes 313. The advantage shrinks when two sources
are copies of each other.
[Result record](labs/evals/evidence-graph-triage/results.md).

**Memory that changes the next run.** A controller keeps what it learned about
a maze between episodes.

```powershell
python applications/bots/memory_ablation.py
```

On 300 seeded mazes, kept memory reaches the shortest path by the sixth
episode, 10.2 steps against 26.7 with memory reset. When the maze changes
between episodes, kept memory almost never reaches the goal.
[Result record](applications/bots/memory-ablation.md).

Each record states its assumptions, its baseline, and where the pattern does
not help.

## Run The Checks

```powershell
python scripts/check_public_base.py
python -m unittest discover -s architecture/reference/python/tests -p "test_*.py"
python -m unittest discover -s applications/bots -p "test_*.py"
python applications/bots/graph_memory_bot.py
```

The complete list is in [PUBLIC_BASE_CHECKLIST.md](PUBLIC_BASE_CHECKLIST.md).

## How It Is Organized

```text
CGF -> Substrate -> Architecture -> Applications
```

```text
substrate/      what is being computed: nine primitives every subject declares
architecture/   how a system operates around it: proposals, gates, commit,
                trace, replay, memory
applications/   worked examples in specific domains
research/       theory, references, and what each result covers
labs/           runnable evals with result records
archive/        historical material
```

The Substrate layer asks every subject to declare graph, typed field,
placement, state, action, constraint, evolution, readout, and validation. The
Architecture layer keeps proposing, verifying, and committing apart, so that
every decision can be traced and replayed.

## Where To Start

| You want to | Start with |
| --- | --- |
| Choose the right pieces for a project | [FOUNDATION_TRAVERSAL.md](FOUNDATION_TRAVERSAL.md) |
| Declare a subject | [substrate/README.md](substrate/README.md) |
| Build a bot, runtime, workflow, or processor that acts and remembers | [architecture/execution-graph.md](architecture/execution-graph.md) |
| Analyze one input through many lenses | [architecture/granular-analysis.md](architecture/granular-analysis.md) |
| Keep evidence, views, routes, proposals, and review apart | [architecture/multimodal-outcome-stack.md](architecture/multimodal-outcome-stack.md) |
| Pick reusable framework cards | [architecture/frameworks/README.md](architecture/frameworks/README.md) |
| Fork a demo | [applications/DEMO_GUIDE.md](applications/DEMO_GUIDE.md) |
| See a review application end to end | [applications/medical-image-analysis/walkthrough.md](applications/medical-image-analysis/walkthrough.md) |
| Apply CGF step by step | [templates/how-to-use-cgf.md](templates/how-to-use-cgf.md) |
| Record a project decision | [templates/project-intake.md](templates/project-intake.md) |
| See what supports a concept | [research/connection-map.md](research/connection-map.md) |

## How To Read The Results

Labs holds 26 evals. Each result record names its layer:

- 19 are isolated. They show a concept is implemented as declared, on small
  fixtures.
- 1 is an integration eval over a small mix of concepts.
- 6 are value-over-baseline. They compare a concept with a simpler baseline on
  seeded data and record where it does not help.

The labels are defined in [labs/evals/README.md](labs/evals/README.md). Public
sources for the theory are in [research/references.md](research/references.md).

## Scope

CGF is patterns, contracts, and reference code. It does not ship an SDK, a
graph database, or a solver, and code stays local to the section that owns it.
Every result here comes from synthetic fixtures, so none of it measures
performance on real data in any domain.

## Webots Applications

The Webots applications are optional. Their worlds target Webots R2025a and
reference version-pinned upstream PROTO and texture assets, so the first load
needs network access unless those assets are cached. The industrial robot arm
can use `ikpy` 3.0 or newer and otherwise uses its documented fallback.

## Project Documents

- Release: [RELEASE_NOTES.md](RELEASE_NOTES.md),
  [RELEASE_MANIFEST.md](RELEASE_MANIFEST.md), [ROADMAP.md](ROADMAP.md), and
  [PUBLISHING.md](PUBLISHING.md).
- Contributing: [agent.md](agent.md), [CONTRIBUTING.md](CONTRIBUTING.md), and
  [SUPPORT.md](SUPPORT.md).
- Security reports: [SECURITY.md](SECURITY.md).

## License

CGF is released under the MIT License. See [LICENSE](LICENSE).
