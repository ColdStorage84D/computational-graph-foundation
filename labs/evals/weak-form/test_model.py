import importlib.util
from pathlib import Path
import random
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


def fixture():
    law = ev.path_law(9, weight=2.0, mass=1.0)
    source = {node: 1.0 + 0.5 * index * index for index, node in enumerate(law.nodes)}
    return law, source


class DiscreteWeakFormTest(unittest.TestCase):
    def test_summation_by_parts_links_weak_and_strong_residuals(self):
        law, source = fixture()
        rng = random.Random(7)
        field = {node: rng.uniform(-2.0, 2.0) for node in law.nodes}
        strong = ev.strong_residual(law, field, source)
        for _ in range(5):
            test = {node: rng.uniform(-1.0, 1.0) for node in law.nodes}
            expected = sum(test[node] * strong[node] for node in law.nodes)
            self.assertAlmostEqual(ev.tested_residual(law, field, source, test), expected, places=10)

    def test_nodal_test_functions_recover_the_local_rule(self):
        law, source = fixture()
        field = {node: float(index) for index, node in enumerate(law.nodes)}
        strong = ev.strong_residual(law, field, source)
        for node in law.nodes:
            indicator = {other: 1.0 if other == node else 0.0 for other in law.nodes}
            self.assertAlmostEqual(ev.tested_residual(law, field, source, indicator), strong[node])

    def test_region_test_function_is_a_boundary_balance(self):
        law, source = fixture()
        rng = random.Random(11)
        field = {node: rng.uniform(0.0, 3.0) for node in law.nodes}
        region = frozenset({"n2", "n3", "n4", "n5"})
        indicator = {node: 1.0 if node in region else 0.0 for node in law.nodes}
        balance = ev.region_balance(law, field, source, region)
        self.assertAlmostEqual(ev.tested_residual(law, field, source, indicator), balance["residual"])
        # Only the two boundary edges contribute to the outflow.
        expected_outflow = 2.0 * (field["n2"] - field["n1"]) + 2.0 * (field["n5"] - field["n6"])
        self.assertAlmostEqual(balance["outflow"], expected_outflow)

    def test_galerkin_passes_every_coarse_test_while_local_failures_stay_visible(self):
        law, source = fixture()
        basis = ev.hat_basis(law, (0, 4, 8))
        field = ev.galerkin_solve(law, source, basis)
        for test in basis:
            self.assertAlmostEqual(ev.tested_residual(law, field, source, test), 0.0, places=9)
        strong = ev.strong_residual(law, field, source)
        self.assertGreater(max(abs(value) for value in strong.values()), 0.5)
        # Hats sum to one, so total balance over the whole graph also closes.
        whole = ev.region_balance(law, field, source, frozenset(law.nodes))
        self.assertAlmostEqual(whole["residual"], 0.0, places=9)

    def test_refining_the_test_space_converges_to_the_local_rule(self):
        law, source = fixture()
        worst = []
        for centers in ((0, 4, 8), (0, 2, 4, 6, 8), tuple(range(9))):
            field = ev.galerkin_solve(law, source, ev.hat_basis(law, centers))
            worst.append(max(abs(value) for value in ev.strong_residual(law, field, source).values()))
        self.assertGreater(worst[0], worst[1])
        self.assertGreater(worst[1], worst[2])
        self.assertLess(worst[2], 1e-9)

    def test_omitted_source_term_shows_up_in_the_tested_condition(self):
        law, source = fixture()
        field = ev.galerkin_solve(law, source, ev.hat_basis(law, tuple(range(9))))
        region = frozenset({"n6", "n7", "n8"})
        without_source = {node: 0.0 for node in law.nodes}
        honest = ev.region_balance(law, field, source, region)
        omitted = ev.region_balance(law, field, without_source, region)
        self.assertAlmostEqual(honest["residual"], 0.0, places=9)
        self.assertAlmostEqual(omitted["residual"], sum(source[node] for node in region), places=9)

    def test_undeclared_structure_is_rejected(self):
        law, source = fixture()
        with self.assertRaises(ValueError):
            ev.strong_residual(law, {"n0": 1.0}, source)
        with self.assertRaises(ValueError):
            ev.validate_law(ev.GraphLaw(("a", "b"), (("a", "b", -1.0),)))
        with self.assertRaises(ValueError):
            ev.region_balance(law, source, source, frozenset({"elsewhere"}))
        with self.assertRaises(ValueError):
            # A pure Laplacian with a partition-of-unity basis has no unique solution.
            ev.galerkin_solve(ev.path_law(9, mass=0.0), source, ev.hat_basis(law, (0, 4, 8)))


if __name__ == "__main__":
    unittest.main()
