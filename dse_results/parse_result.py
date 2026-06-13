"""Parse a chapter PDF into lightweight learning-loop metrics.

This helper intentionally reports metadata and section headings only. It does not
write extracted source prose into the repository.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from pypdf import PdfReader


def parse_pdf(path: Path) -> dict:
    reader = PdfReader(str(path))
    headings: list[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        for line in text.splitlines():
            compact = " ".join(line.split())
            if re.match(r"^(\d+\.\d+|[ABC]\.\d+)\s+[A-Z0-9]", compact) and compact not in headings:
                headings.append(compact)
    return {
        "pdf": path.name,
        "pages": len(reader.pages),
        "section_count": len(headings),
        "sections": headings,
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python dse_results/parse_result.py <chapter.pdf>")
    print(json.dumps(parse_pdf(Path(sys.argv[1])), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

