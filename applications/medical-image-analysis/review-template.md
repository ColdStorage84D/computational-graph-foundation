# Medical Image Analysis Review Template

Copy this template when drafting a medical image analysis CGF application
example.

This template is not a medical record format. It is a CGF review-architecture
declaration.

## Case

```text
case id:
application domain:
review purpose:
review authority:
claim boundary:
```

## Source Evidence

```text
evidence refs:
source type:
source version / timestamp:
decoder or adapter:
coverage:
warnings:
raw payload copied into graph? no
```

## Bounded Records

```text
record id:
record type:
evidence ref:
bounded fields:
missing fields:
warnings:
```

## Typed Multimodal Graph

```text
node types:
edge types:
feature-bearing nodes:
non-feature nodes:
training-only labels:
later-derived labels:
```

## Lenses And Views

```text
lens id:
view kind: raw | invariant | aligned | domain-specific | aggregate
input records:
output fields:
evidence refs:
failure mode:
```

## Processor Routes

```text
processor id:
task:
allowed evidence:
required view kind:
invalid invariances:
route state:
fallback:
```

## Proposals

```text
proposal id:
proposer id:
input lens ids:
route id:
candidate outcome:
score:
confidence:
uncertainty:
supporting evidence refs:
```

## Review Gate

```text
gate id:
basis:
allowed decisions:
selected proposal:
rejected proposals:
blocked reasons:
unknown / missing evidence behavior:
```

## Outcome

```text
decision: commit | review | defer | fallback | abstain | deny
outcome ref:
review state:
explanation refs:
claim boundary:
```

## Trace

```text
trace id:
case id:
evidence refs:
record ids:
lens outputs:
route states:
proposals considered:
selected proposal:
rejected proposals:
review state:
excluded training-only fields:
```

## Checks

```text
[ ] Source evidence stayed external.
[ ] Decoded records stayed bounded.
[ ] Training labels and later outcomes did not enter feature paths.
[ ] Views and route states were explicit.
[ ] Processor output stayed proposal state.
[ ] Review state did not mutate source evidence.
[ ] Selected and rejected proposals remained traceable.
[ ] No medical, clinical, or safety claim was made without domain validation.
```
