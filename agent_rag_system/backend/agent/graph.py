from __future__ import annotations

from collections.abc import AsyncGenerator

from agent.state import AgentState
from agent.nodes.compressor import compress_context
from agent.nodes.generator import generate_answer
from agent.nodes.intent_classifier import classify_intent
from agent.nodes.reranker import rerank_documents
from agent.nodes.retriever_local import retrieve_local
from agent.nodes.retriever_web import retrieve_web


async def run_agent_stream(query: str) -> AsyncGenerator[dict, None]:
    state: AgentState = {"query": query, "node_logs": [], "retrieved_docs": []}

    state = classify_intent(state)
    yield {"type": "node_status", "node": "intent_classifier", "data": state["node_logs"][-1]["message"]}

    if state["intent"] in {"local", "hybrid"}:
        state = retrieve_local(state)
        yield {"type": "node_status", "node": "retriever_local", "data": state["node_logs"][-1]["message"]}

    if state["intent"] in {"web", "hybrid"}:
        state = retrieve_web(state)
        yield {"type": "node_status", "node": "retriever_web", "data": state["node_logs"][-1]["message"]}

    state = rerank_documents(state)
    yield {"type": "node_status", "node": "reranker", "data": state["node_logs"][-1]["message"]}

    state = compress_context(state)
    yield {"type": "node_status", "node": "compressor", "data": state["node_logs"][-1]["message"]}

    state = generate_answer(state)
    for token in state["answer"]:
        yield {"type": "token_stream", "data": token}
    yield {
        "type": "final_answer",
        "content": state["answer"],
        "citations": state.get("citations", []),
        "facts": state.get("facts", []),
    }
