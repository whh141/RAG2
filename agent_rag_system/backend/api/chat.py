from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from agent.graph import run_agent_stream

router = APIRouter()


@router.websocket("/ws/chat")
async def chat_socket(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            payload = await websocket.receive_json()
            query = payload["query"].strip()
            async for event in run_agent_stream(query):
                await websocket.send_json(event)
    except WebSocketDisconnect:
        return
