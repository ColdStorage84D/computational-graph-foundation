import importlib.util
from pathlib import Path
import sys
import unittest


def load_eval():
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location("cgf_surrogate_promotion_eval", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()


class SurrogatePromotionEvalTest(unittest.TestCase):
    def test_learned_surrogate_beats_baseline_on_heldout(self):
        train = ((0.0, 2.0), (1.0, 5.0), (2.0, 8.0))
        heldout = ((3.0, 11.0), (4.0, 14.0))
        model = ev.fit_affine(train)
        baseline = ev.fit_constant(train)
        self.assertLess(ev.mse_affine(model, heldout), ev.mse_constant(baseline, heldout))

    def test_validated_surrogate_promotes(self):
        decision = ev.promotion_gate(0.0, 10.0, 0.0, 0.0, True)
        self.assertEqual(decision, "promote_candidate")

    def test_wrong_residual_holds(self):
        decision = ev.promotion_gate(0.0, 10.0, 2.0, 0.0, True)
        self.assertEqual(decision, "hold: residual too high")

    def test_uncertainty_and_policy_block(self):
        self.assertEqual(ev.promotion_gate(0.0, 10.0, 0.0, 0.9, True), "hold: uncertainty too high")
        self.assertEqual(ev.promotion_gate(0.0, 10.0, 0.0, 0.0, False), "reject")

    def test_residual_compares_expected_law(self):
        model = ev.fit_affine(((0.0, 2.0), (1.0, 5.0), (2.0, 8.0)))
        self.assertLess(ev.residual(model, (3.0, 2.0)), 1e-9)


if __name__ == "__main__":
    unittest.main()
