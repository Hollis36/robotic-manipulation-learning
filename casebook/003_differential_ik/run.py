import numpy as np

from rml.differential_ik import solve_planar_position_ik
from rml.kinematics import planar_forward_kinematics


def main() -> None:
    links = np.array([1.0, 0.8, 0.4])
    target = np.array([1.3, 0.7])
    initial_q = np.array([0.1, 0.1, -0.2])
    result = solve_planar_position_ik(initial_q, target, links, steps=200, damping=0.05, gain=0.6)
    final_position = planar_forward_kinematics(result.joint_angles, links)

    print("case=003_differential_ik")
    print(f"target_xy={np.round(target, 3).tolist()}")
    print(f"joint_angles={np.round(result.joint_angles, 3).tolist()}")
    print(f"final_xy={np.round(final_position, 3).tolist()}")
    print(f"error_norm={result.error_norm:.6f}")


if __name__ == "__main__":
    main()

