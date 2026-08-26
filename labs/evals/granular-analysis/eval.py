"""CGF Granular Analysis eval."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any


CGF_ROOT = Path(__file__).resolve().parents[3]
REFERENCE = CGF_ROOT / "architecture" / "reference" / "python"
if str(REFERENCE) not in sys.path:
    sys.path.insert(0, str(REFERENCE))

from cgf_architecture import AnalysisNode, GranularAnalysisEngine, Lens  # noqa: E402


def synthetic_histology_like_sample() -> dict[str, Any]:
    return {
        "sample_id": "sample:synthetic:1",
        "texture_contrast": 0.86,
        "cell_density": 0.78,
        "region_quality": 0.92,
        "stain_family": "synthetic-a",
        "label": "training-only-hidden",
    }


def build_engine() -> GranularAnalysisEngine:
    return GranularAnalysisEngine(
        lenses=(
            Lens(
                "texture",
                "invariant",
                lambda row: {
                    "texture_signal": float(row["texture_contrast"]),
                    "quality": float(row["region_quality"]),
                },
                ("e:texture",),
            ),
            Lens(
                "morphology",
                "shape",
                lambda row: {
                    "morphology_signal": float(row["cell_density"]),
                    "quality": float(row["region_quality"]),
                },
                ("e:morphology",),
            ),
            Lens(
                "context",
                "metadata",
                lambda row: {
                    "quality": float(row["region_quality"]),
                    "stain_family_seen": 1.0 if row["stain_family"] else 0.0,
                },
                ("e:context",),
            ),
        ),
        analysis_nodes=(
            AnalysisNode(
                "texture-proposer",
                ("texture",),
                lambda outputs: {
                    "outcome_ref": "candidate:texture-supported",
                    "score": outputs[0].features["texture_signal"],
                    "confidence": 0.74,
                    "uncertainty": 0.20,
                },
            ),
            AnalysisNode(
                "morphology-proposer",
                ("morphology",),
                lambda outputs: {
                    "outcome_ref": "candidate:morphology-supported",
                    "score": outputs[0].features["morphology_signal"],
                    "confidence": 0.73,
                    "uncertainty": 0.22,
                },
            ),
            AnalysisNode(
                "texture-context-proposer",
                ("texture", "context"),
                lambda outputs: {
                    "outcome_ref": "candidate:texture-context-supported",
                    "score": (
                        outputs[0].features["texture_signal"]
                        + outputs[1].features["quality"]
                    )
                    / 2.0,
                    "confidence": 0.81,
                    "uncertainty": 0.12,
                },
            ),
            AnalysisNode(
                "combined-proposer",
                ("texture", "morphology", "context"),
                lambda outputs: {
                    "outcome_ref": "candidate:combined-supported",
                    "score": min(
                        1.0,
                        (
                            outputs[0].features["texture_signal"]
                            + outputs[1].features["morphology_signal"]
                            + outputs[2].features["quality"]
                        )
                        / 3.0
                        + 0.08,
                    ),
                    "confidence": 0.90,
                    "uncertainty": 0.08,
                },
            ),
        ),
        commit_threshold=0.70,
        review_threshold=0.45,
    )


def run_fixture():
    sample = synthetic_histology_like_sample()
    return build_engine().run(str(sample["sample_id"]), sample)
