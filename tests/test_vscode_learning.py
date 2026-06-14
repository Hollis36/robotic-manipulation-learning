import json
from pathlib import Path

from tools.score_repository import score_repository


def test_vscode_tasks_expose_learning_workflow():
    tasks_path = Path(".vscode/tasks.json")

    assert tasks_path.exists()
    tasks = json.loads(tasks_path.read_text())
    labels = {task["label"] for task in tasks["tasks"]}

    assert {
        "RML: Install Book Environment",
        "RML: Verify Repository",
        "RML: Serve Jupyter Book",
        "RML: Build Jupyter Book",
        "RML: Regenerate Book Figures",
        "RML: Regenerate Notebooks",
        "RML: Run First Casebook Example",
    }.issubset(labels)


def test_vscode_recommends_python_jupyter_extensions():
    extensions_path = Path(".vscode/extensions.json")

    assert extensions_path.exists()
    recommendations = set(json.loads(extensions_path.read_text())["recommendations"])

    assert "ms-python.python" in recommendations
    assert "ms-toolsai.jupyter" in recommendations
    assert "ms-python.vscode-pylance" in recommendations


def test_vscode_settings_point_at_project_python_paths():
    settings_path = Path(".vscode/settings.json")

    assert settings_path.exists()
    settings = json.loads(settings_path.read_text())

    assert "src" in settings["python.analysis.extraPaths"]
    assert settings["python.testing.pytestEnabled"] is True
    assert settings["python.testing.pytestArgs"] == ["tests"]


def test_vscode_learning_guide_has_first_session_steps():
    guide = Path("docs/vscode_learning.md")

    assert guide.exists()
    text = guide.read_text()

    for expected in [
        "RML: Install Book Environment",
        "RML: Serve Jupyter Book",
        "book/intro.md",
        "book/02_transforms_kinematics_ik.ipynb",
        "casebook/001_spatial_transforms_numpy/run.py",
        "Reflection Template",
    ]:
        assert expected in text


def test_score_repository_tracks_vscode_learning_assets():
    report = score_repository(Path("."))

    assert "vscode_learning" in report["categories"]
    assert report["categories"]["vscode_learning"]["total"] == 4
