# Colab Visual Code Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade all seven Colab notebooks with AI concept images, reproducible Matplotlib result figures, parameter experiments, and prompt-tracked visual assets.

**Architecture:** `tools/generate_jupyter_book_notebooks.py` remains the source of truth for notebook JSON. `docs/colab_visual_prompts.md` stores the professional AI image prompts, `book/assets/colab/` stores generated concept images, and tests enforce notebook structure, image assets, Lite copying, and scoring.

**Tech Stack:** Python 3, pytest, nbformat-compatible JSON, NumPy, Matplotlib, existing `src/rml`, GitHub Pages/JupyterLite, Codex image generation.

---

## File Structure

- Modify `tests/test_colab_project.py`: expand Colab tests from launch links into visual/code learning quality checks.
- Create `docs/colab_visual_prompts.md`: one prompt entry per notebook, including filename and insertion point.
- Create `book/assets/colab/*.png`: seven AI-generated concept images from the prompt catalog.
- Modify `tools/generate_jupyter_book_notebooks.py`: add reusable helpers and per-notebook concept/result/parameter cells.
- Modify generated `book/*.ipynb`: regenerate through the generator only.
- Modify `tools/prepare_lite_workspace.py`: copy `book/assets/colab` into `notebooks/assets/colab`.
- Modify `tools/build_online_platform.py`: copy Colab image assets into the served Lite lab fallback path if needed.
- Modify `tools/score_repository.py`: track stronger Colab visual/code support.
- Modify `platform/colab.html` and `docs/online_platform.md`: describe the new concept-image/result-figure/parameter-experiment loop.
- Modify `docs/repository_quality_standard.md` and `docs/learning_log.md`: record the new quality bar and pass.

---

### Task 1: Add Failing Tests For Colab Visual-Code Quality

**Files:**
- Modify: `tests/test_colab_project.py`
- Test: `tests/test_colab_project.py`

- [ ] **Step 1: Extend test constants**

Add the following constants below `NOTEBOOKS`:

```python
CONCEPT_IMAGES = {
    "02_transforms_kinematics_ik.ipynb": "02_transforms_kinematics_ik_concept.png",
    "03_geometric_perception_icp.ipynb": "03_geometric_perception_icp_concept.png",
    "04_grasp_scoring.ipynb": "04_grasp_scoring_concept.png",
    "05_motion_planning_rrt.ipynb": "05_motion_planning_rrt_concept.png",
    "06_control_pd_impedance.ipynb": "06_control_pd_impedance_concept.png",
    "07_segmentation_to_grasp.ipynb": "07_segmentation_to_grasp_concept.png",
    "08_rl_gridworld.ipynb": "08_rl_gridworld_concept.png",
}

REQUIRED_COLAB_MARKDOWN = [
    "## Concept Map",
    "## Result Figure",
    "## Parameter Experiment",
    "## Reflection Prompt",
]
```

- [ ] **Step 2: Add notebook structure test**

Append this test:

```python
def _notebook_text(path: Path) -> str:
    content = json.loads(path.read_text())
    sources = []
    for cell in content["cells"]:
        source = cell["source"]
        sources.append(source if isinstance(source, str) else "".join(source))
    return "\n\n".join(sources)


def test_colab_notebooks_include_concept_result_and_parameter_sections():
    for notebook, image_name in CONCEPT_IMAGES.items():
        text = _notebook_text(Path("book") / notebook)
        for heading in REQUIRED_COLAB_MARKDOWN:
            assert heading in text, f"{notebook} missing {heading}"
        assert f"assets/colab/{image_name}" in text
        assert "matplotlib.pyplot as plt" in text
        assert "COLAB_PARAMETER_EXPERIMENT" in text
```

- [ ] **Step 3: Add prompt catalog test**

Append this test:

```python
def test_colab_visual_prompt_catalog_covers_every_concept_image():
    prompt_file = Path("docs/colab_visual_prompts.md")

    assert prompt_file.exists()
    text = prompt_file.read_text()
    assert "professional robotics education illustration" in text
    assert "negative prompt" in text.lower()

    for notebook, image_name in CONCEPT_IMAGES.items():
        assert notebook in text
        assert image_name in text
        assert "book/assets/colab/" + image_name in text
```

