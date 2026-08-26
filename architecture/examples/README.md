# Architecture Examples

Architecture examples show how runtime patterns can operate around declared
Substrate subjects.

They are prose examples, not SDKs, packages, schemas, or required
implementations.

## Examples

- [ecommerce-runtime-path.md](ecommerce-runtime-path.md)
- [agent-graph-harness.md](agent-graph-harness.md)
- [evidence-record-flow.md](evidence-record-flow.md)
- [agent-memory-flow.md](agent-memory-flow.md)
- [path-aware-verifier-flow.md](path-aware-verifier-flow.md)
- [bot-execution-graph.md](bot-execution-graph.md)
- [multimodal-review-flow.md](multimodal-review-flow.md)

## Rule

Each example should keep this chain visible:

```text
event -> view -> proposal -> verification -> commit -> trace
  -> eligibility -> outcome -> memory or value update
```
