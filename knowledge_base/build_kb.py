"""
晶体学知识库构建脚本
从 WebSearch 收集的内容整合为结构化 JSON 知识库
"""
import json
import os

KB_DIR = os.path.dirname(os.path.abspath(__file__))
CATEGORIES_DIR = os.path.join(KB_DIR, "categories")

# ============================================================
# 分类 1: 晶体几何基础
# ============================================================
crystal_basics = [
    {
        "id": "crystal_lattice",
        "title_zh": "晶体点阵（晶格）",
        "title_en": "Crystal Lattice",
        "category": "crystal_basics",
        "tags": ["点阵", "晶格", "基矢", "平移对称性", "原胞"],
        "difficulty": "入门",
        "source": "Wikipedia + LibreTexts + IUCr Dictionary",
        "content": (
            "## 定义\n\n"
            "**晶体点阵**（Crystal Lattice）是晶体内部原子排列的数学抽象。它是一个在三维空间中由离散点构成的无限、周期性的阵列，"
            "每个点（阵点）具有完全相同的环境。\n\n"
            "## 数学描述\n\n"
            "任意阵点的位置矢量 $\\mathbf{R}$ 可以表示为三个**基矢**（basis vectors）$\\mathbf{a}$、$\\mathbf{b}$、$\\mathbf{c}$ 的整数线性组合：\n\n"
            "$$\\mathbf{R} = u\\mathbf{a} + v\\mathbf{b} + w\\mathbf{c}$$\n\n"
            "其中 $u, v, w$ 为任意整数。\n\n"
            "## 原胞与晶胞\n\n"
            "- **原胞（Primitive Cell）**：体积最小的重复单元，仅包含一个阵点。原胞体积为 $V = |\\mathbf{a} \\cdot (\\mathbf{b} \\times \\mathbf{c})|$。\n"
            "- **惯用胞（Conventional Cell）**：为方便反映晶体对称性而选取的、可能包含多个阵点的较大单元。例如面心立方（fcc）的惯用胞包含4个阵点。\n"
            "- **Wigner-Seitz 原胞**：以某个阵点为中心、作该点到所有近邻阵点连线的垂直平分面，所围成的最小体积区域。在倒空间中称为 Brillouin 区。\n\n"
            "## 关键理解\n\n"
            "晶体结构 = 点阵（Lattice）+ 基元（Basis）。基元是附着在每个阵点上的原子（或原子团）的具体排列。"
            "同样一个 fcc 点阵，基元为单个 Cu 原子得到金属铜的结构；基元为 Na$^+$-Cl$^-$ 对则得到岩盐结构。"
        ),
        "formulas": [
            "$\\mathbf{R} = u\\mathbf{a} + v\\mathbf{b} + w\\mathbf{c}$",
            "$V = |\\mathbf{a} \\cdot (\\mathbf{b} \\times \\mathbf{c})|$"
        ],
        "related": ["unit_cell", "bravais_lattices", "crystal_systems"]
    },
    {
        "id": "unit_cell",
        "title_zh": "晶胞",
        "title_en": "Unit Cell",
        "category": "crystal_basics",
        "tags": ["晶胞", "原胞", "惯用胞", "晶胞参数", "Wigner-Seitz"],
        "difficulty": "入门",
        "source": "Wikipedia + LibreTexts",
        "content": (
            "## 定义\n\n"
            "**晶胞**（Unit Cell）是晶体结构中最小的平行六面体重复单元，通过它在三维空间中的平移可以重现整个晶体。\n\n"
            "## 晶胞参数\n\n"
            "晶胞由 6 个参数完全描述——**晶格常数**（lattice constants）：\n\n"
            "- **棱长**：$a$、$b$、$c$（沿三个晶轴的长度）\n"
            "- **轴间角**：$\\alpha$（$b$ 与 $c$ 之间的夹角）、$\\beta$（$a$ 与 $c$ 之间的夹角）、$\\gamma$（$a$ 与 $b$ 之间的夹角）\n\n"
            "## 原胞 vs 惯用胞\n\n"
            "| 类型 | 阵点数 | 特点 |\n"
            "|------|--------|------|\n"
            "| 原胞 (Primitive) | 1 | 体积最小，但不一定反映全部对称性 |\n"
            "| 惯用胞 (Conventional) | ≥1 | 反映完整对称性，可能包含多个阵点 |\n\n"
            "例如：\n"
            "- **简单立方（P）**：原胞 = 惯用胞，含 1 个阵点\n"
            "- **体心立方（I）**：惯用胞含 2 个阵点，原胞为菱面体\n"
            "- **面心立方（F）**：惯用胞含 4 个阵点，原胞为菱面体\n"
            "- **底心（C）**：惯用胞含 2 个阵点\n\n"
            "## Wigner-Seitz 原胞\n\n"
            "一种特殊原胞的构造方法：选取一个阵点为中心，作该点到所有近邻阵点连线的垂直平分面，"
            "这些面所围成的最小区域即为 Wigner-Seitz 原胞。在倒空间中，Wigner-Seitz 原胞就是第一 Brillouin 区。"
        ),
        "formulas": [],
        "related": ["crystal_lattice", "bravais_lattices", "crystal_systems"]
    },
    {
        "id": "crystal_systems",
        "title_zh": "七大晶系",
        "title_en": "Seven Crystal Systems",
        "category": "crystal_basics",
        "tags": ["晶系", "晶胞参数", "对称性", "Bravais点阵"],
        "difficulty": "入门",
        "source": "Wikipedia + LibreTexts",
        "content": (
            "## 定义\n\n"
            "根据晶胞参数（$a, b, c, \\alpha, \\beta, \\gamma$）的关系，所有晶体可以分为 **7 大晶系**（Crystal Systems）。\n\n"
            "## 七大晶系一览\n\n"
            "| 晶系 | 棱长关系 | 轴间角关系 | 独立参数数 |\n"
            "|------|----------|------------|------------|\n"
            "| **三斜** (Triclinic) | $a \\neq b \\neq c$ | $\\alpha \\neq \\beta \\neq \\gamma \\neq 90^\\circ$ | 6 |\n"
            "| **单斜** (Monoclinic) | $a \\neq b \\neq c$ | $\\alpha = \\gamma = 90^\\circ, \\beta \\neq 90^\\circ$ | 4 |\n"
            "| **正交** (Orthorhombic) | $a \\neq b \\neq c$ | $\\alpha = \\beta = \\gamma = 90^\\circ$ | 3 |\n"
            "| **四方** (Tetragonal) | $a = b \\neq c$ | $\\alpha = \\beta = \\gamma = 90^\\circ$ | 2 |\n"
            "| **六方** (Hexagonal) | $a = b \\neq c$ | $\\alpha = \\beta = 90^\\circ, \\gamma = 120^\\circ$ | 2 |\n"
            "| **三方/菱面体** (Trigonal/Rhombohedral) | $a = b = c$ | $\\alpha = \\beta = \\gamma \\neq 90^\\circ$ | 2 |\n"
            "| **立方** (Cubic) | $a = b = c$ | $\\alpha = \\beta = \\gamma = 90^\\circ$ | 1 |\n\n"
            "## 对称性层次\n\n"
            "从三斜到立方，对称性依次升高：\n"
            "- 三斜晶系：仅有恒等操作（1）或反演中心（$\\bar{1}$）\n"
            "- 立方晶系：最高的对称性，含 4 个 3 次旋转轴（沿体对角线方向）\n\n"
            "## 为什么有且仅有 7 种？\n\n"
            "7 大晶系的划分基于点阵的**全对称群**（holosymmetric point group）。"
            "每种晶系对应一种特定的基本对称性组合，恰好只有 7 种在三维空间中自洽的可能。"
        ),
        "formulas": [],
        "related": ["bravais_lattices", "point_groups", "space_groups"]
    },
    {
        "id": "bravais_lattices",
        "title_zh": "14种Bravais点阵",
        "title_en": "14 Bravais Lattices",
        "category": "crystal_basics",
        "tags": ["Bravais点阵", "点阵类型", "P", "I", "F", "C", "Auguste Bravais"],
        "difficulty": "入门",
        "source": "Wikipedia + IUCr",
        "content": (
            "## 历史\n\n"
            "1848 年，法国物理学家 **Auguste Bravais** 证明了三维空间中存在且仅存在 **14 种不同的空间点阵**，"
            "称为 Bravais 点阵。\n\n"
            "## 分类\n\n"
            "按点阵类型分为 4 类：\n"
            "- **P（Primitive，简单）**：阵点仅在平行六面体的 8 个顶点\n"
            "- **I（Body-centered，体心）**：除顶点外，体心还有一个阵点\n"
            "- **F（Face-centered，面心）**：除顶点外，6 个面的中心各有一个阵点\n"
            "- **C（Base-centered，底心）**：除顶点外，一对相对面的中心各有一个阵点\n\n"
            "## 14 种 Bravais 点阵列表\n\n"
            "| 晶系 | Bravais 点阵 | 符号 |\n"
            "|------|-------------|------|\n"
            "| 三斜 | 简单三斜 | P |\n"
            "| 单斜 | 简单单斜、底心单斜 | P, C |\n"
            "| 正交 | 简单正交、底心正交、体心正交、面心正交 | P, C, I, F |\n"
            "| 四方 | 简单四方、体心四方 | P, I |\n"
            "| 六方 | 简单六方 | P |\n"
            "| 三方/菱面体 | 简单三方（菱面体） | P |\n"
            "| 立方 | 简单立方、体心立方、面心立方 | P, I, F |\n\n"
            "## 为什么四方没有面心？\n\n"
            "四方晶系的 F 点阵可以通过重新选取晶胞降为 I 点阵（体积减半）。同理，"
            "立方晶系没有 C 点阵（C 立方 = P 四方）。Bravais 点阵的定义要求："
            "每种点阵的对称性必须与该晶系的全对称群一致。"
        ),
        "formulas": [],
        "related": ["crystal_systems", "crystal_lattice", "point_groups"]
    },
    {
        "id": "miller_indices",
        "title_zh": "Miller指数（晶面指数）",
        "title_en": "Miller Indices",
        "category": "crystal_basics",
        "tags": ["Miller指数", "晶面", "晶向", "hkl", "William Miller"],
        "difficulty": "入门",
        "source": "Wikipedia + IUCr Dictionary",
        "content": (
            "## 定义\n\n"
            "**Miller 指数**（Miller Indices），由 William Hallowes Miller 于 1839 年引入，"
            "是用三个整数 $(hkl)$ 标记晶体中晶面（lattice planes）的标准符号系统。\n\n"
            "## 两种等价定义\n\n"
            "### 定义 1：倒易点阵矢量法\n"
            "Miller 指数 $(hkl)$ 定义了一个倒易点阵矢量 $\\mathbf{g}_{hkl}$，该矢量垂直于该族晶面：\n\n"
            "$$\\mathbf{g}_{hkl} = h\\mathbf{a}^* + k\\mathbf{b}^* + l\\mathbf{c}^*$$\n\n"
            "### 定义 2：截距倒数法\n"
            "晶面 $(hkl)$ 在三个晶轴上截距分别为 $\\mathbf{a}/h$、$\\mathbf{b}/k$、$\\mathbf{c}/l$。"
            "指数与截距成反比。指数越小，截距越大。若指数为 0，则该晶面与该轴平行（截距\"无穷大\"）。\n\n"
            "## 符号规范（IUCr 标准）\n\n"
            "| 符号 | 含义 | 示例 |\n"
            "|------|------|------|\n"
            "| $(hkl)$ | 特定晶面或一族平行晶面 | $(111)$ |\n"
            "| $\\{hkl\\}$ | 对称性等效的所有晶面族 | $\\{100\\}$ 在立方中包括 $(100), (010), (001)$ |\n"
            "| $[uvw]$ | 晶向（direct lattice 方向） | $[110]$ |\n"
            "| $\\langle uvw \\rangle$ | 对称性等效的所有晶向族 | $\\langle 111 \\rangle$ |\n\n"
            "## 负指数表示\n\n"
            "负指数在数字上方加横线（读作\"bar\"），LaTeX 写法：`$\\bar{1}$`。如 $(\\bar{1}11)$ 表示 $h=-1, k=1, l=1$。\n\n"
            "## 六方晶系的 Miller-Bravais 指数\n\n"
            "六方晶系常使用 4 指数 $(hkil)$，其中 $i = -(h+k)$，使得三个面内方向具有等价的对称性。\n\n"
            "## 晶面间距公式（立方晶系）\n\n"
            "$$d_{hkl} = \\frac{a}{\\sqrt{h^2 + k^2 + l^2}}$$\n\n"
            "其中 $a$ 为立方晶系的晶格常数。这是 Bragg 定律的关键输入参数。"
        ),
        "formulas": [
            "$d_{hkl} = \\frac{a}{\\sqrt{h^2 + k^2 + l^2}}$",
            "$\\mathbf{g}_{hkl} = h\\mathbf{a}^* + k\\mathbf{b}^* + l\\mathbf{c}^*$"
        ],
        "related": ["bragg_law", "reciprocal_lattice", "close_packing"]
    },
    {
        "id": "close_packing",
        "title_zh": "密堆积结构",
        "title_en": "Close-Packed Structures",
        "category": "crystal_basics",
        "tags": ["密堆积", "hcp", "fcc", "ccp", "堆积率", "配位数", "四面体空隙", "八面体空隙"],
        "difficulty": "入门",
        "source": "Wikipedia + LibreTexts",
        "content": (
            "## 概念\n\n"
            "当等径刚性球以最紧密的方式堆叠时，形成**密堆积结构**（Close-Packed Structures）。"
            "这是大多数金属（Cu, Al, Mg, Ti 等）和稀有气体晶体的基本结构类型。\n\n"
            "## 最大堆积率\n\n"
            "等径球的最大空间填充率为：\n\n"
            "$$\\frac{\\pi}{3\\sqrt{2}} \\approx 74.05\\%$$\n\n"
            "## 两种密堆积方式\n\n"
            "密堆积的层排列方式有两种，用 ABC 记法表示：\n\n"
            "- **六方密堆积（hcp）**：ABABAB... 堆垛序列\n"
            "  - 空间群：$P6_3/mmc$（No. 194）\n"
            "  - 每惯用胞 2 个原子\n"
            "  - 典型材料：Mg, Zn, Ti, Be, Zr\n\n"
            "- **立方密堆积（ccp/fcc）**：ABCABC... 堆垛序列\n"
            "  - 空间群：$Fm\\bar{3}m$（No. 225）\n"
            "  - 每惯用胞 4 个原子\n"
            "  - 典型材料：Cu, Al, Au, Ag, Ni, Pt\n\n"
            "## 关键参数\n"
            "- **配位数（CN）**：12（每个原子被 12 个最近邻包围）\n"
            "- **八面体空隙**：配位数 6，数量 = 原子数（每个原子 1 个）\n"
            "- **四面体空隙**：配位数 4，数量 = 2 × 原子数（每个原子 2 个）\n\n"
            "## 为什么有材料选 hcp 而非 fcc？\n\n"
            "两种结构的最近邻数和堆积率完全相同。区别来自次近邻——hcp 和 fcc 的第三近邻距离不同，"
            "这在过渡金属中影响 d 电子的能带结构和结合能，从而决定了结构稳定性。"
        ),
        "formulas": [
            "$\\frac{\\pi}{3\\sqrt{2}} \\approx 74.05\\%$"
        ],
        "related": ["interstitial_sites", "crystal_systems", "rock_salt_structure"]
    },
    {
        "id": "interstitial_sites",
        "title_zh": "间隙位置",
        "title_en": "Interstitial Sites",
        "category": "crystal_basics",
        "tags": ["间隙", "八面体空隙", "四面体空隙", "填隙原子", "fcc", "hcp", "bcc"],
        "difficulty": "中级",
        "source": "Wikipedia + LibreTexts",
        "content": (
            "## 定义\n\n"
            "在密堆积结构中，原子之间存在着未被占据的空隙，称为**间隙位置**（Interstitial Sites）。"
            "较小的原子（如 H, C, N, O）可以进入这些位置，形成间隙固溶体或间隙化合物。\n\n"
            "## 八面体空隙（Octahedral Sites）\n\n"
            "- 被 6 个原子包围（配位数 = 6）\n"
            "- fcc：位于体心位置 $\\left(\\frac{1}{2}, \\frac{1}{2}, \\frac{1}{2}\\right)$ 及各棱的中点\n"
            "- 数量 = 阵点数（fcc 中 4 个/惯用胞）\n"
            "- 最大可容纳半径比：$r_{间隙}/r_{基体} \\approx 0.414$\n\n"
            "## 四面体空隙（Tetrahedral Sites）\n\n"
            "- 被 4 个原子包围（配位数 = 4）\n"
            "- fcc：位于 $\\left(\\frac{1}{4}, \\frac{1}{4}, \\frac{1}{4}\\right)$ 等 8 个等效位置\n"
            "- 数量 = 2 × 阵点数（fcc 中 8 个/惯用胞）\n"
            "- 最大可容纳半径比：$r_{间隙}/r_{基体} \\approx 0.225$\n\n"
            "## 与典型结构的关系\n\n"
            "| 结构 | 基体点阵 | 占据的间隙 | 占据率 |\n"
            "|------|----------|-----------|--------|\n"
            "| NaCl（岩盐） | fcc | 全部八面体空隙 | 100% |\n"
            "| ZnS（闪锌矿） | fcc | 半数四面体空隙 | 50% |\n"
            "| CaF₂（萤石） | fcc | 全部四面体空隙 | 100% |\n"
            "| 金刚石 | fcc | 半数四面体空隙 | 50% |\n\n"
            "这解释了为什么 NaCl 配位数是 6:6（八面体），而 ZnS 是 4:4（四面体）。"
        ),
        "formulas": [
            "$r_{八面体}/r_{基体} \\approx 0.414$",
            "$r_{四面体}/r_{基体} \\approx 0.225$"
        ],
        "related": ["close_packing", "rock_salt_structure", "zinc_blende_structure", "diamond_structure"]
    },
]

