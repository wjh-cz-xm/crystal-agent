"""晶体智能助手 — FastAPI 入口 (Phase 3: LLM Agent)"""

import json
import logging
import sys
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

# 确保 backend/ 在 sys.path 中
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

from config import FRONTEND_DIR, HOST, PORT, DEEPSEEK_API_KEY, MP_API_KEY, SERPAPI_API_KEY
from websocket_manager import ConnectionManager
from crystal_service import (
    TEST_CIF_SI,
    extract_metadata,
    switch_cell,
    build_supercell,
    add_boundary_atoms,
    get_lattice_vectors,
)
from llm.agent import agent
from llm.tool_registry import register_render_tool, register_phase4_tools, KNOWN_STRUCTURES
from tools.cif_library import cif_library

# ========== 日志 ==========
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ========== 全局 ==========
manager = ConnectionManager()

# 注册 Phase 3 已知结构 → 工具可用
KNOWN_STRUCTURES["mp-149"] = {
    "cif_data": TEST_CIF_SI,
    "label": "Si（单晶硅）",
}
register_render_tool(KNOWN_STRUCTURES)
register_phase4_tools()


# ========== 启动/关闭 ==========
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=" * 50)
    logger.info("  晶体智能助手服务启动 (Phase 5 — 全功能)")
    logger.info(f"  访问 http://{HOST}:{PORT}")
    logger.info("=" * 50)

    if DEEPSEEK_API_KEY:
        logger.info("✓ DEEPSEEK_API_KEY 已配置")
    else:
        logger.warning("⚠ DEEPSEEK_API_KEY 未设置，LLM 功能不可用")

    if MP_API_KEY:
        logger.info("✓ MP_API_KEY 已配置")
    else:
        logger.warning("⚠ MP_API_KEY 未设置，MP-API 工具不可用")

    if SERPAPI_API_KEY:
        logger.info("✓ SERPAPI_API_KEY 已配置")
    else:
        logger.warning("⚠ SERPAPI_API_KEY 未设置，联网搜索不可用")

    yield
    logger.info("服务关闭")


# ========== App ==========
app = FastAPI(title="晶体智能助手", lifespan=lifespan)


