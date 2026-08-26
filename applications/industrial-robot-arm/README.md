# Industrial Robot Arm Graph

Industrial Robot Arm Graph is a shipped CGF Webots application for graph-shaped
robot control.

It shows how a six-axis industrial arm can be represented as:

```text
topology graph
-> action candidates
-> safety gate
-> emitted command
-> evidence paths
-> trace
```

The first profile is an ABB IRB 4600-style six-axis arm profile for topology
and joint-limit demonstration. This app is not a certified robot model and does
not control a real robot.

## What It Demonstrates

- body, joint, actuator, sensor, goal, action, and limit nodes;
- declared constraints before command emission;
- hold and reach-pose trace steps;
- allow, clamp, and block safety-gate outcomes;
- evidence paths from goal to selected action to actuators;
- training-only labels kept out of live authority;
- a Webots world and controller that run the graph-control trace.

## Run

Open the Webots world:

```text
applications/industrial-robot-arm/main/worlds/inverse_kinematics.wbt
```

The controller is:

```text
applications/industrial-robot-arm/main/controllers/abb_irb_4600_controller/abb_irb_4600_controller.py
```

From the repository root:

```powershell
python applications/industrial-robot-arm/industrial_robot_arm.py
python -m unittest discover -s applications/industrial-robot-arm -p "test_*.py"
```

The Python entry point reports whether a local Webots executable is available
and prints the command shape for the shipped ABB world.

Batch smoke run:

```powershell
$env:CGF_WEBOTS_AUTO_QUIT = "1"
$env:CGF_ABB_IRB_4600_MAX_TICKS = "10"
webots --batch --mode=fast --no-rendering --stdout --stderr applications/industrial-robot-arm/main/worlds/inverse_kinematics.wbt
```

When opened normally in the Webots GUI, the controller does not call
`simulationQuit()`. It keeps stepping until Webots is stopped. Use
`CGF_WEBOTS_AUTO_QUIT=1` only for bounded batch smoke runs.

The world uses Webots' ABB `Irb4600-40` robot, a `DEF TARGET` node, and a pen
tool. The controller tries sample-style IK when `ikpy` is installed in the
Python used by Webots. If `ikpy` is missing, it falls back to bounded joint
commands and still emits CGF graph traces.

The IK adapter avoids jerk from recalculating a fresh target solution every
cycle. It reuses the cached IK command while the target remains inside a small
deadband, replans periodically or when the target moves, and applies both joint
step and joint acceleration limits before emitting commands. This is not a
precomputed fixed trajectory: the graph remains reactive to target movement.

Useful tuning variables:

```text
CGF_ABB_IRB_4600_TARGET_DEADBAND_M
CGF_ABB_IRB_4600_REPLAN_INTERVAL
CGF_ABB_IRB_4600_MAX_JOINT_STEP_RAD
CGF_ABB_IRB_4600_MAX_JOINT_ACCEL_STEP_RAD
CGF_ABB_IRB_4600_COMMAND_SMOOTHING_ALPHA
```

## Offline Trace Mode

`run_offline_demo()` remains available for dependency-light tests. It writes the
same graph-control trace contract without launching Webots. It is not the
public demo surface.

## Claim Boundary

See [claim-boundary.md](claim-boundary.md). In short:

- no real robot safety claim;
- no manufacturing production claim;
- no benchmark or autonomy claim;
- no guarantee that a simulator setup matches a physical robot.
