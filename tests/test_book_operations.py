from pathlib import Path

from tools.score_repository import score_repository


def test_makefile_exposes_learning_workflow_targets():
    makefile = Path("Makefile")

    assert makefile.exists()
    text = makefile.read_text()
    for target in [
        "test:",
        "score:",
        "casebook:",
        "book-install:",
        "book-build:",
        "book-serve:",
        "book-clean:",
        "verify:",
    ]:
        assert target in text

    assert "jupyter-book build --html --strict" in text
    assert "jupyter-book start" in text


def test_book_workflow_guide_links_commands_and_pages_constraint():
    guide = Path("docs/book_workflow.md")

    assert guide.exists()
    text = guide.read_text()
    assert "make book-build" in text
    assert "make book-serve" in text
    assert "make verify" in text
    assert "https://hollis36.github.io/robotic-manipulation-learning/" in text
    assert "private Pages support" in text
    assert "GitHub Pages" in text


def test_readme_points_to_book_workflow_guide():
    readme = Path("README.md").read_text()

    assert "docs/book_workflow.md" in readme
    assert "make book-build" in readme


def test_score_repository_tracks_book_workflow_assets():
    report = score_repository(Path("."))

    assert "book_workflow" in report["categories"]
    assert report["categories"]["book_workflow"]["total"] == 2
