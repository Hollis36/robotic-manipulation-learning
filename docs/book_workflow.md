# Jupyter Book Workflow

This page is the operational guide for learning through the interactive book.

## One-Time Setup

Install the normal package and the book tooling:

```bash
make book-install
```

This installs `requirements-book.txt` and the local `src/rml` package.

## Daily Learning Loop

Run the full repository check:

```bash
make verify
```

This runs:

- `make test`
- `make score`
- `make casebook`
- `make book-figures`
- `make notebooks`
- `make book-build`

Use this before committing or pushing learning-material changes.

## Build The Book

Generate static HTML:

```bash
make book-build
```

The output is written to:

```text
book/_build/html
```

The build directory is ignored by Git.

## Preview Locally

Start a local preview server:

```bash
make book-serve
```

Open the URL printed by Jupyter Book, usually:

```text
http://localhost:3000
```

Stop the server with `Ctrl-C`.

## Regenerate Notebooks

The notebooks are generated from `tools/generate_jupyter_book_notebooks.py` so the learning path stays reproducible:

```bash
make notebooks
```

## Regenerate Book Figures

The page figures are generated from `tools/generate_book_figures.py` and stored in `book/assets/figures/`:

```bash
make book-figures
```

Run this after changing the visual design script or before rebuilding the book.

## Rebuild Generated Learning Assets

To refresh both generated layers:

```bash
make book-figures
make notebooks
make book-build
```

After regenerating, run:

```bash
make verify
```

## GitHub Pages

The workflow `.github/workflows/pages.yml` builds the online platform on pushes to `main` and uploads `_site/` as a GitHub Pages artifact.

The published artifact contains:

- `/`: online platform launch page.
- `/book/`: rendered Jupyter Book.
- `/lite/lab/index.html`: JupyterLite browser coding environment.

The current repository is a private repository, and the current GitHub plan does not support GitHub Pages for it. Because of that, deployment is gated to public repositories:

```yaml
if: github.ref == 'refs/heads/main' && github.event.repository.private == false
```

When the repository becomes public, the same workflow can deploy automatically.
