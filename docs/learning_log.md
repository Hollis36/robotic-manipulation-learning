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

## 2026-06-13 Casebook Visualization Pass

Added generated visual assets for all nine casebook examples.

Artifacts produced:

- `tools/generate_casebook_figures.py`
- `docs/assets/casebook/*.png`
- `docs/casebook_visual_index.md`
- `tests/test_casebook_figures.py`

Quality checks:

- Figure generation works from Python API and CLI.
- CLI works without manually setting `PYTHONPATH`.
- Repository score now tracks `visual_assets`.

## 2026-06-13 Process Visualization Pass

Added process storyboards for the two examples where the intermediate states matter most.

Artifacts produced:

- `docs/process_visualizations.md`
- `docs/assets/storyboards/003_differential_ik_storyboard.png`
- `docs/assets/storyboards/006_rrt_motion_planning_storyboard.png`

Quality checks:

- Storyboards are generated from the same tool as the static casebook figures.
- The CLI supports `--storyboards` and `--all`.
- Repository score now tracks `process_visuals`.

Next quality target:

- Add optional animation or trace tables for examples where a static image hides important state transitions.

## 2026-06-13 Jupyter Book Pass

Added an interactive Jupyter Book learning path for the repository.

Artifacts produced:

- `book/_config.yml`
- `book/_toc.yml`
- `book/intro.md`
- `book/00_manipulation_stack.md`
- `book/01_robot_setup.md`
- `book/02_transforms_kinematics_ik.ipynb`
- `book/03_geometric_perception_icp.ipynb`
- `book/04_grasp_scoring.ipynb`
- `book/05_motion_planning_rrt.ipynb`
- `book/06_control_pd_impedance.ipynb`
- `book/07_segmentation_to_grasp.ipynb`
- `book/08_rl_gridworld.ipynb`
- `tools/generate_jupyter_book_notebooks.py`
- `requirements-book.txt`

Quality checks:

- Book structure is covered by `tests/test_jupyter_book.py`.
- Notebooks reuse `src/rml` instead of duplicating casebook logic.
- Repository score now tracks `jupyter_book`.

Next quality target:

- Add GitHub Pages publishing once the book build is stable in CI.

## 2026-06-13 Jupyter Book Pages Pass

Added GitHub Pages publishing for the interactive book.

Artifacts produced:

- `.github/workflows/pages.yml`

Quality checks:

- Pages workflow is covered by `tests/test_jupyter_book.py`.
- Local static HTML build uses `jupyter-book build --html --strict`.
- Repository score now includes the Pages workflow in `jupyter_book`.
- Deploy is gated to public repositories; the current private repository plan does not support Pages.

Next quality target:

- Make the repository public or upgrade the plan, then verify the public Pages URL after the first deployment.

## 2026-06-13 Book Operations Pass

Added local operation shortcuts for the Jupyter Book learning workflow.

Artifacts produced:

- `Makefile`
- `docs/book_workflow.md`
- `tests/test_book_operations.py`

Quality checks:

- `make test` runs pytest.
- `make score` runs repository scoring.
- `make casebook` runs all casebook scripts.
- `make notebooks` regenerates book notebooks.
- `make book-build` builds static HTML.
- `make verify` runs the full local verification loop.
- Repository score now tracks `book_workflow`.

Next quality target:

- Add optional learner progress checklists inside the Jupyter Book chapters.

## 2026-06-13 Book Learning Scaffold Pass

Turned the Jupyter Book from a runnable notebook collection into a guided study path.

Artifacts produced:

- Learning objectives, checkpoints, and practice tasks in all 10 book pages.
- Updated `tools/generate_jupyter_book_notebooks.py` so regenerated notebooks keep the learning scaffold.
- `tests/test_book_learning_scaffold.py`
- `book_learning_scaffold` category in `tools/score_repository.py`

Quality checks:

- Every book page now has `Learning Objectives`, `Checkpoint`, and `Practice Task`.
- Generated notebooks preserve the same scaffold.
- Repository score now tracks the guided-learning layer separately.

Next quality target:

- Add self-check answer keys or reflection templates for the practice tasks.

## 2026-06-13 Book Visual Design Pass

Added a dedicated visual system for the Jupyter Book pages.

Artifacts produced:

- `docs/book_visual_philosophy.md`
- `tools/generate_book_figures.py`
- `book/assets/figures/*.png`
- `tests/test_book_figures.py`

Quality checks:

- Every book page embeds a dedicated generated figure.
- The figure generator creates 10 high-resolution PNG files.
- `make verify` now regenerates book figures before rebuilding notebooks and HTML.
- Repository score now tracks `book_visuals`.

Next quality target:

- Add answer keys or self-check rubrics below the practice tasks.


## Reflection Template

- Chapter:
- What I understood:
- What I implemented:
- Where I got stuck:
- What I should revisit:
- Related casebook item:
