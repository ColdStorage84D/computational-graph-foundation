# Visual Media Encoding

Visual Media Encoding is the Architecture pattern for turning image or video
evidence into traceable fields, regions, objects, tracks, events, and graph
views.

## Definition

```text
media anchor
  -> decoded pixel field
  -> regions / objects / tracks / events
  -> optional graph view
  -> proposal evidence or review surface
```

The raw media remains evidence. Derived visual objects preserve source frame,
region, timing, lens, and confidence records.

## Problem Solved

Image and video systems often erase the path from pixels to claims. CGF keeps
the chain visible so a reviewer or agent can see which frames, regions, masks,
tracks, and lens outputs support the current view.

## Minimum Record

```text
media_anchor_id
frame_refs
pixel_field_ref
region_refs
object_or_track_refs
visual_event_refs
lens_application_refs
confidence
evidence_refs
```

## When To Use

- A visual case needs multiple lenses or proposal routes.
- Regions, masks, objects, or tracks become graph evidence.
- Timing matters.
- Topology, metric placement, or granular analysis needs visual support.

## Boundary

Visual evidence does not become a final decision by itself. It can support
lenses, proposals, review, trace, and outcome comparison, but it stays below
verification and commit authority.

## Claim Boundary

CGF has a tiny local eval for record shape and evidence preservation. It does
not claim object detection, segmentation, tracking, diagnosis, or perception
performance.
