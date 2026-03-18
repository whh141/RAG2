from agent.state import AgentState


def route_by_intent(state: AgentState) -> str:
    intent = state.get("intent", "local")
    if intent == "web":
        return "retriever_web"
    if intent == "hybrid":
        return "retriever_local"
    return "retriever_local"
