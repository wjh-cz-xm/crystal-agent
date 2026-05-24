# 晶体智能助手 — 实施计划书

> **项目路径**: `D:\projects\Crystal agent project 2.0`
> **最后更新**: 2026-05-24
> **当前阶段**: Phase 5 已完成，项目可交付

---

## 零、项目总览

### 技术栈速查

| 层 | 技术 |
|---|---|
| 前端 | HTML5 + CSS3 + Vanilla JS, 3Dmol.js 1.8, marked.js, KaTeX |
| 后端 | Python 3.10+, FastAPI, Pymatgen, CrystalNN |
| 通信 | WebSocket（单一通道，JSON 消息协议） |
| LLM | DeepSeek API (`deepseek-v4-flash`, 非流式, `thinking: {type: "enabled"}`) |
| 工具 | SerpAPI, Materials Project API, 本地知识库(关键词), CIF 文件缓存 |
| 静态服务 | FastAPI 直接 serve `frontend/` |

### 关键设计决策（已确认）

- 思维链内容不展示，仅提取为状态摘要（"正在分析…"）
- 知识库维持关键词匹配，不升级向量检索
- 系统提示词后续迭代，Phase 3 先用初稿
- API Key 均具备：`DEEPSEEK_API_KEY`, `MP_API_KEY`, `SERPAPI_API_KEY`

---

## 一、分阶段总览

```
Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5
骨架      晶体查看器   LLM Agent   工具实现    联调上线
```

| 阶段 | 主题 | 可验收成果 | 预估文件数 |
|---|---|---|---|
| Phase 1 | 骨架搭建 | 蓝白布局 + WebSocket 连通 | 6 |
| Phase 2 | 晶体查看器 | 3D 渲染 + 全部交互按钮 | +3 |
| Phase 3 | LLM Agent | 聊天 + 工具调用循环 | +4 |
| Phase 4 | 工具实现 | MP-API / 知识库 / 搜索 / CIF库 | +4 |
| Phase 5 | 联调上线 | 端到端打通 + CIF 缓存填充 | 收尾 |

**每完成一个 Phase，均得到一个可独立运行、可演示验收的中间版本。**

---

## 二、Phase 1 — 骨架搭建

### 目标
浏览器打开后看到蓝白科技风分栏布局（左2/3 晶体区 + 右1/3 聊天区），WebSocket 连通，控制台可收发消息。

### 2.1 前置条件
- Python 3.10+ 已安装
- 项目目录存在：`D:\projects\Crystal agent project 2.0`

### 2.2 将创建的文件

```
frontend/
├── index.html
├── css/
│   └── style.css
└── js/
    └── app.js
backend/
├── config.py
├── websocket_manager.py
└── main.py
```

### 2.3 实施步骤

#### Step 1: 后端配置 `backend/config.py`
- 定义 `HOST`, `PORT`（默认 `localhost:8000`）
- 从环境变量读取 `DEEPSEEK_API_KEY`, `MP_API_KEY`, `SERPAPI_API_KEY`
- 定义路径常量：`PROJECT_ROOT`, `FRONTEND_DIR`, `CIF_CACHE_DIR`

#### Step 2: WebSocket 管理器 `backend/websocket_manager.py`
- `ConnectionManager` 类：管理活跃连接（`set[WebSocket]`）
- `connect(ws)` / `disconnect(ws)` / `broadcast(message: dict)`
- `send_personal(message: dict, ws)` 单播

#### Step 3: FastAPI 入口 `backend/main.py`
- `@app.get("/")` → 重定向到 `/index.html`
- `app.mount("/", StaticFiles(directory=FRONTEND_DIR))` serve 前端
- `@app.websocket("/ws")` 端点：
  - 接受连接 → `manager.connect(ws)`
  - 收到 `user_message` → 回显（后续 Phase 接 LLM）
  - 收到 `new_conversation` → 确认重置
  - 断开 → `manager.disconnect(ws)`
- 启动时检查 API Key 是否设置，打印警告

