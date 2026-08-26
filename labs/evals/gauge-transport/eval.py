"""CGF gauge transport eval."""

from __future__ import annotations

from dataclasses import dataclass
import math


Vector = tuple[float, ...]
Matrix = tuple[tuple[float, ...], ...]


@dataclass(frozen=True)
class Frame:
    frame_id: str
    basis: tuple[str, ...]

    @property
    def dimension(self) -> int:
        return len(self.basis)


@dataclass(frozen=True)
class TransportMap:
    map_id: str
    source_frame: Frame
    target_frame: Frame
    matrix: Matrix
    source_refs: tuple[str, ...] = ()


def declare_frame(frame_id: str, basis: tuple[str, ...]) -> Frame:
    if not frame_id:
        raise ValueError("frame_id is required")
    if not basis:
        raise ValueError("basis is required")
    return Frame(frame_id, basis)


def _check_matrix(matrix: Matrix, rows: int, columns: int) -> None:
    if len(matrix) != rows:
        raise ValueError("matrix row count does not match target frame")
    if any(len(row) != columns for row in matrix):
        raise ValueError("matrix column count does not match source frame")


def transport_state(state: Vector, transport: TransportMap) -> Vector:
    if len(state) != transport.source_frame.dimension:
        raise ValueError("state dimension does not match source frame")
    _check_matrix(
        transport.matrix,
        transport.target_frame.dimension,
        transport.source_frame.dimension,
    )
    return tuple(sum(a * b for a, b in zip(row, state)) for row in transport.matrix)


def _matmul(left: Matrix, right: Matrix) -> Matrix:
    if not left or not right or len(left[0]) != len(right):
        raise ValueError("matrix dimensions do not compose")
    right_columns = tuple(zip(*right))
    return tuple(
        tuple(sum(a * b for a, b in zip(row, column)) for column in right_columns)
        for row in left
    )


def compose_transport(first: TransportMap, second: TransportMap, map_id: str) -> TransportMap:
    if first.target_frame != second.source_frame:
        raise ValueError("transport frames do not compose")
    return TransportMap(
        map_id=map_id,
        source_frame=first.source_frame,
        target_frame=second.target_frame,
        matrix=_matmul(second.matrix, first.matrix),
        source_refs=first.source_refs + second.source_refs,
    )


def invert_transport(transport: TransportMap, map_id: str) -> TransportMap:
    n = transport.source_frame.dimension
    if transport.target_frame.dimension != n:
        raise ValueError("only square transports can be inverted")
    _check_matrix(transport.matrix, n, n)
    augmented = [
        list(row) + [1.0 if i == j else 0.0 for j in range(n)]
        for i, row in enumerate(transport.matrix)
    ]
    for column in range(n):
        pivot_row = max(range(column, n), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot_row][column]) < 1e-12:
            raise ValueError("transport matrix is singular")
        augmented[column], augmented[pivot_row] = augmented[pivot_row], augmented[column]
        pivot = augmented[column][column]
        augmented[column] = [value / pivot for value in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                augmented[row][i] - factor * augmented[column][i]
                for i in range(2 * n)
            ]
    inverse = tuple(tuple(row[n:]) for row in augmented)
    return TransportMap(
        map_id=map_id,
        source_frame=transport.target_frame,
        target_frame=transport.source_frame,
        matrix=inverse,
        source_refs=transport.source_refs + (f"inverse:{transport.map_id}",),
    )


def score_residual(left: Vector, right: Vector) -> float:
    if len(left) != len(right):
        raise ValueError("residual vectors must share dimension")
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(left, right)))


def detect_holonomy(transports: tuple[TransportMap, ...], probe: Vector) -> float:
    state = probe
    for transport in transports:
        state = transport_state(state, transport)
    return score_residual(probe, state)
