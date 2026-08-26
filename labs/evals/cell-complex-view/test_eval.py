import importlib.util
from pathlib import Path
import sys
import unittest


def load_eval():
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location("cgf_cell_complex_eval", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()


def square_cells():
    return {
        "v0": ev.Cell("v0", 0),
        "v1": ev.Cell("v1", 0),
        "v2": ev.Cell("v2", 0),
        "v3": ev.Cell("v3", 0),
        "e01": ev.Cell("e01", 1, ("v0", "v1")),
        "e12": ev.Cell("e12", 1, ("v1", "v2")),
        "e23": ev.Cell("e23", 1, ("v2", "v3")),
        "e30": ev.Cell("e30", 1, ("v3", "v0")),
    }


class CellComplexViewEvalTest(unittest.TestCase):
    def test_valid_cells_resolve_boundaries(self):
        cells = square_cells()
        ev.validate_cells(cells)
        self.assertEqual(ev.boundary_of(cells, "e01"), {"v0", "v1"})

    def test_closed_path_lifts_to_two_cell(self):
        cells = square_cells()
        face = ev.lift_closed_path_to_cell(cells, ("e01", "e12", "e23", "e30"), "f0")
        self.assertEqual(face.dimension, 2)
        self.assertEqual(set(face.boundary), {"e01", "e12", "e23", "e30"})

    def test_open_path_rejected(self):
        cells = square_cells()
        with self.assertRaises(ValueError):
            ev.lift_closed_path_to_cell(cells, ("e01", "e12"), "bad")

    def test_episode_lifts_to_three_cell(self):
        episode = ev.lift_episode_to_cell("f0", ("event:a", "event:b"), "episode0")
        self.assertEqual(episode.dimension, 3)
        self.assertIn("event:a", episode.support_refs)

    def test_missing_boundary_rejected(self):
        cells = {"edge": ev.Cell("edge", 1, ("v0", "missing"))}
        with self.assertRaises(ValueError):
            ev.validate_cells(cells)


if __name__ == "__main__":
    unittest.main()
