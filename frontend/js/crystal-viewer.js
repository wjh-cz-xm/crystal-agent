/**
 * 晶体 3D 查看器 — 基于 3Dmol.js
 */
class CrystalViewer {
  constructor() {
    this.viewer = null;
    this.currentCif = null;
    this.currentMpId = "";
    this.currentLabel = "";
    this.elements = [];

    this._bondsVisible = true;
    this._unitCellVisible = true;
    this._periodicRepeats = true;
    this._elementVisibility = {};
    this._unitCellShapes = [];   // 手动绘制的晶胞框线 shape 引用
  }

  /** 在指定容器中创建 3Dmol viewer */
  init(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.style.position = "relative";
    container.style.width = "100%";
    container.style.height = "100%";

    this.viewer = $3Dmol.createViewer(container, {
      backgroundColor: "white",
    });
    this.viewer.spin(false);
    this.viewer.resize();
    console.log("[CrystalViewer] init done");
  }

  /** 从后端消息设置元素列表 */
  setElements(elements) {
    if (!elements || elements.length === 0) return;
    for (const e of elements) {
      if (!(e in this._elementVisibility)) {
        this._elementVisibility[e] = true;
      }
    }
    this.elements = elements.slice().sort();
    this._applyElementVisibility();
    this._onElementsChange();
  }

  // ========== 晶格参数解析 ==========

  _parseLatticeVectors(cifData) {
    const num = (re) => { const m = cifData.match(re); return m ? parseFloat(m[1]) : null; };
    const a = num(/_cell_length_a\s+([\d.]+)/) || 5.0;
    const b = num(/_cell_length_b\s+([\d.]+)/) || 5.0;
    const c = num(/_cell_length_c\s+([\d.]+)/) || 5.0;
    const al = (num(/_cell_angle_alpha\s+([\d.]+)/) || 90) * Math.PI / 180;
    const be = (num(/_cell_angle_beta\s+([\d.]+)/)  || 90) * Math.PI / 180;
    const ga = (num(/_cell_angle_gamma\s+([\d.]+)/) || 90) * Math.PI / 180;

    // 3Dmol 通常用直角坐标，CIF 的 lattice vectors 需要转换
    // 但 3Dmol.js addModel("cif") 会自动处理坐标，所以我们直接用 fractional→Cartesian
    // 这里用标准转换公式
    const cosAl = Math.cos(al), sinAl = Math.sin(al);
    const cosBe = Math.cos(be), sinBe = Math.sin(be);
    const cosGa = Math.cos(ga), sinGa = Math.sin(ga);

    const ax = a;
    const ay = 0;
    const az = 0;

    const bx = b * cosGa;
    const by = b * sinGa;
    const bz = 0;

    const cx = c * cosBe;
    const cy = c * (cosAl - cosBe * cosGa) / sinGa;
    const cz = Math.sqrt(Math.max(0, c * c - cx * cx - cy * cy));

    return [
      [ax, ay, az],
      [bx, by, bz],
      [cx, cy, cz],
    ];
  }

  /** 手动画晶胞六面体框线（12条边），无箭头/无标签 */
  _drawUnitCellBox() {
    if (!this.viewer || !this.currentCif) return;

    // 先清除旧框线
    this._clearUnitCellBox();

    try {
      // 优先用后端传来的原始晶格矢量；扩胞 CIF 的矢量会偏大
      const vectors = this._latticeVectors || this._parseLatticeVectors(this.currentCif);
      const av = vectors[0], bv = vectors[1], cv = vectors[2];

      const v = [
        [0, 0, 0],
        av,
        bv,
        cv,
        [av[0] + bv[0], av[1] + bv[1], av[2] + bv[2]],
        [av[0] + cv[0], av[1] + cv[1], av[2] + cv[2]],
        [bv[0] + cv[0], bv[1] + cv[1], bv[2] + cv[2]],
        [av[0] + bv[0] + cv[0], av[1] + bv[1] + cv[1], av[2] + bv[2] + cv[2]],
      ];

      const edges = [
        [0, 1], [0, 2], [0, 3],    // 原点出发三边
        [1, 4], [1, 5],              // 从 a 出发
        [2, 4], [2, 6],              // 从 b 出发
        [3, 5], [3, 6],              // 从 c 出发
        [4, 7], [5, 7], [6, 7],      // 对面顶点收束
      ];

      for (const [i, j] of edges) {
        this.viewer.addCylinder({
          start: { x: v[i][0], y: v[i][1], z: v[i][2] },
          end:   { x: v[j][0], y: v[j][1], z: v[j][2] },
          radius: 0.015,
          color: "#cccccc",
          fromCap: false,
          toCap: false,
        });
      }

      // 记录添加的 shape 数量（用于后续清除）
      this._unitCellShapes = [true]; // 标记已添加
    } catch (e) {
      console.warn("[CrystalViewer] unit cell draw failed:", e);
    }
  }

  _clearUnitCellBox() {
    if (!this.viewer) return;
    // removeAllShapes 会清除自定义的 cylinder
    this.viewer.removeAllShapes();
    this._unitCellShapes = [];
  }

  // ========== 载入 CIF ==========