- [ ] **Step 4: Add concept image asset test**

Append this test:

```python
def test_colab_concept_images_exist_and_are_large_enough():
    image_dir = Path("book/assets/colab")

    for image_name in CONCEPT_IMAGES.values():
        image_path = image_dir / image_name
        assert image_path.exists(), image_path
        assert image_path.stat().st_size > 20_000, image_path
```

- [ ] **Step 5: Add Lite copy test**

Append this test and import `subprocess` plus `sys` if they are not already imported:

```python
def test_lite_workspace_receives_colab_concept_images(tmp_path):
    result = subprocess.run(
        [sys.executable, "tools/prepare_lite_workspace.py", str(tmp_path)],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    for image_name in CONCEPT_IMAGES.values():
        assert (tmp_path / "notebooks" / "assets" / "colab" / image_name).exists()
```

- [ ] **Step 6: Strengthen score test**

Update `test_score_repository_tracks_colab_project_support`:

```python
def test_score_repository_tracks_colab_project_support():
    report = score_repository(Path("."))

    assert "colab_project" in report["categories"]
    assert report["categories"]["colab_project"]["total"] == 8
    assert report["categories"]["colab_project"]["score"] == 100
```

- [ ] **Step 7: Run test to verify it fails**

Run:

```bash
pytest tests/test_colab_project.py -q
```

Expected: FAIL because `docs/colab_visual_prompts.md`, `book/assets/colab/*.png`, notebook sections, and Lite copy support do not exist yet.

- [ ] **Step 8: Commit failing tests**

```bash
git add tests/test_colab_project.py
git commit -m "test: define Colab visual code requirements"
```

---

### Task 2: Create Prompt Catalog And Generate Concept Images

**Files:**
- Create: `docs/colab_visual_prompts.md`
- Create: `book/assets/colab/*.png`
- Test: `tests/test_colab_project.py`

- [ ] **Step 1: Create prompt catalog**

Create `docs/colab_visual_prompts.md` with these seven sections:

```markdown
# Colab Visual Prompts

These prompts generate concept images for the Colab learning notebooks. The images explain concepts; numerical evidence comes from the code-generated result figures.

## 02 Transforms, Kinematics, IK

- notebook: `02_transforms_kinematics_ik.ipynb`
- image: `book/assets/colab/02_transforms_kinematics_ik_concept.png`
- insertion point: `## Concept Map`
- teaching intent: show frame composition, a planar robot arm, a target point, and differential IK as an iterative error reduction process.
- prompt: professional robotics education illustration, clean light engineering background, planar robotic arm with three joints, coordinate frames shown as colored axes near world, gripper, and object, target point and final end-effector point connected by an error vector, subtle ghosted intermediate arm positions, high contrast, notebook-width composition, no embedded text, no logos
- negative prompt: photorealistic clutter, unreadable tiny labels, brand logos, cartoon characters, dark background, misleading 3D humanoid robot, excessive decorative gradients

## 03 Geometric Perception And ICP

- notebook: `03_geometric_perception_icp.ipynb`
- image: `book/assets/colab/03_geometric_perception_icp_concept.png`
- insertion point: `## Concept Map`
- teaching intent: show two point clouds being aligned by rigid transform estimation.
- prompt: professional robotics education illustration, clean point cloud registration scene, blue source points and orange target points, translucent arrows showing correspondences, rigid transform arc between clouds, small robot camera observing an object on a table, light engineering grid background, no embedded text, high contrast, precise technical style
- negative prompt: noisy unreadable point cloud, random abstract dots, heavy text, logos, dark cyberpunk style, photorealistic human hands

## 04 Grasp Scoring

- notebook: `04_grasp_scoring.ipynb`
- image: `book/assets/colab/04_grasp_scoring_concept.png`
- insertion point: `## Concept Map`
- teaching intent: show point-cloud grasp candidates and why balanced antipodal contacts score higher.
- prompt: professional robotics education illustration, bin-picking tabletop scene, simplified object point cloud, three parallel jaw gripper candidates with one highlighted best candidate, contact points indicated with clean markers, balanced left-right contact intuition, light background, no embedded text, technical diagram aesthetic
- negative prompt: cluttered warehouse, human hands, unreadable annotations, aggressive shadows, logos, overly realistic metal textures

