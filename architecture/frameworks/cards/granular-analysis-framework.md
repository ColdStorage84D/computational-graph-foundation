# Granular Analysis Framework

## Purpose

Use this framework when one input should be analyzed through multiple lenses or
encoders, sent through multiple proposal nodes, and resolved into one or more
traceable outcome candidates.

## Reusable Concept

Granular Analysis is:

```text
one input -> many lenses / encoders -> many proposal nodes
  -> verifier / commit -> traceable outcome
```

The sales phrase is:

```text
many lenses, many proposers, one traceable outcome
```

## Uses CGF Pieces

- execution graph;
- lenses, encoders, and typed views;
- typed multimodal graph, when one case has heterogeneous parts;
- processor routing, when valid processors differ by task or view;
- proposal / verifier / commit;
- processor routing;
- path-conditioned and path-gated operators;
- trace and replay;
- evaluation discipline.

## Example Applications

- histology-like analysis;
- medical image analysis;
- robotics perception;
- security findings;
- trading signals;
- predictive maintenance;
- document analysis.

## When To Use

- Several lens outputs reveal different useful signals.
- One lens output should feed more than one proposal node.
- One proposal may need multiple lens outputs.
- The outcome should preserve competing proposals and rejected alternatives.
- A verifier should choose, review, defer, fallback, or abstain instead of
  blindly trusting one path.

## When Not To Use

- One deterministic view is enough.
- No competing proposals exist.
- Rejected alternatives do not need to be preserved.
- Lens ids, proposer ids, or verifier basis cannot be traced.

## Boundary

Granular Analysis does not make a domain truth claim by itself. It makes the
analysis graph visible so domain-specific validation can inspect it.

## Implementation Posture

Reference code may implement small stdlib-only fixtures. Any domain performance
claim needs a separate eval and claim boundary.
