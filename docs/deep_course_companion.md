# Deep Course Companion

This companion is the repository's main learning scaffold. It is organized by what each chapter contributes to the manipulation stack, what assumptions it removes, what code artifact demonstrates the idea, and what a learner should be able to explain afterward.

## Stack View

```text
Task intent
  -> robot body, hand, sensors, and simulator
  -> object and scene state estimation
  -> geometry, frames, and kinematics
  -> grasp/contact choice
  -> collision-aware motion planning
  -> dynamic control and contact execution
  -> learned perception and learned policies
  -> feedback, debugging, and iteration
```

## Chapter Cards

### Preface: Why Manipulation Is A Systems Field

**Role:** motivation.

**Key idea:** dexterous behavior emerges from dynamics, perception, control, and physical interaction. The course should be read as a systems text rather than a catalog of isolated algorithms.

**Learner checkpoint:** explain why manipulating an object is harder than merely detecting it.

**Repository action:** keep every casebook item tied to a physical task.

### Chapter 1: Introduction

**Role:** establishes the manipulation problem.

**Assumption removed later:** that a single scripted pick-and-place routine captures the field.

**Key ideas:**

- Manipulation includes contact-rich tasks beyond pick-and-place.
- Open-world variation makes robustness hard to test exhaustively.
- Simulation enables iteration, but does not eliminate perception and contact difficulty.
- Model-based design helps keep complex stacks understandable.

**Casebook connection:** conceptual; see `chapters/ch01_introduction/problem_taxonomy.md`.

**Common mistake:** treating the course as only a Drake programming tutorial. Drake is the lab bench, not the subject.

**Learner checkpoint:** decompose one household task into perception, planning, control, and failure recovery.

### Chapter 2: Robot Setup

**Role:** defines what the algorithms control.

**Assumption removed later:** that a robot is just an endpoint position command.

**Key ideas:**

- Robot description files define links, joints, frames, geometry, and often inertial information.
- Arms determine reachability and motion constraints.
- Hands or grippers determine which contacts are possible.
- Sensors determine what state can be estimated.
- Simulation connects model, controller, sensors, scene, and command interface.

**Repository upgrade target:** add a small YAML robot description parser and a future pydrake model-loading lab.

**Common mistake:** ignoring frames and model names until pydrake errors become hard to diagnose.

**Learner checkpoint:** draw a block diagram with arm, gripper, camera, plant, controller, and scene.

### Chapter 3: Basic Pick And Place

**Role:** core geometry and kinematics.

**Assumption:** object pose is known.

**Key ideas:**

- Frame notation is a correctness tool.
- Spatial transforms move points and frames between coordinate systems.
- Forward kinematics maps joint angles to end-effector pose.
- Jacobians connect joint velocities to task-space velocities.
- Differential IK solves local motion updates, not global planning.
- Grasp and pre-grasp poses turn a task goal into a motion sequence.

**Casebook connections:**

- `casebook/001_spatial_transforms_numpy`
- `casebook/002_forward_kinematics_planar_arm`
- `casebook/003_differential_ik`

**Common mistake:** composing transforms in the wrong order and then trying to fix the controller.

**Learner checkpoint:** given two frames and one point, predict the result of a transform composition before running code.

### Chapter 4: Geometric Pose Estimation

**Role:** estimates state needed by manipulation.

**Assumption removed:** object pose is no longer given perfectly.

**Key ideas:**

- Depth cameras provide partial geometric observations.
- Point clouds are useful but noisy and incomplete.
- Rigid registration estimates the transform between observed and model points.
- ICP works by alternating correspondences and transform fitting.
- Partial views, outliers, and free-space constraints matter in real manipulation.
- Tracking uses temporal continuity to improve state estimates.

**Casebook connection:** `casebook/004_icp_pose_estimation`

**Common mistake:** expecting ICP to solve a global recognition problem; it is local and initialization-sensitive.

**Learner checkpoint:** describe a point-cloud scene where ICP fails and explain why.

### Chapter 5: Bin Picking

**Role:** practical cluttered grasping.

**Assumption removed:** the robot no longer gets a single isolated known object.

**Key ideas:**

- Bin picking can be useful even without full object identity.
- Cluttered scenes create occlusion, contact ambiguity, and retry logic.
- Simulation contact details affect grasp evaluation.
- Grasp scoring can use geometry and point clouds directly.
- Task-level programming handles success, failure, and repetition.

**Casebook connection:** `casebook/005_point_cloud_grasp_scoring`

**Common mistake:** optimizing a single grasp score while ignoring task-level recovery.

**Learner checkpoint:** list five corner cases that a bin-picking loop must handle.

### Chapter 6: Mobile Manipulation

**Role:** future extension.

**Local source status:** placeholder only.

**Likely connection:** moving the base changes reachability, collision checking, mapping, and task planning.

