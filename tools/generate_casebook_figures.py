"""Generate visual assets for the casebook examples."""

from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from rml.control import simulate_pd_mass
from rml.differential_ik import solve_planar_position_ik
from rml.grasp_scoring import score_antipodal_grasps
from rml.gridworld import GridGraspWorld
from rml.icp import icp
from rml.kinematics import planar_forward_kinematics
from rml.rrt import path_is_collision_free, rrt
from rml.transforms import apply_transform, compose, make_transform

OKABE_ITO = {
    "orange": "#E69F00",
    "sky": "#56B4E9",
    "green": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "vermillion": "#D55E00",
    "purple": "#CC79A7",
    "black": "#000000",
}


def _configure_axes(ax, title: str, xlabel: str = "x", ylabel: str = "y") -> None:
    ax.set_title(title, fontsize=10)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, color="#dddddd", linewidth=0.6, alpha=0.8)


def _save(fig, output_dir: Path, name: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{name}.png"
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return path


def _arm_points(q, links) -> np.ndarray:
    q = np.asarray(q, dtype=float)
    links = np.asarray(links, dtype=float)
    points = [np.array([0.0, 0.0])]
    angle = 0.0
    current = np.array([0.0, 0.0])
    for qi, length in zip(q, links):
        angle += qi
        current = current + length * np.array([np.cos(angle), np.sin(angle)])
        points.append(current.copy())
    return np.vstack(points)


def _draw_frame(ax, transform: np.ndarray, label: str) -> None:
    origin = transform[:2, 2]
    x_axis = transform[:2, 0]
    y_axis = transform[:2, 1]
    ax.arrow(origin[0], origin[1], 0.18 * x_axis[0], 0.18 * x_axis[1], color=OKABE_ITO["blue"], width=0.006)
    ax.arrow(origin[0], origin[1], 0.18 * y_axis[0], 0.18 * y_axis[1], color=OKABE_ITO["vermillion"], width=0.006)
    ax.text(origin[0] + 0.02, origin[1] + 0.02, label, fontsize=8)


def figure_001(output_dir: Path) -> Path:
    world_from_gripper = make_transform(np.pi / 2, [0.5, 0.2])
    gripper_from_brick = make_transform(0.0, [0.1, 0.0])
    world_from_brick = compose(world_from_gripper, gripper_from_brick)
    brick_origin = apply_transform(world_from_brick, np.array([[0.0, 0.0]]))[0]

    fig, ax = plt.subplots(figsize=(4.0, 3.2))
    _configure_axes(ax, "Spatial transform composition")
    _draw_frame(ax, np.eye(3), "W")
    _draw_frame(ax, world_from_gripper, "G")
    _draw_frame(ax, world_from_brick, "B")
    ax.scatter([brick_origin[0]], [brick_origin[1]], color=OKABE_ITO["green"], s=45, label="brick origin")
    ax.legend(frameon=False, fontsize=8)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-0.1, 0.8)
    ax.set_ylim(-0.1, 0.6)
    return _save(fig, output_dir, "001_spatial_transforms_numpy")


def figure_002(output_dir: Path) -> Path:
    q = np.array([0.4, -0.2, 0.3])
    links = np.array([0.7, 0.5, 0.2])
    points = _arm_points(q, links)
    ee = planar_forward_kinematics(q, links)

    fig, ax = plt.subplots(figsize=(4.0, 3.2))
    _configure_axes(ax, "Planar arm forward kinematics")
    ax.plot(points[:, 0], points[:, 1], "-o", color=OKABE_ITO["blue"], linewidth=2.0, label="links")
    ax.scatter([ee[0]], [ee[1]], color=OKABE_ITO["orange"], s=55, label="end effector")
    ax.legend(frameon=False, fontsize=8)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-0.1, 1.5)
    ax.set_ylim(-0.1, 0.8)
    return _save(fig, output_dir, "002_forward_kinematics_planar_arm")


