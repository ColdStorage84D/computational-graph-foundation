# Granular Analysis Fixtures

The fixture is synthetic and intentionally small.

It represents a histology-like analysis shape:

```text
one sample
-> texture lens
-> morphology lens
-> context lens
-> multiple proposal nodes
-> verifier / commit
-> traceable outcome
```

No clinical data, patient data, or diagnostic label is included.

The comparison generates seeded two-outcome cases with three lenses whose
blind spots are either independent or shared.
