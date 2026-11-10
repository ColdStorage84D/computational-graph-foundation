# Local-Voting World Model Framework

## Purpose

Use this framework when a system needs local sensorimotor predictive subgraphs
whose predictions, uncertainty, and outcome memory shape action proposals.

## Reusable Concept

A column is a local evidence, prediction, and memory surface. It is
not a maze cell. Columns encode bounded sensory
views, predict outcomes under candidate actions, report residuals, and update
memory only after observed outcomes.

Lateral voting aggregates column proposals. Safety gates remain outside learned
preference scoring and can block commits.

## Uses CGF Pieces

- [../../execution-graph.md](../../execution-graph.md)
- [../../predictive-action-graph.md](../../predictive-action-graph.md)
- [../../graph-runtime-memory.md](../../graph-runtime-memory.md)
- [../../subgraph-capsules.md](../../subgraph-capsules.md)
- [../../proposal-verifier-commit.md](../../proposal-verifier-commit.md)
- [../../action-accounting-policy.md](../../action-accounting-policy.md)
- [sensor-ingestion-framework.md](sensor-ingestion-framework.md)
- [bot-graph-framework.md](bot-graph-framework.md)

## Example Applications

- stochastic robot or Webots controllers;
- sensorimotor learning demos;
- local predictive control for tools, games, or process automation;
- multi-sensor action selection with visible prediction error.

## When To Use

Use it when:

- the controller should learn from continuous sensorimotor outcomes;
- local views need separate predictions before aggregation;
- uncertainty and prediction error should affect future action selection;
- safety gates must remain explicit commit blockers;
- replay should show evidence, prediction, selected action, outcome, and memory
  update.

## When Not To Use

Do not use it when:

- a simple deterministic rule or planner is enough;
- the project needs a proven global route planner;
- the implementation would relabel maze cells or named states as columns;
- the claim depends on guaranteed benchmark success.

## Boundary

The framework owns the Architecture pattern for local predictive subgraphs,
proposal aggregation, outcome-coupled memory, and safety gate separation.

Applications own their sensors, action set, simulator or hardware adapter,
runtime files, and claim boundary.

## Implementation Posture

This is a reusable Architecture card, not an SDK. Implementations may use
nearest-neighbor memory, prototypes, learned models, stochastic sampling, or
deterministic selection as long as proposals, gates, traces, and outcome memory
remain visible.

## Current Eval Support

The [Local-Voting World Model eval](../../../labs/evals/local-voting-world-model/README.md)
has a tiny-fixture `contract-pass`. It checks feature-location memory, lateral
voting, rejected alternatives, and next-feature prediction only; it does not
support benchmark or real-world performance claims.
