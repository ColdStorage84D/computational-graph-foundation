# Engram / Spatial Memory

Engram / Spatial Memory is the Architecture pattern for sparse, reactivatable
episode traces that bind where, what, action, and outcome.

## Definition

```text
episode trace
  -> sparse recall support
  -> partial cue reactivation
  -> proposal evidence
```

It is useful when a future situation should recall a prior episode from partial
spatial, visual, action, or outcome cues.

## Minimum Record

```text
engram_id
episode_trace_refs
where_refs
what_refs
action_refs
outcome_refs
reactivation_cues
confidence
```

## When To Use

- A system should reactivate prior episodes from partial cues.
- Spatial or visual context matters to recall.
- Episode traces should remain sparse and inspectable.
- Recalled evidence should stay separate from final decision authority.

## Boundary

An engram-like trace is recall support. It can provide proposal evidence, but it
cannot create value, truth, or policy by itself.

## Claim Boundary

This is a docs-led Architecture guide. No direct Labs eval exists yet.
