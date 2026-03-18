from __future__ import annotations

from agent.state import AgentState


def classify_intent(state: AgentState) -> AgentState:
    query = state["query"]
    lowered = query.lower()
    if any(token in query for token in ["今天", "今日", "最近", "新闻"]) or "today" in lowered:
        intent = "web"
        reason = "检测到时效性表达，优先外部搜索。"
    elif any(token in query for token in ["同时", "对比", "结合", "并且"]):
        intent = "hybrid"
        reason = "问题含有综合推理信号，走多源路由。"
    else:
        intent = "local"
        reason = "问题更像稳定知识问答，优先本地知识库。"

    state["intent"] = intent
    state.setdefault("node_logs", []).append(
        {"node": "intent_classifier", "message": f"识别结果：{intent}；原因：{reason}"}
    )
    return state
