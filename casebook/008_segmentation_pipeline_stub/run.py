import numpy as np

from rml.grasp_scoring import score_antipodal_grasps


def main() -> None:
    point_grid = np.array(
        [
            [-0.5, 0.0],
            [-0.45, 0.02],
            [0.45, -0.01],
            [0.5, 0.0],
            [0.0, 0.6],
            [1.2, 1.2],
        ]
    )
    object_mask = np.array([True, True, True, True, False, False])
    target_points = point_grid[object_mask]
    candidates = [
        {"name": "target_object", "center": [0.0, 0.0], "angle": 0.0, "width": 1.0},
        {"name": "background", "center": [0.0, 0.6], "angle": 0.0, "width": 0.5},
    ]
    best = score_antipodal_grasps(target_points, candidates)[0]

    print("case=008_segmentation_pipeline_stub")
    print(f"segmented_points={len(target_points)}")
    print(f"best_downstream_grasp={best.name}")
    print(f"score={best.score:.2f}")


if __name__ == "__main__":
    main()

