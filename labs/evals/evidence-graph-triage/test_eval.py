"""Contract tests for the Evidence Graph Triage eval."""

from __future__ import annotations

import unittest

from eval import (
    Candidate,
    Record,
    TriageRun,
    decide_status,
    fixture_candidates,
    run_eval,
)


class StatusFromEvidenceTests(unittest.TestCase):
    def test_no_records_defers(self) -> None:
        decision = decide_status(())
        self.assertEqual((decision.status, decision.action), ("needs_more_evidence", "defer"))

    def test_single_record_is_inferred(self) -> None:
        decision = decide_status((Record("record:1", "source_a"),))
        self.assertEqual((decision.status, decision.action), ("inferred", "defer"))

    def test_gate_pair_confirms(self) -> None:
        decision = decide_status(
            (Record("record:1", "source_a"), Record("record:2", "source_b"))
        )
        self.assertEqual((decision.status, decision.action), ("confirmed", "commit"))
        self.assertEqual(decision.matched_gate_id, "gate:a-b")

    def test_status_ignores_score(self) -> None:
        """The status function cannot receive a score, so scale cannot reach it."""

        records = (Record("record:1", "source_a"),)
        low = Candidate("finding:low", "rule-one", 0.01, records)
        high = Candidate("finding:high", "rule-one", 99.0, records)
        self.assertEqual(decide_status(low.records), decide_status(high.records))

    def test_highest_scoring_candidate_is_still_deferred(self) -> None:
        result = run_eval()
        self.assertEqual(result["top_raw_finding"], "finding:single-source-high")
        self.assertEqual(result["top_raw_action"], "defer")


class MemoryAffectsOrderOnlyTests(unittest.TestCase):
    def test_outcome_changes_order_but_no_status(self) -> None:
        result = run_eval()
        self.assertTrue(result["statuses_unchanged"])
        self.assertTrue(result["order_changed"])

    def test_true_positive_raises_the_multiplier(self) -> None:
        self.assertGreater(run_eval()["multiplier_after_true_positive"], 1.0)

    def test_uncommitted_finding_cannot_update_value(self) -> None:
        run = TriageRun()
        run.rank(fixture_candidates(), cycle_id="cycle-1")
        with self.assertRaises(ValueError):
            run.record_outcome("verdict:x", "finding:single-source-high", "true_positive")

    def test_second_resolve_is_refused(self) -> None:
        run = TriageRun()
        run.rank(fixture_candidates(), cycle_id="cycle-1")
        run.record_outcome("verdict:1", "finding:corroborated", "true_positive")
        with self.assertRaises(ValueError):
            run.record_outcome("verdict:2", "finding:corroborated", "false_positive")

    def test_replayed_verdict_is_ignored(self) -> None:
        run = TriageRun()
        run.rank(fixture_candidates(), cycle_id="cycle-1")
        run.record_outcome("verdict:1", "finding:corroborated", "true_positive")
        self.assertEqual(
            run.record_outcome("verdict:1", "finding:corroborated", "true_positive"),
            "duplicate_ignored",
        )


class UncertaintyNeverSuccessTests(unittest.TestCase):
    def test_inconclusive_does_not_raise_the_multiplier(self) -> None:
        run = TriageRun()
        run.rank(fixture_candidates(), cycle_id="cycle-1")
        key = "rule-one|confirmed|source_a+source_b"
        run.record_outcome("verdict:1", "finding:corroborated", "true_positive")
        before = run.values.multiplier(key)
        run.values.apply(key, "inconclusive")
        self.assertLessEqual(run.values.multiplier(key), before)

    def test_expiry_raises_uncertainty_and_is_not_success(self) -> None:
        run = TriageRun()
        run.rank(fixture_candidates(), cycle_id="cycle-1")
        key = "rule-one|confirmed|source_a+source_b"
        run.values.apply(key, "true_positive")
        before = run.values.get(key)
        run.expire("finding:corroborated")
        after = run.values.get(key)
        self.assertGreater(after.uncertainty, before.uncertainty)
        self.assertEqual(after.support, before.support)
        self.assertEqual(after.expired_count, 1)


if __name__ == "__main__":
    unittest.main()
