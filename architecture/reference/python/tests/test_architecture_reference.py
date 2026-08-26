from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cgf_architecture import (  # noqa: E402
    AnalysisNode,
    BotGraphBuilder,
    CommitOperator,
    Edge,
    EligibilityStore,
    EventLog,
    GateDecision,
    GranularAnalysisEngine,
    GraphNode,
    GraphState,
    HypergraphEncoder,
    Lens,
    OutcomeObservation,
    Path,
    Proposal,
    Trace,
    ValueMemoryStore,
    validate_path,
)


class ArchitectureReferenceTests(unittest.TestCase):
    def test_hypergraph_encoder_preserves_typed_nodes_and_hyperedges(self):
        graph = (
            HypergraphEncoder("case:1")
            .add_node(
                "sample",
                "evidence-record",
                features={"modality": "image"},
                evidence_refs=("evidence:sample",),
            )
            .add_node("region", "bounded-record", features={"quality": 0.8})
            .add_node("context", "metadata-record", features={"site": "synthetic"})
            .add_hyperedge(
                "case-view",
                "evidence-context",
                ("sample", "region", "context"),
                features={"view": "combined"},
            )
            .build()
        )

        self.assertEqual(3, len(graph.nodes))
        self.assertEqual(1, len(graph.hyperedges))
        self.assertEqual(("sample", "region", "context"), graph.hyperedges["case-view"].endpoint_ids)
        flattened = graph.flatten_features()
        self.assertEqual("image", flattened["hypergraph.node.sample.modality"])
        self.assertEqual("combined", flattened["hypergraph.edge.case-view.view"])

    def test_hypergraph_encoder_fails_closed_for_missing_endpoints(self):
        encoder = HypergraphEncoder("bad").add_node("a", "record")
        with self.assertRaises(ValueError):
            encoder.add_hyperedge("missing", "relation", ("a", "b"))

    def test_path_validation_fails_closed(self):
        graph = GraphState("g")
        graph = graph.with_node(GraphNode("a", "fact"))
        graph = graph.with_node(GraphNode("b", "fact"))
        graph = graph.with_edge(Edge("e:a:b", "a", "b", "links"))

        self.assertEqual([], validate_path(graph, Path("p", ("a", "b"), ("e:a:b",))))
        self.assertIn("missing node c", validate_path(graph, Path("bad", ("a", "c"), ("e:a:b",))))
        self.assertIn(
            "edge e:a:b does not connect path step 0",
            validate_path(graph, Path("wrong", ("b", "a"), ("e:a:b",))),
        )

    def test_hard_gate_and_policy_block_high_score(self):
        blocked = Proposal("p1", "unsafe", score=-100.0, gates=(GateDecision("safety", False),))
        allowed = Proposal("p2", "safe", score=1.0)
        decision = CommitOperator().commit((blocked, allowed))
        self.assertEqual("commit", decision.decision)
        self.assertEqual("p2", decision.selected_proposal_id)

        policy_proposal = Proposal("p3", "needs-policy", score=-1.0, policy_required="can_act")
        rejected = CommitOperator().commit((policy_proposal,))
        self.assertEqual("reject", rejected.decision)
        accepted = CommitOperator().commit((policy_proposal,), policy_basis=frozenset({"can_act"}))
        self.assertEqual("p3", accepted.selected_proposal_id)

    def test_commit_opens_eligibility_and_outcome_updates_memory(self):
        proposal = Proposal("p1", "move", score=0.0, path=Path("path:move", ("a",)))
        decision = CommitOperator().commit((proposal,))
        self.assertTrue(decision.committed)

        eligibility = EligibilityStore()
        trace = eligibility.create("elig:1", proposal=proposal, cycle_id="cycle:1")
        self.assertEqual("pending", trace.status)
        eligibility.resolve("elig:1", True)
        with self.assertRaises(ValueError):
            eligibility.resolve("elig:1", True)

        memory = ValueMemoryStore()
        update = memory.apply(
            OutcomeObservation("out:1", "elig:1", True, ("event:outcome",)),
            key="primitive:move",
        )
        self.assertEqual("reinforce", update.kind)
        self.assertEqual(1, update.after.success_count)
        self.assertLess(update.after.uncertainty, update.before.uncertainty)

    def test_replay_trace_rebuilds_from_event_log(self):
        log = EventLog()
        log.append("cycle_start", "run:1", {"cycle": 1})
        log.append("proposal", "run:1", {"proposal_id": "p1"})
        log.append("commit", "run:1", {"proposal_id": "p1"})
        log.append("outcome", "run:1", {"succeeded": True})

        replayed = EventLog.from_json(log.to_json())
        self.assertEqual(Trace.from_log(log, "run:1"), Trace.from_log(replayed, "run:1"))

    def test_bot_graph_routes_through_spine_and_static_relations_are_not_routes(self):
        graph = (
            BotGraphBuilder("bot")
            .add_surface("sensor", "sensing", handler=lambda payload: {"seen": payload})
            .add_surface("action", "action", handler=lambda payload: {"acted": payload})
            .connect_to_spine("sensor", "sense")
            .connect_to_spine("action", "act")
            .add_relation("sensor", "action", "observes_possible_action")
            .build()
        )

        runs = graph.dispatch("sense", {"x": 1})
        self.assertEqual(("brain", "spine", "sensor"), runs[0].trace_path)
        self.assertEqual(1, len(graph.relations))

        with self.assertRaises(ValueError):
            BotGraphBuilder("bad").add_surface("a", "x").add_surface("b", "y").add_route("a", "b", "x")

    def test_gated_surface_and_child_graph(self):
        child = (
            BotGraphBuilder("child")
            .add_surface("worker", "processing", handler=lambda payload: {"child": payload})
            .connect_to_spine("worker", "work")
            .build()
        )
        parent = (
            BotGraphBuilder("parent")
            .add_gated_surface("closed", "gate", gates=(GateDecision("closed", False),))
            .add_subgraph("child-capsule", "processing", child)
            .connect_to_spine("closed", "work")
            .connect_to_spine("child-capsule", "work")
            .build()
        )

        runs = parent.dispatch("work", {"task": 1})
        closed = [run for run in runs if run.node_id == "closed"][0]
        child_run = [run for run in runs if run.node_id == "child-capsule"][0]
        self.assertTrue(closed.skipped)
        self.assertEqual(({"child": {"task": 1}},), child_run.payload)

    def test_granular_analysis_runs_many_lenses_and_many_proposers(self):
        engine = GranularAnalysisEngine(
            lenses=(
                Lens("texture", "invariant", lambda row: {"texture_score": row["texture"]}, ("e:texture",)),
                Lens("morphology", "shape", lambda row: {"shape_score": row["shape"]}, ("e:shape",)),
                Lens("context", "metadata", lambda row: {"age_bucket": row["age_bucket"]}, ("e:context",)),
            ),
            analysis_nodes=(
                AnalysisNode(
                    "texture-proposer",
                    ("texture",),
                    lambda outputs: {
                        "outcome_ref": "review:pattern-a",
                        "score": outputs[0].features["texture_score"],
                        "confidence": 0.72,
                        "uncertainty": 0.20,
                    },
                ),
                AnalysisNode(
                    "morphology-proposer",
                    ("morphology",),
                    lambda outputs: {
                        "outcome_ref": "review:pattern-b",
                        "score": outputs[0].features["shape_score"],
                        "confidence": 0.70,
                        "uncertainty": 0.22,
                    },
                ),
                AnalysisNode(
                    "combined-proposer",
                    ("texture", "morphology", "context"),
                    lambda outputs: {
                        "outcome_ref": "review:combined",
                        "score": 0.88,
                        "confidence": 0.91,
                        "uncertainty": 0.08,
                    },
                ),
            ),
            commit_threshold=0.70,
            review_threshold=0.45,
        )

        result = engine.run(
            "sample:1",
            {"texture": 0.82, "shape": 0.74, "age_bucket": 3, "label": "training-only"},
        )

        self.assertEqual("commit", result.decision)
        self.assertEqual("review:combined", result.outcome_ref)
        self.assertEqual(3, len(result.trace.lens_outputs))
        self.assertEqual(3, len(result.trace.proposals))
        self.assertEqual(("label",), result.trace.hidden_keys_excluded)
        lens_usage = [proposal.lens_ids for proposal in result.trace.proposals]
        self.assertIn(("texture",), lens_usage)
        self.assertIn(("texture", "morphology", "context"), lens_usage)
        self.assertEqual(2, len(result.trace.rejected_proposal_ids))

    def test_granular_analysis_decision_modes(self):
        weak_engine = GranularAnalysisEngine(
            lenses=(Lens("weak", "raw", lambda row: {"x": row["x"]}),),
            analysis_nodes=(
                AnalysisNode("weak-proposer", ("weak",), lambda outputs: {"outcome_ref": "weak", "score": 0.2}),
            ),
        )
        self.assertEqual("abstain", weak_engine.run("weak", {"x": 1}).decision)

        review_engine = GranularAnalysisEngine(
            lenses=(Lens("mid", "raw", lambda row: {"x": row["x"]}),),
            analysis_nodes=(
                AnalysisNode(
                    "mid-proposer",
                    ("mid",),
                    lambda outputs: {"outcome_ref": "review", "score": 0.55, "confidence": 0.55},
                ),
            ),
        )
        self.assertEqual("review", review_engine.run("mid", {"x": 1}).decision)

        defer_engine = GranularAnalysisEngine(
            lenses=(Lens("bad", "raw", lambda row: {"x": row["missing"]}),),
            analysis_nodes=(
                AnalysisNode("bad-proposer", ("bad",), lambda outputs: {"outcome_ref": "none"}),
            ),
        )
        deferred = defer_engine.run("bad", {"x": 1})
        self.assertEqual("defer", deferred.decision)
        self.assertTrue(deferred.trace.errors)

    def test_granular_analysis_rejects_training_only_lens_output(self):
        engine = GranularAnalysisEngine(
            lenses=(Lens("leaky", "raw", lambda row: {"label": "bad"}),),
            analysis_nodes=(AnalysisNode("node", ("leaky",), lambda outputs: {"outcome_ref": "bad"}),),
        )

        result = engine.run("sample", {"x": 1, "label": "secret"})
        self.assertEqual("defer", result.decision)
        self.assertIn("label", result.trace.hidden_keys_excluded)
        self.assertIn("training-only", result.trace.errors[0])


if __name__ == "__main__":
    unittest.main()