## 05 Motion Planning With RRT

- notebook: `05_motion_planning_rrt.ipynb`
- image: `book/assets/colab/05_motion_planning_rrt_concept.png`
- insertion point: `## Concept Map`
- teaching intent: show a sampling tree growing around an obstacle from start to goal.
- prompt: professional robotics education illustration, 2D motion planning workspace, circular obstacle, green start, gold goal, blue RRT tree branches expanding through free space, final path highlighted with thick line, faint samples in background, clean grid, no embedded text, high readability
- negative prompt: maze game style, dark neon background, unreadable labels, photorealistic robot scene, chaotic random lines

## 06 Control: PD And Impedance Intuition

- notebook: `06_control_pd_impedance.ipynb`
- image: `book/assets/colab/06_control_pd_impedance_concept.png`
- insertion point: `## Concept Map`
- teaching intent: show a mass-spring-damper intuition connecting position target, damping, and control response.
- prompt: professional robotics education illustration, simplified end-effector mass connected to virtual spring and damper, target position marker, smooth response curve in the background, control arrow pushing toward target, light engineering diagram style, no embedded text, colorblind-safe palette
- negative prompt: complex humanoid robot, unreadable equation text, dark background, decorative bokeh, logos

## 07 Segmentation To Grasp

- notebook: `07_segmentation_to_grasp.ipynb`
- image: `book/assets/colab/07_segmentation_to_grasp_concept.png`
- insertion point: `## Concept Map`
- teaching intent: show how a segmentation mask selects target points before grasp scoring.
- prompt: professional robotics education illustration, RGB-D camera view of tabletop objects, semi-transparent segmentation mask selecting one object, selected target point cloud flowing into a gripper candidate, false positive point subtly shown near background, clean pipeline composition, no embedded text, light background
- negative prompt: dense text labels, photo collage, logos, dramatic lighting, unrealistic humanoid robot

## 08 RL Grasping Gridworld

