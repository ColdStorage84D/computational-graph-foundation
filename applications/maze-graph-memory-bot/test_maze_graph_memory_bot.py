import importlib.util
from pathlib import Path
import sys
import unittest


APP_DIR = Path(__file__).resolve().parent
MODULE_PATH = APP_DIR / "maze_graph_memory_webots.py"
POLICY_PATH = APP_DIR / "maze_webots_graph_policy.py"
DIAGNOSTICS_PATH = APP_DIR / "maze_failure_diagnostics.py"

spec = importlib.util.spec_from_file_location("maze_graph_memory_webots", MODULE_PATH)
maze_graph_memory_webots = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = maze_graph_memory_webots
spec.loader.exec_module(maze_graph_memory_webots)

policy_spec = importlib.util.spec_from_file_location("maze_webots_graph_policy", POLICY_PATH)
maze_policy = importlib.util.module_from_spec(policy_spec)
assert policy_spec.loader is not None
sys.modules[policy_spec.name] = maze_policy
policy_spec.loader.exec_module(maze_policy)

diagnostics_spec = importlib.util.spec_from_file_location("maze_failure_diagnostics", DIAGNOSTICS_PATH)
maze_diagnostics = importlib.util.module_from_spec(diagnostics_spec)
assert diagnostics_spec.loader is not None
sys.modules[diagnostics_spec.name] = maze_diagnostics
diagnostics_spec.loader.exec_module(maze_diagnostics)


