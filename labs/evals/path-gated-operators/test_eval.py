import importlib.util
from pathlib import Path
import sys
import unittest


def load_eval():
    name = "cgf_path_gated_operators_eval"
    if name in sys.modules:
        return sys.modules[name]
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()


def graph():
    return ev.EvidenceGraph(
        node_types={
            "record": "evidence",
            "link": "intermediate",
            "claim:a": "claim",
            "claim:b": "claim",
            "note": "intermediate",
        },
        edges={
            "e1": ("record", "link"),
            "e2": ("link", "claim:a"),
            "e3": ("note", "claim:b"),
        },
    )


SUPPORTED = ev.Candidate("a", "claim:a", 0.55, ev.EvidencePath(("record", "link", "claim:a"), ("e1", "e2")))


class PathGatedOperatorsEvalTest(unittest.TestCase):
    def test_resolvable_path_passes_the_gate(self):
        outcome = ev.hard_gate(graph(), SUPPORTED)
        self.assertTrue(outcome.allowed)
        self.assertEqual(outcome.reason, "path_resolved")

    def test_gate_fails_closed_on_every_kind_of_broken_path(self):
        cases = {
            "no_path": ev.Candidate("x", "claim:a", 0.9, None),
            "missing edge": ev.Candidate(
                "x", "claim:a", 0.9, ev.EvidencePath(("record", "link", "claim:a"), ("e1", "e9"))
            ),
            "does not connect": ev.Candidate(
                "x", "claim:a", 0.9, ev.EvidencePath(("record", "link", "claim:a"), ("e2", "e1"))
            ),
            "missing node": ev.Candidate(
                "x", "claim:a", 0.9, ev.EvidencePath(("ghost", "claim:a"), ("e2",))
            ),
            "edge count": ev.Candidate(
                "x", "claim:a", 0.9, ev.EvidencePath(("record", "link", "claim:a"), ("e1",))
            ),
        }
        for label, candidate in cases.items():
            outcome = ev.hard_gate(graph(), candidate)
            self.assertFalse(outcome.allowed, label)
            self.assertIn(label.split()[0], outcome.reason)

    def test_path_must_start_at_evidence_and_reach_its_own_claim(self):
        from_note = ev.Candidate("b", "claim:b", 0.9, ev.EvidencePath(("note", "claim:b"), ("e3",)))
        self.assertEqual(ev.hard_gate(graph(), from_note).reason, "path_does_not_start_at_evidence")
        wrong_claim = ev.Candidate(
            "b", "claim:b", 0.9, ev.EvidencePath(("record", "link", "claim:a"), ("e1", "e2"))
        )
        self.assertEqual(ev.hard_gate(graph(), wrong_claim).reason, "path_does_not_reach_claim")

    def test_highest_score_does_not_commit_without_a_path(self):
        unsupported = ev.Candidate("b", "claim:b", 0.95, ev.EvidencePath(("note", "claim:b"), ("e3",)))
        candidates = (SUPPORTED, unsupported)
        self.assertEqual(ev.decide_score_only(candidates).selected_id, "b")
        gated = ev.decide_path_gated(graph(), candidates)
        self.assertEqual(gated.selected_id, "a")
        self.assertEqual([item.candidate_id for item in gated.rejected], ["b"])

    def test_gate_abstains_and_keeps_the_reasons_when_nothing_passes(self):
        decision = ev.decide_path_gated(
            graph(), (ev.Candidate("x", "claim:a", 0.9, None), ev.Candidate("y", "claim:b", 0.8, None))
        )
        self.assertEqual(decision.action, "abstain")
        self.assertIsNone(decision.selected_id)
        self.assertEqual({item.reason for item in decision.rejected}, {"no_path"})

    def test_conditioning_changes_rank_but_cannot_admit_a_gated_candidate(self):
        direct_graph = ev.EvidenceGraph(
            {"r1": "evidence", "r2": "evidence", "m": "intermediate", "c1": "claim", "c2": "claim"},
            {"d": ("r1", "c1"), "l1": ("r2", "m"), "l2": ("m", "c2")},
        )
        direct = ev.Candidate("direct", "c1", 0.60, ev.EvidencePath(("r1", "c1"), ("d",)))
        chained = ev.Candidate("chained", "c2", 0.70, ev.EvidencePath(("r2", "m", "c2"), ("l1", "l2")))
        blocked = ev.Candidate("blocked", "c2", 0.99, None)
        candidates = (direct, chained, blocked)
        self.assertEqual(ev.decide_path_gated(direct_graph, candidates).selected_id, "chained")
        conditioned = ev.decide_path_gated(direct_graph, candidates, hop_discount=0.8)
        self.assertEqual(conditioned.selected_id, "direct")
        self.assertEqual([item.candidate_id for item in conditioned.rejected], ["blocked"])
        self.assertAlmostEqual(ev.path_conditioned_score(chained, hop_discount=0.8), 0.56)
        with self.assertRaises(ValueError):
            ev.path_conditioned_score(chained, hop_discount=0.0)


if __name__ == "__main__":
    unittest.main()
