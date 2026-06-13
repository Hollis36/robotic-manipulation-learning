"""Small SE(2) transform helpers used by the Chapter 3 casebook."""

from __future__ import annotations

import numpy as np


def rot2(theta: float) -> np.ndarray:
    """Return a 2D rotation matrix."""
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array([[c, -s], [s, c]], dtype=float)


def make_transform(theta: float, translation) -> np.ndarray:
    """Build a 3x3 homogeneous transform from angle and xy translation."""
    t = np.asarray(translation, dtype=float)
    if t.shape != (2,):
        raise ValueError("translation must be a 2-vector")

    transform = np.eye(3)
    transform[:2, :2] = rot2(theta)
    transform[:2, 2] = t
    return transform


def compose(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Compose two homogeneous transforms as a @ b."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.shape != (3, 3) or b.shape != (3, 3):
        raise ValueError("transforms must both be 3x3")
    return a @ b


def apply_transform(transform: np.ndarray, points) -> np.ndarray:
    """Apply a 3x3 homogeneous transform to an array of 2D points."""
    transform = np.asarray(transform, dtype=float)
    points = np.asarray(points, dtype=float)
    if transform.shape != (3, 3):
        raise ValueError("transform must be 3x3")
    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError("points must have shape (N, 2)")

    homogeneous = np.c_[points, np.ones(points.shape[0])]
    transformed = (transform @ homogeneous.T).T
    return transformed[:, :2]

