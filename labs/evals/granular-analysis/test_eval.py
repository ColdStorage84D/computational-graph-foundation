import importlib.util
from pathlib import Path
import sys
import unittest


def load_eval():
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location("cgf_granular_analysis_eval", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()


class GranularAnalysisEvalTest(unittest.TestCase):
    def test_one_input_creates_multiple_lens_outputs(self):
        result = ev.run_fixture()
        self.assertEqual(3, len(result.trace.lens_outputs))
        self.assertEqual({"texture", "morphology", "context"}, {item.lens_id for item in result.trace.lens_outputs})

    def test_one_lens_output_feeds_multiple_proposal_nodes(self):
        result = ev.run_fixture()
        texture_users = [
            proposal.proposer_id
            for proposal in result.trace.proposals
            if "texture" in proposal.lens_ids
        ]
        self.assertGreaterEqual(len(texture_users), 3)

    def test_one_outcome_considers_multiple_proposals(self):
        result = ev.run_fixture()
        self.assertEqual("commit", result.decision)
        self.assertEqual("candidate:combined-supported", result.outcome_ref)
        self.assertEqual(4, len(result.trace.proposals))
        self.assertEqual(3, len(result.trace.rejected_proposal_ids))

    def test_rejected_proposals_are_counterfactual_alternatives(self):
        result = ev.run_fixture()
        proposal_ids = {proposal.proposal_id for proposal in result.trace.proposals}
        self.assertTrue(set(result.trace.rejected_proposal_ids).issubset(proposal_ids))
        self.assertNotIn(result.trace.selected_proposal_id, result.trace.rejected_proposal_ids)

    def test_training_only_labels_do_not_enter_lens_outputs(self):
        result = ev.run_fixture()
        self.assertEqual(("label",), result.trace.hidden_keys_excluded)
        for output in result.trace.lens_outputs:
            self.assertNotIn("label", output.features)

    def test_histology_like_fixture_has_no_domain_claim(self):
        result = ev.run_fixture()
        self.assertTrue(result.outcome_ref.startswith("candidate:"))
        self.assertNotIn("diagnosis", result.outcome_ref)


if __name__ == "__main__":
    unittest.main()
