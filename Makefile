.PHONY: test score casebook book-install book-build book-serve book-clean book-figures notebooks verify

test:
	pytest -q

score:
	python tools/score_repository.py

casebook:
	@for f in casebook/*/run.py; do PYTHONPATH=src python "$$f" >/dev/null || exit 1; done
	@printf 'casebook scripts passed\n'

book-install:
	python -m pip install -r requirements-book.txt
	python -m pip install -e .

notebooks:
	python tools/generate_jupyter_book_notebooks.py

book-build:
	cd book && jupyter-book build --html --strict

book-serve:
	cd book && jupyter-book start

book-clean:
	python -c "from pathlib import Path; import shutil; p = Path('book/_build'); shutil.rmtree(p) if p.exists() else None"

book-figures:
	python tools/generate_book_figures.py

verify: test score casebook book-figures notebooks book-build
