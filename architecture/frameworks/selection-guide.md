# Architecture Framework Selection Guide

Use this guide when a project needs Architecture framework cards but the right
mix is not obvious.

The decision path is:

```text
project shape -> failure mode -> framework cards
  -> owning Architecture docs -> eval / claim boundary
```

Framework cards are reusable patterns. They are not SDK requirements,
application ownership claims, package surfaces, or proof that a domain is
solved.

## Selection Rule

Choose the smallest framework mix that prevents the real failure mode.

Do not select a framework only because its vocabulary sounds relevant. Select
it when skipping it would create hidden authority, unbounded evidence, leakage,
invalid processor fit, unsupported output, missing review boundary, or
untraceable state change.

## Selection Matrix

| Project shape | Use these framework cards | Add these Architecture docs | Avoid if | Current eval support |
| --- | --- | --- | --- | --- |
| Simple evidence review | [Evidence record](cards/evidence-record-framework.md), [proposer-verifier](cards/proposer-verifier-framework.md), optionally [human review](cards/human-review-framework.md) | [anchor-lens-promise.md](../anchor-lens-promise.md), [event-log-trace-replay.md](../event-log-trace-replay.md), [contracts/trace-contract.md](../contracts/trace-contract.md) | Source evidence can be represented directly and no review or trace is needed. | `contract-pass` for stable lens identity; no direct full review eval yet. |
| Multimodal evidence-to-outcome case | [Evidence record](cards/evidence-record-framework.md), [typed multimodal graph](cards/typed-multimodal-graph-framework.md), [feature view](cards/feature-view-framework.md), [processor routing](cards/processor-routing-framework.md), [proposer-verifier](cards/proposer-verifier-framework.md), [human review](cards/human-review-framework.md) | [multimodal-outcome-stack.md](../multimodal-outcome-stack.md), [granular-analysis.md](../granular-analysis.md), [examples/multimodal-review-flow.md](../examples/multimodal-review-flow.md) | There is one deterministic view, no route choice, and no need to preserve alternatives. | `contract-pass` for [multimodal-framework-mix](../../labs/evals/multimodal-framework-mix/results.md). |
| Granular Analysis | [Granular Analysis](cards/granular-analysis-framework.md), [feature view](cards/feature-view-framework.md), [proposer-verifier](cards/proposer-verifier-framework.md), optionally [processor routing](cards/processor-routing-framework.md) | [granular-analysis.md](../granular-analysis.md), [proposal-verifier-commit.md](../proposal-verifier-commit.md), [event-log-trace-replay.md](../event-log-trace-replay.md) | One input has one valid lens, one proposal, and no value in preserving rejected alternatives. | `contract-pass` for [granular-analysis](../../labs/evals/granular-analysis/results.md). |
| Bot / agent execution graph | [Bot graph](cards/bot-graph-framework.md), [proposer-verifier](cards/proposer-verifier-framework.md), optionally [sensor ingestion](cards/sensor-ingestion-framework.md) and [human review](cards/human-review-framework.md) | [execution-graph.md](../execution-graph.md), [graph-brain-and-spine.md](../graph-brain-and-spine.md), [runtime-spine.md](../runtime-spine.md), [subgraph-capsules.md](../subgraph-capsules.md) | The system is a simple script with no proposal, gate, trace, or outcome feedback boundary. | reference tests only for [reference/python](../reference/python/README.md); app tests only for [applications/bots](../../applications/bots/README.md). |
| Sensorimotor world-model controller | [Cortical-Column World Model](cards/cortical-column-world-model-framework.md), [Bot graph](cards/bot-graph-framework.md), [sensor ingestion](cards/sensor-ingestion-framework.md), [proposer-verifier](cards/proposer-verifier-framework.md) | [cortical-column-world-model.md](../cortical-column-world-model.md), [predictive-action-graph.md](../predictive-action-graph.md), [graph-runtime-memory.md](../graph-runtime-memory.md), [action-accounting-policy.md](../action-accounting-policy.md) | The controller is a global route planner, a fixed rule script, or a biological/AGI claim. | `contract-pass` for [cortical-column-world-model](../../labs/evals/cortical-column-world-model/results.md), plus app tests for [Graph Memory Bot](../../applications/bots/README.md) and [Maze Graph Memory Bot](../../applications/maze-graph-memory-bot/README.md); no biological, AGI, benchmark, autonomy, or guaranteed-solver claim. |
| Graph runtime memory | [Bot graph](cards/bot-graph-framework.md), [proposer-verifier](cards/proposer-verifier-framework.md) | [graph-runtime-memory.md](../graph-runtime-memory.md), [memory-outcome-feedback.md](../memory-outcome-feedback.md), [contracts/outcome-contract.md](../contracts/outcome-contract.md) | Notes or preferences do not change future graph behavior through committed outcomes. | reference tests only for [reference/python](../reference/python/README.md); app tests only for [applications/bots](../../applications/bots/README.md). |
| Provisional route or graph growth | [Provisional Graph Growth](cards/provisional-graph-growth-framework.md), [Bot graph](cards/bot-graph-framework.md), [proposer-verifier](cards/proposer-verifier-framework.md), optionally [human review](cards/human-review-framework.md) | [provisional-graph-growth.md](../provisional-graph-growth.md), [graph-runtime-memory.md](../graph-runtime-memory.md), [subgraph-capsules.md](../subgraph-capsules.md), [offline-replay-dream-cycles.md](../offline-replay-dream-cycles.md), [applications/bots/provisional-growth-example.md](../../applications/bots/provisional-growth-example.md) | The graph change is an authored release change, or the evidence is a one-off spike with no promotion and rollback path. | `contract-pass` for [provisional-graph-growth](../../labs/evals/provisional-graph-growth/results.md); no autonomous self-improvement, production safety, or broad learning-performance claim. |
| Human review workflow | [Human review](cards/human-review-framework.md), [evidence record](cards/evidence-record-framework.md), [proposer-verifier](cards/proposer-verifier-framework.md) | [proposal-verifier-commit.md](../proposal-verifier-commit.md), [contracts/commit-contract.md](../contracts/commit-contract.md), [contracts/outcome-contract.md](../contracts/outcome-contract.md) | No human or policy boundary exists and outputs are fully deterministic. | no direct Labs eval yet. |
| Processor routing / model routing | [Processor routing](cards/processor-routing-framework.md), [feature view](cards/feature-view-framework.md), [proposer-verifier](cards/proposer-verifier-framework.md) | [path-conditioned-and-path-gated.md](../path-conditioned-and-path-gated.md), [path-conditioned-operators.md](../path-conditioned-operators.md), [proposal-verifier-commit.md](../proposal-verifier-commit.md) | One processor is always valid and route failures do not change risk or output. | no direct Labs eval yet; covered indirectly by `contract-pass` multimodal-framework-mix fixture when used in that stack. |
| Security finding graph | [Code security graph](cards/code-security-graph-framework.md), [evidence record](cards/evidence-record-framework.md), [proposer-verifier](cards/proposer-verifier-framework.md), optionally [human review](cards/human-review-framework.md) | [event-log-trace-replay.md](../event-log-trace-replay.md), [contracts/proposal-contract.md](../contracts/proposal-contract.md), [contracts/trace-contract.md](../contracts/trace-contract.md) | Findings do not need evidence paths, verification, review, or export. | no direct Labs eval yet. |
| Finding triage queue | [Evidence graph triage](cards/evidence-graph-triage-framework.md), [evidence record](cards/evidence-record-framework.md), [proposer-verifier](cards/proposer-verifier-framework.md), optionally [human review](cards/human-review-framework.md) | [graph-runtime-memory.md](../graph-runtime-memory.md), [memory-outcome-feedback.md](../memory-outcome-feedback.md) | One source is authoritative, every finding is reviewed, or no outcome is ever observed. | `contract-pass` for [evidence-graph-triage](../../labs/evals/evidence-graph-triage/results.md); no detection, triage-quality, or security claim. |
| Cache invalidation / derived view refresh | [Cache invalidation](cards/cache-invalidation-framework.md), optionally [evidence record](cards/evidence-record-framework.md) | [execution-graph.md](../execution-graph.md), [event-log-trace-replay.md](../event-log-trace-replay.md), [contracts/persistence-contract.md](../contracts/persistence-contract.md) | Derived state can be rebuilt trivially and stale data cannot affect users or decisions. | no direct Labs eval yet. |
| Sensor ingestion | [Sensor ingestion](cards/sensor-ingestion-framework.md), [feature view](cards/feature-view-framework.md), optionally [processor routing](cards/processor-routing-framework.md) | [anchor-lens-promise.md](../anchor-lens-promise.md), [visual-media-encoding.md](../visual-media-encoding.md) when media is involved, [lenses-adapters-operators.md](../lenses-adapters-operators.md), [event-log-trace-replay.md](../event-log-trace-replay.md), [execution-graph.md](../execution-graph.md) | Raw observations are already bounded and no frame, view, adapter, or failure record is needed. | `contract-pass` for stable lens identity and visual-media record shape; no full ingestion eval yet. |
| Medical image analysis review | [Evidence record](cards/evidence-record-framework.md), [typed multimodal graph](cards/typed-multimodal-graph-framework.md), [feature view](cards/feature-view-framework.md), [Granular Analysis](cards/granular-analysis-framework.md), [processor routing](cards/processor-routing-framework.md), [proposer-verifier](cards/proposer-verifier-framework.md), [human review](cards/human-review-framework.md) | [multimodal-outcome-stack.md](../multimodal-outcome-stack.md), [granular-analysis.md](../granular-analysis.md), [applications/medical-image-analysis/walkthrough.md](../../applications/medical-image-analysis/walkthrough.md), [applications/medical-image-analysis/claim-boundary.md](../../applications/medical-image-analysis/claim-boundary.md) | The project would imply medical, clinical, or safety authority without domain validation. | application tests only for [applications/medical-image-analysis](../../applications/medical-image-analysis/README.md); no medical claim. |
| Trading / predictive maintenance signal review | [Signal review](cards/signal-review-framework.md), [feature view](cards/feature-view-framework.md), [Granular Analysis](cards/granular-analysis-framework.md), [processor routing](cards/processor-routing-framework.md), [proposer-verifier](cards/proposer-verifier-framework.md), optionally [evidence record](cards/evidence-record-framework.md), optionally [human review](cards/human-review-framework.md) | [granular-analysis.md](../granular-analysis.md), [path-conditioned-and-path-gated.md](../path-conditioned-and-path-gated.md), [event-log-trace-replay.md](../event-log-trace-replay.md) | Signals have one deterministic rule and no competing proposals, review, or audit need. | `contract-pass` for [signal-review](../../labs/evals/signal-review/results.md); no financial, prediction, reliability, anomaly-performance, or maintenance claim. |
| Ecommerce or service workflow | [Evidence record](cards/evidence-record-framework.md), [proposer-verifier](cards/proposer-verifier-framework.md), optionally [cache invalidation](cards/cache-invalidation-framework.md) and [human review](cards/human-review-framework.md) | [execution-graph.md](../execution-graph.md), [examples/ecommerce-runtime-path.md](../examples/ecommerce-runtime-path.md), [proposal-verifier-commit.md](../proposal-verifier-commit.md) | The service is a simple transaction with no proposal, verification, derived view, or trace need. | no direct Labs eval yet. |
| Local specialist subgraph inside a larger runtime | [Bot graph](cards/bot-graph-framework.md), [proposer-verifier](cards/proposer-verifier-framework.md), optionally [feature view](cards/feature-view-framework.md) | [subgraph-capsules.md](../subgraph-capsules.md), [execution-graph.md](../execution-graph.md), [contracts/trace-contract.md](../contracts/trace-contract.md) | The local graph can safely commit final state without parent authority or trace. | reference tests only for Architecture reference code; no direct Labs eval yet. |

## How To Record The Decision

When applying this guide, write down:

```text
project shape:
failure mode:
selected framework mix:
owning Architecture docs:
skipped framework cards:
eval / claim boundary:
reason this mix is enough:
```

If the selected mix has no direct Labs eval, state that plainly. Do not replace
missing eval support with claims from a nearby application.

## Common Mistakes

- Treating an application example as the owner of a reusable framework.
- Selecting every framework card instead of the smallest useful mix.
- Treating a proposal, processor output, or model score as commit authority.
- Using an eval result outside the fixture or contract it tested.
- Hiding source evidence, route failure, rejected proposals, or review state.
- Adding Architecture when a project only needs a Substrate declaration.
