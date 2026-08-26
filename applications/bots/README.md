# Graph Memory Bot

This folder contains the canonical CGF bot/controller skeleton.

Graph Memory Bot is generalized. It is not a MazeBot, a Webots controller, or a
simulator dependency. The reusable framework card is
[../../architecture/frameworks/cards/bot-graph-framework.md](../../architecture/frameworks/cards/bot-graph-framework.md).

The public loop is:

```text
input / sensor state
-> candidate actions
-> predicted outcomes
-> safety / policy gate
-> selected action
-> trace
-> observed outcome
-> graph runtime memory update
-> optional provisional route growth
```

The app shows how the Architecture execution graph can support bots through:

- explicit topology;
- brain/spine-style routing;
- candidate actions, predictions, and gates;
- traceable actions;
- graph runtime memory;
- provisional route growth when recurring unknown patterns need review.

## Examples

- [graph_memory_bot.py](graph_memory_bot.py): the generalized stdlib-only bot
  runner. It creates candidate actions, predicts outcomes, applies a visible
  gate, selects an action, observes prediction error, updates graph runtime
  memory, and preserves rejected candidates in the trace.
- [maze_value_memory.py](maze_value_memory.py): local value memory over a small
  maze graph. It is a teaching fixture only. It shows learned reachability and
  cost-to-go memory changing the next run.
- [robot_topology_trace.py](robot_topology_trace.py): robot topology and trace
  contract. It shows sensors, goals, actions, actuators, limits, gates, evidence
  paths, and outcomes.
- [provisional-growth-example.md](provisional-growth-example.md): bot route
  growth walkthrough. It shows known routes, recurring unknown patterns,
  provisional capsules, candidate variants, stability guards, promotion, and
  rollback.
- [provisional_route_growth.py](provisional_route_growth.py): runnable
  stdlib-only version of the route-growth walkthrough. It keeps shadow
  candidates non-authoritative and requires promotion plus rollback before a
  durable route change is trusted.

## Claim Boundary

Graph Memory Bot is a graph-action and memory skeleton only. It does not claim
autonomous bot performance, guaranteed maze solving, robotics benchmark
results, simulator fidelity, or production safety.

## Run

From the repository root:

```powershell
python -m unittest discover -s applications/bots -p "test_*.py"
```

To print the generalized demo trace:

```powershell
python applications/bots/graph_memory_bot.py
```
