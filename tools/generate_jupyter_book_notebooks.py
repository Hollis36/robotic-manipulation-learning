"""Generate the Jupyter Book notebooks used by the learning book."""

from __future__ import annotations

import json
from pathlib import Path


BOOK_ROOT = Path(__file__).resolve().parents[1] / "book"


COMMON_SETUP = """from pathlib import Path
import sys

COLAB_REPO_URL = "https://github.com/Hollis36/robotic-manipulation-learning.git"

PROJECT_ROOT = Path.cwd()
if not (PROJECT_ROOT / "src").exists():
    in_colab = "google.colab" in sys.modules
    if in_colab:
        import subprocess

        PROJECT_ROOT = Path("/content/robotic-manipulation-learning")
        if not PROJECT_ROOT.exists():
            # Equivalent command: git clone --depth 1 <repo> <target>
            subprocess.run(["git", "clone", "--depth", "1", COLAB_REPO_URL, str(PROJECT_ROOT)], check=True)
    else:
        PROJECT_ROOT = PROJECT_ROOT.parent

if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

PROJECT_ROOT
"""

PLOT_SETUP = """import matplotlib.pyplot as plt
plt.rcParams.update({
    "figure.figsize": (7, 4.2),
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
})
"""


def markdown(source: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": source}


def code(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source,
    }


def concept_image_markdown(filename: str, caption: str) -> dict:
    return markdown(
        "## Concept Map\n\n"
        f"![Colab concept image](assets/colab/{filename})\n\n"
        f"**Concept image.** {caption}"
    )


def result_figure_intro(description: str) -> dict:
    return markdown(
        "## Result Figure\n\n"
        f"{description}\n\n"
        "The figure below is generated from the values computed in this notebook. "
        "Treat it as evidence from the code, not as a decorative illustration."
    )


def parameter_experiment(text: str) -> dict:
    return markdown(
        "## Parameter Experiment\n\n"
        "The next cell is marked with `COLAB_PARAMETER_EXPERIMENT` so it is easy to find in Colab. "
        + text
    )


def reflection_prompt(text: str) -> dict:
    return markdown("## Reflection Prompt\n\n" + text)


def learning_scaffold(
    summary: str,
    objectives: list[str],
    checkpoint: list[str],
    practice: str,
    figure: str,
    alt: str,
) -> str:
    return (
        f"{summary}\n\n"
        f"![{alt}](assets/figures/{figure}.png)\n\n"
        "## Learning Objectives\n\n"
        + "\n".join(f"- {item}" for item in objectives)
        + "\n\n## Checkpoint\n\n"
        + "\n".join(f"- {item}" for item in checkpoint)
        + "\n\n## Practice Task\n\n"
        + practice
    )


def notebook(cells: list[dict]) -> dict:
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "pygments_lexer": "ipython3",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


NOTEBOOKS = {
    "02_transforms_kinematics_ik.ipynb": notebook(
        [
            markdown(
                "# 02 Transforms, Kinematics, And IK\n\n"
                + learning_scaffold(
                    "本章把已知物体位姿转成机器人关节运动。主线是：transforms -> forward kinematics -> Jacobian -> differential IK。",
                    [
                        "Use frame names to compose 2D rigid transforms without losing direction.",
                        "Connect forward kinematics to the planar manipulator Jacobian.",
                        "Explain why differential IK is local, iterative, and target-limited by reachability.",
                    ],
                    [
                        "Given `A_from_B` and `B_from_C`, write the composed transform in the correct order.",
                        "Predict which Jacobian column changes most when a joint is near the base.",
                        "Run the IK cell and explain the final error in task-space terms.",
                    ],
                    "Modify the IK target twice: one reachable point and one unreachable point. Record the final error and explain the difference in one paragraph.",
                    "02_transforms_kinematics_ik",
                    "Transforms, kinematics, and IK visual map",
                )
            ),
            concept_image_markdown(
                "02_transforms_kinematics_ik_concept.png",
                "Frames define where objects are; kinematics and the Jacobian turn frame error into joint updates.",
            ),
            code(COMMON_SETUP),
            markdown("## Spatial Transform Composition\n\n命名规则：`A_from_B @ B_from_C = A_from_C`。"),
            code(
                "import numpy as np\n"
                "from rml.transforms import apply_transform, compose, make_transform\n\n"
                "world_from_gripper = make_transform(np.pi / 2, [0.5, 0.2])\n"
                "gripper_from_brick = make_transform(0.0, [0.1, 0.0])\n"
                "world_from_brick = compose(world_from_gripper, gripper_from_brick)\n"
                "brick_origin_world = apply_transform(world_from_brick, np.array([[0.0, 0.0]]))[0]\n"
                "np.round(world_from_brick, 3), np.round(brick_origin_world, 3)"
            ),
            markdown("## Forward Kinematics And Jacobian\n\nFK 回答“现在末端在哪里”，Jacobian 回答“每个关节微小变化如何影响末端”。"),
            code(
                "from rml.kinematics import planar_forward_kinematics, planar_jacobian\n\n"
                "q = np.array([0.4, -0.2, 0.3])\n"
                "links = np.array([0.7, 0.5, 0.2])\n"
                "position = planar_forward_kinematics(q, links)\n"
                "jacobian = planar_jacobian(q, links)\n"
                "np.round(position, 3), np.round(jacobian, 3)"
            ),
            markdown("## Differential IK\n\n微分 IK 使用局部线性近似，一步一步减小 task-space error。"),
            code(
                "from rml.differential_ik import solve_planar_position_ik\n\n"
                "target = np.array([1.3, 0.7])\n"
                "initial_q = np.array([0.1, 0.1, -0.2])\n"
                "result = solve_planar_position_ik(initial_q, target, np.array([1.0, 0.8, 0.4]), steps=200, damping=0.05, gain=0.6)\n"
                "final_position = planar_forward_kinematics(result.joint_angles, np.array([1.0, 0.8, 0.4]))\n"
                "np.round(result.joint_angles, 3), np.round(final_position, 3), result.error_norm"
            ),
            result_figure_intro("Plot the final planar arm, the desired target, and the remaining end-effector error."),
            code(
                PLOT_SETUP
                + "import numpy as np\n\n"
                "links = np.array([1.0, 0.8, 0.4])\n"
                "cumulative_angles = np.cumsum(result.joint_angles)\n"
                "segments = np.column_stack((links * np.cos(cumulative_angles), links * np.sin(cumulative_angles)))\n"
                "points = np.vstack((np.array([[0.0, 0.0]]), np.cumsum(segments, axis=0)))\n"
                "fig, ax = plt.subplots()\n"
                "ax.plot(points[:, 0], points[:, 1], '-o', lw=4, label='final arm')\n"
                "ax.scatter([target[0]], [target[1]], marker='*', s=180, label='target')\n"
                "ax.scatter([final_position[0]], [final_position[1]], s=90, label='end effector')\n"
                "ax.plot([final_position[0], target[0]], [final_position[1], target[1]], '--', label=f'error={result.error_norm:.3f}')\n"
                "ax.set_aspect('equal', adjustable='box')\n"
                "ax.set_xlabel('x position')\n"
                "ax.set_ylabel('y position')\n"
                "ax.legend(frameon=False)\n"
                "plt.show()"
            ),
            parameter_experiment("Change `target_options` and compare how final error changes for reachable and unreachable targets."),
            code(
                "# COLAB_PARAMETER_EXPERIMENT\n"
                "target_options = [np.array([1.3, 0.7]), np.array([2.0, 0.1]), np.array([3.0, 0.0])]\n"
                "for candidate in target_options:\n"
                "    trial = solve_planar_position_ik(initial_q, candidate, np.array([1.0, 0.8, 0.4]), steps=200, damping=0.05, gain=0.6)\n"
                "    print(candidate.tolist(), 'final_error=', round(trial.error_norm, 4))"
            ),
            reflection_prompt("为什么不可达目标的误差不会归零？用 link length 总和和 task-space error 解释。"),
            markdown("Exercise: 把 target 改成 `[3.0, 0.0]`，解释为什么误差无法真正变成 0。"),
        ]
    ),
    "03_geometric_perception_icp.ipynb": notebook(
        [
            markdown(
                "# 03 Geometric Perception And ICP\n\n"
                + learning_scaffold(
                    "物体位姿不再给定时，机器人要从点云中估计刚体变换。",
                    [
                        "Describe ICP as alternating correspondence search and rigid transform fitting.",
                        "Identify when geometric registration is a good fit for manipulation.",
                        "Name the common failure modes caused by symmetry, occlusion, and poor initialization.",
                    ],
                    [
                        "Run the ICP example and identify the estimated rotation and translation.",
                        "Explain why low mean error does not always mean the correct object pose.",
                        "List one setup change that would make ICP more robust.",
                    ],
                    "Add noise or an outlier to the target points, rerun ICP, and write down how the error and estimated transform change.",
                    "03_geometric_perception_icp",
                    "ICP point cloud alignment visual map",
                )
            ),
            concept_image_markdown(
                "03_geometric_perception_icp_concept.png",
                "ICP alternates between nearest-neighbor correspondences and a rigid transform fit.",
            ),
            code(COMMON_SETUP),
            code(
                "import numpy as np\n"
                "from rml.icp import icp\n"
                "from rml.transforms import apply_transform, make_transform\n\n"
                "source = np.array([[0.0, 0.0], [0.4, 0.1], [0.2, 0.7], [0.9, 0.6], [1.0, 0.0]])\n"
                "target = apply_transform(make_transform(0.15, [0.2, -0.1]), source)\n"
                "result = icp(source, target, iterations=30, tolerance=1e-10)\n"
                "np.round(result.rotation, 3), np.round(result.translation, 3), result.mean_error"
            ),
            result_figure_intro("Compare the original source points, target points, transformed source points, and nearest correspondences."),
            code(
                PLOT_SETUP
                + "distances = np.linalg.norm(result.transformed_source[:, None, :] - target[None, :, :], axis=2)\n"
                "matches = target[np.argmin(distances, axis=1)]\n"
                "fig, ax = plt.subplots()\n"
                "ax.scatter(source[:, 0], source[:, 1], s=80, label='source', alpha=0.55)\n"
                "ax.scatter(target[:, 0], target[:, 1], s=80, label='target')\n"
                "ax.scatter(result.transformed_source[:, 0], result.transformed_source[:, 1], marker='x', s=100, label='transformed source')\n"
                "for transformed_point, matched_point in zip(result.transformed_source, matches):\n"
                "    ax.plot([transformed_point[0], matched_point[0]], [transformed_point[1], matched_point[1]], color='0.55', lw=1)\n"
                "ax.set_aspect('equal', adjustable='box')\n"
                "ax.set_xlabel('x position')\n"
                "ax.set_ylabel('y position')\n"
                "ax.legend(frameon=False)\n"
                "plt.show()"
            ),
            parameter_experiment("Change `noise_scale` and observe how registration error changes under deterministic target perturbations."),
            code(
                "# COLAB_PARAMETER_EXPERIMENT\n"
                "rng = np.random.default_rng(7)\n"
                "for noise_scale in [0.0, 0.02, 0.08]:\n"
                "    noisy_target = target + rng.normal(0.0, noise_scale, size=target.shape)\n"
                "    trial = icp(source, noisy_target, iterations=30, tolerance=1e-10)\n"
                "    print('noise_scale=', noise_scale, 'mean_error=', round(trial.mean_error, 4))"
            ),
            reflection_prompt("什么时候 mean error 很低但姿态仍然可能不可信？结合对称物体、遮挡和初始化解释。"),
            markdown(
                "ICP 的失败模式：初始对齐太差、局部最优、点云遮挡、离群点、物体对称。"
                "\n\nExercise: 给 target 加一个离群点，观察 mean error 如何变化。"
            ),
        ]
    ),
    "04_grasp_scoring.ipynb": notebook(
        [
            markdown(
                "# 04 Grasp Scoring\n\n"
                + learning_scaffold(
                    "Bin picking 中常常不需要完整识别物体，也可以根据点云选择合理抓取。",
                    [
                        "Explain the difference between recognizing an object and selecting a feasible grasp.",
                        "Read a simple antipodal grasp score from contact balance and gripper width.",
                        "Connect grasp scoring errors to point cloud coverage and candidate generation.",
                    ],
                    [
                        "Run the scoring cell and identify why the balanced candidate wins.",
                        "Explain what happens when a candidate is too narrow.",
                        "Name one physical constraint missing from this simplified scorer.",
                    ],
                    "Create one new candidate grasp, predict its score qualitatively, then run the cell and compare your prediction with the output.",
                    "04_grasp_scoring",
                    "Grasp scoring visual map",
                )
            ),
            concept_image_markdown(
                "04_grasp_scoring_concept.png",
                "A grasp scorer turns local point support and gripper geometry into ranked grasp candidates.",
            ),
            code(COMMON_SETUP),
            code(
                "import numpy as np\n"
                "from rml.grasp_scoring import score_antipodal_grasps\n\n"
                "points = np.array([[-0.5, 0.02], [-0.48, -0.02], [0.5, 0.01], [0.52, -0.01], [0.0, 0.6]])\n"
                "candidates = [\n"
                "    {\"name\": \"off_center\", \"center\": [0.0, 0.4], \"angle\": 0.0, \"width\": 1.0},\n"
                "    {\"name\": \"balanced\", \"center\": [0.0, 0.0], \"angle\": 0.0, \"width\": 1.0},\n"
                "    {\"name\": \"too_narrow\", \"center\": [0.0, 0.0], \"angle\": 0.0, \"width\": 0.4},\n"
                "]\n"
                "scores = score_antipodal_grasps(points, candidates)\n"
                "[(s.name, round(s.score, 2), s.left_contacts, s.right_contacts) for s in scores]"
            ),
            result_figure_intro("Show the point cloud next to a score chart so the ranking can be checked against contact evidence."),
            code(
                PLOT_SETUP
                + "fig, (ax_points, ax_scores) = plt.subplots(1, 2, figsize=(8.5, 3.6))\n"
                "ax_points.scatter(points[:, 0], points[:, 1], s=85, label='points')\n"
                "for candidate in candidates:\n"
                "    center = np.asarray(candidate['center'], dtype=float)\n"
                "    ax_points.scatter([center[0]], [center[1]], marker='x', s=90, label=candidate['name'])\n"
                "ax_points.set_aspect('equal', adjustable='box')\n"
                "ax_points.set_xlabel('closing axis')\n"
                "ax_points.set_ylabel('approach axis')\n"
                "ax_points.legend(frameon=False, fontsize=8)\n"
                "names = [score.name for score in scores]\n"
                "values = [score.score for score in scores]\n"
                "ax_scores.bar(names, values, color=['#4C78A8', '#F58518', '#54A24B'])\n"
                "ax_scores.set_ylabel('score')\n"
                "ax_scores.tick_params(axis='x', rotation=25)\n"
                "fig.tight_layout()\n"
                "plt.show()"
            ),
            parameter_experiment("Change the candidate gripper widths and print the resulting score ranking."),
            code(
                "# COLAB_PARAMETER_EXPERIMENT\n"
                "for width in [0.4, 0.8, 1.0, 1.4]:\n"
                "    width_candidates = [dict(candidate, width=width) for candidate in candidates]\n"
                "    ranking = score_antipodal_grasps(points, width_candidates)\n"
                "    print('width=', width, [(score.name, round(score.score, 2)) for score in ranking])"
            ),
            reflection_prompt("为什么 balanced candidate 比 off_center 更可靠？从左右接触数量和夹爪宽度两方面说明。"),
            markdown("Exercise: 增加一个偏心候选，说明为什么它的接触更不均衡。"),
        ]
    ),
    "05_motion_planning_rrt.ipynb": notebook(
        [
            markdown(
                "# 05 Motion Planning With RRT\n\n"
                + learning_scaffold(
                    "IK 只回答目标是否可达，planning 回答路径是否可行。",
                    [
                        "Separate goal feasibility from path feasibility.",
                        "Describe how RRT grows a collision-free tree through sampling.",
                        "Relate planner parameters such as step size and max iterations to success rate.",
                    ],
                    [
                        "Run the RRT example and verify that the returned path is collision-free.",
                        "Explain why the first and last path points matter.",
                        "Identify one obstacle change that makes the planning problem harder.",
                    ],
                    "Increase the obstacle radius in small steps and record the first setting where planning becomes unreliable.",
                    "05_motion_planning_rrt",
                    "RRT motion planning visual map",
                )
            ),
            concept_image_markdown(
                "05_motion_planning_rrt_concept.png",
                "RRT grows a collision-free search tree and extracts a path once it connects start to goal.",
            ),
            code(COMMON_SETUP),
            code(
                "import numpy as np\n"
                "from rml.rrt import path_is_collision_free, rrt\n\n"
                "start = np.array([0.0, 0.0])\n"
                "goal = np.array([1.0, 1.0])\n"
                "obstacles = [(0.5, 0.5, 0.2)]\n"
                "path = np.array(rrt(start, goal, bounds=((0.0, 1.2), (0.0, 1.2)), obstacles=obstacles, step_size=0.15, max_iter=500, seed=4))\n"
                "len(path), path_is_collision_free(path, obstacles), np.round(path[0], 3), np.round(path[-1], 3)"
            ),
            result_figure_intro("Draw the obstacle, planned waypoints, start, and goal to verify the path visually."),
            code(
                PLOT_SETUP
                + "fig, ax = plt.subplots()\n"
                "for ox, oy, radius in obstacles:\n"
                "    ax.add_patch(plt.Circle((ox, oy), radius, color='#E45756', alpha=0.35, label='obstacle'))\n"
                "ax.plot(path[:, 0], path[:, 1], '-o', lw=3, label='RRT path')\n"
                "ax.scatter([start[0]], [start[1]], s=120, marker='s', label='start')\n"
                "ax.scatter([goal[0]], [goal[1]], s=160, marker='*', label='goal')\n"
                "ax.set_xlim(-0.05, 1.25)\n"
                "ax.set_ylim(-0.05, 1.25)\n"
                "ax.set_aspect('equal', adjustable='box')\n"
                "ax.set_xlabel('x position')\n"
                "ax.set_ylabel('y position')\n"
                "ax.legend(frameon=False)\n"
                "plt.show()"
            ),
            parameter_experiment("Change `obstacle_radius` and print whether the deterministic planner finds a path and how long it is."),
            code(
                "# COLAB_PARAMETER_EXPERIMENT\n"
                "for obstacle_radius in [0.12, 0.2, 0.28]:\n"
                "    trial_obstacles = [(0.5, 0.5, obstacle_radius)]\n"
                "    try:\n"
                "        trial_path = np.array(rrt(start, goal, bounds=((0.0, 1.2), (0.0, 1.2)), obstacles=trial_obstacles, step_size=0.15, max_iter=500, seed=4))\n"
                "        path_length = float(np.sum(np.linalg.norm(np.diff(trial_path, axis=0), axis=1)))\n"
                "        print('radius=', obstacle_radius, 'waypoints=', len(trial_path), 'path_length=', round(path_length, 3))\n"
                "    except RuntimeError:\n"
                "        print('radius=', obstacle_radius, 'failure')"
            ),
            reflection_prompt("RRT 找到路径时，为什么还要检查每一段 path 是否 collision-free？结合采样、步长和障碍物半径解释。"),
            markdown("Exercise: 增大 obstacle radius，观察何时 RRT 更难找到路径。"),
        ]
    ),
    "06_control_pd_impedance.ipynb": notebook(
        [
            markdown(
                "# 06 Control: PD And Impedance Intuition\n\n"
                + learning_scaffold(
                    "Planning 给期望轨迹，control 处理真实动态响应。",
                    [
                        "Interpret proportional gain as position-error correction.",
                        "Interpret derivative gain as damping.",
                        "Connect control tuning to overshoot, settling, and force limits.",
                    ],
                    [
                        "Run the PD simulation and read the final position, velocity, and max control.",
                        "Explain what changes when damping is reduced.",
                        "Name one reason a stable simulation may still be unsafe on hardware.",
                    ],
                    "Try three `kd` values while keeping `kp` fixed. Summarize which response you would trust most for a real manipulator and why.",
                    "06_control_pd_impedance",
                    "PD and impedance control visual map",
                )
            ),
            concept_image_markdown(
                "06_control_pd_impedance_concept.png",
                "PD control can be read as a virtual spring and damper driving position error toward zero.",
            ),
            code(COMMON_SETUP),
            code(
                "from rml.control import simulate_pd_mass\n\n"
                "trace = simulate_pd_mass(x0=0.0, v0=0.0, target=1.0, kp=25.0, kd=10.0, dt=0.01, steps=500)\n"
                "trace.positions[-1], trace.velocities[-1], max(abs(trace.controls))"
            ),
            result_figure_intro("Plot the simulated position response against the target to inspect overshoot and settling."),
            code(
                PLOT_SETUP
                + "target = 1.0\n"
                "fig, ax = plt.subplots()\n"
                "ax.plot(trace.times, trace.positions, lw=3, label='position')\n"
                "ax.axhline(target, color='#E45756', linestyle='--', label='target')\n"
                "ax.set_xlabel('time (s)')\n"
                "ax.set_ylabel('position')\n"
                "ax.legend(frameon=False)\n"
                "plt.show()"
            ),
            parameter_experiment("Change derivative gain values and compare the maximum overshoot for each response."),
            code(
                "# COLAB_PARAMETER_EXPERIMENT\n"
                + PLOT_SETUP
                + "import numpy as np\n\n"
                "kd_values = [2.0, 6.0, 10.0, 18.0]\n"
                "fig, ax = plt.subplots()\n"
                "for kd in kd_values:\n"
                "    trial = simulate_pd_mass(x0=0.0, v0=0.0, target=1.0, kp=25.0, kd=kd, dt=0.01, steps=500)\n"
                "    overshoot = max(0.0, float(np.max(trial.positions) - 1.0))\n"
                "    ax.plot(trial.times, trial.positions, label=f'kd={kd}')\n"
                "    print('kd=', kd, 'max_overshoot=', round(overshoot, 4))\n"
                "ax.axhline(1.0, color='#E45756', linestyle='--', label='target')\n"
                "ax.set_xlabel('time (s)')\n"
                "ax.set_ylabel('position')\n"
                "ax.legend(frameon=False)\n"
                "plt.show()"
            ),
            reflection_prompt("如果 `kd` 太小或太大，真实机械臂上分别可能出现什么问题？用 overshoot、settling 和控制力限制回答。"),
            markdown("Exercise: 降低 `kd`，观察系统是否更容易振荡。"),
        ]
    ),
    "07_segmentation_to_grasp.ipynb": notebook(
        [
            markdown(
                "# 07 Segmentation To Grasp\n\n"
                + learning_scaffold(
                    "深度感知常常不是直接输出动作，而是先选择哪些点属于目标物体。",
                    [
                        "Trace how a segmentation mask changes the point cloud passed to grasp scoring.",
                        "Explain false positives and false negatives as downstream manipulation errors.",
                        "Distinguish perception quality from end-to-end task success.",
                    ],
                    [
                        "Run the mask example and identify how many points are treated as target points.",
                        "Explain why a background point can corrupt a grasp score.",
                        "Name one evaluation metric that checks manipulation impact, not just segmentation accuracy.",
                    ],
                    "Flip one mask value at a time and record which mistake damages the selected grasp most.",
                    "07_segmentation_to_grasp",
                    "Segmentation to grasp visual map",
                )
            ),
            concept_image_markdown(
                "07_segmentation_to_grasp_concept.png",
                "A segmentation mask decides which points reach the grasp scorer, so perception errors become grasp errors.",
            ),
            code(COMMON_SETUP),
            code(
                "import numpy as np\n"
                "from rml.grasp_scoring import score_antipodal_grasps\n\n"
                "points = np.array([[-0.5, 0.0], [-0.45, 0.02], [0.45, -0.01], [0.5, 0.0], [0.0, 0.6], [1.2, 1.2]])\n"
                "mask = np.array([True, True, True, True, False, False])\n"
                "target_points = points[mask]\n"
                "candidates = [\n"
                "    {\"name\": \"target_object\", \"center\": [0.0, 0.0], \"angle\": 0.0, \"width\": 1.0},\n"
                "    {\"name\": \"background\", \"center\": [0.0, 0.6], \"angle\": 0.0, \"width\": 0.5},\n"
                "]\n"
                "best = score_antipodal_grasps(target_points, candidates)[0]\n"
                "len(target_points), best.name, round(best.score, 2)"
            ),
            result_figure_intro("Plot all observed points, the selected mask points, and the center of the best grasp candidate."),
            code(
                PLOT_SETUP
                + "fig, ax = plt.subplots()\n"
                "ax.scatter(points[:, 0], points[:, 1], s=85, color='0.7', label='all points')\n"
                "ax.scatter(target_points[:, 0], target_points[:, 1], s=95, label='selected mask points')\n"
                "ax.scatter([best.center[0]], [best.center[1]], marker='x', s=140, label=f'best: {best.name}')\n"
                "ax.set_aspect('equal', adjustable='box')\n"
                "ax.set_xlabel('x position')\n"
                "ax.set_ylabel('y position')\n"
                "ax.legend(frameon=False)\n"
                "plt.show()"
            ),
            parameter_experiment("Flip one mask value at a time and print which grasp becomes best after each perception mistake."),
            code(
                "# COLAB_PARAMETER_EXPERIMENT\n"
                "for flip_index in range(len(mask)):\n"
                "    trial_mask = mask.copy()\n"
                "    trial_mask[flip_index] = ~trial_mask[flip_index]\n"
                "    trial_points = points[trial_mask]\n"
                "    trial_best = score_antipodal_grasps(trial_points, candidates)[0]\n"
                "    print('flipped_index=', flip_index, 'selected_points=', len(trial_points), 'best=', trial_best.name, 'score=', round(trial_best.score, 2))"
            ),
            reflection_prompt("哪一种 mask 错误最危险：漏掉目标点，还是加入背景点？请用 best grasp 的变化解释。"),
            markdown("Exercise: 把一个 background point 错误加入 mask，解释下游 grasp score 会怎样受影响。"),
        ]
    ),
    "08_rl_gridworld.ipynb": notebook(
        [
            markdown(
                "# 08 RL Grasping Gridworld\n\n"
                + learning_scaffold(
                    "RL 用 state、action、reward、transition 和 policy 表达交互学习。",
                    [
                        "Map a manipulation problem into state, action, reward, transition, and policy.",
                        "Explain why reward design changes what the agent learns.",
                        "Use a tiny gridworld to reason about exploration before moving to robot simulators.",
                    ],
                    [
                        "Run the trajectory cell and identify the state after each action.",
                        "Explain what event produces the positive reward.",
                        "Describe how the shortest action sequence changes when the object moves.",
                    ],
                    "Move the object to a new grid cell and write a shortest successful action sequence before running it.",
                    "08_rl_gridworld",
                    "RL gridworld visual map",
                )
            ),
            concept_image_markdown(
                "08_rl_gridworld_concept.png",
                "A tiny gridworld makes state, action, transition, reward, and policy choices inspectable.",
            ),
            code(COMMON_SETUP),
            code(
                "from rml.gridworld import GridGraspWorld\n\n"
                "env = GridGraspWorld(width=4, height=4, object_pos=(1, 0), start_pos=(0, 0))\n"
                "state = env.reset()\n"
                "trajectory = [(\"reset\", state, 0.0, False)]\n"
                "for action in [\"right\", \"grasp\"]:\n"
                "    state, reward, done, info = env.step(action)\n"
                "    trajectory.append((action, state, reward, done, info[\"event\"]))\n"
                "trajectory"
            ),
            result_figure_intro("Draw the grid, executed trajectory, object position, and final reward event."),
            code(
                PLOT_SETUP
                + "fig, ax = plt.subplots(figsize=(4.8, 4.8))\n"
                "for x in range(env.width + 1):\n"
                "    ax.axvline(x - 0.5, color='0.75', lw=1)\n"
                "for y in range(env.height + 1):\n"
                "    ax.axhline(y - 0.5, color='0.75', lw=1)\n"
                "positions = [entry[1].agent_pos for entry in trajectory]\n"
                "for start_cell, end_cell in zip(positions, positions[1:]):\n"
                "    if start_cell != end_cell:\n"
                "        ax.annotate('', xy=end_cell, xytext=start_cell, arrowprops={'arrowstyle': '->', 'lw': 2})\n"
                "ax.scatter([env.start_pos[0]], [env.start_pos[1]], marker='s', s=150, label='start')\n"
                "ax.scatter([env.object_pos[0]], [env.object_pos[1]], marker='*', s=220, label='object')\n"
                "ax.scatter([positions[-1][0]], [positions[-1][1]], marker='x', s=160, label='final agent')\n"
                "final_event = trajectory[-1][-1]\n"
                "final_reward = trajectory[-1][2]\n"
                "ax.set_title(f'final reward={final_reward:.1f}, event={final_event}')\n"
                "ax.set_xlim(-0.5, env.width - 0.5)\n"
                "ax.set_ylim(-0.5, env.height - 0.5)\n"
                "ax.set_xticks(range(env.width))\n"
                "ax.set_yticks(range(env.height))\n"
                "ax.set_aspect('equal', adjustable='box')\n"
                "ax.legend(frameon=False, loc='upper left')\n"
                "plt.show()"
            ),
            parameter_experiment("Move the object and print the outcome of a shortest handwritten action sequence."),
            code(
                "# COLAB_PARAMETER_EXPERIMENT\n"
                "def shortest_actions(start_pos, object_pos):\n"
                "    actions = []\n"
                "    dx = object_pos[0] - start_pos[0]\n"
                "    dy = object_pos[1] - start_pos[1]\n"
                "    actions.extend(['right'] * max(0, dx))\n"
                "    actions.extend(['left'] * max(0, -dx))\n"
                "    actions.extend(['up'] * max(0, dy))\n"
                "    actions.extend(['down'] * max(0, -dy))\n"
                "    return actions + ['grasp']\n\n"
                "for object_pos in [(1, 0), (2, 1), (3, 3)]:\n"
                "    trial_env = GridGraspWorld(width=4, height=4, object_pos=object_pos, start_pos=(0, 0))\n"
                "    state = trial_env.reset()\n"
                "    total_reward = 0.0\n"
                "    event = 'reset'\n"
                "    actions = shortest_actions(trial_env.start_pos, object_pos)\n"
                "    for action in actions:\n"
                "        state, reward, done, info = trial_env.step(action)\n"
                "        total_reward += reward\n"
                "        event = info['event']\n"
                "        if done:\n"
                "            break\n"
                "    print('object_pos=', object_pos, 'actions=', actions, 'event=', event, 'total_reward=', round(total_reward, 2), 'holding=', state.holding_object)"
            ),
            reflection_prompt("为什么同一个 reward 规则在 object_pos 改变后仍然能评价成功？说明 state、action sequence 和 terminal reward 的关系。"),
            markdown("Exercise: 改变 object_pos，写出新的最短 action sequence。"),
        ]
    ),
}


def main() -> None:
    BOOK_ROOT.mkdir(parents=True, exist_ok=True)
    for name, content in NOTEBOOKS.items():
        path = BOOK_ROOT / name
        path.write_text(json.dumps(content, indent=2, ensure_ascii=False) + "\n")
        print(path)


if __name__ == "__main__":
    main()
