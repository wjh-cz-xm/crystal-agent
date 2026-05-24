"""联网搜索工具 — SerpAPI 封装"""

import logging

import requests

from config import SERPAPI_API_KEY

logger = logging.getLogger(__name__)

SERPAPI_URL = "https://serpapi.com/search"
TIMEOUT = 15


def web_search(query: str) -> str:
    """通过 SerpAPI 联网搜索，返回前 5 条结果的摘要"""
    if not SERPAPI_API_KEY:
        return "错误：SERPAPI_API_KEY 未配置，联网搜索不可用。请在 .env 中设置 SERPAPI_API_KEY。"

    if not query or not query.strip():
        return "错误：搜索词不能为空"

    try:
        resp = requests.get(
            SERPAPI_URL,
            params={"q": query.strip(), "api_key": SERPAPI_API_KEY, "hl": "zh-CN"},
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
    except requests.Timeout:
        return "错误：联网搜索请求超时，请稍后重试。"
    except requests.RequestException as e:
        logger.error(f"SerpAPI 请求失败: {e}")
        return f"联网搜索请求失败: {e}"

    # 检查 SerpAPI 返回的错误
    if "error" in data:
        msg = data["error"]
        logger.error(f"SerpAPI 返回错误: {msg}")
        return f"联网搜索出错: {msg}"

    organic = data.get("organic_results", [])
    if not organic:
        return f"未找到与「{query}」相关的搜索结果。"

    lines = [f"「{query}」的搜索结果（前 {min(5, len(organic))} 条）：\n"]
    for i, r in enumerate(organic[:5], 1):
        title = r.get("title", "无标题")
        snippet = r.get("snippet", "无摘要")
        link = r.get("link", "")
        lines.append(f"{i}. **{title}**")
        lines.append(f"   {snippet}")
        if link:
            lines.append(f"   来源: {link}")
        lines.append("")

    return "\n".join(lines)