#### Step 4: 前端 HTML `frontend/index.html`
- 引入：3Dmol.js CDN, marked.js CDN, KaTeX CDN (CSS + JS + auto-render)
- 引入：`css/style.css`, `js/app.js`（type="module"）
- 布局结构：
  ```
  ┌─────────────────────────┐
  │  header (标题栏)         │
  ├─────────────────────┬───┤
  │ crystal-viewer      │聊 │
  │ (左面板)            │天 │  ← 分隔线可拖动
  │                     │框 │
  ├─────────────────────┴───┤
  │  footer (状态栏)         │
  └─────────────────────────┘
  ```
- 左面板 ID: `crystal-viewer`
- 右面板 ID: `chat-panel`
- 分隔线 ID: `divider`（宽 4px, cursor: col-resize）

#### Step 5: 前端样式 `frontend/css/style.css`
- 配色方案：
  - 主背景：`#0a1628`（深蓝黑）
  - 面板背景：`#0d1f3c`（深蓝）
  - 强调色：`#1e90ff`（道奇蓝）
  - 文字：`#e0e8f0`（浅蓝灰）
  - 高亮/边框：`#4da6ff`
- 字体：系统默认中文字体栈（`"Microsoft YaHei", "PingFang SC", sans-serif`）
- 分隔线拖动：hover 变色，mousedown 开始拖拽
- 聊天框消息气泡样式（预置，Phase 3 用）

#### Step 6: 前端主逻辑 `frontend/js/app.js`
- WebSocket 连接 `ws://localhost:8000/ws`
- 分隔线拖动逻辑（mousedown/mousemove/mouseup）
- 基础消息收发：`sendMessage(type, payload)` 封装
- 接收消息按 `type` 分派（预置 switch，后续 Phase 填充）

### 2.4 验收清单

- [ ] `python backend/main.py` 启动，无报错
- [ ] 浏览器打开 `http://localhost:8000`，看到蓝白分栏布局
- [ ] 拖动分隔线，左右面板比例随之调整
- [ ] 浏览器控制台显示 WebSocket 连接成功
- [ ] 在聊天框输入文字回车，控制台能看到发出的消息
- [ ] 后端终端打印收到的消息

### 2.5 完成后文件状态

```
D:\projects\Crystal agent project 2.0\
├── frontend/
│   ├── index.html          ✓
│   ├── css/style.css       ✓
│   └── js/app.js           ✓
├── backend/
│   ├── main.py             ✓
│   ├── config.py           ✓
│   └── websocket_manager.py ✓
├── knowledge_base/         (已有)
├── Brainstorm.md
└── IMPLEMENTATION_PLAN.md  (本文件)
```

---

## 三、Phase 2 — 晶体查看器

### 目标
左侧 3D 区域完整可用：能渲染 CIF、所有按钮/选项卡/勾选项工作、后端 Pymatgen 处理超胞和晶胞转换。

### 3.1 前置条件
- Phase 1 全部完成
- `pip install pymatgen`（Pymatgen 已安装）
- 以下文件存在：`backend/main.py`, `backend/config.py`, `backend/websocket_manager.py`, `frontend/index.html`, `frontend/css/style.css`, `frontend/js/app.js`

### 3.2 将创建/修改的文件

```
新增:
frontend/js/crystal-viewer.js    # 3Dmol.js 完整封装
backend/crystal_service.py       # Pymatgen 晶体处理服务

修改:
frontend/index.html              # 添加左侧面板 UI 控件
frontend/css/style.css           # 查看器控件样式
frontend/js/app.js               # 添加 WebSocket 消息处理
backend/main.py                  # 添加 viewer_action 处理
```

### 3.3 实施步骤

