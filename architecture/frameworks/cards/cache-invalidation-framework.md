# Cache Invalidation Framework

## Purpose

Use this framework when derived views, summaries, features, indexes, or
materialized outputs must update from source dependency paths.

## Reusable Concept

Represent source entities, derived records, dependencies, invalidation events,
refresh proposals, commits, and replayable projections as an execution graph.

## Uses CGF Pieces

- dependency graph;
- event log;
- path-state graph;
- proposal / verifier / commit;
- trace and replay;
- persistence contract.

## Example Applications

- application caches;
- search indexes;
- feature stores;
- data products;
- report materialization;
- record summaries.

## When To Use

- Derived state can become stale.
- Invalidation needs to follow explicit source dependency paths.
- Refresh or purge should be auditable.
- Replay should rebuild the current projection.

## When Not To Use

- All state is recomputed on demand.
- Staleness has no user, policy, or correctness impact.
- Dependency paths cannot be declared.

## Boundary

Invalidation is operational state, not a Substrate primitive. It belongs to the
execution graph around a declared subject.

## Implementation Posture

Implementation should start with small dependency fixtures and replay checks
before claiming cache correctness.
