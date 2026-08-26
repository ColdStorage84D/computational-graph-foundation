# Primitive Implementation

This guide shows how the 9 core Substrate primitives can appear in minimal
representations, light math, and tiny Python-like code sketches.

It is not a public API, SDK, package design, or full numerical method. The goal
is to help a developer see how a declaration can become a small computation
without changing the primitive contract.

The teaching thread is heat relaxation on a 4-node line graph:

```text
n0 -- n1 -- n2 -- n3
```

The declared temperature state is:

```text
u = [100, 60, 40, 0]
```

The endpoints stay fixed. The two interior values move toward their neighbors.

## Graph

### Computational role

Graph gives the support for interaction. It says which values can affect each
other.

### Minimal representation

```text
nodes = ["n0", "n1", "n2", "n3"]
edges = [("n0", "n1"), ("n1", "n2"), ("n2", "n3")]
```

### Tiny code shape

```python
nodes = ["n0", "n1", "n2", "n3"]
edges = [(0, 1), (1, 2), (2, 3)]

neighbors = {
    0: [1],
    1: [0, 2],
    2: [1, 3],
    3: [2],
}
```

### Math / physics intuition

The graph is the discrete support. In heat relaxation, an edge says heat can be
compared or exchanged between neighboring sample points.

### Checks

- Every edge endpoint exists in `nodes`.
- Neighbor relationships match declared edges.
- Direction or weight is declared if it changes the meaning.

## Typed field

### Computational role

Typed field gives values meaning. It prevents an implementation from treating
unrelated values as interchangeable features.

### Minimal representation

```text
temperature: scalar number
```

### Tiny code shape

```python
fields = {
    "temperature": {
        "type": "scalar",
        "meaning": "heat value at a sample point",
    }
}
```

### Math / physics intuition

Temperature is a scalar field on the graph. A scalar value is enough for this
teaching example because each node has one heat value.

### Checks

- The field has a name.
- The field has a value kind.
- The field meaning is domain-readable.

## Placement

### Computational role

Placement says where each typed field lives. It prevents invalid operations
between values on incompatible support.

### Minimal representation

```text
temperature lives on nodes
```

### Tiny code shape

```python
placement = {
    "temperature": "node",
}
```

### Math / physics intuition

For heat relaxation, temperature is node-placed. The edge relation is used to
compare neighboring node temperatures, but the temperature itself lives on
nodes.

### Checks

- Every declared field has placement.
- Every state value is attached to the declared support.
- Node-placed and edge-placed values are not mixed without a declared rule.

## State

### Computational role

State gives current values to the placed fields.

### Minimal representation

```text
n0.temperature = 100
n1.temperature = 60
n2.temperature = 40
n3.temperature = 0
```

### Tiny code shape

```python
u = [100.0, 60.0, 40.0, 0.0]
```

### Math / physics intuition

The state vector `u` holds one temperature value per node. The graph tells how
those entries relate.

### Checks

- Every node has one temperature value.
- Values match the declared field type.
- The current state is not mixed with predicted or final state.

## Action

### Computational role

Action declares what behavior the computation prefers, minimizes, preserves, or
explains.

### Minimal representation

```text
Neighboring temperatures should become smoother.
```

### Tiny code shape

```python
def smoothness(u, edges):
    total = 0.0
    for i, j in edges:
        total += (u[i] - u[j]) ** 2
    return total
```

### Math / physics intuition

A simple smoothing action is:

```text
E(u) = sum over edges (u_i - u_j)^2
```

Lower `E(u)` means neighboring node temperatures are closer. This is enough to
express the primitive-level objective without choosing a full method.

### Checks

- The action uses declared fields.
- The action follows declared graph support.
- The action has a clear direction of preference.

## Constraint

### Computational role

Constraint declares states, changes, or outputs that are not allowed.

### Minimal representation

```text
n0.temperature must remain 100
n3.temperature must remain 0
```

### Tiny code shape

```python
fixed = {
    0: 100.0,
    3: 0.0,
}

def apply_constraints(u):
    u = list(u)
    for index, value in fixed.items():
        u[index] = value
    return u
```

### Math / physics intuition

