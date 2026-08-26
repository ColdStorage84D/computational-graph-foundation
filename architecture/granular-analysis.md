# Granular Analysis

Granular Analysis is the CGF Architecture concept for turning one input into
many analysis branches and one traceable outcome.

```text
one input -> many lenses / encoders -> many proposal nodes
  -> one or more outcome candidates -> verifier / commit -> traceable outcome
```

The sales phrase is:

```text
many lenses, many proposers, one traceable outcome
```

## Definition

Granular Analysis is multi-lens, multi-proposer, outcome-oriented graph
analysis.

It makes a system inspect an input through several lenses or encoders, send
those lens outputs to different proposal nodes, compare the resulting proposals,
and preserve the full proposal set behind the outcome.

## Why It Matters

Most model pipelines hide the path from input to answer. They often look like:

```text
input -> model -> answer
```

Granular Analysis keeps the operating graph visible:

```text
input
-> texture lens
-> morphology lens
-> context lens
-> proposal from texture
-> proposal from morphology
-> proposal from combined evidence
-> verifier
-> commit, review, defer, fallback, or abstain
-> outcome trace
```

The outcome can say not only what was selected, but also which lens branches
supported it, which proposals competed, which proposals were rejected, and why.

## Operating Shape

| Stage | Role | Must preserve |
| --- | --- | --- |
| Input record | The source item, event, case, sample, state, or artifact. | Input id, source refs, declared non-feature labels. |
| Lens or encoder | Produces a bounded view over the input. | Lens id, feature kind, evidence refs, hidden-label exclusion. |
| Analysis node | Consumes one or more lens outputs. | Node id, input lens ids, required evidence, failure mode. |
| Proposal | Candidate answer, finding, route, action, or review item. | Proposal id, proposer id, supporting lens ids, score, confidence, uncertainty, evidence refs. |
| Verifier or gate | Checks support, policy, validation basis, or route fit. | Verifier basis, blocked reasons, abstain/review/defer behavior. |
| Commit | Selects accepted outcome candidate or accepted non-action. | Selected proposal, rejected proposals, decision reason. |
| Trace | Reconstructs the full analysis graph. | Input, lens outputs, proposals considered, verifier basis, commit, outcome. |

## What It Builds On

Granular Analysis is not a replacement for existing Architecture concepts. It
composes them:

- [lenses-adapters-operators.md](lenses-adapters-operators.md): lenses and
  typed views.
- [frameworks/cards/feature-view-framework.md](frameworks/cards/feature-view-framework.md):
  feature views as analysis branches.
- [frameworks/cards/proposer-verifier-framework.md](frameworks/cards/proposer-verifier-framework.md):
  proposals and validated advancement.
- [frameworks/cards/processor-routing-framework.md](frameworks/cards/processor-routing-framework.md):
  route fit for specialized processors.
- [path-conditioned-operators.md](path-conditioned-operators.md): path context
  changes scores, thresholds, routes, or messages.
- [path-gated-operators.md](path-gated-operators.md): gates control influence
  or advancement.
- [event-log-trace-replay.md](event-log-trace-replay.md): rejected proposals
  remain reviewable.

## Example Uses

- Histology-like analysis with texture, morphology, and context lenses.
- Medical image analysis review with image, record, measurement, and prior lenses.
- Robotics perception with sensor, geometry, safety, and task-context lenses.
- Security findings with syntax, control-flow, data-flow, and policy lenses.
- Trading signals with market, portfolio, risk, and regime lenses.
- Predictive maintenance with aggregate, trend, missingness, and recent-window
  lenses.
- Document analysis with layout, citation, semantic, and source-quality lenses.

## Rules

- One input may create many lens outputs.
- One lens output may feed many proposal nodes.
- One proposal node may consume many lens outputs.
- One outcome may consider many proposals.
- Rejected proposals remain traceable counterfactual alternatives.
- Training-only labels, ground truth, or future outcomes must not enter lens
  outputs.
- Commit, review, defer, fallback, and abstain remain explicit outcomes.

## When Not To Use

Do not use Granular Analysis when:

- one deterministic view is enough;
- there are no competing proposals;
- rejected alternatives do not need to be preserved;
- the system cannot name lens ids, proposer ids, or verifier basis;
- adding analysis branches would hide unsupported assumptions.

## Validation Questions

```text
1. What input is being analyzed?
2. Which lenses or encoders produce analysis branches?
3. Which proposal nodes consume each lens output?
4. Can one lens output feed more than one proposal node?
5. Can one proposal consume more than one lens output?
6. What verifier or gate controls advancement?
7. What happens when every proposal is weak or blocked?
8. Does trace preserve selected and rejected proposals?
9. Are training-only labels excluded from lens outputs?
10. What claim is supported by local eval, if any?
```

## Boundary

Granular Analysis is an Architecture concept and reusable framework pattern. It
is not a Substrate primitive, medical claim, model architecture, package API, or
required SDK.
