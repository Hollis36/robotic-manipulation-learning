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


## Reflection Template

- Chapter:
- What I understood:
- What I implemented:
- Where I got stuck:
- What I should revisit:
- Related casebook item:
