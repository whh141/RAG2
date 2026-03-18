from __future__ import annotations

import json

from agent.llm import chat_text
from agent.prompts import COMPRESSOR_PROMPT
from agent.state import AgentState


async def compress_context(state: AgentState) -> AgentState:
    payload = {
        "query": state["query"],
        "documents": [
            {
                "title": doc["title"],
                "source": doc["source"],
                "content": doc["content"],
            }
            for doc in state.get("reranked_docs", [])
        ],
    }
    facts = json.loads(chat_text(COMPRESSOR_PROMPT, json.dumps(payload, ensure_ascii=False)))
    state["facts"] = facts
    await state["event_emitter"].emit(
        "node_status",
        "compressor",
        f"上下文压缩完成，提炼出 {len(facts)} 条核心事实。",
    )
    return state