# ============================================================
# 分类 2: 对称性理论
# ============================================================
symmetry = [
    {
        "id": "symmetry_operations",
        "title_zh": "对称操作",
        "title_en": "Symmetry Operations",
        "category": "symmetry",
        "tags": ["对称操作", "旋转", "反映", "反演", "螺旋轴", "滑移面", "Seitz符号"],
        "difficulty": "入门",
        "source": "IUCr International Tables + LibreTexts",
        "content": (
            "## 定义\n\n"
            "**对称操作**（Symmetry Operation）是一种变换，使晶体在变换后与原来不可区分。\n\n"
            "## 点对称操作（至少保持一点不动）\n\n"
            "| 操作 | 符号 | 描述 |\n"
            "|------|------|------|\n"
            "| 恒等 | $1$ | 什么都不做 |\n"
            "| 旋转 | $n$ | 绕轴旋转 $360^\\circ/n$；$n=1,2,3,4,6$ |\n"
            "| 反映 | $m$ | 通过镜面反映 |\n"
            "| 反演 | $\\bar{1}$ | $(x,y,z) \\to (-x,-y,-z)$，中心对称 |\n"
            "| 旋转反演 | $\\bar{n}$ | 旋转 $360^\\circ/n$ 后反演；$\\bar{2} \\equiv m$ |\n\n"
            "## 晶体学限制定理\n\n"
            "由于平移对称性的约束，晶体中只能存在 $n=1,2,3,4,6$ 次旋转轴。"
            "**五重对称轴**（如准晶中）与周期性点阵不兼容。\n\n"
            "## 含平移的对称操作\n\n"
            "| 操作 | 符号 | 描述 |\n"
            "|------|------|------|\n"
            "| 螺旋轴（Screw Axis） | $n_m$ | 旋转 $360^\\circ/n$ + 沿轴平移 $m/n$ 的晶格周期 |\n"
            "| 滑移面（Glide Plane） | $a,b,c,n,d$ | 反映 + 平移（如 $a$ 滑移 = 反映 + $\\mathbf{a}/2$ 平移）|\n\n"
            "## Seitz 符号\n\n"
            "空间群操作统一记为 $(\\mathbf{R}|\\boldsymbol{\\tau})$：\n\n"
            "$$\\mathbf{x}' = \\mathbf{R}\\mathbf{x} + \\boldsymbol{\\tau}$$\n\n"
            "其中 $\\mathbf{R}$ 为旋转/反映矩阵，$\\boldsymbol{\\tau}$ 为平移矢量。若 $\\boldsymbol{\\tau}=0$，则为点操作。"
        ),
        "formulas": [
            "$\\mathbf{x}' = \\mathbf{R}\\mathbf{x} + \\boldsymbol{\\tau}$"
        ],
        "related": ["point_groups", "space_groups", "crystal_systems"]
    },
    {
        "id": "point_groups",
        "title_zh": "点群",
        "title_en": "Point Groups (Crystal Classes)",
        "category": "symmetry",
        "tags": ["点群", "32种点群", "Laue类", "晶体学限制"],
        "difficulty": "中级",
        "source": "IUCr International Tables + LibreTexts",
        "content": (
            "## 定义\n\n"
            "**点群**（Point Group）是只包含点对称操作（无平移）的对称群。所有操作至少保持一点不动。"
            "描述了晶体的**宏观**对称性。\n\n"
            "## 32 种晶体学点群\n\n"
            "三维空间中共有 32 种晶体学点群，可由以下方式导出：\n"
            "- 7 大晶系各对应一个全对称点群（最高对称性）\n"
            "- 每个全对称点群的子群即为该晶系的其他点群\n\n"
            "### 各晶系对应的点群（部分列举）\n\n"
            "| 晶系 | 点群举例 |\n"
            "|------|----------|\n"
            "| 三斜 | $1$, $\\bar{1}$ |\n"
            "| 单斜 | $2$, $m$, $2/m$ |\n"
            "| 正交 | $222$, $mm2$, $mmm$ |\n"
            "| 四方 | $4$, $\\bar{4}$, $4/m$, $422$, $4mm$, $\\bar{4}2m$, $4/mmm$ |\n"
            "| 三方 | $3$, $\\bar{3}$, $321$, $3m$, $\\bar{3}m$ |\n"
            "| 六方 | $6$, $\\bar{6}$, $6/m$, $622$, $6mm$, $\\bar{6}2m$, $6/mmm$ |\n"
            "| 立方 | $23$, $m\\bar{3}$, $432$, $\\bar{4}3m$, $m\\bar{3}m$ |\n\n"
            "## Laue 类\n\n"
            "32 种点群中，有 11 种是**中心对称**的（含有反演中心 $\\bar{1}$），称为 Laue 类。"
            "X 射线衍射由于 Friedel 定律，衍射图样总是中心对称的，因此只能区分 11 种 Laue 类，而非全部的 32 种点群。\n\n"
            "## 点群与物理性质\n\n"
            "- 只有非中心对称的点群才可能具有压电性（piezoelectricity）\n"
            "- 只有极性点群（10 种）才可能具有铁电性（ferroelectricity）\n"
            "- 光学活性要求晶体属于 15 种手性点群之一"
        ),
        "formulas": [],
        "related": ["space_groups", "symmetry_operations", "crystal_systems"]
    },
    {
        "id": "space_groups",
        "title_zh": "空间群",
        "title_en": "Space Groups",
        "category": "symmetry",
        "tags": ["空间群", "230种空间群", "Hermann-Mauguin符号", "Fm-3m", "Pm-3m", "P63/mmc"],
        "difficulty": "高级",
        "source": "IUCr International Tables + Wikipedia",
        "content": (
            "## 定义\n\n"
            "**空间群**（Space Group）是晶体所有对称操作的完整集合，包含点操作和平移操作（螺旋轴、滑移面）。"
            "1891年，Fedorov 和 Schönflies 独立证明了三维空间中共有 **230 种空间群**。\n\n"
            "## 层级关系\n\n"
            "$$\\text{7 大晶系} \\to \\text{14 Bravais 点阵} \\to \\text{32 点群} \\to \\text{230 空间群}$$\n\n"
            "## Hermann-Mauguin 符号\n\n"
            "国际晶体学表采用的标准符号格式：`[点阵类型][对称元素1][对称元素2][对称元素3]`\n\n"
            "| 空间群 | 编号 | 典型材料 | 含义 |\n"
            "|--------|------|----------|------|\n"
            "| $P1$ | No. 1 | — | 最简单的空间群，仅恒等操作 |\n"
            "| $P\\bar{1}$ | No. 2 | — | 增加反演中心 |\n"
            "| $P2_1/c$ | No. 14 | 许多有机晶体 | $2_1$ 螺旋轴 + $c$ 滑移面 |\n"
            "| $Pm\\bar{3}m$ | No. 221 | CsCl, 钙钛矿（立方相）| 简单立方最高对称 |\n"
            "| $Fm\\bar{3}m$ | No. 225 | Cu, Al, NaCl | 面心立方最高对称 |\n"
            "| $Fd\\bar{3}m$ | No. 227 | 金刚石, Si, Ge | 面心立方 + 金刚石滑移 |\n"
            "| $Im\\bar{3}m$ | No. 229 | Fe, Cr, W (bcc) | 体心立方最高对称 |\n"
            "| $P6_3/mmc$ | No. 194 | Mg, Zn (hcp) | 六方密堆积 |\n\n"
            "## 空间群的物理意义\n\n"
            "- 空间群决定了晶体的全部宏观和微观物理性质\n"
            "- X 射线衍射的系统消光规律直接反映空间群的对称元素\n"
            "- **蛋白质晶体**只有 65 种可能的空间群（因为镜面和反演中心会破坏手性氨基酸的 L 构型）"
        ),
        "formulas": [],
        "related": ["point_groups", "symmetry_operations", "bravais_lattices"]
    },
]

