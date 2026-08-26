import json
import os
import tempfile
import unittest
from pathlib import Path

from benchmark_resources import (
    BENCHMARK_ENV_VAR,
    BenchmarkResourceError,
    export_benchmark_graph_cases,
    load_benchmark_records,
    run_benchmark_smoke,
)
from synthetic_review import (
    APP_DIR,
    TRAINING_ONLY_KEYS,
    build_case,
    build_demo_payload,
    load_fixture_records,
    run_review_for_record,
    run_synthetic_review,
)


class SyntheticMedicalImageAnalysisReviewTests(unittest.TestCase):
    def test_source_evidence_stays_as_refs(self):
        evidence, graph, _ = run_synthetic_review()
        self.assertTrue(all(item.raw_payload_present for item in evidence))
        live_values = set(graph.live_record().values())
        self.assertTrue(any(str(value).startswith("evidence:image:") for value in live_values))
        self.assertNotIn("not-live-input", live_values)

    def test_later_records_are_excluded_from_lens_outputs(self):
        _, _, result = run_synthetic_review()
        self.assertIn("review_decision", result.trace.hidden_keys_excluded)
        for output in result.trace.lens_outputs:
            for key in TRAINING_ONLY_KEYS:
                self.assertNotIn(key, output.features)

    def test_training_only_diagnosis_key_is_excluded_when_present(self):
        record = load_fixture_records()[0] | {"diagnosis": "evaluation-only"}
        _, _, result = run_review_for_record(record)
        self.assertIn("diagnosis", result.trace.hidden_keys_excluded)

    def test_one_case_creates_many_lens_outputs(self):
        _, _, result = run_synthetic_review()
        self.assertEqual({"texture", "morphology", "context"}, {item.lens_id for item in result.trace.lens_outputs})

    def test_one_review_item_considers_many_proposals(self):
        _, _, result = run_synthetic_review()
        self.assertEqual("review", result.decision)
        self.assertEqual("review-item:combined-evidence", result.outcome_ref)
        self.assertEqual(3, len(result.trace.proposals))
        self.assertEqual(2, len(result.trace.rejected_proposal_ids))

    def test_proposals_preserve_routes_and_evidence(self):
        _, _, result = run_synthetic_review()
        routes = {proposal.metadata["route"] for proposal in result.trace.proposals}
        evidence_refs = set()
        for proposal in result.trace.proposals:
            evidence_refs.update(proposal.evidence_refs)
        self.assertEqual({"texture-route", "morphology-route", "combined-review-route"}, routes)
        self.assertEqual(
            {"evidence:sample-image", "evidence:region-measurement", "evidence:case-metadata"},
            evidence_refs,
        )

    def test_graph_has_review_separation_shape(self):
        _, graph = build_case()
        self.assertEqual(4, len(graph.nodes))
        self.assertEqual(3, len(graph.edges))
        self.assertIn("review_decision", graph.later_records)
        self.assertNotIn("review_decision", graph.live_record())

    def test_graph_can_emit_generic_encoded_hypergraph(self):
        _, graph = build_case()
        encoded = graph.encoded_hypergraph()
        self.assertEqual(4, len(encoded.nodes))
        self.assertEqual(3, len(encoded.hyperedges))
        self.assertIn("texture", encoded.nodes)
        self.assertIn("edge:0:has_record", encoded.hyperedges)
        flattened = encoded.flatten_features()
        self.assertEqual(0.79, flattened["hypergraph.node.texture.texture_contrast"])

    def test_fixture_records_drive_review_without_external_data(self):
        records = load_fixture_records()
        self.assertGreaterEqual(len(records), 3)
        decisions = {}
        for record in records:
            _, _, result = run_review_for_record(record)
            decisions[record["case_id"]] = result.decision
            self.assertGreaterEqual(len(result.trace.proposals), 3)
        self.assertEqual("abstain", decisions["fixture-low-confidence-1"])
        self.assertIn(decisions["fixture-texture-1"], {"review", "commit"})

    def test_demo_payload_references_committed_fixture_assets(self):
        payload = build_demo_payload()
        self.assertGreaterEqual(len(payload["cases"]), 3)
        for case in payload["cases"]:
            image_path = APP_DIR / case["image"]
            self.assertTrue(image_path.is_file(), image_path)
            self.assertIn("region graph", case["visual_graph"]["stages"])
            self.assertGreaterEqual(len(case["visual_graph"]["regions"]), 3)
            self.assertIn("proposal routes", case["visual_graph"]["stages"])
            self.assertIn(case["result"]["decision"], {"commit", "review", "abstain", "defer"})
            self.assertIn("rejected_proposal_ids", case["result"])

    def test_static_demo_uses_local_scripts_and_no_canvas(self):
        html = (APP_DIR / "index.html").read_text(encoding="utf-8")
        self.assertIn("demo-data.js", html)
        self.assertIn("demo.js", html)
        self.assertIn("region-overlay", html)
        self.assertIn("flow", html)
        self.assertNotIn("<canvas", html.lower())
        self.assertNotIn("http://", html)
        self.assertNotIn("https://", html)

    def test_optional_benchmark_skips_without_env(self):
        old_value = os.environ.pop(BENCHMARK_ENV_VAR, None)
        try:
            self.assertEqual([], load_benchmark_records())
        finally:
            if old_value is not None:
                os.environ[BENCHMARK_ENV_VAR] = old_value

    def test_optional_benchmark_rejects_invalid_folder(self):
        old_value = os.environ.get(BENCHMARK_ENV_VAR)
        with tempfile.TemporaryDirectory() as tmp:
            os.environ[BENCHMARK_ENV_VAR] = tmp
            with self.assertRaises(BenchmarkResourceError):
                load_benchmark_records()
        if old_value is None:
            os.environ.pop(BENCHMARK_ENV_VAR, None)
        else:
            os.environ[BENCHMARK_ENV_VAR] = old_value

    def test_optional_benchmark_loads_valid_local_shape(self):
        old_value = os.environ.get(BENCHMARK_ENV_VAR)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            images = root / "images"
            images.mkdir()
            (images / "case-001.svg").write_text("<svg></svg>", encoding="utf-8")
            (root / "records.jsonl").write_text(
                json.dumps(
                    {
                        "case_id": "case-001",
                        "image": "images/case-001.svg",
                        "question": "fixture question",
                        "answer": "evaluation-only",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            os.environ[BENCHMARK_ENV_VAR] = str(root)
            records = load_benchmark_records()
            self.assertEqual(1, len(records))
            self.assertEqual("evaluation-only", records[0]["answer"])
            self.assertTrue(Path(records[0]["image_path"]).is_file())
            graph_cases = export_benchmark_graph_cases()
            self.assertEqual(1, len(graph_cases))
            self.assertGreaterEqual(len(graph_cases[0]["nodes"]), 4)
            smoke = run_benchmark_smoke()
            self.assertEqual(1, smoke["record_count"])
            self.assertEqual("local smoke test only", smoke["claim"])
            self.assertIn("answer", smoke["runs"][0]["hidden_keys_excluded"])
        if old_value is None:
            os.environ.pop(BENCHMARK_ENV_VAR, None)
        else:
            os.environ[BENCHMARK_ENV_VAR] = old_value


if __name__ == "__main__":
    unittest.main()
