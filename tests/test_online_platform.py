import json
from pathlib import Path
import subprocess
import sys

import yaml

from tools.score_repository import score_repository


def test_online_platform_assets_exist_and_link_learning_surfaces():
    index = Path("platform/index.html")
    labs = Path("platform/labs.html")
    styles = Path("platform/styles.css")

    assert index.exists()
    assert labs.exists()
    assert styles.exists()

    html = index.read_text()
    assert "在线学习平台" in html
    assert "JupyterLite" in html
    assert "GitHub Codespaces" in html
    assert "labs.html" in html
    assert "lite/lab/index.html" in html
    assert "book/" in html
    assert 'src="assets/figures/intro.png"' in html


def test_lab_index_lists_notebook_and_casebook_launches():
    html = Path("platform/labs.html").read_text()

    assert "实验导航" in html
    for notebook in [
        "02_transforms_kinematics_ik.ipynb",
        "03_geometric_perception_icp.ipynb",
        "04_grasp_scoring.ipynb",
        "05_motion_planning_rrt.ipynb",
        "06_control_pd_impedance.ipynb",
        "07_segmentation_to_grasp.ipynb",
        "08_rl_gridworld.ipynb",
    ]:
        assert f"lite/lab/index.html?path=notebooks/{notebook}" in html

    for case_id in ["001", "003", "006", "009"]:
        assert case_id in html
    assert "github.com/codespaces/new" in html


def test_jupyterlite_requirements_and_build_scripts_exist():
    requirements = Path("requirements-online.txt")

    assert requirements.exists()
    text = requirements.read_text()
    assert "jupyterlite-core" in text
    assert "jupyterlite-pyodide-kernel" in text
    assert Path("tools/prepare_lite_workspace.py").exists()
    assert Path("tools/build_online_platform.py").exists()
    build_script = Path("tools/build_online_platform.py").read_text()
    assert '"*.html"' in build_script
    assert '"assets"' in build_script
    assert '"figures"' in build_script
    assert "intro.png" in build_script
    assert "BOOK_BASE_URL" in build_script
    assert '"BASE_URL"' in build_script
    assert "copy_lite_lab_assets" in build_script
    assert "favicon.ico" in build_script


def test_build_script_bootstraps_project_root_for_direct_execution():
    script = Path("tools/build_online_platform.py").read_text()
    helper_import = "from tools.prepare_lite_workspace import prepare_lite_workspace"

    assert "sys.path.insert(0, str(PROJECT_ROOT))" in script
    assert script.index("sys.path.insert") < script.index(helper_import)


def test_prepare_lite_workspace_copies_notebooks_and_package(tmp_path):
    result = subprocess.run(
        [sys.executable, "tools/prepare_lite_workspace.py", str(tmp_path)],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert (tmp_path / "notebooks" / "02_transforms_kinematics_ik.ipynb").exists()
    assert (tmp_path / "src" / "rml" / "__init__.py").exists()
    assert (tmp_path / "README.md").exists()


def test_makefile_exposes_online_platform_targets():
    makefile = Path("Makefile").read_text()

    for target in [
        "online-install:",
        "online-lite-contents:",
        "online-build:",
        "online-serve:",
    ]:
        assert target in makefile

    assert "python tools/build_online_platform.py" in makefile


def test_vscode_tasks_cover_online_platform_and_casebook_execution():
    tasks = json.loads(Path(".vscode/tasks.json").read_text())["tasks"]
    labels = {task["label"]: task["command"] for task in tasks}

    assert labels["RML: Install Online Platform Environment"] == "make online-install"
    assert labels["RML: Build Online Platform"] == "make online-build"
    assert labels["RML: Serve Online Platform"] == "make online-serve"
    assert labels["RML: Run All Casebook Examples"] == "make casebook"


def test_pages_workflow_builds_online_platform_artifact():
    workflow = yaml.safe_load(Path(".github/workflows/pages.yml").read_text())
    build_steps = workflow["jobs"]["build"]["steps"]
    commands = "\n".join(str(step.get("run", "")) for step in build_steps)
    workflow_text = Path(".github/workflows/pages.yml").read_text()

    assert "pip install -r requirements-online.txt" in commands
    assert "python tools/build_online_platform.py" in commands
    assert "BOOK_BASE_URL" in workflow_text
    assert "path: _site" in workflow_text


def test_codespaces_devcontainer_supports_online_compilation():
    devcontainer = Path(".devcontainer/devcontainer.json")

    assert devcontainer.exists()
    config = json.loads(devcontainer.read_text())

    assert "python" in config["image"]
    assert "requirements-online.txt" in config["postCreateCommand"]
    assert 3000 in config["forwardPorts"]
    assert 8000 in config["forwardPorts"]
    assert "ms-toolsai.jupyter" in config["customizations"]["vscode"]["extensions"]


def test_online_platform_guide_and_score_category_exist():
    guide = Path("docs/online_platform.md")

    assert guide.exists()
    text = guide.read_text()
    assert "GitHub Pages" in text
    assert "JupyterLite" in text
    assert "Codespaces" in text

    report = score_repository(Path("."))
    assert "online_platform" in report["categories"]
    assert report["categories"]["online_platform"]["total"] == 9
