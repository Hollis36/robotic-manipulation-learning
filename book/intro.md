# Robotic Manipulation Learning Book

这本 Jupyter Book 是本仓库的交互式学习入口。它把课程主线、章节笔记、可运行案例和生成图统一成一本可执行教材。

## Learning Objectives

- Build a system-level view of robotic manipulation before diving into algorithms.
- Use the book, casebook, and source package as one learning loop.
- Turn every chapter into a small piece of your own GitHub learning portfolio.

## Checkpoint

- You can explain why manipulation requires perception, geometry, planning, control, and feedback together.
- You can run a book notebook and identify which `src/rml` module it uses.
- You can point to one casebook example that demonstrates each major topic.

## Practice Task

Create a short learning note for the first topic you want to master. Include the chapter name, the runnable case, what you changed in the code, and one question you still have.

学习顺序：

1. 先建立 manipulation stack 的总图。
2. 再理解机器人本体、夹爪、传感器和仿真接口。
3. 用 NumPy 案例掌握 transforms、forward kinematics、Jacobian 和 differential IK。
4. 继续学习 point cloud perception、grasp scoring、motion planning、control、segmentation 和 RL。

本书不复制原始课程讲义，而是把它们转化为 learner-owned notes 和 runnable examples。

## How To Use

在仓库根目录安装依赖：

```bash
pip install -r requirements-book.txt
pip install -e .
```

构建本书：

```bash
make book-build
```

也可以直接在 JupyterLab 或 VS Code 中打开 `book/*.ipynb`，逐个运行代码单元。

## Repository Links

- `casebook/`: 最小可运行学习案例。
- `src/rml/`: 案例复用的 Python 工具包。
- `docs/casebook_visual_index.md`: 静态案例图。
- `docs/process_visualizations.md`: IK 和 RRT 的过程图。
