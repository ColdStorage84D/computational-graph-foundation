# Local-Voting World Model Eval

Status: `contract-pass`

This eval runs a narrow graph mechanism: local columns bind features to
locations, vote laterally, and predict the next feature. The mechanism is
adapted from the Thousand Brains proposal; the references are in the
[Architecture guide](../../../architecture/local-voting-world-model.md#references).

```text
movement + feature -> feature-at-location memory
local observation -> ambiguous object hypotheses
many columns -> lateral voting -> selected object hypothesis
selected object + action -> predicted next feature
```

The fixture is synthetic. It only checks whether a small graph can represent
the mechanism cleanly enough to run and inspect.

## CGF Mapping

| Term in the source proposal | Toy graph role |
| --- | --- |
| Layer 4 | Current feature input. |
| Layer 5 | Movement/action delta. |
| Layer 6 | Path-integrated local reference-frame position. |
| Layers 2/3 | Object hypotheses and lateral voting state. |
| Column | Local subgraph capsule with feature-location memory. |
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
python -m unittest discover -s labs/evals/local-voting-world-model -p "test_*.py"
```
