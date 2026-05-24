"""MP-API 工具组 — Materials Project 数据查询与结构获取"""

import json
import logging

from config import MP_API_KEY

logger = logging.getLogger(__name__)

_mpr = None  # lazy init

RESULT_LIMIT = 10
SUMMARY_FIELDS = [
    "material_id", "formula_pretty", "band_gap", "energy_above_hull",
    "formation_energy_per_atom", "density", "volume", "nelements",
    "nsites", "spacegroup_number", "spacegroup_symbol",
    "is_stable", "is_metal", "is_magnetic",
    "crystal_system", "chemsys",
]


def _get_mpr():
    """延迟初始化 MPRester"""
    global _mpr
    if _mpr is None:
        if not MP_API_KEY:
            raise RuntimeError("MP_API_KEY 未配置，Materials Project API 不可用")
        from mp_api.client import MPRester
        _mpr = MPRester(api_key=MP_API_KEY)
    return _mpr


def _doc_to_dict(doc) -> dict:
    """将 SummaryDoc 转为简单 dict，仅保留关键字段"""
    d = {}
    for f in SUMMARY_FIELDS:
        val = getattr(doc, f, None)
        if val is not None:
            if hasattr(val, "value"):  # Enum
                val = val.value
            d[f] = val
    return d


# ====================================================================
# 工具函数
# ====================================================================

def mp_search_materials(
    formula: str = None,
    elements: str = None,
    band_gap_min: float = None,
    band_gap_max: float = None,
    is_stable: bool = None,
    limit: int = RESULT_LIMIT,
) -> str:
    """按条件搜索 Materials Project 材料数据库"""
    try:
        mpr = _get_mpr()
    except RuntimeError as e:
        return f"错误：{e}"

    if not formula and not elements:
        return "错误：请至少提供 formula 或 elements 参数进行搜索"

    try:
        kwargs = {}
        if formula:
            kwargs["formula"] = formula.strip()
        if elements:
            el_list = [e.strip() for e in elements.split(",")]
            kwargs["elements"] = el_list
        if band_gap_min is not None or band_gap_max is not None:
            kwargs["band_gap"] = (band_gap_min or 0, band_gap_max or 100)
        if is_stable is not None:
            kwargs["is_stable"] = is_stable

        results = mpr.materials.summary.search(**kwargs)
        if not results:
            return f"未找到匹配的材料（formula={formula}, elements={elements}）"

        total = len(results)
        results = results[:limit]

        lines = [f"搜索到 {total} 个材料，显示前 {len(results)} 个：\n"]
        for r in results:
            d = _doc_to_dict(r)
            lines.append(
                f"- **{d.get('material_id', '?')}**: {d.get('formula_pretty', '?')}"
            )
            if d.get("band_gap") is not None:
                lines.append(f"  带隙: {d['band_gap']:.3f} eV")
            if d.get("energy_above_hull") is not None:
                lines.append(f"  Energy above Hull: {d['energy_above_hull']:.4f} eV/atom")
            if d.get("is_stable") is not None:
                lines.append(f"  稳定: {'是' if d['is_stable'] else '否'}")
            if d.get("spacegroup_symbol"):
                lines.append(f"  空间群: {d['spacegroup_symbol']} (#{d.get('spacegroup_number', '?')})")
            lines.append("")

        return "\n".join(lines)

    except Exception as e:
        logger.error(f"mp_search_materials 失败: {e}")
        return f"Materials Project 搜索失败: {e}"


