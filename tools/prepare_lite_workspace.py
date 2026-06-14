"""Prepare notebooks and package files for the browser JupyterLite workspace."""

from __future__ import annotations

from pathlib import Path
import shutil
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = PROJECT_ROOT / "_online" / "lite_files"


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def prepare_lite_workspace(output_dir: Path | str = DEFAULT_OUTPUT) -> list[Path]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    copied: list[Path] = []
    notebooks_dir = output_dir / "notebooks"
    for notebook in sorted((PROJECT_ROOT / "book").glob("*.ipynb")):
        target = notebooks_dir / notebook.name
        copy_file(notebook, target)
        copied.append(target)

    figures_source = PROJECT_ROOT / "book" / "assets" / "figures"
    figures_target = notebooks_dir / "assets" / "figures"
    shutil.copytree(figures_source, figures_target, dirs_exist_ok=True)
    copied.extend(sorted(figures_target.glob("*.png")))

    colab_source = PROJECT_ROOT / "book" / "assets" / "colab"
    colab_target = notebooks_dir / "assets" / "colab"
    shutil.copytree(colab_source, colab_target, dirs_exist_ok=True)
    copied.extend(sorted(colab_target.glob("*.png")))

    package_source = PROJECT_ROOT / "src" / "rml"
    package_target = output_dir / "src" / "rml"
    shutil.copytree(package_source, package_target, dirs_exist_ok=True)
    copied.extend(sorted(package_target.glob("*.py")))

    readme = output_dir / "README.md"
    readme.write_text(
        "# Robotic Manipulation Browser Lab\n\n"
        "Open `notebooks/02_transforms_kinematics_ik.ipynb` first. "
        "The notebooks use the pure-Python `src/rml` package copied into this JupyterLite workspace.\n",
        encoding="utf-8",
    )
    copied.append(readme)

    for path in copied:
        print(path)
    return copied


def main() -> None:
    output_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUTPUT
    prepare_lite_workspace(output_dir)


if __name__ == "__main__":
    main()
