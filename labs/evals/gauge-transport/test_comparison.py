import importlib.util
from pathlib import Path
import sys
import unittest


def load_comparison():
    name = "cgf_gauge_transport_comparison"
    path = Path(__file__).with_name("comparison.py")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


cmp = load_comparison()


class GaugeTransportComparisonTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = cmp.run_comparison()

    def test_run_is_deterministic(self):
        self.assertEqual(self.report, cmp.run_comparison())

    def test_raw_comparison_drowns_in_false_alarms_when_frames_differ(self):
        raw = self.report["frames_differ"]["raw"]
        self.assertLess(raw["precision"], 0.30)
        self.assertGreater(raw["false_positive_edges_per_ring"], 10.0)

    def test_transport_removes_the_false_alarms(self):
        transported = self.report["frames_differ"]["transported"]
        self.assertEqual(transported["false_positive_edges_per_ring"], 0.0)
        self.assertGreater(transported["recall"], 0.99)

    def test_transport_adds_nothing_when_frames_already_agree(self):
        aligned = self.report["frames_aligned"]
        self.assertEqual(aligned["raw"], aligned["transported"])

    def test_wrong_maps_degrade_transport(self):
        for regime in ("independent_map_errors", "consistent_frame_errors"):
            transported = self.report[regime]["transported"]
            self.assertLess(transported["precision"], 0.5, regime)
            self.assertGreater(transported["false_positive_edges_per_ring"], 5.0, regime)

    def test_holonomy_sees_inconsistent_maps_but_not_consistently_wrong_frames(self):
        self.assertLess(self.report["frames_differ"]["mean_loop_holonomy"], 1e-9)
        self.assertGreater(self.report["independent_map_errors"]["mean_loop_holonomy"], 0.5)
        self.assertLess(self.report["consistent_frame_errors"]["mean_loop_holonomy"], 1e-9)


if __name__ == "__main__":
    unittest.main()
