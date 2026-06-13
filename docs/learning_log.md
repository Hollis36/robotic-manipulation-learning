# Learning Log

## 2026-06-13

Started a chapter-driven robotic manipulation learning repository.

Initial learning goals:

- Build intuition for manipulation as the integration of perception, planning, control, and contact.
- Convert key mathematical ideas into small Python examples.
- Keep examples executable before depending on Drake.
- Gradually add Drake labs after the basic concepts are stable.

Repository v0.1 content:

- Chapter study folders for Chapters 1-11.
- Tested Python utilities under `src/rml`.
- Nine runnable casebook examples covering transforms, kinematics, IK, ICP, grasp scoring, RRT, PD control, perception data flow, and RL environment structure.
- Local source PDFs excluded from Git by default.

## 2026-06-13 Chapter 1 First Pass

Completed a first learning pass over Chapter 1: Introduction.

Main takeaway:

- Manipulation should be studied as a system stack, not as a single grasping trick.
- Pick-and-place is a useful starting point, but the real difficulty comes from open-world variation, contact uncertainty, perception errors, and module integration.
- This repository should keep connecting each algorithmic case to a concrete manipulation task.

Artifacts produced:

- `chapters/ch01_introduction/notes.md`
- `chapters/ch01_introduction/exercises.md`
- `chapters/ch01_introduction/problem_taxonomy.md`

Next learning step:

- Move to Chapter 2 and connect robot hardware descriptions, sensors, hands, and simulation interfaces to the later casebook examples.

## 2026-06-13 Full Course DSE Loop

Completed an adapted `dse-loop` pass over all 15 local PDFs.

Artifacts produced:

- `docs/full_course_learning_map.md`
- `docs/teaching_guide.md`
- `docs/study_sessions/full_course_dse_loop.md`
- `dse_results/DSE_REPORT.md`
- `dse_results/dse_log.csv`

Teaching sequence selected:

1. Manipulation stack and system view.
2. Robot setup.
3. Coordinates, kinematics, and IK.
4. Geometric perception.
5. Bin picking and grasp selection.
6. Motion planning.
7. Manipulator control.
8. Detection, segmentation, and deep perception.
9. Reinforcement learning.
10. Drake and hardware appendices.

## 2026-06-13 Repository Quality DSE Pass

Expanded the repository from a course map into a stronger learning system.

Added:

- Deep course companion with chapter cards, assumptions, common mistakes, checkpoints, and mastery rubric.
- External resource index for official course, OCW, Drake, pydrake, and related ecosystem links.
- Learning tracks for fast concept study, coding-first practice, Drake transition, portfolio projects, and research reading.
- Drake setup guide for moving from NumPy examples to optional pydrake labs.
- Capstone portfolio ladder.
- Repository quality standard.
- Automated repository quality scorer.
- GitHub Actions test workflow.

Next quality target:

- Add small generated plots or animations to the casebook where they improve understanding.


## Reflection Template

- Chapter:
- What I understood:
- What I implemented:
- Where I got stuck:
- What I should revisit:
- Related casebook item:
