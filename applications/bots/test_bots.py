import unittest

from graph_memory_bot import build_graph_memory_bot, run_graph_memory_bot_demo
from maze_value_memory import ValueMemory, run_episode
from provisional_route_growth import (
    ProvisionalRouteGrowthBot,
    observation as route_observation,
    run_route_growth_demo,
)
from robot_topology_trace import build_robot_topology, build_trace_step, validate_trace_step


class BotApplicationTests(unittest.TestCase):
    def test_graph_memory_bot_creates_multiple_candidate_actions(self):
        bot = build_graph_memory_bot()
        state = bot.input_state(0)
        candidates = bot.candidate_actions(state)

        self.assertGreaterEqual(len(candidates), 3)
        self.assertEqual("generic_task_state", state.kind)

    def test_graph_memory_bot_selected_action_comes_from_candidates(self):
        run = run_graph_memory_bot_demo(max_ticks=1)
        step = run.steps[0]
        candidate_ids = {item.candidate.action_id for item in step.candidates}

        self.assertIn(step.selected_action_id, candidate_ids)
        self.assertEqual(
            next(item.candidate.command for item in step.candidates if item.candidate.action_id == step.selected_action_id),
            step.selected_command,
        )

    def test_graph_memory_bot_keeps_blocked_candidates_in_trace(self):
        run = run_graph_memory_bot_demo(max_ticks=1)
        step = run.steps[0]
        blocked = [item for item in step.candidates if item.gate.outcome == "block"]

        self.assertTrue(blocked)
        self.assertIn(blocked[0].candidate.action_id, step.rejected_action_ids)

    def test_graph_memory_bot_gate_is_visible_before_selection(self):
        run = run_graph_memory_bot_demo(max_ticks=1)
        step = run.steps[0]
        gate_outcomes = {item.gate.outcome for item in step.candidates}

        self.assertIn("safety / policy gate", step.decision_path)
        self.assertTrue({"block", "downgrade"} & gate_outcomes)

    def test_graph_memory_bot_observation_produces_prediction_error(self):
        run = run_graph_memory_bot_demo(max_ticks=1)
        step = run.steps[0]

        self.assertGreaterEqual(step.observed_outcome.prediction_error, 0.0)
        self.assertTrue(step.memory_updates)

    def test_graph_memory_bot_memory_update_changes_later_scoring(self):
        bot = build_graph_memory_bot()
        state = bot.input_state(0)
        before = {
            item.candidate.action_id: item.score_before_gate
            for item in bot.evaluate_candidates(state)
        }
        first_step = bot.run_tick(0)
        after = {
            item.candidate.action_id: item.score_before_gate
            for item in bot.evaluate_candidates(state)
        }

        self.assertNotEqual(
            before[first_step.selected_action_id],
            after[first_step.selected_action_id],
        )
        self.assertNotEqual(first_step.memory_updates[0].before, first_step.memory_updates[0].after)

    def test_graph_memory_bot_route_growth_is_explicit_and_provisional(self):
        run = run_graph_memory_bot_demo(max_ticks=1)
        summary = run.route_growth_summary

        self.assertEqual("provisional:unknown:c", summary["provisional_route_id"])
        self.assertGreaterEqual(summary["candidate_count"], 1)
        self.assertIn("unknown:c:rolled_back", summary["trace"])

    def test_maze_value_memory_changes_second_run(self):
        memory = ValueMemory()
        first = run_episode(memory)
        second = run_episode(memory)

        self.assertTrue(first["reached"])
        self.assertTrue(second["reached"])
        self.assertGreater(first["blocked_discoveries"], 0)
        self.assertEqual(0, second["blocked_discoveries"])
        self.assertLess(second["steps"], first["steps"])

    def test_robot_topology_has_sensors_actions_actuators_and_limits(self):
        graph = build_robot_topology()
        types = {node["node_type"] for node in graph["nodes"]}
        self.assertIn("sensor", types)
        self.assertIn("action_candidate", types)
        self.assertIn("actuator", types)
        self.assertIn("safety_limit", types)
        self.assertGreaterEqual(len(graph["edges"]), 4)

    def test_robot_trace_requires_selected_action_in_evidence_path(self):
        trace = build_trace_step(
            tick=1,
            selected_action="action:move",
            gate_outcome="allow",
            gate_reason="within_speed_limit",
            emitted_command={"left": 0.5, "right": 0.5},
        )
        self.assertEqual([], validate_trace_step(trace))

        bad = dict(trace)
        bad["selected_action"] = "action:hidden"
        self.assertIn("selected action must appear in evidence paths", validate_trace_step(bad))

    def test_blocked_gate_is_visible(self):
        trace = build_trace_step(
            tick=2,
            selected_action="action:move",
            gate_outcome="deny",
            gate_reason="speed_limit",
            emitted_command={"left": 0.0, "right": 0.0},
        )
        self.assertEqual([], validate_trace_step(trace))

    def test_provisional_route_growth_promotes_recurring_unknown_pattern(self):
        run = run_route_growth_demo()

        self.assertEqual("route:known_a", run.known_route)
        self.assertEqual("route:review_fallback", run.unknown_before_route)
        self.assertEqual("provisional:unknown:c", run.provisional_route_id)
        self.assertGreaterEqual(run.candidate_count, 1)
        self.assertNotEqual("route:review_fallback", run.promoted_route)
        self.assertIn("unknown:c:promoted:new_route", run.trace)

    def test_provisional_route_growth_blocks_bursts_and_rolls_back(self):
        run = run_route_growth_demo()

        self.assertEqual("burst", run.burst_temporal_shape)
        self.assertFalse(run.burst_promoted)
        self.assertEqual("route:review_fallback", run.route_after_rollback)
        self.assertIn("unknown:c:rolled_back", run.trace)

    def test_shadow_candidate_has_no_commit_authority(self):
        bot = ProvisionalRouteGrowthBot()
        items = [
            route_observation(1, "unknown:x", tick=1, quality=0.9, risk=0.05),
            route_observation(2, "unknown:x", tick=5, quality=0.9, risk=0.05),
        ]
        provisional = None
        for item in items:
            provisional = bot.observe(item) or provisional
        candidate = bot.candidate_routes(provisional)[0]
        score = bot.shadow_score(candidate, items[-1])

        self.assertEqual("shadow_only", score["authority"])
        self.assertFalse(score["can_commit"])
        self.assertNotIn("unknown:x", bot.promoted_routes)


if __name__ == "__main__":
    unittest.main()
