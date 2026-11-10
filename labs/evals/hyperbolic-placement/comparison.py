"""Value-over-baseline comparison for hyperbolic placement of a hierarchy.

Failure mode: a tree is placed in a flat plane, where there is not enough room
at the rim, so unrelated leaves end up closer than parent and child.

Both arms use the same layout rule: a node sits at the middle of its angular
wedge, children share the central part of the parent's wedge, and radius grows
with depth. The baseline measures distance in the Euclidean plane. The variant
reads the same radius as hyperbolic distance from the origin and measures
distance with `poincare_distance` from `eval.py`.

A second fixture is a square grid, which has no hierarchy. There the flat plane
is the right geometry and the hyperbolic placement should lose.
"""

from __future__ import annotations

from collections import deque
import importlib.util
import json
import math
from pathlib import Path
import sys


def _load_eval():
    name = "cgf_hyperbolic_placement_eval"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name("eval.py"))
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ev = _load_eval()

Adjacency = dict[str, tuple[str, ...]]
WEDGE_SHARE = 0.5  # children use this central share of the parent's wedge


def complete_tree(branching: int, depth: int) -> tuple[Adjacency, dict[str, tuple[int, float]]]:
    """Adjacency plus (depth, angle) for every node of a complete tree."""

    children: dict[str, list[str]] = {"r": []}
    polar: dict[str, tuple[int, float]] = {"r": (0, 0.0)}
    frontier = [("r", 0.0, 2.0 * math.pi)]
    for level in range(1, depth + 1):
        following = []
        for name, low, high in frontier:
            width = high - low
            share = 1.0 if level == 1 else WEDGE_SHARE
            start = low + 0.5 * width * (1.0 - share)
            slot = width * share / branching
            for index in range(branching):
                child = f"{name}.{index}"
                child_low = start + index * slot
                children[name].append(child)
                children[child] = []
                polar[child] = (level, child_low + 0.5 * slot)
                following.append((child, child_low, child_low + slot))
        frontier = following
    adjacency: dict[str, list[str]] = {name: list(kids) for name, kids in children.items()}
    for name, kids in children.items():
        for kid in kids:
            adjacency[kid].append(name)
    return {name: tuple(neighbours) for name, neighbours in adjacency.items()}, polar


def grid(side: int) -> tuple[Adjacency, dict[str, tuple[float, float]]]:
    adjacency: dict[str, list[str]] = {}
    position = {}
    for x in range(side):
        for y in range(side):
            name = f"{x},{y}"
            position[name] = (float(x), float(y))
            adjacency[name] = [
                f"{x + dx},{y + dy}"
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                if 0 <= x + dx < side and 0 <= y + dy < side
            ]
    return {name: tuple(neighbours) for name, neighbours in adjacency.items()}, position


def graph_distances(adjacency: Adjacency) -> dict[tuple[str, str], int]:
    names = sorted(adjacency)
    distances = {}
    for source in names:
        seen = {source: 0}
        queue = deque([source])
        while queue:
            current = queue.popleft()
            for neighbour in adjacency[current]:
                if neighbour not in seen:
                    seen[neighbour] = seen[current] + 1
                    queue.append(neighbour)
        for target in names:
            if source < target:
                distances[(source, target)] = seen[target]
    return distances


def distortion(graph: dict[tuple[str, str], int], embedded: dict[tuple[str, str], float]) -> dict[str, float]:
    """Worst-case and mean distortion. Both ignore overall scale.

    Worst-case is the largest stretch times the largest squeeze over all pairs;
    1.0 means the embedding is a scaled copy of the graph metric.
    """

    ratios = [embedded[pair] / graph[pair] for pair in graph]
    scale = sum(embedded[pair] * graph[pair] for pair in graph) / sum(
        embedded[pair] ** 2 for pair in graph
    )
    mean_error = sum(abs(scale * embedded[pair] - graph[pair]) / graph[pair] for pair in graph) / len(graph)
    return {
        "worst_case_distortion": round(max(ratios) / min(ratios), 3),
        "mean_relative_error": round(mean_error, 4),
    }


def euclidean_tree_distances(polar, radius_per_level: float = 1.0):
    points = {
        name: (radius_per_level * level * math.cos(angle), radius_per_level * level * math.sin(angle))
        for name, (level, angle) in polar.items()
    }
    names = sorted(points)
    return {
        (a, b): ev.euclidean_distance(points[a], points[b])
        for index, a in enumerate(names)
        for b in names[index + 1 :]
    }


def hyperbolic_tree_distances(polar, radius_per_level: float):
    points = {}
    for name, (level, angle) in polar.items():
        radius = math.tanh(0.5 * radius_per_level * level)
        points[name] = (radius * math.cos(angle), radius * math.sin(angle))
    names = sorted(points)
    return {
        (a, b): ev.poincare_distance(points[a], points[b])
        for index, a in enumerate(names)
        for b in names[index + 1 :]
    }


def tree_report(branching: int, depth: int) -> dict[str, object]:
    adjacency, polar = complete_tree(branching, depth)
    graph = graph_distances(adjacency)
    # Radius per level that matches the exponential growth of the layout.
    radius_per_level = math.log(branching / WEDGE_SHARE)
    return {
        "nodes": len(adjacency),
        "radius_per_level": round(radius_per_level, 4),
        "euclidean": distortion(graph, euclidean_tree_distances(polar)),
        "hyperbolic": distortion(graph, hyperbolic_tree_distances(polar, radius_per_level)),
    }


def grid_report(side: int) -> dict[str, object]:
    adjacency, position = grid(side)
    graph = graph_distances(adjacency)
    names = sorted(position)
    flat = {
        (a, b): ev.euclidean_distance(position[a], position[b])
        for index, a in enumerate(names)
        for b in names[index + 1 :]
    }
    centre = 0.5 * (side - 1)
    reach = math.hypot(centre, centre)
    by_radius = {}
    # A small disk radius keeps the grid in the nearly flat centre of the ball.
    for disk_radius in (0.1, 0.5, 0.9):
        placed = {
            name: ((x - centre) / reach * disk_radius, (y - centre) / reach * disk_radius)
            for name, (x, y) in position.items()
        }
        curved = {
            (a, b): ev.poincare_distance(placed[a], placed[b])
            for index, a in enumerate(names)
            for b in names[index + 1 :]
        }
        by_radius[f"disk_radius_{disk_radius}"] = distortion(graph, curved)
    return {
        "nodes": len(adjacency),
        "euclidean": distortion(graph, flat),
        "hyperbolic": by_radius,
    }


def mismatched_radius_report(branching: int, depth: int) -> dict[str, float]:
    """The gain depends on matching radial growth to the branching factor."""

    adjacency, polar = complete_tree(branching, depth)
    graph = graph_distances(adjacency)
    matched = math.log(branching / WEDGE_SHARE)
    return {
        f"radius_per_level_x{factor}": distortion(
            graph, hyperbolic_tree_distances(polar, factor * matched)
        )["worst_case_distortion"]
        for factor in (0.5, 1.0, 2.0)
    }


def run_comparison() -> dict[str, object]:
    return {
        "binary_tree_depth_4": tree_report(2, 4),
        "binary_tree_depth_6": tree_report(2, 6),
        "ternary_tree_depth_4": tree_report(3, 4),
        "binary_tree_depth_6_mismatched_radius": mismatched_radius_report(2, 6),
        "grid_6x6": grid_report(6),
    }


if __name__ == "__main__":
    print(json.dumps(run_comparison(), indent=2))
