# Computational Graph Foundation (CGF)

Computational Graph Foundation (CGF) is an open, MIT-licensed base for
describing and building graph-shaped computational systems.

CGF is docs-led first, with optional code examples, reference implementations,
and concept implementations expected as the contracts become clear. It is not
an SDK requirement, package lock-in, or a rulebook. Developers may read the
ideas, copy code, fork it, implement the patterns in their own style, or ignore
the suggested structure.

The public base is self-contained. It is ready when a developer can enter from
this README, choose the right layer, inspect claim boundaries, run local checks,
and build independently.

The public ladder is:

```text
CGF -> Substrate -> Architecture -> Applications
```

## Quick Start

CGF has no required Python package dependencies. The current public-base checks
are verified with Python 3.11. Run commands from the directory containing this
README:

```powershell
python -m unittest discover -s architecture/reference/python/tests -p "test_*.py"
python -m unittest discover -s applications/bots -p "test_*.py"
python applications/bots/graph_memory_bot.py
```

The Webots applications are optional. Their checked-in worlds target Webots
R2025a. The industrial robot arm can optionally use `ikpy` 3.0 or newer and
otherwise uses its documented fallback path.

The Webots worlds reference version-pinned upstream R2025a PROTO and texture
assets. Their first simulator load therefore requires network access unless
those Webots assets are already cached locally.

For the complete release verification commands, see
[PUBLIC_BASE_CHECKLIST.md](PUBLIC_BASE_CHECKLIST.md). For repository layout,
release hygiene, tagging, and publication steps, see
[PUBLISHING.md](PUBLISHING.md).

## What This Repo Is

- A shared vocabulary for graph-shaped computation.
- A clean Substrate specification for graph, fields, placement, action,
  constraints, evolution, readout, and validation.
- An Architecture layer for execution graphs, brain/spine coordination,
  subgraph capsules, graph runtime memory, path-conditioned operation,
  path-gated control, proposals, commits, trace, replay, and evaluation.
- Granular Analysis as a pitch pillar: many lenses, many proposers, one
  traceable outcome.
- A Multimodal Outcome Stack for cases that need external evidence records,
  typed graph records, feature views, processor routes, proposals, review, and
  traceable outcomes.
- Signal Review for signal, alert, anomaly, risk, and operational review
  workflows where raw signals should not become direct authority.
- A reusable Architecture framework catalog for concepts that can be applied
  across many applications.
- Section-local code examples and reference implementations where the owning
  docs have a clear contract.
- A place for independent applications, internal research notes, labs, and
  archive material.

## What This Repo Is Not

- Not a mandatory SDK.
- Not a promise that all code must live in one central package.
- Not a graph database.
- Not a GNN framework.
- Not an agent framework.
- Not a universal solver.
- Not a claim that every domain is already solved.

## Sections

```text
substrate/      first technical layer: what is being computed
architecture/   how CGF systems operate around substrate subjects
applications/   independent domain uses
research/       self-contained theory, references, and claim boundaries
labs/           active experiments
archive/        historical material
```

Start with [FOUNDATION_TRAVERSAL.md](FOUNDATION_TRAVERSAL.md) when you need to
choose the right CGF pieces for a project. Start with
[substrate/README.md](substrate/README.md) when you already know you need to
declare a Substrate subject.

Start with [architecture/execution-graph.md](architecture/execution-graph.md)
when the problem is a bot, runtime, workflow, processor, or system that must
act, remember outcomes, and replay decisions.

Start with [architecture/granular-analysis.md](architecture/granular-analysis.md)
when one input should be analyzed through many lenses, encoders, or proposal
nodes before producing a traceable outcome.

Start with
[architecture/multimodal-outcome-stack.md](architecture/multimodal-outcome-stack.md)
when source evidence, typed records, feature views, processor routes, proposals,
review state, and trace all need to stay separated.

Start with [applications/DEMO_GUIDE.md](applications/DEMO_GUIDE.md) when you
want a forkable demo path with honest claim boundaries: Signal Review, Medical
Image Analysis, and Graph Memory Bot.

Start with [applications/medical-image-analysis/walkthrough.md](applications/medical-image-analysis/walkthrough.md)
when you want to see that stack used in a medical image analysis review application with
no medical claim.

Start with [architecture/frameworks/README.md](architecture/frameworks/README.md)
when you need reusable framework concepts before choosing an application.

Use [templates/project-intake.md](templates/project-intake.md) to record a
project-level CGF traversal decision.

Use [templates/how-to-use-cgf.md](templates/how-to-use-cgf.md) for a short
step-by-step guide to applying CGF without adopting a mandatory SDK.

Current release notes live in [RELEASE_NOTES.md](RELEASE_NOTES.md). The public
base release manifest lives in [RELEASE_MANIFEST.md](RELEASE_MANIFEST.md).
Readiness is tracked in [PUBLIC_BASE_CHECKLIST.md](PUBLIC_BASE_CHECKLIST.md)
and summarized in [ROADMAP.md](ROADMAP.md).

For editing and creation standards, see [agent.md](agent.md).
For contribution help, see [CONTRIBUTING.md](CONTRIBUTING.md) and
[SUPPORT.md](SUPPORT.md). Report security-sensitive problems through the
process in [SECURITY.md](SECURITY.md).

## License

CGF is released under the MIT License. See [LICENSE](LICENSE).
