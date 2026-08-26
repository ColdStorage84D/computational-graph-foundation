# Applications

Applications show how CGF ideas can be used in concrete domains.

Applications should be self-contained. They may use CGF reference docs, copy
patterns, fork them, or ignore them.

Here, self-contained means that an application carries its own CGF contract,
claim boundary, and local code or fixture. Optional simulator applications may
still depend on Webots and its version-pinned upstream assets; their READMEs
must state those runtime requirements.

Initial application candidates:

- medical image analysis;
- security;
- robotics;
- optimization;
- multimodal systems;
- predictive maintenance;
- molecules;
- market or trading systems.

Applications must not redefine Substrate or Architecture. They should link back
to the section decisions they use.

## Current Applications

- [DEMO_GUIDE.md](DEMO_GUIDE.md): recommended forkable demo path:
  Signal Review -> Medical Image Analysis -> Graph Memory Bot.
- [bots/README.md](bots/README.md): Graph Memory Bot, the generalized
  stdlib-only bot/controller skeleton for execution graph, graph runtime
  memory, topology, traces, candidate actions, proposals, and gates.
  See [bots/provisional-growth-example.md](bots/provisional-growth-example.md)
  for the route-growth walkthrough using Provisional Graph Growth.
- [maze-graph-memory-bot/README.md](maze-graph-memory-bot/README.md):
  Webots maze application using the Graph Memory Bot action loop. It shows
  candidate actions, predicted outcomes, gates, selected wheel commands, trace,
  and memory update in a small simulator fixture.
- [industrial-robot-arm/README.md](industrial-robot-arm/README.md):
  Industrial Robot Arm Graph as a shipped Webots robot-control demo. It shows
  six-axis topology, action candidates, safety gates, emitted commands,
  evidence paths, and trace. See
  [industrial-robot-arm/claim-boundary.md](industrial-robot-arm/claim-boundary.md)
  for claim limits.
- [medical-image-analysis/README.md](medical-image-analysis/README.md):
  medical image analysis as an application example built from reusable
  evidence, multimodal, Granular Analysis, routing, proposer/verifier, and
  review framework concepts. See
  [medical-image-analysis/index.html](medical-image-analysis/index.html)
  for the local fixture demo,
  [medical-image-analysis/walkthrough.md](medical-image-analysis/walkthrough.md)
  for the application path,
  [medical-image-analysis/BENCHMARK_RESOURCES.md](medical-image-analysis/BENCHMARK_RESOURCES.md)
  for optional local benchmark setup, and
  [medical-image-analysis/claim-boundary.md](medical-image-analysis/claim-boundary.md)
  for claim limits.
- [signal-review/README.md](signal-review/README.md): signal and alert review
  as a third application shape built from Signal Review, feature views,
  processor routing, proposer/verifier, and traceable review or abstain.

## Forkable Demo Positioning

- Signal Review is the default "fork this first" demo: it is
  dependency-light and backed by a tiny Labs `contract-pass`.
- Medical Image Analysis is the clearest Granular Analysis story: one case,
  many lenses, many proposals, verifier, and review or abstain.
- Graph Memory Bot is the technical action-and-memory demo: input or sensor
  state, candidate actions, predicted outcomes, gates, selected action, trace,
  observed outcome, and graph runtime memory. Use
  [maze-graph-memory-bot/README.md](maze-graph-memory-bot/README.md) when that
  story needs a Webots maze fixture, and use the bot route-growth walkthrough
  when recurring unknown patterns should create provisional routes before any
  durable graph change.
- Industrial Robot Arm Graph is the technical safety-gate demo for a six-axis
  manipulator in Webots: topology, bounded command, safety gate, evidence path,
  trace.

Webots demos are shipped as app-local simulator fixtures. They do not create
benchmark, autonomy, real robot safety, or production-control claims.

## Reusable Concepts

If a concept can be used outside one application, put it in
[../architecture/frameworks/README.md](../architecture/frameworks/README.md)
or another owning Architecture/Substrate document. Applications should compose
those concepts rather than own them.
