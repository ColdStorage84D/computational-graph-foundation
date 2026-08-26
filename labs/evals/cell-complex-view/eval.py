"""CGF CellComplexView eval."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Cell:
    cell_id: str
    dimension: int
    boundary: tuple[str, ...] = ()
    support_refs: tuple[str, ...] = ()


def validate_cells(cells: dict[str, Cell]) -> None:
    if not cells:
        raise ValueError("cells are required")
    for cell in cells.values():
        if cell.dimension < 0:
            raise ValueError("cell dimension must be nonnegative")
        for boundary_id in cell.boundary:
            if boundary_id not in cells:
                raise ValueError(f"missing boundary cell: {boundary_id}")
            if cells[boundary_id].dimension != cell.dimension - 1:
                raise ValueError("boundary dimension mismatch")


def boundary_of(cells: dict[str, Cell], cell_id: str) -> set[str]:
    validate_cells(cells)
    if cell_id not in cells:
        raise ValueError("cell missing")
    return set(cells[cell_id].boundary)


def boundary_boundary(cells: dict[str, Cell], cell_id: str) -> set[str]:
    result: set[str] = set()
    for boundary_id in boundary_of(cells, cell_id):
        for lower_id in cells[boundary_id].boundary:
            if lower_id in result:
                result.remove(lower_id)
            else:
                result.add(lower_id)
    return result


def lift_closed_path_to_cell(cells: dict[str, Cell], edge_ids: tuple[str, ...], cell_id: str) -> Cell:
    validate_cells(cells)
    if not edge_ids:
        raise ValueError("edge path is required")
    if any(cells[edge_id].dimension != 1 for edge_id in edge_ids):
        raise ValueError("path must use 1-cells")
    lifted = Cell(cell_id=cell_id, dimension=2, boundary=edge_ids, support_refs=edge_ids)
    merged = {**cells, cell_id: lifted}
    if boundary_boundary(merged, cell_id):
        raise ValueError("path is not closed under the declared boundary rule")
    return lifted


def lift_episode_to_cell(path_cell_id: str, event_refs: tuple[str, ...], cell_id: str) -> Cell:
    if not event_refs:
        raise ValueError("episode needs event support")
    return Cell(cell_id=cell_id, dimension=3, boundary=(path_cell_id,), support_refs=event_refs)
