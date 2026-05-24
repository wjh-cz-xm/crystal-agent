"""工具注册中心 — OpenAI 兼容 tools schema (Phase 4: 完整工具组)"""

import logging

logger = logging.getLogger(__name__)

KNOWN_STRUCTURES: dict[str, dict] = {}


class ToolRegistry:
    """工具注册与执行中心"""

    def __init__(self):
        self._tools: dict[str, dict] = {}

    def register(self, name: str, description: str, parameters: dict, handler):
        self._tools[name] = {
            "description": description,
            "parameters": parameters,
            "handler": handler,
        }
        logger.info(f"工具已注册: {name}")

    def get_tools_schema(self) -> list[dict]:
        if not self._tools:
            return []
        return [
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": info["description"],
                    "parameters": info["parameters"],
                },
            }
            for name, info in self._tools.items()
        ]

    def execute(self, name: str, args: dict) -> str:
        handler = self._tools[name]["handler"]
        try:
            return handler(args)
        except Exception as e:
            logger.error(f"工具执行失败 [{name}]: {e}")
            return f"工具执行出错: {e}"

    @property
    def tool_names(self) -> list[str]:
        return list(self._tools.keys())


tool_registry = ToolRegistry()


# ====================================================================
# render_3d_structure
# ====================================================================

def _render_handler(args: dict) -> str:
    mp_id = args.get("mp_id", "")
    label = args.get("label", "")
    cif_data = args.get("cif_data", "")

    if not cif_data:
        try:
            from tools.cif_library import cif_library
            cached = cif_library.get_cif(mp_id)
            if cached:
                cif_data = cached
                if not label:
                    label = mp_id
        except ImportError:
            pass

    if not cif_data and mp_id in KNOWN_STRUCTURES:
        entry = KNOWN_STRUCTURES[mp_id]
        cif_data = entry["cif_data"]
        if not label:
            label = entry.get("label", mp_id)

    if not cif_data:
        return (
            f"错误：未找到 mp_id={mp_id} 的 CIF 数据。"
            f"请先调用 mp_get_structure 从 Materials Project 获取结构数据。"
        )

    return f"已成功准备渲染 {label or mp_id} 的晶体结构"


def register_render_tool(known_structures: dict[str, dict] = None):
    if known_structures:
        KNOWN_STRUCTURES.update(known_structures)

    tool_registry.register(
        name="render_3d_structure",
        description=(
            "将晶体结构渲染到左侧 3D 查看器中。"
            "当用户请求查看或展示某种晶体结构时调用此工具。"
            "若 CIF 数据已在本地缓存，可直接调用；否则需先调用 mp_get_structure 获取。"
            "当前已知 mp_id: mp-149（Si/单晶硅）。"
        ),
        parameters={
            "type": "object",
            "properties": {
                "mp_id": {
                    "type": "string",
                    "description": "Materials Project 材料 ID，如 mp-149",
                },
                "label": {
                    "type": "string",
                    "description": "显示标签，如 'Si（单晶硅）'",
                },
                "cif_data": {
                    "type": "string",
                    "description": "CIF 数据。若已知缓存可省略",
                },
            },
            "required": ["mp_id", "label"],
        },
        handler=_render_handler,
    )


# ====================================================================
# Phase 4 工具注册
# ====================================================================

