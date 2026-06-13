"""Generate the Jupyter Book notebooks used by the learning book."""

from __future__ import annotations

import json
from pathlib import Path


BOOK_ROOT = Path(__file__).resolve().parents[1] / "book"


COMMON_SETUP = """from pathlib import Path
import sys

PROJECT_ROOT = Path.cwd()
if not (PROJECT_ROOT / "src").exists():
    PROJECT_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

PROJECT_ROOT
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
                "本章把已知物体位姿转成机器人关节运动。主线是：transforms -> forward kinematics -> Jacobian -> differential IK。"
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
            markdown("Exercise: 把 target 改成 `[3.0, 0.0]`，解释为什么误差无法真正变成 0。"),
        ]
    ),
    "03_geometric_perception_icp.ipynb": notebook(
        [
            markdown("# 03 Geometric Perception And ICP\n\n物体位姿不再给定时，机器人要从点云中估计刚体变换。"),
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
            markdown(
                "ICP 的失败模式：初始对齐太差、局部最优、点云遮挡、离群点、物体对称。"
                "\n\nExercise: 给 target 加一个离群点，观察 mean error 如何变化。"
            ),
        ]
    ),
    "04_grasp_scoring.ipynb": notebook(
        [
            markdown("# 04 Grasp Scoring\n\nBin picking 中常常不需要完整识别物体，也可以根据点云选择合理抓取。"),
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
            markdown("Exercise: 增加一个偏心候选，说明为什么它的接触更不均衡。"),
        ]
    ),
    "05_motion_planning_rrt.ipynb": notebook(
        [
            markdown("# 05 Motion Planning With RRT\n\nIK 只回答目标是否可达，planning 回答路径是否可行。"),
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
            markdown("Exercise: 增大 obstacle radius，观察何时 RRT 更难找到路径。"),
        ]
    ),
    "06_control_pd_impedance.ipynb": notebook(
        [
            markdown("# 06 Control: PD And Impedance Intuition\n\nPlanning 给期望轨迹，control 处理真实动态响应。"),
            code(COMMON_SETUP),
            code(
                "from rml.control import simulate_pd_mass\n\n"
                "trace = simulate_pd_mass(x0=0.0, v0=0.0, target=1.0, kp=25.0, kd=10.0, dt=0.01, steps=500)\n"
                "trace.positions[-1], trace.velocities[-1], max(abs(trace.controls))"
            ),
            markdown("Exercise: 降低 `kd`，观察系统是否更容易振荡。"),
        ]
    ),
    "07_segmentation_to_grasp.ipynb": notebook(
        [
            markdown("# 07 Segmentation To Grasp\n\n深度感知常常不是直接输出动作，而是先选择哪些点属于目标物体。"),
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
            markdown("Exercise: 把一个 background point 错误加入 mask，解释下游 grasp score 会怎样受影响。"),
        ]
    ),
    "08_rl_gridworld.ipynb": notebook(
        [
            markdown("# 08 RL Grasping Gridworld\n\nRL 用 state、action、reward、transition 和 policy 表达交互学习。"),
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
