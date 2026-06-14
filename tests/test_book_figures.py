import json
from pathlib import Path
import os
import subprocess
import sys

import matplotlib.image as mpimg
import yaml

from tools.score_repository import score_repository


BOOK_ROOT = Path("book")
FIGURE_DIR = BOOK_ROOT / "assets" / "figures"


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


def test_generate_book_figures_script_creates_page_visuals(tmp_path):
    script = Path("tools/generate_book_figures.py")

    assert script.exists()

    result = subprocess.run(
        [sys.executable, str(script), str(tmp_path)],
        cwd=Path("."),
        env={**os.environ, "PYTHONPATH": ""},
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    generated = sorted(tmp_path.glob("*.png"))
    assert len(generated) == 10
    for path in generated:
        image = mpimg.imread(path)
        assert image.shape[0] >= 700
        assert image.shape[1] >= 1100
        assert path.stat().st_size > 20_000


def test_every_book_page_embeds_a_dedicated_figure():
    missing = {}
    for source in _book_sources():
        figure_ref = f"assets/figures/{source.stem}.png"
        if figure_ref not in _source_text(source):
            missing[source.name] = figure_ref

    assert missing == {}


def test_tracked_book_figures_exist_for_each_page():
    missing = [source.stem for source in _book_sources() if not (FIGURE_DIR / f"{source.stem}.png").exists()]

    assert missing == []


def test_makefile_generates_book_figures_before_verification():
    makefile = Path("Makefile").read_text()
    verify_line = next(line for line in makefile.splitlines() if line.startswith("verify:"))
    verify_targets = verify_line.removeprefix("verify:").split()

    assert "book-figures:" in makefile
    assert "python tools/generate_book_figures.py" in makefile
    assert "book-figures" in verify_targets
    assert "test" in verify_targets
    assert verify_targets.index("book-figures") < verify_targets.index("test")


def test_score_repository_tracks_book_visual_assets():
    report = score_repository(Path("."))

    assert "book_visuals" in report["categories"]
    assert report["categories"]["book_visuals"]["total"] == 10
