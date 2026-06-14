# Online Learning Platform

This repository can be deployed as a GitHub-hosted online learning platform.

## What Gets Published

The GitHub Pages artifact is built into `_site/` and contains three learning surfaces:

| Path | Purpose |
| --- | --- |
| `/` | Platform launch page |
| `/labs.html` | Experiment launcher for notebooks and casebook work |
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

Current constraint: this repository is private, and the current GitHub plan has not enabled private-repository Pages deployment. The workflow still validates the full build. Actual public deployment requires making the repository public or using a GitHub plan that supports Pages for private repositories.
