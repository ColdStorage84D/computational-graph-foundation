"""Value-over-baseline comparison for frame-aware comparison of local values.

Failure mode: neighbours report the same quantity in different local frames,
and their coordinates are compared directly.

Task: on a ring of nodes, flag the edges where the two endpoints genuinely
disagree. Baseline: compare raw local coordinates. Variant: transport one
endpoint into the other's frame with the declared map, then compare, using
`transport_state` and `score_residual` from `eval.py`.

Four regimes: frames differ and the declared maps are right; all frames are
the same, where transport has nothing to add; each map carries its own error,
where transport degrades and the loop holonomy says so; and every frame is
misdeclared consistently, where transport degrades and holonomy stays silent.
"""

from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path
import random
import sys


def _load_eval():
    name = "cgf_gauge_transport_eval"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name("eval.py"))
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ev = _load_eval()

NODES = 24
ANOMALIES = 3
NOISE = 0.02
THRESHOLD = 0.25


def rotation(angle: float):
    return ((math.cos(angle), -math.sin(angle)), (math.sin(angle), math.cos(angle)))


def rotate(angle: float, vector):
    matrix = rotation(angle)
    return tuple(sum(a * b for a, b in zip(row, vector)) for row in matrix)


def build_ring(
    rng: random.Random, *, frame_spread: float, node_error: float = 0.0, edge_error: float = 0.0
):
    """Local observations, declared transports, and which edges truly disagree.

    `node_error` misdeclares each frame once, so the maps stay consistent with
    each other. `edge_error` perturbs each map independently.
    """

    frames = [ev.declare_frame(f"frame:{index}", ("u", "v")) for index in range(NODES)]
    true_angles = [rng.uniform(-frame_spread, frame_spread) for _ in range(NODES)]
    declared_angles = [angle + rng.gauss(0.0, node_error) for angle in true_angles]
    anomalous = set(rng.sample(range(NODES), ANOMALIES))
    shared = (1.0, 0.0)
    values, local = [], []
    for index in range(NODES):
        value = rotate(rng.uniform(1.0, 2.5), shared) if index in anomalous else shared
        values.append(value)
        noisy = (value[0] + rng.gauss(0.0, NOISE), value[1] + rng.gauss(0.0, NOISE))
        # Coordinates of the global value in this node's own frame.
        local.append(rotate(-true_angles[index], noisy))
    transports = []
    for index in range(NODES):
        following = (index + 1) % NODES
        angle = declared_angles[index] - declared_angles[following] + rng.gauss(0.0, edge_error)
        transports.append(
            ev.TransportMap(f"transport:{index}", frames[index], frames[following], rotation(angle))
        )
    # Ground truth is read in the global frame, before noise.
    truth = [
        ev.score_residual(values[index], values[(index + 1) % NODES]) > THRESHOLD
        for index in range(NODES)
    ]
    return local, transports, truth


def _score(flags: list[bool], truth: list[bool]) -> dict[str, int]:
    return {
        "true_positive": sum(f and t for f, t in zip(flags, truth)),
        "false_positive": sum(f and not t for f, t in zip(flags, truth)),
        "false_negative": sum(t and not f for f, t in zip(flags, truth)),
    }


def run_regime(
    *,
    frame_spread: float,
    node_error: float = 0.0,
    edge_error: float = 0.0,
    seed: int = 20260104,
    rings: int = 200,
):
    rng = random.Random(seed)
    totals = {
        "raw": {"true_positive": 0, "false_positive": 0, "false_negative": 0},
        "transported": {"true_positive": 0, "false_positive": 0, "false_negative": 0},
    }
    holonomy = 0.0
    for _ in range(rings):
        local, transports, truth = build_ring(
            rng, frame_spread=frame_spread, node_error=node_error, edge_error=edge_error
        )
        raw_flags, transported_flags = [], []
        for index in range(NODES):
            following = (index + 1) % NODES
            raw_flags.append(ev.score_residual(local[index], local[following]) > THRESHOLD)
            moved = ev.transport_state(local[index], transports[index])
            transported_flags.append(ev.score_residual(moved, local[following]) > THRESHOLD)
        for arm, flags in (("raw", raw_flags), ("transported", transported_flags)):
            for key, value in _score(flags, truth).items():
                totals[arm][key] += value
        holonomy += ev.detect_holonomy(tuple(transports), (1.0, 0.0))
    report = {}
    for arm, counts in totals.items():
        flagged = counts["true_positive"] + counts["false_positive"]
        actual = counts["true_positive"] + counts["false_negative"]
        report[arm] = {
            "precision": round(counts["true_positive"] / flagged, 4) if flagged else None,
            "recall": round(counts["true_positive"] / actual, 4) if actual else None,
            "false_positive_edges_per_ring": round(counts["false_positive"] / rings, 3),
        }
    report["mean_loop_holonomy"] = round(holonomy / rings, 6)
    return report


def run_comparison(*, seed: int = 20260104, rings: int = 200) -> dict[str, object]:
    return {
        "seed": seed,
        "rings_per_regime": rings,
        "nodes_per_ring": NODES,
        "frames_differ": run_regime(frame_spread=math.pi, seed=seed, rings=rings),
        "frames_aligned": run_regime(frame_spread=0.0, seed=seed, rings=rings),
        "independent_map_errors": run_regime(
            frame_spread=math.pi, edge_error=0.3, seed=seed, rings=rings
        ),
        "consistent_frame_errors": run_regime(
            frame_spread=math.pi, node_error=0.3, seed=seed, rings=rings
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run_comparison(), indent=2))
