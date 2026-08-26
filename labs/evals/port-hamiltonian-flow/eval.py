"""CGF port-Hamiltonian flow eval."""

from __future__ import annotations

from dataclasses import dataclass


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
