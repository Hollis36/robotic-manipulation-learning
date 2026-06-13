import json
from pathlib import Path

import yaml

from tools.score_repository import score_repository


BOOK_ROOT = Path("book")
REQUIRED_SECTIONS = ["## Learning Objectives", "## Checkpoint", "## Practice Task"]


def _book_sources() -> list[Path]:
    toc = yaml.safe_load((BOOK_ROOT / "_toc.yml").read_text())
    sources = [BOOK_ROOT / f"{toc['root']}.md"]
    sources.extend(BOOK_ROOT / chapter["file"] for chapter in toc["chapters"])
    return sources


def _source_text(path: Path) -> str:
    if path.suffix == ".ipynb":
        notebook = json.loads(path.read_text())
        return "\n\n".join(
            cell["source"] if isinstance(cell["source"], str) else "".join(cell["source"])
            for cell in notebook["cells"]
            if cell["cell_type"] == "markdown"
        )
    return path.read_text()


def test_every_book_page_has_learner_scaffold():
    missing = {}
    for source in _book_sources():
        text = _source_text(source)
        missing_sections = [section for section in REQUIRED_SECTIONS if section not in text]
        if missing_sections:
            missing[source.name] = missing_sections

    assert missing == {}


def test_generated_notebooks_preserve_learning_scaffold():
    generator = Path("tools/generate_jupyter_book_notebooks.py").read_text()

    for section in REQUIRED_SECTIONS:
        assert section in generator


def test_score_repository_tracks_book_learning_scaffold():
    report = score_repository(Path("."))

    assert "book_learning_scaffold" in report["categories"]
    assert report["categories"]["book_learning_scaffold"]["total"] == 10
