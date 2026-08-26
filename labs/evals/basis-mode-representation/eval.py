"""CGF basis-mode representation eval."""

from __future__ import annotations

import math


ModeLabel = tuple[int, str]
ModeGraph = dict[str, object]


def mode_id(label: ModeLabel) -> str:
    index, component = label
    return f"fourier:{index}:{component}"


def validate_mode_label(label: ModeLabel) -> None:
    index, component = label
    if index < 0:
        raise ValueError("mode index must be non-negative")
    if component not in {"constant", "cos", "sin"}:
        raise ValueError("unknown mode component")
    if index == 0 and component != "constant":
        raise ValueError("zero mode must be constant")
    if index > 0 and component == "constant":
        raise ValueError("nonzero mode cannot be constant")


def build_fourier_mode_graph(max_index: int) -> ModeGraph:
    if max_index < 1:
        raise ValueError("max_index must be at least 1")
    labels: list[ModeLabel] = [(0, "constant")]
    for index in range(1, max_index + 1):
        labels.append((index, "cos"))
        labels.append((index, "sin"))
    for label in labels:
        validate_mode_label(label)

    nodes = {
        mode_id(label): {
            "basis_family": "fourier",
            "mode_label": label,
            "placement": "mode",
        }
        for label in labels
    }
    edges = []
    for left in labels:
        for right in labels:
            if left == right:
                continue
            if allowed_coupling(left, right):
                edges.append((mode_id(left), mode_id(right), "selection_rule"))
    return {"nodes": nodes, "edges": tuple(edges)}


def allowed_coupling(left: ModeLabel, right: ModeLabel) -> bool:
    left_index, left_component = left
    right_index, right_component = right
    if left_index == right_index and left_index > 0:
        return {left_component, right_component} == {"cos", "sin"}
    return abs(left_index - right_index) == 1


def validate_coupling(left: ModeLabel, right: ModeLabel) -> None:
    validate_mode_label(left)
    validate_mode_label(right)
    if not allowed_coupling(left, right):
        raise ValueError("coupling violates declared selection rule")


def place_coefficients(graph: ModeGraph, coefficients: dict[str, float]) -> dict[str, dict[str, object]]:
    nodes = graph["nodes"]
    if not isinstance(nodes, dict):
        raise ValueError("graph nodes must be a dictionary")
    placed = {}
    for node_id, value in coefficients.items():
        if node_id not in nodes:
            raise ValueError("coefficient must live on a declared mode node")
        if not math.isfinite(value):
            raise ValueError("coefficient must be finite")
        placed[node_id] = {"placement": "mode", "value": value}
    return placed


def diagonal_operator(coefficients: dict[str, float], weights: dict[int, float]) -> dict[str, float]:
    output = {}
    for node_id, value in coefficients.items():
        _, index_text, _ = node_id.split(":")
        output[node_id] = value * weights.get(int(index_text), 1.0)
    return output


def block_rotate_first_mode(coefficients: dict[str, float], angle: float) -> dict[str, float]:
    output = dict(coefficients)
    cos_id = mode_id((1, "cos"))
    sin_id = mode_id((1, "sin"))
    cos_value = coefficients.get(cos_id, 0.0)
    sin_value = coefficients.get(sin_id, 0.0)
    output[cos_id] = math.cos(angle) * cos_value - math.sin(angle) * sin_value
    output[sin_id] = math.sin(angle) * cos_value + math.cos(angle) * sin_value
    return output


def readout(coefficients: dict[str, float], x: float) -> float:
    value = coefficients.get(mode_id((0, "constant")), 0.0)
    for node_id, coefficient in coefficients.items():
        _, index_text, component = node_id.split(":")
        index = int(index_text)
        if index == 0:
            continue
        if component == "cos":
            value += coefficient * math.cos(index * x)
        elif component == "sin":
            value += coefficient * math.sin(index * x)
    return value


def truncation_report(coefficients: dict[str, float], kept_max_index: int) -> dict[str, object]:
    kept = {}
    dropped_energy = 0.0
    for node_id, value in coefficients.items():
        _, index_text, _ = node_id.split(":")
        index = int(index_text)
        if index <= kept_max_index:
            kept[node_id] = value
        else:
            dropped_energy += value * value
    return {
        "kept": kept,
        "dropped_mode_residual": math.sqrt(dropped_energy),
        "residual_hidden": False,
    }
