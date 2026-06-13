import numpy as np

from rml.grasp_scoring import score_antipodal_grasps


def main() -> None:
    points = np.array([[-0.5, 0.02], [-0.48, -0.02], [0.5, 0.01], [0.52, -0.01], [0.0, 0.6]])
    candidates = [
        {"name": "off_center", "center": [0.0, 0.4], "angle": 0.0, "width": 1.0},
        {"name": "balanced", "center": [0.0, 0.0], "angle": 0.0, "width": 1.0},
        {"name": "too_narrow", "center": [0.0, 0.0], "angle": 0.0, "width": 0.4},
    ]
    best = score_antipodal_grasps(points, candidates)[0]

    print("case=005_point_cloud_grasp_scoring")
    print(f"best_grasp={best.name}")
    print(f"score={best.score:.2f}")
    print(f"contacts=left:{best.left_contacts}, right:{best.right_contacts}")


if __name__ == "__main__":
    main()

