from pathlib import Path
import os
import subprocess
import sys

from tools.generate_casebook_figures import generate_all_figures, generate_storyboard_figures
from tools.score_repository import score_repository


def test_generate_all_figures_creates_png_assets(tmp_path):
    generated = generate_all_figures(tmp_path)

    assert len(generated) == 9
    for path in generated:
        assert path.suffix == ".png"
        assert path.exists()
        assert path.stat().st_size > 1_000


def test_score_repository_tracks_visual_assets():
    report = score_repository(Path("."))

    assert "visual_assets" in report["categories"]
    assert report["categories"]["visual_assets"]["total"] == 9


def test_generate_storyboard_figures_creates_process_png_assets(tmp_path):
    generated = generate_storyboard_figures(tmp_path)

    assert len(generated) == 2
    for path in generated:
        assert path.suffix == ".png"
        assert path.exists()
        assert path.stat().st_size > 1_000


def test_score_repository_tracks_process_visual_assets():
    report = score_repository(Path("."))

    assert "process_visuals" in report["categories"]
    assert report["categories"]["process_visuals"]["total"] == 2


def test_generate_casebook_figures_cli_works_without_pythonpath(tmp_path):
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)

    result = subprocess.run(
        [sys.executable, "tools/generate_casebook_figures.py", str(tmp_path)],
        cwd=Path("."),
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert len(list(tmp_path.glob("*.png"))) == 9


def test_generate_storyboard_figures_cli_works_without_pythonpath(tmp_path):
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)

    result = subprocess.run(
        [sys.executable, "tools/generate_casebook_figures.py", "--storyboards", str(tmp_path)],
        cwd=Path("."),
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert len(list(tmp_path.glob("*.png"))) == 2