  loadCif(cifData, mpId, label, latticeVectors, format) {
    this.currentCif = cifData;
    this.currentMpId = mpId || "";
    this.currentLabel = label || "";
    this._dataFormat = format || "cif";
    if (latticeVectors) this._latticeVectors = latticeVectors;

    // Count atoms from CIF _atom_site_label lines
    this.numAtoms = 0;
    for (const line of cifData.split("\n")) {
      if (line.trim().startsWith("_atom_site_label")) {
        this.numAtoms++;
      }
    }

    // Notify app of atom count change (for supercell disable)
    if (typeof this.onAtomCountChange === "function") {
      this.onAtomCountChange(this.numAtoms);
    }

    this.viewer.removeAllModels();
    this.viewer.removeAllSurfaces();
    this.viewer.removeAllShapes();
    this.viewer.removeAllLabels();
    this._unitCellShapes = [];

    this.viewer.addModel(cifData, this._dataFormat);
    this._applyStyle();

    if (this._unitCellVisible) {
      this._drawUnitCellBox();
    }

    this.viewer.zoomTo();
    this.viewer.render();
    this._updateLabel();
  }

  // ========== 样式 ==========

  _applyStyle() {
    const style = this._bondsVisible
      ? { sphere: { radius: 0.5, colorscheme: "Jmol" }, stick: { radius: 0.08, color: "#999999" } }
      : { sphere: { radius: 0.5, colorscheme: "Jmol" } };

    for (const elem of this.elements) {
      if (this._elementVisibility[elem] === false) {
        this.viewer.setStyle({ elem: elem }, { sphere: { hidden: true }, stick: { hidden: true } });
      } else {
        this.viewer.setStyle({ elem: elem }, style);
      }
    }
    if (this.elements.length === 0 || Object.values(this._elementVisibility).every(v => v !== false)) {
      this.viewer.setStyle({}, style);
    }
  }

  _applyElementVisibility() {
    if (!this.viewer) return;
    const style = this._bondsVisible
      ? { sphere: { radius: 0.5, colorscheme: "Jmol" }, stick: { radius: 0.08, color: "#999999" } }
      : { sphere: { radius: 0.5, colorscheme: "Jmol" } };

    for (const elem of this.elements) {
      if (this._elementVisibility[elem] === false) {
        this.viewer.setStyle({ elem: elem }, { sphere: { hidden: true }, stick: { hidden: true } });
      } else {
        this.viewer.setStyle({ elem: elem }, style);
      }
    }
    this.viewer.render();
  }

  // ========== 标签 ==========

  _updateLabel() {
    const el = document.getElementById("structure-label");
    if (!el) return;
    let text = this.currentLabel || "未命名";
    if (this.currentMpId) text += `  (${this.currentMpId})`;
    el.textContent = text;
  }

  _onElementsChange() {
    if (typeof this.onElementsChange === "function") {
      this.onElementsChange(this.elements, this._elementVisibility);
    }
  }

  // ========== 视角 ==========

  resetView() {
    if (!this.viewer || !this.currentCif) return;
    // 彻底重建：重载 CIF，重置视角和所有显隐
    this._elementVisibility = {};
    this.loadCif(this.currentCif, this.currentMpId, this.currentLabel);
    if (this.elements.length > 0) {
      for (const e of this.elements) this._elementVisibility[e] = true;
      this._onElementsChange();
    }
  }

  // ========== 显隐切换 ==========

  toggleAtoms(element, show) {
    this._elementVisibility[element] = show;
    if (!this.viewer || !this.currentCif) return;

    const style = this._bondsVisible
      ? { sphere: { radius: 0.5, colorscheme: "Jmol" }, stick: { radius: 0.08, color: "#999999" } }
      : { sphere: { radius: 0.5, colorscheme: "Jmol" } };

    if (show) {
      this.viewer.setStyle({ elem: element }, style);
    } else {
      this.viewer.setStyle({ elem: element }, { sphere: { hidden: true }, stick: { hidden: true } });
    }
    this.viewer.render();
  }

  toggleBonds(show) {
    this._bondsVisible = show;
    if (!this.viewer || !this.currentCif) return;

    const style = show
      ? { sphere: { radius: 0.5, colorscheme: "Jmol" }, stick: { radius: 0.08, color: "#999999" } }
      : { sphere: { radius: 0.5, colorscheme: "Jmol" } };

    for (const elem of this.elements) {
      if (this._elementVisibility[elem] !== false) {
        this.viewer.setStyle({ elem: elem }, style);
      }
    }
    if (this.elements.length === 0) {
      this.viewer.setStyle({}, style);
    }
    this.viewer.render();
  }

  toggleUnitCell(show) {
    this._unitCellVisible = show;
    if (!this.viewer || !this.currentCif) return;
    if (show) {
      this._drawUnitCellBox();
    } else {
      this._clearUnitCellBox();
    }
    this.viewer.render();
  }

  togglePeriodicRepeats(show) {
    this._periodicRepeats = show;
    if (!this.viewer || !this.currentCif) return;
    const savedVis = { ...this._elementVisibility };
    this.loadCif(this.currentCif, this.currentMpId, this.currentLabel);
    this._elementVisibility = savedVis;
    this._applyElementVisibility();
  }

  toggleOutsideAtoms(show) {
    this._outsideAtoms = show;
    if (!this.viewer || !this.currentCif) return;
    const savedVis = { ...this._elementVisibility };
    this.loadCif(this.currentCif, this.currentMpId, this.currentLabel);
    this._elementVisibility = savedVis;
    this._applyElementVisibility();
  }

  refreshStructure(cifData) {
    this.loadCif(cifData, this.currentMpId, this.currentLabel);
  }

  resize() {
    if (this.viewer) this.viewer.resize();
  }
}
