# Repository Quality Standard

This is the quality bar for making the repository useful to future readers, including my future self.

## Learning Quality

- Every chapter has learner-owned notes.
- Every major concept connects to a runnable case or planned lab.
- Every case has a README, run command, expected output, and chapter link.
- Every case has a generated visual asset when a picture clarifies the idea.
- Core iterative algorithms have process visualizations when the intermediate states teach more than the final answer.
- Every advanced topic has a clear prerequisite.
- Failure modes are documented, not hidden.

## Engineering Quality

- Tests run with `pytest -q`.
- Concept cases avoid heavyweight dependencies.
- Drake labs are optional and skip cleanly if pydrake is unavailable.
- Generated outputs are either ignored or intentionally small.
- Code is deterministic by default.

## GitHub Quality

- README explains the audience, structure, setup, and current status.
- Roadmap makes progress visible.
- External resources are cited and separated from original notes.
- PDFs are not committed.
- CI runs tests on push and pull request.
- Casebook figures are generated from code, not hand-edited.
- Process storyboards are generated from code and tracked as small, reviewable assets.

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
```
