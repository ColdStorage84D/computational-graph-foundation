# Maze Graph Memory Bot

Maze Graph Memory Bot is the Webots application for the public Graph Memory Bot
controller skeleton.

It uses the shipped branching-maze Webots scene: a Pioneer3at robot starts in
the bottom-right start area, receives graph-selected wheel commands, and writes
the CGF trace while it moves through the maze.

```text
Webots sensor tick
-> Graph Memory Bot candidate actions
-> predicted outcomes
-> safety / policy gate
-> selected wheel command
-> Webots robot step
-> trace and graph runtime memory update
```

The maze is an application fixture. The reusable concept remains
[../bots/README.md](../bots/README.md).

The world includes the Pioneer3at robot, start and goal markers, lidar, GPS,
compass, and a 68-wall branching maze. The controller is CGF-native and drives
the same four-wheel Pioneer motor layout used by that world.

The Webots controller does not replay the generic offline bot ticks directly.
It reads the live maze sensors, builds a maze graph state, scores candidate
wheel actions, applies clearance and anti-spin gates, and writes the selected
command plus rejected alternatives to the trace.

The controller also keeps action-outcome memory during a run. If an action
repeatedly fails under the same live sensor context, later scoring penalizes
that action and raises alternative escape or arc actions. The context key is
made from goal distance/bearing plus lidar clearances; it is not a maze map or
spatial coordinate bucket. This memory is in-run by default so a bad
exploratory run cannot poison the next reset.

The controller does not contain a precomputed maze solution or solved map. Each
tick reads the goal marker as a sensor target, combines it with GPS, compass,
and lidar clearances, and then lets the local action graph choose a wheel
command. The goal sensor exposes distance, bearing error, alignment, attractor
strength, and inside-goal-radius state. Near the marker this sensor becomes an
attractor that pulls the bot onto the marker. Hold is only allowed inside the
tight final-goal radius, so being beside the green marker keeps producing a
goal-attractor drive command.

If GPS movement stalls while the robot is close to a wall, the controller
switches through a visible recovery sequence: reverse out of contact, rotate
toward the clearer side, then probe forward before returning to normal graph
action selection.

For tight corner traps, the recovery plan is stricter: if lidar reports that
front, left, right, and nearest clearances are all boxed in, the controller uses
a deeper reverse and clearer-side rotation, and it refuses to probe forward
until front clearance is safe.

For the Pioneer3at maze world, the controller also applies a configurable
compass-to-GPS yaw offset. The goal marker is read by DEF name as a Webots
sensor target; `CGF_MAZE_GRAPH_MEMORY_GOAL_XY` is only a fallback if the marker
cannot be read.

## Run

Open the Webots world:

```text
applications/maze-graph-memory-bot/main/worlds/maze_graph_memory.wbt
```

The controller is:

```text
applications/maze-graph-memory-bot/main/controllers/maze_graph_memory_controller/maze_graph_memory_controller.py
```

From the repository root, run the app tests:

```powershell
python -m unittest discover -s applications/maze-graph-memory-bot -p "test_*.py"
```

Batch smoke run:

```powershell
$env:CGF_WEBOTS_AUTO_QUIT = "1"
$env:CGF_MAZE_GRAPH_MEMORY_MAX_TICKS = "10"
webots --batch --mode=fast --no-rendering --stdout --stderr applications/maze-graph-memory-bot/main/worlds/maze_graph_memory.wbt
```

When opened normally in the Webots GUI, the controller does not call
`simulationQuit()`. It keeps stepping until Webots is stopped. Use
`CGF_WEBOTS_AUTO_QUIT=1` only for bounded batch smoke runs.

## Failure Diagnostics

Each Webots run writes local diagnostics under:

```text
applications/maze-graph-memory-bot/main/runtime/
```

The runtime folder is ignored and should not be committed. The useful files
are:

- `maze_graph_memory_webots_trace.jsonl`: every graph decision, selected wheel
  command, rejected alternatives, movement delta, navigation sensor state, and
  recovery state;
- `maze_graph_memory_diagnostics.jsonl`: every tick with pose, yaw, goal,
  lidar clearances, candidate ranking, selected action, emitted wheel velocity,
  navigation sensor reading, goal sensor reading, and failure flags;
- `maze_graph_memory_failure_points.jsonl`: only non-nominal ticks, so corner
  traps and stalls can be inspected quickly.
- `maze_graph_memory_learning.json`: local action-outcome memory snapshot for
  inspection. It is not loaded on reset unless
  `CGF_MAZE_GRAPH_MEMORY_PERSIST_LEARNING=1` is set.

Failure labels include `corner_risk`, `front_blocked`, `wall_hugging`,
`no_progress`, `no_progress_streak_active`, `spin_risk`, and
`recovery_active`.

For isolated batch debugging while a Webots GUI session is open, set:

```powershell
$env:CGF_MAZE_GRAPH_MEMORY_RUNTIME_DIR = "$env:TEMP\cgf-maze-runtime"
```

## Claim Boundary

This is a Webots graph-action fixture. It does not claim autonomous robot
performance, guaranteed maze solving, robotics benchmark success, production
safety, or biological plausibility.
