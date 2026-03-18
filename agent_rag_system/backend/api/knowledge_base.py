from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, File, UploadFile

from knowledge.document_parser import parse_document
from knowledge.vector_index import VectorIndex

router = APIRouter()
UPLOAD_DIR = Path(__file__).resolve().parent.parent / "knowledge" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_knowledge(file: UploadFile = File(...)) -> dict:
    target = UPLOAD_DIR / file.filename
    target.write_bytes(await file.read())
    chunks = parse_document(target)
    chunk_count = VectorIndex().add_documents(file.filename, chunks)
    return {"filename": file.filename, "chunks": chunk_count, "total_chunks": VectorIndex().count()}


@router.delete("/clear")
def clear_knowledge() -> dict[str, str]:
    VectorIndex().clear()
    return {"status": "cleared"}


@router.get("/stats")
def stats() -> dict[str, int]:
    return {"chunks": VectorIndex().count()}
