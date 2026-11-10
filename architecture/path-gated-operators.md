# Path-Gated Operators

Path-gated operators use an explicit gate to control how path evidence
influences computation or whether a proposal can advance.

They answer:

```text
How much is this path allowed to affect computation, and can it advance?
```

## Problem Solved

Some systems need path evidence to affect scoring, routing, message passing,
prediction, or action selection. The risk is that path history becomes hidden
global state, unreviewed bias, or untraceable authority.

A path-gated operator makes the gate explicit, traceable, and reviewable.

## Gate Forms

Path gates can be deterministic, learned, hard, soft, veto-only, or
review-oriented.

| Form | Meaning | Example use |
| --- | --- | --- |
| Deterministic gate | Rule-based gate over path shape, evidence, safety, or policy. | Block unresolved or unsafe evidence paths. |
| Learned gate | Model-estimated gate or blending weight over path context. | Blend path context with graph context for scoring or prediction. |
| Hard gate | Gate can stop advancement before prediction, commit, or side effect. | Unknown path fails closed. |
| Soft gate | Gate changes weight, confidence, or rank while leaving verification active. | Path quality affects score components. |
| Veto-only gate | Gate only blocks known bad paths; unknown paths continue to normal verification. | Outcome-backed failure contexts trigger deny. |
| Review gate | Gate routes uncertain paths to review instead of commit. | Medium-strength evidence cannot auto-commit. |

## Minimal Shape

```text
path evidence
+ gate basis
+ gate weight or gate outcome
+ operator affected by the gate
+ blocked reasons, when blocked
+ unknown-path behavior
+ trace refs
+ evaluation or ablation check, when claiming improvement
```

## Gate Outputs

A soft path gate may produce:

```text
weight
confidence adjustment
blend ratio
rank adjustment
message weight
```

A hard path gate may produce:

```text
allow
deny
defer
review
fallback
abstain
```

The outcome vocabulary can be adapted by a project, but the meaning must be
declared before the gate is used.

## Gate Basis

A gate basis can include:

- path resolution;
- source count or source diversity;
- evidence quality;
- contradiction status;
- safety status;
- policy requirements;
- outcome-backed failure or success context;
- operator confidence or uncertainty;
- learned path/context blend weight;
- unknown-path behavior.

The basis should be visible in trace. A gate that cannot explain its basis
should not be used for hard advancement control.

For hard verification or commit gates, prefer an evidence path over a loose
graph neighborhood. Neighborhood context can support review or exploration, but
a gate that blocks or advances a proposal should name the bounded path evidence
or path key it used.

## When To Use

- Path history changes the meaning of a node, state, artifact, or route.
- Evidence chains need to condition scoring or routing.
- A learned model needs to blend path context with graph context.
- A proposal should advance only when path evidence is trusted enough.
- Unknown, weak, contradictory, or unsafe paths need explicit behavior.
- A system needs to test whether path evidence improves or protects decisions.

## When Not To Use

- The computation is independent of path history.
- The gate cannot be evaluated or explained.
- A simpler operator produces the same result.
- Gate failure would silently disappear instead of producing a traceable
  decision.
- The gate would bypass verifier, commit, policy, or replay.

## Required Trace Fields

When a path gate is used, trace should preserve:

```text
path refs
gate id
gate basis
gate weight or gate outcome
blocked reasons
unknown-path behavior
operator or proposal affected
verifier basis
commit decision
```

## Validation Questions

```text
1. Is the path evidence explicit?
2. Is the gate basis visible?
3. Is unknown-path behavior declared?
4. Is this a soft influence gate, hard advancement gate, or both?
5. Can a hard gate block a high score?
6. Can the verifier still reject an allowed path?
7. Does trace preserve the gate weight, gate decision, or blocked reasons?
8. Is any improvement claim supported by evaluation or ablation?
```

## Maturity

Core Architecture pattern, with a value-over-baseline eval of the hard gate:
[labs/evals/path-gated-operators/results.md](../labs/evals/path-gated-operators/results.md).

This page does not define a mandatory operator API.
