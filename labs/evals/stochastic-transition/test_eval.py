import importlib.util
from pathlib import Path
import sys
import unittest


def load_eval():
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location("cgf_stochastic_transition_eval", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()


class StochasticTransitionEvalTest(unittest.TestCase):
    def kernel(self):
        return {
            "clear": {"success": 0.9, "review": 0.1},
            "uncertain": {"success": 0.3, "review": 0.6, "fail": 0.1},
        }

    def test_valid_and_invalid_kernels(self):
        ev.validate_kernel(self.kernel())
        with self.assertRaises(ValueError):
            ev.validate_kernel({"bad": {"a": 0.5, "b": 0.6}})

    def test_belief_pushforward_returns_distribution(self):
        result = ev.push_forward_belief({"clear": 0.5, "uncertain": 0.5}, self.kernel())
        self.assertAlmostEqual(sum(result.values()), 1.0)
        self.assertGreater(result["review"], 0.3)

    def test_risk_mass_is_visible(self):
        distribution = ev.predict_distribution("uncertain", self.kernel())
        self.assertAlmostEqual(ev.score_risk(distribution, {"review", "fail"}), 0.7)

    def test_sampled_future_is_not_observed(self):
        record = ev.sample_record("uncertain", ev.predict_distribution("uncertain", self.kernel()))
        self.assertEqual(record["status"], "counterfactual")

    def test_kernel_composition_checks_compatibility(self):
        decision = {
            "success": {"accept": 1.0},
            "review": {"defer": 1.0},
            "fail": {"reject": 1.0},
        }
        composed = ev.compose_kernels(self.kernel(), decision)
        self.assertGreater(composed["uncertain"]["defer"], composed["uncertain"]["accept"])
        with self.assertRaises(ValueError):
            ev.compose_kernels({"a": {"missing": 1.0}}, decision)


if __name__ == "__main__":
    unittest.main()
