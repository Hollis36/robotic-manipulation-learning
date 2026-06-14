# Google Colab Learning

This page is the quick-start path for studying the repository in Google Colab.

Use Colab when you want a cloud notebook with a Python runtime and do not need the full VS Code environment. Use Codespaces when you want to run the whole casebook, tests, site build, and Git workflow.

## How It Works

Each notebook includes a setup cell that works in three places:

- Local checkout or Codespaces: it adds the local `src/` package to `sys.path`.
- JupyterLite: it uses the copied Lite workspace package.
- Google Colab: it detects `google.colab`, runs `git clone --depth 1 https://github.com/Hollis36/robotic-manipulation-learning.git`, and adds the cloned `src/` package to `sys.path`.

After opening a notebook in Colab, run the first setup cell before running the learning cells.

## Colab Notebook Index

| Notebook | Open |
| --- | --- |
| 02 Transforms, Kinematics, IK | [Open in Colab](https://colab.research.google.com/github/Hollis36/robotic-manipulation-learning/blob/main/book/02_transforms_kinematics_ik.ipynb) |
| 03 Geometric Perception And ICP | [Open in Colab](https://colab.research.google.com/github/Hollis36/robotic-manipulation-learning/blob/main/book/03_geometric_perception_icp.ipynb) |
| 04 Grasp Scoring | [Open in Colab](https://colab.research.google.com/github/Hollis36/robotic-manipulation-learning/blob/main/book/04_grasp_scoring.ipynb) |
| 05 Motion Planning With RRT | [Open in Colab](https://colab.research.google.com/github/Hollis36/robotic-manipulation-learning/blob/main/book/05_motion_planning_rrt.ipynb) |
| 06 Control: PD And Impedance Intuition | [Open in Colab](https://colab.research.google.com/github/Hollis36/robotic-manipulation-learning/blob/main/book/06_control_pd_impedance.ipynb) |
| 07 Segmentation To Grasp | [Open in Colab](https://colab.research.google.com/github/Hollis36/robotic-manipulation-learning/blob/main/book/07_segmentation_to_grasp.ipynb) |
| 08 RL Grasping Gridworld | [Open in Colab](https://colab.research.google.com/github/Hollis36/robotic-manipulation-learning/blob/main/book/08_rl_gridworld.ipynb) |

## Recommended Study Loop

1. Read the matching Jupyter Book chapter.
2. Open the notebook in Colab.
3. Run the setup cell.
4. Run the example once without changes.
5. Modify the practice variable requested by the notebook.
6. Write the result in your learning log or chapter notes.

## Runtime Notes

- These notebooks are intentionally lightweight and use NumPy plus the repository's small `rml` package.
- They do not require Drake or pydrake.
- Colab sessions are temporary, so changes should be saved back to your own copy or recorded in the repository notes.
- For full engineering work, open the repository in Codespaces and run `make verify`.
