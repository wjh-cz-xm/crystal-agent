"""晶体智能助手 — 全局配置"""

import os
from pathlib import Path

# 自动加载项目根目录 .env 文件
try:
    from dotenv import load_dotenv
    _env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(_env_path)
except ImportError:
    pass

# ========== 路径常量 ==========
PROJECT_ROOT = Path(__file__).parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
CIF_CACHE_DIR = PROJECT_ROOT / "cif_cache"
KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "knowledge_base"

# ========== 服务配置 ==========
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", "8000"))

# ========== API Keys ==========
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
MP_API_KEY = os.getenv("MP_API_KEY", "")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "")

# ========== LLM 配置 ==========
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-v4-flash"

# ========== 目录初始化 ==========
CIF_CACHE_DIR.mkdir(parents=True, exist_ok=True)