#### Step 1: 后端晶体处理 `backend/crystal_service.py`
函数清单（纯计算，无状态）：
- `parse_cif_to_structure(cif_data: str) → Structure`：CIF 文本 → Pymatgen Structure
- `structure_to_cif(structure: Structure) → str`：Structure → CIF 文本（返回给前端）
- `get_primitive_cell(cif_data: str) → str`：转原胞，返回 CIF
- `get_conventional_cell(cif_data: str) → str`：转惯用胞，返回 CIF
- `build_supercell(cif_data: str, matrix: tuple) → str`：构建超胞，返回 CIF
  - 若原胞原子数 > 50 → 拒绝
- `compute_bonds(cif_data: str) → dict`：CrystalNN 计算键连，返回 `{pairs: [[i,j],...], orders: [...]}`
- `extract_elements(cif_data: str) → list[str]`：提取元素列表
- `extract_formula_and_symmetry(cif_data: str) → dict`：提取化学式、空间群等

#### Step 2: 前端晶体查看器 `frontend/js/crystal-viewer.js`
`CrystalViewer` 类：
- `init(containerId)`：在指定元素中创建 3Dmol  viewer
  - 背景色 `0x0d1f3c`（与面板一致）
  - 默认视角
- `loadCif(cifData, mpId, label)`：
  - 调用 `viewer.addModel(cifData, "cif")`
  - 原子样式：`{radius: 0.5, colorscheme: "Jmol"}`
  - 显示化学式 + MP-ID 标签于左上角
  - 默认显示晶胞框线
  - 自动缩放到合适视角
- `resetView()`：视角和大小回正
- `setUnitCellType(type)`：触发后端请求，切换 primitive/conventional
- `setSupercell(size)`：触发后端请求，构建超胞
- `toggleAtoms(element, show)`：单独显隐某元素
- `toggleBonds(show)`：显隐键连
- `toggleUnitCell(show)`：显隐晶胞框线
- `togglePeriodicBoundaries(show)`：`set {replicateUnitCell: "2,2,2"}` 或清除
- `toggleOutsideAtoms(show)`：对应 3Dmol 选项

3Dmol.js 关键 API 速查：
- `viewer.addModel(cif, "cif")` 载入结构
- `viewer.setStyle({}, {stick: {radius: 0.5, colorscheme: "Jmol"}})` 原子样式
- `viewer.addUnitCell` 晶胞框线
- `viewer.zoomTo()` 自动缩放
- `viewer.spin(false)` 停转
- `viewer.setStyle({elem: "Si"}, {stick: {hidden: true}})` 显隐

#### Step 3: 更新前端 HTML `frontend/index.html`
左侧面板增加：
- 左上角：`<div id="structure-label">` 化学式 + MP-ID
- 左侧工具栏（垂直排列，绝对定位在查看器左侧）：
  - 🔄 刷新按钮 `id="btn-reset"`
  - 晶胞形式下拉：`<select id="cell-type">` (Primitive / Conventional)
  - 超胞下拉：`<select id="supercell-size">` (1×1×1 / 2×2×2)
  - 显隐控制复选框组：
    - 原子 → 子列表（动态生成元素复选框）
    - 键连
    - 晶胞框线
    - 配位多面体（disabled, 置灰）
  - 其他选项：
    - "Draw repeats of atoms on periodic boundaries"（默认勾选）
    - "Draw atoms outside unit cell bonded to atoms within unit cell"（默认勾选）
- 查看器容器：`<div id="crystal-viewer-3d">`（占满剩余空间）

#### Step 4: 更新 WebSocket 消息处理
后端 `main.py` 新增 `viewer_action` 处理：
- `{action: "switch_cell", cell_type: "primitive"|"conventional"}` → `crystal_service` 处理 → 返回新 CIF
- `{action: "build_supercell", size: [2,2,2]}` → 检查原子数 → 返回新 CIF
- `{action: "compute_bonds"}` → CrystalNN → 返回键连数据

前端 `app.js` 新增消息处理：
- `render_structure` → 调用 `crystalViewer.loadCif()`
- `viewer_config` → 更新查看器配置

#### Step 5: 测试用 CIF
在 `backend/crystal_service.py` 中硬编码一段 Si (mp-149) 的 CIF 用于开发测试。
启动时自动将测试 CIF 渲染到前端。

