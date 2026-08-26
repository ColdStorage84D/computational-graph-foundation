"""CGF exterior placement eval."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExteriorQuantity:
    quantity_id: str
    kind: str
    value: float
    contact_support: tuple[str, ...]


def validate_exterior_quantity(internal_nodes: set[str], quantity: ExteriorQuantity) -> None:
    if quantity.quantity_id in internal_nodes:
        raise ValueError("exterior quantity cannot be internal graph state")
    if not quantity.contact_support:
        raise ValueError("contact support is required")
    missing = set(quantity.contact_support) - internal_nodes
    if missing:
        raise ValueError("contact support must resolve to internal nodes")


def exterior_contribution(internal_nodes: set[str], quantity: ExteriorQuantity, weights: dict[str, float]) -> dict[str, float]:
    validate_exterior_quantity(internal_nodes, quantity)
    result = {node: 0.0 for node in internal_nodes}
    for node in quantity.contact_support:
        result[node] = quantity.value * weights.get(node, 1.0)
    return result


def internal_state_without_exterior(internal_state: dict[str, float], quantity: ExteriorQuantity) -> dict[str, float]:
    if quantity.quantity_id in internal_state:
        raise ValueError("exterior quantity leaked into internal state")
    return dict(internal_state)
