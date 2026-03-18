from __future__ import annotations

import json
from typing import Any

from zhipuai import ZhipuAI

from config import settings


_client = ZhipuAI(api_key=settings.zhipu_api_key, base_url=settings.zhipu_base_url)


def chat_json(system_prompt: str, user_prompt: str) -> Any:
    response = _client.chat.completions.create(
        model=settings.glm_chat_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content
    return json.loads(content)


def chat_text(system_prompt: str, user_prompt: str) -> str:
    response = _client.chat.completions.create(
        model=settings.glm_chat_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content
