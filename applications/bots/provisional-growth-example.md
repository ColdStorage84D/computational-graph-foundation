# Bot Route Growth Example

This example shows how a bot-shaped execution graph can use
[Provisional Graph Growth](../../architecture/provisional-graph-growth.md)
without letting a spike or one bad run mutate durable graph structure.

It is an application walkthrough, not a new runtime and not a production
self-improvement claim.

Reusable framework card:
[Provisional Graph Growth framework](../../architecture/frameworks/cards/provisional-graph-growth-framework.md).

Runnable companion:
[provisional_route_growth.py](provisional_route_growth.py).

## Scenario

A bot has two known routes and one review fallback:

```text
known pattern A -> known route A
known pattern B -> known route B
unknown pattern -> review fallback
```

During operation, the same unknown pattern appears repeatedly. The graph should
not keep pretending the fallback is enough, but it also should not permanently
add a new route from one burst of evidence.

The CGF route-growth path is:

```text
known pattern -> existing route
recurring unknown pattern -> provisional graph capsule
candidate variants -> shadow scoring
stable support -> promotion gate
regression after promotion -> rollback
burst / spike -> held, not promoted
```

## Graph Roles

| Role | Example record | Authority |
| --- | --- | --- |
| Known route | `route:known_a` | Durable route, already accepted. |
| Review fallback | `route:review_fallback` | Safe handling for unknown or unsupported patterns. |
| Observation | `trace:c:1`, `trace:c:2`, `trace:c:3` | Evidence only. |
| Provisional capsule | `provisional:unknown:c` | Can explain, shadow-score, or request review. |
| Candidate variant | `new_edge`, `new_rule`, `new_route`, `new_specialist` | No commit authority. |
| Stability guard | `stable`, `burst`, `one_off`, `unstable` | Blocks promotion unless support is stable. |
| Growth patch | proposed nodes and edges | Durable only after promotion. |
| Rollback record | regression after promotion | Restores fallback when promoted behavior fails. |

## Bot Flow

### 1. Known Pattern Uses Existing Route

```text
input pattern: known:a
route: route:known_a
growth: none
reason: durable route already exists
```

Known patterns should not create provisional graph structure. The graph should
prefer the existing accepted route.

### 2. First Unknown Pattern Falls Back

```text
input pattern: unknown:c
route: route:review_fallback
growth: none yet
reason: insufficient recurrence
```

One unknown event is evidence, not a graph-growth mandate.

### 3. Recurring Unknown Pattern Creates Provisional Capsule

```text
observations:
  trace:c:1 at tick 1
  trace:c:2 at tick 5
  trace:c:3 at tick 11

created:
  provisional:unknown:c
```

The capsule is allowed to organize evidence and candidate variants. It cannot
commit itself into the durable graph.

### 4. Candidate Variants Are Bounded

```text
candidate variants:
  new_edge
  new_rule
  new_route
  new_specialist
```

The bot does not create unlimited routes. Candidates remain bounded,
probationary, and traceable.

Risky variants enter quarantine. Low-affinity variants can be retired.

### 5. Shadow Scoring Has No Commit Authority

```text
variant: new_route
score: 0.74
authority: shadow_only
can_commit: false
```

Shadow scores can inform review or promotion. They do not mutate durable graph
state.

### 6. Stability Guard Blocks Spikes

```text
burst observations:
  trace:d:1 at tick 20
  trace:d:2 at tick 21

temporal shape: burst
accepted: false
reason: burst_pattern
```

Burst evidence stays visible, but it cannot promote a durable route by itself.

### 7. Promotion Requires A Gate

A growth patch can become durable only when it has:

```text
evidence refs
stable temporal support
baseline comparison pass
held-out check pass
safety / policy review pass
risk below limit
rollback policy
trace refs
```

If the gate passes, the route can be promoted:

```text
unknown:c -> route:new_route
```

### 8. Regression Rolls Back

If the promoted route later performs worse than the baseline or violates its
rollback condition:

```text
unknown:c -> route:review_fallback
provisional:unknown:c -> rolled_back
```

Rollback is part of the graph memory record, not a hidden edit.

## What This Demonstrates

This bot example demonstrates:

- recurring evidence can be represented without immediate durable mutation;
- a bot can test candidate routes in shadow mode;
- spikes and bursts are distinguished from stable support;
- durable graph changes require promotion and rollback rules;
- regression returns the bot to a fallback route.

## Claim Boundary

This walkthrough inherits the CGF-local eval boundary:
[../../labs/evals/provisional-graph-growth/results.md](../../labs/evals/provisional-graph-growth/results.md).

It does not claim autonomous self-improvement, production safety, broad
learning performance, or better bot performance than a hand-authored route.