# ========== WebSocket ==========
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)

    # 当前结构状态（per-connection）
    base_cif: str = TEST_CIF_SI
    current_cif: str = TEST_CIF_SI
    current_mp_id: str = "mp-149"
    current_label: str = "Si（单晶硅）"
    # 显示选项
    disp_periodic: bool = True
    disp_outside: bool = False
    # 对话 ID
    conv_id: str = str(uuid.uuid4())[:8]

    async def _send_structure(ws, cif, mp_id, label):
        """统一发送结构：应用显示选项 → 发 render_structure"""
        data, fmt = add_boundary_atoms(cif, disp_periodic, disp_outside)
        meta = extract_metadata(cif)
        vectors = get_lattice_vectors(cif)
        await manager.send(ws, {
            "type": "render_structure",
            "cif_data": data,
            "format": fmt,
            "mp_id": mp_id,
            "label": label,
            "elements": meta["elements"],
            "lattice_vectors": vectors,
        })

    # 连接后自动渲染测试结构
    try:
        await _send_structure(ws, current_cif, current_mp_id, current_label)
    except Exception as e:
        logger.error(f"初始结构加载失败: {e}")

    try:
        while True:
            data = await ws.receive_text()
            msg = json.loads(data)
            msg_type = msg.get("type", "")

            # ---- 聊天消息 (LLM Agent) ----
            if msg_type == "user_message":
                text = msg.get("text", "").strip()
                if not text:
                    continue
                logger.info(f"[{conv_id}] 用户: {text[:80]}")

                # 回显用户消息
                await manager.send(ws, {
                    "type": "chat_message",
                    "role": "user",
                    "content": text,
                })

                # 调用 LLM Agent
                try:
                    async for event in agent.chat(text, conv_id):
                        ev_type = event.get("type", "")

                        if ev_type == "render_structure":
                            # 补充元素元数据和晶格矢量
                            cif_data = event.get("cif_data", "")
                            mp_id = event.get("mp_id", "")
                            label = event.get("label", "")
                            if cif_data:
                                try:
                                    meta = extract_metadata(cif_data)
                                    vectors = get_lattice_vectors(cif_data)
                                    event["elements"] = meta["elements"]
                                    event["lattice_vectors"] = vectors
                                    # 更新当前结构状态
                                    current_cif = cif_data
                                    current_mp_id = mp_id
                                    current_label = label
                                except Exception as e:
                                    logger.error(f"结构解析失败: {e}")

                        await manager.send(ws, event)

                except Exception as e:
                    logger.error(f"Agent 调用失败: {e}")
                    await manager.send(ws, {
                        "type": "system_message",
                        "text": f"模型响应异常: {e}",
                        "level": "error",
                    })
                    await manager.send(ws, {
                        "type": "chat_message",
                        "role": "assistant",
                        "content": f"抱歉，模型响应出现异常：{e}\n\n请稍后重试。",
                    })

            # ---- 新对话 ----
            elif msg_type == "new_conversation":
                old_conv_id = conv_id
                conv_id = str(uuid.uuid4())[:8]
                agent.clear_conversation(old_conv_id)
                logger.info(f"[{conv_id}] 新对话 (旧: {old_conv_id})")
                await manager.send(ws, {
                    "type": "system_message",
                    "text": "已开启新对话，上下文已清空",
                    "level": "info",
                })

            # ---- 晶体查看器操作 ----
            elif msg_type == "viewer_action":
                action = msg.get("action", "")

                if action == "switch_cell":
                    cell_type = msg.get("cell_type", "conventional")
                    try:
                        new_cif = switch_cell(current_cif, cell_type)
                        base_cif = new_cif
                        current_cif = new_cif
                        await _send_structure(ws, current_cif, current_mp_id, current_label)
                    except Exception as e:
                        await manager.send(ws, {
                            "type": "system_message",
                            "text": f"切换晶胞失败: {e}",
                            "level": "error",
                        })

                elif action == "build_supercell":
                    try:
                        dims = msg.get("size", [1, 1, 1])
                        a, b, c = dims[0], dims[1], dims[2]
                        if a == 1 and b == 1 and c == 1:
                            current_cif = base_cif
                        else:
                            current_cif = build_supercell(base_cif, a, b, c)
                        await _send_structure(ws, current_cif, current_mp_id, current_label)
                    except ValueError as e:
                        await manager.send(ws, {
                            "type": "system_message",
                            "text": str(e),
                            "level": "warning",
                        })
                    except Exception as e:
                        await manager.send(ws, {
                            "type": "system_message",
                            "text": f"构建超胞失败: {e}",
                            "level": "error",
                        })

                elif action == "toggle_display":
                    disp_periodic = msg.get("periodic", True)
                    disp_outside = msg.get("outside", True)
                    await _send_structure(ws, current_cif, current_mp_id, current_label)

                elif action == "render":
                    # 直接渲染（来自 LLM 工具调用）
                    cif_data = msg.get("cif_data", "")
                    mp_id = msg.get("mp_id", "")
                    label = msg.get("label", "")
                    if cif_data:
                        current_cif = cif_data
                        current_mp_id = mp_id
                        current_label = label
                        meta = extract_metadata(cif_data)
                        await manager.send(ws, {
                            "type": "render_structure",
                            "cif_data": cif_data,
                            "mp_id": mp_id,
                            "label": label,
                            "elements": meta["elements"],
                        })
                    else:
                        await manager.send(ws, {
                            "type": "system_message",
                            "text": "渲染失败: cif_data 为空",
                            "level": "error",
                        })

                else:
                    await manager.send(ws, {
                        "type": "system_message",
                        "text": f"未知查看器操作: {action}",
                        "level": "warning",
                    })

            else:
                await manager.send(ws, {
                    "type": "system_message",
                    "text": f"未知消息类型: {msg_type}",
                    "level": "warning",
                })

    except WebSocketDisconnect:
        manager.disconnect(ws)
    except Exception as e:
        logger.error(f"WebSocket 异常: {e}")
        manager.disconnect(ws)


# ========== 静态文件（须在最后注册） ==========
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="static")

# ========== 启动入口 ==========
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")
