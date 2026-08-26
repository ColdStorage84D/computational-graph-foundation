import importlib.util
from pathlib import Path
import sys
import unittest


def load_eval():
    path = Path(__file__).with_name("eval.py")
    spec = importlib.util.spec_from_file_location("cgf_provisional_graph_growth_eval", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ev = load_eval()


def observation(index, *, pattern="new_pattern", surprise=0.8, quality=0.9, risk=0.2, tick=None):
    return ev.Observation(
        observation_id=f"obs-{index}",
        pattern_key=pattern,
        evidence_ref=f"trace:{index}",
        surprise=surprise,
        quality=quality,
        risk=risk,
        tick=index if tick is None else tick,
    )


class ProvisionalGraphGrowthEvalTests(unittest.TestCase):
    def test_repeated_observations_create_provisional_graph(self):
        runtime = ev.ProvisionalGraphGrowthRuntime(activation_threshold=1.0)
        self.assertIsNone(runtime.observe(observation(1, surprise=0.5, quality=0.8)))
        graph = runtime.observe(observation(4, surprise=0.9, quality=0.9))

        self.assertIsNotNone(graph)
        self.assertEqual("provisional", graph.status)
        self.assertIn("trace:1", graph.evidence_refs)
        self.assertIn("trace:4", graph.evidence_refs)

    def test_one_off_burst_is_held_by_refractory_and_evidence_rules(self):
        runtime = ev.ProvisionalGraphGrowthRuntime(activation_threshold=0.7, refractory_ticks=3)
        first = runtime.observe(observation(1, surprise=1.0, quality=0.9))
        duplicate = runtime.observe(observation(2, surprise=1.0, quality=0.9))

        self.assertIsNotNone(first)
        self.assertIsNone(duplicate)
        self.assertEqual(1, len(runtime.provisional_graphs))

    def test_activation_decay_requires_recurring_support(self):
        runtime = ev.ProvisionalGraphGrowthRuntime(activation_threshold=1.0, decay=0.2)
        runtime.observe(observation(1, surprise=0.6, quality=0.8))
        runtime.observe(observation(10, surprise=0.2, quality=0.8))

        self.assertEqual({}, runtime.provisional_graphs)

    def test_candidate_variants_are_bounded_and_probationary(self):
        runtime = ev.ProvisionalGraphGrowthRuntime(activation_threshold=0.8, max_variants=2)
        graph = runtime.observe(observation(1, surprise=1.0, quality=0.9))
        variants = runtime.spawn_variants(graph, [observation(1), observation(2)])

        self.assertEqual(2, len(variants))
        self.assertEqual(2, len({variant.strategy for variant in variants}))
        self.assertTrue(all(variant.status == "probation" for variant in variants))
        self.assertTrue(all(0.0 < variant.traffic_weight <= 0.5 for variant in variants))

    def test_risky_variants_are_quarantined(self):
        runtime = ev.ProvisionalGraphGrowthRuntime(activation_threshold=0.8, max_variants=3, risk_limit=0.35)
        graph = runtime.observe(observation(1, surprise=1.0, quality=0.9, risk=0.4))
        variants = runtime.spawn_variants(graph, [observation(1, risk=0.4), observation(2, risk=0.5)])

        self.assertTrue(any(variant.status == "quarantine" for variant in variants))
        quarantined = [variant for variant in variants if variant.status == "quarantine"]
        self.assertTrue(all(variant.traffic_weight == 0.0 for variant in quarantined))

    def test_shadow_scoring_never_commits_authority(self):
        runtime = ev.ProvisionalGraphGrowthRuntime(activation_threshold=0.8)
        graph = runtime.observe(observation(1, surprise=1.0, quality=0.9))
        variant = runtime.spawn_variants(graph, [observation(1)])[0]
        before = runtime.durable_snapshot()

        score = runtime.shadow_score(variant, observation(2, quality=0.8))

        self.assertEqual("shadow_only", score["authority"])
        self.assertFalse(score["can_commit"])
        self.assertEqual(before, runtime.durable_snapshot())

    def test_stability_guard_rejects_bursts_and_accepts_stable_support(self):
        runtime = ev.ProvisionalGraphGrowthRuntime()
        burst = [
            observation(1, tick=10, quality=0.9),
            observation(2, tick=11, quality=0.9),
        ]
        stable = [
            observation(1, tick=1, quality=0.8),
            observation(2, tick=5, quality=0.9),
            observation(3, tick=11, quality=0.85),
        ]

        self.assertEqual("burst", runtime.stability_guard(burst)["temporal_shape"])
        self.assertFalse(runtime.stability_guard(burst)["accepted"])
        self.assertEqual("stable", runtime.stability_guard(stable)["temporal_shape"])
        self.assertTrue(runtime.stability_guard(stable)["accepted"])

    def test_low_affinity_variants_are_retired(self):
        runtime = ev.ProvisionalGraphGrowthRuntime(activation_threshold=0.2)
        graph = runtime.observe(observation(1, surprise=1.0, quality=0.3, risk=0.1))
        variants = runtime.spawn_variants(graph, [observation(1, quality=0.3, risk=0.1)])

        retired = runtime.retire_variants(min_affinity=0.35)

        self.assertIn(variants[0].variant_id, retired)
        self.assertEqual("retired", variants[0].status)
        self.assertEqual(0.0, variants[0].traffic_weight)

    def test_growth_patch_requires_evidence_and_probation_variant(self):
        runtime = ev.ProvisionalGraphGrowthRuntime(activation_threshold=0.8)
        graph = runtime.observe(observation(1, surprise=1.0, quality=0.9))
        variant = runtime.spawn_variants(graph, [observation(1)])[0]

        with self.assertRaises(ev.GrowthRejectedError):
            runtime.make_growth_patch(variant, [])

        variant.status = "quarantine"
        with self.assertRaises(ev.GrowthRejectedError):
            runtime.make_growth_patch(variant, ["trace:1"])

    def test_durable_graph_does_not_change_before_promotion(self):
        runtime = ev.ProvisionalGraphGrowthRuntime(activation_threshold=0.8)
        before = runtime.durable_snapshot()
        graph = runtime.observe(observation(1, surprise=1.0, quality=0.95))
        variant = runtime.spawn_variants(graph, [observation(1, quality=0.95)])[0]
        patch = runtime.make_growth_patch(variant, graph.evidence_refs)

        with self.assertRaises(ev.DurableMutationError):
            runtime.apply_patch(patch, promoted=False)
        self.assertEqual(before, runtime.durable_snapshot())

    def test_promotion_requires_quality_cost_risk_and_updates_durable_graph(self):
        runtime = ev.ProvisionalGraphGrowthRuntime(activation_threshold=0.8, risk_limit=0.6)
        graph = runtime.observe(observation(1, surprise=1.0, quality=1.0, risk=0.05))
        variant = runtime.spawn_variants(graph, [observation(1, quality=1.0, risk=0.05)])[0]
        patch = runtime.make_growth_patch(variant, graph.evidence_refs)

        self.assertTrue(runtime.should_promote(patch))
        runtime.apply_patch(patch, promoted=True)

        after = runtime.durable_snapshot()
        self.assertIn("node:new_edge", after["nodes"])
        self.assertIn(("source", "node:new_edge"), after["edges"])
        self.assertEqual("promoted", runtime.provisional_graphs[graph.graph_id].status)

    def test_promotion_requires_stable_temporal_shape_and_review_flags(self):
        runtime = ev.ProvisionalGraphGrowthRuntime(activation_threshold=0.8, risk_limit=0.6)
        graph = runtime.observe(observation(1, surprise=1.0, quality=1.0, risk=0.05))
        variant = runtime.spawn_variants(graph, [observation(1, quality=1.0, risk=0.05)])[0]

        burst_patch = runtime.make_growth_patch(variant, graph.evidence_refs, temporal_shape="burst")
        unsafe_patch = runtime.make_growth_patch(variant, graph.evidence_refs, safety_review_pass=False)
        no_baseline_patch = runtime.make_growth_patch(variant, graph.evidence_refs, baseline_comparison_pass=False)
        no_held_out_patch = runtime.make_growth_patch(variant, graph.evidence_refs, held_out_pass=False)

        self.assertFalse(runtime.should_promote(burst_patch))
        self.assertFalse(runtime.should_promote(unsafe_patch))
        self.assertFalse(runtime.should_promote(no_baseline_patch))
        self.assertFalse(runtime.should_promote(no_held_out_patch))

    def test_failed_benefit_selection_rejects_promotion(self):
        runtime = ev.ProvisionalGraphGrowthRuntime(activation_threshold=0.2, risk_limit=0.6)
        graph = runtime.observe(observation(1, surprise=1.0, quality=0.3, risk=0.5))
        variant = runtime.spawn_variants(graph, [observation(1, quality=0.3, risk=0.5)])[0]
        patch = runtime.make_growth_patch(variant, graph.evidence_refs)

        self.assertFalse(runtime.should_promote(patch))
        with self.assertRaises(ev.GrowthRejectedError):
            runtime.apply_patch(patch, promoted=True)

    def test_scenario_routes_known_pattern_without_growth(self):
        run = ev.run_provisional_growth_scenario()

        self.assertEqual("route:known_a", run.known_route)
        self.assertEqual("route:review_fallback", run.unknown_before_route)

    def test_scenario_promotes_recurring_unknown_pattern(self):
        run = ev.run_provisional_growth_scenario()

        self.assertEqual("provisional:unknown:c", run.provisional_graph_id)
        self.assertGreaterEqual(run.candidate_variant_count, 1)
        self.assertTrue(run.promoted_route.startswith("route:"))
        self.assertNotEqual("route:review_fallback", run.promoted_route)
        self.assertTrue(run.durable_changed_after_promotion)
        self.assertTrue(any(event.startswith("unknown:c:promoted") for event in run.events))

    def test_scenario_rejects_burst_unknown_pattern(self):
        run = ev.run_provisional_growth_scenario()

        self.assertEqual("burst", run.burst_temporal_shape)
        self.assertFalse(run.burst_promoted)
        self.assertIn("unknown:d:held:burst_pattern", run.events)

    def test_scenario_rolls_back_regressed_promoted_pattern(self):
        run = ev.run_provisional_growth_scenario()

        self.assertEqual("route:review_fallback", run.route_after_rollback)
        self.assertTrue(run.durable_restored_after_rollback)
        self.assertIn("unknown:c:rolled_back", run.events)


if __name__ == "__main__":
    unittest.main()
