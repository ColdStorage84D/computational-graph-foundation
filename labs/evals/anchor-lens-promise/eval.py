"""CGF Anchor / Lens / Promise eval."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json


@dataclass(frozen=True)
class LensApplication:
    anchor_id: str
    input_version: str
    lens_id: str
    lens_version: str
    lens_params: dict[str, object]


@dataclass(frozen=True)
class Promise:
    application_id: str
    status: str
    output_ref: str | None = None
    evidence_refs: tuple[str, ...] = ()


def stable_lens_application_id(application: LensApplication) -> str:
    payload = {
        "anchor_id": application.anchor_id,
        "input_version": application.input_version,
        "lens_id": application.lens_id,
        "lens_version": application.lens_version,
        "lens_params": application.lens_params,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "lensapp:" + hashlib.sha256(encoded).hexdigest()[:16]


def validate_promise(promise: Promise) -> None:
    allowed = {"pending", "fulfilled", "failed", "frozen"}
    if promise.status not in allowed:
        raise ValueError("invalid promise status")
    if promise.status in {"fulfilled", "frozen"} and not promise.output_ref:
        raise ValueError("fulfilled or frozen promise requires output_ref")
    if promise.status == "pending" and promise.output_ref:
        raise ValueError("pending promise cannot have output_ref")


def fulfill_promise(promise: Promise, output_ref: str, evidence_refs: tuple[str, ...]) -> Promise:
    validate_promise(promise)
    if promise.status != "pending":
        raise ValueError("only pending promises can be fulfilled")
    if not evidence_refs:
        raise ValueError("evidence refs are required")
    return Promise(promise.application_id, "fulfilled", output_ref, evidence_refs)