- notebook: `08_rl_gridworld.ipynb`
- image: `book/assets/colab/08_rl_gridworld_concept.png`
- insertion point: `## Concept Map`
- teaching intent: show state, action, reward, and policy intuition in a small grasping gridworld.
- prompt: professional robotics education illustration, small 4x4 gridworld, robot gripper icon moving across cells toward an object, arrows showing actions, highlighted reward event at grasp cell, simple policy arrows, clean light background, no embedded text, readable notebook illustration
- negative prompt: video game UI, pixel art, unreadable small text, dark fantasy style, logos
```

- [ ] **Step 2: Generate seven AI images**

Use the Codex image generation tool with each `prompt` and save the returned image to the matching `book/assets/colab/*.png` path. Keep the image content free of embedded text; captions will be in notebook Markdown.

- [ ] **Step 3: Validate image assets**

Run:

```bash
python - <<'PY'
from pathlib import Path
for path in sorted(Path("book/assets/colab").glob("*.png")):
    print(path, path.stat().st_size)
PY
```

Expected: seven PNG files, each larger than 20,000 bytes.

- [ ] **Step 4: Run tests to confirm remaining failures are notebook/Lite related**

Run:

```bash
pytest tests/test_colab_project.py -q
```

Expected: prompt and image existence checks pass; notebook structure and Lite copy checks still fail.

- [ ] **Step 5: Commit prompts and image assets**

```bash
git add docs/colab_visual_prompts.md book/assets/colab
git commit -m "feat: add Colab concept image prompts and assets"
```

---

### Task 3: Add Notebook Concept, Result Figure, Parameter, And Reflection Cells

**Files:**
- Modify: `tools/generate_jupyter_book_notebooks.py`
- Modify: `book/*.ipynb` by running the generator
- Test: `tests/test_colab_project.py`

- [ ] **Step 1: Add helper functions**

In `tools/generate_jupyter_book_notebooks.py`, add these helpers after `code(...)`:

```python
def concept_image_markdown(filename: str, caption: str) -> dict:
    return markdown(
        "## Concept Map\n\n"
        f"![Colab concept image](assets/colab/{filename})\n\n"
        f"**Concept image.** {caption}"
    )


def result_figure_intro(description: str) -> dict:
    return markdown(
        "## Result Figure\n\n"
        f"{description}\n\n"
        "The figure below is generated from the values computed in this notebook. Treat it as evidence from the code, not as a decorative illustration."
    )


def parameter_experiment(text: str) -> dict:
    return markdown(
        "## Parameter Experiment\n\n"
        "The next cell is marked with `COLAB_PARAMETER_EXPERIMENT` so it is easy to find in Colab. "
        + text
    )


def reflection_prompt(text: str) -> dict:
    return markdown("## Reflection Prompt\n\n" + text)
```

- [ ] **Step 2: Add common plotting setup snippet**

Add this constant below `COMMON_SETUP`:

```python
PLOT_SETUP = """import matplotlib.pyplot as plt
plt.rcParams.update({
    "figure.figsize": (7, 4.2),
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
})
"""
```

- [ ] **Step 3: Insert concept/result/parameter/reflection cells for transforms notebook**

In `02_transforms_kinematics_ik.ipynb` cell list, insert after the title markdown:

```python
concept_image_markdown(
    "02_transforms_kinematics_ik_concept.png",
    "Frames define where objects are; kinematics and the Jacobian turn frame error into joint updates.",
),
```

Insert after the differential IK computation cell:

```python
result_figure_intro("Plot the final planar arm, the desired target, and the remaining end-effector error."),
code(
    PLOT_SETUP
    + "import numpy as np\n"
    "from rml.kinematics import planar_joint_positions\n\n"
    "links = np.array([1.0, 0.8, 0.4])\n"
    "points = planar_joint_positions(result.joint_angles, links)\n"
    "fig, ax = plt.subplots()\n"
    "ax.plot(points[:, 0], points[:, 1], '-o', lw=4, label='final arm')\n"
    "ax.scatter([target[0]], [target[1]], marker='*', s=180, label='target')\n"
    "ax.scatter([final_position[0]], [final_position[1]], s=90, label='end effector')\n"
    "ax.plot([final_position[0], target[0]], [final_position[1], target[1]], '--', label=f'error={result.error_norm:.3f}')\n"
    "ax.set_aspect('equal', adjustable='box')\n"
    "ax.set_xlabel('x position')\n"
    "ax.set_ylabel('y position')\n"
    "ax.legend(frameon=False)\n"
    "plt.show()"
),
parameter_experiment("Change `target_options` and compare how final error changes for reachable and unreachable targets."),
code(
    "# COLAB_PARAMETER_EXPERIMENT\n"
    "target_options = [np.array([1.3, 0.7]), np.array([2.0, 0.1]), np.array([3.0, 0.0])]\n"
    "for candidate in target_options:\n"
    "    trial = solve_planar_position_ik(initial_q, candidate, np.array([1.0, 0.8, 0.4]), steps=200, damping=0.05, gain=0.6)\n"
    "    print(candidate.tolist(), round(trial.error_norm, 4))"
),
reflection_prompt("为什么不可达目标的误差不会归零？用 link length 总和和 task-space error 解释。"),
```

- [ ] **Step 4: Insert cells for the remaining six notebooks**

Use the same pattern with these result figures and parameter experiments:

```python
# 03 ICP result: scatter source, target, transformed source, and correspondence lines.
# Parameter experiment: change noise_scale = [0.0, 0.02, 0.08] and print mean_error.

# 04 Grasp result: scatter points and plot score bar chart for candidates.
# Parameter experiment: change candidate widths [0.4, 0.8, 1.0, 1.4] and print ranking.

# 05 RRT result: draw obstacle, path, start, goal, and path waypoints.
# Parameter experiment: change obstacle_radius [0.12, 0.2, 0.28] and print path length or failure.

# 06 PD result: plot position over time and target line.
# Parameter experiment: change kd_values [2.0, 6.0, 10.0, 18.0] and plot/print max overshoot.

# 07 Segmentation result: scatter all points, selected mask points, and best grasp center.
# Parameter experiment: flip one mask value at a time and print selected best grasp and score.

# 08 RL result: draw 4x4 grid, trajectory arrows, object position, and final reward event.
# Parameter experiment: change object positions [(1, 0), (2, 1), (3, 3)] and print shortest hand-written action sequence outcome.
```

The implementation must use actual notebook variables already computed where possible. If a helper from `src/rml` does not expose an intermediate, recompute the small deterministic example inside the result cell instead of adding new package API.

- [ ] **Step 5: Regenerate notebooks**

Run:

```bash
python tools/generate_jupyter_book_notebooks.py
```

Expected: seven `book/*.ipynb` paths printed.

- [ ] **Step 6: Run notebook structure tests**

Run:

```bash
pytest tests/test_colab_project.py::test_colab_notebooks_include_concept_result_and_parameter_sections -q
```

Expected: PASS.

- [ ] **Step 7: Commit notebook generator and generated notebooks**

```bash
git add tools/generate_jupyter_book_notebooks.py book/*.ipynb
git commit -m "feat: enrich Colab notebooks with visual experiments"
```

---

### Task 4: Copy Colab Assets Into JupyterLite And Online Platform

**Files:**
- Modify: `tools/prepare_lite_workspace.py`
- Modify: `tools/build_online_platform.py`
- Test: `tests/test_colab_project.py`

- [ ] **Step 1: Copy Colab concept assets into Lite workspace**

In `prepare_lite_workspace`, after copying `figures_source`, add:

```python
    colab_source = PROJECT_ROOT / "book" / "assets" / "colab"
    colab_target = notebooks_dir / "assets" / "colab"
    shutil.copytree(colab_source, colab_target, dirs_exist_ok=True)
    copied.extend(sorted(colab_target.glob("*.png")))
```

- [ ] **Step 2: Copy Colab concept assets into served Lite lab fallback**

In `tools/build_online_platform.py`, update `copy_lite_lab_assets`:

```python
def copy_lite_lab_assets(site_root: Path) -> None:
    asset_pairs = [
        (PROJECT_ROOT / "book" / "assets" / "figures", site_root / "lite" / "lab" / "assets" / "figures"),
        (PROJECT_ROOT / "book" / "assets" / "colab", site_root / "lite" / "lab" / "assets" / "colab"),
    ]
    for source, target in asset_pairs:
        target.mkdir(parents=True, exist_ok=True)
        for figure in source.glob("*.png"):
            shutil.copy2(figure, target / figure.name)
```

- [ ] **Step 3: Run Lite copy test**

Run:

```bash
pytest tests/test_colab_project.py::test_lite_workspace_receives_colab_concept_images -q
```

Expected: PASS.

- [ ] **Step 4: Run online build**

Run:

```bash
make online-build
```

Expected: `_site/lite/lab/assets/colab/02_transforms_kinematics_ik_concept.png` exists.

- [ ] **Step 5: Commit asset copy support**

```bash
git add tools/prepare_lite_workspace.py tools/build_online_platform.py
git commit -m "feat: publish Colab concept assets in Lite workspace"
```

---

### Task 5: Strengthen Repository Scoring And Documentation

**Files:**
- Modify: `tools/score_repository.py`
- Modify: `platform/colab.html`
- Modify: `docs/online_platform.md`
- Modify: `docs/repository_quality_standard.md`
- Modify: `docs/learning_log.md`
- Test: `tests/test_colab_project.py`

- [ ] **Step 1: Expand score repository Colab requirements**

Replace `colab_required` in `tools/score_repository.py` with:

```python
    colab_required = [
        root / "docs" / "colab.md",
        root / "docs" / "colab_visual_prompts.md",
        root / "platform" / "colab.html",
        root / "tools" / "generate_jupyter_book_notebooks.py",
        root / "tools" / "prepare_lite_workspace.py",
        root / "book" / "assets" / "colab" / "02_transforms_kinematics_ik_concept.png",
        root / "book" / "assets" / "colab" / "05_motion_planning_rrt_concept.png",
        root / "book" / "02_transforms_kinematics_ik.ipynb",
    ]
```

- [ ] **Step 2: Update Colab page copy**

In `platform/colab.html`, update the hero summary to mention:

```html
每个 notebook 现在包含 AI 概念图、代码生成结果图和参数实验区，适合先理解概念，再通过运行结果验证。
```

- [ ] **Step 3: Update docs**

Add a "Visual And Code Learning Rhythm" section to `docs/online_platform.md`:

```markdown
## Visual And Code Learning Rhythm

The Colab notebooks use a fixed rhythm:

1. AI concept image for the mental model.
2. Code-generated result figure for computed evidence.
3. Parameter experiment for active learning.
4. Reflection prompt for short written explanation.
```

Add matching bullets to `docs/repository_quality_standard.md` and append a 2026-06-14 learning log entry titled `Colab Visual Code Upgrade Pass`.

- [ ] **Step 4: Run scoring test**

Run:

```bash
pytest tests/test_colab_project.py::test_score_repository_tracks_colab_project_support -q
```

Expected: PASS with `total == 8`.

- [ ] **Step 5: Commit scoring and docs**

```bash
git add tools/score_repository.py platform/colab.html docs/online_platform.md docs/repository_quality_standard.md docs/learning_log.md
git commit -m "docs: document Colab visual learning rhythm"
```

---

### Task 6: Full Verification, Browser Smoke Test, Push, And Deploy Check

**Files:**
- No planned edits unless verification reveals a bug.

- [ ] **Step 1: Run all Python tests**

Run:

```bash
pytest -q
```

Expected: `60 passed` or higher, depending on added tests.

- [ ] **Step 2: Run full repository verification**

Run:

```bash
make verify
```

Expected: tests pass, score remains 100, casebook scripts pass, figures/notebooks regenerate, Jupyter Book strict build passes.

- [ ] **Step 3: Build online platform**

Run:

```bash
make online-build
```

Expected: `_site/colab.html`, `_site/lite/lab/assets/colab/*.png`, and `_site/lite/files/notebooks/assets/colab/*.png` are available through the static server.

- [ ] **Step 4: Run browser smoke test**

Start:

```bash
python -m http.server 8765 --bind 127.0.0.1 --directory _site
```

Then verify with Playwright or curl:

```bash
curl -I -L http://127.0.0.1:8765/colab.html
curl -I -L http://127.0.0.1:8765/lite/lab/assets/colab/02_transforms_kinematics_ik_concept.png
```

Expected: both return 200. Stop the server before continuing.

- [ ] **Step 5: Push implementation commits**

Run:

```bash
git status --short --branch
git push origin main
```

Expected: push succeeds and local branch tracks `origin/main`.

- [ ] **Step 6: Watch GitHub Actions**

Run:

```bash
gh run list --branch main --limit 6 --json databaseId,workflowName,status,conclusion,headSha,url
gh run watch <tests-run-id> --exit-status
gh run watch <pages-run-id> --exit-status
```

Expected: `tests` passes and `pages` build/deploy passes.

- [ ] **Step 7: Verify public site**

Run:

```bash
curl -I -L https://hollis36.github.io/robotic-manipulation-learning/colab.html
curl -I -L https://hollis36.github.io/robotic-manipulation-learning/lite/lab/assets/colab/02_transforms_kinematics_ik_concept.png
curl -L --max-time 30 -o /tmp/colab-first.html -w '%{http_code} %{content_type} %{url_effective}\n' 'https://colab.research.google.com/github/Hollis36/robotic-manipulation-learning/blob/main/book/02_transforms_kinematics_ik.ipynb'
```

Expected: site and image return 200; Colab URL returns 200 HTML.

---

## Self-Review Notes

- Spec coverage: concept images, prompt catalog, code result figures, parameter experiments, Lite/site asset copying, scoring, docs, and deployment verification are all covered.
- No filler markers remain; all generated filenames and commands are explicit.
- The plan keeps generated notebooks source-controlled and edits them through `tools/generate_jupyter_book_notebooks.py`.
