# 晶体智能助手 (Crystal Agent)

集成了 3D 晶体结构查看器与 AI 对话的交互式晶体学研究平台。支持 Materials Project 数据查询、本地知识库检索、联网搜索，能够帮助研究者探索、分析和理解晶体结构及其物理化学性质。

## 功能特性

- **3D 晶体查看器** — 基于 3Dmol.js，支持旋转/缩放、原胞/惯用胞切换、超胞构建、元素显隐、键连与晶胞框线显示
- **AI 对话** — 基于 DeepSeek 大模型，支持 Markdown + LaTeX 渲染，思考模式开启
- **Materials Project 集成** — 按化学式/元素/带隙搜索材料，获取结构、能带、态密度、综合性质
- **本地知识库** — 29 条晶体学词条（晶格、对称性、衍射、缺陷、能带理论、常见结构等）
- **联网搜索** — SerpAPI 补充最新研究进展
- **CIF 缓存** — 20 种常见晶体预置，支持动态扩展
- **一键公网分享** — 内置 ngrok 隧道，`启动公网.bat` 即开即用

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | HTML5 + CSS3 + Vanilla JS, 3Dmol.js, marked.js, KaTeX |
| 后端 | Python 3.10+, FastAPI, Pymatgen, CrystalNN |
| 通信 | WebSocket（JSON 消息协议） |
| AI | DeepSeek API (`deepseek-v4-flash`), thinking mode |
| 工具 | SerpAPI, Materials Project API, 本地知识库 |

## 快速开始

### 1. 环境准备

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

复制 `.env.example` 为 `.env`，填入密钥：

```ini
DEEPSEEK_API_KEY=sk-your-key-here   # 必填，LLM 对话
MP_API_KEY=your-mp-key-here         # Materials Project
SERPAPI_API_KEY=your-serpapi-key-here  # 联网搜索
```

API Key 获取：
- [DeepSeek API](https://platform.deepseek.com/api_keys)
- [Materials Project API](https://next-gen.materialsproject.org/api)
- [SerpAPI](https://serpapi.com/)

### 3. 启动

**本地模式：**
```bash
python backend/main.py
# 访问 http://localhost:8000
```

**公网分享（需安装 ngrok）：**
```bash
python start_public.py
# 终端打印公网 URL，分享链接即可
```

Windows 用户可直接双击 `启动公网.bat`。

## 系统架构

```
启动公网.bat → start_public.py → FastAPI + ngrok tunnel
                                   │
浏览器 ←── WebSocket ──→ backend/main.py
  │                            │
  ├─ 3D 查看器              ├─ crystal_service.py (Pymatgen)
  │  (crystal-viewer.js)    ├─ llm/agent.py (DeepSeek)
  ├─ 聊天框                 │   └─ llm/tool_registry.py
  │  (chat.js)              ├─ tools/cif_library.py
  └─ 布局控制               ├─ tools/mp_api.py
     (app.js)               ├─ tools/knowledge_search.py
                            └─ tools/web_search.py
```

## 工具清单

| 工具 | 说明 |
|---|---|
| `render_3d_structure` | 将 CIF 结构渲染到左侧 3D 查看器 |
| `get_cif` | 从本地 CIF 缓存读取结构 |
| `mp_search_materials` | 按化学式/元素/带隙搜索 MP 材料库 |
| `mp_get_structure` | 获取材料 CIF 结构并缓存 |
| `mp_get_summary` | 获取材料综合性质（带隙、形成能、密度等） |
| `mp_get_bandstructure` | 获取能带结构数据 |
| `mp_get_dos` | 获取态密度数据 |
| `mp_search_by_chemsys` | 按化学体系搜索材料 |
| `retrieve_knowledge_base` | 搜索本地晶体学知识库 |
| `web_search` | SerpAPI 联网搜索 |

## 项目结构

```
Crystal agent project 2.0/
├── backend/
│   ├── main.py                # FastAPI 入口 + WebSocket
│   ├── config.py              # 全局配置
│   ├── crystal_service.py     # Pymatgen 结构处理
│   ├── websocket_manager.py   # WebSocket 连接管理
│   ├── llm/
│   │   ├── agent.py           # DeepSeek Agent 循环
│   │   └── tool_registry.py   # 工具注册中心
│   └── tools/
│       ├── cif_library.py     # CIF 缓存管理
│       ├── mp_api.py          # MP-API 工具组
│       ├── knowledge_search.py# 知识库检索
│       └── web_search.py      # SerpAPI 搜索
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   └── js/
│       ├── app.js             # 主逻辑 + WebSocket
│       ├── crystal-viewer.js  # 3Dmol.js 查看器
│       └── chat.js            # 聊天框 UI
├── knowledge_base/            # 晶体学知识库（29 条）
├── cif_cache/                 # CIF 文件缓存（20 种）
├── scripts/
│   └── batch_fetch_cif.py     # 批量获取 CIF 脚本
├── system_prompt.md           # LLM 系统提示词
├── start_public.py            # 公网启动脚本
├── 启动公网.bat               # Windows 一键启动
├── requirements.txt
├── .env.example
└── README.md
```

## License

MIT License
