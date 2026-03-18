from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.chat import router as chat_router
from api.knowledge_base import router as knowledge_router

app = FastAPI(title="Agentic RAG System")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(chat_router)
app.include_router(knowledge_router, prefix="/api/knowledge", tags=["knowledge"])


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
