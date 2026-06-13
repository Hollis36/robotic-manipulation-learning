import numpy as np

from rml.icp import icp
from rml.transforms import apply_transform, make_transform


def main() -> None:
    source = np.array([[0.0, 0.0], [0.4, 0.1], [0.2, 0.7], [0.9, 0.6], [1.0, 0.0]])
    target = apply_transform(make_transform(0.15, [0.2, -0.1]), source)
    result = icp(source, target, iterations=30, tolerance=1e-10)

    print("case=004_icp_pose_estimation")
    print("estimated_rotation=")
    print(np.round(result.rotation, 3))
    print(f"estimated_translation={np.round(result.translation, 3).tolist()}")
    print(f"mean_error={result.mean_error:.8f}")


if __name__ == "__main__":
    main()

