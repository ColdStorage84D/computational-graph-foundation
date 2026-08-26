import importlib.util
from pathlib import Path
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


class RenormalizationEvalTest(unittest.TestCase):
    def positive_nodes(self):
        return (
            ev.FineNode("a", "source", "law", ("a-ref",)),
            ev.FineNode("b", "bridge", "law", ("b-ref",)),
            ev.FineNode("c", "sink", "law", ("c-ref",)),
            ev.FineNode("d", "noise", "distractor", ("d-ref",)),
        )

    def hard_negative_nodes(self):
        return (
            ev.FineNode("a", "source", "law", ("a-ref",)),
            ev.FineNode("b", "bridge", "law", ("b-ref",)),
            ev.FineNode("d1", "noise", "distractor", ("d1-ref",)),
            ev.FineNode("d2", "noise", "distractor", ("d2-ref",)),
        )

    def test_coarse_nodes_preserve_source_refs(self):
        coarse = ev.coarse_grain(self.positive_nodes())
        self.assertIn("a-ref", coarse["source"]["source_refs"])
        self.assertIn("d-ref", coarse["noise"]["source_refs"])

    def test_relevant_law_separates_positive_from_hard_negative(self):
        positive = ev.relevant_law_score(ev.coarse_grain(self.positive_nodes()), (("source", "bridge"), ("bridge", "sink")))
        hard_negative = ev.relevant_law_score(ev.coarse_grain(self.hard_negative_nodes()), (("source", "bridge"),))
        self.assertEqual(positive, 2)
        self.assertLess(hard_negative, positive)

    def test_distractor_baseline_overvalues_noise(self):
        self.assertGreater(ev.distractor_baseline(self.hard_negative_nodes()), ev.distractor_baseline(self.positive_nodes()) - 1)

    def test_consistency_residual_is_visible(self):
        self.assertEqual(ev.consistency_residual(3, 3), 0)
        self.assertGreater(ev.consistency_residual(3, 2), 0)


if __name__ == "__main__":
    unittest.main()
