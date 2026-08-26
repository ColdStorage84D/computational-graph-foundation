# Topology In CGF

## Purpose

Topology in CGF means the structure that remains meaningful when exact
coordinates, distances, or display layout change.

This guide separates the main topology meanings so a developer or agent can
choose the right CGF piece without guessing.

## Short rule

Start with ordinary graph topology. Add higher-dimensional topology or
topological rigidity only when the subject would become misleading or invalid
without that extra structure.

## Four topology meanings

| Meaning | Owner | Use it for | First document |
| --- | --- | --- | --- |
| Graph topology | Core Substrate graph primitive | Nodes, edges, paths, connectivity, adjacency, and support. | [../primitives.md](../primitives.md) |
| Higher-dimensional topology | Research direction | Cells, faces, surfaces, volumes, boundary maps, and cycles as explicit objects. | [../../research/extension-studies/higher-dimensional-topology.md](../../research/extension-studies/higher-dimensional-topology.md) |
| Topological rigidity | Substrate extension | Protecting declared cycles, explicit phase degree, named regime diagnostics, transition corridors, or reference-relative collapse-sensitive structure. | [cards/topological-rigidity.md](cards/topological-rigidity.md) |
| Application graph topology | Application or example declaration | Domain structure such as a robot arm, maze, workflow, catalog, or sensor layout expressed as a graph. | [../examples/README.md](../examples/README.md) |

## Graph topology

Graph topology is the default. It is enough when the subject only needs:

- declared nodes and edges;
- paths or neighborhoods;
- connectivity or reachability;
- support for fields and readout;
- validation that relationships exist where the subject says they exist.

Do not add a topology extension when ordinary graph structure already protects
the result.

## Higher-dimensional topology

Use higher-dimensional topology when nodes and edges are not enough because the
subject needs objects such as:

- closed paths as declared cycles;
- faces, patches, or surfaces;
- volumes or regions with boundaries;
- higher-order relations that are not reducible to independent pairwise edges;
- boundary checks such as `boundary(boundary(cell)) = 0`.

Current status: research-only. It can inform declarations, but it should not be
presented as a validated extension until narrowed into examples, cards, or Labs
evals.

## Topological rigidity

Use topological rigidity when important structure may be erased by smoothing,
compression, embedding, simplification, or learning.

Good fit:

- a loop must not collapse into a line;
- an explicit phase degree or a separately named cycle diagnostic affects the
  readout;
- rare regimes or transition corridors must not merge into common regions;
- a cyclic or recurrent structure must remain visible after transformation;
- collapse risk should be reported as part of validation.

Minimum declaration:

- protected support: cycle, closed path, recurrent region, transition corridor,
  phase loop, cell, or topological-domain support;
- carrier field: a nonvanishing $U(1)$ phase when integer phase degree is
  claimed; otherwise a unit vector, orientation, transition label, or other
  typed state with no automatic winding interpretation;
- protection term: a reference-relative action or constraint that resists
  declared invalid collapse;
- topology summary: exact phase degree, named cycle or twist diagnostic,
  reference-relative collapse risk, or related readout with estimator,
  exactness status, and uncertainty;
- validation scope: where and when the topology claim is meaningful.

Current status: Substrate extension with a tiny CGF-local `contract-pass` eval.
The pass claim is limited to unit-carrier validation, reference-relative area
and non-collinearity retention, sampled explicit-phase degree, labeled
closed-area cycle diagnostics, collapse-risk composition, and evidence-only
output on tiny fixtures.

## Topology-aware encoding assumption

When an encoder turns structured input into vectors, features, regions, or a
graph view, assume topology may matter if the arrangement of parts carries
domain meaning.

This assumption is useful when an ordinary embedding might preserve local
similarity while losing:

- loops or closed regions;
- boundary continuity;
- nested or adjacent compartments;
- rare transition regions;
- explicit-phase or separately labeled orientation structure;
- region connectivity that affects readout.

In that case, a topology-aware encoding path should be considered. It can add
explicit region support, boundary support, cycle candidates, carrier fields,
collapse-risk checks, or topology summaries before the subject is read out.

Treat this as a design hypothesis until the project has its own eval. A
topology-aware encoder can guide feature design and validation, but it should
not be described as an improvement claim unless a CGF-local or documented
external benchmark reproduces the result.

## Application graph topology

Application graph topology is ordinary domain structure declared as a graph.
For example, an application may declare joint chains, maze cells, evidence
relationships, or dependency paths.

This is not automatically topological rigidity. It becomes topological rigidity
only when the application must protect cycles, phases, winding, collapse risk,
or higher-order structure from invalid transformation.

## How topology differs from nearby concepts

| Concept | Use when | Do not confuse with |
| --- | --- | --- |
| Metric placement | Distance, scale, curvature, or coordinate validity matters. | Topology; metric can change while topology remains. |
| Basis-mode representation | Symmetry or an eigenbasis makes modes the natural graph nodes. | Topology; mode structure can exist without cycles or collapse risk. |
| Gauge transport | Values must be compared across frames, bases, orientations, or phase conventions. | Rigidity; transport makes comparison meaningful, rigidity protects structure. |
| Sheaf consistency | Local views overlap and must agree before a global assignment is trusted. | Higher-dimensional topology; sheaves may use topology but solve consistency. |
| Weak form | Aggregate tested laws are more valid than pointwise laws. | Topology; weak support can be topological, but the problem is law validation. |

## Decision path

Use this path after the 9 core primitives are complete:

```text
1. Are nodes, edges, paths, and support enough?
   yes -> use graph topology only.

2. Do cycles, faces, cells, or boundaries need to be declared as objects?
   yes -> use higher-dimensional topology as research support.

3. Can smoothing, compression, embedding, simplification, or learning erase
   structure that affects readout or validation?
   yes -> use topological rigidity.

4. Is an encoder turning structured input into vectors, features, regions, or
   a graph view?
   yes -> check whether topology-aware encoding should protect arrangement,
          boundaries, loops, rare transitions, or connectivity.

5. Is the problem actually distance, symmetry, frame comparison, local
   consistency, or aggregate laws?
   yes -> use the matching extension instead of topology language.
```

## When not to use topology language

Avoid topology vocabulary when:

- it only means visual layout;
- ordinary graph connectivity is enough;
- no protected structure is named;
- no validation can detect topology loss;
- the extension would preserve noise rather than domain meaning;
- the problem is better handled by metric placement, basis-mode representation,
  gauge transport, sheaf consistency, weak form, or another extension.

## Review questions

Before adding topology to a subject, answer:

```text
1. Which topology meaning is being used?
2. What exact structure is protected or declared?
3. Which core primitives already carry it?
4. What failure happens if the topology is ignored?
5. What validation detects topology loss or invalid topology?
6. If an encoder is used, what structural information could it collapse?
7. What claim is supported by current Research or Labs results?
```

If those answers are unclear, keep ordinary graph topology and mark the rest as
research.
