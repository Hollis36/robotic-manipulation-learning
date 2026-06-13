"""A compact 2D RRT planner for motion-planning study cases."""

from __future__ import annotations

import numpy as np


def _as_point(point) -> np.ndarray:
    array = np.asarray(point, dtype=float)
    if array.shape != (2,):
        raise ValueError("point must be a 2-vector")
    return array


def _segment_circle_distance(a: np.ndarray, b: np.ndarray, center: np.ndarray) -> float:
    ab = b - a
    denom = float(ab @ ab)
    if denom == 0:
        return float(np.linalg.norm(center - a))
    t = float(np.clip(((center - a) @ ab) / denom, 0.0, 1.0))
    closest = a + t * ab
    return float(np.linalg.norm(center - closest))


def segment_is_collision_free(a, b, obstacles) -> bool:
    """Return True when a line segment avoids all circular obstacles."""
    a = _as_point(a)
    b = _as_point(b)
    for ox, oy, radius in obstacles:
        if _segment_circle_distance(a, b, np.array([ox, oy], dtype=float)) <= float(radius):
            return False
    return True


def path_is_collision_free(path, obstacles) -> bool:
    """Return True when every path segment avoids all circular obstacles."""
    if len(path) < 2:
        return True
    return all(segment_is_collision_free(path[i], path[i + 1], obstacles) for i in range(len(path) - 1))


def _within_bounds(point: np.ndarray, bounds) -> bool:
    return bounds[0][0] <= point[0] <= bounds[0][1] and bounds[1][0] <= point[1] <= bounds[1][1]


def _reconstruct_path(nodes: list[np.ndarray], parents: list[int], goal_index: int) -> list[np.ndarray]:
    path = []
    index = goal_index
    while index != -1:
        path.append(nodes[index])
        index = parents[index]
    return list(reversed(path))


def rrt(
    start,
    goal,
    bounds,
    obstacles,
    step_size: float = 0.2,
    max_iter: int = 1000,
    seed: int = 0,
) -> list[np.ndarray]:
    """Plan a 2D path with a small deterministic RRT implementation."""
    start = _as_point(start)
    goal = _as_point(goal)
    if step_size <= 0:
        raise ValueError("step_size must be positive")
    if max_iter <= 0:
        raise ValueError("max_iter must be positive")
    if not _within_bounds(start, bounds) or not _within_bounds(goal, bounds):
        raise ValueError("start and goal must lie inside bounds")

    rng = np.random.default_rng(seed)
    nodes = [start]
    parents = [-1]

    for iteration in range(max_iter):
        if iteration % 10 == 0:
            sample = goal
        else:
            sample = np.array(
                [
                    rng.uniform(bounds[0][0], bounds[0][1]),
                    rng.uniform(bounds[1][0], bounds[1][1]),
                ]
            )

        distances = np.array([np.linalg.norm(sample - node) for node in nodes])
        nearest_index = int(np.argmin(distances))
        nearest = nodes[nearest_index]
        direction = sample - nearest
        length = float(np.linalg.norm(direction))
        if length == 0:
            continue
        step = direction / length * min(step_size, length)
        new_node = nearest + step
        if not _within_bounds(new_node, bounds):
            continue
        if not segment_is_collision_free(nearest, new_node, obstacles):
            continue

        nodes.append(new_node)
        parents.append(nearest_index)
        new_index = len(nodes) - 1

        if np.linalg.norm(goal - new_node) <= step_size and segment_is_collision_free(new_node, goal, obstacles):
            nodes.append(goal)
            parents.append(new_index)
            return _reconstruct_path(nodes, parents, len(nodes) - 1)

    raise RuntimeError("RRT failed to find a path")

