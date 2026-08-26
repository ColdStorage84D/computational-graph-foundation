import unittest

from eval import processor_allowed, run_eval


class MultimodalFrameworkMixEvalTests(unittest.TestCase):
    def test_evidence_records_keep_raw_payload_out_of_graph(self):
        records, graph, *_ = run_eval()
        self.assertTrue(any(record.raw_payload for record in records))
        feature_values = set(graph.feature_record().values())
        self.assertNotIn("not-copied-image-bytes", feature_values)
        self.assertIn("evidence:image-a", feature_values)

    def test_training_only_label_does_not_enter_lens_outputs(self):
        *_, result = run_eval()
        self.assertIn("label", result.trace.hidden_keys_excluded)
        for output in result.trace.lens_outputs:
            self.assertNotIn("label", output.features)

    def test_feature_views_keep_kinds_separate(self):
        _, graph, views, *_ = run_eval()
        record = graph.feature_record()
        self.assertEqual("invariant", views["texture"].kind)
        self.assertEqual("raw", views["layout"].kind)
        self.assertIn("texture.texture_contrast", views["texture"].select(record))
        self.assertNotIn("layout.orientation_score", views["texture"].select(record))

    def test_processor_routing_rejects_invalid_invariance_fit(self):
        _, _, _, processors, tasks, _ = run_eval()
        self.assertFalse(processor_allowed(processors["texture-invariant"], tasks["orientation-task"]))
        self.assertTrue(processor_allowed(processors["layout-direct"], tasks["orientation-task"]))
        self.assertTrue(processor_allowed(processors["texture-invariant"], tasks["texture-task"]))

    def test_proposals_preserve_route_and_view_basis(self):
        *_, result = run_eval()
        routes = {proposal.metadata["route"] for proposal in result.trace.proposals}
        lens_sets = {proposal.lens_ids for proposal in result.trace.proposals}
        self.assertIn("texture-invariant", routes)
        self.assertIn("layout-direct", routes)
        self.assertIn("combined", routes)
        self.assertIn(("texture", "layout", "metadata"), lens_sets)

    def test_review_outcome_preserves_rejected_alternatives(self):
        *_, result = run_eval()
        self.assertEqual("review", result.decision)
        self.assertEqual("proposal:combined-review", result.outcome_ref)
        self.assertEqual(3, len(result.trace.proposals))
        self.assertEqual(2, len(result.trace.rejected_proposal_ids))

    def test_trace_carries_all_evidence_refs(self):
        *_, result = run_eval()
        evidence_refs = set()
        for output in result.trace.lens_outputs:
            evidence_refs.update(output.evidence_refs)
        self.assertEqual(
            {"evidence:image-a", "evidence:layout-a", "evidence:metadata-a"},
            evidence_refs,
        )


if __name__ == "__main__":
    unittest.main()
