# Adapted DSE Learning Loop Report

**Task:** Learn the full local *Robotic Manipulation* chapter set and prepare to teach it.

**Total iterations:** 15 source PDFs

## Objective

- **Metric:** teaching readiness
- **Direction:** maximize
- **Baseline:** Chapter 1 first pass only
- **Best found:** full-course map plus teaching guide

## Search Trajectory

The loop processed the Preface, Chapters 1-11, and Appendices A-C. Each iteration extracted chapter structure, mapped it into the repository's learning model, and connected the content to casebook examples where possible.

## High-Level Result

The course has a clean learning arc:

1. Establish why manipulation is a systems problem.
2. Define the robot, gripper, sensors, and simulator interface.
3. Learn geometry and kinematics for scripted pick-and-place.
4. Add geometric perception so object pose is estimated instead of assumed.
5. Study bin picking as a bridge between geometric methods, contact, data, and task-level logic.
6. Add motion planning when hand-written trajectories are insufficient.
7. Add control when planned motion must be executed near dynamic and contact limits.
8. Add detection, segmentation, and learned perception for clutter and object diversity.
9. Add RL as a framework for learning policies in manipulation settings.
10. Use Drake and the Manipulation Station appendices as the software/hardware path.

## Stopping Reason

Success criteria met: every local PDF is represented in a learner-owned map, and the teaching sequence is ready.

## Recommendations

- Teach from the stack view first, then go chapter by chapter.
- Use the existing `casebook/` examples as live demonstrations.
- Do not start Drake labs until Chapter 2 and Appendix A environment assumptions are clear.
- Keep Chapter 6 as future content because the local PDF is only a placeholder.

## Repository Upgrade Pass

After the first full-course map, the DSE loop was extended from "coverage" to "repository quality". The optimization target became a public-quality learning repository, measured across:

- chapter coverage,
- runnable casebook coverage,
- testing,
- deep course companion material,
- external authoritative resources,
- Drake transition readiness,
- capstone project readiness,
- CI and repository scoring.

New artifacts:

- `docs/deep_course_companion.md`
- `docs/external_resources.md`
- `docs/learning_tracks.md`
- `docs/drake_setup.md`
- `docs/capstone_portfolio.md`
- `docs/repository_quality_standard.md`
- `tools/score_repository.py`
- `.github/workflows/tests.yml`

## Visualization Pass

The next DSE target was casebook presentation quality. The repository now includes generated PNG figures for all nine casebook examples, plus a visual index page. The figures are generated from code using a tested CLI:

```bash
python tools/generate_casebook_figures.py docs/assets/casebook
```

This improves the repository's usefulness as a GitHub learning artifact: readers can inspect the main idea of each case before running it.

## Process Storyboard Pass

The next DSE target was algorithm process clarity. Static figures show final outputs, but iterative methods are easier to learn when their intermediate states are visible. The repository now includes generated storyboards for:

- differential IK convergence,
- RRT tree growth and final path connection.

The storyboards are generated from code using:

```bash
python tools/generate_casebook_figures.py --storyboards docs/assets/storyboards
```

The repository scorer now tracks `process_visuals` as a separate category, so future quality passes can distinguish static visual coverage from process-level teaching assets.

## Jupyter Book Pass

The next DSE target was interactive teaching. The repository now includes a Jupyter Book source tree under `book/` with:

- a manipulation-stack introduction,
- robot setup notes,
- seven runnable notebooks covering transforms, kinematics, IK, ICP, grasp scoring, RRT, PD control, segmentation-to-grasp, and RL gridworlds.

The notebooks reuse `src/rml` package code rather than duplicating casebook logic. The repository scorer now tracks `jupyter_book`, and the book can be built with the current MyST-backed Jupyter Book CLI:

```bash
cd book
jupyter-book build --html
```

## Jupyter Book Pages Pass

The next DSE target was publication. The repository now includes a GitHub Pages workflow that:

- installs `requirements-book.txt`,
- builds static HTML with `jupyter-book build --html --strict`,
- uploads `book/_build/html` as a Pages artifact,
- deploys the artifact to the `github-pages` environment from `main` when the repository is public.

This turns the learning repository into a publishable online course rather than only a local casebook.

Current constraint: GitHub returned `Your current plan does not support GitHub Pages for this repository` while the repository is private. The workflow still validates the HTML build on `main`, and deployment will run after the repository becomes public.

## Book Operations Pass

The next DSE target was day-to-day usability. The repository now includes a `Makefile` and a Book workflow guide so the learning loop has short, memorable commands:

- `make test`
- `make score`
- `make casebook`
- `make notebooks`
- `make book-build`
- `make book-serve`
- `make verify`

The repository scorer now tracks `book_workflow`, and `docs/book_workflow.md` explains the local build, preview, verification, and private-repository Pages constraint.

## Book Learning Scaffold Pass

The next DSE target was guided learning quality. A runnable book is useful, but a learner still needs to know what each page is asking them to master. Every Jupyter Book page now includes:

- `Learning Objectives`
- `Checkpoint`
- `Practice Task`

The generated notebooks preserve these sections through `tools/generate_jupyter_book_notebooks.py`, so future notebook regeneration will not remove the teaching layer. The repository scorer now tracks `book_learning_scaffold` as a separate category.
