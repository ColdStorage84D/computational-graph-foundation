import importlib.util
from pathlib import Path
import sys
import unittest


def load_comparison():
    name = "cgf_bayesian_filtering_comparison"
    path = Path(__file__).with_name("comparison.py")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


cmp = load_comparison()


class BayesianFilteringComparisonTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = cmp.run_comparison()

    def test_run_is_deterministic(self):
        self.assertEqual(self.report, cmp.run_comparison())

    def test_filter_beats_both_baselines_when_the_model_matches(self):
        matched = self.report["matched_model"]
        self.assertLess(matched["rmse_filter"], 0.5 * matched["rmse_raw_measurement"])
        self.assertLess(matched["rmse_filter"], 0.5 * matched["rmse_moving_average"])

    def test_raw_measurement_error_equals_the_declared_noise(self):
        matched = self.report["matched_model"]
        self.assertAlmostEqual(matched["rmse_raw_measurement"], cmp.MEASUREMENT_NOISE ** 0.5, delta=0.05)

    def test_filter_loses_badly_when_the_model_is_wrong(self):
        wrong = self.report["unmodelled_maneuver"]
        self.assertGreater(wrong["rmse_filter"], 5.0 * wrong["rmse_raw_measurement"])

    def test_innovation_exposes_the_wrong_model(self):
        matched = self.report["matched_model"]["mean_normalized_innovation"]
        wrong = self.report["unmodelled_maneuver"]["mean_normalized_innovation"]
        self.assertLess(matched, 1.0)
        self.assertGreater(wrong, 5.0 * matched)

    def test_result_holds_across_seeds(self):
        for seed in (1, 2, 3):
            matched = cmp.run_regime(maneuver=False, seed=seed, tracks=40)
            self.assertLess(matched["rmse_filter"], 0.5 * matched["rmse_raw_measurement"])


if __name__ == "__main__":
    unittest.main()
