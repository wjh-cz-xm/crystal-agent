"""CIF 缓存管理 — 本地 CIF 文件索引与读写"""

import logging
from pathlib import Path

from config import CIF_CACHE_DIR

logger = logging.getLogger(__name__)

MAX_CIF_CHARS = 5000


class CifLibrary:
    """管理 cif_cache/ 目录中的 CIF 文件"""

    def __init__(self, cache_dir: Path = CIF_CACHE_DIR):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._index: dict[str, Path] = {}
        self._rescan()

    def _rescan(self):
        """重新扫描缓存目录"""
        self._index.clear()
        for fp in self.cache_dir.glob("*.cif"):
            mp_id = fp.stem  # e.g. mp-149
            self._index[mp_id] = fp
        logger.info(f"CIF 库已扫描: {len(self._index)} 个文件")

    def get_cif(self, mp_id: str) -> str | None:
        """读取 CIF 文本，不存在则返回 None"""
        fp = self._index.get(mp_id)
        if not fp or not fp.exists():
            return None
        try:
            return fp.read_text(encoding="utf-8")
        except Exception as e:
            logger.error(f"读取 CIF 失败 [{mp_id}]: {e}")
            return None

    def save_cif(self, mp_id: str, cif_data: str):
        """写入 CIF 到缓存并更新索引"""
        fp = self.cache_dir / f"{mp_id}.cif"
        fp.write_text(cif_data, encoding="utf-8")
        self._index[mp_id] = fp
        logger.info(f"CIF 已缓存: {mp_id}")

    def list_cached(self) -> list[str]:
        """列出已缓存的 mp_id"""
        return sorted(self._index.keys())

    def has(self, mp_id: str) -> bool:
        return mp_id in self._index and self._index[mp_id].exists()

    def get_cif_summary(self, mp_id: str) -> str:
        """返回截断后的 CIF 文本，供 LLM 工具调用"""
        cif = self.get_cif(mp_id)
        if not cif:
            return f"错误：CIF 缓存中未找到 {mp_id}"
        if len(cif) > MAX_CIF_CHARS:
            return cif[:MAX_CIF_CHARS] + f"\n\n… (CIF 文本已截断，共 {len(cif)} 字符)"
        return cif


# ========== 全局单例 ==========
cif_library = CifLibrary()
