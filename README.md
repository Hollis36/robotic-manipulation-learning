# Robotic Manipulation Learning

这是我的机器人操作学习仓库，围绕 *Robotic Manipulation: Perception, Planning, and Control* 建立章节笔记、数学推导、可运行小案例和后续 Drake 实验。

The repository is organized as a personal learning casebook rather than a copy of the source notes. Each chapter has a study folder, and the `casebook/` directory contains runnable examples that turn core ideas into code.

## Repository Map

```text
chapters/    Chapter-by-chapter notes, exercises, and Drake lab notes.
casebook/    Runnable learning cases with small deterministic examples.
src/rml/     Shared Python utilities used by the casebook and tests.
tests/       Pytest coverage for math, perception, planning, control, and RL utilities.
docs/        Learning log, glossary, math notes, and GitHub publishing notes.
references/ How local source PDFs are used without republishing them.
```

## First Casebook Track

| Case | Topic | Related chapter |
| --- | --- | --- |
| `001_spatial_transforms_numpy` | 2D rotations and homogeneous transforms | Chapter 3 |
| `002_forward_kinematics_planar_arm` | Planar arm forward kinematics | Chapter 3 |
| `003_differential_ik` | Jacobian-based differential IK | Chapter 3 |
| `004_icp_pose_estimation` | Synthetic ICP pose recovery | Chapter 4 |
| `005_point_cloud_grasp_scoring` | Point-cloud grasp scoring | Chapter 5 |
| `006_rrt_motion_planning` | RRT path planning in 2D | Chapter 7 |
| `007_pd_impedance_control` | PD-controlled point-mass behavior | Chapter 8 |
| `008_segmentation_pipeline_stub` | Segmentation-to-manipulation data flow | Chapters 9-10 |
| `009_rl_grasping_gridworld` | Small RL grasping gridworld | Chapter 11 |

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
pytest -q
```

For quick scripts without editable install:

```bash
PYTHONPATH=src python casebook/001_spatial_transforms_numpy/run.py
```

## Learning Principles

- Write notes in my own words.
- Turn each important concept into a minimal executable example.
- Keep low-dependency concept cases useful before Drake is installed.
- Add Drake labs gradually once the environment is stable.
- Track confusion explicitly instead of hiding it.

## Source Notes

The local PDFs are used as study references only. They are ignored by Git by default. See `CITATION.md` and `references/README.md` for citation and source-handling notes.

