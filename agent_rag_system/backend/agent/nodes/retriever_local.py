from __future__ import annotations

from agent.state import AgentState
from knowledge.vector_index import VectorIndex


async def retrieve_local(state: AgentState) -> AgentState:
    documents = VectorIndex().search(state["query"], limit=6)
    state["retrieved_docs"] = [*state.get("retrieved_docs", []), *documents]
    await state["event_emitter"].emit(
        "node_status",
        "retriever_local",
        f"ChromaDB 检索完成，命中 {len(documents)} 条候选片段。",
    )
    return state
