import importlib.util
from pathlib import Path
import sys
import unittest


def load_eval():
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location("cgf_basis_mode_representation_eval", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()


class BasisModeRepresentationEvalTest(unittest.TestCase):
    def test_mode_labels_are_explicit(self):
        graph = ev.build_fourier_mode_graph(2)
        node = graph["nodes"][ev.mode_id((1, "cos"))]
        self.assertEqual(node["basis_family"], "fourier")
        self.assertEqual(node["mode_label"], (1, "cos"))
        self.assertEqual(node["placement"], "mode")

    def test_coefficients_live_on_mode_nodes(self):
        graph = ev.build_fourier_mode_graph(1)
        placed = ev.place_coefficients(graph, {ev.mode_id((1, "sin")): 0.5})
        self.assertEqual(placed[ev.mode_id((1, "sin"))]["placement"], "mode")
        with self.assertRaises(ValueError):
            ev.place_coefficients(graph, {"sample:12": 1.0})

    def test_selection_rules_create_allowed_edges(self):
        graph = ev.build_fourier_mode_graph(2)
        edges = set(graph["edges"])
        self.assertIn((ev.mode_id((1, "cos")), ev.mode_id((2, "cos")), "selection_rule"), edges)
        self.assertIn((ev.mode_id((1, "cos")), ev.mode_id((1, "sin")), "selection_rule"), edges)

    def test_forbidden_couplings_reject(self):
        ev.validate_coupling((1, "cos"), (2, "sin"))
        with self.assertRaises(ValueError):
            ev.validate_coupling((0, "constant"), (2, "cos"))

    def test_diagonal_and_block_operator_preserve_support(self):
        coefficients = {
            ev.mode_id((0, "constant")): 1.0,
            ev.mode_id((1, "cos")): 2.0,
            ev.mode_id((1, "sin")): 0.0,
            ev.mode_id((2, "cos")): 0.5,
        }
        diagonal = ev.diagonal_operator(coefficients, {0: 1.0, 1: 3.0, 2: 4.0})
        self.assertEqual(set(diagonal), set(coefficients))
        self.assertEqual(diagonal[ev.mode_id((1, "cos"))], 6.0)

        rotated = ev.block_rotate_first_mode(coefficients, angle=0.5)
        self.assertEqual(set(rotated), set(coefficients))
        self.assertNotEqual(rotated[ev.mode_id((1, "sin"))], 0.0)

    def test_readout_reconstructs_simple_signal(self):
        coefficients = {
            ev.mode_id((0, "constant")): 1.0,
            ev.mode_id((1, "cos")): 2.0,
            ev.mode_id((1, "sin")): 0.0,
        }
        self.assertAlmostEqual(ev.readout(coefficients, 0.0), 3.0)
        self.assertAlmostEqual(ev.readout(coefficients, 3.141592653589793), -1.0)

    def test_truncation_reports_residual(self):
        coefficients = {
            ev.mode_id((0, "constant")): 1.0,
            ev.mode_id((1, "cos")): 0.5,
            ev.mode_id((3, "sin")): 0.25,
        }
        report = ev.truncation_report(coefficients, kept_max_index=1)
        self.assertGreater(report["dropped_mode_residual"], 0.0)
        self.assertFalse(report["residual_hidden"])
        self.assertNotIn(ev.mode_id((3, "sin")), report["kept"])


if __name__ == "__main__":
    unittest.main()
