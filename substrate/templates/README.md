# Substrate Templates

Templates help developers declare new Substrate subjects before turning them
into examples, applications, or code.

Use a template when you have a graph-shaped problem but have not yet made each
core primitive explicit. The goal is a clear declaration of what is computed,
not an implementation plan.

## Available Templates

- [subject-template.md](subject-template.md): a copyable Markdown template for
  declaring a complete Substrate subject with the 9 core primitives.
- [walkthrough.md](walkthrough.md): a blank-to-filled teaching pass using heat
  relaxation.

## What Complete Means

A complete Substrate subject declares:

```text
graph
typed field
placement
state
action
constraint
evolution
readout
validation
```

All 9 primitives must be explicit. A subject can be small, but it is not ready
if any primitive is missing, implied, or mixed into another section.

## How Templates Relate To Specs And Examples

Use the template as the drafting form. Use the spec pages to review whether the
draft satisfies the contract. Use examples to see what a filled subject looks
like in a small domain.

Recommended order:

```text
subject-template.md -> walkthrough.md -> ../spec/00-overview.md
-> ../examples/README.md
```

Once a subject is complete, it can be rewritten as a clean example, application
note, or section-local code example.
