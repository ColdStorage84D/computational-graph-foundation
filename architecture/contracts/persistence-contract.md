# Persistence Contract

## Purpose

Persistence defines how Architecture records survive replay, restart, audit,
and projection rebuilds without choosing a specific database.

## Minimum Record Discipline

```text
ordered durable records
stable ids
record types
schema or version marker
append or update rule
projection rebuild rule
replay boundary
retention or redaction policy
```

## Validation Questions

```text
1. Can projections rebuild from durable records?
2. Are ids stable across replay?
3. Are updates explicit rather than silent mutation?
4. Can failed or partial operations be represented?
5. Is private or large data referenced safely?
```

## Failure Modes

- Hidden in-process state is required for replay.
- Record order is unstable.
- Updates overwrite audit history.
- Schema changes cannot be interpreted.
- Large or private data is copied into every record.

## Boundary

Persistence is a discipline, not a database requirement.
