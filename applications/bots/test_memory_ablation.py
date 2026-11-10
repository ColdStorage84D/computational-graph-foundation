import random
import unittest

import memory_ablation as ablation
from maze_value_memory import ValueMemory, edge, run_episode


class MemoryAblationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = ablation.run_ablation()

    def test_run_is_deterministic(self):
        self.assertEqual(self.report, ablation.run_ablation())

    def test_generated_mazes_are_solvable_and_hide_their_walls(self):
        rng = random.Random(5)
        graph = ablation.open_grid()
        walls = ablation.draw_walls(rng, graph)
        self.assertIsNotNone(ablation.shortest_path(graph, walls))
        memory = ValueMemory(graph=graph, goal=ablation.GOAL)
        self.assertEqual(memory.blocked_edges, set())
        result = run_episode(memory, max_steps=ablation.MAX_STEPS, start=ablation.START, true_blocked=walls)
        self.assertTrue(result["reached"])
        self.assertTrue(all(edge(*pair) in walls for pair in result["blocked_edges"]))

    def test_both_arms_start_from_the_same_first_episode(self):
        for regime in ("same_maze_every_episode", "walls_redrawn_every_episode"):
            arms = self.report[regime]
            self.assertEqual(
                arms["memory_kept"]["mean_steps_first_episode"],
                arms["memory_reset"]["mean_steps_first_episode"],
            )

    def test_kept_memory_reaches_the_shortest_path_in_a_stable_maze(self):
        stable = self.report["same_maze_every_episode"]
        kept = stable["memory_kept"]
        self.assertEqual(kept["reached_goal_last_episode"], 1.0)
        self.assertEqual(kept["mean_wall_bumps_last_episode"], 0.0)
        self.assertLessEqual(
            kept["mean_steps_last_episode"], 1.05 * stable["mean_shortest_path_last_episode"]
        )

    def test_reset_memory_repeats_the_first_episode(self):
        reset = self.report["same_maze_every_episode"]["memory_reset"]
        self.assertEqual(reset["mean_steps_last_episode"], reset["mean_steps_first_episode"])
        self.assertGreater(reset["mean_wall_bumps_last_episode"], 3.0)
        kept = self.report["same_maze_every_episode"]["memory_kept"]
        self.assertGreater(reset["mean_steps_last_episode"], 2.0 * kept["mean_steps_last_episode"])

    def test_kept_memory_fails_when_the_maze_changes(self):
        changing = self.report["walls_redrawn_every_episode"]
        self.assertLess(changing["memory_kept"]["reached_goal_last_episode"], 0.05)
        self.assertEqual(changing["memory_reset"]["reached_goal_last_episode"], 1.0)


if __name__ == "__main__":
    unittest.main()
