import importlib.util
from pathlib import Path
import sys
import unittest


def load_eval():
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location("cgf_information_geometry_eval", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()


class InformationGeometryEvalTest(unittest.TestCase):
    def test_kl_detects_mode_preserving_shift(self):
        prior = {"normal": 0.6, "degraded": 0.3, "fault": 0.1}
        shifted = {"normal": 0.51, "degraded": 0.25, "fault": 0.24}
        self.assertEqual(max(prior, key=prior.get), max(shifted, key=shifted.get))
        self.assertAlmostEqual(ev.kl_divergence(prior, prior), 0.0)
        self.assertGreater(ev.kl_divergence(shifted, prior), 0.05)

    def test_entropy_separates_sharp_and_broad(self):
        sharp = {"a": 0.98, "b": 0.01, "c": 0.01}
        broad = {"a": 0.34, "b": 0.33, "c": 0.33}
        self.assertGreater(ev.entropy(broad), ev.entropy(sharp))

    def test_surprise_and_calibration_error_are_visible(self):
        belief = {"normal": 0.8, "fault": 0.2}
        self.assertGreater(ev.surprise(belief, "fault"), ev.surprise(belief, "normal"))
        self.assertGreater(ev.calibration_error({"normal": 0.99, "fault": 0.01}, "fault"), 0.9)

    def test_belief_distance_grows_with_shift(self):
        base = {"a": 0.7, "b": 0.2, "c": 0.1}
        small = {"a": 0.65, "b": 0.25, "c": 0.1}
        large = {"a": 0.4, "b": 0.3, "c": 0.3}
        self.assertGreater(ev.belief_distance(large, base), ev.belief_distance(small, base))

    def test_information_gain_is_zero_for_unchanged_belief(self):
        prior = {"normal": 0.7, "degraded": 0.2, "fault": 0.1}
        posterior = {"normal": 0.45, "degraded": 0.35, "fault": 0.2}
        self.assertAlmostEqual(ev.information_gain(prior, prior), 0.0)
        self.assertGreater(ev.information_gain(prior, posterior), 0.05)

    def test_tail_risk_mass_remains_visible(self):
        belief = {"normal": 0.7, "degraded": 0.2, "fault": 0.08, "critical": 0.02}
        self.assertAlmostEqual(ev.tail_risk_mass(belief, {"fault", "critical"}), 0.10)
        with self.assertRaises(ValueError):
            ev.tail_risk_mass(belief, {"unknown"})


if __name__ == "__main__":
    unittest.main()
