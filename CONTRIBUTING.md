# Contributing

CGF is meant to be easy to read, copy, fork, and adapt.

For the working rules used by agents and contributors, see [agent.md](agent.md).
For public-base release readiness, see
[PUBLIC_BASE_CHECKLIST.md](PUBLIC_BASE_CHECKLIST.md).
For usage questions and reproducible defects, see [SUPPORT.md](SUPPORT.md).
Report sensitive vulnerabilities through [SECURITY.md](SECURITY.md), not a
public issue.

## Contribution Rules

- Keep the public ladder consistent:

  ```text
  CGF -> Substrate -> Architecture -> Applications
  ```

- Put base computational primitives in `substrate/`.
- Put runtime organization in `architecture/`.
- Put optional Substrate extensions in `substrate/extensions/`.
- Put Architecture patterns in `architecture/`.
- Put domain-specific work in `applications/`.
- Put theory, studies, and self-contained research notes in `research/`.
- Put experiments in `labs/`.
- Put historical or deprecated material in `archive/`.
- Keep future code section-local by default:
  `substrate/examples/`, `architecture/reference/python/`, `labs/evals/`, or
  `applications/<domain>/`.

## Writing Style

- Prefer clear definitions over broad claims.
- Say what a concept does before saying what it is not. Keep claim boundaries
  in result records and claim-boundary pages, and link to them from elsewhere.
- Mark maturity honestly.
- Keep examples small enough to inspect.
- Add code only when it is tied to a stable doc contract or a clear example.
- Name a concept for what its code does. Keep a name from mathematics or
  another field only when the code implements the object that name refers to,
  and cite the source.
- Declare an eval's layer in its result record. Claim that a concept helps only
  from a value-over-baseline eval that also records where it does not.
- Avoid creating a top-level SDK or package until the project has a clear reason.

## Release Readiness

Before describing a snapshot as public-base complete, run the checks listed in
[PUBLIC_BASE_CHECKLIST.md](PUBLIC_BASE_CHECKLIST.md). Do not promote broad
claims from docs, examples, or applications unless the claim boundary is linked
to a Labs result or explicitly marked as unvalidated.

Maintainers should complete [PUBLISHING.md](PUBLISHING.md) before tagging or
creating a hosted release.
