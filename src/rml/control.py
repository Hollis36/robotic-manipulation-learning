"""Simple dynamic control examples."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ControlTrace:
    times: np.ndarray
    positions: np.ndarray
    velocities: np.ndarray
    controls: np.ndarray


def simulate_pd_mass(
    x0: float,
    v0: float,
    target: float,
    kp: float = 20.0,
    kd: float = 8.0,
    dt: float = 0.01,
    steps: int = 300,
) -> ControlTrace:
    """Simulate a unit-mass point controlled by u = kp error - kd velocity."""
    if dt <= 0:
        raise ValueError("dt must be positive")
    if steps <= 0:
        raise ValueError("steps must be positive")

    times = np.arange(steps + 1, dtype=float) * dt
    positions = np.zeros(steps + 1, dtype=float)
    velocities = np.zeros(steps + 1, dtype=float)
    controls = np.zeros(steps, dtype=float)
    positions[0] = float(x0)
    velocities[0] = float(v0)

    for i in range(steps):
        error = float(target) - positions[i]
        control = float(kp) * error - float(kd) * velocities[i]
        controls[i] = control
        velocities[i + 1] = velocities[i] + control * dt
        positions[i + 1] = positions[i] + velocities[i + 1] * dt

    return ControlTrace(times=times, positions=positions, velocities=velocities, controls=controls)

