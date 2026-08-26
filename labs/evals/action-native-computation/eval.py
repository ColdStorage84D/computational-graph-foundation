from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


class MissingActionError(ValueError):
    """Raised when computation is requested without a declared action."""


class HiddenForcingError(ValueError):
    """Raised when state change depends on an undeclared source."""


class ReadoutAuthorityError(ValueError):
    """Raised when readout claims authority without required checks."""


class ConstraintViolationError(ValueError):
    """Raised when a candidate violates declared constraints."""


class HiddenScoringError(ValueError):
    """Raised when path scoring depends on undeclared weights."""


@dataclass(frozen=True)
class ActionNativeRun:
    initial_state: tuple[float, ...]
    states: tuple[tuple[float, ...], ...]
    action_values: tuple[float, ...]
    residuals: tuple[tuple[float, ...], ...]
    errors: tuple[float, ...]
    readout: dict[str, object]


class HeatRelaxationSubject:
    """Tiny relaxation fixture, not a CGF API."""

    def __init__(
        self,
        *,
        action_declared: bool = True,
        source: dict[int, float] | None = None,
        source_declared: bool = False,
        tolerance: float = 1e-4,
    ) -> None:
        self.edges = ((0, 1), (1, 2), (2, 3))
        self.boundary = {0: 100.0, 3: 0.0}
        self.action_declared = action_declared
        self.source = source or {}
        self.source_declared = source_declared
        self.tolerance = tolerance

    def normalize_state(self, state: tuple[float, ...] | list[float]) -> tuple[float, ...]:
        values = tuple(float(value) for value in state)
        if len(values) != 4:
            raise ValueError("fixture requires one value per graph node")
        if not all(isfinite(value) for value in values):
            raise ValueError("state contains non-finite values")
        return values

    def enforce_boundary(self, state: tuple[float, ...] | list[float]) -> tuple[float, ...]:
        values = list(self.normalize_state(state))
        for index, value in self.boundary.items():
            values[index] = value
        return tuple(values)

    def validate_source(self) -> None:
        hidden = [value for value in self.source.values() if abs(value) > 0.0]
        if hidden and not self.source_declared:
            raise HiddenForcingError("source/forcing must be declared before it can affect evolution")

    def local_action(self, state: tuple[float, ...], edge: tuple[int, int]) -> float:
        if not self.action_declared:
            raise MissingActionError("declared action is required")
        left, right = edge
        return (state[left] - state[right]) ** 2

    def action(self, state: tuple[float, ...] | list[float]) -> float:
        values = self.enforce_boundary(state)
        return sum(self.local_action(values, edge) for edge in self.edges)

    def residual(self, state: tuple[float, ...] | list[float]) -> tuple[float, float]:
        values = self.enforce_boundary(state)
        return (
            values[1] - 0.5 * (values[0] + values[2]),
            values[2] - 0.5 * (values[1] + values[3]),
        )

    def error_size(self, state: tuple[float, ...] | list[float]) -> float:
        return max(abs(value) for value in self.residual(state))

    def update_direction(self, state: tuple[float, ...] | list[float]) -> tuple[float, ...]:
        current = self.enforce_boundary(state)
        self.action(current)
        next_state = list(current)
        next_state[1] = 0.5 * (current[0] + current[2])
        next_state[2] = 0.5 * (current[1] + current[3])
        next_state = list(self.apply_declared_source(tuple(next_state)))
        next_state = self.enforce_boundary(next_state)
        return tuple(next_value - old_value for next_value, old_value in zip(next_state, current))

    def apply_declared_source(self, state: tuple[float, ...]) -> tuple[float, ...]:
        self.validate_source()
        if not self.source:
            return state
        values = list(state)
        for index, amount in self.source.items():
            if index in self.boundary:
                continue
            values[index] += float(amount)
        return tuple(values)

    def step(self, state: tuple[float, ...] | list[float]) -> tuple[float, ...]:
        current = self.enforce_boundary(state)
        direction = self.update_direction(current)
        return self.enforce_boundary([value + delta for value, delta in zip(current, direction)])

    def validate_state(self, state: tuple[float, ...] | list[float]) -> dict[str, object]:
        values = self.enforce_boundary(state)
        boundary_ok = all(values[index] == value for index, value in self.boundary.items())
        error = self.error_size(values)
        return {
            "boundary_ok": boundary_ok,
            "residual": self.residual(values),
            "error": error,
            "accepted": boundary_ok and error <= self.tolerance,
        }

    def trusted_readout(
        self,
        state: tuple[float, ...] | list[float],
        *,
        include_residual: bool = True,
        validate: bool = True,
    ) -> dict[str, object]:
        if not include_residual:
            raise ReadoutAuthorityError("readout requires visible residual/error")
        if not validate:
            raise ReadoutAuthorityError("readout requires validation")
        values = self.enforce_boundary(state)
        validation = self.validate_state(values)
        return {
            "field": values,
            "residual": validation["residual"],
            "error": validation["error"],
            "accepted": validation["accepted"],
            "validation": validation,
        }

    def run(self, initial_state: tuple[float, ...] = (100.0, 60.0, 40.0, 0.0), steps: int = 32) -> ActionNativeRun:
        state = self.enforce_boundary(initial_state)
        states = [state]
        action_values = [self.action(state)]
        residuals = [self.residual(state)]
        errors = [self.error_size(state)]
        for _ in range(steps):
            state = self.step(state)
            states.append(state)
            action_values.append(self.action(state))
            residuals.append(self.residual(state))
            errors.append(self.error_size(state))
        return ActionNativeRun(
            initial_state=self.enforce_boundary(initial_state),
            states=tuple(states),
            action_values=tuple(action_values),
            residuals=tuple(residuals),
            errors=tuple(errors),
            readout=self.trusted_readout(state),
        )


