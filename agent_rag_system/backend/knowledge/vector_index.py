from __future__ import annotations

import json
from pathlib import Path
from typing import Any

STORE_PATH = Path(__file__).resolve().parent / "vector_store.json"


class VectorIndex:
    def __init__(self) -> None:
        if not STORE_PATH.exists():
            STORE_PATH.write_text("[]", encoding="utf-8")

    def add_documents(self, filename: str, chunks: list[str]) -> int:
        rows = self._read()
        start = len(rows) + 1
        for offset, chunk in enumerate(chunks):
            rows.append(
                {
                    "id": f"local-{start + offset}",
                    "source": filename,
                    "title": filename,
                    "content": chunk,
                    "score": 0.0,
                }
            )
        self._write(rows)
        return len(chunks)

    def clear(self) -> None:
        self._write([])

    def count(self) -> int:
        return len(self._read())

    def search(self, query: str, limit: int = 4) -> list[dict[str, Any]]:
        docs = self._read()
        query_terms = [term for term in query.lower().split() if term]
        for doc in docs:
            content = doc["content"].lower()
            doc["score"] = sum(content.count(term) for term in query_terms) or 0.1
        ordered = sorted(docs, key=lambda item: item["score"], reverse=True)
        return ordered[:limit]

    def _read(self) -> list[dict[str, Any]]:
        return json.loads(STORE_PATH.read_text(encoding="utf-8"))

    def _write(self, rows: list[dict[str, Any]]) -> None:
        STORE_PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
