# Repository Quality Standard

This is the quality bar for making the repository useful to future readers, including my future self.

## Learning Quality

- Every chapter has learner-owned notes.
- Every major concept connects to a runnable case or planned lab.
- Every case has a README, run command, expected output, and chapter link.
- Every case has a generated visual asset when a picture clarifies the idea.
- Core iterative algorithms have process visualizations when the intermediate states teach more than the final answer.
- The main learning path is available as a Jupyter Book with runnable notebooks.
- Every Jupyter Book page has learning objectives, a checkpoint, and a practice task.
- Every Jupyter Book page has a dedicated generated visual asset.
- VS Code users have tracked tasks, recommended extensions, and a documented learning loop.
- GitHub Pages builds a full online platform with launch page, book, and browser coding environment.
- Codespaces configuration supports full online programming, testing, and site builds.
- Every advanced topic has a clear prerequisite.
- Failure modes are documented, not hidden.

## Engineering Quality

- Tests run with `pytest -q`.
- Concept cases avoid heavyweight dependencies.
- Drake labs are optional and skip cleanly if pydrake is unavailable.
- Generated outputs are either ignored or intentionally small.
- Code is deterministic by default.
- Repeated learning operations are available through `Makefile` targets.
- Editor task shortcuts call the same `Makefile` targets instead of duplicating workflow logic.

## GitHub Quality

- README explains the audience, structure, setup, and current status.
- Roadmap makes progress visible.
- External resources are cited and separated from original notes.
- PDFs are not committed.
- CI runs tests on push and pull request.
- Casebook figures are generated from code, not hand-edited.
- Process storyboards are generated from code and tracked as small, reviewable assets.
- Jupyter Book sources are tracked, while generated `_build/` output is ignored.
- Jupyter Book page figures are generated from code and tracked as small, reviewable assets.
- VS Code workspace files are tracked when they improve reproducible study workflows.
- GitHub Pages deployment builds `_site/` from `platform/`, `book/`, and JupyterLite; the public site is served from `https://hollis36.github.io/robotic-manipulation-learning/`, and automatic deployment remains gated to public repositories.

## Study Quality

- Learning sessions are logged in `docs/study_sessions/`.
- Chapter notes are written in my own words.
- Exercises include answers or reflection prompts.
- Capstone ideas are linked back to chapter concepts.

## DSE Quality Loop

Score the repository periodically:

```bash
python tools/score_repository.py
```

Use low-scoring categories to choose the next improvement pass.

Generate visual assets:

```bash
python tools/generate_casebook_figures.py docs/assets/casebook
python tools/generate_casebook_figures.py --storyboards docs/assets/storyboards
python tools/generate_book_figures.py
```

Build the learning book:

```bash
make book-build
```

Run the full local verification loop:

```bash
make verify
```