The endpoints are fixed boundary values in the teaching example. At the
primitive level, the important point is simply that some state values are not
allowed to change.

### Checks

- Fixed values remain fixed after each update.
- Invalid state changes are rejected or repaired.
- Constraint failure is visible to validation.

## Evolution

### Computational role

Evolution declares how state changes.

### Minimal representation

```text
Interior nodes move toward the average of neighboring temperatures.
Endpoints remain fixed.
```

### Tiny code shape

```python
def step(u):
    next_u = list(u)
    next_u[1] = 0.5 * (u[0] + u[2])
    next_u[2] = 0.5 * (u[1] + u[3])
    return apply_constraints(next_u)
```

### Math / physics intuition

For this small line graph, a simple relaxation step is:

```text
u_1' = (u_0 + u_2) / 2
u_2' = (u_1 + u_3) / 2
```

This moves interior temperatures toward neighboring values while preserving the
declared constraints.

### Checks

- Only allowed state values change.
- The update uses declared graph relationships.
- Constraints still hold after the update.

## Readout

### Computational role

Readout declares the domain answer extracted from state or a sequence of states.

### Minimal representation

```text
final temperature profile
```

### Tiny code shape

```python
def readout(u):
    return {
        "temperature_profile": {
            "n0": u[0],
            "n1": u[1],
            "n2": u[2],
            "n3": u[3],
        }
    }
```

### Math / physics intuition

The readout is not the update rule. It is the answer the domain asks for: the
temperature value at each sample point after relaxation.

### Checks

- The readout comes from declared state.
- The readout has domain meaning.
- Readout does not mutate state.

## Validation

### Computational role

Validation declares how to decide whether the result should be trusted.

### Minimal representation

```text
Endpoints remain fixed.
Every node has one readable temperature.
The final profile is no sharper than the starting profile.
```

### Tiny code shape

```python
def validate(start_u, final_u):
    endpoint_ok = final_u[0] == 100.0 and final_u[3] == 0.0
    readable = len(final_u) == 4 and all(isinstance(x, float) for x in final_u)
    smoother = smoothness(final_u, edges) <= smoothness(start_u, edges)
    return endpoint_ok and readable and smoother
```

### Math / physics intuition

Validation checks declared promises. For the heat example, the promises are
fixed endpoints, readable node temperatures, and reduced neighbor difference.

### Checks

- Pass/fail conditions are explicit.
- Failure can be inspected.
- Validation checks the declared action, constraint, evolution, and readout.

## Complete Tiny Sketch

This sketch is illustrative. It is not a CGF API.

```python
nodes = ["n0", "n1", "n2", "n3"]
edges = [(0, 1), (1, 2), (2, 3)]
fixed = {0: 100.0, 3: 0.0}

start_u = [100.0, 60.0, 40.0, 0.0]

def smoothness(u, edges):
    total = 0.0
    for i, j in edges:
        total += (u[i] - u[j]) ** 2
    return total

def apply_constraints(u):
    u = list(u)
    for index, value in fixed.items():
        u[index] = value
    return u

def step(u):
    next_u = list(u)
    next_u[1] = 0.5 * (u[0] + u[2])
    next_u[2] = 0.5 * (u[1] + u[3])
    return apply_constraints(next_u)

def readout(u):
    return {
        "temperature_profile": {
            "n0": u[0],
            "n1": u[1],
            "n2": u[2],
            "n3": u[3],
        }
    }

def validate(start_u, final_u):
    endpoint_ok = final_u[0] == 100.0 and final_u[3] == 0.0
    readable = len(final_u) == 4 and all(isinstance(x, float) for x in final_u)
    smoother = smoothness(final_u, edges) <= smoothness(start_u, edges)
    return endpoint_ok and readable and smoother

final_u = start_u
for _ in range(3):
    final_u = step(final_u)

result = readout(final_u)
ok = validate(start_u, final_u)
```

## Research Need

Core primitives usually do not need papers. They are declaration vocabulary.

Research and references become important when a primitive is tied to a specific
method, equation family, physics model, optimization rule, uncertainty model, or
extension component. Those belong in derivative mechanics, extension components,
research notes, or future section-local implementation docs.
