"""Score this learning repository against its quality standard."""

from __future__ import annotations

import json
from pathlib import Path


def _count_existing(paths: list[Path]) -> int:
    return sum(1 for path in paths if path.exists())


def _category(score: int, passed: int, total: int) -> dict:
    return {"score": score, "passed": passed, "total": total}


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

    categories = {
        "top_level_docs": _category(round(top_level_passed / len(top_level_required) * 100), top_level_passed, len(top_level_required)),
        "chapter_coverage": _category(round(min(chapter_passed, 11) / 11 * 100), chapter_passed, 11),
        "casebook": _category(round(min(case_passed, 9) / 9 * 100), case_passed, 9),
        "tests": _category(round(min(len(tests), 8) / 8 * 100), len(tests), 8),
        "deep_learning_docs": _category(round(docs_passed / len(tools_required) * 100), docs_passed, len(tools_required)),
        "ci": _category(round(ci_passed / len(ci_required) * 100), ci_passed, len(ci_required)),
    }

    weights = {
        "top_level_docs": 0.15,
        "chapter_coverage": 0.2,
        "casebook": 0.2,
        "tests": 0.15,
        "deep_learning_docs": 0.2,
        "ci": 0.1,
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