# ============================================================
# 分类 3: 典型晶体结构
# ============================================================
crystal_structures = [
    {
        "id": "rock_salt_structure",
        "title_zh": "岩盐型结构（NaCl型）",
        "title_en": "Rock Salt Structure (NaCl type)",
        "category": "crystal_structures",
        "tags": ["NaCl", "岩盐", "B1", "Strukturbericht", "离子晶体", "八面体配位"],
        "difficulty": "入门",
        "source": "Wikipedia + LibreTexts + Materials Project",
        "content": (
            "## 概述\n\n"
            "**岩盐型结构**（Rock Salt / Halite），Strukturbericht 符号 **B1**，是最常见的离子晶体结构类型之一。\n\n"
            "## 结构特征\n\n"
            "- **原型**：NaCl（氯化钠）\n"
            "- **晶系**：立方\n"
            "- **Bravais 点阵**：面心立方（fcc）\n"
            "- **空间群**：$Fm\\bar{3}m$（No. 225）\n"
            "- **每惯用胞分子数**：Z = 4\n"
            "- **配位数**：6:6（八面体）\n\n"
            "## 原子位置\n\n"
            "- Cl$^-$：$(0, 0, 0)$ —— fcc 位置\n"
            "- Na$^+$：$(\\frac{1}{2}, \\frac{1}{2}, \\frac{1}{2})$ —— 全部八面体空隙\n\n"
            "实际上就是两个 fcc 亚点阵互相穿插，沿 $[100]$ 方向错开半个晶格常数。\n\n"
            "## 晶体参数\n\n"
            "- **晶格常数**：$a = 5.64 \\mathring{A}$（0.564 nm）\n"
            "- **Pearson 符号**：cF8\n\n"
            "## 其他代表性材料\n\n"
            "绝大多数碱金属卤化物（LiF, NaF, KCl, KBr, RbI）和碱土金属氧化物（MgO, CaO, NiO, FeO）"
            "都采用此结构。\n\n"
            "## 几何关系\n\n"
            "在刚球模型中：\n"
            "$$r_{阳} + r_{阴} = a/2$$\n"
            "配位数 6 要求半径比 $r_{阳}/r_{阴} > 0.414$（八面体配位的下限）。"
        ),
        "formulas": [
            "$r_{阳} + r_{阴} = a/2$"
        ],
        "related": ["cscl_structure", "zinc_blende_structure", "interstitial_sites", "close_packing"]
    },
    {
        "id": "cscl_structure",
        "title_zh": "氯化铯型结构（CsCl型）",
        "title_en": "Cesium Chloride Structure (CsCl type)",
        "category": "crystal_structures",
        "tags": ["CsCl", "B2", "简单立方", "8配位", "离子晶体"],
        "difficulty": "入门",
        "source": "Wikipedia + LibreTexts + Materials Project",
        "content": (
            "## 概述\n\n"
            "**氯化铯型结构**，Strukturbericht 符号 **B2**。注意：CsCl 常被误认为是体心立方（bcc）结构，"
            "但它实际上是**简单立方（P）**点阵，基元为 Cl$^-$（0,0,0）+ Cs$^+$（½,½,½）。\n\n"
            "## 结构特征\n\n"
            "- **原型**：CsCl（氯化铯）\n"
            "- **晶系**：立方\n"
            "- **Bravais 点阵**：简单立方（P）\n"
            "- **空间群**：$Pm\\bar{3}m$（No. 221）\n"
            "- **每惯用胞分子数**：Z = 1\n"
            "- **配位数**：8:8（立方体形）\n\n"
            "## 原子位置\n\n"
            "- Cl$^-$：$(0, 0, 0)$\n"
            "- Cs$^+$：$(\\frac{1}{2}, \\frac{1}{2}, \\frac{1}{2})$\n\n"
            "两个简单立方亚点阵沿体对角线方向错开 $a\\sqrt{3}/2$。\n\n"
            "## 晶体参数\n\n"
            "- **晶格常数**：$a = 4.12 \\mathring{A}$（0.412 nm）\n"
            "- **Pearson 符号**：cP2\n\n"
            "## 为什么不是 bcc？\n\n"
            "bcc 结构要求顶点和体心的原子是**同种原子**。CsCl 中顶点是 Cl$^-$、体心是 Cs$^+$，"
            "两者的化学环境和散射因子完全不同，因此它不是 bcc，而是简单立方 + 两原子基元。\n\n"
            "## 形成条件\n\n"
            "配位数 8 要求半径比 $r_{阳}/r_{阴} > 0.732$（立方体配位的下限）。Cs$^+$ 半径（1.67 Å）较大，"
            "满足此条件。而 Na$^+$（1.02 Å）太小，无法形成 CsCl 结构。"
        ),
        "formulas": [],
        "related": ["rock_salt_structure", "bravais_lattices"]
    },
    {
        "id": "zinc_blende_structure",
        "title_zh": "闪锌矿型结构（ZnS型）",
        "title_en": "Zinc Blende (Sphalerite) Structure",
        "category": "crystal_structures",
        "tags": ["ZnS", "闪锌矿", "B3", "四面体配位", "半导体", "GaAs"],
        "difficulty": "中级",
        "source": "Wikipedia + LibreTexts + Materials Project",
        "content": (
            "## 概述\n\n"
            "**闪锌矿型结构**（Zinc Blende / Sphalerite），Strukturbericht 符号 **B3**。"
            "是 III-V 族和 II-VI 族半导体（GaAs, InP, ZnSe, CdTe 等）的主流结构。\n\n"
            "## 结构特征\n\n"
            "- **原型**：ZnS（立方硫化锌）\n"
            "- **晶系**：立方\n"
            "- **Bravais 点阵**：面心立方（fcc）\n"
            "- **空间群**：$F\\bar{4}3m$（No. 216）\n"
            "- **每惯用胞分子数**：Z = 4\n"
            "- **配位数**：4:4（四面体）\n\n"
            "## 原子位置\n\n"
            "- Zn：$(0, 0, 0)$ —— fcc 位置\n"
            "- S：$(\\frac{1}{4}, \\frac{1}{4}, \\frac{1}{4})$ —— 半数四面体空隙\n\n"
            "两个 fcc 亚点阵沿体对角线方向错开 $a\\sqrt{3}/4$。\n\n"
            "## 与金刚石结构的关系\n\n"
            "闪锌矿和金刚石结构的原子排布完全相同，但：\n"
            "- **金刚石**（$Fd\\bar{3}m$）：两种原子是同一元素（C-C），有反演中心\n"
            "- **闪锌矿**（$F\\bar{4}3m$）：两种原子是不同元素（Zn-S），无反演中心\n\n"
            "## 晶体参数\n\n"
            "- **晶格常数**：$a = 5.41 \\mathring{A}$（ZnS）\n"
            "- GaAs：$a = 5.653 \\mathring{A}$；InP：$a = 5.869 \\mathring{A}$\n\n"
            "## 物理意义\n\n"
            "闪锌矿结构缺乏反演中心 → 具有压电性。加上其 $sp^3$ 杂化导致半导体性质，"
            "使其成为光电子器件（LED、激光器、光电探测器）的核心材料。"
        ),
        "formulas": [],
        "related": ["diamond_structure", "wurtzite_structure", "rock_salt_structure"]
    },
    {
        "id": "diamond_structure",
        "title_zh": "金刚石型结构",
        "title_en": "Diamond Cubic Structure",
        "category": "crystal_structures",
        "tags": ["金刚石", "A4", "sp3杂化", "四面体配位", "Si", "Ge"],
        "difficulty": "入门",
        "source": "Wikipedia + LibreTexts + Materials Project",
        "content": (
            "## 概述\n\n"
            "**金刚石型结构**（Diamond Cubic），Strukturbericht 符号 **A4**。该结构完美诠释了 $sp^3$ 共价键的几何要求。\n\n"
            "## 结构特征\n\n"
            "- **原型**：C（金刚石）\n"
            "- **晶系**：立方\n"
            "- **Bravais 点阵**：面心立方（fcc）\n"
            "- **空间群**：$Fd\\bar{3}m$（No. 227）\n"
            "- **每惯用胞原子数**：8（两个 fcc 亚点阵 × 4）\n"
            "- **配位数**：4（$sp^3$ 正四面体）\n\n"
            "## 原子位置\n\n"
            "- C1：$(0, 0, 0)$ —— fcc 位置\n"
            "- C2：$(\\frac{1}{4}, \\frac{1}{4}, \\frac{1}{4})$ —— 半数四面体空隙\n\n"
            "## $sp^3$ 杂化与键角\n\n"
            "每个碳原子与 4 个最近邻形成 $sp^3$ 共价键，键角 $109.5^\\circ$（正四面体角）。"
            "C-C 键长为 $a\\sqrt{3}/4 \\approx 1.544 \\mathring{A}$。\n\n"
            "## 晶体参数\n\n"
            "| 材料 | 晶格常数 $a$（Å） | 带隙（eV） |\n"
            "|------|-------------------|------------|\n"
            "| C（金刚石） | 3.567 | 5.47 |\n"
            "| Si（硅） | 5.431 | 1.12 |\n"
            "| Ge（锗） | 5.658 | 0.67 |\n"
            "| $\\alpha$-Sn（灰锡） | 6.46 | 0（半金属） |\n\n"
            "## 原子堆积率\n\n"
            "$$\\frac{\\sqrt{3}\\pi}{16} \\approx 34\\%$$\n\n"
            "远低于密堆积的 74%，因为 $sp^3$ 共价键的方向性要求开放结构。"
        ),
        "formulas": [
            "$\\frac{\\sqrt{3}\\pi}{16} \\approx 34\\%$"
        ],
        "related": ["zinc_blende_structure", "close_packing", "interstitial_sites"]
    },
    {
        "id": "perovskite_structure",
        "title_zh": "钙钛矿型结构",
        "title_en": "Perovskite Structure",
        "category": "crystal_structures",
        "tags": ["钙钛矿", "ABX3", "CaTiO3", "八面体", "铁电体", "太阳能电池"],
        "difficulty": "中级",
        "source": "Wikipedia + LibreTexts + Materials Project",
        "content": (
            "## 概述\n\n"
            "**钙钛矿型结构**（Perovskite）是功能材料中最重要的结构类型之一，通式为 $ABX_3$。"
            "该结构家族涵盖铁电体（BaTiO₃）、超导体（YBa₂Cu₃O₇）、"
            "离子导体和高效太阳能电池材料（MAPbI₃）。\n\n"
            "## 理想立方结构\n\n"
            "- **原型**：CaTiO₃（钛酸钙），但高温相才为理想立方\n"
            "- **晶系**：立方（高温相）\n"
            "- **Bravais 点阵**：简单立方（P）\n"
            "- **空间群**：$Pm\\bar{3}m$（No. 221）\n"
            "- **每惯用胞分子数**：Z = 1\n\n"
            "## 原子位置（理想立方）\n\n"
            "- A 位（Ca）：$(\\frac{1}{2}, \\frac{1}{2}, \\frac{1}{2})$ —— 12 配位（立方八面体空隙）\n"
            "- B 位（Ti）：$(0, 0, 0)$ —— 6 配位（八面体）\n"
            "- X 位（O）：$(\\frac{1}{2}, 0, 0), (0, \\frac{1}{2}, 0), (0, 0, \\frac{1}{2})$ —— 被 2 个 B 共享\n\n"
            "## Goldschmidt 容差因子\n\n"
            "$$t = \\frac{r_A + r_X}{\\sqrt{2}(r_B + r_X)}$$\n\n"
            "- $t \\approx 1$：理想立方钙钛矿\n"
            "- $0.9 < t < 1$：轻微畸变（四方/正交）\n"
            "- $t < 0.9$ 或 $t > 1$：其他结构类型\n\n"
            "## 畸变与相变\n\n"
            "CaTiO₃ 在室温下并非立方，而是正交畸变（空间群 $Pbnm$，No. 62），"
            "原因是 Ca²⁺ 太小导致 TiO₆ 八面体发生倾斜（octahedral tilting）。\n\n"
            "典型相变序列（降温）：立方 $Pm\\bar{3}m \\to$ 四方 $I4/mcm \\to$ 正交 $Pbnm$\n\n"
            "## 应用\n\n"
            "- BaTiO₃：铁电陶瓷（MLCC 电容器）\n"
            "- MAPbI₃（有机-无机杂化钙钛矿）：太阳能电池效率 > 25%\n"
            "- LSGM：固体氧化物燃料电池电解质"
        ),
        "formulas": [
            "$t = \\frac{r_A + r_X}{\\sqrt{2}(r_B + r_X)}$"
        ],
        "related": ["rock_salt_structure", "space_groups"]
    },
    {
        "id": "wurtzite_structure",
        "title_zh": "纤锌矿型结构",
        "title_en": "Wurtzite Structure",
        "category": "crystal_structures",
        "tags": ["ZnS", "纤锌矿", "B4", "hcp", "GaN", "ZnO", "六方"],
        "difficulty": "中级",
        "source": "Wikipedia + LibreTexts",
        "content": (
            "## 概述\n\n"
            "**纤锌矿型结构**（Wurtzite），Strukturbericht 符号 **B4**。是闪锌矿的六方对应物。"
            "重要的宽禁带半导体 GaN、ZnO、AlN 都采用此结构。\n\n"
            "## 结构特征\n\n"
            "- **原型**：ZnS（六方硫化锌）\n"
            "- **晶系**：六方\n"
            "- **Bravais 点阵**：六方 P\n"
            "- **空间群**：$P6_3mc$（No. 186）\n"
            "- **每惯用胞分子数**：Z = 2\n"
            "- **配位数**：4:4（四面体）\n\n"
            "## 与闪锌矿的关系\n\n"
            "纤锌矿 vs 闪锌矿 = hcp vs fcc 的对应关系：\n"
            "- 闪锌矿：基于 fcc 的 ABCABC 堆垛 → 立方对称\n"
            "- 纤锌矿：基于 hcp 的 ABAB 堆垛 → 六方对称\n"
            "- 两者的最近邻配位完全相同（四面体 4:4），区别在于次近邻\n\n"
            "## 典型材料\n\n"
            "| 材料 | $a$（Å） | $c$（Å） | 带隙（eV） |\n"
            "|------|----------|----------|------------|\n"
            "| GaN | 3.189 | 5.185 | 3.4 |\n"
            "| ZnO | 3.250 | 5.207 | 3.37 |\n"
            "| AlN | 3.112 | 4.982 | 6.2 |\n\n"
            "## 自发极化\n\n"
            "纤锌矿结构缺乏反演中心且 $c/a$ 偏离理想值 $\\sqrt{8/3} \\approx 1.633$，"
            "导致沿 $c$ 轴产生自发极化——这对 GaN 基 HEMT 器件的二维电子气（2DEG）形成至关重要。"
        ),
        "formulas": [],
        "related": ["zinc_blende_structure", "close_packing", "space_groups"]
    },
]