def register_phase4_tools():
    """注册全部工具：CIF库 / MP-API / 知识库 / 联网搜索"""

    # -- CIF 库 --
    from tools.cif_library import cif_library

    def _get_cif(args: dict) -> str:
        return cif_library.get_cif_summary(args.get("mp_id", ""))

    tool_registry.register(
        name="get_cif",
        description=(
            "从本地 CIF 缓存读取指定材料的晶体结构数据。"
            "若缓存无此材料，建议先调用 mp_get_structure 获取。"
            f"已缓存: {', '.join(cif_library.list_cached()) if cif_library.list_cached() else '无'}。"
        ),
        parameters={
            "type": "object",
            "properties": {
                "mp_id": {"type": "string", "description": "Materials Project 材料 ID"},
            },
            "required": ["mp_id"],
        },
        handler=_get_cif,
    )

    # -- MP-API --
    from tools.mp_api import (
        mp_search_materials, mp_get_structure, mp_get_summary,
        mp_get_bandstructure, mp_get_dos, mp_search_by_chemsys,
    )

    tool_registry.register(
        name="mp_search_materials",
        description=(
            "在 Materials Project 中搜索材料。按化学式、元素组成、带隙范围、"
            "稳定性等条件筛选。当用户询问'含锂的材料''带隙>2eV的半导体'时调用。"
        ),
        parameters={
            "type": "object",
            "properties": {
                "formula": {"type": "string", "description": "化学式，如 Si, LiFePO4"},
                "elements": {"type": "string", "description": "逗号分隔元素，如 Li,Fe,P,O"},
                "band_gap_min": {"type": "number", "description": "最小带隙 (eV)"},
                "band_gap_max": {"type": "number", "description": "最大带隙 (eV)"},
                "is_stable": {"type": "boolean", "description": "仅搜索稳定材料"},
                "limit": {"type": "integer", "description": "结果上限，默认 10"},
            },
            "required": [],
        },
        handler=lambda a: mp_search_materials(
            formula=a.get("formula"), elements=a.get("elements"),
            band_gap_min=a.get("band_gap_min"), band_gap_max=a.get("band_gap_max"),
            is_stable=a.get("is_stable"), limit=a.get("limit", 10),
        ),
    )

    tool_registry.register(
        name="mp_get_summary",
        description=(
            "获取指定 Materials Project 材料的综合属性摘要：带隙、形成能、密度、"
            "空间群、稳定性、磁性。当用户询问某材料物理化学性质时调用。"
        ),
        parameters={
            "type": "object",
            "properties": {
                "mp_id": {"type": "string", "description": "材料 ID，如 mp-149"},
            },
            "required": ["mp_id"],
        },
        handler=lambda a: mp_get_summary(a.get("mp_id", "")),
    )

    tool_registry.register(
        name="mp_get_structure",
        description=(
            "从 Materials Project 获取材料的 CIF 晶体结构并缓存到本地。"
            "调用后通常需接着调用 render_3d_structure 渲染。"
        ),
        parameters={
            "type": "object",
            "properties": {
                "mp_id": {"type": "string", "description": "材料 ID，如 mp-149"},
            },
            "required": ["mp_id"],
        },
        handler=lambda a: mp_get_structure(a.get("mp_id", "")),
    )

    tool_registry.register(
        name="mp_get_bandstructure",
        description=(
            "获取材料的能带结构：带隙值、直接/间接带隙类型、VBM/CBM 能量和位置。"
            "当用户询问能带结构或带隙特性时调用。"
        ),
        parameters={
            "type": "object",
            "properties": {
                "mp_id": {"type": "string", "description": "材料 ID"},
            },
            "required": ["mp_id"],
        },
        handler=lambda a: mp_get_bandstructure(a.get("mp_id", "")),
    )

    tool_registry.register(
        name="mp_get_dos",
        description=(
            "获取材料的态密度 (DOS) 数据：费米能级处 DOS 值、带隙、能量范围。"
            "当用户询问电子态密度时调用。"
        ),
        parameters={
            "type": "object",
            "properties": {
                "mp_id": {"type": "string", "description": "材料 ID"},
            },
            "required": ["mp_id"],
        },
        handler=lambda a: mp_get_dos(a.get("mp_id", "")),
    )

    tool_registry.register(
        name="mp_search_by_chemsys",
        description=(
            "按化学体系搜索材料，如 Li-Fe-O 返回该三元体系所有材料。"
            "当用户问'X-Y-Z 体系有哪些化合物'时调用。"
        ),
        parameters={
            "type": "object",
            "properties": {
                "chemsys": {"type": "string", "description": "化学体系，如 Li-Fe-O"},
                "limit": {"type": "integer", "description": "结果上限，默认 10"},
            },
            "required": ["chemsys"],
        },
        handler=lambda a: mp_search_by_chemsys(chemsys=a.get("chemsys", ""), limit=a.get("limit", 10)),
    )

    # -- 知识库 --
    from tools.knowledge_search import retrieve_knowledge_base

    tool_registry.register(
        name="retrieve_knowledge_base",
        description=(
            "搜索本地晶体学知识库。涵盖晶格、对称性、衍射、缺陷、能带理论、"
            "常见晶体结构等主题。当用户询问理论概念时调用，如'布拉格定律''空间群'。"
            "注意：不包含具体材料实验数据。"
        ),
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "搜索关键词"},
            },
            "required": ["query"],
        },
        handler=lambda a: retrieve_knowledge_base(a.get("query", "")),
    )

    # -- 联网搜索 --
    from tools.web_search import web_search

    tool_registry.register(
        name="web_search",
        description=(
            "联网搜索最新研究进展或超出本地知识库和 MP-API 范围的信息。"
            "如'钙钛矿太阳能电池最新进展''2024年MOF研究热点'。"
        ),
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "搜索关键词"},
            },
            "required": ["query"],
        },
        handler=lambda a: web_search(a.get("query", "")),
    )

    logger.info(f"Phase 4 工具注册完成，共 {len(tool_registry._tools)} 个: {tool_registry.tool_names}")
