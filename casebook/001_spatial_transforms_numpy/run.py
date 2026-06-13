import numpy as np

from rml.transforms import apply_transform, compose, make_transform


def main() -> None:
    world_from_gripper = make_transform(np.pi / 2, [0.5, 0.2])
    gripper_from_brick = make_transform(0.0, [0.1, 0.0])
    world_from_brick = compose(world_from_gripper, gripper_from_brick)
    brick_origin = apply_transform(world_from_brick, np.array([[0.0, 0.0]]))[0]

    print("case=001_spatial_transforms_numpy")
    print("world_from_brick=")
    print(np.round(world_from_brick, 3))
    print(f"brick_origin_world={np.round(brick_origin, 3).tolist()}")


if __name__ == "__main__":
    main()