### 3.4 验收清单

- [ ] 页面打开后左侧自动渲染 Si 晶体结构
- [ ] 左上角显示 "Si（单晶硅）mp-149"
- [ ] 鼠标滚轮缩放，鼠标拖动旋转视角
- [ ] 点刷新按钮，视角回到默认
- [ ] 切换 Primitive/Conventional cell，结构更新
- [ ] 构建 2×2×2 超胞，原子正确重复排列
- [ ] 各元素单独显隐有效
- [ ] 键连可开关
- [ ] 晶胞框线可开关
- [ ] 两个 "Draw repeats…" 选项可切换
- [ ] 配位多面体选项置灰不生效

### 3.5 完成后文件状态

```
D:\projects\Crystal agent project 2.0\
├── frontend/
│   ├── index.html              (修改)
│   ├── css/style.css           (修改)
│   └── js/
│       ├── app.js              (修改)
│       └── crystal-viewer.js   ✓ 新增
├── backend/
│   ├── main.py                 (修改)
│   ├── config.py
│   ├── websocket_manager.py
│   └── crystal_service.py      ✓ 新增
├── knowledge_base/
├── Brainstorm.md
└── IMPLEMENTATION_PLAN.md
```

---

## 四、Phase 3 — LLM Agent

### 目标
聊天框完整可用：消息流显示、Markdown+LaTeX 渲染、DeepSeek 思考模式打通、工具调用循环、系统消息展示。

### 4.1 前置条件
- Phase 1 + Phase 2 全部完成
- `pip install openai`（DeepSeek API 兼容 OpenAI SDK）
- 环境变量 `DEEPSEEK_API_KEY` 已设置
- 以下文件存在：Phase 2 全部文件

### 4.2 将创建/修改的文件

```
新增:
backend/llm/__init__.py
backend/llm/agent.py             # DeepSeek agent 循环
backend/llm/tool_registry.py     # 工具注册中心
backend/llm/system_prompt.md     # 系统提示词（从根目录复制或直接引用）

修改:
backend/main.py                  # 接入 agent 处理 user_message
backend/config.py                # 增加 LLM 相关配置
frontend/js/app.js               # 完整聊天消息处理
frontend/js/chat.js              (新增) 聊天框 UI 逻辑
frontend/index.html              # 聊天框 UI 完善
frontend/css/style.css           # 聊天框样式完善
```

### 4.3 实施步骤

#### Step 1: 工具注册中心 `backend/llm/tool_registry.py`
- `ToolRegistry` 类：
  - `register(name, description, parameters_schema, handler_func)`
  - `get_tools_schema() → list[dict]`：返回 OpenAI 兼容的 tools 数组
  - `execute(name, args) → str`：执行工具并返回结果字符串
- 初始注册一个 `render_3d_structure` 工具（已有后端逻辑）
- 后续 Phase 4 注册其余工具

#### Step 2: Agent 循环 `backend/llm/agent.py`
核心类 `CrystalAgent`：
- `__init__()`：初始化 DeepSeek client（base_url="https://api.deepseek.com"）
- `chat(user_message, conversation_id) → async generator`：
  ```
  1. 构建 messages = [system_prompt] + history + [user_message]
  2. while True:
       response = client.chat.completions.create(
           model="deepseek-v4-flash",
           messages=messages,
           tools=tool_registry.get_schemas(),
           thinking={"type": "enabled"},
           stream=False
       )
       msg = response.choices[0].message
       
       # 提取思维链状态
       if hasattr(msg, 'reasoning_content') and msg.reasoning_content:
           status = extract_status(msg.reasoning_content)
           yield {"type": "status_update", "status": "thinking", "detail": status}
       
       if msg.tool_calls:
           for tc in msg.tool_calls:
               yield {"type": "status_update", "status": "calling_tool", "detail": f"正在调用{tc.function.name}…"}
               result = tool_registry.execute(tc.function.name, tc.function.arguments)
               messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
           continue  # 再问 LLM
       
       # 最终回复
       yield {"type": "chat_message", "role": "assistant", "content": msg.content}
       break
   ```
