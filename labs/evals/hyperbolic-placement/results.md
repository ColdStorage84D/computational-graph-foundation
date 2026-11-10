# Hyperbolic Placement Results

Status: `contract-pass`

Eval layer: `value-over-baseline`

Reviewed date: 2026-11-10

Reviewed command:

```powershell
python -m unittest discover -s labs/evals/hyperbolic-placement -p "test_*.py"
python labs/evals/hyperbolic-placement/comparison.py
```

Reviewed result:

```text
Ran 9 tests
OK
```

## Comparison

No randomness. Both arms place a complete tree with the same rule: a node sits
at the middle of its angular wedge, children share the central half of the
parent's wedge, and radius grows with depth. The baseline measures distance in
the flat plane. The variant reads the radius as hyperbolic distance from the
origin, `ln(2 * branching)` per level, and measures distance in the Poincare
ball.

Failure mode: a hierarchy placed in a flat plane runs out of room at the rim.
Metric: worst-case distortion, the largest stretch times the largest squeeze
over all node pairs. 1.0 is a perfect scaled copy of the tree metric.

| Fixture | Nodes | Euclidean | Hyperbolic |
| --- | --- | --- | --- |
| Binary tree, depth 4 | 31 | 11.6 | 1.40 |
| Binary tree, depth 6 | 127 | 124.1 | 1.40 |
| Ternary tree, depth 4 | 121 | 57.5 | 1.62 |
| 6 by 6 grid, no hierarchy | 36 | 1.41 | 1.43 to 4.33 |

The hyperbolic gain needs radial growth matched to the branching factor. On
the depth-6 binary tree, half the matched radius per level gives distortion
16.8 and twice the matched radius gives 5.9.

Pass thresholds, checked by `test_comparison.py`: hyperbolic distortion stays
under 2.0 on every tree and does not grow with depth, Euclidean distortion
grows more than five-fold from depth 4 to depth 6, and on the grid the flat
plane is better at every disk radius tried.

## Where It Does Not Help

On a grid the flat plane is the right geometry. The hyperbolic placement is
never better there; it only approaches the flat result when the grid is
squeezed into the nearly flat centre of the ball. On trees the result depends
on choosing the radius per level correctly.

Claim boundary: complete trees placed by one deterministic rule, with the same
rule used in both geometries. The Euclidean arm is that rule's flat reading,
not the best possible flat embedding. The result does not claim learned
embeddings, behaviour on irregular hierarchies, or retrieval performance.
