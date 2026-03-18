from __future__ import annotations

from agent.state import AgentState


async def route_after_intent(state: AgentState) -> str:
    intent = state["intent"]
    if intent == "local":
        return "retriever_local"
    if intent == "web":
        return "retriever_web"
    return "retriever_local"


async def route_after_local(state: AgentState) -> str:
    if state["intent"] == "hybrid":
        return "retriever_web"
    return "reranker"
