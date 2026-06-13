# Robotic Manipulation Learning Repository Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first GitHub-ready version of a personal robotic manipulation learning repository with chapter notes, runnable concept cases, and tested Python utilities.

**Architecture:** The repository root is the GitHub project. Top-level Markdown files explain the learning purpose, roadmap, citation, and publishing workflow. Chapter folders hold study notes and exercise logs; `casebook/` holds public-facing runnable examples; `src/rml/` holds shared Python utilities used by the casebook and tests.

**Tech Stack:** Python 3.11+, NumPy, SciPy, Matplotlib, PyYAML, pytest, optional future pydrake.

---

### Task 1: Repository Metadata And Tooling

**Files:**
- Create: `.gitignore`
- Create: `README.md`
- Create: `ROADMAP.md`
- Create: `CITATION.md`
- Create: `requirements.txt`
- Create: `environment.yml`
- Create: `pyproject.toml`
- Create: `references/README.md`
- Create: `docs/learning_log.md`
- Create: `docs/glossary.md`
- Create: `docs/math_notes.md`
- Create: `docs/github_publish_notes.md`

- [ ] **Step 1: Add repository ignore rules**

Create `.gitignore` with Python cache, virtual environment, generated output, notebook checkpoint, local Drake cache, and local PDF rules:

```gitignore
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
.venv/
venv/
env/
.DS_Store
outputs/
casebook/*/outputs/*
*.pdf
!docs/**/*.pdf
```

- [ ] **Step 2: Add Python packaging and dependency files**

Create `requirements.txt`, `environment.yml`, and `pyproject.toml` so `pytest` can import `src/rml`.

- [ ] **Step 3: Add GitHub-facing Markdown**

Create the top-level README, roadmap, citation note, source reference guide, learning log, glossary, math notes, and publish notes. These documents must explain that the PDF files are local references and are not copied into the repository.

- [ ] **Step 4: Commit metadata**

Run:

```bash
git add .gitignore README.md ROADMAP.md CITATION.md requirements.txt environment.yml pyproject.toml references docs
git commit -m "chore: scaffold learning repository metadata"
```

Expected: commit succeeds, with local PDFs ignored.

### Task 2: Chapter Study Skeleton

**Files:**
- Create: `chapters/ch01_introduction/README.md`
- Create: `chapters/ch01_introduction/notes.md`
- Create: `chapters/ch01_introduction/exercises.md`
- Create: matching files for chapters `ch02_robot_setup` through `ch11_reinforcement_learning`
- Create: `chapters/*/concepts/.gitkeep`
- Create: `chapters/*/drake_labs/README.md`

- [ ] **Step 1: Create chapter directories**

Create one directory per chapter, including `concepts/` and `drake_labs/` subdirectories.

- [ ] **Step 2: Add chapter landing pages**

Each `README.md` must include chapter focus, learning outputs, linked casebook items, and study status.

- [ ] **Step 3: Add learner-owned notes**

Each `notes.md` must be a learner summary scaffold in Chinese, with sections for core question, key concepts, formulas, implementation ideas, and open questions.

- [ ] **Step 4: Add exercise logs**

Each `exercises.md` must provide a checklist and reflection template for the chapter exercises without reproducing the original textbook.

- [ ] **Step 5: Commit chapter skeleton**

Run:

```bash
git add chapters
git commit -m "docs: add chapter study skeleton"
```

Expected: commit succeeds.

### Task 3: Tested Core Math Utilities

**Files:**
- Create: `src/rml/__init__.py`
- Create: `src/rml/transforms.py`
- Create: `src/rml/kinematics.py`
- Create: `src/rml/differential_ik.py`
- Create: `tests/test_transforms.py`
- Create: `tests/test_kinematics.py`
- Create: `tests/test_differential_ik.py`

- [ ] **Step 1: Write failing tests**

Tests must cover SE(2) rotation/transform composition, planar arm forward kinematics/Jacobian, and damped least-squares differential IK.

- [ ] **Step 2: Verify red state**

Run:

```bash
pytest tests/test_transforms.py tests/test_kinematics.py tests/test_differential_ik.py -q
```

Expected: tests fail because `rml` modules do not exist yet.

- [ ] **Step 3: Implement math utilities**

Implement:

