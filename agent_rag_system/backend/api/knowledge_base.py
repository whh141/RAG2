from __future__ import annotations

from fastapi import APIRouter, File, UploadFile

from config import settings
from knowledge.document_parser import parse_document
from knowledge.vector_index import VectorIndex

router = APIRouter()
settings.upload_dir.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_knowledge(file: UploadFile = File(...)) -> dict:
    target = settings.upload_dir / file.filename
    target.write_bytes(await file.read())
    chunks = parse_document(target)
    inserted = VectorIndex().add_documents(file.filename, chunks)
    return {"filename": file.filename, "chunks": inserted, "total_chunks": VectorIndex().count()}


@router.delete("/clear")
def clear_knowledge() -> dict[str, str]:
    VectorIndex().clear()
    return {"status": "cleared"}


@router.get("/stats")
def stats() -> dict[str, int]:
    return {"chunks": VectorIndex().count()}
