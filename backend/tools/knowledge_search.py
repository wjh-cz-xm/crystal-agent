"""知识库检索工具 — 封装现有 KnowledgeBase 搜索"""

import logging
import sys
from pathlib import Path

# 将 knowledge_base/ 加入 sys.path 以便导入 kb_search
_KB_DIR = Path(__file__).parent.parent.parent / "knowledge_base"
if str(_KB_DIR) not in sys.path:
    sys.path.insert(0, str(_KB_DIR))

from kb_search import KnowledgeBase

logger = logging.getLogger(__name__)

# 全局单例
kb = KnowledgeBase()


def retrieve_knowledge_base(query: str) -> str:
    """搜索本地知识库并返回格式化结果，供 LLM 工具调用"""
    if not query or not query.strip():
        return "错误：搜索词不能为空"

    try:
        results = kb.search(query.strip(), top_k=5)
    except Exception as e:
        logger.error(f"知识库搜索失败: {e}")
        return f"知识库搜索出错: {e}"

    if not results:
        return f"未在知识库中找到与「{query}」相关的内容。建议尝试其他关键词。"

    lines = [f"共找到 {len(results)} 条与「{query}」相关的结果：\n"]
    for i, entry in enumerate(results, 1):
        formatted = kb.format_for_llm(entry, include_related=(len(results) <= 3))
        lines.append(f"### 结果 {i}（匹配度: {entry.get('score', 0)}）")
        lines.append(formatted)
        lines.append("")

    return "\n".join(lines)