- 思维链状态提取 `extract_status(reasoning: str) → str`：
  - 简单策略：取思维链最后 1-2 句作为状态（这些通常是模型即将执行的行动的总结）
  - 或用正则匹配关键短语
- 对话历史管理：按 `conversation_id` 存储 `list[dict]`
- `clear_conversation(conversation_id)`：清空历史

#### Step 3: 系统提示词
将根目录的 `system_prompt.md` 复制到 `backend/llm/system_prompt.md`，运行时加载。
提示词中工具描述与实际注册的 schema 保持一致。

#### Step 4: 聊天框前端 `frontend/js/chat.js`
`ChatBox` 类：
- `init(containerId)`：绑定 DOM
- `addMessage(role, content)`：
  - 用户消息：右侧蓝色气泡
  - 助手消息：左侧深色气泡，**渲染 Markdown + LaTeX**
  - 系统消息：居中灰色小字
- `renderMarkdown(text)`：
  - 先用正则提取 `$$...$$` 和 `$...$`，用 KaTeX 渲染为 HTML
  - 剩余文本用 marked.js 渲染
  - 组合放回消息框
- `showTypingIndicator()`：显示 "思考中…" 动画
- `hideTypingIndicator()`
- `addSystemMessage(text, level)`：level = info/warning/error，不同颜色
- `clearMessages()`
- 顶部 "新对话" 按钮

#### Step 5: 更新 WebSocket 消息流 `backend/main.py`
`user_message` 处理：
```
收到用户消息
  → 发给前端回显 (chat_message, role="user")
  → 调用 agent.chat(message, conv_id)
  → 逐步 yield:
      - status_update → 前端显示状态小字
      - chat_message (assistant) → 前端渲染回复
      - render_structure → 前端更新 3D 查看器
```

#### Step 6: 更新前端 `frontend/js/app.js`
完整的消息分派：
- `chat_message` → `chatBox.addMessage(role, content)`
- `system_message` → `chatBox.addSystemMessage(text, level)`
- `status_update` → `chatBox.addSystemMessage(detail, "info")` 或专门的 status bar
- `render_structure` → `crystalViewer.loadCif(...)`

### 4.4 验收清单

- [ ] 输入"你好"，助手回复（纯文本对话通）
- [ ] 输入"解释一下空间群的概念"，回复包含 Markdown 格式（标题、列表）
- [ ] 输入"布拉格定律的公式"，回复包含正确渲染的 LaTeX 公式
- [ ] 输入一长段话，消息框自动滚动到底部
- [ ] 回复过程中，状态栏显示"Thinking…"或思维链摘要
- [ ] 点"新对话"，历史清空，上下文重置
- [ ] 输入"帮我看一下硅的晶体结构"，LLM 调用 render_3d_structure 工具
- [ ] 工具调用时，状态消息显示"正在调用render_3d_structure…"
- [ ] 3D 查看器成功更新为硅的结构

### 4.5 完成后文件状态

```
D:\projects\Crystal agent project 2.0\
├── frontend/
│   ├── index.html              (修改)
│   ├── css/style.css           (修改)
│   └── js/
│       ├── app.js              (修改)
│       ├── crystal-viewer.js
│       └── chat.js             ✓ 新增
├── backend/
│   ├── main.py                 (修改)
│   ├── config.py               (修改)
│   ├── websocket_manager.py
│   ├── crystal_service.py
│   └── llm/
│       ├── __init__.py         ✓ 新增
│       ├── agent.py            ✓ 新增
│       ├── tool_registry.py    ✓ 新增
│       └── system_prompt.md    ✓ 新增
├── knowledge_base/
├── Brainstorm.md
└── IMPLEMENTATION_PLAN.md
```

---

## 五、Phase 4 — 工具实现

