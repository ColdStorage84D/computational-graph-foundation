# Path-Conditioned Operators

Path-conditioned operators use path context as an explicit input to computation.

They answer:

```text
How should this operator behave differently because of the path that produced,
supports, or surrounds this state?
```

## Definition

A path-conditioned operator is an Architecture operator whose score, threshold,
ranking, route, message passing, readout, or projection changes based on
declared path context.

The path context must be visible. It cannot be hidden process memory or an
unrecorded side channel.

Path-conditioned does not require a gate. If the path context is simply an
input feature, context key, score component, or threshold selector, the operator
is path-conditioned even when no gate weight or allow/deny decision exists.

## Typical Uses

| Use | Path-conditioned effect |
| --- | --- |
| Ranking | Increase or decrease priority based on evidence strength or path quality. |
| Verifier threshold | Use different thresholds for different observed path contexts. |
| Routing | Choose a specialist, tool, or review route based on the active path. |
| Scoring | Add path strength, diversity, risk, or uncertainty as score components. |
| Message passing | Use path context as a message input or context feature. |
| Readout adjustment | Produce a different readout when the path indicates a regime or support class. |

If a learned gate blends path context with graph context, that is both
path-conditioned and softly path-gated. Use
[path-gated-operators.md](path-gated-operators.md) to declare the gate basis
and trace expectations.

## Rule

Path conditioning may influence computation, but it does not create authority by
itself.

If a path-conditioned result can lead to action, it must still pass the normal
Architecture chain:

```text
proposal -> verification -> commit -> trace -> outcome
```

## Minimum Declaration

Declare:

```text
path context
affected operator
effect surface
evidence refs
uncertainty or confidence
failure mode
evaluation check
trace fields
```

## Path Context

Path context can include:

- path id or path key;
- ordered evidence steps;
- path strength or quality;
- path score or path prior;
- source count or diversity;
- recent decision context;
- outcome-backed context;
- phase, route, or workflow position;
- uncertainty, contradiction, or blocked-reason signals.

The context should be stable enough to replay or reconstruct from durable
records.

## Effect Surface

The effect surface is the exact place where path context changes computation.

Examples:

- rank score;
- verifier threshold;
- route selection;
- proposal priority;
- operator blending weight;
- message aggregation weight;
- readout label or confidence;
- fallback choice.

Avoid vague statements such as "uses path history" without naming the effect
surface.

## When To Use

Use path-conditioned operators when:

- the path changes the meaning of a local fact, state, or proposal;
- evidence chains should affect ranking or thresholding;
- a route should depend on how the current state was reached;
- outcome-backed path context can improve future selection;
- a model or rule needs path features but does not own commit authority;
- the effect can be traced and evaluated.

## When Not To Use

Do not use path-conditioned operators when:

- the computation is independent of path context;
- path context cannot be reconstructed;
- the effect surface is unclear;
- the path signal would bypass verification or commit;
- a hard allow/deny/review/fallback decision is required; use a path gate
  instead or in combination;
- no evaluation or ablation can check whether the path signal helps.

## Validation Questions

```text
1. Is the path context explicit and replayable?
2. Is the affected operator named?
3. Is the effect surface bounded?
4. Can verification or policy still block the result?
5. Does trace preserve the path context and resulting effect?
6. Is there an evaluation plan before claiming improvement?
```

## Boundary

Path-conditioned operators are Architecture concepts. They operate around a
declared Substrate subject but do not redefine Substrate primitives.
