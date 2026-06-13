# Robotic Manipulation Learning

这是我的机器人操作学习仓库，围绕 *Robotic Manipulation: Perception, Planning, and Control* 建立章节笔记、数学推导、可运行小案例和后续 Drake 实验。

The repository is organized as a personal learning casebook rather than a copy of the source notes. Each chapter has a study folder, and the `casebook/` directory contains runnable examples that turn core ideas into code.

## What Makes This Repository Useful

- **Stack-first learning:** every chapter is tied back to the manipulation stack.
- **Runnable casebook:** concepts are paired with small deterministic Python examples.
- **Jupyter Book path:** the casebook is also organized as an interactive learning book under `book/`.
- **Pages publishing:** `.github/workflows/pages.yml` builds the book HTML for GitHub Pages.
- **Process visualizations:** selected algorithms include storyboards that show convergence or search over time.
- **Deep companion docs:** course map, learning tracks, Drake setup, capstone portfolio, and external resources are separated from chapter notes.
- **Quality loop:** `tools/score_repository.py` scores the repository against explicit quality standards.
- **GitHub-ready engineering:** tests and CI keep the learning code executable.

## Repository Map

```text
chapters/    Chapter-by-chapter notes, exercises, and Drake lab notes.
casebook/    Runnable learning cases with small deterministic examples.
src/rml/     Shared Python utilities used by the casebook and tests.
tests/       Pytest coverage for math, perception, planning, control, and RL utilities.
docs/        Learning log, glossary, math notes, and GitHub publishing notes.
book/        Jupyter Book source for the interactive learning textbook.
references/ How local source PDFs are used without republishing them.
```

## Best Starting Points

| If you want to... | Start here |
| --- | --- |
| understand the whole course | `docs/deep_course_companion.md` |
| learn through notebooks | `book/intro.md` |
| choose a study route | `docs/learning_tracks.md` |
| prepare for Drake | `docs/drake_setup.md` |
| build portfolio projects | `docs/capstone_portfolio.md` |
| check authoritative references | `docs/external_resources.md` |
| see the repository quality bar | `docs/repository_quality_standard.md` |
| browse casebook figures | `docs/casebook_visual_index.md` |
| inspect algorithm process storyboards | `docs/process_visualizations.md` |

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

## Current Version

- 11 chapter folders are scaffolded for reading notes, exercises, concept work, and future Drake labs.
- 9 runnable casebook examples are available.
- 7 Jupyter notebooks are available in `book/` for interactive study.
- GitHub Pages deployment is configured for the Jupyter Book; deployment runs automatically when the repository is public.
- 9 generated casebook figures are available in `docs/casebook_visual_index.md`.
- 2 generated process storyboards are available in `docs/process_visualizations.md`.
- Core utilities are covered by pytest tests.
- Drake labs are intentionally documented as future work until pydrake is configured.

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

Score repository quality:

```bash
python tools/score_repository.py
```

Generate casebook figures:

```bash
python tools/generate_casebook_figures.py docs/assets/casebook
```

Generate process storyboards:

```bash
python tools/generate_casebook_figures.py --storyboards docs/assets/storyboards
```

Build the Jupyter Book:

```bash
pip install -r requirements-book.txt
cd book
jupyter-book build --html
```

## Learning Principles

- Write notes in my own words.
- Turn each important concept into a minimal executable example.
- Keep low-dependency concept cases useful before Drake is installed.
- Add Drake labs gradually once the environment is stable.
- Track confusion explicitly instead of hiding it.

## Source Notes

The local PDFs are used as study references only. They are ignored by Git by default. See `CITATION.md` and `references/README.md` for citation and source-handling notes.
