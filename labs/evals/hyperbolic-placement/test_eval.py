import importlib.util
from pathlib import Path
import sys
import unittest


def load_eval():
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location("cgf_hyperbolic_placement_eval", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()


class HyperbolicPlacementEvalTest(unittest.TestCase):
    def test_valid_and_invalid_placements(self):
        ev.validate_placement((0.2, 0.3))
        with self.assertRaises(ValueError):
            ev.validate_placement((1.0, 0.0))
        projected = ev.project_to_ball((2.0, 0.0))
        ev.validate_placement(projected)

    def test_equal_euclidean_distance_separates_hyperbolically(self):
        query = (0.8, 0.0)
        ancestor = (0.4, 0.0)
        distractor = (0.8, 0.4)
        self.assertAlmostEqual(ev.euclidean_distance(query, ancestor), ev.euclidean_distance(query, distractor))
        self.assertLess(ev.poincare_distance(query, ancestor), ev.poincare_distance(query, distractor))

    def test_recall_ranks_same_branch_ancestor_first(self):
        query = (0.8, 0.0)
        ranked = ev.rank_recall(query, {"ancestor": (0.4, 0.0), "distractor": (0.8, 0.4)})
        self.assertEqual(ranked[0], "ancestor")

    def test_clean_descent_beats_backtracking_path(self):
        clean = ((0.0, 0.0), (0.4, 0.0), (0.8, 0.0))
        zigzag = ((0.0, 0.0), (0.8, 0.0), (0.4, 0.0), (0.8, 0.0))
        self.assertGreater(ev.path_score(clean), ev.path_score(zigzag))


if __name__ == "__main__":
    unittest.main()
