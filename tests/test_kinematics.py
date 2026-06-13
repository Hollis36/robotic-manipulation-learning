import numpy as np

from rml.kinematics import planar_forward_kinematics, planar_jacobian


def test_planar_forward_kinematics_stretches_along_x_axis():
    position = planar_forward_kinematics([0.0, 0.0], [1.0, 0.5])

    np.testing.assert_allclose(position, np.array([1.5, 0.0]), atol=1e-9)


def test_planar_forward_kinematics_accumulates_joint_angles():
    position = planar_forward_kinematics([np.pi / 2, -np.pi / 2], [1.0, 1.0])

    np.testing.assert_allclose(position, np.array([1.0, 1.0]), atol=1e-9)


def test_planar_jacobian_matches_finite_difference():
    q = np.array([0.4, -0.2, 0.3])
    links = np.array([0.7, 0.5, 0.2])
    jacobian = planar_jacobian(q, links)
    eps = 1e-6
    finite_difference = np.zeros((2, 3))

    for i in range(3):
        dq = np.zeros(3)
        dq[i] = eps
        forward = planar_forward_kinematics(q + dq, links)
        backward = planar_forward_kinematics(q - dq, links)
        finite_difference[:, i] = (forward - backward) / (2 * eps)

    np.testing.assert_allclose(jacobian, finite_difference, atol=1e-6)

