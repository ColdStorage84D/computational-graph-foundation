# Derivative Implementation

This guide shows how derivative mechanics can turn a complete Substrate subject
into computable structure.

It continues the heat relaxation example from
[../primitive-implementation.md](../primitive-implementation.md). The snippets
are Python-like pseudocode inside documentation. They are not a CGF API, package,
or required implementation style.

The core subject is already declared:

```text
graph: n0 -- n1 -- n2 -- n3
typed field: temperature
placement: temperature lives on nodes
state: u = [100, 60, 40, 0]
action: reduce neighbor differences
constraint: endpoints fixed
evolution: interior values relax toward neighbors
readout: final temperature profile
validation: endpoint and smoothness checks
```

Derivative mechanics add the extra declarations needed to make that subject more
formal, inspectable, and method-ready.

## Units / Dimensions

### Computational role

Units / dimensions make field operations meaningful.

### Minimal representation

```text
temperature: degrees C
distance between adjacent nodes: one unit interval
```

### Tiny code shape

```python
units = {
    "temperature": "degC",
    "edge_length": "unit_interval",
}
```

### Math / physics intuition

The smoothing action compares temperature differences. Those differences only
make sense if every temperature is in the same unit.

### Checks

- Every temperature value has the same unit.
- Any conversion happens before action or evolution.
- Readout reports the unit.

## Boundary

### Computational role

Boundary declares fixed or externally constrained graph support.

### Minimal representation

```text
n0 is fixed at 100 degC
n3 is fixed at 0 degC
```

### Tiny code shape

```python
boundary = {
    0: {"kind": "fixed", "temperature": 100.0},
    3: {"kind": "fixed", "temperature": 0.0},
}

def enforce_boundary(u):
    u = list(u)
    for index, rule in boundary.items():
        u[index] = rule["temperature"]
    return u
```

### Math / physics intuition

Fixed endpoints are boundary conditions. The interior can relax, but the edge
conditions define the problem being solved.

### Checks

- Boundary support exists in the graph.
- Boundary values are not overwritten by evolution.
- Validation checks boundary values after each update or final readout.

## Source

### Computational role

Source declares external addition, removal, forcing, or observation that changes
state.

### Minimal representation

```text
No internal heat source is present.
```

### Tiny code shape

```python
source = {
    0: 0.0,
    1: 0.0,
    2: 0.0,
    3: 0.0,
}
```

### Math / physics intuition

For this teaching subject, all temperature change comes from relaxation between
neighbors and fixed endpoints. A source term would represent added heat or
removed heat at a node.

### Checks

- If source is absent, state change is not attributed to hidden forcing.
- If source is present, its support and unit match the field.
- Validation can account for source contribution.

## Local Action / Lagrangian

### Computational role

Local action / Lagrangian declares graph-local terms that compose the global
action.

### Minimal representation

```text
Each edge contributes squared temperature difference.
```

### Tiny code shape

```python
def local_action(u, edge):
    i, j = edge
    return (u[i] - u[j]) ** 2

def action(u, edges):
    return sum(local_action(u, edge) for edge in edges)
```

### Math / physics intuition

The global smoothing action can be written as:

```text
E(u) = sum_(i,j in edges) (u_i - u_j)^2
```

Each edge term is local. The global action is the sum of those local
contributions.

### Checks

- Every local term uses declared graph support.
- Every local term uses declared fields.
- The global action is assembled from visible local terms.

## Variation

### Computational role

Variation declares which values can change when deriving an update or condition.

### Minimal representation

```text
u1 and u2 may vary
u0 and u3 may not vary
```

### Tiny code shape

```python
free_nodes = [1, 2]
fixed_nodes = [0, 3]

def can_vary(index):
    return index in free_nodes
```

### Math / physics intuition

Only interior temperatures are varied. A valid change leaves fixed endpoints
unchanged.

For the smoothing action, the equilibrium condition for an interior node is
roughly:

```text
u_i should move toward the average of its neighbors
```

### Checks

- Variation only touches allowed support.
- Fixed values have zero allowed change.
- Evolution follows the variation rule.

## Operator Assembly

### Computational role

Operator assembly connects local graph relations into a global update structure.

### Minimal representation

```text
Interior update uses neighbor averaging.
```

### Tiny code shape

```python
def assemble_neighbor_average():
    return {
        1: {0: 0.5, 2: 0.5},
        2: {1: 0.5, 3: 0.5},
    }

operator = assemble_neighbor_average()

def apply_operator(u, operator):
    next_u = list(u)
    for target, weights in operator.items():
        next_u[target] = sum(weight * u[source] for source, weight in weights.items())
    return enforce_boundary(next_u)
```

