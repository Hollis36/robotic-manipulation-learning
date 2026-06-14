"""Build the GitHub Pages online learning platform."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.prepare_lite_workspace import prepare_lite_workspace

SITE_ROOT = PROJECT_ROOT / "_site"
LITE_CONTENTS = PROJECT_ROOT / "_online" / "lite_files"


def run(command: list[str], cwd: Path = PROJECT_ROOT, env: dict[str, str] | None = None) -> None:
    process_env = os.environ.copy()
    if env:
        process_env.update(env)
    subprocess.run(command, cwd=cwd, env=process_env, check=True)


def copy_platform_shell(site_root: Path) -> None:
    site_root.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PROJECT_ROOT / "platform" / "index.html", site_root / "index.html")
    shutil.copy2(PROJECT_ROOT / "platform" / "styles.css", site_root / "styles.css")
    figures_root = site_root / "assets" / "figures"
    figures_root.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PROJECT_ROOT / "book" / "assets" / "figures" / "intro.png", figures_root / "intro.png")


def copy_book(site_root: Path) -> None:
    book_output = PROJECT_ROOT / "book" / "_build" / "html"
    book_base_url = os.environ.get("BOOK_BASE_URL", "/book")
    run(
        ["jupyter-book", "build", "--html", "--strict"],
        cwd=PROJECT_ROOT / "book",
        env={"BASE_URL": book_base_url},
    )
    shutil.copytree(book_output, site_root / "book", dirs_exist_ok=True)


def build_lite(site_root: Path) -> None:
    prepare_lite_workspace(LITE_CONTENTS)
    run(
        [
            "jupyter",
            "lite",
            "build",
            "--contents",
            str(LITE_CONTENTS),
            "--output-dir",
            str(site_root / "lite"),
        ]
    )


def build_online_platform(site_root: Path | str = SITE_ROOT) -> Path:
    site_root = Path(site_root)
    if site_root.exists():
        shutil.rmtree(site_root)
    copy_platform_shell(site_root)
    copy_book(site_root)
    build_lite(site_root)
    return site_root


def main() -> None:
    site_root = Path(sys.argv[1]) if len(sys.argv) > 1 else SITE_ROOT
    print(build_online_platform(site_root))


if __name__ == "__main__":
    main()
