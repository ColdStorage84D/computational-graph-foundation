# Gauge Transport Results

Status: `contract-pass`

Eval layer: `value-over-baseline`

Reviewed date: 2026-11-10

Reviewed command:

```powershell
python -m unittest discover -s labs/evals/gauge-transport -p "test_*.py"
python labs/evals/gauge-transport/comparison.py
```

Reviewed result:

```text
Ran 12 tests
OK
```

## Comparison

Seed 20260104, 200 rings of 24 nodes per regime, three anomalous nodes per
ring. Each node reports a two-dimensional value in its own rotated frame.

Failure mode: neighbours report the same quantity in different frames and
their coordinates are compared directly. Task: flag the edges whose endpoints
genuinely disagree. Metric: precision, recall, and false alarms per ring.

| Regime | Arm | Precision | Recall | False alarms per ring |
| --- | --- | --- | --- | --- |
| Frames differ, maps correct | Raw coordinates (baseline) | 0.235 | 0.923 | 16.96 |
| Frames differ, maps correct | Transported | 1.000 | 0.998 | 0.00 |
| Frames already aligned | Raw coordinates (baseline) | 1.000 | 0.998 | 0.00 |
| Frames already aligned | Transported | 1.000 | 0.998 | 0.00 |
| Each map has its own error | Transported | 0.429 | 0.989 | 7.45 |
| Every frame misdeclared consistently | Transported | 0.354 | 0.989 | 10.20 |

Mean loop holonomy is 0 with correct maps, 1.01 when each map has its own
error, and 0 when every frame is misdeclared consistently.

Pass thresholds, checked by `test_comparison.py`: with differing frames, raw
comparison has precision under 0.30 and transport has no false alarms; with
aligned frames the two arms are identical; with wrong maps transport precision
falls below 0.5.

## Where It Does Not Help

Transport adds nothing when frames already agree. It is only as good as the
declared maps: with errors of 0.3 radians it still raises seven to ten false
alarms per ring. Holonomy detects maps that are inconsistent with each other.
It cannot detect frames that are consistently misdeclared, because those maps
still compose to the identity around every loop.

Claim boundary: planar rotations on a ring, with frames and anomalies set by
the generator. The result covers frame-aware comparison on that fixture. It
does not claim production correspondence construction, domain adapter quality,
or a method for estimating frames.
