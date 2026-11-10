import importlib.util
import math
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


def shifted(base, displacement):
    return {key: base[key] + displacement[key] for key in base}


class FisherMetricTest(unittest.TestCase):
    def test_fisher_rao_is_a_metric_on_the_fixture(self):
        points = (
            {"a": 0.7, "b": 0.2, "c": 0.1},
            {"a": 0.4, "b": 0.3, "c": 0.3},
            {"a": 0.05, "b": 0.05, "c": 0.9},
        )
        for p in points:
            self.assertAlmostEqual(ev.fisher_rao_distance(p, p), 0.0, places=6)
            for q in points:
                self.assertAlmostEqual(ev.fisher_rao_distance(p, q), ev.fisher_rao_distance(q, p))
                for r in points:
                    self.assertLessEqual(
                        ev.fisher_rao_distance(p, r),
                        ev.fisher_rao_distance(p, q) + ev.fisher_rao_distance(q, r) + 1e-12,
                    )

    def test_divergence_and_distance_agree_with_the_metric_locally(self):
        base = {"a": 0.6, "b": 0.3, "c": 0.1}
        displacement = {"a": 0.002, "b": -0.0005, "c": -0.0015}
        nearby = shifted(base, displacement)
        quadratic = ev.fisher_quadratic_form(base, displacement)
        # KL is half the squared Fisher length to second order ...
        self.assertAlmostEqual(ev.kl_divergence(nearby, base) / (0.5 * quadratic), 1.0, places=2)
        # ... and the geodesic distance is the Fisher length to first order.
        self.assertAlmostEqual(ev.fisher_rao_distance(nearby, base) / math.sqrt(quadratic), 1.0, places=2)

    def test_same_absolute_shift_counts_more_where_probability_is_scarce(self):
        base = {"common": 0.50, "other": 0.49, "rare": 0.01}
        rare_shift = shifted(base, {"common": 0.0, "other": -0.05, "rare": 0.05})
        common_shift = shifted(base, {"common": 0.05, "other": -0.05, "rare": 0.0})
        # A flat distance cannot tell these two changes apart.
        self.assertAlmostEqual(
            ev.belief_distance(rare_shift, base), ev.belief_distance(common_shift, base)
        )
        # The Fisher geometry can: a rare state becoming six times likelier is the bigger change.
        self.assertGreater(
            ev.fisher_rao_distance(rare_shift, base), 2.0 * ev.fisher_rao_distance(common_shift, base)
        )

    def test_tangent_displacement_must_stay_on_the_simplex(self):
        base = {"a": 0.5, "b": 0.5}
        with self.assertRaises(ValueError):
            ev.fisher_quadratic_form(base, {"a": 0.1, "b": 0.1})
        with self.assertRaises(ValueError):
            ev.fisher_rao_distance(base, {"a": 0.5, "c": 0.5})


if __name__ == "__main__":
    unittest.main()
