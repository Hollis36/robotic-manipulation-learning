# Capstone Portfolio

The goal of this repository is not only to learn chapters, but to produce visible projects that demonstrate manipulation reasoning.

## Capstone 1: Planar Pick-And-Place Studio

**Chapters:** 3, 7, 8

**Core idea:** build a 2D arm simulator that moves a block from start to goal.

**Milestones:**

- Forward kinematics and Jacobian visualization.
- Differential IK target tracking.
- Collision-aware RRT path.
- PD execution of a planned joint path.

**Evidence:**

- Unit tests.
- Plot or animation.
- README explaining assumptions and failure modes.

## Capstone 2: Synthetic Geometric Perception Lab

**Chapters:** 4, 5

**Core idea:** generate synthetic object point clouds, perturb them, and evaluate ICP plus grasp scoring.

**Milestones:**

- Clean registration.
- Registration with noise and outliers.
- Partial-view failure case.
- Grasp candidate ranking from segmented points.

**Evidence:**

- Error table.
- Failure examples.
- Notes on when geometric perception is enough.

## Capstone 3: Bin-Picking Task Loop

**Chapters:** 5, 7, 8

**Core idea:** simulate a simplified bin-picking loop with perception, grasp scoring, planning, execution, and retry.

**Milestones:**

- Random clutter generator.
- Grasp score with collision penalty.
- Task-level state machine.
- Recovery after failed grasps.

**Evidence:**

- Success-rate report.
- Logged failure categories.
- Short screencast or terminal transcript.

## Capstone 4: Perception-To-Grasp Pipeline

**Chapters:** 4, 9, 10

**Core idea:** show how segmentation quality affects downstream pose or grasp decisions.

**Milestones:**

- Simulated mask output.
- Segmented point cloud extraction.
- Pose or grasp pipeline.
- Noise and false-positive sensitivity study.

**Evidence:**

- Pipeline diagram.
- Sensitivity plot.
- Lessons on interface design between perception and manipulation.

## Capstone 5: RL Grasping Gridworld

**Chapters:** 11 plus earlier stack concepts.

**Core idea:** turn the current gridworld into a small learning experiment.

**Milestones:**

- Environment tests.
- Tabular Q-learning baseline.
- Reward shaping comparison.
- Policy visualization.

**Evidence:**

- Learning curve.
- Reward-design analysis.
- Failure cases where the reward induces bad behavior.

## Selection Rule

Pick the smallest project that forces integration across at least three stack layers. A narrow but complete project is better than a broad demo that hides assumptions.

