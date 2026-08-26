# Substrate

Substrate is the first technical layer of CGF.

It defines the graph-shaped computational subject:

```text
graph + typed field + placement + state
+ action + constraint
+ evolution + readout + validation
```

Substrate answers:

```text
What is being computed?
What quantities live on the graph?
Where do those quantities live?
What state do those quantities have now?
What action, cost, law, or objective governs the system?
What constraints apply?
How does state evolve?
What answer is read out?
How is validity checked?
```

## Start Here

- [../FOUNDATION_TRAVERSAL.md](../FOUNDATION_TRAVERSAL.md): the project-wide
  path for choosing a CGF mix and tracing support through Research and Labs.
- [INDEX.md](INDEX.md): the complete Substrate map, with summaries of every
  component and what to look for while reading or writing a subject.
- [status.md](status.md): the current v0.1 readiness marker for Substrate.
- [concept.md](concept.md): the master explanation of Substrate and its
  primitive model.
- [primitives.md](primitives.md): the focused guide to the 9 mandatory core
  primitives.
- [primitive-implementation.md](primitive-implementation.md): light math and
  tiny code sketches for the primitive layer.
- [derivatives/README.md](derivatives/README.md): derivative mechanics for
  sharpening complete subjects into computable forms.
- [derivatives/action-native-computation.md](derivatives/action-native-computation.md):
  computation as constrained graph-state evolution.
- [derivatives/implementation.md](derivatives/implementation.md): light math
  and tiny pseudocode for derivative mechanics.
- [extensions/README.md](extensions/README.md): optional extension components
  for domain-triggered structure.
- [templates/subject-template.md](templates/subject-template.md): the copyable
  form for declaring a new Substrate subject.
- [templates/walkthrough.md](templates/walkthrough.md): a blank-to-filled pass
  through the subject template.
- [examples/heat-relaxation.md](examples/heat-relaxation.md): the first complete
  core primitive example.
- [vision.md](vision.md): why Substrate exists.
- [spec/00-overview.md](spec/00-overview.md): the public contract.
- [research-notes.md](research-notes.md): open research notes that grow from
  the Substrate concept.

## Boundary

Substrate does not decide how an application orchestrates work. It does not own
operational roles, ordered activity records, adaptive policy state, or product
behavior. Those belong to Architecture or Applications.
