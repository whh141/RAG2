from __future__ import annotations

from agent.llm import chat_json
from agent.prompts import INTENT_CLASSIFIER_PROMPT
from agent.state import AgentState


async def classify_intent(state: AgentState) -> AgentState:
    result = chat_json(INTENT_CLASSIFIER_PROMPT, state["query"])
    state["intent"] = result["intent"]
    state["intent_reason"] = result["reason"]
    await state["event_emitter"].emit(
        "node_status",
        "intent_classifier",
        {
            "summary": f"识别为 {state['intent']}",
            "intent": state["intent"],
            "reason": state["intent_reason"],
        },
    )
    return state
