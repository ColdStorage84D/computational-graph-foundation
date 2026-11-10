import importlib.util
from pathlib import Path
import sys
import unittest


def load_comparison():
    name = "cgf_path_gated_operators_comparison"
    path = Path(__file__).with_name("comparison.py")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


cmp = load_comparison()


class PathGatedComparisonTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = cmp.run_comparison()

    def test_run_is_deterministic(self):
        self.assertEqual(self.report, cmp.run_comparison())

    def test_gate_cuts_wrong_commits_when_paths_carry_information(self):
        arms = self.report["paths_informative"]
        self.assertGreater(arms["score_only"]["wrong_commit_rate"], 0.60)
        self.assertLess(arms["path_gated"]["wrong_commit_rate"], 0.25)
        self.assertGreater(arms["path_gated"]["precision"], 2.0 * arms["score_only"]["precision"])

    def test_gate_pays_for_that_with_abstentions(self):
        arms = self.report["paths_informative"]
        self.assertEqual(arms["score_only"]["abstain_rate"], 0.0)
        self.assertGreater(arms["path_gated"]["abstain_rate"], 0.05)

    def test_conditioning_adds_a_smaller_gain_on_top_of_the_gate(self):
        arms = self.report["paths_informative"]
        self.assertLess(
            arms["path_gated_conditioned"]["wrong_commit_rate"], arms["path_gated"]["wrong_commit_rate"]
        )
        self.assertEqual(
            arms["path_gated_conditioned"]["abstain_rate"], arms["path_gated"]["abstain_rate"]
        )

    def test_gate_does_not_help_when_paths_carry_no_information(self):
        arms = self.report["paths_uninformative"]
        self.assertLess(arms["path_gated"]["precision"], arms["score_only"]["precision"])
        self.assertGreater(arms["path_gated"]["abstain_rate"], 0.0)

    def test_result_holds_across_seeds(self):
        for seed in (1, 2, 3):
            arms = cmp.run_regime(cmp.INFORMATIVE, seed=seed, cases=2000)
            self.assertLess(
                arms["path_gated"]["wrong_commit_rate"], 0.5 * arms["score_only"]["wrong_commit_rate"]
            )


if __name__ == "__main__":
    unittest.main()
