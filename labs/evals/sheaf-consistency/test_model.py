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


class CellularSheafTest(unittest.TestCase):
    def test_constant_sheaf_sections_are_the_constant_assignments(self):
        sheaf = ev.cycle_sheaf(2, twisted=False)
        self.assertEqual(ev.global_section_dimension(sheaf), 2)
        constant = {node: (3.0, -1.0) for node in ("a", "b", "c")}
        self.assertTrue(ev.is_global_section(sheaf, constant))
        self.assertAlmostEqual(ev.consistency_energy(sheaf, constant), 0.0)

    def test_residual_localizes_the_disagreeing_view(self):
        sheaf = ev.cycle_sheaf(2, twisted=False)
        assignment = {"a": (3.0, -1.0), "b": (3.0, -1.0), "c": (3.0, 1.0)}
        residuals = ev.edge_residuals(sheaf, assignment)
        self.assertFalse(ev.is_global_section(sheaf, assignment))
        self.assertAlmostEqual(residuals["ab"], 0.0)
        self.assertAlmostEqual(residuals["bc"], 2.0)
        self.assertAlmostEqual(residuals["ca"], 2.0)

    def test_twist_is_locally_satisfiable_and_globally_obstructed(self):
        sheaf = ev.cycle_sheaf(1, twisted=True)
        # Each edge on its own can be satisfied by a nonzero assignment ...
        for satisfied, assignment in (
            ("ab", {"a": (1.0,), "b": (1.0,), "c": (0.0,)}),
            ("bc", {"a": (0.0,), "b": (1.0,), "c": (1.0,)}),
            ("ca", {"a": (-1.0,), "b": (0.0,), "c": (1.0,)}),
        ):
            self.assertAlmostEqual(ev.edge_residuals(sheaf, assignment)[satisfied], 0.0)
        # ... but no nonzero assignment satisfies all three.
        self.assertEqual(ev.global_section_dimension(sheaf), 0)
        self.assertEqual(ev.global_section_dimension(ev.cycle_sheaf(1, twisted=False)), 1)
        best_effort = {"a": (1.0,), "b": (1.0,), "c": (1.0,)}
        self.assertAlmostEqual(ev.consistency_energy(sheaf, best_effort), 4.0)

    def test_views_only_have_to_agree_where_they_overlap(self):
        sheaf = ev.shared_coordinate_sheaf()
        self.assertEqual(ev.global_section_dimension(sheaf), 3)
        agree = {"left": (5.0, 1.0), "right": (5.0, -7.0)}
        differ = {"left": (5.0, 1.0), "right": (4.0, 1.0)}
        self.assertTrue(ev.is_global_section(sheaf, agree))
        self.assertAlmostEqual(ev.edge_residuals(sheaf, differ)["overlap"], 1.0)

    def test_diffusion_lowers_energy_and_lands_on_the_nearest_section(self):
        sheaf = ev.cycle_sheaf(1, twisted=False)
        start = {"a": (0.0,), "b": (3.0,), "c": (6.0,)}
        energies = [ev.consistency_energy(sheaf, start)]
        current = start
        for _ in range(60):
            current = ev.diffuse(sheaf, current, step_size=0.2, iterations=1)
            energies.append(ev.consistency_energy(sheaf, current))
        self.assertTrue(all(later <= earlier + 1e-12 for earlier, later in zip(energies, energies[1:])))
        self.assertLess(energies[-1], 1e-12)
        # The projection onto constants is the mean of the starting values.
        for node in ("a", "b", "c"):
            self.assertAlmostEqual(current[node][0], 3.0, places=6)

    def test_diffusion_cannot_remove_a_global_obstruction_without_collapsing(self):
        sheaf = ev.cycle_sheaf(1, twisted=True)
        result = ev.diffuse(sheaf, {"a": (1.0,), "b": (1.0,), "c": (1.0,)}, step_size=0.2, iterations=200)
        self.assertLess(max(abs(value[0]) for value in result.values()), 1e-6)

    def test_undeclared_structure_is_rejected(self):
        sheaf = ev.cycle_sheaf(1, twisted=False)
        missing = dict(sheaf.restrictions)
        del missing[("a", "ab")]
        with self.assertRaises(ValueError):
            ev.validate_sheaf(
                ev.CellularSheaf(sheaf.node_dimensions, sheaf.edge_dimensions, sheaf.edges, missing)
            )
        with self.assertRaises(ValueError):
            ev.coboundary(sheaf, {"a": (1.0,), "b": (1.0,)})
        with self.assertRaises(ValueError):
            ev.coboundary(sheaf, {"a": (1.0, 2.0), "b": (1.0,), "c": (1.0,)})


if __name__ == "__main__":
    unittest.main()
