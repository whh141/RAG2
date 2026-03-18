from __future__ import annotations

from uuid import uuid4

import chromadb
import httpx

from config import settings


class VectorIndex:
    def __init__(self) -> None:
        settings.chroma_dir.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(settings.chroma_dir))
        self.collection = self.client.get_or_create_collection(name=settings.chroma_collection)

    def add_documents(self, filename: str, chunks: list[str]) -> int:
        ids = [str(uuid4()) for _ in chunks]
        embeddings = self._embed(chunks)
        metadatas = [{"filename": filename, "chunk": index + 1} for index, _ in enumerate(chunks)]
        self.collection.upsert(ids=ids, documents=chunks, embeddings=embeddings, metadatas=metadatas)
        return len(chunks)

    def clear(self) -> None:
        self.client.delete_collection(settings.chroma_collection)
        self.collection = self.client.get_or_create_collection(name=settings.chroma_collection)

    def count(self) -> int:
        return self.collection.count()

    def search(self, query: str, limit: int = 6) -> list[dict]:
        result = self.collection.query(query_embeddings=[self._embed([query])[0]], n_results=limit)
        ids = result.get("ids", [[]])[0]
        docs = result.get("documents", [[]])[0]
        metas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]
        rows = []
        for doc_id, document, metadata, distance in zip(ids, docs, metas, distances):
            rows.append(
                {
                    "id": doc_id,
                    "source": metadata["filename"],
                    "title": metadata["filename"],
                    "content": document,
                    "score": 1 - float(distance),
                    "metadata": metadata,
                }
            )
        return rows

    def _embed(self, texts: list[str]) -> list[list[float]]:
        response = httpx.post(
            f"{settings.zhipu_base_url}/embeddings",
            headers={"Authorization": f"Bearer {settings.zhipu_api_key}"},
            json={"model": settings.glm_embedding_model, "input": texts},
            timeout=60.0,
        )
        response.raise_for_status()
        payload = response.json()
        return [item["embedding"] for item in payload["data"]]
