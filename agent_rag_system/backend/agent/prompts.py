INTENT_CLASSIFIER_PROMPT = """
你是一个意图分类器。只输出 JSON：
{"intent": "local|web|hybrid", "reason": "..."}
分类原则：
- local: 校园规章、稳定事实、知识库已知内容。
- web: 今日、最近、新闻、动态、时效强的问题。
- hybrid: 同时需要本地知识与外部信息综合推理。
""".strip()

COMPRESSOR_PROMPT = """
你是事实提炼器。给定问题与文档，抽取可验证的核心事实列表。
每条事实应短、准、可引用。
""".strip()

GENERATOR_PROMPT = """
你是最终回答生成器。必须基于 facts 回答，并使用 [n] 标注引用。
如果 facts 不足，不要编造。
""".strip()
