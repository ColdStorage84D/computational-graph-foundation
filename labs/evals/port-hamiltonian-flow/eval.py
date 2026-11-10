"""CGF port-Hamiltonian flow eval.

Two layers live here:

- a linear port-Hamiltonian system, x' = (J - R) grad H(x) + G u with output
  y = G^T grad H(x) and quadratic storage H(x) = 1/2 x^T Q x, stepped with the
  implicit midpoint rule so the discrete power balance holds exactly;
- the accounting records that carry storage, supply, and dissipation out of
  the model without hiding a residual.

The structure is the point: J is skew-symmetric, so interconnection moves
energy without creating it; R is positive semidefinite, so dissipation can only
remove it; ports are the only way energy enters or leaves.
"""

from __future__ import annotations

from dataclasses import dataclass


Vector = tuple[float, ...]
Matrix = tuple[tuple[float, ...], ...]


# --- Small dense linear algebra ---------------------------------------------


def _matvec(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(sum(a * b for a, b in zip(row, vector)) for row in matrix)


def _transpose(matrix: Matrix, columns: int) -> Matrix:
    if not matrix:
        return tuple(() for _ in range(columns))
    return tuple(zip(*matrix))


def _dot(left: Vector, right: Vector) -> float:
    return sum(a * b for a, b in zip(left, right))


def _solve(matrix: Matrix, rhs: Vector) -> Vector:
    n = len(rhs)
    rows = [list(row) + [value] for row, value in zip(matrix, rhs)]
    for column in range(n):
        pivot = max(range(column, n), key=lambda index: abs(rows[index][column]))
        if abs(rows[pivot][column]) < 1e-14:
            raise ValueError("linear system is singular")
        rows[column], rows[pivot] = rows[pivot], rows[column]
        scale = rows[column][column]
        rows[column] = [value / scale for value in rows[column]]
        for index in range(n):
            if index == column:
                continue
            factor = rows[index][column]
            if factor:
                rows[index] = [a - factor * b for a, b in zip(rows[index], rows[column])]
    return tuple(row[n] for row in rows)


def _is_symmetric(matrix: Matrix, tolerance: float) -> bool:
    n = len(matrix)
    return all(abs(matrix[i][j] - matrix[j][i]) <= tolerance for i in range(n) for j in range(n))


def _is_positive_semidefinite(matrix: Matrix, tolerance: float) -> bool:
    """Symmetric elimination. A zero pivot must have a zero column below it."""

    work = [list(row) for row in matrix]
    n = len(work)
    for k in range(n):
        pivot = work[k][k]
        if pivot < -tolerance:
            return False
        if abs(pivot) <= tolerance:
            if any(abs(work[i][k]) > tolerance for i in range(k + 1, n)):
                return False
            continue
        for i in range(k + 1, n):
            factor = work[i][k] / pivot
            for j in range(k, n):
                work[i][j] -= factor * work[k][j]
    return True


# --- Port-Hamiltonian system -------------------------------------------------


@dataclass(frozen=True)
class PortHamiltonianSystem:
    interconnection: Matrix  # J, skew-symmetric
    dissipation: Matrix  # R, symmetric positive semidefinite
    storage: Matrix  # Q, symmetric positive definite, H(x) = 1/2 x^T Q x
    input_map: Matrix  # G, one column per port

    @property
    def dimension(self) -> int:
        return len(self.storage)

    @property
    def port_count(self) -> int:
        return len(self.input_map[0]) if self.input_map and self.input_map[0] else 0


def validate_system(system: PortHamiltonianSystem, tolerance: float = 1e-12) -> None:
    n = system.dimension
    if n == 0:
        raise ValueError("state dimension must be positive")
    for name, matrix in (
        ("interconnection", system.interconnection),
        ("dissipation", system.dissipation),
        ("storage", system.storage),
    ):
        if len(matrix) != n or any(len(row) != n for row in matrix):
            raise ValueError(f"{name} matrix must be {n} x {n}")
    if len(system.input_map) != n or len({len(row) for row in system.input_map}) != 1:
        raise ValueError("input map must have one row per state")
    j = system.interconnection
    if any(abs(j[a][b] + j[b][a]) > tolerance for a in range(n) for b in range(n)):
        raise ValueError("interconnection matrix must be skew-symmetric")
    if not _is_symmetric(system.dissipation, tolerance):
        raise ValueError("dissipation matrix must be symmetric")
    if not _is_positive_semidefinite(system.dissipation, tolerance):
        raise ValueError("dissipation matrix must be positive semidefinite")
    if not _is_symmetric(system.storage, tolerance):
        raise ValueError("storage matrix must be symmetric")
    shifted = tuple(
        tuple(value - (1e-12 if a == b else 0.0) for b, value in enumerate(row))
        for a, row in enumerate(system.storage)
    )
    if not _is_positive_semidefinite(shifted, 0.0):
        raise ValueError("storage matrix must be positive definite")


def gradient(system: PortHamiltonianSystem, state: Vector) -> Vector:
    return _matvec(system.storage, state)


def hamiltonian(system: PortHamiltonianSystem, state: Vector) -> float:
    return 0.5 * _dot(state, gradient(system, state))


def port_output(system: PortHamiltonianSystem, state: Vector) -> Vector:
    return _matvec(_transpose(system.input_map, system.port_count), gradient(system, state))


def step(
    system: PortHamiltonianSystem, state: Vector, port_input: Vector, dt: float
) -> tuple[Vector, dict[str, float]]:
    """One implicit-midpoint step and its power balance.

    For quadratic storage the balance is exact up to rounding:
    H(next) - H(state) = supplied - dissipated.
    """

    validate_system(system)
    if dt <= 0.0:
        raise ValueError("time step must be positive")
    n = system.dimension
    if len(state) != n or len(port_input) != system.port_count:
        raise ValueError("state or input has the wrong dimension")
    flow = tuple(
        tuple(
            sum(
                (system.interconnection[a][k] - system.dissipation[a][k]) * system.storage[k][b]
                for k in range(n)
            )
            for b in range(n)
        )
        for a in range(n)
    )
    forcing = _matvec(system.input_map, port_input) if system.port_count else tuple(0.0 for _ in range(n))
    left = tuple(
        tuple((1.0 if a == b else 0.0) - 0.5 * dt * flow[a][b] for b in range(n)) for a in range(n)
    )
    right = tuple(
        value + 0.5 * dt * drift + dt * force
        for value, drift, force in zip(state, _matvec(flow, state), forcing)
    )
    next_state = _solve(left, right)
    midpoint = tuple(0.5 * (a + b) for a, b in zip(state, next_state))
    effort = gradient(system, midpoint)
    supplied = dt * _dot(port_output(system, midpoint), port_input)
    dissipated = dt * _dot(effort, _matvec(system.dissipation, effort))
    stored_change = hamiltonian(system, next_state) - hamiltonian(system, state)
    return next_state, {
        "stored_change": stored_change,
        "supplied": supplied,
        "dissipated": dissipated,
        "residual": stored_change - supplied + dissipated,
    }


def simulate(
    system: PortHamiltonianSystem, state: Vector, port_inputs: tuple[Vector, ...], dt: float
) -> dict[str, object]:
    energies = [hamiltonian(system, state)]
    supplied = 0.0
    dissipated = 0.0
    worst_residual = 0.0
    for port_input in port_inputs:
        state, balance = step(system, state, port_input, dt)
        energies.append(hamiltonian(system, state))
        supplied += balance["supplied"]
        dissipated += balance["dissipated"]
        worst_residual = max(worst_residual, abs(balance["residual"]))
    return {
        "final_state": state,
        "energies": tuple(energies),
        "supplied": supplied,
        "dissipated": dissipated,
        "worst_step_residual": worst_residual,
    }


def interconnect(first: PortHamiltonianSystem, second: PortHamiltonianSystem) -> PortHamiltonianSystem:
    """Power-conserving feedback: u_first = -y_second, u_second = y_first.

    The composite is again port-Hamiltonian, with no remaining external port.
    """

    validate_system(first)
    validate_system(second)
    if first.port_count != second.port_count or first.port_count == 0:
        raise ValueError("systems need matching, nonempty ports to interconnect")
    n, m = first.dimension, second.dimension
    coupling = tuple(
        tuple(
            sum(first.input_map[a][p] * second.input_map[b][p] for p in range(first.port_count))
            for b in range(m)
        )
        for a in range(n)
    )

    def block(top_left: Matrix, top_right: Matrix, bottom_left: Matrix, bottom_right: Matrix) -> Matrix:
        top = tuple(tuple(top_left[a]) + tuple(top_right[a]) for a in range(n))
        bottom = tuple(tuple(bottom_left[b]) + tuple(bottom_right[b]) for b in range(m))
        return top + bottom

    zeros_nm = tuple(tuple(0.0 for _ in range(m)) for _ in range(n))
    zeros_mn = tuple(tuple(0.0 for _ in range(n)) for _ in range(m))
    minus_coupling = tuple(tuple(-value for value in row) for row in coupling)
    coupling_t = tuple(tuple(coupling[a][b] for a in range(n)) for b in range(m))
    return PortHamiltonianSystem(
        interconnection=block(first.interconnection, minus_coupling, coupling_t, second.interconnection),
        dissipation=block(first.dissipation, zeros_nm, zeros_mn, second.dissipation),
        storage=block(first.storage, zeros_nm, zeros_mn, second.storage),
        input_map=tuple(() for _ in range(n + m)),
    )


def mass_spring_damper(mass: float, stiffness: float, damping: float) -> PortHamiltonianSystem:
    """State (position, momentum). The port is force in, velocity out."""

    return PortHamiltonianSystem(
        interconnection=((0.0, 1.0), (-1.0, 0.0)),
        dissipation=((0.0, 0.0), (0.0, damping)),
        storage=((stiffness, 0.0), (0.0, 1.0 / mass)),
        input_map=((0.0,), (1.0,)),
    )


# --- Accounting records ------------------------------------------------------


@dataclass(frozen=True)
class Port:
    port_id: str
    quantity: str
    direction: str


def balance_storage(initial: float, final: float, supply: float, work: float, dissipation: float) -> dict[str, float]:
    expected_final = initial + supply - work - dissipation
    residual = final - expected_final
    return {
        "initial": initial,
        "final": final,
        "supply": supply,
        "work": work,
        "dissipation": dissipation,
        "residual": residual,
    }


def compose_ports(source: Port, target: Port, available: float, requested: float) -> dict[str, object]:
    if source.quantity != target.quantity:
        raise ValueError("port quantities do not match")
    if source.direction != "out" or target.direction != "in":
        raise ValueError("port directions do not compose")
    exchanged = min(available, requested)
    return {"quantity": source.quantity, "exchanged": exchanged, "residual_request": requested - exchanged}


def score_dissipation(work: float, overhead: float) -> dict[str, float]:
    return {"work": work, "dissipation": overhead, "consumed": work + overhead}


def flow_record(balance: dict[str, float]) -> dict[str, object]:
    return {"kind": "flow_evidence", "balance": balance, "authority": False}
