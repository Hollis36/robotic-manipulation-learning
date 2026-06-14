# VS Code Learning Guide

This guide is the quickest way to study this repository inside VS Code.

## One-Time Setup

1. Open this folder in VS Code.
2. Install the recommended extensions when VS Code prompts you.
3. Open the Command Palette with `Cmd-Shift-P`.
4. Run `Tasks: Run Task`.
5. Choose `RML: Install Online Platform Environment`.

This installs the Jupyter Book dependencies, JupyterLite build dependencies, and the local `src/rml` package.

## Daily Start

Run:

```text
Tasks: Run Task -> RML: Serve Online Platform
```

Open the printed local URL, usually:

```text
http://localhost:8000
```

Keep VS Code beside the browser:

- Browser: use the online platform, experiment launcher, rendered book, and JupyterLite.
- VS Code editor: inspect Markdown, notebooks, casebook scripts, and `src/rml` code.
- VS Code terminal: run tasks and casebook examples.

## First Session

Open these files in this order:

1. `book/intro.md`
2. `book/00_manipulation_stack.md`
3. `book/01_robot_setup.md`
4. `book/02_transforms_kinematics_ik.ipynb`
5. `casebook/001_spatial_transforms_numpy/run.py`
6. `src/rml/transforms.py`

Use the notebook page as the main learning surface. Use the casebook script to see the same idea as a small Python program. Use `src/rml` to inspect the reusable implementation.

## First Casebook Run

From the Command Palette:

```text
Tasks: Run Task -> RML: Run First Casebook Example
```

The first case demonstrates homogeneous transforms and frame composition. While reading it, keep one rule in mind:

```text
A_from_B @ B_from_C = A_from_C
```

To run the full casebook in Codespaces or local VS Code:

```text
Tasks: Run Task -> RML: Run All Casebook Examples
```

## Verification Loop

Before committing learning changes, run:

```text
Tasks: Run Task -> RML: Verify Repository
```

This runs tests, repository scoring, casebook scripts, book figure generation, notebook generation, and the Jupyter Book build.

## Useful Tasks

| Task | Use it when |
| --- | --- |
| `RML: Install Book Environment` | first setup or dependency refresh |
| `RML: Install Online Platform Environment` | setup for GitHub Pages, JupyterLite, and local package work |
| `RML: Serve Jupyter Book` | start reading the rendered book |
| `RML: Build Jupyter Book` | check static HTML generation |
| `RML: Build Online Platform` | build `_site/` with launch page, book, and JupyterLite |
| `RML: Serve Online Platform` | preview the full learning platform locally |
| `RML: Regenerate Book Figures` | update page visuals |
| `RML: Regenerate Notebooks` | rebuild generated notebooks |
| `RML: Run All Casebook Examples` | execute the full runnable case collection |
| `RML: Verify Repository` | check everything before saving progress |

## Reflection Template

Use this after each learning session:

```text
Date:
Page:
Casebook example:
What I understood:
What I changed:
What failed or confused me:
Next question:
```

Save reflections under `docs/study_sessions/` when they are worth keeping.
