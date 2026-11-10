# Evaluation Methodology

CGF Labs evals are small, local contract checks. They are not broad domain
benchmarks unless a document explicitly says so and the data/license/review
requirements have been met.

## Evaluation Layers

| Layer | Purpose | Claim allowed |
| --- | --- | --- |
| Isolated eval | Tests one concept on tiny fixtures. | `contract-pass` for that local contract only. |
| Integration eval | Tests a small concept mix. | `contract-pass` for the mix and fixture only. |
| Value-over-baseline eval | Compares a concept against a simpler baseline on a named failure mode. | Local value improvement only when the baseline, metric, and fixture are declared. |
| Recipe-grounded eval | Rewrites a real application failure mode as a self-contained CGF fixture. | Narrow recipe result only; no general domain claim. |

Every result record declares its layer on an `Eval layer:` line. The layer is
checked: a record that declares value-over-baseline or recipe-grounded must
ship `comparison.py` and `test_comparison.py`, name its baseline, and include a
`Where It Does Not Help` section. See [README.md](README.md).

A value-over-baseline comparison should:

- generate its data from a seed, so the numbers can be reproduced;
- state the generator's assumptions as named parameters;
- include at least one regime where those assumptions do not hold;
- assert its pass thresholds in tests, including the regime where the concept
  does not help.

## Promotion Gate

A concept can move from research language into public CGF guidance when it has:

```text
definition
parent layer
failure mode
minimum record shape
small example
maturity label
claim boundary
```

A concept can move from guidance into a stronger claim only when it also has:

```text
runnable CGF-local eval
reviewed result record
explicit baseline when value is claimed
failure behavior
no authority-boundary bypass
```

## Result Labels

Use the labels in [README.md](README.md):

```text
pending-cgf-eval
cgf-eval-present
contract-pass
contract-fail
mixed
```

Do not use stronger wording such as validated, proven, production-ready, or
benchmark-beating unless a specific reviewed benchmark document supports that
exact claim.

## Recipe-Grounded Rules

Recipe-grounded evals must be rewritten as CGF-local fixtures. They must not
copy private datasets, generated artifacts, caches, old logs, or package
scaffolding.

Each recipe-grounded eval should state:

- failure mode;
- baseline;
- variant under test;
- metric;
- pass threshold;
- claim boundary;
- data/license status.

## Authority Rule

No score, view, filter posterior, geometry, transport, cell view, belief metric,
flow balance, intervention label, or learned operator can promote itself into a
final decision or durable update. Eval fixtures should preserve the relevant
authority boundary when that boundary is part of the concept.