# ============================================================
# 分类 4: 衍射理论
# ============================================================
diffraction = [
    {
        "id": "bragg_law",
        "title_zh": "布拉格定律",
        "title_en": "Bragg's Law",
        "category": "diffraction",
        "tags": ["Bragg定律", "X射线衍射", "干涉", "Bragg角", "晶面间距"],
        "difficulty": "入门",
        "source": "Wikipedia + IUCr Teaching Pamphlets",
        "content": (
            "## 历史\n\n"
            "1912-1913 年，**William Lawrence Bragg** 与其父 William Henry Bragg 提出该定律，"
            "并于 1915 年获诺贝尔物理学奖。Bragg 定律是 X 射线晶体学的基石。\n\n"
            "## 公式\n\n"
            "$$n\\lambda = 2d\\sin\\theta$$\n\n"
            "其中：\n"
            "- $n$：衍射级数（正整数，1, 2, 3, …）\n"
            "- $\\lambda$：入射 X 射线波长\n"
            "- $d$：晶面间距（interplanar spacing）\n"
            "- $\\theta$：Bragg 角（入射束与晶面的夹角）\n\n"
            "## 物理图像\n\n"
            "将晶体看作一组间距为 $d$ 的平行原子面。X 射线在这些面上发生\"反射\"（散射）。\n"
            "相邻面反射的光程差为 $2d\\sin\\theta$。当该程差等于波长的整数倍时，反射波同相叠加——"
            "即发生**相长干涉**（constructive interference）。\n\n"
            "## 推导（几何）\n\n"
            "1. 相邻两束反射线的光程差 = $FG + GH = d\\sin\\theta + d\\sin\\theta = 2d\\sin\\theta$\n"
            "2. 相长干涉条件：$2d\\sin\\theta = n\\lambda$\n"
            "3. 仅在特定角度 $\\theta$ 下满足此条件时出现衍射峰\n\n"
            "## 重要推论\n\n"
            "- 对于已知 $\\lambda$，测量 $\\theta$ 可得 $d$ → 确定晶胞参数\n"
            "- $\\sin\\theta \\leq 1$ → 衍射级数有限，$n\\lambda/(2d) \\leq 1$\n"
            "- 衍射峰位置仅取决于晶格几何（$d$），不依赖于原子种类\n"
            "- Bragg 定律是必要条件而非充分条件——结构因子 $F_{hkl}$ 也必须非零\n\n"
            "## 与倒易空间的关系\n\n"
            "Bragg 条件 $2d\\sin\\theta = \\lambda$ 等价于散射矢量等于倒易点阵矢量："
            "$\\mathbf{Q} = \\mathbf{k}_{散射} - \\mathbf{k}_{入射} = \\mathbf{H}_{hkl}$。"
            "这就是 Ewald 球的几何基础。"
        ),
        "formulas": [
            "$n\\lambda = 2d\\sin\\theta$",
            "$d_{hkl} = \\frac{a}{\\sqrt{h^2 + k^2 + l^2}}$"
        ],
        "related": ["reciprocal_lattice", "ewald_sphere", "structure_factor", "miller_indices"]
    },
    {
        "id": "reciprocal_lattice",
        "title_zh": "倒易点阵",
        "title_en": "Reciprocal Lattice",
        "category": "diffraction",
        "tags": ["倒易点阵", "倒空间", "Fourier变换", "布里渊区", "衍射"],
        "difficulty": "高级",
        "source": "Wikipedia + IUCr International Tables",
        "content": (
            "## 定义\n\n"
            "**倒易点阵**（Reciprocal Lattice）是实空间晶体点阵的 Fourier 变换。它在理解衍射物理中"
            "扮演核心角色——衍射图样本质上是倒易点阵的映射。\n\n"
            "## 数学定义\n\n"
            "给定实空间基矢 $\\mathbf{a}, \\mathbf{b}, \\mathbf{c}$，倒易基矢定义为：\n\n"
            "$$\\mathbf{a}^* = \\frac{\\mathbf{b} \\times \\mathbf{c}}{\\mathbf{a} \\cdot (\\mathbf{b} \\times \\mathbf{c})}$$\n"
            "$$\\mathbf{b}^* = \\frac{\\mathbf{c} \\times \\mathbf{a}}{\\mathbf{b} \\cdot (\\mathbf{c} \\times \\mathbf{a})}$$\n"
            "$$\\mathbf{c}^* = \\frac{\\mathbf{a} \\times \\mathbf{b}}{\\mathbf{c} \\cdot (\\mathbf{a} \\times \\mathbf{b})}$$\n\n"
            "满足正交关系：$\\mathbf{a}_i \\cdot \\mathbf{a}_j^* = \\delta_{ij}$（Kronecker delta）\n\n"
            "## 性质\n\n"
            "1. 倒易点阵的每个点 $(hkl)$ 对应于实空间的一族晶面 $(hkl)$\n"
            "2. 倒易矢量 $\\mathbf{H}_{hkl} = h\\mathbf{a}^* + k\\mathbf{b}^* + l\\mathbf{c}^*$ 垂直于晶面 $(hkl)$\n"
            "3. 倒易矢量的长度 = 晶面间距的倒数：$|\\mathbf{H}_{hkl}| = 1/d_{hkl}$\n"
            "4. 倒易空间中的 Wigner-Seitz 原胞 = 第一 Brillouin 区\n\n"
            "## 为什么叫\"倒易\"？\n\n"
            "- 实空间大 → 倒空间小（$d$ 大 → $|\\mathbf{H}|$ 小）\n"
            "- 实空间小 → 倒空间大（$d$ 小 → $|\\mathbf{H}|$ 大）\n"
            "- 简单立方 → 倒易点阵也是简单立方\n"
            "- fcc → 倒易点阵是 bcc\n"
            "- bcc → 倒易点阵是 fcc\n\n"
            "## 与衍射的关系\n\n"
            "衍射条件（Laue 条件）：散射矢量等于倒易点阵矢量\n"
            "$$\\mathbf{k}' - \\mathbf{k} = \\mathbf{H}_{hkl}$$\n"
            "这意味着衍射斑点直接对应于倒易点阵的各个阵点。"
        ),
        "formulas": [
            "$\\mathbf{a}^* = \\frac{\\mathbf{b} \\times \\mathbf{c}}{\\mathbf{a} \\cdot (\\mathbf{b} \\times \\mathbf{c})}$",
            "$|\\mathbf{H}_{hkl}| = 1/d_{hkl}$",
            "$\\mathbf{k}' - \\mathbf{k} = \\mathbf{H}_{hkl}$"
        ],
        "related": ["bragg_law", "ewald_sphere", "structure_factor", "brillouin_zone"]
    },
    {
        "id": "ewald_sphere",
        "title_zh": "Ewald球构造",
        "title_en": "Ewald Sphere Construction",
        "category": "diffraction",
        "tags": ["Ewald球", "衍射几何", "倒易空间", "Ewald", "衍射条件"],
        "difficulty": "高级",
        "source": "IUCr International Tables + Wikipedia",
        "content": (
            "## 定义\n\n"
            "**Ewald 球**（Ewald Sphere / Ewald Construction），由 Paul Peter Ewald 于 1921 年提出，"
            "是 Bragg 定律在倒易空间中的几何表述。\n\n"
            "## 构造步骤\n\n"
            "1. 画出入射波矢量 $\\mathbf{k}_0$，其长度为 $|\\mathbf{k}_0| = 1/\\lambda$，指向样品\n"
            "2. 以 $\\mathbf{k}_0$ 的起点为球心，$1/\\lambda$ 为半径画球——这就是 Ewald 球\n"
            "3. 将倒易点阵原点放在 $\\mathbf{k}_0$ 的终点（即倒易空间原点在球面上）\n"
            "4. **当某个倒易阵点恰好落在球面上时，衍射发生**\n\n"
            "## 物理含义\n\n"
            "散射矢量 $\\mathbf{Q} = \\mathbf{k}' - \\mathbf{k}_0$ 恰好等于该倒易阵点对应的倒易矢量 $\\mathbf{H}_{hkl}$。\n"
            "此时 Bragg 条件满足：\n"
            "$$|\\mathbf{Q}| = 2\\sin\\theta/\\lambda = 1/d_{hkl}$$\n\n"
            "## 实验应用\n\n"
            "- **单晶衍射**：旋转晶体 = 旋转倒易点阵，使不同倒易阵点依次切割 Ewald 球面\n"
            "- **粉末衍射**：大量随机取向的晶粒 → 倒易阵点在球面上\"涂\"成环 → Debye-Scherrer 环\n"
            "- **TEM 电子衍射**：电子波长极短（0.025 Å @ 200 kV），Ewald 球半径极大，"
            "近似为一个平面 → 可同时看到大量衍射斑点\n\n"
            "## 直观理解\n\n"
            "Ewald 球统一了实空间散射几何与倒空间点阵结构，是理解单晶衍射实验数据采集策略"
            "（如 $\\omega$ 扫描、$\\phi$ 扫描）的关键工具。"
        ),
        "formulas": [
            "$|\\mathbf{Q}| = 2\\sin\\theta/\\lambda = 1/d_{hkl}$",
            "$\\mathbf{Q} = \\mathbf{k}' - \\mathbf{k}_0 = \\mathbf{H}_{hkl}$"
        ],
        "related": ["bragg_law", "reciprocal_lattice", "structure_factor"]
    },
    {
        "id": "structure_factor",
        "title_zh": "结构因子",
        "title_en": "Structure Factor",
        "category": "diffraction",
        "tags": ["结构因子", "Fhkl", "散射因子", "消光", "衍射强度"],
        "difficulty": "高级",
        "source": "IUCr International Tables + Wikipedia",
        "content": (
            "## 定义\n\n"
            "**结构因子** $F_{hkl}$ 描述了晶胞内所有原子的散射对衍射峰 $(hkl)$ 的贡献。"
            "它决定了每个衍射斑点的**强度**。\n\n"
            "## 公式\n\n"
            "$$F_{hkl} = \\sum_{n} f_n \\, e^{2\\pi i (h x_n + k y_n + l z_n)}$$\n\n"
            "其中：\n"
            "- $f_n$：第 $n$ 个原子的原子散射因子（atomic scattering factor / form factor）\n"
            "- $(x_n, y_n, z_n)$：第 $n$ 个原子的分数坐标\n"
            "- 求和遍历晶胞中所有原子\n\n"
            "## 衍射强度\n\n"
            "衍射峰的强度正比于结构因子模的平方：\n"
            "$$I_{hkl} \\propto |F_{hkl}|^2 = F_{hkl} \\cdot F_{hkl}^*$$\n\n"
            "## 系统消光（Systematic Absences）\n\n"
            "某些 $(hkl)$ 的组合使得 $F_{hkl} = 0$，即使满足 Bragg 条件也没有衍射峰——"
            "称为**系统消光**。\n\n"
            "| 点阵类型 | 消光条件 |\n"
            "|----------|----------|\n"
            "| P（简单） | 无消光 |\n"
            "| I（体心） | $h+k+l$ = 奇数 消光 |\n"
            "| F（面心） | $h,k,l$ 奇偶混合 消光 |\n"
            "| C（底心） | $h+k$ = 奇数 消光 |\n\n"
            "## 物理意义\n\n"
            "- Bragg 定律告诉你**峰在哪里**（位置 = $d$ 和晶胞参数）\n"
            "- 结构因子告诉你**峰有多强**（强度 = 原子种类 + 位置）\n"
            "- 两者结合才能通过衍射数据求解晶体结构\n\n"
            "## Friedel 定律\n\n"
            "$$|F_{hkl}|^2 = |F_{\\bar{h}\\bar{k}\\bar{l}}|^2$$\n"
            "衍射图样总是中心对称的，即使晶体本身没有反演中心。这就是为什么 X 射线衍射只能区分 11 种 Laue 类。"
        ),
        "formulas": [
            "$F_{hkl} = \\sum_{n} f_n \\, e^{2\\pi i (h x_n + k y_n + l z_n)}$",
            "$I_{hkl} \\propto |F_{hkl}|^2$"
        ],
        "related": ["bragg_law", "reciprocal_lattice", "space_groups"]
    },
]

