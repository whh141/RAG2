from __future__ import annotations

import json

from agent.llm import chat_text
from agent.prompts import GENERATOR_PROMPT
from agent.state import AgentState


async def generate_answer(state: AgentState) -> AgentState:
    payload = {
        "query": state["query"],
        "facts": state.get("facts", []),
    }
    answer = chat_text(GENERATOR_PROMPT, json.dumps(payload, ensure_ascii=False))
    state["answer"] = answer
    state["citations"] = state.get("facts", [])
    await state["event_emitter"].emit("node_status", "generator", "最终答案生成完成。")
    return state
