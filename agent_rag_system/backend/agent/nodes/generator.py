from __future__ import annotations

from agent.state import AgentState


def generate_answer(state: AgentState) -> AgentState:
    facts = state.get("facts", [])
    if not facts:
        answer = "当前没有可用事实，无法生成答案。"
    else:
        joined = "；".join(f"{fact['statement']}[{fact['id']}]" for fact in facts)
        answer = f"基于检索与压缩结果，得到如下回答：{joined}"
    state["answer"] = answer
    state["citations"] = facts
    state.setdefault("node_logs", []).append(
        {"node": "generator", "message": "答案生成完成。"}
    )
    return state