def mp_get_summary(mp_id: str) -> str:
    """获取指定材料的综合属性摘要"""
    if not mp_id or not mp_id.strip():
        return "错误：请提供 mp_id 参数"

    mp_id = mp_id.strip()
    try:
        mpr = _get_mpr()
    except RuntimeError as e:
        return f"错误：{e}"

    try:
        results = mpr.materials.summary.search(material_ids=mp_id)
        if not results:
            return f"未找到材料 {mp_id}"

        doc = results[0]
        d = _doc_to_dict(doc)

        # 补充更多字段
        extra_fields = [
            "energy_per_atom", "density_atomic", "total_magnetization",
            "e_ionic", "e_total", "weighted_surface_energy",
            "universal_anisotropy", "shape_factor",
            "num_unique_magnetic_sites", "possible_species",
        ]
        for f in extra_fields:
            val = getattr(doc, f, None)
            if val is not None:
                d[f] = val

        lines = [f"## {d.get('formula_pretty', mp_id)} ({mp_id}) 综合属性\n"]
        for key, val in d.items():
            if key == "material_id":
                continue
            label = {
                "formula_pretty": "化学式",
                "band_gap": "带隙 (eV)",
                "energy_above_hull": "Energy above Hull (eV/atom)",
                "formation_energy_per_atom": "形成能 (eV/atom)",
                "energy_per_atom": "总能量 (eV/atom)",
                "density": "密度 (g/cm³)",
                "density_atomic": "原子密度",
                "volume": "体积 (Å³)",
                "nelements": "元素种类数",
                "nsites": "原子位数",
                "spacegroup_number": "空间群编号",
                "spacegroup_symbol": "空间群符号",
                "crystal_system": "晶系",
                "chemsys": "化学体系",
                "is_stable": "热力学稳定",
                "is_metal": "金属",
                "is_magnetic": "磁性",
                "total_magnetization": "总磁矩",
                "e_ionic": "离子贡献能",
                "e_total": "总能",
                "weighted_surface_energy": "加权表面能",
                "universal_anisotropy": "通用各向异性",
                "shape_factor": "形状因子",
                "num_unique_magnetic_sites": "独立磁性位点数",
                "possible_species": "可能氧化态",
            }.get(key, key)
            if isinstance(val, float):
                lines.append(f"- **{label}**: {val:.4f}")
            elif isinstance(val, bool):
                lines.append(f"- **{label}**: {'是' if val else '否'}")
            elif isinstance(val, list):
                lines.append(f"- **{label}**: {', '.join(str(v) for v in val)}")
            else:
                lines.append(f"- **{label}**: {val}")

        # 分解产物
        decomposes = getattr(doc, "decomposes_to", None)
        if decomposes:
            lines.append(f"- **可能分解为**: {decomposes}")

        return "\n".join(lines)

    except Exception as e:
        logger.error(f"mp_get_summary 失败 [{mp_id}]: {e}")
        return f"获取 {mp_id} 摘要失败: {e}"


def mp_get_structure(mp_id: str) -> str:
    """获取材料的 CIF 晶体结构，并自动缓存到 cif_cache"""
    if not mp_id or not mp_id.strip():
        return "错误：请提供 mp_id 参数"

    mp_id = mp_id.strip()
    try:
        mpr = _get_mpr()
    except RuntimeError as e:
        return f"错误：{e}"

    try:
        structure = mpr.get_structure_by_material_id(mp_id)
        if structure is None:
            return f"错误：{mp_id} 的结构数据不存在或无法获取。请尝试搜索其他材料。"

        cif_data = structure.to(fmt="cif")

        # 写入本地缓存（走 cif_library 保证索引一致）
        from tools.cif_library import cif_library
        cif_library.save_cif(mp_id, cif_data)

        formula = structure.composition.reduced_formula
        logger.info(f"已获取并缓存 {mp_id} ({formula})")

        return f"成功获取 {mp_id}（{formula}）的晶体结构，CIF 已缓存。可直接调用 render_3d_structure 展示。"
    except Exception as e:
        logger.error(f"mp_get_structure 失败 [{mp_id}]: {e}")
        return f"获取 {mp_id} 结构失败: {e}"


