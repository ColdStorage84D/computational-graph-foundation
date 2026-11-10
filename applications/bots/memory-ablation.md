# Memory Ablation

This page records what graph runtime memory is worth in the maze value-memory
example, measured by removing it.

Reviewed date: 2026-11-10

Reviewed command:

```powershell
python applications/bots/memory_ablation.py
python -m unittest discover -s applications/bots -p "test_*.py"
```

## Setup

The controller in [maze_value_memory.py](maze_value_memory.py) moves greedily
on a 6 by 6 grid toward the opposite corner. It cannot see walls. It learns a
wall by bumping into it, and it backs up a cost-to-go value at every step.

Both arms run that same controller on the same 300 seeded mazes for six
episodes each, with a budget of 400 steps per episode. About 30% of the edges
are walls, redrawn until the goal is reachable.

- `memory_kept`: one `ValueMemory` is carried across all six episodes.
- `memory_reset`: every episode starts with an empty `ValueMemory`.

A bump counts as a step.

## Result

Seed 20260106.

The maze is the same in every episode. The shortest path averages 10.24 steps.

| Arm | Steps, first episode | Steps, sixth episode | Wall bumps, sixth episode | Reached goal |
| --- | --- | --- | --- | --- |
| Memory kept | 26.69 | 10.24 | 0.00 | 100% |
| Memory reset | 26.69 | 26.69 | 5.35 | 100% |

The walls are redrawn before every episode.

| Arm | Steps, first episode | Steps, sixth episode | Wall bumps, sixth episode | Reached goal |
| --- | --- | --- | --- | --- |
| Memory kept | 27.56 | 398.76 | 0.54 | 0.3% |
| Memory reset | 27.56 | 26.33 | 5.31 | 100% |

## Where It Does Not Help

Memory helps only while the world it describes still exists. This controller
never forgets a wall and never lowers a learned cost. After five episodes of
different walls it believes the goal is unreachable and spends its whole budget
without arriving. Keeping memory is then far worse than having none.

That is why the Architecture pattern treats decay, expiry, and outcome-coupled
update as part of memory and not as an optional extra. See
[graph-runtime-memory.md](../../architecture/graph-runtime-memory.md) and
[memory-outcome-feedback.md](../../architecture/memory-outcome-feedback.md).

## Claim Boundary

One small controller on synthetic 6 by 6 mazes. The result measures the effect
of carrying this controller's memory between episodes in a stable and in a
changing maze. It does not measure the Webots maze application, any robot, or
any other memory design, and it is not a navigation benchmark.
