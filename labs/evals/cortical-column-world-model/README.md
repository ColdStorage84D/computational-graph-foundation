# Cortical-Column World Model Eval

Status: `contract-pass`

This eval recreates a narrow graph mechanism inspired by the cortical-column /
Thousand Brains concept:

```text
movement + feature -> feature-at-location memory
local observation -> ambiguous object hypotheses
many columns -> lateral voting -> selected object hypothesis
selected object + action -> predicted next feature
```

The fixture is synthetic. It is not a biological simulation, not an AGI system,
and not evidence that CGF has solved world models. It only checks whether a
small graph can represent the concept cleanly enough to run and inspect.

## CGF Mapping

| Concept term | Toy graph role |
| --- | --- |
| Layer 4 | Current feature input. |
| Layer 5 | Movement/action delta. |
| Layer 6 | Path-integrated local reference-frame position. |
| Layers 2/3 | Object hypotheses and lateral voting state. |
| Cortical column | Local subgraph capsule with feature-location memory. |
| Voting | Architecture readout over column hypotheses. |
| Prediction | One-step readout from selected object model and action. |

## Contract

The eval passes when:

- path integration updates a column location;
- a sensed feature is bound to that location;
- one local observation remains ambiguous;
- two columns vote for the only shared object hypothesis;
- the selected object predicts the next sensed feature after movement;
- the result carries an explicit claim boundary.

## Connections

- Architecture: [graph-brain-and-spine.md](../../../architecture/graph-brain-and-spine.md).
- Architecture: [subgraph-capsules.md](../../../architecture/subgraph-capsules.md).
- Architecture: [path-conditioned-and-path-gated.md](../../../architecture/path-conditioned-and-path-gated.md).
- Result record: [results.md](results.md).

## Run

```powershell
python -m unittest discover -s labs/evals/cortical-column-world-model -p "test_*.py"
```
