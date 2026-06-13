import numpy as np

from rml.transforms import apply_transform, compose, make_transform, rot2


def test_rot2_rotates_unit_x_by_ninety_degrees():
    rotated = rot2(np.pi / 2) @ np.array([1.0, 0.0])

    np.testing.assert_allclose(rotated, np.array([0.0, 1.0]), atol=1e-9)


def test_compose_applies_inner_transform_first():
    first = make_transform(np.pi / 2, [1.0, 0.0])
    second = make_transform(0.0, [2.0, 0.0])

    combined = compose(first, second)
    point = apply_transform(combined, np.array([[0.0, 0.0]]))[0]

    np.testing.assert_allclose(point, np.array([1.0, 2.0]), atol=1e-9)


def test_apply_transform_accepts_many_points():
    transform = make_transform(0.0, [1.0, -2.0])
    points = np.array([[0.0, 0.0], [2.0, 3.0]])

    moved = apply_transform(transform, points)

    np.testing.assert_allclose(moved, np.array([[1.0, -2.0], [3.0, 1.0]]))