**Learner checkpoint:** explain how adding a mobile base changes the configuration space.

### Chapter 7: Motion Planning

**Role:** automated feasible motion.

**Assumption removed:** hand-written gripper trajectories are enough.

**Key ideas:**

- IK handles endpoint feasibility; planning handles path feasibility.
- Trajectory optimization searches over paths with smoothness and constraints.
- Sampling-based planning explores spaces that are difficult to optimize directly.
- Time-optimal path parameterization adds timing under velocity/acceleration limits.
- Graphs of convex sets provide a structured planning viewpoint.

**Casebook connection:** `casebook/006_rrt_motion_planning`

**Common mistake:** confusing a valid goal pose with a valid path to that pose.

**Learner checkpoint:** compare when to try IK, RRT, and trajectory optimization.

### Chapter 8: Manipulator Control

**Role:** turns plans into physical behavior.

**Assumption removed:** planned trajectory equals executed trajectory.

**Key ideas:**

- A point-mass model gives intuition for feedback control.
- PD behavior is a useful entry point to impedance-like control.
- General manipulators require dynamics-aware control.
- Contact-rich tasks need compliance and feedback, not only position tracking.
- Peg-in-hole style tasks expose the limits of pure geometric planning.

**Casebook connection:** `casebook/007_pd_impedance_control`

**Common mistake:** treating contact as a collision to avoid rather than a physical interaction to control.

**Learner checkpoint:** explain how increasing `kp` and `kd` changes response in the point-mass case.

### Chapter 9: Object Detection And Segmentation

**Role:** learned perception for clutter and object diversity.

**Assumption removed:** geometry alone can identify the relevant object or region.

**Key ideas:**

- Detection answers whether and where an object category appears.
- Segmentation identifies which pixels or points belong to an object.
- Segmented point clouds can improve pose estimation and grasp selection.
- Data quality and domain shift shape downstream manipulation reliability.

**Casebook connection:** `casebook/008_segmentation_pipeline_stub`

**Common mistake:** evaluating perception in isolation while ignoring how errors affect grasping or planning.

**Learner checkpoint:** trace how one segmentation false positive can become a grasp failure.

### Chapter 10: Deep Perception For Manipulation

**Role:** task-specific scene representations.

**Assumption removed:** generic CV outputs are always the right manipulation state.

**Key ideas:**

- Manipulation may need learned pose, grasp affordance, dense descriptors, or task-level state.
- Pretraining and fine-tuning help but do not remove the need for task-specific evaluation.
- The best representation is the one that improves action selection.

**Casebook connection:** `casebook/008_segmentation_pipeline_stub`

**Common mistake:** choosing a perception target because it is popular instead of because the downstream action needs it.

**Learner checkpoint:** define the input and output for three manipulation-specific perception tasks.

### Chapter 11: Reinforcement Learning

**Role:** learning action policies from interaction.

**Assumption removed:** all useful manipulation behavior can be scripted or optimized from a fixed model.

**Key ideas:**

- RL requires a state, action, reward, transition, and termination definition.
- Policy-gradient, value-based, and model-based methods use different information.
- Manipulation is attractive for RL because contact-rich behavior is hard to script.
- Manipulation is difficult for RL because data, safety, rewards, and generalization are hard.

**Casebook connection:** `casebook/009_rl_grasping_gridworld`

**Common mistake:** designing rewards that encourage shortcut behavior unrelated to real task success.

**Learner checkpoint:** write a reward function for one manipulation task and list how it could be exploited.

### Appendix A: Drake

**Role:** software toolchain.

**Key ideas:**

- Drake provides multibody modeling, systems composition, optimization, and Python bindings.
- pydrake examples are useful, but the generated Python API docs sometimes require cross-checking C++ documentation.
- Online tutorials are a lower-friction way to start before local installation.

**Repository action:** keep Drake labs optional and environment-checked.

### Appendix B: Manipulation Station

**Role:** simulation-to-hardware bridge.

**Key ideas:**

- A physical station includes robot arm, gripper, depth cameras, message passing, drivers, and supporting hardware.
- Simulation can mirror parts of this interface, but hardware assumptions must be explicit.

**Repository action:** future labs should document what is simulated and what would change on hardware.

### Appendix C: Miscellaneous

**Role:** citation and extension.

**Key ideas:**

- Cite the course notes properly.
- Use final projects as inspiration after the stack is understood.
- Keep notes and exercises learner-owned.

## Mastery Rubric

| Level | Evidence |
| --- | --- |
| Beginner | Can run each casebook script and explain the printed output. |
| Working learner | Can connect each casebook script to a chapter assumption it removes. |
| Strong learner | Can modify a case, predict failure modes, and write a test for the modification. |
| Project-ready | Can combine perception, planning, and control into a small end-to-end manipulation demo. |
| Research-ready | Can identify which assumption blocks real-world deployment and design an experiment around it. |

