# Cognitive Map Memory

Cognitive Map Memory is the Architecture pattern for reusable relational
structure over physical, conceptual, or latent task spaces.

## Definition

```text
observations + actions + outcomes
  -> relational map state
  -> recall candidates
  -> proposal evidence
```

The map organizes where things are, how they relate, and which paths or regions
have mattered before.

## Minimum Record

```text
map_id
node_refs
relation_refs
place_or_context_refs
evidence_refs
value_refs
uncertainty
last_outcome_refs
```

## When To Use

- A task benefits from reusable spatial, conceptual, or latent structure.
- Recall depends on relations rather than only text or scalar scores.
- Prior paths or regions should guide future proposals.
- Outcome-backed value should shape future route preference.

## Boundary

A cognitive map is a recall and organization surface. It is not a separate
foundation, not policy authority, and not durable truth without outcome support.

## Claim Boundary

This is a docs-led Architecture guide. No direct Labs eval exists yet.
