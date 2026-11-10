import importlib.util
from pathlib import Path
import sys
import unittest


def load_comparison():
    name = "cgf_granular_analysis_comparison"
    path = Path(__file__).with_name("comparison.py")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


cmp = load_comparison()
SINGLE = tuple(f"single_lens_{name}" for name in cmp.LENSES)


class GranularAnalysisComparisonTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = cmp.run_comparison()

    def test_run_is_deterministic(self):
        self.assertEqual(self.report, cmp.run_comparison())

    def test_single_lens_commits_its_blind_spot(self):
        arms = self.report["independent_blind_spots"]
        for arm in SINGLE:
            self.assertAlmostEqual(arms[arm]["wrong_commit_rate"], cmp.BLIND_RATE, delta=0.02)

    def test_pairs_halve_wrong_commits_without_adding_review(self):
        arms = self.report["independent_blind_spots"]
        best_single = min(arms[arm]["wrong_commit_rate"] for arm in SINGLE)
        self.assertLess(arms["many_lenses_pairs"]["wrong_commit_rate"], 0.6 * best_single)
        self.assertLess(arms["many_lenses_pairs"]["review_rate"], 0.05)

    def test_unanimity_nearly_removes_wrong_commits_and_sends_half_to_review(self):
        arms = self.report["independent_blind_spots"]
        self.assertLess(arms["many_lenses_unanimous"]["wrong_commit_rate"], 0.02)
        self.assertGreater(arms["many_lenses_unanimous"]["review_rate"], 0.45)

    def test_more_lenses_do_not_help_when_they_share_a_blind_spot(self):
        arms = self.report["shared_blind_spot"]
        best_single = min(arms[arm]["wrong_commit_rate"] for arm in SINGLE)
        for arm in ("many_lenses_pairs", "many_lenses_unanimous"):
            self.assertGreater(arms[arm]["wrong_commit_rate"], 0.9 * best_single, arm)

    def test_label_never_reaches_a_lens(self):
        engine = cmp.build_engine(cmp.LENSES, 2)
        row = {"label": "class_a", "texture": 0.9, "shape": 0.9, "context": 0.9}
        result = engine.run("case:probe", row)
        self.assertEqual(result.trace.hidden_keys_excluded, ("label",))
        self.assertEqual(result.outcome_ref, "class_a")
        self.assertTrue(result.trace.rejected_proposal_ids)


if __name__ == "__main__":
    unittest.main()