```python
rot2(theta)
make_transform(theta, translation)
compose(a, b)
apply_transform(transform, points)
planar_forward_kinematics(joint_angles, link_lengths)
planar_jacobian(joint_angles, link_lengths)
damped_least_squares_step(jacobian, error, damping=1e-3)
solve_planar_position_ik(initial_q, target_xy, link_lengths, steps=100, damping=1e-2, gain=0.5)
```

- [ ] **Step 4: Verify green state**

Run:

```bash
pytest tests/test_transforms.py tests/test_kinematics.py tests/test_differential_ik.py -q
```

Expected: all tests pass.

- [ ] **Step 5: Commit math utilities**

Run:

```bash
git add src/rml tests
git commit -m "feat: add core manipulation math utilities"
```

Expected: commit succeeds.

### Task 4: Perception, Planning, Control, And RL Utilities

**Files:**
- Create: `src/rml/icp.py`
- Create: `src/rml/grasp_scoring.py`
- Create: `src/rml/rrt.py`
- Create: `src/rml/control.py`
- Create: `src/rml/gridworld.py`
- Create: `tests/test_icp.py`
- Create: `tests/test_grasp_scoring.py`
- Create: `tests/test_rrt.py`
- Create: `tests/test_control.py`
- Create: `tests/test_gridworld.py`

- [ ] **Step 1: Write failing tests**

Tests must cover synthetic ICP recovery, point-cloud grasp scoring order, RRT path validity, PD mass convergence, and gridworld transitions/rewards.

- [ ] **Step 2: Verify red state**

Run:

```bash
pytest tests/test_icp.py tests/test_grasp_scoring.py tests/test_rrt.py tests/test_control.py tests/test_gridworld.py -q
```

Expected: tests fail because these modules do not exist yet.

- [ ] **Step 3: Implement utilities**

Implement deterministic, small examples:

```python
best_fit_transform(source, target)
icp(source, target, iterations=20, tolerance=1e-8)
score_antipodal_grasps(points, candidates)
rrt(start, goal, bounds, obstacles, step_size=0.2, max_iter=1000, seed=0)
simulate_pd_mass(x0, v0, target, kp=20.0, kd=8.0, dt=0.01, steps=300)
GridGraspWorld.reset()
GridGraspWorld.step(action)
```

- [ ] **Step 4: Verify green state**

Run:

```bash
pytest tests/test_icp.py tests/test_grasp_scoring.py tests/test_rrt.py tests/test_control.py tests/test_gridworld.py -q
```

Expected: all tests pass.

- [ ] **Step 5: Commit utilities**

Run:

```bash
git add src/rml tests
git commit -m "feat: add perception planning control and rl utilities"
```

Expected: commit succeeds.

### Task 5: Casebook Examples

**Files:**
- Create: `casebook/001_spatial_transforms_numpy/README.md`
- Create: `casebook/001_spatial_transforms_numpy/run.py`
- Create: matching README and `run.py` files for casebook items `002` through `009`

- [ ] **Step 1: Create casebook directories**

Each case directory must include a README with learning goal, related chapter, run command, and expected output.

- [ ] **Step 2: Add runnable scripts**

Each `run.py` must import `rml` utilities and print deterministic results suitable for quick terminal verification.

- [ ] **Step 3: Verify each script**

Run:

```bash
for f in casebook/*/run.py; do PYTHONPATH=src python "$f"; done
```

Expected: each script exits with status 0 and prints a short result.

- [ ] **Step 4: Commit casebook**

Run:

```bash
git add casebook
git commit -m "feat: add runnable manipulation learning casebook"
```

Expected: commit succeeds.

### Task 6: Final Verification And Repository Review

**Files:**
- Modify: `README.md`
- Modify: `ROADMAP.md`
- Modify: `docs/learning_log.md`

- [ ] **Step 1: Run all tests**

Run:

```bash
pytest -q
```

Expected: all tests pass.

- [ ] **Step 2: Run all casebook scripts**

Run:

```bash
for f in casebook/*/run.py; do PYTHONPATH=src python "$f"; done
```

Expected: all scripts pass.

- [ ] **Step 3: Review Git state**

Run:

```bash
git status --short --branch
git log --oneline --max-count=6
```

Expected: implementation files are committed; ignored PDFs do not appear in short status.

- [ ] **Step 4: Report publishing next step**

If the local repo is complete, report the branch name and give the exact GitHub publish options: create a new GitHub repository, add remote, push branch, and optionally merge to `main`.
