import json
import math
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

from abb_webots_ik_adapter import RelativeTarget, WebotsIkAdapter, _ikpy_major_version
from industrial_robot_arm import (
    AXES,
    build_hold_trace_step,
    build_industrial_arm_topology,
    build_reach_trace_step,
    run_offline_demo,
    run_webots_app,
    safety_gate_command,
    summarize_topology,
    validate_trace_step,
    webots_world_path,
    zero_command,
)


APP_DIR = Path(__file__).resolve().parent


class IndustrialRobotArmGraphTests(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = build_industrial_arm_topology()
        self.nodes = self.graph["nodes"]
        self.edges = self.graph["edges"]
        self.summary = summarize_topology(self.graph)

    def test_topology_has_six_axis_contract(self):
        self.assertEqual(6, self.summary["joints"])
        self.assertEqual(6, self.summary["actuators"])
        self.assertEqual(6, self.summary["limits"])
        self.assertIn({"source": "body:tool", "type": "attached_to", "to": "body:flange"}, self.edges)

    def test_each_actuator_drives_one_joint(self):
        actuators = [node["id"] for node in self.nodes if node["type"] == "actuator"]
        self.assertEqual(6, len(actuators))
        for actuator in actuators:
            drives = [edge for edge in self.edges if edge["source"] == actuator and edge["type"] == "drives"]
            self.assertEqual(1, len(drives), actuator)
            self.assertTrue(drives[0]["to"].startswith("joint:"))

    def test_each_axis_has_limit_constraint(self):
        for axis in AXES:
            limit = f"limit:{axis}_range"
            self.assertIn({"source": limit, "type": "constrains", "to": f"joint:{axis}"}, self.edges)
            self.assertIn({"source": limit, "type": "constrains", "to": f"actuator:{axis}"}, self.edges)

    def test_hold_trace_emits_zero_bounded_command(self):
        step = build_hold_trace_step(
            episode_id="hold-test",
            seed=1,
            tick=0,
            graph_summary=self.summary,
        )
        self.assertEqual([], validate_trace_step(step))
        self.assertEqual("action:hold", step["selected_action"])
        self.assertEqual(zero_command(), step["safety_gate"]["emitted_command"])
        self.assertFalse(step["outcome"]["limit_violation"])

    def test_reach_trace_evidence_matches_all_actuators(self):
        command = {axis: 0.01 for axis in AXES}
        gate = safety_gate_command(command)
        step = build_reach_trace_step(
            episode_id="reach-test",
            seed=1,
            tick=1,
            graph_summary=self.summary,
            destination_pose={"x": 1.0, "y": 0.2, "z": 0.8},
            safety_gate=gate,
        )
        self.assertEqual([], validate_trace_step(step))
        evidence_text = json.dumps(step["evidence_paths"])
        for axis in AXES:
            self.assertIn(f"actuator:{axis}", evidence_text)
        self.assertIn("action:bounded_joint_delta", evidence_text)

    def test_safety_gate_clamps_large_command(self):
        command = {axis: 1.0 for axis in AXES}
        gate = safety_gate_command(command, previous=zero_command(), max_joint_step_rad=0.15)
        self.assertEqual("clamp", gate["outcome"])
        self.assertEqual(0.15, gate["emitted_command"]["axis_1"])

    def test_safety_gate_blocks_invalid_command(self):
        command = {axis: 0.0 for axis in AXES}
        command["axis_2"] = math.inf
        gate = safety_gate_command(command)
        self.assertEqual("block", gate["outcome"])
        self.assertEqual(zero_command(), gate["emitted_command"])

    def test_training_labels_are_marked_training_only(self):
        step = build_hold_trace_step(
            episode_id="label-test",
            seed=2,
            tick=0,
            graph_summary=self.summary,
        )
        self.assertTrue(step["training_labels"]["training_only"])

    def test_offline_runner_writes_jsonl_trace(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = run_offline_demo(seed=3, max_ticks=3, trace_dir=tmp)
            self.assertEqual(3, report.ticks)
            lines = report.trace_path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(3, len(lines))
            steps = [json.loads(line) for line in lines]
            self.assertEqual("action:hold", steps[0]["selected_action"])
            self.assertEqual("clamp", steps[2]["safety_gate"]["outcome"])

    def test_webots_app_skips_or_reports_available(self):
        result = run_webots_app(seed=0, max_ticks=1)
        self.assertIn(result["status"], {"skipped", "available"})
        self.assertIn("claim", result)
        self.assertTrue(str(result["world"]).endswith("inverse_kinematics.wbt"))

    def test_webots_app_uses_abb_sample_world(self):
        world = webots_world_path()
        controller = (
            APP_DIR
            / "main"
            / "controllers"
            / "abb_irb_4600_controller"
            / "abb_irb_4600_controller.py"
        )
        world_text = world.read_text(encoding="utf-8")

        self.assertTrue(world.exists())
        self.assertTrue(controller.exists())
        self.assertIn("Irb4600-40", world_text)
        self.assertIn('controller "abb_irb_4600_controller"', world_text)
        self.assertIn("DEF TARGET Solid", world_text)
        self.assertIn("Pen {", world_text)
        self.assertIn("build_reach_trace_step", controller.read_text(encoding="utf-8"))
        self.assertFalse((APP_DIR / "index.html").exists())
        self.assertFalse((APP_DIR / "demo.js").exists())
        self.assertFalse((APP_DIR / "styles.css").exists())

    def test_webots_adapter_is_section_local(self):
        adapter = (APP_DIR / "abb_webots_ik_adapter.py").read_text(encoding="utf-8")

        self.assertIn("class WebotsIkAdapter", adapter)
        self.assertIn("DEF TARGET", adapter)
        self.assertIn("target_deadband_m", adapter)
        self.assertIn("replan_interval", adapter)
        self.assertIn("inverse_kinematics", webots_world_path().name)

    def test_ik_adapter_reuses_cached_command_inside_target_deadband(self):
        adapter = WebotsIkAdapter.__new__(WebotsIkAdapter)
        adapter.cached_goal_command = zero_command()
        adapter.last_target = RelativeTarget(1.0, 2.0, 3.0)
        adapter.target_deadband_m = 0.05
        adapter.replan_interval = 8
        adapter.ticks_since_replan = 2

        self.assertFalse(adapter._should_replan(RelativeTarget(1.01, 2.0, 3.0)))
        self.assertTrue(adapter._should_replan(RelativeTarget(1.10, 2.0, 3.0)))

    def test_ik_adapter_replans_after_interval_even_if_target_stable(self):
        adapter = WebotsIkAdapter.__new__(WebotsIkAdapter)
        adapter.cached_goal_command = zero_command()
        adapter.last_target = RelativeTarget(1.0, 2.0, 3.0)
        adapter.target_deadband_m = 0.05
        adapter.replan_interval = 8
        adapter.ticks_since_replan = 8

        self.assertTrue(adapter._should_replan(RelativeTarget(1.0, 2.0, 3.0)))

    def test_ik_adapter_acceleration_limits_joint_delta(self):
        adapter = WebotsIkAdapter.__new__(WebotsIkAdapter)
        adapter.max_joint_step_rad = 0.15
        adapter.max_joint_accel_step_rad = 0.04
        adapter.last_command_delta = {axis: 0.0 for axis in AXES}
        previous = zero_command()
        command = {axis: 1.0 for axis in AXES}

        emitted, clamped = adapter._smooth_rate_limited_command(command, previous)
        self.assertTrue(clamped)
        self.assertAlmostEqual(0.04, emitted["axis_1"])

        emitted_next, clamped_next = adapter._smooth_rate_limited_command(command, emitted)
        self.assertTrue(clamped_next)
        self.assertAlmostEqual(0.12, emitted_next["axis_1"])

    def test_ikpy_major_version_is_compared_numerically(self):
        self.assertEqual(3, _ikpy_major_version("3.0.1"))
        self.assertEqual(10, _ikpy_major_version("10.0"))
        with self.assertRaises(RuntimeError):
            _ikpy_major_version("unknown")

    def test_ik_adapter_removes_temporary_urdf(self):
        observed: dict[str, object] = {}

        class FakeChain:
            @staticmethod
            def from_urdf_file(filename, *, active_links_mask):
                observed["exists_during_parse"] = Path(filename).exists()
                observed["filename"] = filename
                observed["mask"] = active_links_mask
                return "chain"

        fake_ikpy = types.ModuleType("ikpy")
        fake_ikpy.__version__ = "10.0"
        fake_chain = types.ModuleType("ikpy.chain")
        fake_chain.Chain = FakeChain
        adapter = WebotsIkAdapter.__new__(WebotsIkAdapter)
        adapter.supervisor = types.SimpleNamespace(getUrdf=lambda: "<robot />")

        with patch.dict(sys.modules, {"ikpy": fake_ikpy, "ikpy.chain": fake_chain}):
            self.assertEqual("chain", adapter._chain_from_supervisor_urdf())

        self.assertTrue(observed["exists_during_parse"])
        self.assertFalse(Path(str(observed["filename"])).exists())

    def test_webots_controller_does_not_auto_quit_by_default(self):
        controller = (
            APP_DIR
            / "main"
            / "controllers"
            / "abb_irb_4600_controller"
            / "abb_irb_4600_controller.py"
        ).read_text(encoding="utf-8")

        self.assertIn('os.environ.get("CGF_ABB_IRB_4600_MAX_TICKS", "0")', controller)
        self.assertIn('auto_quit = _env_flag("CGF_WEBOTS_AUTO_QUIT")', controller)
        self.assertIn("if auto_quit:", controller)
        self.assertIn("supervisor.simulationQuit(0)", controller)

    def test_webots_controller_records_ik_temporal_coherence_metadata(self):
        controller = (
            APP_DIR
            / "main"
            / "controllers"
            / "abb_irb_4600_controller"
            / "abb_irb_4600_controller.py"
        ).read_text(encoding="utf-8")

        self.assertIn('"mode": "ik_temporal_coherence"', controller)
        self.assertIn('"replanned": result["replanned"]', controller)
        self.assertIn('"ticks_since_replan": result["ticks_since_replan"]', controller)


if __name__ == "__main__":
    unittest.main()