# ============================================================
# 分类 5: 缺陷与位错
# ============================================================
defects = [
    {
        "id": "point_defects",
        "title_zh": "点缺陷概述",
        "title_en": "Point Defects Overview",
        "category": "defects",
        "tags": ["点缺陷", "空位", "间隙原子", "置换杂质", "间隙杂质"],
        "difficulty": "入门",
        "source": "Wikipedia + MIT OCW",
        "content": (
            "## 定义\n\n"
            "**点缺陷**（Point Defects）是局限在单个阵点或其附近的零维晶体缺陷。\n\n"
            "## 类型\n\n"
            "| 缺陷类型 | 描述 | 示例 |\n"
            "|----------|------|------|\n"
            "| **空位（Vacancy）** | 原子从其正常阵点缺失 | 所有晶体在有限温度下都有空位 |\n"
            "| **自间隙原子（Self-Interstitial）** | 原子从正常位置位移到间隙中 | 辐照损伤 |\n"
            "| **置换杂质（Substitutional Impurity）** | 外来原子替换宿主原子 | P 代 Si（n 型半导体）|\n"
            "| **间隙杂质（Interstitial Impurity）** | 外来原子进入间隙位置 | C 在 Fe 中（钢的强化）|\n\n"
            "## 空位的热力学\n\n"
            "平衡空位浓度随温度呈指数增长：\n"
            "$$C_v = e^{-E_f/(k_B T)}$$\n\n"
            "- 熔点附近：$C_v \\sim 10^{-4}$（每 10,000 个阵点中有 1 个空位）\n"
            "- 室温：$C_v \\sim 10^{-15}$（几乎无可动空位）\n\n"
            "这就是为什么固态扩散在高温下才显著。\n\n"
            "## 点缺陷的作用\n\n"
            "- **扩散**：空位和间隙原子是原子迁移的载体\n"
            "- **离子电导**：离子晶体中空位迁移 → 离子导电\n"
            "- **颜色**：F 中心（阴离子空位捕获电子）→ 晶体着色\n"
            "- **半导体掺杂**：置换杂质控制载流子类型和浓度"
        ),
        "formulas": [
            "$C_v = e^{-E_f/(k_B T)}$"
        ],
        "related": ["schottky_defect", "frenkel_defect", "edge_dislocation"]
    },
    {
        "id": "schottky_defect",
        "title_zh": "Schottky缺陷",
        "title_en": "Schottky Defect",
        "category": "defects",
        "tags": ["Schottky", "空位对", "离子晶体", "NaCl", "电荷中性"],
        "difficulty": "中级",
        "source": "Wikipedia + Britannica",
        "content": (
            "## 定义\n\n"
            "**Schottky 缺陷**是离子晶体中为保持电荷中性而同时形成的一对**阳离子空位 + 阴离子空位**。\n\n"
            "以 NaCl 为例：一个 Na$^+$ 空位（有效电荷 $-1$）和一个 Cl$^-$ 空位（有效电荷 $+1$）同时出现，"
            "保持整体电中性。\n\n"
            "## 形成条件\n\n"
            "- 阳离子和阴离子半径相近（$r_{阳}/r_{阴} \\approx 1$）\n"
            "- 典型材料：NaCl, KCl, KBr, MgO\n"
            "- 形成能：通常 2-3 eV/缺陷对\n\n"
            "## 平衡浓度\n\n"
            "$$n_s \\propto e^{-E_s/(2k_BT)}$$\n\n"
            "其中 $E_s$ 是形成一个 Schottky 对（两个空位）的总能量，因子 2 来自两种空位的平衡。\n\n"
            "## 与 Frenkel 缺陷的比较\n\n"
            "| 特征 | Schottky | Frenkel |\n"
            "|------|----------|--------|\n"
            "| 涉及离子 | 阳离子 + 阴离子 | 仅一种离子（通常阳离子）|\n"
            "| 位置 | 两个空位（表面/晶界） | 一个空位 + 一个间隙 |\n"
            "| 体积变化 | 晶体体积膨胀 | 体积基本不变 |\n"
            "| 典型材料 | NaCl, KCl, MgO | AgCl, AgBr, CaF₂ |"
        ),
        "formulas": [
            "$n_s \\propto e^{-E_s/(2k_BT)}$"
        ],
        "related": ["frenkel_defect", "point_defects"]
    },
    {
        "id": "frenkel_defect",
        "title_zh": "Frenkel缺陷",
        "title_en": "Frenkel Defect",
        "category": "defects",
        "tags": ["Frenkel", "空位-间隙对", "AgCl", "离子晶体"],
        "difficulty": "中级",
        "source": "Wikipedia + Britannica",
        "content": (
            "## 定义\n\n"
            "**Frenkel 缺陷**是离子晶体中一个离子（通常为较小的阳离子）离开其正常阵点进入间隙位置，"
            "同时留下一个空位的缺陷组合。\n\n"
            "## 电荷守恒\n\n"
            "Frenkel 缺陷自动保持电荷中性：阳离子空位（有效负电荷）+ 阳离子间隙（有效正电荷）= 净电荷为零。\n\n"
            "## 形成条件\n\n"
            "- 阳离子远小于阴离子（$r_{阳} \\ll r_{阴}$），容易进入间隙\n"
            "- 典型材料：\n"
            "  - AgCl, AgBr（Ag$^+$ 很小，容易进入间隙）\n"
            "  - CaF₂, SrF₂, BaF₂（萤石结构，F$^-$ 进入间隙 → 反 Frenkel）\n\n"
            "## 平衡浓度\n\n"
            "$$n_f \\propto e^{-E_f/(2k_BT)}$$\n\n"
            "## 与 Schottky 的能量竞争\n\n"
            "晶体选择 Schottky 还是 Frenkel 取决于哪种方式的形成能更低：\n"
            "- Schottky：需要同时在表面形成两个空位，体积膨胀\n"
            "- Frenkel：需要一个空位 + 一个间隙，对晶体体积影响小\n"
            "- 在 NaCl 中，Schottky 形成能（~2.3 eV）< Frenkel 形成能（~3 eV）→ Schottky 主导"
        ),
        "formulas": [
            "$n_f \\propto e^{-E_f/(2k_BT)}$"
        ],
        "related": ["schottky_defect", "point_defects"]
    },
    {
        "id": "dislocations",
        "title_zh": "位错（线缺陷）",
        "title_en": "Dislocations (Line Defects)",
        "category": "defects",
        "tags": ["位错", "刃位错", "螺位错", "Burgers矢量", "滑移", "塑性变形"],
        "difficulty": "中级",
        "source": "Wikipedia + MIT OCW",
        "content": (
            "## 定义\n\n"
            "**位错**（Dislocation）是一维线缺陷，是晶体中沿某条线原子排列异常的线状区域。"
            "位错是晶体塑性变形的微观载体。\n\n"
            "## Burgers 矢量\n\n"
            "位错的特征量是 **Burgers 矢量** $\\mathbf{b}$，通过绕位错线作 Burgers 回路得到。\n"
            "$\\mathbf{b}$ 的大小和方向决定了位错的类型和强度。\n\n"
            "## 刃位错（Edge Dislocation）\n\n"
            "- $\\mathbf{b} \\perp$ 位错线\n"
            "- 形象类比：在书中夹入半页纸——纸边就是位错线\n"
            "- 有压应力区和拉应力区\n"
            "- 杂质原子偏聚到应力区 → 固溶强化\n"
            "- 符号：$\\perp$（正刃位错）、$\\top$（负刃位错）\n\n"
            "## 螺位错（Screw Dislocation）\n\n"
            "- $\\mathbf{b} \\parallel$ 位错线\n"
            "- 形象类比：将晶体沿一个面切开，然后平行于切口方向剪切位移一个 Burgers 矢量\n"
            "- 晶体表面形成螺旋台阶 → 晶体生长的优先位点\n"
            "- 解释了为什么晶体可以在远低于理论强度的过饱和度下生长\n\n"
            "## 混合位错\n\n"
            "大多数真实位错兼有刃型和螺型分量，$\\mathbf{b}$ 与位错线的夹角在 0° 到 90° 之间。\n\n"
            "## 位错密度\n\n"
            "- 充分退火的金属：$\\sim 10^6$ cm$^{-2}$\n"
            "- 严重冷加工的金属：$\\sim 10^{12}$ cm$^{-2}$\n\n"
            "## 位错与力学性能\n\n"
            "位错既可以**减弱**晶体强度（通过滑移使晶体变形），也可以**增强**晶体强度"
            "（位错间的缠结导致加工硬化）。这看似矛盾的双重角色是理解所有金属力学行为的核心。"
        ),
        "formulas": [],
        "related": ["point_defects", "grain_boundaries"]
    },
]

