"""Thresholds for the Evidence Graph Triage value-over-baseline comparison."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest


def load_comparison():
    name = "cgf_evidence_graph_triage_comparison"
    path = Path(__file__).with_name("comparison.py")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


cmp = load_comparison()


class EvidenceTriageComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = cmp.run_comparison()

    def test_run_is_deterministic(self) -> None:
        self.assertEqual(self.report, cmp.run_comparison())

    def test_arms_are_compared_at_equal_commit_volume(self) -> None:
        for regime in ("independent_sources", "correlated_sources"):
            arms = self.report[regime]
            self.assertEqual(arms["score_ranked"]["commits"], arms["corroborated"]["commits"])

    def test_corroboration_halves_wrong_commits_against_score_ranking(self) -> None:
        arms = self.report["independent_sources"]
        self.assertLess(
            arms["corroborated"]["wrong_commits"], 0.5 * arms["score_ranked"]["wrong_commits"]
        )
        self.assertGreater(arms["corroborated"]["precision"], 0.80)
        self.assertLess(arms["score_ranked"]["precision"], 0.70)

    def test_counting_records_is_worse_than_counting_sources(self) -> None:
        arms = self.report["independent_sources"]
        self.assertLess(arms["record_count"]["precision"], arms["score_ranked"]["precision"])
        self.assertGreater(
            arms["record_count"]["wrong_commits"], 5 * arms["corroborated"]["wrong_commits"]
        )

    def test_corroboration_gives_up_recall(self) -> None:
        arms = self.report["independent_sources"]
        self.assertLess(arms["corroborated"]["recall"], arms["record_count"]["recall"])
        self.assertLess(arms["corroborated"]["recall"], 0.70)

    def test_correlated_sources_erode_the_advantage(self) -> None:
        independent = self.report["independent_sources"]
        correlated = self.report["correlated_sources"]
        gain_independent = (
            independent["corroborated"]["precision"] - independent["score_ranked"]["precision"]
        )
        gain_correlated = (
            correlated["corroborated"]["precision"] - correlated["score_ranked"]["precision"]
        )
        self.assertGreater(gain_independent, 0.15)
        self.assertLess(gain_correlated, 0.5 * gain_independent)
        self.assertLess(correlated["corroborated"]["precision"], 0.65)

    def test_result_holds_across_seeds(self) -> None:
        for seed in (1, 2, 3):
            arms = cmp.run_regime(cmp.INDEPENDENT, seed=seed, count=3000)
            self.assertLess(
                arms["corroborated"]["wrong_commits"], 0.6 * arms["score_ranked"]["wrong_commits"]
            )


if __name__ == "__main__":
    unittest.main()
