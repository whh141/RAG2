from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader


def parse_document(file_path: Path) -> list[str]:
    if file_path.suffix.lower() == ".txt":
        text = file_path.read_text(encoding="utf-8")
    elif file_path.suffix.lower() == ".pdf":
        reader = PdfReader(str(file_path))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        raise ValueError("Only .txt and .pdf are supported")

    return [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