def figure_003(output_dir: Path) -> Path:
    links = np.array([1.0, 0.8, 0.4])
    target = np.array([1.3, 0.7])
    initial_q = np.array([0.1, 0.1, -0.2])
    result = solve_planar_position_ik(initial_q, target, links, steps=200, damping=0.05, gain=0.6)
    initial_points = _arm_points(initial_q, links)
    final_points = _arm_points(result.joint_angles, links)

    fig, ax = plt.subplots(figsize=(4.0, 3.2))
    _configure_axes(ax, "Differential IK target reach")
    ax.plot(initial_points[:, 0], initial_points[:, 1], "--o", color=OKABE_ITO["sky"], label="initial")
    ax.plot(final_points[:, 0], final_points[:, 1], "-o", color=OKABE_ITO["blue"], linewidth=2.0, label="solved")
    ax.scatter([target[0]], [target[1]], marker="*", color=OKABE_ITO["vermillion"], s=95, label="target")
    ax.legend(frameon=False, fontsize=8)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-0.5, 2.4)
    ax.set_ylim(-0.7, 1.5)
    return _save(fig, output_dir, "003_differential_ik")


def figure_004(output_dir: Path) -> Path:
    source = np.array([[0.0, 0.0], [0.4, 0.1], [0.2, 0.7], [0.9, 0.6], [1.0, 0.0]])
    target = apply_transform(make_transform(0.15, [0.2, -0.1]), source)
    result = icp(source, target, iterations=30, tolerance=1e-10)

    fig, ax = plt.subplots(figsize=(4.0, 3.2))
    _configure_axes(ax, "ICP alignment")
    ax.scatter(source[:, 0], source[:, 1], color=OKABE_ITO["sky"], label="source")
    ax.scatter(target[:, 0], target[:, 1], color=OKABE_ITO["vermillion"], label="target")
    ax.scatter(result.transformed_source[:, 0], result.transformed_source[:, 1], marker="x", color=OKABE_ITO["black"], label="aligned")
    ax.legend(frameon=False, fontsize=8)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-0.1, 1.4)
    ax.set_ylim(-0.25, 0.9)
    return _save(fig, output_dir, "004_icp_pose_estimation")


def _draw_gripper(ax, center, width, angle, color, label=None) -> None:
    center = np.asarray(center, dtype=float)
    axis = np.array([np.cos(angle), np.sin(angle)])
    approach = np.array([-np.sin(angle), np.cos(angle)])
    left = center - axis * width / 2.0
    right = center + axis * width / 2.0
    jaw = 0.18
    ax.plot([left[0], right[0]], [left[1], right[1]], color=color, linewidth=2.0, label=label)
    for point in [left, right]:
        p0 = point - approach * jaw / 2.0
        p1 = point + approach * jaw / 2.0
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=color, linewidth=2.0)


def figure_005(output_dir: Path) -> Path:
    points = np.array([[-0.5, 0.02], [-0.48, -0.02], [0.5, 0.01], [0.52, -0.01], [0.0, 0.6]])
    candidates = [
        {"name": "off_center", "center": [0.0, 0.4], "angle": 0.0, "width": 1.0},
        {"name": "balanced", "center": [0.0, 0.0], "angle": 0.0, "width": 1.0},
        {"name": "too_narrow", "center": [0.0, 0.0], "angle": 0.0, "width": 0.4},
    ]
    best = score_antipodal_grasps(points, candidates)[0]

    fig, ax = plt.subplots(figsize=(4.0, 3.2))
    _configure_axes(ax, "Point-cloud grasp scoring")
    ax.scatter(points[:, 0], points[:, 1], color=OKABE_ITO["blue"], s=45, label="points")
    _draw_gripper(ax, best.center, best.width, best.angle, OKABE_ITO["orange"], label=f"best: {best.name}")
    ax.legend(frameon=False, fontsize=8)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-0.8, 0.8)
    ax.set_ylim(-0.25, 0.8)
    return _save(fig, output_dir, "005_point_cloud_grasp_scoring")


def figure_006(output_dir: Path) -> Path:
    start = np.array([0.0, 0.0])
    goal = np.array([1.0, 1.0])
    obstacles = [(0.5, 0.5, 0.2)]
    path = np.array(rrt(start, goal, bounds=((0.0, 1.2), (0.0, 1.2)), obstacles=obstacles, step_size=0.15, max_iter=500, seed=4))
    assert path_is_collision_free(path, obstacles)

    fig, ax = plt.subplots(figsize=(4.0, 3.2))
    _configure_axes(ax, "RRT path around obstacle")
    for ox, oy, radius in obstacles:
        ax.add_patch(plt.Circle((ox, oy), radius, color=OKABE_ITO["vermillion"], alpha=0.25))
    ax.plot(path[:, 0], path[:, 1], "-o", color=OKABE_ITO["blue"], markersize=3, label="path")
    ax.scatter([start[0]], [start[1]], color=OKABE_ITO["green"], s=55, label="start")
    ax.scatter([goal[0]], [goal[1]], marker="*", color=OKABE_ITO["orange"], s=95, label="goal")
    ax.legend(frameon=False, fontsize=8)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-0.05, 1.25)
    ax.set_ylim(-0.05, 1.25)
    return _save(fig, output_dir, "006_rrt_motion_planning")


