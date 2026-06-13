import json
from pathlib import Path

import yaml

from tools.score_repository import score_repository


BOOK_ROOT = Path("book")


def test_jupyter_book_config_and_toc_exist():
    assert (BOOK_ROOT / "_config.yml").exists()
    assert (BOOK_ROOT / "_toc.yml").exists()
    assert (BOOK_ROOT / "myst.yml").exists()
    assert Path("requirements-book.txt").exists()


def test_jupyter_book_toc_points_to_existing_sources():
    toc = yaml.safe_load((BOOK_ROOT / "_toc.yml").read_text())

    assert toc["root"] == "intro"
    sources = [BOOK_ROOT / f"{toc['root']}.md"]
    for chapter in toc["chapters"]:
        sources.append(BOOK_ROOT / chapter["file"])

    missing = [path for path in sources if not path.exists()]
    assert missing == []


def test_jupyter_book_notebooks_are_valid_and_reuse_package_code():
    notebooks = sorted(BOOK_ROOT.glob("*.ipynb"))

    assert len(notebooks) >= 7
    for notebook_path in notebooks:
        notebook = json.loads(notebook_path.read_text())
        assert notebook["nbformat"] == 4
        assert notebook["cells"]

    code = "\n".join(
        cell["source"] if isinstance(cell["source"], str) else "".join(cell["source"])
        for notebook_path in notebooks
        for cell in json.loads(notebook_path.read_text())["cells"]
        if cell["cell_type"] == "code"
    )
    assert "from rml." in code


def test_book_requirements_include_jupyter_book():
    requirements = Path("requirements-book.txt").read_text()

    assert "jupyter-book" in requirements
    assert "-r requirements.txt" in requirements


def test_score_repository_tracks_jupyter_book_assets():
    report = score_repository(Path("."))

    assert "jupyter_book" in report["categories"]
    assert report["categories"]["jupyter_book"]["total"] == 14
