"""Planar serial-arm kinematics for lightweight manipulation examples."""

from __future__ import annotations

import numpy as np


def _as_matching_vectors(joint_angles, link_lengths) -> tuple[np.ndarray, np.ndarray]:
    q = np.asarray(joint_angles, dtype=float)
    links = np.asarray(link_lengths, dtype=float)
    if q.ndim != 1 or links.ndim != 1:
        raise ValueError("joint_angles and link_lengths must be one-dimensional")
    if q.shape != links.shape:
        raise ValueError("joint_angles and link_lengths must have the same length")
    return q, links


def planar_forward_kinematics(joint_angles, link_lengths) -> np.ndarray:
    """Return the xy end-effector position of a planar serial arm."""
    q, links = _as_matching_vectors(joint_angles, link_lengths)
    cumulative = np.cumsum(q)
    x = np.sum(links * np.cos(cumulative))
    y = np.sum(links * np.sin(cumulative))
    return np.array([x, y], dtype=float)


def planar_jacobian(joint_angles, link_lengths) -> np.ndarray:
    """Return the 2 x N position Jacobian for a planar serial arm."""
    q, links = _as_matching_vectors(joint_angles, link_lengths)
    cumulative = np.cumsum(q)
    jacobian = np.zeros((2, len(q)), dtype=float)

    for joint_index in range(len(q)):
        active_angles = cumulative[joint_index:]
        active_links = links[joint_index:]
        jacobian[0, joint_index] = -np.sum(active_links * np.sin(active_angles))
        jacobian[1, joint_index] = np.sum(active_links * np.cos(active_angles))

    return jacobian

