# Robotic Manipulation Learning Repository Design

## Goal

Build a personal GitHub-ready learning repository for studying *Robotic Manipulation: Perception, Planning, and Control* chapter by chapter. The repository should function both as a study notebook and as a public casebook of runnable learning projects.

## Source Material

The current workspace contains chapter-split PDFs:

- Preface
- Chapter 1: Introduction
- Chapter 2: Let's get you a robot
- Chapter 3: Basic Pick and Place
- Chapter 4: Geometric Pose Estimation
- Chapter 5: Bin Picking
- Chapter 6: Mobile Manipulation
- Chapter 7: Motion Planning
- Chapter 8: Manipulator Control
- Chapter 9: Object Detection and Segmentation
- Chapter 10: Deep Perception for Manipulation
- Chapter 11: Reinforcement Learning
- Appendix A: Drake
- Appendix B: Manipulation Station
- Appendix C: Miscellaneous

The PDFs are treated as local reference material, not as generated study content. Public repository text should summarize concepts in the learner's own words and cite the course notes instead of copying long passages.

## Recommended Repository Shape

Use a chapter-driven repository with a casebook index.

```text
robotic-manipulation-learning/
  README.md
  ROADMAP.md
  CITATION.md
  requirements.txt
  environment.yml

  references/
    README.md

  chapters/
    ch01_introduction/
      README.md
      notes.md
      concepts/
      drake_labs/
      exercises.md
    ch02_robot_setup/
    ch03_basic_pick_and_place/
    ch04_geometric_pose_estimation/
    ch05_bin_picking/
    ch06_mobile_manipulation/
    ch07_motion_planning/
    ch08_manipulator_control/
    ch09_object_detection_segmentation/
    ch10_deep_perception/
    ch11_reinforcement_learning/

  casebook/
    001_spatial_transforms_numpy/
    002_forward_kinematics_planar_arm/
    003_differential_ik/
    004_icp_pose_estimation/
    005_point_cloud_grasp_scoring/
    006_rrt_motion_planning/
    007_pd_impedance_control/
    008_segmentation_pipeline_stub/
    009_rl_grasping_gridworld/

  docs/
    learning_log.md
    glossary.md
    math_notes.md
    github_publish_notes.md
```

## Learning Model

Each chapter gets two implementation levels:

1. Concept case: a low-dependency Python or notebook example that isolates the core idea.
2. Drake lab: a later pydrake-oriented example that connects the concept to the robotics simulation workflow.

This keeps the repository usable before the Drake environment is fully configured, while still leaving a path toward faithful robotics examples.

## Chapter Plan

### Chapter 1: Introduction

Purpose: frame manipulation as perception, planning, control, contact, uncertainty, and open-world decision making.

Repository outputs:

- Notes on why manipulation is broader than pick-and-place.
- A problem taxonomy table.
- A first learning log entry defining personal goals.

### Chapter 2: Let's Get You a Robot

Purpose: understand robot description formats, arms, hands, sensors, and the simulation interface.

Repository outputs:

- A hardware and software component map.
- A concept case that parses simple robot metadata from a small YAML file.
- A Drake lab placeholder documenting the future pydrake setup path.

### Chapter 3: Basic Pick and Place

Purpose: learn spatial transforms, monogram notation, forward kinematics, Jacobians, differential inverse kinematics, grasp poses, and pick-and-place trajectories.

Repository outputs:

- `001_spatial_transforms_numpy`
- `002_forward_kinematics_planar_arm`
- `003_differential_ik`
- Chapter notes with formulas and debugging checklists.

### Chapter 4: Geometric Pose Estimation

Purpose: learn depth sensing, geometry representations, point clouds, registration, ICP, partial views, outliers, free-space constraints, and tracking.

Repository outputs:

- `004_icp_pose_estimation`
- Notes on point cloud representations and registration failure modes.
- A synthetic point cloud example that can run without camera hardware.

