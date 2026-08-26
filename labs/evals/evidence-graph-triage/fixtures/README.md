# Evidence Graph Triage Fixtures

The fixture for this eval is defined in code, in `fixture_candidates()` inside
[../eval.py](../eval.py), rather than in a data file. It is four synthetic
candidates with neutral source labels, small enough to read in one screen.

```text
finding:corroborated        source_a + source_b, raw 0.60
finding:single-source-high  source_a,            raw 0.95
finding:multi-record        source_c x2,         raw 0.62
finding:unsupported         no records,          raw 0.80
```

Two properties of the fixture are deliberate:

- `finding:single-source-high` carries the highest raw score in the set and is
  still deferred, because one source supports it;
- `finding:multi-record` is scored just above `finding:corroborated`, so a single
  recorded outcome is enough to swap them and make the reordering observable.

There is no domain data here. The labels `source_a`, `source_b`, and `source_c`
are intentionally meaningless, because the contract under test is the reusable
pattern rather than any application of it.
