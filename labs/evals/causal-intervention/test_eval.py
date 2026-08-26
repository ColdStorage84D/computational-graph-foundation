import importlib.util
from pathlib import Path
import sys
import unittest


def load_eval():
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location("cgf_causal_intervention_eval", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()


class CausalInterventionEvalTest(unittest.TestCase):
    def test_observation_has_no_attribution(self):
        observation = ev.observe("obs", "molecule", "distractor_present")
        outcome = ev.observe("out", "molecule", "active")
        self.assertEqual(ev.score_attribution(observation, outcome, ("source", "bridge", "sink")), 0.0)

    def test_intervention_scope_controls_attribution(self):
        intervention = ev.intervene("do-chain", "molecule", "ablated", ("source", "bridge", "sink"))
        distractor = ev.intervene("do-distractor", "molecule", "ablated", ("distractor",))
        outcome = ev.observe("out", "molecule", "inactive")
        self.assertEqual(ev.score_attribution(intervention, outcome, ("source", "bridge", "sink")), 1.0)
        self.assertEqual(ev.score_attribution(distractor, outcome, ("source", "bridge", "sink")), 0.0)

    def test_counterfactual_promotion_is_blocked(self):
        dream = ev.mark_counterfactual("dream", "route", "alternate")
        self.assertTrue(ev.block_counterfactual_promotion(dream))

    def test_missing_intervention_scope_rejects(self):
        with self.assertRaises(ValueError):
            ev.intervene("bad", "subject", "value", ())

    def test_attribution_trace_links_candidate_and_outcome(self):
        intervention = ev.intervene("do", "system", "change", ("control",))
        outcome = ev.observe("out", "system", "changed")
        trace = ev.trace_attribution(intervention, outcome, ("control",))
        self.assertTrue(trace["allowed"])
        self.assertEqual(trace["candidate_ref"], "do")
        self.assertEqual(trace["outcome_ref"], "out")


if __name__ == "__main__":
    unittest.main()
