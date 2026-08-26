# Architecture Contracts

Architecture contracts define the minimum record shape needed for runtime
operation around a declared Substrate subject.

They are not schemas, packages, or SDK APIs. They are public documentation
contracts that future implementations can translate into their own records.

## Contract Cards

- [event-contract.md](event-contract.md)
- [proposal-contract.md](proposal-contract.md)
- [commit-contract.md](commit-contract.md)
- [outcome-contract.md](outcome-contract.md)
- [trace-contract.md](trace-contract.md)
- [persistence-contract.md](persistence-contract.md)

## Standard Shape

Each contract card uses:

```text
Purpose
Minimum record
Validation questions
Failure modes
Boundary
```

## Rule

Contracts should preserve the runtime spine:

```text
event log -> graph/path view -> proposal -> verification -> commit
  -> trace -> eligibility -> outcome -> value/memory update -> replay
```

When path-conditioned or path-gated operation is used, contracts should also
preserve path context refs, path-conditioned effects, gate basis, gate weight or
outcome, blocked reasons, unknown-path behavior, and verifier basis where
relevant.

When graph brain/spine, subgraph capsules, or graph runtime memory are used,
contracts should also preserve capsule ids, route trace paths, static relation
refs, eligibility ids, memory role, memory update kind, promotion/quarantine
status, and counterfactual status where relevant.
