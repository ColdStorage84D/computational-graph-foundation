import importlib.util
from pathlib import Path
import random
import sys
import unittest


def load_eval():
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location("cgf_renormalization_eval", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()


class NetworkRenormalizationTest(unittest.TestCase):
    def test_eliminating_a_middle_node_gives_the_series_coupling(self):
        network = ev.make_network((("a", "m", 2.0), ("m", "b", 6.0)))
        coarse, _ = ev.renormalize(network, ("a", "b"))
        self.assertEqual(set(coarse), {("a", "b")})
        self.assertAlmostEqual(coarse[("a", "b")], 2.0 * 6.0 / (2.0 + 6.0))

    def test_coarse_network_reproduces_the_fine_response_on_kept_nodes(self):
        fine = ev.ladder_network(rungs=5, rail=2.0, rung=1.0)
        keep = ("t0", "t4", "b0", "b4")
        coarse, _ = ev.renormalize(fine, keep)
        # Renormalization creates couplings that the fine network never had.
        self.assertIn(("b0", "t4"), coarse)
        self.assertNotIn(("b0", "t4"), fine)
        injections = {"t0": 1.0, "b0": 0.5}
        fine_response = ev.potentials(fine, injections, ground="b4")
        coarse_response = ev.potentials(coarse, injections, ground="b4")
        for node in keep:
            self.assertAlmostEqual(coarse_response[node], fine_response[node], places=10)
        self.assertAlmostEqual(
            ev.effective_coupling(coarse, "t0", "b4"), ev.effective_coupling(fine, "t0", "b4"), places=10
        )

    def test_dropping_detail_without_renormalizing_changes_the_answer(self):
        fine = ev.ladder_network(rungs=3, rail=2.0, rung=1.0)
        keep = ("t0", "b0", "t2", "b2")
        exact = ev.effective_coupling(fine, "t0", "b0")
        renormalized, _ = ev.renormalize(fine, keep)
        naive = ev.naive_coarse_grain(fine, keep)
        self.assertAlmostEqual(ev.effective_coupling(renormalized, "t0", "b0"), exact, places=10)
        # The naive coarse network keeps only the two rungs: it loses every
        # path through the eliminated nodes and underestimates the coupling.
        self.assertEqual(set(naive), {("b0", "t0"), ("b2", "t2")})
        self.assertLess(naive[("b0", "t0")], 0.8 * exact)

    def test_uniform_chain_coupling_flows_by_a_factor_of_two_per_step(self):
        couplings = (4.0,) * 16
        end_to_end = ev.effective_coupling(ev.chain_network(couplings), "n000", "n016")
        segment = 1
        while len(couplings) > 1:
            couplings = ev.decimate_chain(couplings)
            segment *= 2
            self.assertAlmostEqual(couplings[0], 4.0 / segment)
            # Coupling times segment length is the scale-invariant quantity.
            self.assertAlmostEqual(couplings[0] * segment, 4.0)
        self.assertAlmostEqual(couplings[0], end_to_end)

    def test_repeated_coarse_graining_of_a_disordered_chain_does_not_drift(self):
        rng = random.Random(3)
        couplings = tuple(rng.uniform(0.2, 5.0) for _ in range(32))
        reference = ev.effective_coupling(ev.chain_network(couplings), "n000", "n032")
        levels = 0
        while len(couplings) > 1:
            couplings = ev.decimate_chain(couplings)
            levels += 1
            last = f"n{len(couplings):03d}"
            self.assertAlmostEqual(
                ev.effective_coupling(ev.chain_network(couplings), "n000", last), reference, places=10
            )
        self.assertEqual(levels, 5)

    def test_sources_on_eliminated_nodes_must_be_renormalized_too(self):
        fine = ev.ladder_network(rungs=4, rail=2.0, rung=1.0)
        keep = ("t0", "b0", "t3", "b3")
        injections = {"t1": 1.0}
        fine_response = ev.potentials(fine, injections, ground="b3")
        coarse, coarse_sources = ev.renormalize(fine, keep, injections)
        with_sources = ev.potentials(coarse, coarse_sources, ground="b3")
        without_sources = ev.potentials(coarse, {}, ground="b3")
        for node in keep:
            self.assertAlmostEqual(with_sources[node], fine_response[node], places=10)
        self.assertGreater(abs(without_sources["t0"] - fine_response["t0"]), 0.1)
        self.assertAlmostEqual(sum(coarse_sources.values()), 1.0)

    def test_undeclared_structure_is_rejected(self):
        network = ev.make_network((("a", "m", 2.0), ("m", "b", 6.0)))
        with self.assertRaises(ValueError):
            ev.renormalize(network, ("a", "elsewhere"))
        with self.assertRaises(ValueError):
            ev.renormalize(network, ("a",))
        with self.assertRaises(ValueError):
            ev.make_network((("a", "b", 0.0),))
        with self.assertRaises(ValueError):
            ev.decimate_chain((1.0, 2.0, 3.0))


if __name__ == "__main__":
    unittest.main()
