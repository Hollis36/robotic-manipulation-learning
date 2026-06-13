import numpy as np

from rml.kinematics import planar_forward_kinematics, planar_jacobian


def main() -> None:
    q = np.array([0.4, -0.2, 0.3])
    links = np.array([0.7, 0.5, 0.2])
    position = planar_forward_kinematics(q, links)
    jacobian = planar_jacobian(q, links)

    print("case=002_forward_kinematics_planar_arm")
    print(f"joint_angles={np.round(q, 3).tolist()}")
    print(f"end_effector_xy={np.round(position, 3).tolist()}")
    print("jacobian=")
    print(np.round(jacobian, 3))


if __name__ == "__main__":
    main()

