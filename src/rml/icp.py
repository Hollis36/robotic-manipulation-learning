"""Small point-cloud registration utilities."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ICPResult:
    rotation: np.ndarray
    translation: np.ndarray
    transformed_source: np.ndarray
    mean_error: float
    iterations: int


def _as_point_cloud(points) -> np.ndarray:
    array = np.asarray(points, dtype=float)
    if array.ndim != 2 or array.shape[1] != 2:
        raise ValueError("point cloud must have shape (N, 2)")
    if len(array) < 2:
        raise ValueError("point cloud must contain at least two points")
    return array


def best_fit_transform(source, target) -> tuple[np.ndarray, np.ndarray]:
    """Return the 2D rigid transform that best maps source points to target."""
    source = _as_point_cloud(source)
    target = _as_point_cloud(target)
    if source.shape != target.shape:
        raise ValueError("source and target must have matching shapes")

    source_centroid = source.mean(axis=0)
    target_centroid = target.mean(axis=0)
    source_centered = source - source_centroid
    target_centered = target - target_centroid

    covariance = source_centered.T @ target_centered
    u, _, vt = np.linalg.svd(covariance)
    rotation = vt.T @ u.T
    if np.linalg.det(rotation) < 0:
        vt[-1, :] *= -1
        rotation = vt.T @ u.T

    translation = target_centroid - rotation @ source_centroid
    return rotation, translation


def _nearest_neighbors(source: np.ndarray, target: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    deltas = source[:, None, :] - target[None, :, :]
    distances = np.linalg.norm(deltas, axis=2)
    indices = np.argmin(distances, axis=1)
    return target[indices], distances[np.arange(len(source)), indices]


def icp(source, target, iterations: int = 20, tolerance: float = 1e-8) -> ICPResult:
    """Align source to target using a minimal 2D ICP loop."""
    source = _as_point_cloud(source)
    target = _as_point_cloud(target)
    if iterations <= 0:
        raise ValueError("iterations must be positive")

    transformed = source.copy()
    total_rotation = np.eye(2)
    total_translation = np.zeros(2)
    previous_error = float("inf")
    mean_error = float("inf")
    completed = 0

    for completed in range(1, iterations + 1):
        matched, _ = _nearest_neighbors(transformed, target)
        rotation, translation = best_fit_transform(transformed, matched)
        transformed = (rotation @ transformed.T).T + translation
        total_rotation = rotation @ total_rotation
        total_translation = rotation @ total_translation + translation

        _, distances = _nearest_neighbors(transformed, target)
        mean_error = float(np.mean(distances))
        if abs(previous_error - mean_error) < tolerance:
            break
        previous_error = mean_error

    return ICPResult(
        rotation=total_rotation,
        translation=total_translation,
        transformed_source=transformed,
        mean_error=mean_error,
        iterations=completed,
    )