# ============================================================
# 分类 6: 电子性质
# ============================================================
electronic = [
    {
        "id": "brillouin_zone",
        "title_zh": "Brillouin区",
        "title_en": "Brillouin Zone",
        "category": "electronic_properties",
        "tags": ["Brillouin区", "倒空间", "Wigner-Seitz", "能带", "Bloch波"],
        "difficulty": "高级",
        "source": "Wikipedia + IUCr",
        "content": (
            "## 定义\n\n"
            "**Brillouin 区**（Brillouin Zone）是倒空间中定义为倒易点阵的 Wigner-Seitz 原胞的区域。"
            "它包含了晶体中电子波函数所有物理上不等价的波矢 $\\mathbf{k}$。\n\n"
            "## 第一 Brillouin 区\n\n"
            "第一 Brillouin 区是距离倒易点阵原点（$\\Gamma$ 点）比任何其他倒易阵点更近的"
            "所有 $\\mathbf{k}$ 点的集合。其边界由 Bragg 面（垂直于倒易矢量的中垂面）构成。\n\n"
            "## 高对称点（立方晶系的常用符号）\n\n"
            "| 符号 | 位置（fcc 倒空间 = bcc 型） | 坐标（以 $2\\pi/a$ 为单位） |\n"
            "|------|---------------------------|---------------------------|\n"
            "| $\\Gamma$ | Brillouin 区中心 | $(0, 0, 0)$ |\n"
            "| $X$ | $[100]$ 方向与区边界交点 | $(1, 0, 0)$ |\n"
            "| $L$ | $[111]$ 方向与区边界交点 | $(\\frac{1}{2}, \\frac{1}{2}, \\frac{1}{2})$ |\n"
            "| $K$ | $[110]$ 方向与区边界交点 | $(\\frac{3}{4}, \\frac{3}{4}, 0)$ |\n"
            "| $W$ | $X$ 和 $K$ 之间的边界点 | $(1, \\frac{1}{2}, 0)$ |\n\n"
            "## 物理意义\n\n"
            "- Bloch 定理：晶体中的电子波函数由波矢 $\\mathbf{k}$（在第一 Brillouin 区内）和能带指数 $n$ 标记\n"
            "- 能带在 Brillouin 区边界处分裂 → 带隙\n"
            "- 自由电子抛物面 $E = \\hbar^2 k^2/(2m)$ 在 Brillouin 区边界处被 Bragg 反射 → 能隙打开\n"
            "- 半导体的价带顶和导带底在 Brillouin 区中的相对位置（$\\Gamma$ 点 vs X 点 vs L 点）"
            "决定其是直接带隙还是间接带隙半导体"
        ),
        "formulas": [],
        "related": ["reciprocal_lattice", "band_theory", "bloch_theorem"]
    },
    {
        "id": "band_theory",
        "title_zh": "能带理论",
        "title_en": "Band Theory of Solids",
        "category": "electronic_properties",
        "tags": ["能带", "价带", "导带", "带隙", "金属", "半导体", "绝缘体"],
        "difficulty": "中级",
        "source": "Wikipedia + LibreTexts",
        "content": (
            "## 起源\n\n"
            "**能带理论**解释了为什么一些固体是金属、一些是半导体、一些是绝缘体。"
            "它从 Bloch 定理出发，描述电子在周期性晶格势场中的能量本征态。\n\n"
            "## 核心物理\n\n"
            "当 $N$ 个原子聚集成晶体时，每个原子能级分裂为 $N$ 个能级，形成**能带**（Energy Band）。\n"
            "允许电子占据的能带之间可能被**带隙**（Band Gap / Forbidden Gap）分隔。\n\n"
            "## 金属 vs 半导体 vs 绝缘体\n\n"
            "| 类型 | 带隙 $E_g$ | 电阻率（室温） | 示例 |\n"
            "|------|-----------|---------------|------|\n"
            "| 金属 | 无（价带部分填充） | $\\sim 10^{-8}$ Ω·m | Cu, Al, Fe |\n"
            "| 半导体 | $0 < E_g < 4$ eV | $10^{-4} \\sim 10^{7}$ Ω·m | Si (1.12 eV), GaAs (1.43 eV) |\n"
            "| 绝缘体 | $E_g > 4$ eV | $> 10^{10}$ Ω·m | 金刚石 (5.47 eV), SiO₂ |\n\n"
            "## 直接 vs 间接带隙\n\n"
            "- **直接带隙**：导带底和价带顶在同一 $\\mathbf{k}$ 点（如 GaAs 在 $\\Gamma$ 点）\n"
            "  → 电子可直接跃迁发光，适合 LED/激光器\n"
            "- **间接带隙**：导带底和价带顶在不同 $\\mathbf{k}$ 点（如 Si：价带顶在 $\\Gamma$，导带底在 $X$ 点附近）\n"
            "  → 跃迁需要声子参与，发光效率极低\n\n"
            "## 有效质量\n\n"
            "能带曲率决定载流子的有效质量：\n"
            "$$\\frac{1}{m^*} = \\frac{1}{\\hbar^2} \\frac{\\partial^2 E}{\\partial k^2}$$\n\n"
            "窄带（$d$ 轨道）→ 曲率大 → 有效质量大（\"重\"电子）；宽带（$s,p$ 轨道）→ 曲率小 → 有效质量小（\"轻\"电子）。"
        ),
        "formulas": [
            "$\\frac{1}{m^*} = \\frac{1}{\\hbar^2} \\frac{\\partial^2 E}{\\partial k^2}$"
        ],
        "related": ["brillouin_zone", "bloch_theorem", "density_of_states"]
    },
    {
        "id": "bloch_theorem",
        "title_zh": "Bloch定理",
        "title_en": "Bloch's Theorem",
        "category": "electronic_properties",
        "tags": ["Bloch定理", "Bloch波", "周期势", "晶体电子", "Floquet理论"],
        "difficulty": "高级",
        "source": "Wikipedia + IUCr",
        "content": (
            "## 陈述\n\n"
            "**Bloch 定理**（1928年，Felix Bloch）是固体物理中最重要的定理之一。它指出：\n\n"
            "在周期性势场 $V(\\mathbf{r} + \\mathbf{R}) = V(\\mathbf{r})$ 中（$\\mathbf{R}$ 为任意点阵矢量），"
            "单电子 Schrödinger 方程的本征函数具有如下形式：\n\n"
            "$$\\psi_{n\\mathbf{k}}(\\mathbf{r}) = e^{i\\mathbf{k} \\cdot \\mathbf{r}} u_{n\\mathbf{k}}(\\mathbf{r})$$\n\n"
            "其中 $u_{n\\mathbf{k}}(\\mathbf{r})$ 具有晶格的周期性：$u_{n\\mathbf{k}}(\\mathbf{r} + \\mathbf{R}) = u_{n\\mathbf{k}}(\\mathbf{r})$。\n\n"
            "## 核心含义\n\n"
            "Bloch 波 = 平面波 $\\times$ 周期性调幅函数：\n"
            "- 电子在晶体中并非像自由电子一样是纯平面波\n"
            "- 但也不是完全局域在某原子周围\n"
            "- 它是在自由传播的基础上被原子核的周期性所\"调制\"\n\n"
            "## 推论\n\n"
            "1. $\\mathbf{k}$ 限制在第一 Brillouin 区内（周期性边界条件）\n"
            "2. 对于每个 $\\mathbf{k}$，能量 $E_n(\\mathbf{k})$ 形成能带结构\n"
            "3. $E_n(\\mathbf{k})$ 是 $\\mathbf{k}$ 的周期函数：$E_n(\\mathbf{k} + \\mathbf{G}) = E_n(\\mathbf{k})$（$\\mathbf{G}$ 为倒易矢量）\n\n"
            "## 为什么 Bloch 定理如此重要？\n\n"
            "它将一个原本在 $\\sim 10^{23}$ 个原子尺度上不可解的量子力学问题，"
            "简化为在一个晶胞（几个原子）内求解，然后通过 $\\mathbf{k}$ 遍历 Brillouin 区得到整个晶体的所有电子态。"
        ),
        "formulas": [
            "$\\psi_{n\\mathbf{k}}(\\mathbf{r}) = e^{i\\mathbf{k} \\cdot \\mathbf{r}} u_{n\\mathbf{k}}(\\mathbf{r})$",
            "$E_n(\\mathbf{k} + \\mathbf{G}) = E_n(\\mathbf{k})$"
        ],
        "related": ["band_theory", "brillouin_zone", "density_of_states"]
    },
]

