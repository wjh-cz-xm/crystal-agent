"""DeepSeek Agent 循环 — 非流式 + thinking 模式 + 工具调用"""

from __future__ import annotations

import json
import logging
import re
from typing import AsyncGenerator

from openai import AsyncOpenAI

from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL, PROJECT_ROOT
from .tool_registry import tool_registry, KNOWN_STRUCTURES

logger = logging.getLogger(__name__)

# 工具调用最大轮次（防止无限循环）
MAX_TOOL_ROUNDS = 12

# 系统提示词路径
SYSTEM_PROMPT_PATH = PROJECT_ROOT / "system_prompt.md"


def _load_system_prompt() -> str:
    """加载系统提示词；若文件不存在则用内置简版"""
    if SYSTEM_PROMPT_PATH.exists():
        return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    logger.warning(f"系统提示词文件不存在: {SYSTEM_PROMPT_PATH}，使用内置简版")
    return (
        "你是一位晶体学与材料科学 AI 助手。"
        "用中文回答，支持 Markdown 和 LaTeX 格式。"
        "可以调用工具获取数据并将结构渲染到 3D 查看器。"
    )


def _extract_thinking_status(reasoning: str) -> str:
    """从思维链文本中提取简短状态摘要"""
    if not reasoning or not reasoning.strip():
        return "正在分析…"

    # 取最后 2-3 句作为状态
    sentences = re.split(r"[。．.!！?\n]", reasoning)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return "正在分析…"

    # 取最后 2 句，每句限 25 字
    last = sentences[-2:] if len(sentences) >= 2 else sentences[-1:]
    summary = "。".join(s[:25] for s in last)
    return summary[:60]


class CrystalAgent:
    """DeepSeek Agent — 对话 + 工具调用循环"""

    def __init__(self):
        self.client = None
        if DEEPSEEK_API_KEY:
            self.client = AsyncOpenAI(
                base_url=DEEPSEEK_BASE_URL,
                api_key=DEEPSEEK_API_KEY,
            )
        else:
            logger.warning("DEEPSEEK_API_KEY 未设置，LLM 功能不可用")
        self.system_prompt = _load_system_prompt()
        self._histories: dict[str, list[dict]] = {}

    # ====================================================================

    async def chat(
        self, user_message: str, conversation_id: str
    ) -> AsyncGenerator[dict, None]:
        """主对话循环，逐事件 yield"""

        if not self.client:
            yield {
                "type": "system_message",
                "text": "LLM 未配置: DEEPSEEK_API_KEY 环境变量缺失",
                "level": "error",
            }
            yield {
                "type": "chat_message",
                "role": "assistant",
                "content": (
                    "抱歉，DeepSeek API Key 未配置，LLM 对话功能暂不可用。\n\n"
                    "请设置环境变量 `DEEPSEEK_API_KEY` 后重启服务。"
                ),
            }
            return

        # 初始化或追加历史
        if conversation_id not in self._histories:
            self._histories[conversation_id] = [
                {"role": "system", "content": self.system_prompt}
            ]
        history = self._histories[conversation_id]

        # 添加用户消息
        history.append({"role": "user", "content": user_message})

        tool_rounds = 0

        while True:
            tool_rounds += 1
            if tool_rounds > MAX_TOOL_ROUNDS:
                yield {
                    "type": "system_message",
                    "text": "工具调用轮次超限，已强制终止",
                    "level": "warning",
                }
                break

            # ---- 调用 DeepSeek ----
            try:
                kwargs: dict = {
                    "model": DEEPSEEK_MODEL,
                    "messages": history,
                    "stream": False,
                    "extra_body": {"thinking": {"type": "enabled"}},
                }
                tools = tool_registry.get_tools_schema()
                if tools:
                    kwargs["tools"] = tools

                response = await self.client.chat.completions.create(**kwargs)
            except Exception as e:
                logger.error(f"DeepSeek API 调用失败: {e}")
                yield {
                    "type": "system_message",
                    "text": f"模型响应异常: {e}",
                    "level": "error",
                }
                break

            msg = response.choices[0].message

            # ---- 提取思维链状态 ----
            reasoning = getattr(msg, "reasoning_content", None)
            if not reasoning:
                reasoning = (getattr(msg, "model_extra", {}) or {}).get("reasoning_content")
            # 保存 reasoning_content 以便后续历史回传（DeepSeek thinking 模式要求）
            reasoning_content = reasoning or ""
            if reasoning:
                status_text = _extract_thinking_status(reasoning)
                yield {
                    "type": "status_update",
                    "status": "thinking",
                    "detail": status_text,
                }

            # ---- 工具调用 ----
            if msg.tool_calls:
                # 将 assistant 消息加入历史（含 reasoning_content，DeepSeek 要求）
                history_msg: dict = {
                    "role": "assistant",
                    "content": msg.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            },
                        }
                        for tc in msg.tool_calls
                    ],
                }
                if reasoning_content:
                    history_msg["reasoning_content"] = reasoning_content
                history.append(history_msg)

                for tc in msg.tool_calls:
                    tool_name = tc.function.name
                    try:
                        tool_args = json.loads(tc.function.arguments)
                    except json.JSONDecodeError:
                        tool_args = {}

                    yield {
                        "type": "status_update",
                        "status": "calling_tool",
                        "detail": f"正在调用 {tool_name}…",
                    }

                    result = tool_registry.execute(tool_name, tool_args)

                    # render_3d_structure：yield 渲染事件到前端
                    if tool_name == "render_3d_structure":
                        mp_id = tool_args.get("mp_id", "")
                        label = tool_args.get("label", "")
                        cif_data = tool_args.get("cif_data", "")
                        # Phase 4: 优先从 cif_library 获取
                        if not cif_data:
                            try:
                                from tools.cif_library import cif_library
                                cif_data = cif_library.get_cif(mp_id)
                                if cif_data and not label:
                                    label = mp_id
                            except ImportError:
                                pass
                        if not cif_data and mp_id in KNOWN_STRUCTURES:
                            cif_data = KNOWN_STRUCTURES[mp_id]["cif_data"]
                        if cif_data:
                            yield {
                                "type": "render_structure",
                                "cif_data": cif_data,
                                "mp_id": mp_id,
                                "label": label,
                            }

                    history.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": result,
                    })

                    yield {
                        "type": "status_update",
                        "status": "tool_done",
                        "detail": f"{tool_name} 完成",
                    }

                continue  # 回到 LLM 继续

            # ---- 最终文本回复 ----
            content = msg.content or ""
            history.append({"role": "assistant", "content": content})

            yield {
                "type": "chat_message",
                "role": "assistant",
                "content": content,
            }
            break

    # ====================================================================

    def clear_conversation(self, conversation_id: str):
        """清空对话历史"""
        self._histories.pop(conversation_id, None)
        logger.info(f"对话已清空: {conversation_id}")

    def has_conversation(self, conversation_id: str) -> bool:
        return conversation_id in self._histories


# ========== 全局单例 ==========
agent = CrystalAgent()
