from __future__ import annotations

from agent.state import AgentState


class TavilyRetriever:
    def search(self, query: str) -> list[dict]:
        return [
            {
                "id": "web-1",
                "source": "web",
                "title": "Tavily placeholder result",
                "content": f"与问题“{query}”相关的外部搜索结果占位内容。",
                "score": 0.72,
            }
        ]


def retrieve_web(state: AgentState) -> AgentState:
    docs = TavilyRetriever().search(state["query"])
    state.setdefault("retrieved_docs", []).extend(docs)
    state.setdefault("node_logs", []).append(
        {"node": "retriever_web", "message": f"外部搜索完成，命中 {len(docs)} 条结果。"}
    )
    return state
