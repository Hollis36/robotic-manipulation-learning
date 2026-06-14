# Online Learning Platform

This repository can be deployed as a GitHub-hosted online learning platform.

## What Gets Published

The GitHub Pages artifact is built into `_site/` and publishes these learning routes:

| Path | Purpose |
| --- | --- |
| `/` | Platform launch page |
| `/labs.html` | Experiment launcher for notebooks and casebook work |
| `/colab.html` | Google Colab notebook index |
| `/book/` | Rendered Jupyter Book |
| `/lite/lab/index.html` | JupyterLite browser coding environment |

## Browser Coding With JupyterLite

JupyterLite runs JupyterLab in the browser. It is static, so it can be hosted by GitHub Pages without a Python server. The repository copies the generated notebooks, book figures, and pure-Python `src/rml` package into the Lite workspace.

Build it locally:

```bash
make online-install
make online-build
make online-serve
```

Then open:

```text
http://localhost:8000
```

The first online notebook is:

```text
lite/lab/index.html?path=notebooks/02_transforms_kinematics_ik.ipynb
```

The experiment launcher at `/labs.html` lists all browser notebooks and the
casebook route for Codespaces. Use it as the main practice dashboard after
reading each book chapter.

## Cloud Notebooks With Google Colab

The Colab route is:

```text
colab.html
```

It links every generated learning notebook through:

```text
https://colab.research.google.com/github/Hollis36/robotic-manipulation-learning/blob/main/book/<notebook>.ipynb
```

Each notebook includes a setup cell that detects `google.colab`, clones the
public repository with `git clone --depth 1`, and adds `src/` to `sys.path`.
This keeps the same notebook usable in Colab, JupyterLite, Codespaces, and a
local checkout.

The Colab page also publishes a concept gallery from `book/assets/colab/*.png`.
Those PNG files are exported from tracked SVG sources by
`tools/generate_colab_svg_illustrations.py`, so the visual style is reproducible
instead of depending on one-off image replacements.

## Visual And Code Learning Rhythm

The Colab notebooks use a fixed rhythm:

1. SVG-sourced concept image for the mental model.
2. Code-generated result figure for computed evidence.
3. Parameter experiment for active learning.
4. Reflection prompt for short written explanation.

## Full Online Programming With Codespaces

JupyterLite is ideal for lightweight Python notebooks. For full online programming, compiling, testing, and Git operations, use GitHub Codespaces. The `.devcontainer/devcontainer.json` file installs the book, online platform, and local package dependencies automatically.

After a Codespace opens, run:

```bash
make verify
make online-build
make online-serve
```

The same flow is available from the VS Code task picker:

```text
RML: Install Online Platform Environment
RML: Build Online Platform
RML: Serve Online Platform
RML: Run All Casebook Examples
RML: Verify Repository
```

## GitHub Pages Deployment

The Pages workflow builds `_site/` from:

- `platform/`
- `book/_build/html`
- JupyterLite output

Because the book is mounted under `/book/`, the workflow sets `BOOK_BASE_URL` to
`/${repository_name}/book` before building the Jupyter Book. Local builds default
to `/book`, which keeps Book CSS, JavaScript, images, and internal navigation
aligned with the platform route.

Current deployment:

- Repository: `Hollis36/robotic-manipulation-learning`
- Public URL: <https://hollis36.github.io/robotic-manipulation-learning/>
- Pages source: GitHub Actions workflow
- Published routes: `/`, `/labs.html`, `/colab.html`, `/book/`, and `/lite/lab/index.html`

The deploy job is still gated to public repositories:

```yaml
if: github.ref == 'refs/heads/main' && github.event.repository.private == false
```

If the repository is made private again, the workflow can still validate the full build artifact, but Pages deployment will be skipped unless the GitHub account plan and repository settings support private Pages.
