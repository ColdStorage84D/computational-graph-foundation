# Forkable Demo Guide

Use this guide when you want a small CGF demo that another developer can fork
without needing private context or unsupported claims. Webots demos are included
where the app is explicitly simulator-shaped.

The recommended path is:

```text
Signal Review -> Medical Image Analysis -> Graph Memory Bot
```

Each demo is an application of reusable CGF Architecture concepts. The
applications do not own the concepts; they show how to compose them.

## 1. Signal Review

Start here when you want the cleanest forkable contract demo.

- App: [signal-review/README.md](signal-review/README.md)
- Eval: [../labs/evals/signal-review/results.md](../labs/evals/signal-review/results.md)
- Reusable card: [../architecture/frameworks/cards/signal-review-framework.md](../architecture/frameworks/cards/signal-review-framework.md)

Use it to show:

```text
signal packet
-> feature views
-> route-specific processors
-> competing proposals
-> verifier / review / abstain
-> traceable signal decision
```

Claim boundary: synthetic contract demo only. It does not claim financial
advice, market prediction, anomaly-detection performance, reliability
improvement, or domain generalization.

## 2. Medical Image Analysis

Use this as the clearest story for Granular Analysis:

```text
one case -> many lenses -> many proposals -> verifier -> review / abstain
```

- App: [medical-image-analysis/README.md](medical-image-analysis/README.md)
- Walkthrough: [medical-image-analysis/walkthrough.md](medical-image-analysis/walkthrough.md)
- Claim boundary: [medical-image-analysis/claim-boundary.md](medical-image-analysis/claim-boundary.md)
- Reusable concept: [../architecture/granular-analysis.md](../architecture/granular-analysis.md)

Claim boundary: review-shape example only. It does not make a medical,
clinical, diagnostic, safety, or model-performance claim.

## 3. Graph Memory Bot

Use this when you want the technical action-and-memory story:

```text
input / sensor state
-> candidate actions
-> predicted outcomes
-> gates
-> selected action
-> trace
-> observed outcome
-> graph runtime memory
```

- Graph Memory Bot: [bots/README.md](bots/README.md)
- Generalized runner: [bots/graph_memory_bot.py](bots/graph_memory_bot.py)
- Webots maze app: [maze-graph-memory-bot/README.md](maze-graph-memory-bot/README.md)
- Bot route growth walkthrough: [bots/provisional-growth-example.md](bots/provisional-growth-example.md)
- Owning Architecture: [../architecture/cortical-column-world-model.md](../architecture/cortical-column-world-model.md)
- Predictive Action Graph: [../architecture/predictive-action-graph.md](../architecture/predictive-action-graph.md)
- Graph runtime memory: [../architecture/graph-runtime-memory.md](../architecture/graph-runtime-memory.md)
- Provisional Graph Growth: [../architecture/provisional-graph-growth.md](../architecture/provisional-graph-growth.md)

Claim boundary: graph action and memory skeleton only. It does not claim
autonomous bot performance, benchmark success, guaranteed maze solving,
robotics performance, AGI, or biological cortex.

Use the route-growth walkthrough when the story is about a bot learning that an
unknown pattern needs a new route. It is backed only by the tiny CGF-local
[Provisional Graph Growth eval](../labs/evals/provisional-graph-growth/results.md).

## 4. Industrial Robot Arm Graph

Use this when you want the clearest robot safety-gate story:

```text
six-axis topology
-> action candidate
-> safety gate
-> emitted command
-> evidence paths
-> trace
```

- App: [industrial-robot-arm/README.md](industrial-robot-arm/README.md)
- Webots world: [industrial-robot-arm/main/worlds/inverse_kinematics.wbt](industrial-robot-arm/main/worlds/inverse_kinematics.wbt)
- Claim boundary: [industrial-robot-arm/claim-boundary.md](industrial-robot-arm/claim-boundary.md)

Claim boundary: Webots graph-control demo only. It does not claim real robot
safety, manufacturing readiness, simulator benchmark performance, vendor
accuracy, or autonomous industrial control.

The Webots IK adapter uses temporal coherence to reduce jerky motion: it
reuses a cached IK command while the target is stable, replans when the target
moves or the interval expires, and applies joint step plus acceleration limits.
This keeps the app reactive without turning it into a fixed replay.

For Webots batch smoke runs, set `CGF_WEBOTS_AUTO_QUIT=1` and a small app
tick budget. For normal GUI use, leave auto-quit unset so Webots remains open.

## Recommended Checks

Run the dependency-light demos first:

```powershell
python -m unittest discover -s applications/bots -p "test_*.py"
python -m unittest discover -s applications/maze-graph-memory-bot -p "test_*.py"
python -m unittest discover -s applications/industrial-robot-arm -p "test_*.py"
python -m unittest discover -s applications/medical-image-analysis -p "test_*.py"
python -m unittest discover -s labs/evals/signal-review -p "test_*.py"
python -m unittest discover -s labs/evals/evidence-graph-triage -p "test_*.py"
```

Run the generalized Graph Memory Bot tests:

```powershell
python -m unittest discover -s applications/bots -p "test_*.py"
```