### 目标
四大工具组全部实现并注册到 Agent：MP-API、CIF 库、知识库、联网搜索。Agent 可自主选择调用。

### 5.1 前置条件
- Phase 1-3 全部完成
- `pip install mp-api`（Materials Project 官方 SDK）
- `pip install serpapi`（或使用 requests 直接调 SerpAPI）
- 环境变量 `MP_API_KEY`, `SERPAPI_API_KEY` 已设置
- 以下文件存在：Phase 3 全部文件

### 5.2 将创建/修改的文件

```
新增:
backend/tools/__init__.py
backend/tools/mp_api.py           # MP-API 工具组
backend/tools/cif_library.py      # CIF 缓存管理
backend/tools/knowledge_search.py # 知识库检索封装
backend/tools/web_search.py       # SerpAPI 联网搜索

修改:
backend/llm/tool_registry.py      # 注册所有新工具
backend/llm/system_prompt.md      # 更新工具描述（或留到 Phase 5）
```

### 5.3 实施步骤

#### Step 1: CIF 库 `backend/tools/cif_library.py`
- `CifLibrary` 类：
  - `__init__(cache_dir)`：扫描 `cif_cache/` 目录，建立 `{mp_id: filepath}` 索引
  - `get_cif(mp_id) → str | None`：读取 CIF 文本
  - `save_cif(mp_id, cif_data)`：写入 `cif_cache/{mp_id}.cif`
  - `list_cached() → list[str]`：列出已缓存 mp_id
  - `has(mp_id) → bool`
- 工具函数 `get_cif(mp_id)`：供 LLM 调用
  - 命中的话返回 CIF 文本（截断过长文本，保留前 5000 字符 + 提示）

#### Step 2: MP-API 工具组 `backend/tools/mp_api.py`
基于 Materials Project 新版 API (`materialsproject.api` / MPRester)：

```python
# 初始化
from mp_api.client import MPRester
mpr = MPRester(api_key=os.environ["MP_API_KEY"])
```

工具函数：
- `mp_search_materials(formula=None, elements=None, band_gap_min=None, band_gap_max=None, is_stable=None, keywords=None, limit=10) → str`
  - 实现：`mpr.materials.summary.search(...)`
  - 返回 JSON 摘要列表（material_id, formula_pretty, band_gap, energy_above_hull 等）
- `mp_get_summary(mp_id) → str`
  - 返回材料综合属性 JSON
  - 字段：formula, symmetry, band_gap, density, formation_energy_per_atom, 等
- `mp_get_structure(mp_id) → str`
  - 调用 `mpr.get_structure_by_material_id(mp_id)` → Pymatgen Structure → `.to(fmt="cif")` → 写入 `cif_cache` → 返回 CIF 文本
- `mp_get_bandstructure(mp_id) → str`
  - 调用 `mpr.get_bandstructure_by_material_id(mp_id)` → 提取关键数据（带隙类型、VBM/CBM 位置等）→ 文本摘要
- `mp_get_dos(mp_id) → str`
  - 调用 `mpr.get_dos_by_material_id(mp_id)` → 提取 DOS 关键特征 → 文本摘要
- `mp_search_by_chemsys(chemsys, limit=10) → str`
  - 按化学体系搜索，如 "Li-Fe-O"

> **注意**：MP-API 可能超时或报错，每个函数需 try/except，出错返回友好错误信息，让 LLM 能根据错误信息向用户解释。

#### Step 3: 知识库检索 `backend/tools/knowledge_search.py`
- 复用现有 `knowledge_base/kb_search.py` 的 `KnowledgeBase` 类
- 工具函数 `retrieve_knowledge_base(query) → str`：
  - `kb = KnowledgeBase()`
  - `results = kb.search(query, top_k=5)`
  - 格式化为 LLM 友好的文本（用 `kb.format_for_llm()`）