# ============================================================
# 分类 7: 材料数据
# ============================================================
material_data = [
    {
        "id": "material_silicon",
        "title_zh": "硅 (Si)",
        "title_en": "Silicon",
        "category": "material_data",
        "tags": ["Si", "硅", "半导体", "金刚石结构", "Fd-3m", "间接带隙"],
        "difficulty": "入门",
        "source": "Materials Project + Wikipedia",
        "content": (
            "| 属性 | 数值 |\n"
            "|------|------|\n"
            "| **化学式** | Si |\n"
            "| **晶系** | 立方 |\n"
            "| **空间群** | $Fd\\bar{3}m$（No. 227） |\n"
            "| **结构类型** | 金刚石型 |\n"
            "| **晶格常数** | $a = 5.431 \\mathring{A}$ |\n"
            "| **密度** | 2.33 g/cm³ |\n"
            "| **带隙** | 1.12 eV（间接） |\n"
            "| **配位数** | 4（$sp^3$ 四面体） |\n"
            "| **熔点** | 1414 °C |\n"
            "| **应用** | 集成电路、太阳能电池、MEMS |\n\n"
            "硅是地球上最丰富的半导体元素，构成了现代微电子工业的基础。"
            "其间接带隙性质使得它不适合做高效发光器件，但非常适合做晶体管和光伏器件。"
        ),
        "formulas": [],
        "related": ["diamond_structure", "band_theory"]
    },
    {
        "id": "material_gaas",
        "title_zh": "砷化镓 (GaAs)",
        "title_en": "Gallium Arsenide",
        "category": "material_data",
        "tags": ["GaAs", "砷化镓", "闪锌矿", "III-V族", "直接带隙", "光电子"],
        "difficulty": "中级",
        "source": "Materials Project + Wikipedia",
        "content": (
            "| 属性 | 数值 |\n"
            "|------|------|\n"
            "| **化学式** | GaAs |\n"
            "| **晶系** | 立方 |\n"
            "| **空间群** | $F\\bar{4}3m$（No. 216） |\n"
            "| **结构类型** | 闪锌矿型 |\n"
            "| **晶格常数** | $a = 5.653 \\mathring{A}$ |\n"
            "| **密度** | 5.32 g/cm³ |\n"
            "| **带隙** | 1.43 eV（**直接**） |\n"
            "| **电子迁移率** | 8500 cm²/(V·s)（远高于 Si 的 1350） |\n"
            "| **熔点** | 1238 °C |\n"
            "| **应用** | LED、激光器、高速晶体管、光伏 |\n\n"
            "GaAs 是继 Si 之后最重要的半导体。其直接带隙和高的电子迁移率使其在光电子和射频领域不可替代。"
            "与 Si 不同，GaAs 晶体缺乏反演中心，因此具有压电性。"
        ),
        "formulas": [],
        "related": ["zinc_blende_structure", "band_theory"]
    },
    {
        "id": "material_nacl",
        "title_zh": "氯化钠 (NaCl)",
        "title_en": "Sodium Chloride",
        "category": "material_data",
        "tags": ["NaCl", "氯化钠", "岩盐", "B1", "离子晶体", "Fm-3m"],
        "difficulty": "入门",
        "source": "Materials Project + Wikipedia",
        "content": (
            "| 属性 | 数值 |\n"
            "|------|------|\n"
            "| **化学式** | NaCl |\n"
            "| **晶系** | 立方 |\n"
            "| **空间群** | $Fm\\bar{3}m$（No. 225） |\n"
            "| **结构类型** | 岩盐型（B1） |\n"
            "| **晶格常数** | $a = 5.64 \\mathring{A}$ |\n"
            "| **密度** | 2.17 g/cm³ |\n"
            "| **配位数** | 6:6（八面体） |\n"
            "| **熔点** | 801 °C |\n"
            "| **带隙** | $\\sim 8.5$ eV（绝缘体） |\n"
            "| **解理面** | $\\{100\\}$ |\n\n"
            "NaCl 是离子晶体中最重要的结构原型。其 $Fm\\bar{3}m$ 空间群是所有 B1 型结构（碱金属卤化物、"
            "碱土金属氧化物）的共同特征。NaCl 沿 $\\{100\\}$ 面容易解理，因为该面的表面能最低。"
        ),
        "formulas": [],
        "related": ["rock_salt_structure", "schottky_defect"]
    },
    {
        "id": "material_diamond",
        "title_zh": "金刚石 (C)",
        "title_en": "Diamond (Carbon)",
        "category": "material_data",
        "tags": ["C", "金刚石", "A4", "超硬材料", "宽禁带", "sp3"],
        "difficulty": "入门",
        "source": "Materials Project + Wikipedia",
        "content": (
            "| 属性 | 数值 |\n"
            "|------|------|\n"
            "| **化学式** | C（碳的同素异形体） |\n"
            "| **晶系** | 立方 |\n"
            "| **空间群** | $Fd\\bar{3}m$（No. 227） |\n"
            "| **结构类型** | 金刚石型（A4） |\n"
            "| **晶格常数** | $a = 3.567 \\mathring{A}$ |\n"
            "| **密度** | 3.52 g/cm³ |\n"
            "| **C-C 键长** | 1.544 Å |\n"
            "| **键角** | 109.5°（正四面体） |\n"
            "| **带隙** | 5.47 eV（绝缘体） |\n"
            "| **硬度** | 莫氏 10（自然界最硬） |\n"
            "| **热导率** | 2200 W/(m·K)（所有材料中最高） |\n\n"
            "金刚石是碳在高压下的热力学稳定相。其极高的硬度和热导率源于强的 $sp^3$ 共价键网络"
            "和轻的原子质量（高 Debye 频率）。金刚石也是宽禁带半导体的代表，在高压功率电子学中有应用前景。"
        ),
        "formulas": [],
        "related": ["diamond_structure", "band_theory"]
    },
    {
        "id": "material_perovskite",
        "title_zh": "钛酸钙 (CaTiO₃)",
        "title_en": "Calcium Titanate",
        "category": "material_data",
        "tags": ["CaTiO3", "钛酸钙", "钙钛矿", "Pbnm", "正交"],
        "difficulty": "中级",
        "source": "Materials Project + Wikipedia",
        "content": (
            "| 属性 | 数值 |\n"
            "|------|------|\n"
            "| **化学式** | CaTiO₃ |\n"
            "| **晶系** | 正交（室温） |\n"
            "| **空间群** | $Pbnm$（No. 62，室温相） |\n"
            "| **结构类型** | 钙钛矿型（畸变） |\n"
            "| **晶格常数（室温）** | $a = 5.38 \\mathring{A}$, $b = 5.44 \\mathring{A}$, $c = 7.64 \\mathring{A}$ |\n"
            "| **高温立方相** | $Pm\\bar{3}m$（No. 221），$a \\approx 3.84 \\mathring{A}$ |\n"
            "| **密度** | 4.10 g/cm³ |\n"
            "| **带隙** | $\\sim 3.5$ eV |\n"
            "| **应用** | 微波介质陶瓷、铁电材料原型结构 |\n\n"
            "CaTiO₃ 是钙钛矿家族的命名来源（矿物名：perovskite）。虽然室温下 CaTiO₃ 本身为畸变的正交相，"
            "但其理想立方结构（$Pm\\bar{3}m$）是所有钙钛矿类材料——包括 BaTiO₃（铁电体）、"
            "MAPbI₃（光伏）——的共同 aristotype。"
        ),
        "formulas": [],
        "related": ["perovskite_structure", "space_groups"]
    },
]