class MazeGraphMemoryBotWebotsTests(unittest.TestCase):
    def test_world_and_controller_are_shipped(self):
        world = APP_DIR / "main" / "worlds" / "maze_graph_memory.wbt"
        controller = (
            APP_DIR
            / "main"
            / "controllers"
            / "maze_graph_memory_controller"
            / "maze_graph_memory_controller.py"
        )
        self.assertTrue(world.exists())
        self.assertTrue(controller.exists())
        world_text = world.read_text(encoding="utf-8")
        controller_text = controller.read_text(encoding="utf-8")
        self.assertIn('controller "maze_graph_memory_controller"', world_text)
        self.assertIn("Pioneer3at", world_text)
        self.assertIn("DEF MAZEBOT_START", world_text)
        self.assertIn("DEF MAZEBOT_GOAL", world_text)
        self.assertIn("DEF MAZE_WALL_68", world_text)
        self.assertIn("SickLms291", world_text)
        self.assertEqual(1, world_text.count('controller "maze_graph_memory_controller"'))
        self.assertIn("select_maze_action", controller_text)
        self.assertIn("build_sensor_state", controller_text)
        self.assertIn("front left wheel", controller_text)
        self.assertIn("back right wheel", controller_text)

    def test_launch_info_points_to_webots_world(self):
        info = maze_graph_memory_webots.build_webots_launch_info(seed=2, max_ticks=5)

        self.assertEqual("Maze Graph Memory Bot", info["app"])
        self.assertTrue(info["world"].endswith("maze_graph_memory.wbt"))
        self.assertEqual("maze_graph_memory_controller", info["controller"])
        self.assertEqual("Webots graph-action fixture only", info["claim"])

    def test_optional_webots_status_skips_or_reports_available(self):
        result = maze_graph_memory_webots.run_webots_app(seed=0, max_ticks=1)

        self.assertIn(result["status"], {"skipped", "available"})
        self.assertIn("world", result)
        self.assertIn("claim", result)

    def test_graph_trace_uses_generalized_graph_memory_bot(self):
        trace = maze_graph_memory_webots.build_graph_memory_trace(max_ticks=1)
        step = trace["steps"][0]

        self.assertGreaterEqual(len(step["candidates"]), 3)
        self.assertIn(step["selected_action_id"], {item["candidate"]["action_id"] for item in step["candidates"]})
        self.assertTrue(step["rejected_action_ids"])

    def test_no_webapp_surface_is_shipped(self):
        self.assertFalse((APP_DIR / "index.html").exists())
        self.assertFalse((APP_DIR / "demo.js").exists())
        self.assertFalse((APP_DIR / "styles.css").exists())

    def test_webots_controller_does_not_auto_quit_by_default(self):
        controller = (
            APP_DIR
            / "main"
            / "controllers"
            / "maze_graph_memory_controller"
            / "maze_graph_memory_controller.py"
        ).read_text(encoding="utf-8")

        self.assertIn('os.environ.get("CGF_MAZE_GRAPH_MEMORY_MAX_TICKS", "0")', controller)
        self.assertIn('auto_quit = _env_flag("CGF_WEBOTS_AUTO_QUIT")', controller)
        self.assertIn("if auto_quit:", controller)
        self.assertIn("robot.simulationQuit(0)", controller)
        self.assertIn("recovery_queue", controller)
        self.assertIn("movement_delta", controller)
        self.assertIn("goal_sensor_reading", controller)
        self.assertIn('"goal_sensor"', controller)
        self.assertIn("no_progress_streak", controller)
        self.assertIn("CGF_MAZE_GRAPH_MEMORY_YAW_OFFSET_RAD", controller)
        self.assertIn("_goal_target", controller)
        self.assertIn("navigation_sensor_record", controller)
        self.assertIn("CGF_MAZE_GRAPH_MEMORY_GOAL_DEF", controller)
        self.assertIn("build_recovery_plan", controller)
        self.assertIn("guard_recovery_item", controller)
        self.assertIn("MazeActionOutcomeMemory", controller)
        self.assertIn("pending_learning", controller)
        self.assertIn("maze_graph_memory_learning.json", controller)
        self.assertIn("CGF_MAZE_GRAPH_MEMORY_PERSIST_LEARNING", controller)
        self.assertIn('"persistent_learning_enabled"', controller)
        self.assertIn('"learning_outcome"', controller)
        self.assertIn('"learning_memory"', controller)
        self.assertIn("memory_biases", controller)
        self.assertIn("CGF_MAZE_GRAPH_MEMORY_RUNTIME_DIR", controller)
        self.assertIn("maze_graph_memory_diagnostics.jsonl", controller)
        self.assertIn("maze_graph_memory_failure_points.jsonl", controller)
        self.assertNotIn("MAZE_ROUTE", controller)
        self.assertNotIn("route_index", controller)
        self.assertNotIn("select_navigation_goal", controller)

    def test_maze_policy_advances_when_goal_and_front_are_clear(self):
        state = maze_policy.build_sensor_state(
            tick=0,
            pose=(0.0, 0.0, 0.0),
            goal=(8.0, 0.0),
            clearances=(0.9, 0.8, 0.8, 0.8),
        )
        decision = maze_policy.select_maze_action(state)

        self.assertEqual("action:advance", decision.selected_action_id)
        self.assertGreater(decision.selected_command["throttle"], 0.0)
        self.assertLess(abs(decision.selected_command["turn"]), 0.2)

    def test_policy_has_no_predeclared_maze_route_or_cells(self):
        policy_text = POLICY_PATH.read_text(encoding="utf-8")

        self.assertFalse(hasattr(maze_policy, "MAZE_ROUTE"))
        self.assertNotIn("route_index", policy_text)
        self.assertNotIn("select_navigation_goal", policy_text)
        self.assertNotIn("cell_key", policy_text)
        self.assertNotIn("route:", policy_text)
        self.assertNotIn(":cell:", policy_text)

    def test_navigation_uses_arbitrary_goal_sensor_not_route_node(self):
        state = maze_policy.build_sensor_state(
            tick=12,
            pose=(3.0, -2.0, 0.0),
            goal=(6.0, -2.0),
            clearances=(0.9, 0.8, 0.8, 0.8),
        )
        sensor = maze_policy.navigation_sensor_record(state)
        decision = maze_policy.select_maze_action(state)

        self.assertFalse(sensor["maze_map_known"])
        self.assertEqual({"x": 6.0, "y": -2.0}, sensor["target"])
        self.assertTrue(sensor["memory_context_key"].startswith("sensor:"))
        self.assertEqual("action:advance", decision.selected_action_id)

    def test_navigation_sensor_context_changes_with_live_evidence(self):
        open_state = maze_policy.build_sensor_state(
            tick=13,
            pose=(0.0, 0.0, 0.0),
            goal=(8.0, 0.0),
            clearances=(0.9, 0.8, 0.8, 0.8),
        )
        tight_state = maze_policy.build_sensor_state(
            tick=14,
            pose=(0.0, 0.0, 0.0),
            goal=(8.0, 0.0),
            clearances=(0.04, 0.16, 0.8, 0.04),
        )

        self.assertNotEqual(
            maze_policy.MazeActionOutcomeMemory.context_key(open_state),
            maze_policy.MazeActionOutcomeMemory.context_key(tight_state),
        )

    def test_final_goal_is_an_attractor_near_marker(self):
        state = maze_policy.build_sensor_state(
            tick=4000,
            pose=(-14.8, 15.4, 2.9),
            goal=(-16.0, 16.0),
            clearances=(0.28, 0.42, 0.12, 0.12),
        )
        decision = maze_policy.select_maze_action(state)

        self.assertEqual("action:goal_attractor", decision.selected_action_id)
        self.assertEqual("final_goal_attractor", decision.candidates[0].reason)
        self.assertNotIn(decision.selected_action_id, {"action:escape_left", "action:escape_right"})

    def test_goal_sensor_reports_distance_and_attractor_strength(self):
        state = maze_policy.build_sensor_state(
            tick=4000,
            pose=(-14.8, 15.4, 2.9),
            goal=(-16.0, 16.0),
            clearances=(0.28, 0.42, 0.12, 0.12),
        )
        sensor = maze_policy.goal_sensor_reading(state)

        self.assertEqual({"x": -16.0, "y": 16.0}, sensor["target"])
        self.assertGreater(sensor["distance"], 1.0)
        self.assertGreater(sensor["attractor_strength"], 0.0)
        self.assertTrue(sensor["inside_attractor_radius"])
        self.assertFalse(sensor["inside_goal_radius"])

    def test_final_goal_keeps_attracting_beside_marker(self):
        state = maze_policy.build_sensor_state(
            tick=4001,
            pose=(-15.45, 15.65, 2.9),
            goal=(-16.0, 16.0),
            clearances=(0.22, 0.18, 0.16, 0.16),
        )
        decision = maze_policy.select_maze_action(state)

        self.assertEqual("action:goal_attractor", decision.selected_action_id)
        self.assertGreater(decision.selected_command["throttle"], 0.0)

    def test_final_goal_holds_only_on_marker(self):
        state = maze_policy.build_sensor_state(
            tick=4002,
            pose=(-15.72, 15.82, 2.9),
            goal=(-16.0, 16.0),
            clearances=(0.22, 0.18, 0.16, 0.16),
        )
        decision = maze_policy.select_maze_action(state)

        self.assertEqual("action:hold", decision.selected_action_id)
        self.assertEqual({"throttle": 0.0, "turn": 0.0}, decision.selected_command)

    def test_maze_policy_rotates_when_heading_is_wrong_at_start(self):
        state = maze_policy.build_sensor_state(
            tick=0,
            pose=(16.0, -16.0, -1.5708),
            goal=(16.0, -12.0),
            clearances=(0.9, 0.8, 0.8, 0.8),
        )
        decision = maze_policy.select_maze_action(state)

        self.assertIn(decision.selected_action_id, {"action:rotate_left", "action:rotate_right"})
        self.assertLessEqual(abs(decision.selected_command["turn"]), 0.62)

    def test_maze_policy_uses_arcs_or_reverse_when_front_is_blocked(self):
        state = maze_policy.build_sensor_state(
            tick=0,
            pose=(0.0, 0.0, 0.0),
            goal=(8.0, 0.0),
            clearances=(0.04, 0.75, 0.2, 0.04),
        )
        decision = maze_policy.select_maze_action(state)

        self.assertIn(decision.selected_action_id, {"action:arc_left", "action:reverse"})
        self.assertNotEqual("action:advance", decision.selected_action_id)

    def test_maze_policy_turns_away_from_right_wall_even_when_goal_aligned(self):
        state = maze_policy.build_sensor_state(
            tick=899,
            pose=(0.0, 0.0, 0.0),
            goal=(8.0, 0.0),
            clearances=(0.105, 0.50, 0.062, 0.062),
        )
        decision = maze_policy.select_maze_action(state)
        advance = next(item for item in decision.candidates if item.action_id == "action:advance")

        self.assertEqual("action:escape_left", decision.selected_action_id)
        self.assertEqual("block", advance.gate)
        self.assertEqual("side_wall_escape_required", advance.reason)

    def test_maze_policy_turns_away_from_left_wall_even_when_goal_aligned(self):
        state = maze_policy.build_sensor_state(
            tick=900,
            pose=(0.0, 0.0, 0.0),
            goal=(8.0, 0.0),
            clearances=(0.105, 0.062, 0.50, 0.062),
        )
        decision = maze_policy.select_maze_action(state)
        advance = next(item for item in decision.candidates if item.action_id == "action:advance")

        self.assertEqual("action:escape_right", decision.selected_action_id)
        self.assertEqual("block", advance.gate)
        self.assertEqual("side_wall_escape_required", advance.reason)

    def test_maze_policy_wall_escape_beats_heading_rotation_into_wall(self):
        state = maze_policy.build_sensor_state(
            tick=899,
            pose=(14.45294, -11.04977, -3.0653),
            goal=(-16.0, 16.0),
            clearances=(0.511, 0.342, 0.104, 0.104),
        )
        decision = maze_policy.select_maze_action(state)

        self.assertEqual("action:escape_left", decision.selected_action_id)
        self.assertNotEqual("action:rotate_right", decision.selected_action_id)

    def test_maze_policy_centers_between_corridor_walls(self):
        state = maze_policy.build_sensor_state(
            tick=901,
            pose=(0.0, 0.0, 0.0),
            goal=(8.0, 0.0),
            clearances=(0.35, 0.26, 0.12, 0.12),
        )
        decision = maze_policy.select_maze_action(state)
        advance = next(item for item in decision.candidates if item.action_id == "action:advance")

        self.assertEqual("action:escape_left", decision.selected_action_id)
        self.assertIn(advance.gate, {"block", "downgrade"})
        self.assertNotEqual("action:advance", decision.selected_action_id)

    def test_maze_policy_keeps_centering_on_small_side_imbalance(self):
        state = maze_policy.build_sensor_state(
            tick=1799,
            pose=(11.76154, -8.03351, 1.55968),
            goal=(-16.0, 16.0),
            clearances=(0.67239, 0.19233, 0.25145, 0.19233),
        )
        decision = maze_policy.select_maze_action(state)

        self.assertEqual("action:escape_right", decision.selected_action_id)
        self.assertNotEqual("action:rotate_left", decision.selected_action_id)

    def test_maze_policy_keeps_centering_on_sensor_noise_band(self):
        state = maze_policy.build_sensor_state(
            tick=1799,
            pose=(11.86128, -7.97842, 1.56065),
            goal=(-16.0, 16.0),
            clearances=(0.70215, 0.20474, 0.23900, 0.20474),
        )
        decision = maze_policy.select_maze_action(state)

        self.assertEqual("action:escape_right", decision.selected_action_id)
        self.assertNotEqual("action:rotate_left", decision.selected_action_id)

    def test_maze_policy_blocks_in_place_rotation_between_walls(self):
        state = maze_policy.build_sensor_state(
            tick=1799,
            pose=(11.93921, -8.49395, 1.56034),
            goal=(-16.0, 16.0),
            clearances=(0.74846, 0.21453, 0.22926, 0.21453),
        )
        decision = maze_policy.select_maze_action(state)
        blocked_rotations = [
            item for item in decision.candidates
            if item.action_id.startswith("action:rotate") and item.gate == "block"
        ]

        self.assertEqual(2, len(blocked_rotations))
        self.assertNotIn(decision.selected_action_id, {"action:rotate_left", "action:rotate_right"})

    def test_maze_policy_anti_spin_guard_blocks_rotation_when_front_is_clear(self):
        state = maze_policy.build_sensor_state(
            tick=6,
            pose=(0.0, 0.0, 1.5),
            goal=(8.0, 0.0),
            clearances=(0.85, 0.8, 0.8, 0.8),
            spin_streak=6,
        )
        decision = maze_policy.select_maze_action(state)
        blocked_rotations = [
            item for item in decision.candidates
            if item.action_id.startswith("action:rotate") and item.gate == "block"
        ]

        self.assertEqual(2, len(blocked_rotations))
        self.assertNotIn(decision.selected_action_id, {"action:rotate_left", "action:rotate_right"})
        self.assertGreater(decision.selected_command["throttle"], 0.0)

    def test_maze_policy_memory_bias_can_change_selected_action(self):
        state = maze_policy.build_sensor_state(
            tick=30,
            pose=(0.0, 0.0, 0.0),
            goal=(8.0, 0.0),
            clearances=(0.9, 0.8, 0.8, 0.8),
        )
        baseline = maze_policy.select_maze_action(state)
        learned = maze_policy.select_maze_action(
            state,
            memory_biases={"action:advance": -2.0, "action:arc_left": 0.8},
        )
        advance = next(item for item in learned.candidates if item.action_id == "action:advance")

        self.assertEqual("action:advance", baseline.selected_action_id)
        self.assertNotEqual("action:advance", learned.selected_action_id)
        self.assertIn("action-outcome memory", learned.decision_path)
        self.assertIn("memory_bias=-2.00", advance.reason)

    def test_poisoned_memory_cannot_select_hold_away_from_goal(self):
        state = maze_policy.build_sensor_state(
            tick=31,
            pose=(16.12, -15.95, 1.82),
            goal=(16.0, -12.0),
            clearances=(0.70, 0.23, 0.22, 0.21),
        )
        decision = maze_policy.select_maze_action(
            state,
            memory_biases={
                "action:advance": -1.76,
                "action:arc_left": -1.60,
                "action:arc_right": -1.16,
                "action:escape_left": -1.68,
                "action:reverse": -0.66,
            },
        )

        self.assertNotEqual("action:hold", decision.selected_action_id)
        self.assertTrue(
            abs(decision.selected_command["throttle"]) > 0.0
            or abs(decision.selected_command["turn"]) > 0.0
        )

    def test_action_outcome_memory_penalizes_repeated_local_failure(self):
        memory = maze_policy.MazeActionOutcomeMemory()
        state = maze_policy.build_sensor_state(
            tick=40,
            pose=(0.0, 0.0, 0.0),
            goal=(8.0, 0.0),
            clearances=(0.9, 0.8, 0.8, 0.8),
        )
        context_key = maze_policy.MazeActionOutcomeMemory.context_key(state)
        for _ in range(2):
            outcome = memory.record_outcome(
                context_key=context_key,
                action_id="action:advance",
                movement_delta=0.0,
                previous_goal_distance=8.0,
                current_goal_distance=8.0,
                contact_active=False,
                no_progress=True,
            )

        biases = memory.biases_for(context_key=context_key)

        self.assertEqual("failure", outcome["status"])
        self.assertTrue(outcome["key"].startswith("sensor:"))
        self.assertLess(biases["action:advance"], -0.3)
        self.assertGreater(biases["action:arc_left"], 0.0)
        self.assertGreater(biases["action:arc_right"], 0.0)

    def test_action_outcome_memory_preserves_success_and_round_trips(self):
        memory = maze_policy.MazeActionOutcomeMemory()
        state = maze_policy.build_sensor_state(
            tick=41,
            pose=(1.0, 1.0, 0.0),
            goal=(8.0, 1.0),
            clearances=(0.9, 0.6, 0.6, 0.6),
        )
        context_key = maze_policy.MazeActionOutcomeMemory.context_key(state)
        outcome = memory.record_outcome(
            context_key=context_key,
            action_id="action:arc_left",
            movement_delta=0.2,
            previous_goal_distance=8.0,
            current_goal_distance=7.8,
            contact_active=False,
            no_progress=False,
        )
        restored = maze_policy.MazeActionOutcomeMemory.from_dict(memory.to_dict())
        biases = restored.biases_for(context_key=context_key)

        self.assertEqual("success", outcome["status"])
        self.assertGreater(biases["action:arc_left"], 0.0)
        self.assertIn("actions", restored.summary_for(context_key=context_key))

    def test_recovery_decision_backs_out_from_contact(self):
        state = maze_policy.build_sensor_state(
            tick=10,
            pose=(0.0, 0.0, 0.0),
            goal=(8.0, 0.0),
            clearances=(0.12, 0.10, 0.18, 0.10),
        )
        decision = maze_policy.recovery_decision(
            state,
            action_id="action:recovery_reverse",
            command={"throttle": -0.36, "turn": 0.0},
            reason="back_out_from_contact",
        )

        self.assertEqual("action:recovery_reverse", decision.selected_action_id)
        self.assertLess(decision.selected_command["throttle"], 0.0)
        self.assertIn("gps no-progress / contact detection", decision.decision_path)

    def test_tight_corner_recovery_plan_does_not_probe_forward(self):
        state = maze_policy.build_sensor_state(
            tick=58272,
            pose=(-8.81881, -9.06866, -2.78671),
            goal=(-12.0, -8.0),
            clearances=(0.0724, 0.0824, 0.0735, 0.0724),
        )
        plan = maze_policy.build_recovery_plan(state)
        action_ids = [item["action_id"] for item in plan]
        rotate = next(item for item in plan if item["action_id"] == "action:recovery_rotate_clear")

        self.assertTrue(maze_policy.tight_corner_trap(state))
        self.assertEqual("action:recovery_deep_reverse", action_ids[0])
        self.assertNotIn("action:recovery_probe_forward", action_ids)
        self.assertLess(rotate["command"]["turn"], 0.0)

    def test_probe_recovery_is_guarded_when_front_still_blocked(self):
        state = maze_policy.build_sensor_state(
            tick=58273,
            pose=(-8.82198, -9.06952, -2.79251),
            goal=(-12.0, -8.0),
            clearances=(0.0719, 0.0824, 0.0732, 0.0719),
        )
        guarded = maze_policy.guard_recovery_item(
            state,
            {
                "action_id": "action:recovery_probe_forward",
                "command": {"throttle": 0.24, "turn": -0.12},
                "reason": "probe_after_contact_recovery",
            },
        )

        self.assertEqual("action:recovery_probe_blocked_reverse", guarded["action_id"])
        self.assertLess(guarded["command"]["throttle"], 0.0)

    def test_normal_recovery_plan_keeps_probe_after_reverse_and_rotate(self):
        state = maze_policy.build_sensor_state(
            tick=20,
            pose=(1.0, 2.0, 0.5),
            goal=(8.0, 2.0),
            clearances=(0.10, 0.40, 0.22, 0.09),
        )
        plan = maze_policy.build_recovery_plan(state)
        action_ids = [item["action_id"] for item in plan]

        self.assertFalse(maze_policy.tight_corner_trap(state))
        self.assertIn("action:recovery_probe_forward", action_ids)

    def test_diagnostics_marks_corner_risk_failure_point(self):
        state = maze_policy.build_sensor_state(
            tick=20,
            pose=(1.0, 2.0, 0.5),
            goal=(8.0, 2.0),
            clearances=(0.12, 0.09, 0.22, 0.08),
        )
        decision = maze_policy.select_maze_action(state)
        record = maze_diagnostics.diagnostic_record(
            state=state,
            decision=decision,
            movement_delta=0.001,
            contact_streak=1,
            no_progress_streak=2,
            recovery_queue_remaining=0,
            emitted_wheel_velocity={"left": 0.5, "right": 0.1},
            navigation_sensor={
                "maze_map_known": False,
                "target": {"x": 8.0, "y": 2.0},
                "memory_context_key": "sensor:goal:mid:ahead:front:tight:left:tight:right:near:nearest:blocked:stable",
            },
            goal_sensor={"distance": 3.2, "attractor_strength": 0.0},
            learning_outcome={"status": "failure", "action_id": "action:advance"},
            learning_memory={"key": "sensor:goal:mid:ahead", "biases": {"action:advance": -0.44}},
        )

        self.assertEqual("corner_risk", record["failure_label"])
        self.assertTrue(record["flags"]["corner_risk"])
        self.assertTrue(maze_diagnostics.is_failure_point(record))
        self.assertIn("candidate_ranking", record)
        self.assertFalse(record["navigation_sensor"]["maze_map_known"])
        self.assertEqual(3.2, record["goal_sensor"]["distance"])
        self.assertEqual("failure", record["learning_outcome"]["status"])
        self.assertLess(record["learning_memory"]["biases"]["action:advance"], 0.0)

    def test_diagnostics_marks_nominal_clear_motion(self):
        state = maze_policy.build_sensor_state(
            tick=21,
            pose=(1.0, 2.0, 0.0),
            goal=(8.0, 2.0),
            clearances=(0.9, 0.8, 0.8, 0.8),
        )
        decision = maze_policy.select_maze_action(state)
        record = maze_diagnostics.diagnostic_record(
            state=state,
            decision=decision,
            movement_delta=0.02,
            contact_streak=0,
            no_progress_streak=0,
            recovery_queue_remaining=0,
            emitted_wheel_velocity={"left": 2.2, "right": 2.2},
        )

        self.assertEqual("nominal", record["failure_label"])
        self.assertFalse(maze_diagnostics.is_failure_point(record))


if __name__ == "__main__":
    unittest.main()
