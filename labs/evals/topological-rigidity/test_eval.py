import importlib.util
import math
from pathlib import Path
import sys
import unittest


def load_eval():
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location("cgf_topological_rigidity_eval", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()


class TopologicalRigidityEvalTest(unittest.TestCase):
    def test_unit_vectors_validate_and_invalid_rejects(self):
        ev.validate_unit_vector((1.0, 0.0))
        ev.validate_unit_vector((0.0, 0.0, 1.0))
        with self.assertRaises(ValueError):
            ev.validate_unit_vector((0.0, 0.0))

    def test_triangle_structure_separates_area_and_non_collinearity(self):
        spread = ev.triangle_structure((0.0, 0.0), (1.0, 0.0), (0.0, 1.0))
        collinear = ev.triangle_structure((0.0, 0.0), (1.0, 0.0), (2.0, 0.0))
        self.assertEqual(spread["area_squared"], 1.0)
        self.assertEqual(spread["non_collinearity"], 1.0)
        self.assertEqual(collinear["area_squared"], 0.0)
        self.assertEqual(collinear["non_collinearity"], 0.0)

    def test_retention_metrics_detect_area_and_angular_collapse(self):
        reference = ((0.0, 0.0), (1.0, 0.0), (0.0, 1.0))
        area_shrink = ((0.0, 0.0), (1.0, 0.0), (0.0, 0.5))
        collinear = ((0.0, 0.0), (1.0, 0.0), (2.0, 0.0))
        shrink_metrics = ev.retention_metrics(reference, area_shrink)
        collapse_metrics = ev.retention_metrics(reference, collinear)
        self.assertEqual(shrink_metrics["angular_deficit"], 0.0)
        self.assertGreater(shrink_metrics["area_deficit"], 0.0)
        self.assertGreater(
            collapse_metrics["retention_loss"], shrink_metrics["retention_loss"]
        )

    def test_retention_metrics_are_reference_relative_under_rescaling(self):
        reference = ((0.0, 0.0), (1.0, 0.0), (0.0, 1.0))
        observed = ((0.0, 0.0), (1.0, 0.0), (0.0, 0.5))
        scaled_reference = ((0.0, 0.0), (2.0, 0.0), (0.0, 2.0))
        scaled_observed = ((0.0, 0.0), (2.0, 0.0), (0.0, 1.0))
        base = ev.retention_metrics(reference, observed)
        scaled = ev.retention_metrics(scaled_reference, scaled_observed)
        self.assertAlmostEqual(base["area_retention_ratio"], scaled["area_retention_ratio"])
        self.assertAlmostEqual(base["retention_loss"], scaled["retention_loss"])

    def test_u1_phase_degree_preserves_orientation_and_multiple_winding(self):
        ccw = (0.0, math.pi / 2.0, math.pi, 3.0 * math.pi / 2.0)
        clockwise = tuple(reversed(ccw))
        twice = tuple(step * math.pi / 2.0 for step in range(8))
        self.assertEqual(ev.u1_phase_degree(ccw), 1)
        self.assertEqual(ev.u1_phase_degree(clockwise), -1)
        self.assertEqual(ev.u1_phase_degree(twice), 2)

    def test_closed_area_cycle_is_labeled_as_non_invariant_diagnostic(self):
        far_loop = ((10.0, 10.0), (11.0, 10.0), (10.0, 11.0), (10.0, 10.0))
        diagnostic = ev.closed_area_cycle_diagnostic(far_loop)
        self.assertEqual(diagnostic["value"], 1)
        self.assertEqual(diagnostic["estimator"], "closed_area_cycle")
        self.assertFalse(diagnostic["exact_topological_invariant"])

    def test_collapse_risk_uses_reference_relative_deficit(self):
        stable = ev.collapse_risk(1.0, 0.9, 0.1)
        collapsed = ev.collapse_risk(1.0, 0.05, 1.5)
        self.assertGreater(collapsed, stable * 100.0)

    def test_report_is_evidence_and_never_physical_authority(self):
        report = ev.topology_evidence_report(
            10.0,
            1,
            0,
            m_data_expected=2,
            m_data_observed=1,
        )
        self.assertFalse(report["authority"])
        self.assertFalse(report["validates_physical_theory"])
        self.assertEqual(report["n_data"]["mismatch"], 1)
        self.assertFalse(report["n_data"]["exact_topological_invariant"])
        self.assertEqual(report["m_data"]["mismatch"], 1)
        self.assertEqual(
            report["m_data"]["status"], "integer-degree-under-sampling-contract"
        )


if __name__ == "__main__":
    unittest.main()