### Chapter 5: Bin Picking

Purpose: learn cluttered scene generation, contact simulation nuance, model-based grasp selection, point-cloud grasp scoring, and task-level sequencing.

Repository outputs:

- `005_point_cloud_grasp_scoring`
- Notes on grasp scoring criteria and corner cases.
- A task-level state machine sketch.

### Chapter 6: Mobile Manipulation

Purpose: keep a placeholder because the local PDF is marked "Coming soon".

Repository outputs:

- A short note explaining that this chapter has no local content yet.
- A future-study checklist connecting mobile base planning to manipulation.

### Chapter 7: Motion Planning

Purpose: learn inverse kinematics, kinematic trajectory optimization, sampling-based planning, time-optimal parameterization, and graphs of convex sets.

Repository outputs:

- `006_rrt_motion_planning`
- Notes comparing IK, trajectory optimization, RRT-style methods, and convex-set planning.

### Chapter 8: Manipulator Control

Purpose: learn point-mass control intuition, manipulator equations, trajectory tracking, impedance-style behavior, and peg-in-hole style contact tasks.

Repository outputs:

- `007_pd_impedance_control`
- Notes separating kinematic planning from dynamic execution.

### Chapter 9: Object Detection and Segmentation

Purpose: understand object detection, segmentation, datasets, and how deep perception complements geometric methods.

Repository outputs:

- `008_segmentation_pipeline_stub`
- Notes on dataset construction and perception-to-manipulation interfaces.

### Chapter 10: Deep Perception for Manipulation

Purpose: study learned pose estimation, learned grasp selection, dense descriptors, task-level state, and manipulation-specific perception targets.

Repository outputs:

- Extension notes for case `008_segmentation_pipeline_stub`.
- A comparison table of perception tasks and downstream manipulation use.

### Chapter 11: Reinforcement Learning

Purpose: study RL interfaces, policy-gradient methods, value-based methods, and model-based RL in manipulation contexts.

Repository outputs:

- `009_rl_grasping_gridworld`
- Notes connecting policy learning to contact-rich manipulation.

## Casebook Standards

Each casebook item should include:

- `README.md` with the concept, learning goal, run command, expected output, and relation to the chapter.
- `src/` for implementation.
- `tests/` for focused checks where practical.
- `outputs/` for generated plots or logs, ignored unless small and useful.

The first implementation pass should prioritize clear, runnable examples over advanced realism.

## Tooling

Use Python as the default language.

Baseline dependencies:

- `numpy`
- `scipy`
- `matplotlib`
- `pytest`
- `pyyaml`

Optional later dependencies:

- `pydrake`
- computer vision and ML libraries for perception chapters
- RL environment libraries if needed for Chapter 11

## GitHub Readiness

The repository should include:

- A top-level README that explains the learning purpose and chapter map.
- A citation note for the original course notes.
- A roadmap that tracks chapter progress.
- A `.gitignore` that excludes caches, local environments, large generated artifacts, and local-only source PDFs unless the learner explicitly chooses to publish them.

## Testing Strategy

The first pass should test mathematical utilities and deterministic cases:

- Rotation and transform composition.
- Forward kinematics for a small planar arm.
- Differential IK shape and convergence behavior.
- ICP recovery on synthetic transformed points.
- RRT path validity on a small 2D map.
- PD control convergence in a simple simulated system.
- RL gridworld transition and reward logic.

Drake labs should be allowed to skip tests when pydrake is not installed, but each lab should include a documented environment check.

## Non-Goals

- Do not reproduce the full textbook content.
- Do not require Drake for the first useful version.
- Do not build a polished web app.
- Do not claim physical robot readiness.
- Do not publish large PDFs by default.

## Open Decisions

- GitHub remote name and visibility can be decided at publish time.
- Whether to include notebooks in addition to plain Python can be decided after the initial casebook skeleton is working.
- Drake installation should be documented before pydrake-specific labs are implemented.
