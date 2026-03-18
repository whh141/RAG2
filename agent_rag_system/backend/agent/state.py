from __future__ import annotations

from typing import Any, Literal, TypedDict


IntentLabel = Literal["local", "web", "hybrid"]


class RetrievedDocument(TypedDict):
    id: str
    source: str
    title: str
    content: str
    score: float
    metadata: dict[str, Any]


class Fact(TypedDict):
    id: int
    statement: str
    source: str


class AgentState(TypedDict, total=False):
    query: str
    intent: IntentLabel
    intent_reason: str
    retrieved_docs: list[RetrievedDocument]
    reranked_docs: list[RetrievedDocument]
    facts: list[Fact]
    answer: str
    citations: list[Fact]
    event_emitter: Any
