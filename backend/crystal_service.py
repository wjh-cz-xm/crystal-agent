"""晶体结构处理服务 — 基于 Pymatgen + CrystalNN"""

from __future__ import annotations
import logging

from pymatgen.core import Structure, Lattice
from pymatgen.analysis.local_env import CrystalNN

logger = logging.getLogger(__name__)

# ========== Si 测试结构（金刚石立方, mp-149）==========
_lat = Lattice.cubic(5.4687)
_SI_STRUCTURE = Structure.from_spacegroup("Fd-3m", _lat, ["Si"], [[0, 0, 0]])
TEST_CIF_SI = _SI_STRUCTURE.to(fmt="cif")


def _parse(cif_data: str) -> Structure:
    """CIF 文本 → Structure"""
    return Structure.from_str(cif_data, fmt="cif")


def _to_cif(structure: Structure) -> str:
    """Structure → CIF 文本"""
    return structure.to(fmt="cif")


def extract_metadata(cif_data: str) -> dict:
    """提取化学式、空间群、元素列表、原子数等元数据"""
    s = _parse(cif_data)
    elements = sorted(set(str(sp) for sp in s.composition.elements))
    sg = "N/A"
    try:
        sg = s.get_space_group_info()[0]
    except Exception:
        pass
    return {
        "formula": s.composition.reduced_formula,
        "formula_pretty": s.composition.formula.replace(" ", ""),
        "num_atoms": len(s),
        "elements": elements,
        "space_group": sg,
    }


def switch_cell(cif_data: str, cell_type: str) -> str:
    """切换原胞/惯用胞, 返回新 CIF"""
    s = _parse(cif_data)
    if cell_type == "primitive":
        result = s.to_primitive()
    elif cell_type == "conventional":
        result = s.to_conventional()
    else:
        raise ValueError(f"未知晶胞类型: {cell_type}")
    return _to_cif(result)


def build_supercell(cif_data: str, a: int, b: int, c: int) -> str:
    """构建超胞, 返回新 CIF; 原胞原子数 > 50 时拒绝"""
    s = _parse(cif_data)
    primitive = s.to_primitive()
    if len(primitive) > 50:
        raise ValueError(f"原胞原子数 ({len(primitive)}) 超过 50, 不支持构建超胞")
    result = s.make_supercell([a, b, c])
    return _to_cif(result)


def _structure_to_xyz(sites, total) -> str:
    """将 site 列表转为 XYZ 格式（笛卡尔坐标，无折叠问题）"""
    lines = [str(total), "crystal"]
    for site in sites:
        c = site.coords
        lines.append(f"{site.species_string}  {c[0]:.6f}  {c[1]:.6f}  {c[2]:.6f}")
    return "\n".join(lines)


def add_boundary_atoms(cif_data: str, periodic: bool, outside: bool):
    """返回 (data, format)；仅在启用时通过 XYZ 补齐边界/成键原子"""
    if not periodic and not outside:
        return cif_data, "cif"

    from pymatgen.core import PeriodicSite
    s = _parse(cif_data)
    sites_out = list(s.sites)
    added: set[tuple] = set()

    # ---- 周期性边界原子重复（只复制面/棱/角上的原子）----
    if periodic:
        threshold = 0.05
        for site in s.sites:
            fc = site.frac_coords
            x_shifts = []
            if fc[0] < threshold: x_shifts.append(1)
            if fc[0] > 1 - threshold: x_shifts.append(-1)
            y_shifts = []
            if fc[1] < threshold: y_shifts.append(1)
            if fc[1] > 1 - threshold: y_shifts.append(-1)
            z_shifts = []
            if fc[2] < threshold: z_shifts.append(1)
            if fc[2] > 1 - threshold: z_shifts.append(-1)

            for sx in [0] + x_shifts:
                for sy in [0] + y_shifts:
                    for sz in [0] + z_shifts:
                        if sx == 0 and sy == 0 and sz == 0:
                            continue
                        shift = [sx, sy, sz]
                        key = (site.species_string,
                               round(fc[0] + shift[0], 6),
                               round(fc[1] + shift[1], 6),
                               round(fc[2] + shift[2], 6))
                        if key not in added:
                            added.add(key)
                            new_site = PeriodicSite(
                                species=site.specie,
                                coords=[fc[k] + shift[k] for k in range(3)],
                                lattice=s.lattice,
                                coords_are_cartesian=False,
                            )
                            sites_out.append(new_site)

    # ---- 晶胞外成键原子 ----
    if outside:
        cnn = CrystalNN()
        # 获取 CrystalNN 的键长判据（每种元素对的截断距离）
        bond_cutoffs: dict[tuple[str, str], float] = {}
        for i in range(len(s)):
            try:
                for nb in cnn.get_nn_info(s, i):
                    j = nb["site_index"]
                    ei = str(s[i].species_string)
                    ej = str(s[j].species_string)
                    dist = float(s[i].distance(nb["site"]))
                    key = tuple(sorted([ei, ej]))
                    if key not in bond_cutoffs or dist > bond_cutoffs[key]:
                        bond_cutoffs[key] = dist
            except Exception:
                continue
        # 给截断距离加 10% 容差
        for k in bond_cutoffs:
            bond_cutoffs[k] *= 1.10

        # 对 6 个相邻胞方向逐一检查
        for shift in [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]:
            for orig in s.sites:
                for target in s.sites:
                    ei = str(orig.species_string)
                    ej = str(target.species_string)
                    cutoff = bond_cutoffs.get(tuple(sorted([ei, ej])))
                    if cutoff is None:
                        continue
                    # target 平移 shift 后的位置
                    shifted_frac = [target.frac_coords[k] + shift[k] for k in range(3)]
                    shifted_site = PeriodicSite(
                        species=target.specie,
                        coords=shifted_frac,
                        lattice=s.lattice,
                        coords_are_cartesian=False,
                    )
                    if orig.distance(shifted_site) <= cutoff:
                        key = (ej,
                               round(shifted_frac[0], 6),
                               round(shifted_frac[1], 6),
                               round(shifted_frac[2], 6))
                        if key not in added:
                            added.add(key)
                            sites_out.append(shifted_site)

    return _structure_to_xyz(sites_out, len(sites_out)), "xyz"


def get_lattice_vectors(cif_data: str) -> list[list[float]]:
    """提取晶格矢量（Cartesian 坐标），供前端画单胞框线"""
    s = _parse(cif_data)
    m = s.lattice.matrix
    return [m[0].tolist(), m[1].tolist(), m[2].tolist()]


def compute_bonds(cif_data: str) -> dict:
    """CrystalNN 计算键连, 返回 {pairs, total}"""
    s = _parse(cif_data)
    cnn = CrystalNN()
    pairs: list[dict] = []
    seen: set[tuple[int, int]] = set()

    for i in range(len(s)):
        try:
            for nb in cnn.get_nn_info(s, i):
                j = int(nb["site_index"])
                key = (min(i, j), max(i, j))
                if key not in seen:
                    seen.add(key)
                    dist = round(float(s[i].distance(nb["site"])), 3)
                    pairs.append({
                        "from": i,
                        "to": j,
                        "from_elem": str(s[i].species_string),
                        "to_elem": str(s[j].species_string),
                        "distance": dist,
                    })
        except Exception:
            continue

    return {"pairs": pairs, "total": len(pairs)}
