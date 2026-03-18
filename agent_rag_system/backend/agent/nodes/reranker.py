from __future__ import annotations

from sentence_transformers import CrossEncoder

from config import settings
from agent.state import AgentState


_reranker = CrossEncoder(settings.reranker_model)


async def rerank_documents(state: AgentState) -> AgentState:
    documents = state.get("retrieved_docs", [])
    pairs = [[state["query"], doc["content"]] for doc in documents]
    scores = _reranker.predict(pairs) if pairs else []
    reranked = []
    for doc, score in zip(documents, scores):
        reranked.append({**doc, "score": float(score)})
    reranked.sort(key=lambda item: item["score"], reverse=True)
    state["reranked_docs"] = reranked[:4]
    await state["event_emitter"].emit(
        "node_status",
        "reranker",
        {
            "summary": f"Cross-Encoder 重排序完成，保留 {len(state['reranked_docs'])} 条高相关文档。",
            "documents": [
                {
                    "title": document["title"],
                    "score": round(document["score"], 4),
                    "preview": document["content"][:180],
                }
                for document in state["reranked_docs"]
            ],
        },
    )
    return state
