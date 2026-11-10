"""Value-over-baseline comparison for Granular Analysis.

Failure mode: one lens decides alone, so its blind spot becomes the outcome.

Every arm runs the reference `GranularAnalysisEngine` with the same thresholds.

- `single_lens_*`: one lens, one proposer per outcome.
- `many_lenses_pairs`: three lenses, one proposer per outcome for every pair of
  lenses. Two lenses that agree can commit.
- `many_lenses_unanimous`: three lenses, one proposer per outcome reading all
  three. Any disagreement lowers confidence and lands in review.

A lens looking into a blind spot reports confident support for the wrong
outcome. In the first regime each lens is blind independently. In the second
all three are blind together, where more lenses should not help.
"""

from __future__ import annotations

from itertools import combinations
import json
from pathlib import Path
import random
import sys

REFERENCE = Path(__file__).resolve().parents[3] / "architecture" / "reference" / "python"
if str(REFERENCE) not in sys.path:
    sys.path.insert(0, str(REFERENCE))

from cgf_architecture import AnalysisNode, GranularAnalysisEngine, Lens  # noqa: E402

LENSES = ("texture", "shape", "context")
CLASSES = ("class_a", "class_b")
BLIND_RATE = 0.20
SIGNAL_NOISE = 0.08
COMMIT_THRESHOLD = 0.70
REVIEW_THRESHOLD = 0.45


def build_case(rng: random.Random, *, shared_blind_spot: bool) -> dict[str, object]:
    """One input. Each lens reads support for class_a in [0, 1]."""

    truth = rng.choice(CLASSES)
    together = rng.random() < BLIND_RATE
    row: dict[str, object] = {"label": truth}
    for lens in LENSES:
        alone = rng.random() < BLIND_RATE
        blind = together if shared_blind_spot else alone
        target = CLASSES[1 - CLASSES.index(truth)] if blind else truth
        centre = 0.85 if target == "class_a" else 0.15
        row[lens] = min(1.0, max(0.0, rng.gauss(centre, SIGNAL_NOISE)))
    return row


def _lens(name: str) -> Lens:
    return Lens(name, "signal", lambda row, key=name: {"support_a": float(row[key])}, (f"e:{name}",))


def _proposer(outcome: str, lens_ids: tuple[str, ...]) -> AnalysisNode:
    def handler(outputs):
        supports = [
            output.features["support_a"] if outcome == "class_a" else 1.0 - output.features["support_a"]
            for output in outputs
        ]
        spread = max(supports) - min(supports)
        return {
            "outcome_ref": outcome,
            "score": sum(supports) / len(supports),
            # One lens cannot see disagreement, so its confidence never drops.
            "confidence": 0.95 - spread,
            "uncertainty": min(1.0, 0.05 + spread),
        }

    return AnalysisNode(f"{outcome}-from-{'+'.join(lens_ids)}", lens_ids, handler)


def build_engine(lens_ids: tuple[str, ...], group_size: int) -> GranularAnalysisEngine:
    groups = tuple(combinations(lens_ids, group_size))
    return GranularAnalysisEngine(
        lenses=tuple(_lens(name) for name in lens_ids),
        analysis_nodes=tuple(_proposer(outcome, group) for group in groups for outcome in CLASSES),
        commit_threshold=COMMIT_THRESHOLD,
        review_threshold=REVIEW_THRESHOLD,
    )


def run_regime(*, shared_blind_spot: bool, seed: int = 20260105, cases: int = 4000) -> dict[str, object]:
    rng = random.Random(seed)
    rows = [build_case(rng, shared_blind_spot=shared_blind_spot) for _ in range(cases)]
    arms = {f"single_lens_{name}": build_engine((name,), 1) for name in LENSES}
    arms["many_lenses_pairs"] = build_engine(LENSES, 2)
    arms["many_lenses_unanimous"] = build_engine(LENSES, 3)
    report = {}
    for arm, engine in arms.items():
        commits = wrong = review = 0
        for index, row in enumerate(rows):
            result = engine.run(f"case:{index}", row)
            if result.decision == "commit":
                commits += 1
                wrong += int(result.outcome_ref != row["label"])
            elif result.decision == "review":
                review += 1
        report[arm] = {
            "commit_rate": round(commits / cases, 4),
            "wrong_commit_rate": round(wrong / cases, 4),
            "review_rate": round(review / cases, 4),
            "precision": round((commits - wrong) / commits, 4) if commits else None,
        }
    return report


def run_comparison(*, seed: int = 20260105, cases: int = 4000) -> dict[str, object]:
    return {
        "seed": seed,
        "cases_per_regime": cases,
        "blind_rate": BLIND_RATE,
        "independent_blind_spots": run_regime(shared_blind_spot=False, seed=seed, cases=cases),
        "shared_blind_spot": run_regime(shared_blind_spot=True, seed=seed, cases=cases),
    }


if __name__ == "__main__":
    print(json.dumps(run_comparison(), indent=2))
