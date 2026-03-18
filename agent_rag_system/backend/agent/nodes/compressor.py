from __future__ import annotations

from agent.state import AgentState, Fact


def compress_context(state: AgentState) -> AgentState:
    facts: list[Fact] = []
    for index, doc in enumerate(state.get("reranked_docs", []), start=1):
        snippet = doc["content"][:120].replace("\n", " ")
        facts.append({"id": index, "statement": snippet, "source": doc["title"]})
    state["facts"] = facts
    state.setdefault("node_logs", []).append(
        {"node": "compressor", "message": f"事实提炼完成，生成 {len(facts)} 条 facts。"}
    )
    return state
