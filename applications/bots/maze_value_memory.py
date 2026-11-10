"""Small maze value-memory example for CGF bot applications.

The example is intentionally dependency-free. It shows graph runtime memory as
future behavior change: blocked edges and cost-to-go values learned in one run
affect the next run.
"""

from __future__ import annotations

from dataclasses import dataclass, field


Cell = tuple[int, int]
GOAL: Cell = (2, 0)

GRAPH: dict[Cell, tuple[Cell, ...]] = {
    (0, 0): ((1, 0), (0, 1)),
    (1, 0): ((2, 0), (1, 1)),
    (0, 1): ((1, 1),),
    (1, 1): ((2, 1),),
    (2, 1): ((2, 0),),
    (2, 0): (),
}

TRUE_BLOCKED: set[frozenset[Cell]] = {frozenset(((1, 0), (2, 0)))}


def edge(a: Cell, b: Cell) -> frozenset[Cell]:
    return frozenset((a, b))


def manhattan(cell: Cell, goal: Cell = GOAL) -> float:
    return float(abs(cell[0] - goal[0]) + abs(cell[1] - goal[1]))


@dataclass
class ValueMemory:
    """Learned cost-to-go and reachability memory over a tiny cell graph."""

    values: dict[Cell, float] = field(default_factory=dict)
    open_edges: set[frozenset[Cell]] = field(default_factory=set)
    blocked_edges: set[frozenset[Cell]] = field(default_factory=set)
    graph: dict[Cell, tuple[Cell, ...]] = field(default_factory=lambda: GRAPH)
    goal: Cell = GOAL

    def value(self, cell: Cell) -> float:
        return self.values.get(cell, manhattan(cell, self.goal))

    def mark_open(self, a: Cell, b: Cell) -> None:
        self.open_edges.add(edge(a, b))
        self.blocked_edges.discard(edge(a, b))

    def mark_blocked(self, a: Cell, b: Cell) -> None:
        self.blocked_edges.add(edge(a, b))

    def reachable_neighbors(self, cell: Cell) -> tuple[Cell, ...]:
        return tuple(
            neighbor for neighbor in self.graph[cell] if edge(cell, neighbor) not in self.blocked_edges
        )

    def backup(self, cell: Cell) -> float:
        successors = self.reachable_neighbors(cell)
        if not successors:
            updated = self.value(cell) + 10.0
        else:
            updated = max(self.value(cell), min(1.0 + self.value(neighbor) for neighbor in successors))
        self.values[cell] = updated
        return updated

    def choose_neighbor(self, cell: Cell) -> Cell:
        successors = self.reachable_neighbors(cell)
        if not successors:
            return cell
        return min(successors, key=lambda neighbor: (1.0 + self.value(neighbor), neighbor))


def run_episode(
    memory: ValueMemory,
    *,
    max_steps: int = 12,
    start: Cell = (0, 0),
    true_blocked: set[frozenset[Cell]] | None = None,
) -> dict[str, object]:
    """Run one local greedy episode with online memory update.

    The world is the graph and goal held by `memory` plus `true_blocked`, the
    edges that are really closed. The agent only learns an edge is closed by
    trying it.
    """

    blocked_in_world = TRUE_BLOCKED if true_blocked is None else true_blocked
    cell = start
    steps = 0
    path = [cell]
    blocked_discoveries = 0
    while cell != memory.goal and steps < max_steps:
        steps += 1
        candidate = memory.choose_neighbor(cell)
        if edge(cell, candidate) in blocked_in_world:
            memory.mark_blocked(cell, candidate)
            memory.backup(cell)
            blocked_discoveries += 1
            continue
        memory.mark_open(cell, candidate)
        memory.backup(cell)
        cell = candidate
        path.append(cell)
    return {
        "reached": cell == memory.goal,
        "steps": steps,
        "path": path,
        "blocked_discoveries": blocked_discoveries,
        "learned_values": dict(memory.values),
        "blocked_edges": [tuple(sorted(item)) for item in memory.blocked_edges],
    }
