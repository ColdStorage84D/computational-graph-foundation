# Cortical-Column World Model

## Purpose

The Cortical-Column World Model is a reusable Architecture pattern for systems
that learn local sensorimotor predictions from bounded observations and actions.

In CGF, a column is not a biological claim and not a maze cell. It is a local
subgraph surface that keeps evidence, predictions, prediction error, and
outcome-coupled memory for one view or sensorimotor context.

## Operating Shape

```text
bounded sensory frame + action context
-> local column encoders
-> action-conditioned predictions
-> lateral proposal aggregation
-> policy score + safety gate
-> committed action
-> observed outcome
-> prediction error
-> outcome-coupled memory update
```

This pattern is Architecture because it defines how runtime graph parts operate
around a declared subject. It does not add a new Substrate primitive.

## Columns

A column is a local sensorimotor predictive subgraph. It may own:

- a bounded sensory frame, such as a lidar slice, image patch, touch channel, or
  proprioceptive view;
- an action context, such as the command or motor primitive being considered;
- local encoders that produce feature vectors or compact evidence records;
- predictions for the next local sensory frame;
- residuals between predicted and observed outcomes;
- memory keyed by observed outcome, not by unsupported labels.

Columns should avoid hidden global authority. They return evidence, predictions,
uncertainty, and proposal terms to the parent runtime.

## Lateral Voting

Lateral voting is proposal aggregation across columns.

Each column may propose:

- a predicted next sensory state;
- a confidence or uncertainty term;
- an action preference or warning;
- a residual that says the local model is failing.

The aggregation step combines these proposals into a runtime decision surface.
It does not become the commit boundary by itself. The commit boundary remains in
the execution graph.

## Prediction Error And Memory

Prediction error compares expected and observed outcomes after an action is
committed and executed.

Memory updates are outcome-coupled:

- a prediction can create eligibility before the result is known;
- an observation resolves the prediction;
- residuals update the local model and uncertainty;
- repeated failure can reduce confidence or promote alternate proposals;
- replay should reconstruct the evidence, prediction, selected action, outcome,
  and update.

This connects the pattern directly to graph runtime memory.

## Safety Gates

Safety gates are commit blockers outside learned preference scoring.

A learned model may score an action highly, but a policy gate can still block it
when the action violates a declared constraint, such as collision risk, actuator
limit, or human review requirement. The gate should be explicit in the trace and
should not be treated as learned preference.

## Relationships

| CGF piece | Relationship |
| --- | --- |
| [Bot Graph](frameworks/cards/bot-graph-framework.md) | Provides the sense, propose, gate, act, observe, and learn operating shape. |
| [Predictive Action Graph](predictive-action-graph.md) | Provides candidate action prediction, selected first action, rejected alternatives, and trace. |
| [Sensor Ingestion](frameworks/cards/sensor-ingestion-framework.md) | Provides bounded frames and sensor views before columns encode them. |
| [Graph Runtime Memory](graph-runtime-memory.md) | Owns outcome-coupled memory rules and replay expectations. |
| [Subgraph Capsules](subgraph-capsules.md) | Bound each column as a local graph that cannot commit final state alone. |
| [Path-conditioned and path-gated operators](path-conditioned-and-path-gated.md) | Let path context condition scoring while gates block invalid advancement. |
| [Proposal / verifier / commit](proposal-verifier-commit.md) | Keeps column proposals separate from accepted action. |
| [Event log, trace, replay](event-log-trace-replay.md) | Reconstructs evidence, prediction, decision, outcome, and memory update. |

## Minimum Declaration

A cortical-column world-model implementation should declare:

```text
subject:
bounded sensory frames:
action context:
column surfaces:
prediction target:
lateral aggregation:
commit gate:
prediction error:
memory update:
trace records:
claim boundary:
```

## Current CGF Examples

- [labs/evals/cortical-column-world-model](../labs/evals/cortical-column-world-model/README.md)
  records the tiny-fixture `contract-pass` and its claim boundary.
- [applications/bots](../applications/bots/README.md) is the public Graph
  Memory Bot skeleton. It demonstrates the reusable loop of candidate actions,
  predicted outcomes, gates, trace, observed prediction error, memory update,
  and optional provisional route growth.
- [applications/maze-graph-memory-bot](../applications/maze-graph-memory-bot/README.md)
  runs the Graph Memory Bot action loop as a Webots maze fixture.
- [applications/industrial-robot-arm](../applications/industrial-robot-arm/README.md)
  remains a separate Webots safety-gated manipulator topology and trace demo.

## Claim Boundary

This pattern may be described as a local sensorimotor predictive world-model
architecture.

It does not claim:

- biological cortical realism;
- AGI, consciousness, or thinking;
- a guaranteed maze solver;
- benchmark success;
- safety beyond declared gates and tests;
- a mandatory SDK or runtime package.
