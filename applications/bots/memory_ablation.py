"""Memory ablation for the maze value-memory example.

Question: does graph runtime memory carried from one run to the next change
later behaviour, and by how much?

Both arms run the same local greedy controller from `maze_value_memory.py` on
the same seeded mazes. The controller cannot see walls; it learns a wall by
bumping into it. One arm keeps its `ValueMemory` across episodes. The other
starts every episode with an empty one.

Two regimes. In the first the maze stays the same between episodes. In the
second the walls are redrawn before every episode, so remembered walls and
remembered costs describe a maze that no longer exists.

This is a synthetic fixture. It measures this controller on these mazes and
nothing else.
"""

from __future__ import annotations

from collections import deque
import json
import random

from maze_value_memory import Cell, ValueMemory, edge, run_episode

SIDE = 6
WALL_RATE = 0.30
EPISODES = 6
MAX_STEPS = 400
START: Cell = (0, 0)
GOAL: Cell = (SIDE - 1, SIDE - 1)


def open_grid(side: int = SIDE) -> dict[Cell, tuple[Cell, ...]]:
    graph = {}
    for x in range(side):
        for y in range(side):
            graph[(x, y)] = tuple(
                (x + dx, y + dy)
                for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1))
                if 0 <= x + dx < side and 0 <= y + dy < side
            )
    return graph


def shortest_path(graph: dict[Cell, tuple[Cell, ...]], walls: set[frozenset[Cell]]) -> int | None:
    seen = {START: 0}
    queue = deque([START])
    while queue:
        cell = queue.popleft()
        if cell == GOAL:
            return seen[cell]
        for neighbour in graph[cell]:
            if neighbour not in seen and edge(cell, neighbour) not in walls:
                seen[neighbour] = seen[cell] + 1
                queue.append(neighbour)
    return None


def draw_walls(rng: random.Random, graph: dict[Cell, tuple[Cell, ...]]) -> set[frozenset[Cell]]:
    """Random walls, redrawn until the goal is reachable."""

    edges = sorted({tuple(sorted((cell, neighbour))) for cell in graph for neighbour in graph[cell]})
    while True:
        walls = {edge(a, b) for a, b in edges if rng.random() < WALL_RATE}
        if shortest_path(graph, walls) is not None:
            return walls


def run_maze(rng: random.Random, *, walls_change: bool) -> dict[str, dict[str, float]]:
    graph = open_grid()
    schedule = [draw_walls(rng, graph)]
    for _ in range(EPISODES - 1):
        schedule.append(draw_walls(rng, graph) if walls_change else schedule[0])
    results = {}
    for arm in ("memory_kept", "memory_reset"):
        memory = ValueMemory(graph=graph, goal=GOAL)
        first = last = None
        for walls in schedule:
            if arm == "memory_reset":
                memory = ValueMemory(graph=graph, goal=GOAL)
            last = run_episode(memory, max_steps=MAX_STEPS, start=START, true_blocked=walls)
            first = first or last
        results[arm] = {
            "first_steps": float(first["steps"]),
            "last_steps": float(last["steps"]),
            "last_reached": float(bool(last["reached"])),
            "last_bumps": float(last["blocked_discoveries"]),
        }
    results["shortest_last"] = {"steps": float(shortest_path(graph, schedule[-1]))}
    return results


def run_regime(*, walls_change: bool, seed: int = 20260106, mazes: int = 300) -> dict[str, object]:
    rng = random.Random(seed)
    totals: dict[str, dict[str, float]] = {}
    for _ in range(mazes):
        for arm, values in run_maze(rng, walls_change=walls_change).items():
            bucket = totals.setdefault(arm, {})
            for key, value in values.items():
                bucket[key] = bucket.get(key, 0.0) + value
    report: dict[str, object] = {
        "mean_shortest_path_last_episode": round(totals["shortest_last"]["steps"] / mazes, 2)
    }
    for arm in ("memory_kept", "memory_reset"):
        report[arm] = {
            "mean_steps_first_episode": round(totals[arm]["first_steps"] / mazes, 2),
            "mean_steps_last_episode": round(totals[arm]["last_steps"] / mazes, 2),
            "mean_wall_bumps_last_episode": round(totals[arm]["last_bumps"] / mazes, 2),
            "reached_goal_last_episode": round(totals[arm]["last_reached"] / mazes, 4),
        }
    return report


def run_ablation(*, seed: int = 20260106, mazes: int = 300) -> dict[str, object]:
    return {
        "seed": seed,
        "mazes_per_regime": mazes,
        "grid_side": SIDE,
        "episodes_per_maze": EPISODES,
        "step_budget": MAX_STEPS,
        "same_maze_every_episode": run_regime(walls_change=False, seed=seed, mazes=mazes),
        "walls_redrawn_every_episode": run_regime(walls_change=True, seed=seed, mazes=mazes),
    }


if __name__ == "__main__":
    print(json.dumps(run_ablation(), indent=2))
