"""Score this learning repository against its quality standard."""

from __future__ import annotations

import json
from pathlib import Path


def _count_existing(paths: list[Path]) -> int:
    return sum(1 for path in paths if path.exists())


def _category(score: int, passed: int, total: int) -> dict:
    return {"score": score, "passed": passed, "total": total}


def _book_page_text(path: Path) -> str:
    if path.suffix == ".ipynb":
        notebook = json.loads(path.read_text())
        return "\n\n".join(
            cell["source"] if isinstance(cell["source"], str) else "".join(cell["source"])
            for cell in notebook["cells"]
            if cell["cell_type"] == "markdown"
        )
    return path.read_text()


def score_repository(root: Path) -> dict:
    """Return a simple quality report for the repository."""
    root = Path(root)

    top_level_required = [
        root / "README.md",
        root / "ROADMAP.md",
        root / "CITATION.md",
        root / "requirements.txt",
        root / "pyproject.toml",
    ]
    top_level_passed = _count_existing(top_level_required)

    chapter_dirs = list((root / "chapters").glob("ch*")) if (root / "chapters").exists() else []
    chapter_passed = sum(
        1
        for chapter in chapter_dirs
        if (chapter / "README.md").exists()
        and (chapter / "notes.md").exists()
        and (chapter / "exercises.md").exists()
    )

    case_dirs = list((root / "casebook").glob("*")) if (root / "casebook").exists() else []
    case_passed = sum(1 for case in case_dirs if (case / "README.md").exists() and (case / "run.py").exists())

    tests = list((root / "tests").glob("test_*.py")) if (root / "tests").exists() else []
    tools_required = [
        root / "docs" / "deep_course_companion.md",
        root / "docs" / "external_resources.md",
        root / "docs" / "learning_tracks.md",
        root / "docs" / "drake_setup.md",
        root / "docs" / "capstone_portfolio.md",
        root / "docs" / "repository_quality_standard.md",
    ]
    docs_passed = _count_existing(tools_required)

    ci_required = [root / ".github" / "workflows" / "tests.yml"]
    ci_passed = _count_existing(ci_required)
    visual_assets = list((root / "docs" / "assets" / "casebook").glob("*.png")) if (root / "docs" / "assets" / "casebook").exists() else []
    process_visuals = list((root / "docs" / "assets" / "storyboards").glob("*.png")) if (root / "docs" / "assets" / "storyboards").exists() else []
    book_required = [
        root / ".github" / "workflows" / "pages.yml",
        root / "requirements-book.txt",
        root / "book" / "_config.yml",
        root / "book" / "_toc.yml",
        root / "book" / "myst.yml",
        root / "book" / "intro.md",
        root / "book" / "00_manipulation_stack.md",
        root / "book" / "01_robot_setup.md",
        root / "book" / "02_transforms_kinematics_ik.ipynb",
        root / "book" / "03_geometric_perception_icp.ipynb",
        root / "book" / "04_grasp_scoring.ipynb",
        root / "book" / "05_motion_planning_rrt.ipynb",
        root / "book" / "06_control_pd_impedance.ipynb",
        root / "book" / "07_segmentation_to_grasp.ipynb",
        root / "book" / "08_rl_gridworld.ipynb",
    ]
    book_passed = _count_existing(book_required)
    book_workflow_required = [
        root / "Makefile",
        root / "docs" / "book_workflow.md",
    ]
    book_workflow_passed = _count_existing(book_workflow_required)
    book_pages = [
        root / "book" / "intro.md",
        root / "book" / "00_manipulation_stack.md",
        root / "book" / "01_robot_setup.md",
        root / "book" / "02_transforms_kinematics_ik.ipynb",
        root / "book" / "03_geometric_perception_icp.ipynb",
        root / "book" / "04_grasp_scoring.ipynb",
        root / "book" / "05_motion_planning_rrt.ipynb",
        root / "book" / "06_control_pd_impedance.ipynb",
        root / "book" / "07_segmentation_to_grasp.ipynb",
        root / "book" / "08_rl_gridworld.ipynb",
    ]
    scaffold_sections = ["## Learning Objectives", "## Checkpoint", "## Practice Task"]
    book_scaffold_passed = sum(
        1
        for page in book_pages
        if page.exists() and all(section in _book_page_text(page) for section in scaffold_sections)
    )
    book_visuals = [
        root / "book" / "assets" / "figures" / f"{page.stem}.png"
        for page in book_pages
    ]
    book_visuals_passed = _count_existing(book_visuals)
    vscode_required = [
        root / ".vscode" / "tasks.json",
        root / ".vscode" / "settings.json",
        root / ".vscode" / "extensions.json",
        root / "docs" / "vscode_learning.md",
    ]
    vscode_passed = _count_existing(vscode_required)
    online_required = [
        root / "platform" / "index.html",
        root / "platform" / "labs.html",
        root / "platform" / "styles.css",
        root / "requirements-online.txt",
        root / "tools" / "prepare_lite_workspace.py",
        root / "tools" / "build_online_platform.py",
        root / ".devcontainer" / "devcontainer.json",
        root / "docs" / "online_platform.md",
        root / ".github" / "workflows" / "pages.yml",
    ]
    online_passed = _count_existing(online_required)

    categories = {
        "top_level_docs": _category(round(top_level_passed / len(top_level_required) * 100), top_level_passed, len(top_level_required)),
        "chapter_coverage": _category(round(min(chapter_passed, 11) / 11 * 100), chapter_passed, 11),
        "casebook": _category(round(min(case_passed, 9) / 9 * 100), case_passed, 9),
        "tests": _category(round(min(len(tests), 8) / 8 * 100), len(tests), 8),
        "deep_learning_docs": _category(round(docs_passed / len(tools_required) * 100), docs_passed, len(tools_required)),
        "ci": _category(round(ci_passed / len(ci_required) * 100), ci_passed, len(ci_required)),
        "visual_assets": _category(round(min(len(visual_assets), 9) / 9 * 100), len(visual_assets), 9),
        "process_visuals": _category(round(min(len(process_visuals), 2) / 2 * 100), len(process_visuals), 2),
        "jupyter_book": _category(round(book_passed / len(book_required) * 100), book_passed, len(book_required)),
        "book_workflow": _category(round(book_workflow_passed / len(book_workflow_required) * 100), book_workflow_passed, len(book_workflow_required)),
        "book_learning_scaffold": _category(round(book_scaffold_passed / len(book_pages) * 100), book_scaffold_passed, len(book_pages)),
        "book_visuals": _category(round(book_visuals_passed / len(book_visuals) * 100), book_visuals_passed, len(book_visuals)),
        "vscode_learning": _category(round(vscode_passed / len(vscode_required) * 100), vscode_passed, len(vscode_required)),
        "online_platform": _category(round(online_passed / len(online_required) * 100), online_passed, len(online_required)),
    }

    weights = {
        "top_level_docs": 0.13,
        "chapter_coverage": 0.13,
        "casebook": 0.14,
        "tests": 0.15,
        "deep_learning_docs": 0.11,
        "ci": 0.09,
        "visual_assets": 0.07,
        "process_visuals": 0.05,
        "jupyter_book": 0.05,
        "book_workflow": 0.01,
        "book_learning_scaffold": 0.01,
        "book_visuals": 0.02,
        "vscode_learning": 0.02,
        "online_platform": 0.02,
    }
    total_score = round(sum(categories[name]["score"] * weight for name, weight in weights.items()))
    recommendations = []
    for name, result in categories.items():
        if result["score"] < 100:
            recommendations.append(f"Improve {name}: {result['passed']}/{result['total']} checks passed.")

    return {
        "total_score": total_score,
        "categories": categories,
        "recommendations": recommendations,
    }


def main() -> None:
    report = score_repository(Path("."))
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