def run_action_native_heat_eval() -> ActionNativeRun:
    return HeatRelaxationSubject().run()


class ConstraintAssignmentSubject:
    """Tiny constraint-satisfaction fixture, not a CGF API."""

    def __init__(
        self,
        *,
        action_declared: bool = True,
        allowed_labels: dict[str, tuple[str, ...]] | None = None,
        adjacency_requires_different: bool = True,
    ) -> None:
        self.nodes = ("a", "b", "c")
        self.edges = (("a", "b"), ("b", "c"))
        self.action_declared = action_declared
        self.allowed_labels = allowed_labels or {
            "a": ("red", "blue"),
            "b": ("red", "blue"),
            "c": ("red", "blue"),
        }
        self.adjacency_requires_different = adjacency_requires_different

    def action(self, assignment: dict[str, str]) -> int:
        if not self.action_declared:
            raise MissingActionError("declared action is required")
        return self.constraint_residual(assignment)

    def constraint_residual(self, assignment: dict[str, str]) -> int:
        missing = sum(1 for node in self.nodes if node not in assignment)
        invalid_label = sum(
            1
            for node, label in assignment.items()
            if node in self.allowed_labels and label not in self.allowed_labels[node]
        )
        adjacency_violations = 0
        if self.adjacency_requires_different:
            adjacency_violations = sum(
                1
                for left, right in self.edges
                if assignment.get(left) is not None
                and assignment.get(right) is not None
                and assignment[left] == assignment[right]
            )
        return missing + invalid_label + adjacency_violations

    def validate_assignment(self, assignment: dict[str, str]) -> dict[str, object]:
        residual = self.constraint_residual(assignment)
        return {
            "residual": residual,
            "error": float(residual),
            "accepted": residual == 0,
        }

    def trusted_readout(
        self,
        assignment: dict[str, str],
        *,
        include_residual: bool = True,
        validate: bool = True,
    ) -> dict[str, object]:
        if not include_residual:
            raise ReadoutAuthorityError("readout requires visible residual/error")
        if not validate:
            raise ReadoutAuthorityError("readout requires validation")
        self.action(assignment)
        validation = self.validate_assignment(assignment)
        if not validation["accepted"]:
            raise ConstraintViolationError("assignment failed declared constraints")
        return {
            "assignment": dict(assignment),
            "residual": validation["residual"],
            "error": validation["error"],
            "accepted": validation["accepted"],
            "validation": validation,
        }

    def solve(self) -> dict[str, object]:
        candidates = (
            {"a": "red", "b": "blue", "c": "red"},
            {"a": "blue", "b": "red", "c": "blue"},
            {"a": "red", "b": "red", "c": "blue"},
        )
        ranked = sorted(
            (self.action(candidate), index, candidate)
            for index, candidate in enumerate(candidates)
        )
        return self.trusted_readout(ranked[0][2])


class LeastActionPathSubject:
    """Tiny least-action-path fixture, not a CGF API."""

    def __init__(
        self,
        *,
        action_declared: bool = True,
        weights_declared: bool = True,
        blocked_edges: tuple[tuple[str, str], ...] = (("b", "d"),),
    ) -> None:
        self.start = "s"
        self.goal = "g"
        self.action_declared = action_declared
        self.weights_declared = weights_declared
        self.weights = {
            ("s", "a"): 1.0,
            ("a", "g"): 2.0,
            ("s", "b"): 1.0,
            ("b", "d"): 0.2,
            ("d", "g"): 0.2,
            ("s", "c"): 3.0,
            ("c", "g"): 3.0,
        }
        self.blocked_edges = set(blocked_edges)
        self.candidates = (
            ("s", "a", "g"),
            ("s", "b", "d", "g"),
            ("s", "c", "g"),
        )

    def _edges_for_path(self, path: tuple[str, ...]) -> tuple[tuple[str, str], ...]:
        return tuple(zip(path, path[1:]))

    def validate_path(self, path: tuple[str, ...]) -> dict[str, object]:
        endpoint_ok = bool(path) and path[0] == self.start and path[-1] == self.goal
        missing_edges = [edge for edge in self._edges_for_path(path) if edge not in self.weights]
        blocked = [edge for edge in self._edges_for_path(path) if edge in self.blocked_edges]
        residual = len(missing_edges) + len(blocked) + (0 if endpoint_ok else 1)
        return {
            "endpoint_ok": endpoint_ok,
            "missing_edges": missing_edges,
            "blocked_edges": blocked,
            "residual": residual,
            "error": float(residual),
            "accepted": residual == 0,
        }

    def action(self, path: tuple[str, ...]) -> float:
        if not self.action_declared:
            raise MissingActionError("declared action is required")
        if not self.weights_declared:
            raise HiddenScoringError("path weights must be declared before scoring")
        validation = self.validate_path(path)
        if validation["residual"] != 0:
            return float("inf")
        return sum(self.weights[edge] for edge in self._edges_for_path(path))

    def trusted_readout(
        self,
        path: tuple[str, ...],
        *,
        include_residual: bool = True,
        validate: bool = True,
    ) -> dict[str, object]:
        if not include_residual:
            raise ReadoutAuthorityError("readout requires visible residual/error")
        if not validate:
            raise ReadoutAuthorityError("readout requires validation")
        score = self.action(path)
        validation = self.validate_path(path)
        if not validation["accepted"]:
            raise ConstraintViolationError("path failed declared constraints")
        return {
            "path": path,
            "action": score,
            "residual": validation["residual"],
            "error": validation["error"],
            "accepted": validation["accepted"],
            "validation": validation,
        }

    def solve(self) -> dict[str, object]:
        scored = sorted((self.action(path), path) for path in self.candidates)
        return self.trusted_readout(scored[0][1])
