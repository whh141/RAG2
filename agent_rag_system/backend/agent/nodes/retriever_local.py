from __future__ import annotations

from agent.state import AgentState
from knowledge.vector_index import VectorIndex


def retrieve_local(state: AgentState) -> AgentState:
    docs = VectorIndex().search(state["query"], limit=4)
    state["retrieved_docs"] = docs
    state.setdefault("node_logs", []).append(
        {"node": "retriever_local", "message": f"本地检索完成，命中 {len(docs)} 条文档。"}
    )
    return state
