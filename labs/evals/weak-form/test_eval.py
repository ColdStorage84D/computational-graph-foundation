import importlib.util
from pathlib import Path
import sys
import unittest


def load_eval():
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location("cgf_weak_form_eval", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()


class WeakFormEvalTest(unittest.TestCase):
    def test_aggregate_residual_uses_declared_support(self):
        observed = {"a": 1.0, "b": 3.0, "c": 100.0}
        expected = {"a": 2.0, "b": 2.0, "c": 0.0}
        self.assertAlmostEqual(ev.weak_residual(observed, expected, ("a", "b")), 0.0)

    def test_missing_support_rejected(self):
        with self.assertRaises(ValueError):
            ev.weak_residual({"a": 1.0}, {"a": 1.0}, ("missing",))

    def test_local_failures_remain_visible(self):
        observed = {"a": 1.0, "b": 3.0}
        expected = {"a": 2.0, "b": 2.0}
        report = ev.weak_form_report(observed, expected, ("a", "b"), 0.5)
        self.assertTrue(report["passes_aggregate"])
        self.assertEqual(set(report["local_failures"]), {"a", "b"})

    def test_weighted_residual_changes_reported_value(self):
        observed = {"a": 1.0, "b": 3.0}
        expected = {"a": 2.0, "b": 2.0}
        residual = ev.weak_residual(observed, expected, ("a", "b"), {"a": 3.0, "b": 1.0})
        self.assertAlmostEqual(residual, -0.5)

    def test_empty_support_rejected(self):
        with self.assertRaises(ValueError):
            ev.weak_residual({}, {}, ())


if __name__ == "__main__":
    unittest.main()
