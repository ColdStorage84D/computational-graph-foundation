# Publishing CGF

This guide defines the final steps for publishing the Computational Graph
Foundation public base.

## Repository Root

CGF is designed to publish with this directory as the repository root. Hosted
repository features such as the landing README, issue templates, security
policy, and CI workflows are discovered from that root.

When CGF lives inside a larger monorepo, use one of these deliberate release
layouts:

- export the currently tracked CGF tree into a dedicated repository as a clean,
  squashed initial commit; or
- publish this directory through a subtree or history split only after auditing
  every reachable historical file and commit message; or
- keep it in the monorepo and add a host-root landing page plus host-root
  automation that explicitly points to CGF.

Do not publish an unrelated parent working tree as though it were the CGF
project. Do not upload a raw copy of a working directory because ignored caches,
runtime traces, and simulator project files may still be present locally. Export
tracked files only.

## Candidate Requirements

Before tagging a release:

1. Run every command in [PUBLIC_BASE_CHECKLIST.md](PUBLIC_BASE_CHECKLIST.md)
   from the CGF root.
2. Confirm [RELEASE_MANIFEST.md](RELEASE_MANIFEST.md) records the same test and
   link-check results produced by the candidate commit.
3. Confirm `git status --short` contains only intended release changes.
4. Confirm caches, runtime traces, crash dumps, credentials, downloaded data,
   and large generated binaries are not tracked.
5. When preserving history, confirm deleted generated artifacts, private drafts,
   and unrelated commit messages are not reachable from the public repository.
6. Review application claim boundaries, especially the medical and robot
   demonstrations.
7. Choose a version, create an annotated tag from the verified commit, and use
   the same version in the hosted release title.

References to Substrate or Architecture `v0.1` and `v0.2` describe the maturity
of those documentation layers. They do not assign a repository release version;
the published tag does that.

## Hosted Repository Setup

For a dedicated public repository:

- enable the workflow in `.github/workflows/ci.yml`;
- enable private vulnerability reporting when the host supports it;
- configure branch protection to require the CGF test workflow;
- add repository topics and a short description that match README language;
- create the release from the verified tag, using [RELEASE_NOTES.md](RELEASE_NOTES.md)
  as the starting text.

## Academic Citation

Before an archival or academic release, add `CITATION.cff` with confirmed
author names, preferred citation text, release version, and persistent
identifier. Do not invent contributor metadata merely to complete the file.

## Release Decision

A passing local checkout is a release candidate. It becomes a published
snapshot only after the verified changes are committed, tagged, and made
available from the intended public repository root.
