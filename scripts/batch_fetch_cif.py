"""Phase 5: 批量预填充 15 种常见晶体 CIF"""

import io, os, sys
from pathlib import Path

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

# Load .env
env_path = PROJECT_ROOT / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k, v)

from tools.mp_api import mp_get_structure
from tools.cif_library import cif_library

# 15 种常见晶体（涵盖了知识库中的 material_data 和常见结构原型）
CRYSTALS = [
    ("mp-149", "Si（金刚石型）"),
    ("mp-22862", "NaCl（岩盐型）"),
    ("mp-1179", "CsCl（氯化铯型）"),
    ("mp-66", "C（金刚石）"),
    ("mp-804", "GaAs（闪锌矿型）"),
    ("mp-2133", "ZnO（纤锌矿型）"),
    ("mp-5229", "BaTiO₃（钙钛矿型）"),
    ("mp-13", "Fe（BCC 金属）"),
    ("mp-33", "Al（FCC 金属）"),
    ("mp-79", "Cu（FCC 金属）"),
    ("mp-105", "W（BCC 金属）"),
    ("mp-10805", "Mg（HCP 金属）"),
    ("mp-22905", "LiFePO₄（橄榄石型）"),
    ("mp-778", "SiO₂（α-石英）"),
    ("mp-158", "As（黑砷）"),
]

def main():
    print(f"CIF 缓存目录: {cif_library.cache_dir}")
    print(f"当前缓存: {cif_library.list_cached()}")
    print(f"待获取: {len(CRYSTALS)} 种\n")

    success = 0
    fail = 0

    for mp_id, name in CRYSTALS:
        if cif_library.has(mp_id):
            print(f"✓ {mp_id} {name} — 已缓存，跳过")
            success += 1
            continue

        print(f"↓ {mp_id} {name} ... ", end="", flush=True)
        result = mp_get_structure(mp_id)
        if "成功获取" in result:
            print("OK")
            success += 1
        else:
            print(f"失败: {result}")
            fail += 1

    print(f"\n{'='*50}")
    print(f"完成: {success} 成功, {fail} 失败")
    print(f"缓存文件: {cif_library.list_cached()}")


if __name__ == "__main__":
    main()
