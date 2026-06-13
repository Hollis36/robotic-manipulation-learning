# Teaching Guide

## Teaching Contract

I will teach this course as a stack-building sequence. Each lesson should have:

- one mental model,
- one concrete manipulation task,
- one failure mode,
- one connection to the repository,
- one short exercise.

## Lesson Sequence

### Lesson 0: The Manipulation Stack

Goal: understand why manipulation is a systems problem.

Core stack:

```text
task goal
  -> robot body and sensors
  -> state estimation
  -> geometry and kinematics
  -> grasp or contact choice
  -> motion planning
  -> control execution
  -> feedback and recovery
```

Exercise: choose one everyday task and mark which stack layer is hardest.

### Lesson 1: Robot Setup

Goal: know what must exist before any algorithm can control a robot.

Teach:

- robot description files,
- arms and joints,
- hands/end-effectors,
- sensors,
- simulator command interface.

Repository link: `chapters/ch02_robot_setup/notes.md`

### Lesson 2: Coordinates, Kinematics, And IK

Goal: move from desired object motion to robot joint motion.

Teach:

- frames and transforms,
- forward kinematics,
- Jacobians,
- differential IK,
- grasp and pre-grasp poses.

Repository links:

- `casebook/001_spatial_transforms_numpy`
- `casebook/002_forward_kinematics_planar_arm`
- `casebook/003_differential_ik`

### Lesson 3: Geometric Perception

Goal: estimate object pose from depth data instead of assuming it is known.

Teach:

- depth sensors,
- point clouds,
- rigid registration,
- ICP,
- partial views and outliers.

Repository link: `casebook/004_icp_pose_estimation`

### Lesson 4: Bin Picking And Grasp Selection

Goal: choose useful grasps in clutter without complete object understanding.

Teach:

- clutter generation,
- contact simulation limits,
- model-based grasp selection,
- point-cloud grasp scoring,
- task-level retries.

Repository link: `casebook/005_point_cloud_grasp_scoring`

### Lesson 5: Motion Planning

Goal: generate feasible paths when hand-written motion scripts are not enough.

Teach:

- IK vs planning,
- trajectory optimization,
- RRT,
- time parameterization,
- graph-of-convex-sets intuition.

Repository link: `casebook/006_rrt_motion_planning`

### Lesson 6: Manipulator Control

Goal: understand how planned motion becomes dynamic execution.

Teach:

- point-mass control,
- PD and impedance intuition,
- manipulator dynamics,
- peg-in-hole as a contact-rich example.

Repository link: `casebook/007_pd_impedance_control`

### Lesson 7: Detection, Segmentation, And Deep Perception

Goal: connect learned perception to manipulation state.

Teach:

- detection,
- segmentation,
- segmented point clouds,
- learned pose and grasp prediction,
- task-level state.

Repository link: `casebook/008_segmentation_pipeline_stub`

### Lesson 8: Reinforcement Learning

Goal: understand RL as a framework for learning actions from interaction.

Teach:

- state, action, reward, transition,
- policy-gradient methods,
- value-based methods,
- model-based RL,
- manipulation-specific RL difficulties.

Repository link: `casebook/009_rl_grasping_gridworld`

## Default Teaching Style

- Prefer Chinese explanations with English technical terms retained where standard.
- Use small equations only when they clarify the mechanism.
- When a concept is abstract, tie it to a casebook script.
- End each lesson with a question for the learner to answer.

