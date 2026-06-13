"""Damped least-squares differential IK for planar examples."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from rml.kinematics import planar_forward_kinematics, planar_jacobian


@dataclass(frozen=True)
class IKResult:
    joint_angles: np.ndarray
    error_norm: float
    iterations: int


def damped_least_squares_step(jacobian, error, damping: float = 1e-3) -> np.ndarray:
    """Compute dq = J^T (J J^T + lambda^2 I)^-1 error."""
    j = np.asarray(jacobian, dtype=float)
    e = np.asarray(error, dtype=float)
    if j.ndim != 2:
        raise ValueError("jacobian must be two-dimensional")
    if e.shape != (j.shape[0],):
        raise ValueError("error length must match jacobian row count")
    if damping < 0:
        raise ValueError("damping must be non-negative")

    regularized = j @ j.T + (damping**2) * np.eye(j.shape[0])
    task_step = np.linalg.solve(regularized, e)
    return j.T @ task_step


def solve_planar_position_ik(
    initial_q,
    target_xy,
    link_lengths,
    steps: int = 100,
    damping: float = 1e-2,
    gain: float = 0.5,
    tolerance: float = 1e-6,
) -> IKResult:
    """Iteratively solve planar position IK with damped least squares."""
    q = np.asarray(initial_q, dtype=float).copy()
    target = np.asarray(target_xy, dtype=float)
    links = np.asarray(link_lengths, dtype=float)
    if q.shape != links.shape:
        raise ValueError("initial_q and link_lengths must have the same shape")
    if target.shape != (2,):
        raise ValueError("target_xy must be a 2-vector")
    if steps <= 0:
        raise ValueError("steps must be positive")

    error_norm = float("inf")
    iteration = 0
    for iteration in range(1, steps + 1):
        current = planar_forward_kinematics(q, links)
        error = target - current
        error_norm = float(np.linalg.norm(error))
        if error_norm < tolerance:
            break
        jacobian = planar_jacobian(q, links)
        q += gain * damped_least_squares_step(jacobian, error, damping=damping)

    final_error = target - planar_forward_kinematics(q, links)
    return IKResult(
        joint_angles=q,
        error_norm=float(np.linalg.norm(final_error)),
        iterations=iteration,
    )

