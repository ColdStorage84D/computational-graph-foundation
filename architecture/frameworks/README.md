# Architecture Frameworks

Architecture frameworks are reusable CGF operating patterns.

In this folder, framework does not mean mandatory SDK, package, runtime, or
lock-in. It means a named pattern that a developer can copy, fork, adapt, or
ignore when building a project.

Applications such as bots, medical image analysis, security, cache, trading, and ecommerce are
examples of use. They are not the owners of the concepts.

## What A Framework Card Does

A framework card answers:

```text
What problem shape does this pattern solve?
Which CGF pieces does it use?
What records, roles, gates, or traces must be visible?
Which applications can use it?
When is it the wrong fit?
What implementation claims are not made yet?
```

## Reading Order

Start here when a project looks like an operating system, processor family,
review workflow, evidence workflow, bot, model-routing problem, or domain graph
rather than a single Substrate subject.

Use [../granular-analysis.md](../granular-analysis.md) when the project has one
input feeding many lenses, encoders, proposal nodes, or outcome candidates.

Use [../multimodal-outcome-stack.md](../multimodal-outcome-stack.md) when the
project has source evidence, typed records, feature views, processor routes,
proposals, review state, and traceable outcomes.

Use [cards/provisional-graph-growth-framework.md](cards/provisional-graph-growth-framework.md)
when recurring evidence may justify candidate graph routes or local structure,
but durable graph mutation must remain gated and reversible.

```text
README.md -> selection-guide.md -> registry.md -> cards/README.md
```

Then read the owning Architecture docs:

```text
../execution-graph.md
../runtime-spine.md
../graph-brain-and-spine.md
../subgraph-capsules.md
../graph-runtime-memory.md
../path-conditioned-and-path-gated.md
../proposal-verifier-commit.md
../event-log-trace-replay.md
```

## Current Framework Cards

- [selection-guide.md](selection-guide.md)
- [cards/bot-graph-framework.md](cards/bot-graph-framework.md)
- [cards/evidence-record-framework.md](cards/evidence-record-framework.md)
- [cards/typed-multimodal-graph-framework.md](cards/typed-multimodal-graph-framework.md)
- [cards/feature-view-framework.md](cards/feature-view-framework.md)
- [cards/granular-analysis-framework.md](cards/granular-analysis-framework.md)
- [cards/local-voting-world-model-framework.md](cards/local-voting-world-model-framework.md)
- [cards/provisional-graph-growth-framework.md](cards/provisional-graph-growth-framework.md)
- [cards/proposer-verifier-framework.md](cards/proposer-verifier-framework.md)
- [cards/processor-routing-framework.md](cards/processor-routing-framework.md)
- [cards/human-review-framework.md](cards/human-review-framework.md)
- [cards/cache-invalidation-framework.md](cards/cache-invalidation-framework.md)
- [cards/code-security-graph-framework.md](cards/code-security-graph-framework.md)
- [cards/sensor-ingestion-framework.md](cards/sensor-ingestion-framework.md)
- [cards/signal-review-framework.md](cards/signal-review-framework.md)

## Rule

Keep the reusable framework concept separate from the application that first
shows it.

```text
framework card = reusable Architecture pattern
application = one concrete use of one or more framework cards
reference code = optional section-local implementation
```

If a page cannot be reused outside one domain, it belongs in `applications/`,
not here.
