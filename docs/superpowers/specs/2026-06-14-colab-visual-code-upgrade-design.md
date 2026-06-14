# Colab Visual And Code Upgrade Design

## Objective

Upgrade the Colab learning path from "notebooks that run" into "notebooks that teach." Each Colab notebook should combine a polished AI-generated concept image, a reproducible code-generated result figure, and a small parameter experiment that makes the chapter idea visible through execution.

The work targets the seven generated learning notebooks under `book/`:

- `02_transforms_kinematics_ik.ipynb`
- `03_geometric_perception_icp.ipynb`
- `04_grasp_scoring.ipynb`
- `05_motion_planning_rrt.ipynb`
- `06_control_pd_impedance.ipynb`
- `07_segmentation_to_grasp.ipynb`
- `08_rl_gridworld.ipynb`

## Design Choice

Use a hybrid visual strategy:

- AI-generated concept images explain the mental model of each topic.
- Code-generated figures show the actual computed result from the notebook.
- Captions and self-check prompts connect both images back to the manipulation task.

This avoids two weak extremes. Pure AI visuals can look good but drift from the computation; pure code plots are reproducible but often too dry for first-pass learning.

## Notebook Structure

Each notebook will follow the same learning rhythm:

1. **Concept Map**: one AI-generated image with a short caption and chapter-specific intuition.
2. **Colab Setup**: current bootstrap cell, kept compatible with Colab, JupyterLite, Codespaces, and local checkout.
3. **Core Computation**: existing minimal `rml` example, refactored only where clarity improves.
4. **Result Figure**: one code cell that renders an interpretable plot from the actual computation.
5. **Parameter Experiment**: one explicit parameter block with 2-3 safe values to change.
6. **Reflection Prompt**: a short Chinese self-check that asks what changed and why.

The notebooks should remain lightweight. They will use only standard library modules, NumPy, Matplotlib, and the existing `src/rml` package.

## AI Image Prompt System

Prompts will be stored in `docs/colab_visual_prompts.md`. Each entry will include:

- notebook id
- image filename
- teaching intent
- professional prompt
- negative prompt or constraints
- insertion point in the notebook

AI image assets will be stored under:

```text
book/assets/colab/
```

Suggested filenames:

- `02_transforms_kinematics_ik_concept.png`
- `03_geometric_perception_icp_concept.png`
- `04_grasp_scoring_concept.png`
- `05_motion_planning_rrt_concept.png`
- `06_control_pd_impedance_concept.png`
- `07_segmentation_to_grasp_concept.png`
- `08_rl_gridworld_concept.png`

Prompt style constraints:

- professional robotics education illustration
- clear manipulation scene or algorithm process
- no tiny unreadable text inside the image
- no logos or copyrighted character styles
- light engineering background, high contrast, readable at notebook width
- conceptually accurate enough to support the adjacent code, but not treated as numerical evidence

The image caption in the notebook will carry labels and interpretation, so the generated image does not need embedded text.

## Code Figure Design

Each notebook gets one result-plot cell that uses computed values from that notebook:

- Transforms and IK: planar arm configuration, target, final end-effector position, and residual error.
- ICP: source points, transformed target points, correspondence lines, and final alignment error.
- Grasp scoring: point cloud, gripper candidates, and ranked score bars.
- RRT planning: obstacle, sampled tree, returned path, start, and goal.
- PD control: position trace, target line, velocity or control trace, and damping comparison.
- Segmentation to grasp: original points, mask-selected target points, and selected grasp candidate.
- RL gridworld: grid, object, gripper path, reward event, and policy arrows or trajectory.

These plots should be code-first and deterministic. Random examples must use fixed seeds.

## Generator Changes

The existing `tools/generate_jupyter_book_notebooks.py` remains the source of truth for notebook cells. The implementation should add helper builders rather than hand-editing each notebook:

- `concept_image_markdown(...)`
- `result_plot_intro(...)`
- small reusable code snippets for display setup
- per-notebook parameter experiment cells

Generated notebooks should still be committed, because the repository tracks book sources directly.

## Online Platform Changes

The Colab page should link to the improved notebooks and mention the new image + experiment rhythm. If the AI concept images are useful as a gallery, the page can show small thumbnails later, but the first implementation should prioritize notebook quality over a decorative gallery.

The online platform build already copies `platform/*.html` and `platform/*.css`. If Colab images need to render in JupyterLite as notebook-relative assets, `tools/prepare_lite_workspace.py` or `tools/build_online_platform.py` must copy `book/assets/colab/` into the Lite workspace or site path.

## Testing

Add or extend tests before implementation:

- each generated notebook references its concept image
- every concept image prompt exists in `docs/colab_visual_prompts.md`
- every notebook contains a parameter experiment section
- every notebook contains a result figure code cell using Matplotlib
- every concept image asset exists and is large enough to be useful
- online build or Lite workspace includes the required Colab image assets
- `score_repository` tracks a stronger Colab visual/code category

Existing verification remains mandatory:

```bash
pytest -q
make online-build
make verify
```

After deployment, check:

```bash
curl -I -L https://hollis36.github.io/robotic-manipulation-learning/colab.html
curl -L https://colab.research.google.com/github/Hollis36/robotic-manipulation-learning/blob/main/book/02_transforms_kinematics_ik.ipynb
```

## Non-Goals

- Do not add Drake or pydrake dependencies to Colab notebooks in this pass.
- Do not make AI-generated images the source of numerical truth.
- Do not manually edit generated notebook JSON except through the generator script.
- Do not turn the project into a heavy ML training environment.
- Do not introduce large binary assets beyond the seven concept images unless there is a clear teaching need.

## Acceptance Criteria

- All seven Colab notebooks include one concept image, one code-generated result figure, and one parameter experiment.
- The prompt catalog is complete enough to regenerate the concept images.
- Colab notebooks remain one-click openable from the public repository.
- Jupyter Book and JupyterLite builds still pass.
- Repository score remains 100 with an explicit Colab visual/code check.
