"""CGF Visual Media Encoding eval."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Region:
    region_id: str
    frame_ref: str
    bbox: tuple[int, int, int, int]
    source_ref: str
    confidence: float


@dataclass(frozen=True)
class Track:
    track_id: str
    region_refs: tuple[str, ...]
    source_refs: tuple[str, ...]


def validate_region(region: Region) -> None:
    x, y, width, height = region.bbox
    if width <= 0 or height <= 0 or x < 0 or y < 0:
        raise ValueError("invalid bbox")
    if not region.frame_ref or not region.source_ref:
        raise ValueError("frame and source refs are required")
    if not 0.0 <= region.confidence <= 1.0:
        raise ValueError("confidence must be bounded")


def build_track(track_id: str, regions: tuple[Region, ...]) -> Track:
    if not regions:
        raise ValueError("track requires regions")
    for region in regions:
        validate_region(region)
    return Track(
        track_id=track_id,
        region_refs=tuple(region.region_id for region in regions),
        source_refs=tuple(region.source_ref for region in regions),
    )


def graph_view_from_regions(view_id: str, regions: tuple[Region, ...]) -> dict[str, object]:
    if not view_id:
        raise ValueError("view id is required")
    for region in regions:
        validate_region(region)
    return {
        "view_id": view_id,
        "node_refs": [region.region_id for region in regions],
        "frame_refs": sorted({region.frame_ref for region in regions}),
        "evidence_refs": [region.source_ref for region in regions],
    }
