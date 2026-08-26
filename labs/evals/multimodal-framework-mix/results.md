# Multimodal Framework Mix Results

Status: `contract-pass`

## Reviewed Command

```powershell
python -m unittest discover -s labs/evals/multimodal-framework-mix -p "test_*.py"
```

## Result

```text
Ran 7 tests
OK
```

## Claim Boundary

This result supports only the CGF-local Multimodal Outcome Stack contract on a
tiny synthetic fixture:

- evidence refs remain handles;
- raw source payloads are not copied into graph feature paths;
- training-only labels are excluded from lens outputs;
- feature views keep raw, invariant, and aligned views separate;
- processor routing can reject invalid invariance fit;
- proposals preserve route and view basis;
- review outcome preserves rejected alternatives;
- trace carries the evidence refs behind the outcome.

## Not Supported

This result does not support any domain-performance, clinical, safety, model
quality, production, or broad generalization claim.
