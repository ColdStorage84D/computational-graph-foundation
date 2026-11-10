import importlib.util
from pathlib import Path
import sys
import unittest


def load_comparison():
    name = "cgf_hyperbolic_placement_comparison"
    path = Path(__file__).with_name("comparison.py")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


cmp = load_comparison()


class HyperbolicPlacementComparisonTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = cmp.run_comparison()

    def test_tree_distances_are_computed_from_the_graph(self):
        adjacency, _ = cmp.complete_tree(2, 3)
        distances = cmp.graph_distances(adjacency)
        self.assertEqual(len(adjacency), 15)
        self.assertEqual(distances[("r", "r.0.0.0")], 3)
        self.assertEqual(distances[("r.0.0.0", "r.1.1.1")], 6)
        self.assertEqual(distances[("r.0.0.0", "r.0.0.1")], 2)

    def test_hyperbolic_placement_keeps_tree_distortion_bounded(self):
        for name in ("binary_tree_depth_4", "binary_tree_depth_6", "ternary_tree_depth_4"):
            self.assertLess(self.report[name]["hyperbolic"]["worst_case_distortion"], 2.0, name)

    def test_euclidean_distortion_grows_with_depth_and_hyperbolic_does_not(self):
        shallow = self.report["binary_tree_depth_4"]
        deep = self.report["binary_tree_depth_6"]
        self.assertGreater(
            deep["euclidean"]["worst_case_distortion"], 5.0 * shallow["euclidean"]["worst_case_distortion"]
        )
        self.assertAlmostEqual(
            deep["hyperbolic"]["worst_case_distortion"],
            shallow["hyperbolic"]["worst_case_distortion"],
            delta=0.05,
        )
        self.assertGreater(
            deep["euclidean"]["worst_case_distortion"], 50.0 * deep["hyperbolic"]["worst_case_distortion"]
        )

    def test_gain_needs_radial_growth_matched_to_branching(self):
        mismatched = self.report["binary_tree_depth_6_mismatched_radius"]
        self.assertGreater(mismatched["radius_per_level_x0.5"], 5.0 * mismatched["radius_per_level_x1.0"])
        self.assertGreater(mismatched["radius_per_level_x2.0"], 2.0 * mismatched["radius_per_level_x1.0"])

    def test_flat_plane_wins_on_a_grid(self):
        grid = self.report["grid_6x6"]
        flat = grid["euclidean"]["worst_case_distortion"]
        self.assertAlmostEqual(flat, 2 ** 0.5, places=2)
        for result in grid["hyperbolic"].values():
            self.assertGreater(result["worst_case_distortion"], flat)
        self.assertGreater(grid["hyperbolic"]["disk_radius_0.9"]["worst_case_distortion"], 3.0 * flat)


if __name__ == "__main__":
    unittest.main()