def figure_007(output_dir: Path) -> Path:
    trace = simulate_pd_mass(x0=0.0, v0=0.0, target=1.0, kp=25.0, kd=10.0, dt=0.01, steps=500)

    fig, ax = plt.subplots(figsize=(4.4, 3.0))
    _configure_axes(ax, "PD point-mass convergence", xlabel="time (s)", ylabel="position / velocity")
    ax.plot(trace.times, trace.positions, color=OKABE_ITO["blue"], label="position")
    ax.plot(trace.times, trace.velocities, color=OKABE_ITO["orange"], label="velocity")
    ax.axhline(1.0, color=OKABE_ITO["black"], linestyle=":", linewidth=1.0, label="target")
    ax.legend(frameon=False, fontsize=8)
    return _save(fig, output_dir, "007_pd_impedance_control")


def figure_008(output_dir: Path) -> Path:
    points = np.array([[-0.5, 0.0], [-0.45, 0.02], [0.45, -0.01], [0.5, 0.0], [0.0, 0.6], [1.2, 1.2]])
    mask = np.array([True, True, True, True, False, False])
    target_points = points[mask]
    candidates = [
        {"name": "target_object", "center": [0.0, 0.0], "angle": 0.0, "width": 1.0},
        {"name": "background", "center": [0.0, 0.6], "angle": 0.0, "width": 0.5},
    ]
    best = score_antipodal_grasps(target_points, candidates)[0]

    fig, ax = plt.subplots(figsize=(4.0, 3.2))
    _configure_axes(ax, "Segmentation to grasp pipeline")
    ax.scatter(points[~mask, 0], points[~mask, 1], color="#999999", s=45, label="background")
    ax.scatter(target_points[:, 0], target_points[:, 1], color=OKABE_ITO["blue"], s=50, label="segmented object")
    _draw_gripper(ax, best.center, best.width, best.angle, OKABE_ITO["orange"], label="downstream grasp")
    ax.legend(frameon=False, fontsize=8)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-0.8, 1.35)
    ax.set_ylim(-0.25, 1.35)
    return _save(fig, output_dir, "008_segmentation_pipeline_stub")


def figure_009(output_dir: Path) -> Path:
    env = GridGraspWorld(width=4, height=4, object_pos=(1, 0), start_pos=(0, 0))
    env.reset()
    trajectory = [(0, 0)]
    for action in ["right", "grasp"]:
        state, _, _, _ = env.step(action)
        trajectory.append(state.agent_pos)
    trajectory = np.array(trajectory)

    fig, ax = plt.subplots(figsize=(3.6, 3.4))
    _configure_axes(ax, "RL grasping gridworld", xlabel="grid x", ylabel="grid y")
    ax.set_xticks(range(4))
    ax.set_yticks(range(4))
    ax.set_xlim(-0.5, 3.5)
    ax.set_ylim(-0.5, 3.5)
    ax.set_aspect("equal", adjustable="box")
    ax.scatter([0], [0], color=OKABE_ITO["green"], s=70, label="start")
    ax.scatter([1], [0], marker="s", color=OKABE_ITO["orange"], s=85, label="object")
    ax.plot(trajectory[:, 0], trajectory[:, 1], "-o", color=OKABE_ITO["blue"], label="policy trace")
    ax.legend(frameon=False, fontsize=8)
    return _save(fig, output_dir, "009_rl_grasping_gridworld")


FIGURE_BUILDERS = [
    figure_001,
    figure_002,
    figure_003,
    figure_004,
    figure_005,
    figure_006,
    figure_007,
    figure_008,
    figure_009,
]


def generate_all_figures(output_dir: Path | str = Path("docs/assets/casebook")) -> list[Path]:
    """Generate all casebook figure assets and return their paths."""
    output_dir = Path(output_dir)
    return [builder(output_dir) for builder in FIGURE_BUILDERS]


def main() -> None:
    output_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/assets/casebook")
    generated = generate_all_figures(output_dir)
    for path in generated:
        print(path)


if __name__ == "__main__":
    main()
