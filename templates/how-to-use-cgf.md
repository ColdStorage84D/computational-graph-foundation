# How To Use CGF In Your Project

Use this guide when applying CGF to a project without adopting a mandatory SDK.

## 1. Start With The Subject

Use [../substrate/templates/subject-template.md](../substrate/templates/subject-template.md)
to declare the 9 core Substrate primitives:

```text
graph
typed field
placement
state
action
constraint
evolution
readout
validation
```

If those are not clear, stay in Substrate drafting.

## 2. Check Derivatives And Extensions

Use:

- [../substrate/derivatives/README.md](../substrate/derivatives/README.md);
- [../substrate/extensions/decision-guide.md](../substrate/extensions/decision-guide.md);
- [../substrate/extensions/registry.md](../substrate/extensions/registry.md).

Add only the derivatives or extensions that prevent a real failure mode.

## 3. Decide Whether Architecture Is Needed

Use Architecture only when the project needs operation around the subject:
execution graph, proposals, verification, commit, trace, replay, memory,
review, path-aware behavior, or framework cards.

Start with:

- [../architecture/INDEX.md](../architecture/INDEX.md);
- [../architecture/frameworks/selection-guide.md](../architecture/frameworks/selection-guide.md).

## 4. Trace Claims

Use [../research/connection-map.md](../research/connection-map.md) and
[../labs/evals/README.md](../labs/evals/README.md).

If no Labs eval exists, do not describe the idea as validated. If a result says
`contract-pass`, the claim is limited to that tiny fixture and contract.

## 5. Record The Decision

Use [project-intake.md](project-intake.md) to record:

```text
starting point
selected Substrate pieces
selected Architecture patterns
selected framework cards
Labs result and claim boundary
remaining gaps before implementation
```

## 6. Build Independently

You can:

- read the docs and implement in your own style;
- copy or fork section-local examples;
- ignore patterns that do not fit;
- add project-specific code outside CGF.

CGF does not require a package, SDK, database, model framework, or deployment
style.
