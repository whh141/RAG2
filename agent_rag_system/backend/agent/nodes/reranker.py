from __future__ import annotations

from agent.state import AgentState


def rerank_documents(state: AgentState) -> AgentState:
    docs = state.get("retrieved_docs", [])
    reranked = sorted(docs, key=lambda item: item.get("score", 0.0), reverse=True)[:3]
    state["reranked_docs"] = reranked
    state.setdefault("node_logs", []).append(
        {"node": "reranker", "message": f"重排序完成，保留 {len(reranked)} 条文档。"}
    )
    return state
