# Human Review Framework

## Purpose

Use this framework when model, processor, or rule output must remain proposal
state until a qualified reviewer or policy accepts, edits, rejects, defers, or
requests more evidence.

## Reusable Concept

Human review is an Architecture boundary. It separates source evidence,
processor output, candidate findings, draft text, reviewer judgment, final
records, and later labels.

Review is especially important in multimodal outcome stacks because several
views and processors may disagree. The review record should preserve the
proposal set, not only the accepted text or selected candidate.

## Review States

Common review states:

```text
pending
accepted
accepted-with-edit
rejected
deferred
needs-more-evidence
unsupported
not-reviewed
```

These states are review records. They are not source evidence and they are not
training labels until a later derivation rule says so.

## Uses CGF Pieces

- proposal / verifier / commit;
- review gates;
- evidence paths;
- trace contract;
- outcome contract;
- graph runtime memory;
- later label derivation boundary.

## Example Applications

- medical image analysis review;
- security triage;
- compliance review;
- editorial review;
- quality assurance;
- legal or audit workflows.

## When To Use

- A model output is not allowed to become final state by itself.
- Review status affects what can be shown, drafted, exported, or learned.
- Later labels are derived from review outcomes, not live inputs.
- Unsupported questions or unsupported summaries must be refused.
- Several candidate proposals must be reconciled without hiding rejected
  alternatives.

## When Not To Use

- No human or policy review boundary exists.
- Outputs are fully deterministic and self-validating.
- Review records would be used to rewrite source evidence.

## Boundary

Review modifies review state. It does not mutate source evidence. Later labels
or training data require explicit derivation from accepted outcomes.

## Implementation Posture

This framework is especially useful in high-stakes domains, but it does not
claim domain safety by itself. Safety claims require domain-specific evaluation
and governance.
