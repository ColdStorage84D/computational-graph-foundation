# Bot Graph Framework

## Purpose

Use this framework when a system acts through sensing, proposing, gating,
committing, executing, observing, and learning.

## Reusable Concept

A bot is an execution graph with a brain/spine route boundary, surface nodes,
subgraph capsules, proposals, gates, committed actions or non-actions, outcome
records, and graph runtime memory.

The bot example is only one use. The same pattern can support tool agents,
robots, workflow automation, simulations, games, and process controllers.

## Uses CGF Pieces

- execution graph;
- graph brain and spine;
- subgraph capsules;
- proposal / verifier / commit;
- path-conditioned and path-gated operators;
- graph runtime memory;
- trace and replay.

## Example Applications

- robot controller;
- maze or navigation example;
- tool-using assistant;
- automation worker;
- process controller;
- game agent.

## When To Use

- Actions need a visible commit boundary.
- Local specialists or tools should not own global authority.
- The system learns from outcomes.
- Memory must affect future behavior without becoming hidden state.
- Path context changes scoring, routing, or gate behavior.

## When Not To Use

- The project only needs a static graph declaration.
- No action, non-action, or outcome feedback exists.
- A simple script can run safely without proposal, commit, trace, or replay.

## Boundary

The brain coordinates phases. The spine routes records. Surface nodes own local
transforms. Subgraph capsules own local detail. Commit and outcome coupling own
learning authority.

## Implementation Posture

The optional reference code in [../../reference/python/README.md](../../reference/python/README.md)
contains a small bot graph surface. It is a reference, not a required runtime.
