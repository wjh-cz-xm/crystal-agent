/**
 * 晶体智能助手 — 前端主逻辑
 * Phase 3: LLM Agent + ChatBox 集成
 */
(function () {
  "use strict";

  // ========== DOM 引用 ==========
  const $ = (sel) => document.querySelector(sel);

  const chatInput = $("#chat-input");
  const btnSend = $("#btn-send");
  const btnNewChat = $("#btn-new-chat");
  const divider = $("#divider");
  const crystalViewerPanel = $("#crystal-viewer");
  const chatPanel = $("#chat-panel");
  const connectionStatus = $("#connection-status");
  const llmStatus = $("#llm-status");

  // 查看器控件
  const btnReset = $("#btn-reset");
  const selCellType = $("#cell-type");
  const selSupercell = $("#supercell-size");
  const cbBonds = $("#show-bonds");
  const cbUnitcell = $("#show-unitcell");
  const cbPeriodic = $("#opt-periodic");
  const cbOutside = $("#opt-outside");
  const elementsList = $("#elements-list");

  // ========== CrystalViewer ==========
  let viewer = null;

  function initViewer() {
    viewer = new CrystalViewer();
    viewer.init("viewer-3d-container");

    viewer.onElementsChange = function (elements, visibility) {
      renderElementsList(elements, visibility);
    };

    viewer.onAtomCountChange = function (numAtoms) {
      // 原胞原子数 > 50 时禁用超胞选项
      if (selSupercell) {
        const tooBig = numAtoms > 50;
        selSupercell.disabled = tooBig;
        if (tooBig) {
          selSupercell.title = "原胞原子数超过 50，不支持构建超胞";
          selSupercell.value = "1,1,1";
        } else {
          selSupercell.title = "";
        }
      }
    };

    window.addEventListener("resize", () => {
      viewer.resize();
    });
  }

  function renderElementsList(elements, visibility) {
    if (!elementsList) return;
    elementsList.innerHTML = "";
    elements.forEach((elem) => {
      const div = document.createElement("div");
      div.className = "cb-item element-item";

      const id = `elem-${elem}`;
      const input = document.createElement("input");
      input.type = "checkbox";
      input.id = id;
      input.checked = visibility[elem] !== false;
      input.addEventListener("change", () => {
        viewer.toggleAtoms(elem, input.checked);
      });

      const label = document.createElement("label");
      label.htmlFor = id;
      label.textContent = elem;

      div.appendChild(input);
      div.appendChild(label);
      elementsList.appendChild(div);
    });
  }

  // ========== ChatBox ==========
  const chatBox = new ChatBox();
  chatBox.init("chat-messages");

  // ========== WebSocket ==========
  let ws = null;
  let reconnectTimer = null;
  let reconnectDelay = 1000;
  const MAX_RECONNECT_DELAY = 30000;

  function connectWebSocket() {
    const protocol = location.protocol === "https:" ? "wss:" : "ws:";
    const url = `${protocol}//${location.host}/ws`;

    ws = new WebSocket(url);

    ws.onopen = () => {
      console.log("[WS] connected");
      reconnectDelay = 1000;
      connectionStatus.textContent = "● 已连接";
      connectionStatus.className = "connected";
      chatBox.addSystemMessage("已连接到服务器", "info");
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        handleMessage(msg);
      } catch (e) {
        console.error("[WS] parse error:", e);
      }
    };

    ws.onclose = () => {
      console.log("[WS] disconnected");
      connectionStatus.textContent = "● 连接断开，重连中…";
      connectionStatus.className = "disconnected";
      scheduleReconnect();
    };

    ws.onerror = () => {
      console.error("[WS] error");
    };
  }

  function scheduleReconnect() {
    if (reconnectTimer) return;
    reconnectTimer = setTimeout(() => {
      reconnectTimer = null;
      reconnectDelay = Math.min(reconnectDelay * 2, MAX_RECONNECT_DELAY);
      console.log(`[WS] reconnecting in ${reconnectDelay}ms...`);
      connectWebSocket();
    }, reconnectDelay);
  }

  function sendMessage(type, payload) {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      chatBox.addSystemMessage("连接未就绪，请稍后重试", "warning");
      return false;
    }
    ws.send(JSON.stringify({ type, ...payload }));
    return true;
  }

  // ========== 消息处理 ==========
  function handleMessage(msg) {
    switch (msg.type) {
      case "chat_message":
        chatBox.addMessage(msg.role, msg.content);
        // 收到助手消息后清除状态
        llmStatus.textContent = "";
        break;

      case "system_message":
        chatBox.addSystemMessage(msg.text, msg.level);
        break;

      case "status_update":
        // 显示在底部状态栏
        if (msg.detail) {
          llmStatus.textContent = msg.detail;
        }
        break;

      case "render_structure":
        if (viewer && msg.cif_data) {
          viewer.loadCif(
            msg.cif_data,
            msg.mp_id,
            msg.label,
            msg.lattice_vectors,
            msg.format
          );
          if (msg.elements && msg.elements.length > 0) {
            viewer.setElements(msg.elements);
          }
          if (selSupercell) selSupercell.value = "1,1,1";
        }
        break;

      default:
        console.log("[WS] unknown type:", msg.type, msg);
    }
  }

  function sendChatMessage() {
    const text = chatInput.value.trim();
    if (!text) return;
    if (sendMessage("user_message", { text })) {
      chatInput.value = "";
      chatInput.style.height = "auto";
      // 显示等待状态
      llmStatus.textContent = "正在思考…";
    }
  }

  // ========== 分隔线拖动 ==========
  function setupDivider() {
    let dragging = false;

    divider.addEventListener("mousedown", (e) => {
      dragging = true;
      divider.classList.add("active");
      document.body.style.cursor = "col-resize";
      document.body.style.userSelect = "none";
      e.preventDefault();
    });

    document.addEventListener("mousemove", (e) => {
      if (!dragging) return;
      const main = document.getElementById("main");
      const rect = main.getBoundingClientRect();
      const totalW = rect.width;
      const dividerW = 4;
      const minLeft = 300;
      const minRight = 280;
      let leftW = e.clientX - rect.left;
      leftW = Math.max(minLeft, Math.min(leftW, totalW - dividerW - minRight));
      crystalViewerPanel.style.flex = `0 0 ${leftW}px`;
    });

    document.addEventListener("mouseup", () => {
      if (!dragging) return;
      dragging = false;
      divider.classList.remove("active");
      document.body.style.cursor = "";
      document.body.style.userSelect = "";

      const main = document.getElementById("main");
      const totalW = main.getBoundingClientRect().width;
      const leftW = crystalViewerPanel.getBoundingClientRect().width;
      const ratio = leftW / (totalW - 4);
      const flexLeft = Math.round(ratio * 100);
      const flexRight = 100 - flexLeft;
      crystalViewerPanel.style.flex = `${flexLeft} 1 0%`;
      chatPanel.style.flex = `${flexRight} 1 0%`;

      if (viewer) viewer.resize();
    });
  }

  // ========== 查看器控件事件 ==========
  function setupViewerControls() {
    btnReset.addEventListener("click", () => {
      if (viewer) viewer.resetView();
    });

    selCellType.addEventListener("change", () => {
      sendMessage("viewer_action", {
        action: "switch_cell",
        cell_type: selCellType.value,
      });
    });

    selSupercell.addEventListener("change", () => {
      const val = selSupercell.value;
      const [a, b, c] = val.split(",").map(Number);
      sendMessage("viewer_action", {
        action: "build_supercell",
        size: [a, b, c],
      });
    });

    cbBonds.addEventListener("change", () => {
      if (viewer) viewer.toggleBonds(cbBonds.checked);
    });

    cbUnitcell.addEventListener("change", () => {
      if (viewer) viewer.toggleUnitCell(cbUnitcell.checked);
    });

    cbPeriodic.addEventListener("change", () => {
      sendMessage("viewer_action", {
        action: "toggle_display",
        periodic: cbPeriodic.checked,
        outside: cbOutside.checked,
      });
    });

    cbOutside.addEventListener("change", () => {
      sendMessage("viewer_action", {
        action: "toggle_display",
        periodic: cbPeriodic.checked,
        outside: cbOutside.checked,
      });
    });
  }

  // ========== 初始化 ==========
  function init() {
    initViewer();
    connectWebSocket();
    setupDivider();
    setupViewerControls();

    btnSend.addEventListener("click", sendChatMessage);

    chatInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendChatMessage();
      }
    });

    chatInput.addEventListener("input", () => {
      chatInput.style.height = "auto";
      chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + "px";
    });

    btnNewChat.addEventListener("click", () => {
      sendMessage("new_conversation", {});
      chatBox.clearMessages();
      chatBox.addSystemMessage("已开启新对话", "info");
    });

    console.log("[App] Phase 3 初始化完成");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