#### Step 4: 联网搜索 `backend/tools/web_search.py`
- 工具函数 `web_search(query) → str`
- 实现：`requests.get("https://serpapi.com/search", params={q: query, api_key: ...})`
- 提取 organic_results 的 title + snippet + link
- 返回前 5 条结果摘要
- 错误处理：SerpAPI 配额用完 / 网络错误 → 返回错误描述

#### Step 5: 注册全部工具 `backend/llm/tool_registry.py`
按以下 JSON Schema 注册：

```python
# 注册顺序（影响 LLM 选择优先级，把常用的放前面）
tool_registry.register("get_cif", ...)
tool_registry.register("render_3d_structure", ...)
tool_registry.register("mp_search_materials", ...)
tool_registry.register("mp_get_structure", ...)
tool_registry.register("mp_get_summary", ...)
tool_registry.register("mp_get_bandstructure", ...)
tool_registry.register("mp_get_dos", ...)
tool_registry.register("retrieve_knowledge_base", ...)
tool_registry.register("web_search", ...)
```

每个工具的 description 需清晰说明**何时使用、参数含义**，这对 LLM 正确选择工具至关重要。

### 5.4 验收清单

- [ ] 直接调用 `get_cif("mp-149")`（后端脚本测试），能从 `cif_cache` 读取
- [ ] `mp_get_structure("mp-149")` 能成功调用 MP-API 并写入 CIF
- [ ] `mp_get_summary("mp-149")` 返回能带隙等信息
- [ ] `retrieve_knowledge_base("布拉格衍射")` 返回相关知识条目
- [ ] `web_search("perovskite solar cell")` 返回搜索结果摘要
- [ ] 通过聊天框输入"帮我查 mp-149 的能带隙"，Agent 能自主选择 mp_get_summary 并回答
- [ ] 通过聊天框输入"搜索钙钛矿太阳能电池最新进展"，Agent 调用 web_search 并总结
- [ ] 通过聊天框输入"什么是布拉格定律"，Agent 调用知识库并回答
- [ ] 工具调用失败时（如不存在的 mp_id），Agent 能向用户解释错误

### 5.5 完成后文件状态

```
D:\projects\Crystal agent project 2.0\
├── frontend/                   (不变)
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── websocket_manager.py
│   ├── crystal_service.py
│   ├── llm/
│   │   ├── agent.py
│   │   ├── tool_registry.py    (修改)
│   │   └── system_prompt.md    (修改)
│   └── tools/
│       ├── __init__.py         ✓ 新增
│       ├── mp_api.py           ✓ 新增
│       ├── cif_library.py      ✓ 新增
│       ├── knowledge_search.py ✓ 新增
│       └── web_search.py       ✓ 新增
├── cif_cache/                  (至少含 mp-149.cif)
├── knowledge_base/
├── Brainstorm.md
└── IMPLEMENTATION_PLAN.md
```

---

## 六、Phase 5 — 联调上线

### 目标
端到端流程无死角、CIF 缓存填充 15 种晶体、错误处理完善、系统提示词与工具同步。

### 6.1 前置条件
- Phase 1-4 全部完成

### 6.2 任务清单

#### 6.2.1 CIF 缓存批量填充
- 脚本或手动逐个获取 15 种晶体 CIF（列表见 Brainstorm.md 或上文）
- 验证每个 CIF 可正常渲染

#### 6.2.2 端到端典型对话测试
用以下对话序列完整走通：

| # | 输入 | 预期调用链 |
|---|---|---|
| 1 | "你好" | 纯文本回复 |
| 2 | "看看 NaCl 的结构" | get_cif → render_3d_structure |
| 3 | "它的空间群是什么" | mp_get_summary（或基于上下文回答） |
| 4 | "切换成原胞看看" | viewer_action: switch_cell |
| 5 | "构建 2×2×2 超胞" | viewer_action: build_supercell |
| 6 | "NaCl 为什么是 FCC 结构？结合离子半径解释" | retrieve_knowledge_base 或自己回答 |
| 7 | "最近有什么关于卤化物钙钛矿的新研究" | web_search |
| 8 | "查一下 BaTiO3 (mp-5229) 的能带结构" | mp_get_structure → render + mp_get_bandstructure |
| 9 | "新对话" | 清空上下文 |
| 10 | "刚才我们聊了什么" | 应回答不知道（上下文已清空） |

