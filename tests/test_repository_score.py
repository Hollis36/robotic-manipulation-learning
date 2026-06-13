from pathlib import Path

from tools.score_repository import score_repository


def test_score_repository_reports_core_quality_categories():
    report = score_repository(Path("."))

    assert report["total_score"] >= 80
    assert report["categories"]["chapter_coverage"]["passed"] >= 11
    assert report["categories"]["casebook"]["passed"] >= 9
    assert report["categories"]["tests"]["passed"] >= 8
    assert "recommendations" in report


def test_score_repository_penalizes_missing_required_files(tmp_path):
    (tmp_path / "chapters").mkdir()
    (tmp_path / "casebook").mkdir()

    report = score_repository(tmp_path)

    assert report["total_score"] < 50
    assert report["categories"]["top_level_docs"]["score"] == 0

