import json
from pathlib import Path

from tools.score_repository import score_repository


REPO = "Hollis36/robotic-manipulation-learning"
COLAB_BASE = f"https://colab.research.google.com/github/{REPO}/blob/main/book"
NOTEBOOKS = [
    "02_transforms_kinematics_ik.ipynb",
    "03_geometric_perception_icp.ipynb",
    "04_grasp_scoring.ipynb",
    "05_motion_planning_rrt.ipynb",
    "06_control_pd_impedance.ipynb",
    "07_segmentation_to_grasp.ipynb",
    "08_rl_gridworld.ipynb",
]


def test_colab_guide_links_every_learning_notebook():
    guide = Path("docs/colab.md")

    assert guide.exists()
    text = guide.read_text()
    assert "Google Colab" in text
    assert "git clone --depth 1" in text
    assert "rml" in text

    for notebook in NOTEBOOKS:
        assert f"{COLAB_BASE}/{notebook}" in text


def test_online_platform_exposes_colab_route_and_notebook_links():
    labs = Path("platform/labs.html").read_text()
    colab_page = Path("platform/colab.html")

    assert colab_page.exists()
    assert "colab.html" in labs
    assert "Google Colab" in labs

    colab_html = colab_page.read_text()
    assert "Open In Colab" in colab_html
    for notebook in NOTEBOOKS:
        assert f"{COLAB_BASE}/{notebook}" in colab_html


def test_generated_notebooks_bootstrap_colab_repository_source():
    generator = Path("tools/generate_jupyter_book_notebooks.py").read_text()

    assert "COLAB_REPO_URL" in generator
    assert "google.colab" in generator
    assert "git clone --depth 1" in generator
    assert "/content/robotic-manipulation-learning" in generator

    for notebook in NOTEBOOKS:
        content = json.loads((Path("book") / notebook).read_text())
        setup_sources = [
            cell["source"]
            for cell in content["cells"]
            if cell["cell_type"] == "code" and "PROJECT_ROOT" in cell["source"]
        ]
        assert setup_sources
        assert "COLAB_REPO_URL" in setup_sources[0]
        assert "git clone" in setup_sources[0]


def test_score_repository_tracks_colab_project_support():
    report = score_repository(Path("."))

    assert "colab_project" in report["categories"]
    assert report["categories"]["colab_project"]["total"] == 4
    assert report["categories"]["colab_project"]["score"] == 100
