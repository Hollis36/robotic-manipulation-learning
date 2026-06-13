import numpy as np

from rml.differential_ik import damped_least_squares_step, solve_planar_position_ik
from rml.kinematics import planar_forward_kinematics


def test_damped_least_squares_step_solves_simple_identity_task():
    jacobian = np.eye(2)
    error = np.array([0.5, -0.25])

    step = damped_least_squares_step(jacobian, error, damping=1e-6)

    np.testing.assert_allclose(step, error, atol=1e-6)


def test_solve_planar_position_ik_reaches_target():
    links = np.array([1.0, 0.8, 0.4])
    target = np.array([1.3, 0.7])
    initial_q = np.array([0.1, 0.1, -0.2])

    result = solve_planar_position_ik(
        initial_q,
        target,
        links,
        steps=200,
        damping=0.05,
        gain=0.6,
    )

    final_position = planar_forward_kinematics(result.joint_angles, links)
    np.testing.assert_allclose(final_position, target, atol=1e-3)
    assert result.error_norm < 1e-3
    assert result.iterations <= 200

