# Multimodal Framework Mix Eval

This eval tests the CGF-local Multimodal Outcome Stack contract:

```text
external evidence -> bounded records -> typed graph -> feature views
  -> processor routes -> proposals -> review / commit -> trace
```

The fixture is synthetic and domain-neutral. It does not use clinical data and
does not make health, safety, model-performance, or production claims.

## Owning Docs

- Architecture: [multimodal-outcome-stack.md](../../../architecture/multimodal-outcome-stack.md).
- Example: [multimodal-review-flow.md](../../../architecture/examples/multimodal-review-flow.md).
- Framework cards:
  [evidence-record-framework.md](../../../architecture/frameworks/cards/evidence-record-framework.md),
  [typed-multimodal-graph-framework.md](../../../architecture/frameworks/cards/typed-multimodal-graph-framework.md),
  [feature-view-framework.md](../../../architecture/frameworks/cards/feature-view-framework.md),
  [processor-routing-framework.md](../../../architecture/frameworks/cards/processor-routing-framework.md),
  [proposer-verifier-framework.md](../../../architecture/frameworks/cards/proposer-verifier-framework.md),
  [human-review-framework.md](../../../architecture/frameworks/cards/human-review-framework.md).

## Run

```powershell
python -m unittest discover -s labs/evals/multimodal-framework-mix -p "test_*.py"
```

## Claim Boundary

Passing this eval supports only `contract-pass` for the tiny CGF-local fixture:

- evidence refs remain handles;
- bounded records do not copy raw source payloads;
- training-only labels do not enter feature paths;
- feature views keep raw and invariant views separate;
- processor routing rejects invalid invariance fit;
- proposals preserve route and view basis;
- review or commit leaves a trace.

It does not validate any real domain, model, dataset, workflow, or safety
claim.
