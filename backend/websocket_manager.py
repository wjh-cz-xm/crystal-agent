"""WebSocket 连接管理器"""

import json
import logging
from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    """管理所有活跃 WebSocket 连接"""

    def __init__(self):
        self.active_connections: set[WebSocket] = set()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.add(ws)
        logger.info(f"新连接, 当前连接数: {len(self.active_connections)}")

    def disconnect(self, ws: WebSocket):
        self.active_connections.discard(ws)
        logger.info(f"连接断开, 当前连接数: {len(self.active_connections)}")

    async def send(self, ws: WebSocket, message: dict):
        """向单个连接发送 JSON 消息"""
        try:
            await ws.send_text(json.dumps(message, ensure_ascii=False))
        except Exception:
            self.disconnect(ws)

    async def broadcast(self, message: dict):
        """向所有连接广播消息"""
        stale: list[WebSocket] = []
        for ws in self.active_connections:
            try:
                await ws.send_text(json.dumps(message, ensure_ascii=False))
            except Exception:
                stale.append(ws)
        for ws in stale:
            self.disconnect(ws)