def mp_get_bandstructure(mp_id: str) -> str:
    """获取材料的能带结构数据摘要"""
    if not mp_id or not mp_id.strip():
        return "错误：请提供 mp_id 参数"

    mp_id = mp_id.strip()
    try:
        mpr = _get_mpr()
    except RuntimeError as e:
        return f"错误：{e}"

    try:
        bs = mpr.get_bandstructure_by_material_id(mp_id)
        if bs is None:
            # 通过 summary 查带隙
            results = mpr.materials.summary.search(material_ids=mp_id)
            if results:
                d = results[0]
                gap = d.band_gap
                is_direct = d.is_gap_direct
                vbm = d.vbm
                cbm = d.cbm
                efermi = d.efermi
                lines = [
                    f"## {d.formula_pretty} ({mp_id}) 能带信息（来自摘要数据）",
                    f"- **带隙**: {gap:.4f} eV（{'直接' if is_direct else '间接'}带隙）",
                ]
                if vbm is not None:
                    lines.append(f"- **VBM 能量**: {vbm:.4f} eV")
                if cbm is not None:
                    lines.append(f"- **CBM 能量**: {cbm:.4f} eV")
                if efermi is not None:
                    lines.append(f"- **费米能级**: {efermi:.4f} eV")
                return "\n".join(lines)
            return f"未找到 {mp_id} 的能带结构数据"

        # bs is a BandStructure object
        gap = bs.get_band_gap()
        gap_info = f"{gap['energy']:.4f} eV（{'直接' if gap['direct'] else '间接'}带隙）"
        vbm = bs.get_vbm()
        cbm = bs.get_cbm()

        lines = [
            f"## {mp_id} 能带结构",
            f"- **带隙**: {gap_info}",
            f"- **VBM**: {vbm['energy']:.4f} eV @ k=[{float(vbm['kpoint'].frac_coords[0]):.4f}, {float(vbm['kpoint'].frac_coords[1]):.4f}, {float(vbm['kpoint'].frac_coords[2]):.4f}]",
            f"- **CBM**: {cbm['energy']:.4f} eV @ k=[{float(cbm['kpoint'].frac_coords[0]):.4f}, {float(cbm['kpoint'].frac_coords[1]):.4f}, {float(cbm['kpoint'].frac_coords[2]):.4f}]",
            f"- **能带数**: {bs.nb_bands}",
            f"- **k 点路径**: {len(bs.kpoints)} 个点",
        ]
        return "\n".join(lines)

    except Exception as e:
        logger.error(f"mp_get_bandstructure 失败 [{mp_id}]: {e}")
        return f"获取 {mp_id} 能带结构失败: {e}"


def mp_get_dos(mp_id: str) -> str:
    """获取材料的态密度数据摘要"""
    if not mp_id or not mp_id.strip():
        return "错误：请提供 mp_id 参数"

    mp_id = mp_id.strip()
    try:
        mpr = _get_mpr()
    except RuntimeError as e:
        return f"错误：{e}"

    try:
        dos = mpr.get_dos_by_material_id(mp_id)
        if dos is None:
            return f"未找到 {mp_id} 的态密度数据"

        # dos is a CompleteDos object
        gap_raw = dos.get_gap()
        if isinstance(gap_raw, dict):
            gap = gap_raw.get("energy", None)
        else:
            gap = gap_raw  # float or None
        fermi = dos.efermi

        lines = [
            f"## {mp_id} 态密度 (DOS)",
            f"- **费米能级**: {fermi:.4f} eV",
        ]
        if gap is not None:
            lines.append(f"- **带隙**: {gap:.4f} eV")
        else:
            lines.append("- **带隙**: 无（金属性）")

        lines.append(f"- **能量范围**: {dos.energies[0]:.2f} ~ {dos.energies[-1]:.2f} eV")
        lines.append(f"- **能量点数**: {len(dos.energies)}")

        # 总 DOS 在费米面处的值
        try:
            td_val = dos.get_interpolated_value(fermi)
            lines.append(f"- **TDOS(Fermi)**: {td_val:.4f} states/eV")
        except Exception:
            pass

        return "\n".join(lines)

    except Exception as e:
        logger.error(f"mp_get_dos 失败 [{mp_id}]: {e}")
        return f"获取 {mp_id} 态密度失败: {e}"


def mp_search_by_chemsys(chemsys: str, limit: int = RESULT_LIMIT) -> str:
    """按化学体系搜索材料，如 'Li-Fe-O'"""
    if not chemsys or not chemsys.strip():
        return "错误：请提供 chemsys 参数"

    chemsys = chemsys.strip()
    try:
        mpr = _get_mpr()
    except RuntimeError as e:
        return f"错误：{e}"

    try:
        results = mpr.materials.summary.search(chemsys=chemsys)
        if not results:
            return f"化学体系 {chemsys} 未找到材料"

        total = len(results)
        results = results[:limit]

        lines = [f"化学体系 **{chemsys}** 共找到 {total} 个材料，显示前 {len(results)} 个：\n"]
        for r in results:
            d = _doc_to_dict(r)
            lines.append(
                f"- **{d.get('material_id', '?')}**: {d.get('formula_pretty', '?')}"
            )
            if d.get("band_gap") is not None:
                lines.append(f"  带隙: {d['band_gap']:.3f} eV | E_above_hull: {d.get('energy_above_hull', 'N/A')}")
            lines.append("")

        return "\n".join(lines)

    except Exception as e:
        logger.error(f"mp_search_by_chemsys 失败 [{chemsys}]: {e}")
        return f"化学体系搜索失败: {e}"
