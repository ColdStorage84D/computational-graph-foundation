"""CGF hyperbolic placement eval."""

from __future__ import annotations

import math


Point = tuple[float, float]


def norm(point: Point) -> float:
    return math.sqrt(point[0] ** 2 + point[1] ** 2)


def validate_placement(point: Point, eps: float = 1e-9) -> None:
    if norm(point) >= 1.0 - eps:
        raise ValueError("point must lie inside the Poincare ball")


def project_to_ball(point: Point, eps: float = 1e-6) -> Point:
    radius = norm(point)
    if radius < 1.0 - eps:
        return point
    scale = (1.0 - eps) / radius
    return (point[0] * scale, point[1] * scale)


def euclidean_distance(left: Point, right: Point) -> float:
    return math.sqrt((left[0] - right[0]) ** 2 + (left[1] - right[1]) ** 2)


def poincare_distance(left: Point, right: Point) -> float:
    validate_placement(left)
    validate_placement(right)
    diff2 = (left[0] - right[0]) ** 2 + (left[1] - right[1]) ** 2
    denom = (1.0 - norm(left) ** 2) * (1.0 - norm(right) ** 2)
    return math.acosh(1.0 + 2.0 * diff2 / denom)


def rank_recall(query: Point, candidates: dict[str, Point]) -> list[str]:
    return sorted(candidates, key=lambda key: poincare_distance(query, candidates[key]))


def path_score(path: tuple[Point, ...]) -> float:
    length = sum(poincare_distance(left, right) for left, right in zip(path, path[1:]))
    radial_backtracking = sum(
        max(0.0, norm(left) - norm(right))
        for left, right in zip(path, path[1:])
    )
    return -(length + radial_backtracking)
