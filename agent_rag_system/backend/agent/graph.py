from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator

from langgraph.graph import END, StateGraph

from agent.nodes.compressor import compress_context
from agent.nodes.generator import generate_answer
from agent.nodes.intent_classifier import classify_intent
from agent.nodes.reranker import rerank_documents
from agent.nodes.retriever_local import retrieve_local
from agent.nodes.retriever_web import retrieve_web
from agent.nodes.router import route_after_intent, route_after_local
from agent.state import AgentState


class EventEmitter:
    def __init__(self) -> None:
        self.queue: asyncio.Queue[dict | None] = asyncio.Queue()

    async def emit(self, event_type: str, node: str, data: str) -> None:
        await self.queue.put({"type": event_type, "node": node, "data": data})

    async def finish(self) -> None:
        await self.queue.put(None)


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("intent_classifier", classify_intent)
    graph.add_node("retriever_local", retrieve_local)
    graph.add_node("retriever_web", retrieve_web)
    graph.add_node("reranker", rerank_documents)
    graph.add_node("compressor", compress_context)
    graph.add_node("generator", generate_answer)

    graph.set_entry_point("intent_classifier")
    graph.add_conditional_edges("intent_classifier", route_after_intent)
    graph.add_conditional_edges("retriever_local", route_after_local)
    graph.add_edge("retriever_web", "reranker")
    graph.add_edge("reranker", "compressor")
    graph.add_edge("compressor", "generator")
    graph.add_edge("generator", END)
    return graph.compile()


async def run_agent_stream(query: str) -> AsyncGenerator[dict, None]:
    emitter = EventEmitter()
    graph = build_graph()
    state: AgentState = {"query": query, "retrieved_docs": [], "event_emitter": emitter}

    async def runner() -> None:
        final_state = await graph.ainvoke(state)
        for token in final_state["answer"]:
            await emitter.queue.put({"type": "token_stream", "data": token})
        await emitter.queue.put(
            {
                "type": "final_answer",
                "content": final_state["answer"],
                "citations": final_state.get("citations", []),
                "facts": final_state.get("facts", []),
            }
        )
        await emitter.finish()

    task = asyncio.create_task(runner())
    while True:
        event = await emitter.queue.get()
        if event is None:
            break
        yield event
    await task
