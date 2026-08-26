# Path-Aware Verifier Flow

This example shows how path-conditioned and path-gated operation can work
together without replacing proposal, verification, commit, trace, or outcome.

It is a prose Architecture example, not a schema, SDK, or implementation.

## Situation

A system receives a candidate claim or action. The candidate is supported by an
evidence path through records, views, graph nodes, or prior decisions.

The system must decide whether to commit, review, defer, reject, or fall back.

## Flow

```text
event
-> graph/path view
-> evidence path
-> path-conditioned score or threshold
-> path gate
-> verifier
-> commit / review / defer / fallback
-> trace
-> outcome
```

## Event

An event records the new candidate or observation.

Minimum event information:

```text
event id
event type
source ref
time or order
subject ref
```

## Graph / Path View

Architecture builds a runtime view over the declared subject. The view exposes
the candidate path instead of treating supporting context as hidden state.

Example path forms:

```text
claim -> graph node -> record -> source view -> source artifact
task -> tool -> result -> proposed action
query -> memory anchor -> prior event -> value context
```

## Path-Conditioned Score Or Threshold

The path context changes a bounded computation.

Examples:

- a stronger path increases review priority;
- repeated safe outcome context raises a verifier threshold;
- weak or single-source support lowers confidence;
- a regime-specific path selects a different scorer.

This influence is recorded as a score component, threshold choice, or route
choice. It does not authorize commit by itself.

## Path Gate

The path gate controls path influence or advancement.

A soft gate can change a blend weight, confidence adjustment, rank adjustment,
or message weight while normal verification remains active.

A hard gate decides whether the path can support advancement.

Hard gate outcomes:

```text
allow
deny
defer
review
fallback
abstain
```

Example gate checks:

- every path step resolves;
- required evidence is present;
- source diversity is sufficient for the action level;
- no contradiction blocks advancement;
- unknown path behavior is explicit;
- unsafe support fails closed.

## Verifier

The verifier checks the candidate, conditioned effect, gate result, policy, and
constraints.

The verifier can still reject or defer an allowed path. A path gate is not a
replacement for verification.

## Commit

Commit decides the accepted action or deliberate non-action.

Possible decisions:

```text
commit
review
defer
reject
fallback
abort
```

Only a committed accepted path can create eligibility for later outcome
resolution.

## Trace

Trace preserves:

```text
event refs
view refs
evidence path refs
path context
conditioned score or threshold
gate decision
gate weight, when used
blocked reasons
verifier basis
commit decision
outcome refs, when observed
```

Trace must make it possible to understand whether path context influenced a
score, whether a gate blocked advancement, and why commit chose action or
non-action.

## Validation Questions

```text
1. Is the evidence path explicit?
2. Is the path-conditioned effect surface visible?
3. Does the path gate state unknown-path behavior?
4. Can hard gate failure block a high score?
5. Can trace reconstruct path context, gate basis, and commit decision?
6. Is any improvement claim tied to an evaluation or ablation?
```
