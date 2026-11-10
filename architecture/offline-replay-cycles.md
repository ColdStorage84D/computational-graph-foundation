# Offline Replay Cycles

Offline Replay Cycles are Architecture patterns for resolving late
outcomes, replaying real traces, and generating counterfactual hypotheses
without confusing those hypotheses with outcome-backed memory.

## Definition

```text
eligible committed traces
  -> late outcome resolution
  -> real-trace replay
  -> counterfactual simulation
  -> promotion review
```

The key rule is simple: real committed traces with resolved outcomes can update
value. Counterfactual simulations can create hypotheses, but not durable truth.

## Cycle Types

| Cycle | Purpose |
| --- | --- |
| Resolve | Attach late outcomes to eligible committed traces. |
| Replay | Re-run real traces for consolidation or review. |
| Simulate | Generate counterfactual candidates or failure hypotheses. |
| Promotion review | Decide whether repeated resolved outcomes justify promotion. |

## Minimum Record

```text
offline_cycle_id
source_trace_refs
cycle_type
counterfactual_status
resolved_outcome_refs
promotion_candidate_refs
blocked_reason
trace_refs
```

## Boundary

Simulated output is not observed outcome. It can guide future proposals or tests,
but value and durable promotion require resolved real outcomes.

## Promotion Review And Provisional Growth

Offline replay can support
[Provisional Graph Growth](provisional-graph-growth.md) by replaying real
traces, comparing candidates against baseline behavior, and checking whether a
pattern is stable instead of a burst.

Counterfactual cycles may propose candidate growth patches. They cannot promote
those patches as durable graph state without resolved evidence, review, and a
rollback policy.

## Claim Boundary

This is a docs-led Architecture pattern. No direct Labs eval exists yet.

## References

Public sources for replaying stored experience and for learning from simulated experience, which earlier drafts of this page called dream cycles.

- [Self-improving reactive agents based on reinforcement learning, planning and teaching](https://doi.org/10.1007/BF00992699), Lin (1992). Experience replay: reusing stored transitions for learning.
- [Human-level control through deep reinforcement learning](https://doi.org/10.1038/nature14236), Mnih et al. (2015). Experience replay at scale in a learning agent.
- [Dream to Control: Learning Behaviors by Latent Imagination](https://arxiv.org/abs/1912.01603), Hafner, Lillicrap, Ba, and Norouzi (2019). Learning from rollouts imagined by a model, kept separate from real experience.
- [Reactivation of Hippocampal Ensemble Memories During Sleep](https://doi.org/10.1126/science.8036517), Wilson and McNaughton (1994). The observation in animals that waking activity patterns are replayed offline.