# ============================================================
# 合并所有条目
# ============================================================
all_entries = {
    "crystal_basics": crystal_basics,
    "symmetry": symmetry,
    "crystal_structures": crystal_structures,
    "diffraction": diffraction,
    "defects": defects,
    "electronic_properties": electronic,
    "material_data": material_data,
}

# ============================================================
# 保存为分类 JSON 文件
# ============================================================
def build_kb():
    os.makedirs(CATEGORIES_DIR, exist_ok=True)

    total_entries = 0
    for cat_name, entries in all_entries.items():
        filepath = os.path.join(CATEGORIES_DIR, f"{cat_name}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
        total_entries += len(entries)
        print(f"  [{cat_name}] {len(entries)} entries -> {filepath}")

    # 生成索引文件
    index = {}
    for cat_name, entries in all_entries.items():
        for entry in entries:
            index[entry["id"]] = {
                "title_zh": entry["title_zh"],
                "title_en": entry["title_en"],
                "category": entry["category"],
                "tags": entry["tags"],
                "difficulty": entry["difficulty"],
                "file": f"categories/{cat_name}.json"
            }

    index_path = os.path.join(KB_DIR, "kb_index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"\n  Total: {total_entries} entries")
    print(f"  Index: {index_path}")
    return total_entries

if __name__ == "__main__":
    build_kb()
