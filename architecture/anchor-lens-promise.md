# Anchor / Lens / Promise

Anchor / Lens / Promise is the Architecture pattern for turning external or
upstream material into replayable graph views without hiding where the view came
from.

## Definition

```text
anchor -> lens application -> promised or fulfilled view -> traceable graph view
```

- Anchor: stable identity for a source object, record, file, stream window,
  case, sample, task, or upstream view.
- Lens: a declared transformation that reads an anchor or view and produces a
  typed output.
- Promise: a record that a lens output is expected, pending, fulfilled, failed,
  or frozen for replay.

## Problem Solved

Without this pattern, views can appear as if they were raw truth. CGF needs the
view to preserve input identity, lens identity, lens version, parameters, input
version, and fulfillment status.

## Minimum Record

```text
anchor_id
anchor_kind
input_version
lens_id
lens_version
lens_params
lens_application_id
status
output_ref
evidence_refs
```

## When To Use

- External data becomes a graph-shaped view.
- A view must be replayed or compared across lens versions.
- A pending external process will fulfill a result later.
- Multiple lenses compete over one input.

## Boundary

A lens output is evidence or a view. It is not authority by itself. Final
decisions still require the normal proposal, verification, commit, trace, and
outcome path.

## Claim Boundary

CGF has a tiny local eval for stable lens identity and promise status. It does
not claim a production data-ingestion system.
