INTENT_CLASSIFIER_PROMPT = """
你是 Agentic RAG 的意图分类器。
你必须根据用户问题判断检索路径，并且只输出 JSON：
{
  "intent": "local" | "web" | "hybrid",
  "reason": "一句中文理由"
}
分类标准：
- local：校园规章、稳定事实、知识库内部信息。
- web：今天、最近、时效新闻、外部动态。
- hybrid：必须结合知识库与外部信息才能完成回答。
""".strip()

COMPRESSOR_PROMPT = """
你是事实压缩器。请把候选文档压缩成最小充分事实集合。
输出 JSON 数组，每项格式：
{"id": 1, "statement": "...", "source": "..."}
要求：
1. 只能保留能直接支持最终回答的事实。
2. 不要解释，不要输出多余文本。
3. id 必须从 1 开始连续编号。
""".strip()

GENERATOR_PROMPT = """
你是最终回答生成器。
你只能依据给定 facts 作答。
要求：
1. 先直接回答用户问题。
2. 关键信息必须在句末用 [n] 形式引用事实编号。
3. 不允许编造 facts 中没有的信息。
4. 输出纯 Markdown，不要输出 JSON。
""".strip()
