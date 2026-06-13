import numpy as np

from rml.rrt import path_is_collision_free, rrt


def main() -> None:
    start = np.array([0.0, 0.0])
    goal = np.array([1.0, 1.0])
    obstacles = [(0.5, 0.5, 0.2)]
    path = rrt(start, goal, bounds=((0.0, 1.2), (0.0, 1.2)), obstacles=obstacles, step_size=0.15, max_iter=500, seed=4)

    print("case=006_rrt_motion_planning")
    print(f"waypoints={len(path)}")
    print(f"collision_free={path_is_collision_free(path, obstacles)}")
    print(f"first={np.round(path[0], 3).tolist()} last={np.round(path[-1], 3).tolist()}")


if __name__ == "__main__":
    main()

