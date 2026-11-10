"""Value-over-baseline comparison for path-gated and path-conditioned decisions.

Failure mode: a proposer always cites support, and the highest score commits
even when the cited path does not exist.

Baseline: commit the highest score. Variants: gate on a resolvable evidence
path, then optionally discount long chains.

The generator states its assumptions as parameters. The comparison is only as
good as those assumptions, so a second regime sets them to "paths carry no
information" and reports what the gate costs there.
"""

from __future__ import annotations

from dataclasses import dataclass
import importlib.util
import json
from pathlib import Path
import random
import sys


def _load_eval():
    name = "cgf_path_gated_operators_eval"
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
    """Generator assumptions. Each one is a claim about the world, not a result."""

    name: str
    support_if_correct: float  # P(a genuine chain exists | candidate is correct)
    support_if_wrong: float  # P(a genuine chain exists | candidate is wrong)
    short_chain_if_correct: float  # P(chain is one hop | correct and supported)
    short_chain_if_wrong: float  # P(chain is one hop | wrong and supported)
    score_gap: float = 0.05  # mean score advantage of the correct candidate
    score_noise: float = 0.15
    candidates_per_case: int = 4


INFORMATIVE = Regime(
    "paths_informative",
    support_if_correct=0.85,
    support_if_wrong=0.15,
    short_chain_if_correct=0.75,
    short_chain_if_wrong=0.25,
)
UNINFORMATIVE = Regime(
    "paths_uninformative",
    support_if_correct=0.50,
    support_if_wrong=0.50,
    short_chain_if_correct=0.50,
    short_chain_if_wrong=0.50,
)


def build_case(rng: random.Random, regime: Regime, case_index: int):
    """One decision: several candidate claims, exactly one of them correct."""

    node_types: dict[str, str] = {}
    edges: dict[str, tuple[str, str]] = {}
    candidates = []
    correct_index = rng.randrange(regime.candidates_per_case)
    for index in range(regime.candidates_per_case):
        is_correct = index == correct_index
        prefix = f"c{case_index}:{index}"
        claim = f"{prefix}:claim"
        node_types[claim] = "claim"
        supported = rng.random() < (
            regime.support_if_correct if is_correct else regime.support_if_wrong
        )
        short = rng.random() < (
            regime.short_chain_if_correct if is_correct else regime.short_chain_if_wrong
        )
        hops = 1 if short else rng.choice((2, 3))
        chain = [f"{prefix}:evidence"] + [f"{prefix}:mid{step}" for step in range(hops - 1)] + [claim]
        edge_ids = tuple(f"{prefix}:edge{step}" for step in range(hops))
        node_types[chain[0]] = "evidence"
        for middle in chain[1:-1]:
            node_types[middle] = "intermediate"
        if supported:
            for edge_id, source, target in zip(edge_ids, chain, chain[1:]):
                edges[edge_id] = (source, target)
        else:
            # The proposer still cites the chain. One link of it was never recorded.
            missing = rng.randrange(hops)
            for step, (edge_id, source, target) in enumerate(zip(edge_ids, chain, chain[1:])):
                if step != missing:
                    edges[edge_id] = (source, target)
        mean = 0.5 + (regime.score_gap if is_correct else 0.0)
        score = min(1.0, max(0.0, rng.gauss(mean, regime.score_noise)))
        candidates.append(
            ev.Candidate(f"{prefix}", claim, score, ev.EvidencePath(tuple(chain), edge_ids))
        )
    graph = ev.EvidenceGraph(node_types, edges)
    return graph, tuple(candidates), candidates[correct_index].candidate_id


def run_regime(regime: Regime, *, seed: int = 20260101, cases: int = 4000, hop_discount: float = 0.8):
    rng = random.Random(seed)
    arms = {
        "score_only": {"commit": 0, "correct": 0},
        "path_gated": {"commit": 0, "correct": 0},
        "path_gated_conditioned": {"commit": 0, "correct": 0},
    }
    for case_index in range(cases):
        graph, candidates, correct_id = build_case(rng, regime, case_index)
        decisions = {
            "score_only": ev.decide_score_only(candidates),
            "path_gated": ev.decide_path_gated(graph, candidates),
            "path_gated_conditioned": ev.decide_path_gated(
                graph, candidates, hop_discount=hop_discount
            ),
        }
        for arm, decision in decisions.items():
            if decision.action == "commit":
                arms[arm]["commit"] += 1
                arms[arm]["correct"] += int(decision.selected_id == correct_id)
    report = {}
    for arm, counts in arms.items():
        wrong = counts["commit"] - counts["correct"]
        report[arm] = {
            "commit_rate": round(counts["commit"] / cases, 4),
            "wrong_commit_rate": round(wrong / cases, 4),
            "correct_commit_rate": round(counts["correct"] / cases, 4),
            "abstain_rate": round(1.0 - counts["commit"] / cases, 4),
            "precision": round(counts["correct"] / counts["commit"], 4) if counts["commit"] else None,
        }
    return report


def run_comparison(*, seed: int = 20260101, cases: int = 4000) -> dict[str, object]:
    return {
        "seed": seed,
        "cases_per_regime": cases,
        "candidates_per_case": INFORMATIVE.candidates_per_case,
        INFORMATIVE.name: run_regime(INFORMATIVE, seed=seed, cases=cases),
        UNINFORMATIVE.name: run_regime(UNINFORMATIVE, seed=seed, cases=cases),
    }


if __name__ == "__main__":
    print(json.dumps(run_comparison(), indent=2))
