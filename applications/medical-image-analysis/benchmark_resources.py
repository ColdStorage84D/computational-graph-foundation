"""Optional local benchmark resource support for the medical image app."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

BENCHMARK_ENV_VAR = "CGF_MEDICAL_BENCHMARK_DIR"
RECORDS_FILE = "records.jsonl"


class BenchmarkResourceError(ValueError):
    """Raised when an optional local benchmark folder is malformed."""


def configured_benchmark_dir() -> Path | None:
    value = os.environ.get(BENCHMARK_ENV_VAR, "").strip()
    return Path(value).expanduser().resolve() if value else None


def benchmark_available() -> bool:
    root = configured_benchmark_dir()
    return bool(root and (root / RECORDS_FILE).is_file() and (root / "images").is_dir())


def _safe_relative_path(root: Path, relative_path: str) -> Path:
    if not relative_path or Path(relative_path).is_absolute():
        raise BenchmarkResourceError("image path must be relative to the benchmark folder")
    resolved = (root / relative_path).resolve()
    if root not in resolved.parents and resolved != root:
        raise BenchmarkResourceError("image path escapes the benchmark folder")
    return resolved


def load_benchmark_records(limit: int | None = None) -> list[dict[str, Any]]:
    root = configured_benchmark_dir()
    if root is None:
        return []
    if not root.is_dir():
        raise BenchmarkResourceError(f"benchmark folder does not exist: {root}")
    records_path = root / RECORDS_FILE
    if not records_path.is_file():
        raise BenchmarkResourceError(f"missing {RECORDS_FILE}")

    records: list[dict[str, Any]] = []
    with records_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if limit is not None and len(records) >= limit:
                break
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise BenchmarkResourceError(f"invalid JSON on line {line_number}") from exc
            for key in ("case_id", "image", "question"):
                if key not in row:
                    raise BenchmarkResourceError(f"line {line_number} missing {key}")
            image_path = _safe_relative_path(root, str(row["image"]))
            if not image_path.is_file():
                raise BenchmarkResourceError(f"line {line_number} image not found: {row['image']}")
            row = dict(row)
            row["image_path"] = str(image_path)
            records.append(row)
    return records


def _bounded(value: float, low: float = 0.05, high: float = 0.95) -> float:
    return min(high, max(low, value))


def benchmark_record_to_review_record(row: dict[str, Any]) -> dict[str, Any]:
    """Create smoke-test review features from local benchmark metadata.

    This is deliberately not a benchmark scorer. It gives the CGF graph path
    bounded numeric evidence so local records can exercise the same review
    pipeline without treating `answer` as live evidence.
    """

    image_path = Path(str(row["image_path"]))
    image_size = image_path.stat().st_size
    question = str(row.get("question", ""))
    question_signal = _bounded(len(question) / 160)
    size_signal = _bounded((image_size % 1000) / 1000)
    return {
        "case_id": str(row["case_id"]),
        "image": str(row["image"]),
        "question": question,
        "texture_contrast": _bounded(0.25 + size_signal * 0.55),
        "region_quality": _bounded(0.35 + question_signal * 0.45),
        "cell_density": _bounded(0.30 + ((image_size // 7) % 100) / 200),
        "boundary_clarity": _bounded(0.30 + ((image_size // 13) % 100) / 200),
        "source_quality": 0.70,
        "collection_flag": "local-benchmark-smoke",
        "answer": row.get("answer"),
    }


def export_benchmark_graph_cases(limit: int = 3) -> list[dict[str, Any]]:
    from synthetic_review import build_case_from_record

    cases: list[dict[str, Any]] = []
    for row in load_benchmark_records(limit=limit):
        _, graph = build_case_from_record(benchmark_record_to_review_record(row))
        cases.append(
            {
                "case_id": graph.case_id,
                "nodes": graph.nodes,
                "edges": [
                    {"source": source, "target": target, "relation": relation}
                    for source, target, relation in graph.edges
                ],
                "later_record_keys": sorted(graph.later_records),
            }
        )
    return cases


def run_benchmark_smoke(limit: int = 3) -> dict[str, Any]:
    from synthetic_review import run_review_for_record

    runs: list[dict[str, Any]] = []
    for row in load_benchmark_records(limit=limit):
        review_record = benchmark_record_to_review_record(row)
        _, _, result = run_review_for_record(review_record)
        runs.append(
            {
                "case_id": review_record["case_id"],
                "decision": result.decision,
                "proposal_count": len(result.trace.proposals),
                "rejected_count": len(result.trace.rejected_proposal_ids),
                "hidden_keys_excluded": list(result.trace.hidden_keys_excluded),
            }
        )
    return {
        "mode": "optional-local-benchmark",
        "record_count": len(runs),
        "claim": "local smoke test only",
        "runs": runs,
    }


def benchmark_smoke_summary(limit: int = 3) -> dict[str, Any]:
    records = load_benchmark_records(limit=limit)
    return {
        "mode": "optional-local-benchmark",
        "available": bool(records),
        "record_count": len(records),
        "env_var": BENCHMARK_ENV_VAR,
        "live_fields": ["case_id", "image", "question"],
        "evaluation_only_fields": ["answer", "label", "ground_truth"],
    }
