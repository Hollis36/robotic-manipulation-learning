"""Simplified point-cloud grasp scoring for bin-picking intuition."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class GraspScore:
    name: str
    score: float
    center: np.ndarray
    angle: float
    width: float
    left_contacts: int
    right_contacts: int


def _candidate_value(candidate: dict, key: str, default=None):
    if key in candidate:
        return candidate[key]
    if default is not None:
        return default
    raise ValueError(f"candidate missing required key: {key}")


def score_antipodal_grasps(points, candidates) -> list[GraspScore]:
    """Rank simple parallel-jaw grasp candidates against a 2D point cloud."""
    points = np.asarray(points, dtype=float)
    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError("points must have shape (N, 2)")

    scores: list[GraspScore] = []
    for index, candidate in enumerate(candidates):
        center = np.asarray(_candidate_value(candidate, "center"), dtype=float)
        angle = float(_candidate_value(candidate, "angle", 0.0))
        width = float(_candidate_value(candidate, "width"))
        if center.shape != (2,):
            raise ValueError("candidate center must be a 2-vector")
        if width <= 0:
            raise ValueError("candidate width must be positive")

        closing_axis = np.array([np.cos(angle), np.sin(angle)])
        approach_axis = np.array([-np.sin(angle), np.cos(angle)])
        relative = points - center
        closing_distance = relative @ closing_axis
        approach_distance = np.abs(relative @ approach_axis)

        contact_tolerance = max(0.08, 0.12 * width)
        approach_band = max(0.08, 0.15 * width)
        left = np.logical_and(
            np.abs(closing_distance + width / 2.0) <= contact_tolerance,
            approach_distance <= approach_band,
        )
        right = np.logical_and(
            np.abs(closing_distance - width / 2.0) <= contact_tolerance,
            approach_distance <= approach_band,
        )

        left_contacts = int(np.count_nonzero(left))
        right_contacts = int(np.count_nonzero(right))
        balance = min(left_contacts, right_contacts)
        support = left_contacts + right_contacts
        score = 2.0 * balance + 0.1 * support
        name = str(_candidate_value(candidate, "name", f"candidate_{index}"))

        scores.append(
            GraspScore(
                name=name,
                score=float(score),
                center=center,
                angle=angle,
                width=width,
                left_contacts=left_contacts,
                right_contacts=right_contacts,
            )
        )

    return sorted(scores, key=lambda item: item.score, reverse=True)

