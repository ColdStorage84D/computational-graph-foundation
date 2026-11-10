import importlib.util
from pathlib import Path
import sys
import unittest


def load_eval():
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location("cgf_sheaf_consistency_eval", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()


class SheafConsistencyEvalTest(unittest.TestCase):
    def test_restriction_happens_before_compare(self):
        view = ev.LocalView("feature", "molecule", {"activity": "active", "irrelevant": 7})
        restriction = ev.RestrictionMap("to_activity", "molecule", "activity_basis", ("activity",))
        restricted = ev.restrict_view(view, restriction)
        self.assertEqual(restricted.support, "activity_basis")
        self.assertEqual(restricted.payload, {"activity": "active"})

    def test_agreeing_views_glue(self):
        left = ev.LocalView("a", "overlap", {"activity": "active"})
        right = ev.LocalView("b", "overlap", {"activity": "active", "chain": "present"})
        comparison = ev.compare_overlap(left, right)
        glued = ev.glue_views(left, right, comparison)
        self.assertEqual(comparison["residual"], 1)
        # Missing keys are conflicts; restrict to a shared key for clean glue.
        left = ev.LocalView("a", "overlap", {"activity": "active"})
        right = ev.LocalView("b", "overlap", {"activity": "active"})
        comparison = ev.compare_overlap(left, right)
        glued = ev.glue_views(left, right, comparison)
        self.assertEqual(glued["kind"], "gluing_candidate")
        self.assertEqual(glued["merged_payload"], {"activity": "active"})

    def test_conflicting_views_raise_obstruction(self):
        left = ev.LocalView("feature", "activity_basis", {"activity": "active"})
        right = ev.LocalView("chain", "activity_basis", {"activity": "inactive"})
        comparison = ev.compare_overlap(left, right)
        glued = ev.glue_views(left, right, comparison)
        self.assertEqual(comparison["residual"], 1)
        self.assertEqual(glued["kind"], "obstruction")
        self.assertEqual(glued["merged_payload"], {})

    def test_counterfactual_status_survives(self):
        left = ev.LocalView("simulated", "overlap", {"risk": "high"}, "counterfactual")
        right = ev.LocalView("real", "overlap", {"risk": "high"}, "observed")
        glued = ev.glue_views(left, right, ev.compare_overlap(left, right))
        self.assertEqual(glued["status"], "counterfactual")

    def test_unshared_support_rejects_compare(self):
        with self.assertRaises(ValueError):
            ev.compare_overlap(
                ev.LocalView("a", "node", {"x": 1}),
                ev.LocalView("b", "edge", {"x": 1}),
            )


if __name__ == "__main__":
    unittest.main()
