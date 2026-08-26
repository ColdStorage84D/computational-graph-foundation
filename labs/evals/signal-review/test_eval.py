import unittest

from eval import HIDDEN_KEYS, run_fixture, synthetic_signal_packet


class SignalReviewEvalTests(unittest.TestCase):
    def test_raw_signal_does_not_become_authority(self):
        result = run_fixture()
        self.assertEqual("review", result.decision)
        self.assertNotEqual("commit", result.decision)
        self.assertIsNotNone(result.outcome_ref)

    def test_one_signal_creates_multiple_feature_views(self):
        result = run_fixture()
        self.assertEqual(
            {"level-view", "trend-view", "regime-view"},
            {item.lens_id for item in result.trace.lens_outputs},
        )

    def test_route_specific_processors_create_competing_proposals(self):
        result = run_fixture()
        routes = {proposal.metadata["route"] for proposal in result.trace.proposals}
        self.assertEqual(
            {"level-route", "trend-route", "regime-route", "fallback-route"},
            routes,
        )
        self.assertEqual(4, len(result.trace.proposals))

    def test_rejected_alternatives_remain_in_trace(self):
        result = run_fixture()
        self.assertEqual(3, len(result.trace.rejected_proposal_ids))
        proposal_ids = {proposal.proposal_id for proposal in result.trace.proposals}
        self.assertTrue(set(result.trace.rejected_proposal_ids).issubset(proposal_ids))

    def test_weak_signal_support_abstains(self):
        weak = synthetic_signal_packet(raw_signal=0.18, trend_score=0.21, source_quality=0.74)
        result = run_fixture(weak)
        self.assertEqual("abstain", result.decision)
        self.assertIsNone(result.outcome_ref)

    def test_stale_signal_uses_fallback_review(self):
        stale = synthetic_signal_packet(raw_signal=0.83, trend_score=0.78, source_quality=0.30, stale=True)
        result = run_fixture(stale)
        self.assertEqual("review", result.decision)
        self.assertEqual("candidate:fallback-review", result.outcome_ref)

    def test_future_labels_do_not_enter_lens_outputs(self):
        result = run_fixture()
        self.assertIn("future_outcome", result.trace.hidden_keys_excluded)
        self.assertIn("profit_loss", result.trace.hidden_keys_excluded)
        self.assertIn("maintenance_result", result.trace.hidden_keys_excluded)
        for output in result.trace.lens_outputs:
            for key in HIDDEN_KEYS:
                self.assertNotIn(key, output.features)


if __name__ == "__main__":
    unittest.main()
