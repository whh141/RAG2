from __future__ import annotations

from tavily import TavilyClient

from config import settings
from agent.state import AgentState, RetrievedDocument


async def retrieve_web(state: AgentState) -> AgentState:
    client = TavilyClient(api_key=settings.tavily_api_key)
    response = client.search(
        state["query"],
        search_depth="advanced",
        max_results=5,
        include_answer=False,
        include_raw_content=True,
    )
    web_docs: list[RetrievedDocument] = []
    for index, item in enumerate(response.get("results", []), start=1):
        web_docs.append(
            {
                "id": f"web-{index}",
                "source": item.get("url", "web"),
                "title": item.get("title", "Web Result"),
                "content": item.get("raw_content") or item.get("content") or "",
                "score": 0.0,
                "metadata": {"url": item.get("url", "")},
            }
        )
    state["retrieved_docs"] = [*state.get("retrieved_docs", []), *web_docs]
    await state["event_emitter"].emit(
        "node_status",
        "retriever_web",
        {
            "summary": f"Tavily 搜索完成，命中 {len(web_docs)} 条网页结果。",
            "documents": [
                {
                    "title": document["title"],
                    "url": document["metadata"].get("url", ""),
                    "preview": document["content"][:180],
                }
                for document in web_docs
            ],
        },
    )
    return state
