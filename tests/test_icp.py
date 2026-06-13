import numpy as np

from rml.icp import best_fit_transform, icp
from rml.transforms import apply_transform, make_transform


def test_best_fit_transform_recovers_known_2d_rigid_motion():
    source = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    transform = make_transform(0.3, [0.4, -0.2])
    target = apply_transform(transform, source)

    rotation, translation = best_fit_transform(source, target)

    np.testing.assert_allclose(rotation, transform[:2, :2], atol=1e-9)
    np.testing.assert_allclose(translation, transform[:2, 2], atol=1e-9)


def test_icp_aligns_synthetic_point_cloud_with_near_initial_pose():
    source = np.array(
        [
            [0.0, 0.0],
            [0.4, 0.1],
            [0.2, 0.7],
            [0.9, 0.6],
            [1.0, 0.0],
        ]
    )
    target = apply_transform(make_transform(0.15, [0.2, -0.1]), source)

    result = icp(source, target, iterations=30, tolerance=1e-10)

    np.testing.assert_allclose(result.transformed_source, target, atol=1e-5)
    assert result.mean_error < 1e-5
    assert result.iterations <= 30

