"""Value-over-baseline comparison for evidence-set status.

Failure modes, both named on the framework card:

- a high score from one source is treated as confirmation;
- repeated records from one source are counted as corroboration.

Arms:

- `score_ranked`: commit the highest-scoring findings, at the same volume the
  corroboration arm commits, so the comparison is at equal review budget;
- `record_count`: commit any finding with two or more records;
- `corroborated`: commit only what `decide_status` confirms, which requires a
  declared pair of distinct source categories.

The generator's assumptions are parameters. A second regime makes two sources
copies of each other, where the card says corroboration should stop helping.
"""

from __future__ import annotations

from dataclasses import dataclass
import importlib.util
import json
from pathlib import Path
import random
import sys


def _load_eval():
    name = "cgf_evidence_graph_triage_eval"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name("eval.py"))
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ev = _load_eval()


@dataclass(frozen=True)
class Regime:
    name: str
    prevalence: float = 0.25  # P(finding is real)
    fire_if_real: float = 0.70  # P(a source records a real finding)
    fire_if_false: float = 0.15  # P(a source records a false finding)
    copy_rate: float = 0.0  # P(source_b simply repeats source_a)
    max_burst: int = 3  # a source that fires emits 1..max_burst records
    score_gap: float = 0.10
    score_noise: float = 0.18
    burst_bonus: float = 0.06  # score added per extra record


INDEPENDENT = Regime("independent_sources")
CORRELATED = Regime("correlated_sources", copy_rate=0.95)


def build_findings(rng: random.Random, regime: Regime, count: int):
    findings = []
    for index in range(count):
        real = rng.random() < regime.prevalence
        fire = regime.fire_if_real if real else regime.fire_if_false
        fired = {category: rng.random() < fire for category in ev.SOURCE_CATEGORIES}
        if rng.random() < regime.copy_rate:
            fired["source_b"] = fired["source_a"]
        records = []
        for category in ev.SOURCE_CATEGORIES:
            if fired[category]:
                for burst in range(rng.randint(1, regime.max_burst)):
                    records.append(ev.Record(f"record:{index}:{category}:{burst}", category))
        mean = 0.5 + (regime.score_gap if real else 0.0)
        # The score rewards volume, which is how repeated records inflate it.
        score = rng.gauss(mean, regime.score_noise) + regime.burst_bonus * max(0, len(records) - 1)
        candidate = ev.Candidate(f"finding:{index}", "rule", min(1.0, max(0.0, score)), tuple(records))
        findings.append((candidate, real))
    return findings


def _summarise(committed: list[bool], total_real: int) -> dict[str, float | int | None]:
    commits = len(committed)
    correct = sum(committed)
    return {
        "commits": commits,
        "wrong_commits": commits - correct,
        "precision": round(correct / commits, 4) if commits else None,
        "recall": round(correct / total_real, 4) if total_real else None,
    }


def run_regime(regime: Regime, *, seed: int = 20260102, count: int = 5000) -> dict[str, object]:
    rng = random.Random(seed)
    findings = build_findings(rng, regime, count)
    total_real = sum(real for _, real in findings)

    corroborated = [
        real for candidate, real in findings if ev.decide_status(candidate.records).action == "commit"
    ]
    record_count = [real for candidate, real in findings if len(candidate.records) >= 2]
    by_score = sorted(findings, key=lambda item: (-item[0].raw_score, item[0].finding_id))
    score_ranked = [real for _, real in by_score[: len(corroborated)]]

    return {
        "findings": count,
        "real_findings": total_real,
        "score_ranked": _summarise(score_ranked, total_real),
        "record_count": _summarise(record_count, total_real),
        "corroborated": _summarise(corroborated, total_real),
    }


def run_comparison(*, seed: int = 20260102, count: int = 5000) -> dict[str, object]:
    return {
        "seed": seed,
        INDEPENDENT.name: run_regime(INDEPENDENT, seed=seed, count=count),
        CORRELATED.name: run_regime(CORRELATED, seed=seed, count=count),
    }


if __name__ == "__main__":
    print(json.dumps(run_comparison(), indent=2))
