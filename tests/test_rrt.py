import numpy as np

from rml.rrt import path_is_collision_free, rrt


def test_rrt_finds_collision_free_path_around_circle():
    start = np.array([0.0, 0.0])
    goal = np.array([1.0, 1.0])
    obstacles = [(0.5, 0.5, 0.2)]

    path = rrt(
        start,
        goal,
        bounds=((0.0, 1.2), (0.0, 1.2)),
        obstacles=obstacles,
        step_size=0.15,
        max_iter=500,
        seed=4,
    )

    np.testing.assert_allclose(path[0], start)
    np.testing.assert_allclose(path[-1], goal)
    assert path_is_collision_free(path, obstacles)
    assert len(path) > 2