#### 6.2.3 错误处理完善
- [ ] DeepSeek API 超时 → 显示"模型响应超时，请重试"
- [ ] DeepSeek API 返回错误码（429/500等）→ 显示具体错误
- [ ] MP-API 请求失败 → Agent 能感知并在回复中说明
- [ ] SerpAPI 配额用尽 → 提示用户
- [ ] WebSocket 断连 → 前端显示"连接断开，正在重连…"
- [ ] CIF 格式错误 → 后端返回错误，前端提示
- [ ] 超胞原子数 > 50 → 后端拒绝 + 前端按钮置灰

#### 6.2.4 系统提示词最终同步
- 确保 `system_prompt.md` 中的工具描述与 `tool_registry.py` 注册的完全一致
- 实际测试几轮对话后微调提示词

#### 6.2.5 配置文件
- 创建 `.env.example` 列出需要的环境变量
- 创建 `requirements.txt`（完整依赖列表）

### 6.3 验收清单

- [ ] 以上 10 条端到端对话全部通过
- [ ] 所有错误场景优雅降级
- [ ] 15 种晶体全部可渲染
- [ ] `requirements.txt` 可一键安装依赖
- [ ] 启动命令简单明确：`python backend/main.py`

---

## 七、开发规范

### 7.1 代码风格
- Python：类型注解（`def foo(x: str) -> dict:`）
- JS：ES6+ 语法，`async/await`
- 注释：仅关键逻辑处一行注释，不写长文档注释

### 7.2 跨会话衔接指南

**开始新会话时，按以下步骤快速定位进度：**

1. 阅读本文件 `IMPLEMENTATION_PLAN.md`，对照"完成后文件状态"检查哪些文件已存在
2. `git status`（如果启用了 Git）或 `ls -R` 对比文件清单
3. 找到当前 Phase 的起始位置，按 Step 顺序继续
4. 完成后更新本文件头部的 `当前阶段` 状态

**每个 Phase 完成后的收尾动作：**
- [ ] 运行验证清单确认全部通过
- [ ] 更新本文件头部 `当前阶段`
- [ ] 将关键配置项记录到 `.env.example`
- [ ] 如有新增依赖，更新 `requirements.txt`

### 7.3 环境变量清单

```bash
DEEPSEEK_API_KEY=sk-xxx    # DeepSeek API 密钥
MP_API_KEY=xxx              # Materials Project API 密钥
SERPAPI_API_KEY=xxx          # SerpAPI 密钥
```

### 7.4 requirements.txt（完整）

```
fastapi>=0.110.0
uvicorn[standard]>=0.27.0
websockets>=12.0
pymatgen>=2024.1.0
mp-api>=0.41.0
openai>=1.12.0          # 兼容 DeepSeek API
requests>=2.31.0
```

---

## 八、文件依赖关系图

```
index.html
├── css/style.css
├── js/app.js ───────── 入口，WebSocket，消息路由
│   ├── js/crystal-viewer.js ── 3Dmol.js 封装
│   └── js/chat.js ──────────── 聊天框 UI
│
backend/main.py ──────── FastAPI + WebSocket endpoint
├── config.py ────────── 配置中心
├── websocket_manager.py WS 连接管理
├── crystal_service.py ── Pymatgen 计算
└── llm/agent.py ──────── DeepSeek Agent 循环
    ├── llm/tool_registry.py ── 工具注册
    │   ├── tools/mp_api.py
    │   ├── tools/cif_library.py
    │   ├── tools/knowledge_search.py → knowledge_base/
    │   └── tools/web_search.py
    └── llm/system_prompt.md
```

---

*计划书版本 v1.0，2026-05-24。开始实施 Phase 1。*
