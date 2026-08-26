"""CGF Signal Review eval."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any


CGF_ROOT = Path(__file__).resolve().parents[3]
REFERENCE = CGF_ROOT / "architecture" / "reference" / "python"
if str(REFERENCE) not in sys.path:
    sys.path.insert(0, str(REFERENCE))

from cgf_architecture import AnalysisNode, GranularAnalysisEngine, Lens  # noqa: E402


HIDDEN_KEYS = frozenset(
    {
        "label",
        "future_outcome",
        "actual_failure",
        "profit_loss",
        "maintenance_result",
    }
)


def synthetic_signal_packet(
    *,
    signal_id: str = "signal:synthetic:1",
    raw_signal: float = 0.82,
    trend_score: float = 0.76,
    volatility: float = 0.24,
    source_quality: float = 0.86,
    regime_known: bool = True,
    stale: bool = False,
) -> dict[str, Any]:
    return {
        "signal_id": signal_id,
        "raw_signal": raw_signal,
        "trend_score": trend_score,
        "volatility": volatility,
        "source_quality": source_quality,
        "regime_known": regime_known,
        "stale": stale,
        "future_outcome": "training-only-hidden",
        "profit_loss": "not-live-input",
        "maintenance_result": "not-live-input",
    }


def build_engine() -> GranularAnalysisEngine:
    return GranularAnalysisEngine(
        lenses=(
            Lens(
                "level-view",
                "raw",
                lambda row: {
                    "level_signal": float(row["raw_signal"]),
                    "source_quality": float(row["source_quality"]),
                },
                ("signal:level",),
            ),
            Lens(
                "trend-view",
                "aggregate",
                lambda row: {
                    "trend_signal": float(row["trend_score"]),
                    "volatility": float(row["volatility"]),
                },
                ("signal:trend",),
            ),
            Lens(
                "regime-view",
                "context",
                lambda row: {
                    "regime_known": 1.0 if row["regime_known"] else 0.0,
                    "stale": 1.0 if row["stale"] else 0.0,
                    "source_quality": float(row["source_quality"]),
                },
                ("signal:regime",),
            ),
        ),
        analysis_nodes=(
            AnalysisNode(
                "level-processor",
                ("level-view",),
                lambda outputs: {
                    "outcome_ref": "candidate:level-review",
                    "score": outputs[0].features["level_signal"],
                    "confidence": outputs[0].features["source_quality"],
                    "uncertainty": 0.22,
                    "metadata": {"route": "level-route"},
                },
            ),
            AnalysisNode(
                "trend-processor",
                ("trend-view",),
                lambda outputs: {
                    "outcome_ref": "candidate:trend-review",
                    "score": outputs[0].features["trend_signal"],
                    "confidence": max(0.0, 1.0 - outputs[0].features["volatility"]),
                    "uncertainty": outputs[0].features["volatility"],
                    "metadata": {"route": "trend-route"},
                },
            ),
            AnalysisNode(
                "regime-processor",
                ("level-view", "trend-view", "regime-view"),
                lambda outputs: {
                    "outcome_ref": "candidate:regime-supported-review",
                    "score": (
                        (
                            outputs[0].features["level_signal"]
                            + outputs[1].features["trend_signal"]
                            + outputs[2].features["regime_known"]
                        )
                        / 3.0
                    )
                    * outputs[2].features["source_quality"],
                    "confidence": min(
                        outputs[0].features["source_quality"],
                        outputs[2].features["source_quality"],
                    ),
                    "uncertainty": 0.18 + outputs[2].features["stale"] * 0.30,
                    "metadata": {"route": "regime-route"},
                },
            ),
            AnalysisNode(
                "fallback-processor",
                ("regime-view",),
                lambda outputs: {
                    "outcome_ref": "candidate:fallback-review",
                    "score": 0.95
                    if outputs[0].features["stale"] or outputs[0].features["source_quality"] < 0.50
                    else 0.35,
                    "confidence": 0.78
                    if outputs[0].features["stale"] or outputs[0].features["source_quality"] < 0.50
                    else 0.40,
                    "uncertainty": 0.20,
                    "metadata": {"route": "fallback-route"},
                },
            ),
        ),
        commit_threshold=0.90,
        review_threshold=0.50,
        training_only_keys=HIDDEN_KEYS,
    )


def run_fixture(packet: dict[str, Any] | None = None):
    sample = packet or synthetic_signal_packet()
    return build_engine().run(str(sample["signal_id"]), sample)


if __name__ == "__main__":
    result = run_fixture()
    print(result.decision)
    print(result.outcome_ref)
