/**
 * 晶体智能助手 — 聊天框 UI
 * Markdown + LaTeX 渲染，系统消息，状态指示
 */
class ChatBox {
  constructor() {
    this._container = null;
    this._typingEl = null;
    this._typingVisible = false;
  }

  /** 绑定 DOM 容器 */
  init(containerId) {
    this._container = document.getElementById(containerId);
    if (!this._container) {
      console.error("[ChatBox] 容器不存在:", containerId);
    }
  }

  // ========== 消息添加 ==========

  /** 添加聊天消息气泡 */
  addMessage(role, content) {
    this._hideTyping();
    const div = document.createElement("div");
    div.className = `message message-${role}`;

    if (role === "assistant") {
      div.innerHTML = this._renderContent(content);
    } else {
      div.textContent = content;
    }

    this._container.appendChild(div);
    this._scrollToBottom();
  }

  /** 添加系统状态消息（居中灰色小字）*/
  addSystemMessage(text, level) {
    const div = document.createElement("div");
    div.className = `system-message system-${level || "info"}`;
    div.textContent = text;
    this._container.appendChild(div);
    this._scrollToBottom();
  }

  /** 添加 HTML 系统消息（用于状态指示器） */
  addStatusMessage(html, cssClass) {
    const div = document.createElement("div");
    div.className = cssClass || "status-indicator";
    div.innerHTML = html;
    this._container.appendChild(div);
    this._scrollToBottom();
  }

  // ========== 打字/思考指示器 ==========

  /** 显示"思考中…"动画 */
  showTyping() {
    if (this._typingVisible) return;
    this._typingVisible = true;
    this._typingEl = document.createElement("div");
    this._typingEl.className = "typing-indicator";
    this._typingEl.innerHTML =
      '<span></span><span></span><span></span>';
    this._container.appendChild(this._typingEl);
    this._scrollToBottom();
  }

  _hideTyping() {
    if (this._typingEl) {
      this._typingEl.remove();
      this._typingEl = null;
    }
    this._typingVisible = false;
  }

  // ========== 消息管理 ==========

  /** 清空所有消息 */
  clearMessages() {
    this._hideTyping();
    if (this._container) {
      this._container.innerHTML = "";
    }
  }

  // ========== Markdown + LaTeX 渲染 ==========

  _renderContent(text) {
    if (!text) return "";

    // Step 1: 提取块级 LaTeX $$...$$
    const displayBlocks = [];
    let processed = text.replace(/\$\$([\s\S]*?)\$\$/g, (_m, math) => {
      displayBlocks.push(math.trim());
      return `\x00D${displayBlocks.length - 1}\x00`;
    });

    // Step 2: 提取行内 LaTeX $...$（避免匹配 $$ 残骸）
    const inlineBlocks = [];
    processed = processed.replace(/\$([^$]+?)\$/g, (_m, math) => {
      inlineBlocks.push(math.trim());
      return `\x00I${inlineBlocks.length - 1}\x00`;
    });

    // Step 3: Markdown → HTML
    let html = "";
    try {
      html = marked.parse(processed);
    } catch (e) {
      html = this._escapeHtml(processed);
    }

    // Step 4: 替换回块级 LaTeX
    displayBlocks.forEach((math, i) => {
      try {
        const rendered = katex.renderToString(math, {
          displayMode: true,
          throwOnError: false,
          trust: true,
        });
        html = html.replace(`\x00D${i}\x00`, rendered);
      } catch (e) {
        html = html.replace(
          `\x00D${i}\x00`,
          `<pre class="katex-error">$$${this._escapeHtml(math)}$$</pre>`
        );
      }
    });

    // Step 5: 替换回行内 LaTeX
    inlineBlocks.forEach((math, i) => {
      try {
        const rendered = katex.renderToString(math, {
          displayMode: false,
          throwOnError: false,
          trust: true,
        });
        html = html.replace(`\x00I${i}\x00`, rendered);
      } catch (e) {
        html = html.replace(
          `\x00I${i}\x00`,
          `<code class="katex-error">$${this._escapeHtml(math)}$</code>`
        );
      }
    });

    // Step 6: KaTeX auto-render 兜底（处理 marked 未转义的公式）
    try {
      if (typeof renderMathInElement === "function") {
        const temp = document.createElement("div");
        temp.innerHTML = html;
        renderMathInElement(temp, {
          delimiters: [
            { left: "$$", right: "$$", display: true },
            { left: "$", right: "$", display: false },
          ],
          throwOnError: false,
        });
        html = temp.innerHTML;
      }
    } catch (e) {
      // 兜底失败不处理
    }

    return html;
  }

  _escapeHtml(text) {
    const map = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" };
    return String(text).replace(/[&<>"]/g, (c) => map[c] || c);
  }

  // ========== 辅助 ==========

  _scrollToBottom() {
    if (this._container) {
      this._container.scrollTop = this._container.scrollHeight;
    }
  }
}
