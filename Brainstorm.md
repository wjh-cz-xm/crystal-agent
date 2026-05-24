做一个晶体演示网页应用，包含能展示晶体结构的3D模型查看器和能帮助用户研究晶体相关的物理和化学问题的ai智能体
下面是我的头脑风暴，备份在：Brainstorm.md
# 项目路径
本项目所有相关文件保存在：D:\projects\Crystal agent project 2.0
# 设计
架构：前端+后端python
## 前端(frontend)
WebSocket推送
显示语言文字一律为中文
配色采用蓝白配色，页面设计要有科技感
网页分为两部分，晶体模型展示区和ai聊天框，初始设置为左2/3区域为晶体模型展示区，右1/3为聊天框
可以通过拖动分隔线来调整页面占比
### 3D晶体模型展示(crystal-viewer)（前端部分）
集成3Dmol.js
原子半径(atomic radii)统一设为0.5埃，仅用颜色区分原子
配色方案(color scheme)采用Jmol的
鼠标滚轮控制缩放
鼠标拖动控制视角
区域左上角显示物质化学式+MP-ID标签
#### 区域左侧有如下按钮
刷新按钮：一键回正，视角和大小回到默认值
晶胞形式更改选项卡(Change unit cell) ，可选：primitive cell/conventional cell 
超胞(supercell)构建选项卡,可选：1×1×1/2×2×2，原胞原子数大于50时不生效(置灰即可)
##### 可勾选选项：
###### 显隐控制(Hide/show):
原子(Atoms)
	晶体文件所包含的各元素列表，单独控制显隐
键连(Bonds)
晶胞框线(Unit cell)
配位多面体(Polyhedra):技术难度偏高，先设按钮但不生效(置灰即可)，后续补上
###### 其他可选项:
Draw repeats of atoms on periodic boundaries （默认勾选）
Draw atoms outside unit cell bonded to atoms within unit cell （默认勾选）
### 聊天框
类微信/QQ 的消息流，系统消息以小字显示于消息间
顶部有开启新对话按钮
用户与大模型的消息框均能渲染markdown格式和Latex公式
#### 系统消息包括：
##### 报错消息
deepseek api 掉线/报错 
其他报错消息
##### 大模型状态消息
显示当前大模型的状态
如“Thinking...”、“正在调用MP-API的...工具获取...数据”、“错误：...工具出现...问题”、“调用知识库”、“调用cif库”

## 后端（backend）
### 3D晶体模型展示(crystal-viewer)（后端部分）
晶体文件处理FastAPI + **Pymatgen (Python Materials Genomics)** 
超胞、unit cell的转换等计算都放在后端，前端只负责展示
键合算法(bonding algorithm)采用CrystalNN
可以被大模型的工具唤起

### 大模型(LLM)
调用deepseek api
model="deepseek-v4-flash"
全部采用非流式输出，保持思考模式，思考强度(effort)为high
支持多轮对话，仅在重启和用户手动按下“新对话”按钮时清除上下文并开始新对话
附几个相关的官方文档
	[首次调用 API | DeepSeek API Docs](https://api-docs.deepseek.com/zh-cn/)
	[思考模式 | DeepSeek API Docs](https://api-docs.deepseek.com/zh-cn/guides/thinking_mode)
	[多轮对话 | DeepSeek API Docs](https://api-docs.deepseek.com/zh-cn/guides/multi_round_chat)
	[JSON Output | DeepSeek API Docs](https://api-docs.deepseek.com/zh-cn/guides/json_mode)

采用单一agent模式，即只有一套提示词，大模型可以按需调用所有工具
#### 提示词(Prompt)
我拟的系统提示词初稿保存在system_prompt.md
需要你帮我润色和规范化，采用Markdown 结构化标签来组织系统提示词，后续持续迭代
#### 工具清单(Tools)
`render_3d_structure(cif_data, mp_id, label)`(crystal-viewer唤起):
- 参数：cif_data (CIF 文本), mp_id, label (物质名称)。
- 作用：告诉前端“请在左侧 3D 视口渲染此晶体结构”。大模型调用此工具来更新界面。

`get__cif(mp_id)`(cif库的调用):
- 参数：mp_id (如 "mp-149")。
- 作用：从CIF库中获取CIF 文本

`web_search(query)`(网络搜索)
- 参数：query
- 作用：当遇到 Materials Project 或本地库没有的常识、最新文献时，进行联网搜索。

`retrieve_knowledge_base(query)`(知识库的调用)：
- 参数：query。
- 作用：检索本地向量数据库。
##### MP-API工具组
用于通过Materials Project API获取晶体学数据
相关网页资源：
	[Materials Project API - Swagger UI](https://api.materialsproject.org/docs)
	[materialsproject/api: New API client for the Materials Project](https://github.com/materialsproject/api)
	[Getting Started | Materials Project Documentation](https://docs.materialsproject.org/downloading-data/using-the-api/getting-started)
	[Querying Data | Materials Project Documentation](https://docs.materialsproject.org/downloading-data/using-the-api/querying-data)
	[Examples | Materials Project Documentation](https://docs.materialsproject.org/downloading-data/using-the-api/examples)
你来将其中与晶体结构相关的查询封装为工具
其中获得的晶体数据一律以cif文件保存在cif_cache中，便于后续调用

## 库
### cif_cache (cif晶体学文件库)
你帮我构建，用于存放所有.cif晶体学文件
预存15种常见晶体的.cif文件
可供大模型调用
### knowledge_base (知识库)
大模型的知识库，已经构建好，可以直接使用，保存在文件夹：knowledge_base