### Math / physics intuition

The update can be seen as an operator acting on state:

```text
u_1' = 0.5 u_0 + 0.5 u_2
u_2' = 0.5 u_1 + 0.5 u_3
```

The operator is assembled from graph adjacency and the declared boundary rule.

### Checks

- Operator inputs and outputs match placed fields.
- Weights refer to existing graph support.
- Boundary constraints are applied after the operator.

## Invariant

### Computational role

Invariant declares what should remain stable across updates.

### Minimal representation

```text
endpoint temperatures remain unchanged
the state remains one temperature per node
```

### Tiny code shape

```python
def invariant_holds(u):
    endpoints_ok = u[0] == 100.0 and u[3] == 0.0
    shape_ok = len(u) == 4
    return endpoints_ok and shape_ok
```

### Math / physics intuition

The fixed endpoint values are preserved by every admissible update. This makes
the boundary a stability condition, not just an initial fact.

### Checks

- Invariant is named before validation uses it.
- Invariant is checked after evolution.
- Invariant failure blocks readout acceptance.

## Residual / Error Estimator

### Computational role

Residual / error estimator measures how far the current state is from satisfying
the declared condition.

### Minimal representation

```text
Interior node residual is the difference between current value and neighbor average.
```

### Tiny code shape

```python
def residual(u):
    r1 = u[1] - 0.5 * (u[0] + u[2])
    r2 = u[2] - 0.5 * (u[1] + u[3])
    return [r1, r2]

def error_size(u):
    r = residual(u)
    return max(abs(value) for value in r)
```

### Math / physics intuition

At a relaxed interior node:

```text
u_i = average(neighbor temperatures)
```

The residual says how far that condition is from true.

### Checks

- Residual uses declared interior support.
- Error threshold is explicit when used.
- Validation reports unresolved error instead of hiding it.

## Solver Selection

### Computational role

Solver selection names the method shape justified by the declared subject and
derivative mechanics.

### Minimal representation

```text
Use repeated neighbor averaging for this tiny teaching subject.
```

### Tiny code shape

```python
def solve(u, steps=10, tolerance=1e-6):
    u = enforce_boundary(u)
    for _ in range(steps):
        next_u = apply_operator(u, operator)
        if error_size(next_u) <= tolerance:
            return next_u
        u = next_u
    return u
```

### Math / physics intuition

Repeated neighbor averaging is enough for a small teaching example because the
graph is tiny, the field is scalar, and the boundary is fixed.

This is not a claim that every Substrate subject should use this method. Solver
choice belongs after the subject, derivative mechanics, and validation checks
are visible.

### Checks

- Method choice matches the declared subject.
- Stop condition is explicit.
- Final state is validated before readout is trusted.

## Complete Tiny Derivative Sketch

This sketch is illustrative. It is not a CGF API.

```python
edges = [(0, 1), (1, 2), (2, 3)]
u0 = [100.0, 60.0, 40.0, 0.0]

units = {"temperature": "degC", "edge_length": "unit_interval"}
boundary = {
    0: {"kind": "fixed", "temperature": 100.0},
    3: {"kind": "fixed", "temperature": 0.0},
}
source = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}

def enforce_boundary(u):
    u = list(u)
    for index, rule in boundary.items():
        u[index] = rule["temperature"]
    return u

def local_action(u, edge):
    i, j = edge
    return (u[i] - u[j]) ** 2

def action(u):
    return sum(local_action(u, edge) for edge in edges)

operator = {
    1: {0: 0.5, 2: 0.5},
    2: {1: 0.5, 3: 0.5},
}

def apply_operator(u):
    next_u = list(u)
    for target, weights in operator.items():
        next_u[target] = sum(weight * u[source] for source, weight in weights.items())
    return enforce_boundary(next_u)

def invariant_holds(u):
    return u[0] == 100.0 and u[3] == 0.0 and len(u) == 4

def residual(u):
    return [
        u[1] - 0.5 * (u[0] + u[2]),
        u[2] - 0.5 * (u[1] + u[3]),
    ]

def error_size(u):
    return max(abs(value) for value in residual(u))

def solve(u, steps=10, tolerance=1e-6):
    u = enforce_boundary(u)
    for _ in range(steps):
        next_u = apply_operator(u)
        if not invariant_holds(next_u):
            raise ValueError("invariant failed")
        if error_size(next_u) <= tolerance:
            return next_u
        u = next_u
    return u

final_u = solve(u0)
```

## Research Need

This page uses simple teaching math. It does not require a bibliography.

Research references become important when a derivative mechanic makes a stronger
claim, such as a specific discretization, conservation law, error estimator,
optimization method, physical model, or solver guarantee.
