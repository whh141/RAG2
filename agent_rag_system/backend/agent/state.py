from __future__ import annotations

from typing import Any, Literal, TypedDict


IntentLabel = Literal["local", "web", "hybrid"]


class RetrievedDocument(TypedDict):
    id: str
    source: str
    title: str
    content: str
    score: float


class Fact(TypedDict):
    id: int
    statement: str
    source: str


class AgentState(TypedDict, total=False):
    query: str
    intent: IntentLabel
    node_logs: list[dict[str, Any]]
    retrieved_docs: list[RetrievedDocument]
    reranked_docs: list[RetrievedDocument]
    facts: list[Fact]
    answer: str
    citations: list[Fact]
