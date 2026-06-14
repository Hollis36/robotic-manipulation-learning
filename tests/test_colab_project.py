import json
import struct
import subprocess
import sys
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
CONCEPT_IMAGES = {
    "02_transforms_kinematics_ik.ipynb": "02_transforms_kinematics_ik_concept.png",
    "03_geometric_perception_icp.ipynb": "03_geometric_perception_icp_concept.png",
    "04_grasp_scoring.ipynb": "04_grasp_scoring_concept.png",
    "05_motion_planning_rrt.ipynb": "05_motion_planning_rrt_concept.png",
    "06_control_pd_impedance.ipynb": "06_control_pd_impedance_concept.png",
    "07_segmentation_to_grasp.ipynb": "07_segmentation_to_grasp_concept.png",
    "08_rl_gridworld.ipynb": "08_rl_gridworld_concept.png",
}

REQUIRED_COLAB_MARKDOWN = [
    "## Concept Map",
    "## Result Figure",
    "## Parameter Experiment",
    "## Reflection Prompt",
]
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
CONCEPT_IMAGE_WIDTH = 1600
CONCEPT_IMAGE_HEIGHT = 900
SVG_STYLE_MARKER = 'data-rml-style="technical-svg-v1"'


def _cell_source(cell: dict) -> str:
    source = cell["source"]
    return source if isinstance(source, str) else "".join(source)


def _notebook_cells(path: Path) -> list[dict]:
    content = json.loads(path.read_text())
    return content["cells"]


def _notebook_text(path: Path) -> str:
    sources = [_cell_source(cell) for cell in _notebook_cells(path)]
    return "\n\n".join(sources)


def _notebook_cell_text(path: Path, cell_type: str) -> str:
    sources = []
    for cell in _notebook_cells(path):
        if cell["cell_type"] == cell_type:
            sources.append(_cell_source(cell))
    return "\n\n".join(sources)


def _png_dimensions(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    assert header[:8] == PNG_SIGNATURE, path
    assert len(header) == 24, path
    ihdr_length, ihdr_type = struct.unpack(">I4s", header[8:16])
    assert ihdr_length == 13, path
    assert ihdr_type == b"IHDR", path
    return struct.unpack(">II", header[16:24])


def test_colab_concept_image_inventory_matches_notebook_inventory():
    assert set(CONCEPT_IMAGES) == set(NOTEBOOKS)


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
    assert "concept-gallery" in colab_html
    for notebook in NOTEBOOKS:
        assert f"{COLAB_BASE}/{notebook}" in colab_html
    for image_name in CONCEPT_IMAGES.values():
        assert f"assets/colab/{image_name}" in colab_html


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


def test_colab_svg_illustrations_are_part_of_local_build_workflow():
    makefile = Path("Makefile").read_text()
    online_builder = Path("tools/build_online_platform.py").read_text()

    assert "colab-figures:" in makefile
    assert "python tools/generate_colab_svg_illustrations.py" in makefile
    assert "colab-figures" in makefile.split("verify:", maxsplit=1)[1]
    assert 'site_root / "assets" / "colab"' in online_builder


def test_score_repository_tracks_colab_project_support():
    report = score_repository(Path("."))

    assert "colab_project" in report["categories"]
    assert report["categories"]["colab_project"]["total"] == 8
    assert report["categories"]["colab_project"]["score"] == 100


def test_svg_illustration_generator_exports_complete_colab_asset_set(tmp_path):
    result = subprocess.run(
        [sys.executable, "tools/generate_colab_svg_illustrations.py", str(tmp_path)],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    for image_name in CONCEPT_IMAGES.values():
        stem = Path(image_name).stem
        svg_path = tmp_path / "svg" / f"{stem}.svg"
        png_path = tmp_path / image_name

        assert svg_path.exists(), svg_path
        svg_text = svg_path.read_text()
        assert SVG_STYLE_MARKER in svg_text
        assert len(svg_text) > 8_000

        assert png_path.exists(), png_path
        assert png_path.stat().st_size > 20_000, png_path
        assert _png_dimensions(png_path) == (CONCEPT_IMAGE_WIDTH, CONCEPT_IMAGE_HEIGHT)


def test_colab_notebooks_include_concept_result_and_parameter_sections():
    for notebook, image_name in CONCEPT_IMAGES.items():
        notebook_path = Path("book") / notebook
        markdown_text = _notebook_cell_text(notebook_path, "markdown")
        code_text = _notebook_cell_text(notebook_path, "code")

        for heading in REQUIRED_COLAB_MARKDOWN:
            assert heading in markdown_text, f"{notebook} missing {heading}"
        assert f"assets/colab/{image_name}" in markdown_text
        assert "matplotlib.pyplot as plt" in code_text
        assert "COLAB_PARAMETER_EXPERIMENT" in code_text


def test_colab_visual_prompt_catalog_covers_every_concept_image():
    prompt_file = Path("docs/colab_visual_prompts.md")

    assert prompt_file.exists()
    text = prompt_file.read_text()
    assert "professional robotics education illustration" in text
    assert "negative prompt" in text.lower()

    for notebook, image_name in CONCEPT_IMAGES.items():
        assert notebook in text
        assert image_name in text
        assert "book/assets/colab/" + image_name in text


def test_colab_concept_images_exist_and_are_large_enough():
    image_dir = Path("book/assets/colab")

    for image_name in CONCEPT_IMAGES.values():
        image_path = image_dir / image_name
        assert image_path.exists(), image_path
        assert image_path.stat().st_size > 20_000, image_path
        assert _png_dimensions(image_path) == (CONCEPT_IMAGE_WIDTH, CONCEPT_IMAGE_HEIGHT)


def test_lite_workspace_receives_colab_concept_images(tmp_path):
    result = subprocess.run(
        [sys.executable, "tools/prepare_lite_workspace.py", str(tmp_path)],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    for image_name in CONCEPT_IMAGES.values():
        assert (tmp_path / "notebooks" / "assets" / "colab" / image_name).exists()
