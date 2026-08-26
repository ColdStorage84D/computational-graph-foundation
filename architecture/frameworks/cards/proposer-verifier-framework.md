# Proposer-Verifier Framework

## Purpose

Use this framework when candidates should be generated freely but accepted only
after a visible validation boundary.

## Reusable Concept

Proposers create candidates. Verifiers check whether a candidate has enough
support, fit, policy clearance, confidence, or evaluation backing. Commit
accepts, rejects, reviews, defers, falls back, or abstains.

In Granular Analysis, proposers can compete across lenses, encoders,
processors, and combined evidence views. The verifier can choose one, send the
case to review, defer it, fall back, or abstain.

The useful pattern is:

```text
many proposal nodes -> verifier basis -> commit, review, defer, fallback, or abstain
```

A proposer can be a model, rule, processor, route, search routine, human draft,
or graph operation. The verifier is the boundary that decides whether the
proposal is supported enough to advance.

## Verifier Basis

A verifier should state the basis it uses:

```text
supporting evidence refs
required lens ids or route ids
score and confidence threshold
uncertainty or coverage rule
policy gate
default or fallback rule
abstain rule
review rule
```

When several proposals are close or weak, the verifier should preserve that
fact instead of pretending the highest score is final truth.

## Uses CGF Pieces

- proposal contract;
- verifier basis;
- commit contract;
- path-conditioned scoring;
- path-gated advancement;
- trace and replay;
- evaluation discipline.

## Example Applications

- model answer selection;
- finding triage;
- route selection;
- recommendation systems;
- action selection;
- report or summary drafting.

## When To Use

- High scores are not enough to trust a candidate.
- A default or abstain path is safer than unsupported promotion.
- Multiple views, processors, or routes compete.
- One outcome should preserve the full proposal set, including rejected
  alternatives.
- The system needs an audit trail for why a candidate advanced.
- A route-specific or view-specific model should be trusted only after a
  declared validation basis supports it.

## When Not To Use

- There is only one deterministic valid output.
- No candidate can be rejected, deferred, or reviewed.
- The verifier would merely repeat the proposer score.

## Boundary

The verifier does not make an application truth claim. It states whether a
candidate can advance under the declared basis.

Commit remains a separate authority boundary. A verifier can recommend,
approve for review, defer, block, or abstain, but it should not silently mutate
accepted state.

## Implementation Posture

Implementation should preserve route table, verifier basis, abstain/review
behavior, and evaluation results when any performance claim is made.
