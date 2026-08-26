# Architecture Reference Python

This folder contains a small, stdlib-only reference implementation for the CGF
Architecture contracts.

It is optional and copyable. It is not a required SDK, package scaffold, or
lock-in surface.

## What It Covers

- event log and replay trace;
- graph and path views;
- generic evidence-to-hypergraph encoding;
- proposals, gates, and commit;
- Granular Analysis over multiple lenses and proposal nodes;
- eligibility and outcome/value memory;
- spine-routed bot graph surfaces;
- static topology relations.

## Run

From the repository root:

```powershell
python -m unittest discover -s architecture/reference/python/tests -p "test_*.py"
```
