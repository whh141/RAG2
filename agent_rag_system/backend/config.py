from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    zhipu_api_key: str = os.environ.get("ZHIPUAI_API_KEY", "")
    zhipu_base_url: str = os.environ.get("ZHIPUAI_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")
    glm_chat_model: str = os.environ.get("GLM_CHAT_MODEL", "glm-4-plus")
    glm_embedding_model: str = os.environ.get("GLM_EMBEDDING_MODEL", "embedding-3")
    tavily_api_key: str = os.environ.get("TAVILY_API_KEY", "")
    reranker_model: str = os.environ.get("RERANKER_MODEL", "BAAI/bge-reranker-base")
    chroma_dir: Path = Path(os.environ.get("CHROMA_DIR", Path(__file__).resolve().parent / "knowledge" / "chroma"))
    chroma_collection: str = os.environ.get("CHROMA_COLLECTION", "agent_rag_knowledge")
    upload_dir: Path = Path(os.environ.get("UPLOAD_DIR", Path(__file__).resolve().parent / "knowledge" / "uploads"))


settings = Settings()
