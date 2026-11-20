import json

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Психодрама — сцена",
    page_icon="🎭",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(ellipse at 10% 5%, rgba(196,228,248,.42), transparent 34%),
            radial-gradient(ellipse at 92% 18%, rgba(219,239,251,.55), transparent 36%),
            #F3F9FD;
    }
    .block-container {
        max-width: 1400px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }
    h1, h2, h3 {
        color: #234D6B;
        letter-spacing: -.025em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


POOL = [
    {"id": "person", "label": "Нейтральная фигура", "type": "person", "color": "#72A9C8"},
    {"id": "person2", "label": "Другая фигура", "type": "person", "color": "#A88BC7"},
    {"id": "child", "label": "Невысокая фигура", "type": "child", "color": "#E6AD69"},
    {"id": "observer", "label": "Наблюдатель", "type": "person", "color": "#7D9D88"},
    {"id": "circle", "label": "Круг", "type": "circle", "color": "#88B8D3"},
    {"id": "star", "label": "Звезда", "type": "star", "color": "#E3B95F"},
    {"id": "cloud", "label": "Облако", "type": "cloud", "color": "#A5B9D2"},
    {"id": "heart", "label": "Символ", "type": "heart", "color": "#D98991"},
    {"id": "chair", "label": "Стул", "type": "chair", "color": "#B98964"},
    {"id": "house", "label": "Дом", "type": "house", "color": "#D59B72"},
    {"id": "door", "label": "Дверь", "type": "door", "color": "#A8815F"},
    {"id": "tree", "label": "Дерево", "type": "tree", "color": "#78A783"},
    {"id": "table", "label": "Стол", "type": "table", "color": "#9B8069"},
    {"id": "wall", "label": "Преграда", "type": "wall", "color": "#8E9EAC"},
    {"id": "boundary", "label": "Граница", "type": "boundary", "color": "#688BA7"},
]


APP_HTML = r"""
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      color: #294A65;
      background: #F3F9FD;
      font: 14px "Segoe UI", Arial, sans-serif;
    }
    button, input, select {
      font: inherit;
    }
    button {
      cursor: pointer;
    }
    .app {
      display: flex;
      gap: 14px;
      min-height: 840px;
    }
    .sidebar {
      width: 280px;
      min-width: 250px;
      padding: 14px;
      border: 1px solid #D4E5F0;
      border-radius: 18px;
      background: rgba(255,255,255,.92);
      box-shadow: 0 8px 24px rgba(62,112,148,.07);
    }
    .workspace {
      flex: 1;
      min-width: 0;
      padding: 14px;
      border: 1px solid #D4E5F0;
      border-radius: 18px;
      background: rgba(255,255,255,.92);
      box-shadow: 0 8px 24px rgba(62,112,148,.07);
    }
    h2 {
      margin: 2px 0 6px;
      color: #234D6B;
      font-size: 19px;
    }
    .muted {
      color: #69849A;
      line-height: 1.45;
    }
    .tabs, .toolbar, .scene-tabs, .selection-tools {
      display: flex;
      flex-wrap: wrap;
      gap: 7px;
      align-items: center;
    }
    .tabs {
      margin: 14px 0 12px;
    }
    .tab, .tool-btn, .scene-tab, .download-btn {
      border: 1px solid #B9D5E6;
      border-radius: 9px;
      background: #F5FAFD;
      color: #315773;
      padding: 8px 10px;
      font-weight: 600;
    }
    .tab.active, .scene-tab.active {
      border-color: #6EA7CB;
      background: #DFF0FA;
      color: #234D6B;
    }
    .pool {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }
    .pool-item {
      display: flex;
      min-height: 84px;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 4px;
      padding: 8px 5px;
      border: 1px solid #D6E6F0;
      border-radius: 12px;
      background: linear-gradient(145deg, #FFFFFF, #F1F8FC);
      color: #355C76;
      text-align: center;
      font-size: 12px;
      transition: .15s ease;
      user-select: none;
    }
    .pool-item:hover {
      transform: translateY(-2px);
      border-color: #78B0D1;
      box-shadow: 0 5px 14px rgba(71,130,164,.12);
    }
    .pool-icon {
      width: 36px;
      height: 36px;
    }
    .section-label {
      margin: 15px 0 8px;
      color: #55748B;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: .06em;
      text-transform: uppercase;
    }
    .help-card {
      margin-top: 14px;
      padding: 10px 12px;
      border: 1px solid #CDE0EC;
      border-radius: 12px;
      background: #F1F8FC;
      color: #52718A;
      font-size: 12px;
      line-height: 1.5;
    }
    .toolbar {
      justify-content: space-between;
      margin-bottom: 10px;
    }
    .toolbar-left, .toolbar-right {
      display: flex;
      flex-wrap: wrap;
      gap: 7px;
      align-items: center;
    }
    .toolbar button, .download-btn {
      min-height: 38px;
    }
    .scene-tabs {
      margin: 7px 0 10px;
    }
    .scene-tab {
      padding: 7px 12px;
    }
    .stage-wrap {
      overflow: hidden;
      border: 1px solid #C9DFEF;
      border-radius: 15px;
      background: #FBFDFF;
    }
    #stage {
      display: block;
      width: 100%;
      height: min(66vh, 650px);
      min-height: 440px;
      touch-action: none;
      user-select: none;
    }
    .selection-panel {
      display: none;
      margin-top: 12px;
      padding: 12px;
      border: 1px solid #C6DCEB;
      border-radius: 13px;
      background: #F5FAFD;
    }
    .selection-panel.visible {
      display: block;
    }
    .selection-tools {
      margin-top: 9px;
    }
    .field {
      display: flex;
      flex-direction: column;
      gap: 5px;
      min-width: 130px;
      color: #55748B;
      font-size: 12px;
    }
    .field input[type="text"] {
      width: 230px;
      max-width: 100%;
      padding: 8px 9px;
      border: 1px solid #C2D9E8;
      border-radius: 8px;
      background: white;
      color: #294A65;
    }
    .field input[type="range"] {
      width: 150px;
    }
    .field input[type="color"] {
      width: 44px;
      height: 35px;
      padding: 2px;
      border: 1px solid #C2D9E8;
      border-radius: 8px;
      background: white;
    }
    .danger {
      border-color: #E5B8B8 !important;
      background: #FFF4F3 !important;
      color: #9B4D4A !important;
    }
    .status {
      min-height: 20px;
      margin-top: 8px;
      color: #69849A;
      font-size: 12px;
    }
    .privacy {
      margin: 12px 0 0;
      color: #69849A;
      font-size: 12px;
      line-height: 1.45;
    }
    .hidden { display: none !important; }
    @media (max-width: 850px) {
      .app { flex-direction: column; }
      .sidebar { width: 100%; }
      .pool { grid-template-columns: repeat(3, 1fr); }
      #stage { height: 520px; }
    }
    @media (max-width: 560px) {
      .pool { grid-template-columns: repeat(2, 1fr); }
      #stage { min-height: 390px; height: 440px; }
      .toolbar { align-items: flex-start; }
    }
  </style>
</head>
<body>
<div class="app">
  <aside class="sidebar">
    <h2>Библиотека фигур</h2>
    <div class="muted">Выберите элемент, чтобы добавить его на сцену. Затем перетащите фигурку в нужное место.</div>
    <div class="tabs" id="category-tabs"></div>
    <div class="pool" id="pool"></div>
    <div class="help-card">
      Фигуры нейтральны: их цвет, форма и положение не имеют заранее заданного психологического значения.
      Подписи и интерпретации выбираете вы.
    </div>
  </aside>

  <main class="workspace">
    <div class="toolbar">
      <div class="toolbar-left">
        <button class="tool-btn" id="grid-toggle" type="button">Сетка: выкл.</button>
        <button class="tool-btn" id="clear-scene" type="button">Очистить сцену</button>
      </div>
      <div class="toolbar-right">
        <button class="tool-btn" id="export-svg" type="button">Скачать SVG</button>
        <button class="tool-btn" id="export-png" type="button">Скачать PNG</button>
        <button class="tool-btn" id="export-json" type="button">Скачать проект</button>
        <button class="tool-btn" id="import-json-btn" type="button">Открыть проект</button>
        <input id="import-json" class="hidden" type="file" accept=".json,application/json">
      </div>
    </div>

    <div class="scene-tabs" id="scene-tabs"></div>

    <div class="stage-wrap" id="stage-wrap">
      <svg id="stage" xmlns="http://www.w3.org/2000/svg"
           viewBox="0 0 1200 760" aria-label="Доска-сцена">
        <defs>
          <pattern id="grid-pattern" width="32" height="32"
                   patternUnits="userSpaceOnUse">
            <circle cx="2" cy="2" r="1.2" fill="#D9E7F0"/>
          </pattern>
          <linearGradient id="stage-gradient" x1="0" x2="1" y1="0" y2="1">
            <stop offset="0%" stop-color="#FCFEFF"/>
            <stop offset="100%" stop-color="#F3F9FD"/>
          </linearGradient>
        </defs>
        <rect id="stage-background" x="0" y="0" width="1200" height="760"
              fill="url(#stage-gradient)"/>
        <rect id="stage-grid" x="0" y="0" width="1200" height="760"
              fill="url(#grid-pattern)" opacity="0"/>
        <g id="scene-items"></g>
        <g id="drop-hint" pointer-events="none">
          <text x="600" y="365" text-anchor="middle"
                fill="#8BA5B8" font-size="24" font-family="Segoe UI, Arial">
            Добавьте фигуры из библиотеки
          </text>
          <text x="600" y="399" text-anchor="middle"
                fill="#A0B4C3" font-size="16" font-family="Segoe UI, Arial">
            Перемещайте их и создавайте собственную композицию
          </text>
        </g>
      </svg>
    </div>

    <div class="selection-panel" id="selection-panel">
      <strong id="selection-title">Выбранный элемент</strong>
      <div class="selection-tools">
        <label class="field">
          Подпись
          <input id="node-label" type="text" maxlength="60" placeholder="Например: Я">
        </label>
        <label class="field">
          Цвет
          <input id="node-color" type="color" value="#72A9C8">
        </label>
        <label class="field">
          Размер
          <input id="node-size" type="range" min="0.65" max="1.6" step="0.05" value="1">
        </label>
        <label class="field">
          Поворот
          <input id="node-rotation" type="range" min="-180" max="180" step="5" value="0">
        </label>
        <button class="tool-btn danger" id="delete-node" type="button">Удалить фигуру</button>
      </div>
    </div>

    <div class="status" id="status"></div>
    <div class="privacy">
      Упражнение добровольное: можно сделать паузу, изменить сцену или завершить работу в любой момент.
      Не используйте доску для самостоятельной проработки ситуации, в которой вы чувствуете себя небезопасно.
      Сцена хранится в текущей вкладке; для продолжения работы скачайте файл проекта JSON.
    </div>
  </main>
</div>

<script>
(() => {
  const POOL = __POOL_JSON__;
  const svgNS = "http://www.w3.org/2000/svg";
  const categories = [
    {id: "people", label: "Люди", types: ["person", "child"]},
    {id: "symbols", label: "Символы", types: ["circle", "star", "cloud", "heart"]},
    {id: "objects", label: "Объекты", types: ["chair", "house", "door", "tree", "table", "wall", "boundary"]}
  ];

  const stage = document.getElementById("stage");
  const layer = document.getElementById("scene-items");
  const hint = document.getElementById("drop-hint");
  const pool = document.getElementById("pool");
  const tabsRoot = document.getElementById("category-tabs");
  const sceneTabs = document.getElementById("scene-tabs");
  const selectionPanel = document.getElementById("selection-panel");
  const status = document.getElementById("status");
  const grid = document.getElementById("stage-grid");

  let scenes = [{name: "Сцена 1", nodes: []}];
  let activeScene = 0;
  let activeCategory = "people";
  let selectedId = null;
  let nextId = 1;
  let gridOn = false;
  let dragState = null;

  const currentScene = () => scenes[activeScene];

  function setStatus(message) {
    status.textContent = message || "";
  }

  function svgEl(tag, attrs = {}) {
    const element = document.createElementNS(svgNS, tag);
    for (const [key, value] of Object.entries(attrs)) {
      element.setAttribute(key, value);
    }
    return element;
  }

  function addShape(type, color, parent) {
    const add = (tag, attrs) => parent.appendChild(svgEl(tag, attrs));

    if (type === "person" || type === "child") {
      const scale = type === "child" ? 0.82 : 1;
      const group = svgEl("g", {transform: `scale(${scale})`});
      parent.appendChild(group);
      group.appendChild(svgEl("circle", {
        cx: 0, cy: -24, r: 12,
        fill: color, stroke: "#426782", "stroke-width": 2
      }));
      group.appendChild(svgEl("path", {
        d: "M-17 30 Q-17 3 -12 -5 Q0 -13 12 -5 Q17 3 17 30 Z",
        fill: color, stroke: "#426782", "stroke-width": 2,
        "stroke-linejoin": "round"
      }));
      group.appendChild(svgEl("path", {
        d: "M-10 2 L-25 17 M10 2 L25 17 M-8 29 L-15 47 M8 29 L15 47",
        fill: "none", stroke: "#426782", "stroke-width": 5,
        "stroke-linecap": "round"
      }));
    } else if (type === "circle") {
      add("circle", {
        cx: 0, cy: 0, r: 30,
        fill: color, "fill-opacity": .82,
        stroke: "#426782", "stroke-width": 2.5
      });
    } else if (type === "star") {
      add("path", {
        d: "M0-36 L9-12 L35-11 L15 5 L22 31 L0 16 L-22 31 L-15 5 L-35-11 L-9-12 Z",
        fill: color, stroke: "#927333", "stroke-width": 2
      });
    } else if (type === "cloud") {
      add("path", {
        d: "M-31 13 Q-39 -2 -23 -9 Q-20 -29 0 -21 Q15 -35 25 -17 Q42 -14 36 2 Q40 17 23 19 L-22 19 Q-36 19 -31 13 Z",
        fill: color, stroke: "#647D96", "stroke-width": 2.5
      });
    } else if (type === "heart") {
      add("path", {
        d: "M0 29 C-8 19 -34 2 -31 -15 C-29 -32 -8 -34 0 -19 C9 -34 30 -32 32 -15 C34 2 9 20 0 29 Z",
        fill: color, stroke: "#925D66", "stroke-width": 2
      });
    } else if (type === "chair") {
      add("path", {
        d: "M-20 -25 L18 -25 L18 3 L-20 3 Z M-20 3 L-20 31 M18 3 L18 31 M-20 3 L18 3",
        fill: "none", stroke: color, "stroke-width": 7,
        "stroke-linecap": "round", "stroke-linejoin": "round"
      });
    } else if (type === "house") {
      add("path", {
        d: "M-36 -3 L0 -33 L36 -3 L29 0 L29 32 L-29 32 L-29 0 Z",
        fill: color, "fill-opacity": .82,
        stroke: "#765744", "stroke-width": 2.5,
        "stroke-linejoin": "round"
      });
      add("rect", {
        x: -7, y: 9, width: 14, height: 23, rx: 2,
        fill: "#FFF9F1", stroke: "#765744", "stroke-width": 2
      });
    } else if (type === "door") {
      add("rect", {
        x: -25, y: -38, width: 50, height: 76, rx: 3,
        fill: color, "fill-opacity": .78,
        stroke: "#765744", "stroke-width": 3
      });
      add("circle", {cx: 14, cy: 3, r: 3, fill: "#765744"});
    } else if (type === "tree") {
      add("path", {
        d: "M-7 8 L-12 42 L12 42 L7 8 Z",
        fill: "#A77B55", stroke: "#795A42", "stroke-width": 2
      });
      add("circle", {cx: 0, cy: -10, r: 27, fill: color, stroke: "#547B5A", "stroke-width": 2});
      add("circle", {cx: -18, cy: 1, r: 17, fill: color, stroke: "#547B5A", "stroke-width": 2});
      add("circle", {cx: 18, cy: 1, r: 17, fill: color, stroke: "#547B5A", "stroke-width": 2});
    } else if (type === "table") {
      add("path", {
        d: "M-34 -12 L34 -12 L30 1 L-30 1 Z M-24 1 L-28 33 M24 1 L28 33",
        fill: color, stroke: "#765D4A", "stroke-width": 4,
        "stroke-linejoin": "round", "stroke-linecap": "round"
      });
    } else if (type === "wall") {
      add("rect", {
        x: -34, y: -39, width: 68, height: 78, rx: 5,
        fill: color, "fill-opacity": .66,
        stroke: "#677B8A", "stroke-width": 2.5
      });
      add("path", {
        d: "M-34 -10 H34 M-34 16 H34 M0 -39 V-10 M-16 -10 V16 M12 -10 V16 M-2 16 V39",
        fill: "none", stroke: "#FFFFFF", "stroke-opacity": .8,
        "stroke-width": 2
      });
    } else if (type === "boundary") {
      add("ellipse", {
        cx: 0, cy: 0, rx: 42, ry: 28,
        fill: "none", stroke: color, "stroke-width": 4,
        "stroke-dasharray": "9 7"
      });
    }
  }

  function addPoolIcon(parent, item) {
    const icon = svgEl("svg", {
      viewBox: "-48 -48 96 96",
      class: "pool-icon",
      "aria-hidden": "true"
    });
    addShape(item.type, item.color, icon);
    parent.appendChild(icon);
  }

  function renderTabs() {
    tabsRoot.innerHTML = "";
    categories.forEach(category => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "tab" + (activeCategory === category.id ? " active" : "");
      button.textContent = category.label;
      button.onclick = () => {
        activeCategory = category.id;
        renderTabs();
        renderPool();
      };
      tabsRoot.appendChild(button);
    });
  }

  function renderPool() {
    pool.innerHTML = "";
    const category = categories.find(item => item.id === activeCategory);
    const items = POOL.filter(item => category.types.includes(item.type));

    items.forEach(item => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "pool-item";
      button.draggable = true;
      button.title = "Нажмите, чтобы добавить, или перетащите на сцену";

      addPoolIcon(button, item);

      const label = document.createElement("span");
      label.textContent = item.label;
      button.appendChild(label);

      button.onclick = () => addNode(item);
      button.ondragstart = event => {
        event.dataTransfer.setData("text/plain", item.id);
        event.dataTransfer.effectAllowed = "copy";
      };

      pool.appendChild(button);
    });
  }

  function renderSceneTabs() {
    sceneTabs.innerHTML = "";

    scenes.forEach((scene, index) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "scene-tab" + (index === activeScene ? " active" : "");
      button.textContent = scene.name;
      button.title = "Дважды нажмите, чтобы переименовать сцену";
      button.onclick = () => switchScene(index);
      button.ondblclick = event => {
        event.preventDefault();
        const newName = prompt("Название сцены:", scene.name);
        if (newName && newName.trim()) {
          scene.name = newName.trim().slice(0, 40);
          renderSceneTabs();
        }
      };
      sceneTabs.appendChild(button);
    });

    if (scenes.length < 6) {
      const addButton = document.createElement("button");
      addButton.type = "button";
      addButton.className = "scene-tab";
      addButton.textContent = "＋ Новая сцена";
      addButton.onclick = addScene;
      sceneTabs.appendChild(addButton);
    }

    const hintText = document.createElement("span");
    hintText.className = "muted";
    hintText.textContent = "Двойной клик по вкладке — переименовать";
    sceneTabs.appendChild(hintText);
  }

  function switchScene(index) {
    activeScene = index;
    selectedId = null;
    renderSceneTabs();
    renderStage();
    updateSelectionPanel();
  }

  function addScene() {
    if (scenes.length >= 6) return;
    scenes.push({
      name: `Сцена ${scenes.length + 1}`,
      nodes: []
    });
    activeScene = scenes.length - 1;
    selectedId = null;
    renderSceneTabs();
    renderStage();
    updateSelectionPanel();
    setStatus("Создана новая пустая сцена.");
  }

  function addNode(item, position = null) {
    const offset = (currentScene().nodes.length % 8) * 18;
    const node = {
      id: `figure_${nextId++}`,
      type: item.type,
      label: item.label,
      color: item.color,
      size: 1,
      rotation: 0,
      x: position ? position.x : 440 + offset,
      y: position ? position.y : 300 + offset
    };

    currentScene().nodes.push(node);
    selectedId = node.id;
    renderStage();
    updateSelectionPanel();
    setStatus(`Добавлена фигура «${item.label}». Перетащите её в нужное место.`);
  }

  function findSelected() {
    return currentScene().nodes.find(node => node.id === selectedId) || null;
  }

  function renderNode(node) {
    const group = svgEl("g", {
      "data-node-id": node.id,
      transform: `translate(${node.x} ${node.y}) rotate(${node.rotation}) scale(${node.size})`,
      tabindex: "0",
      role: "button",
      "aria-label": node.label || "Фигура"
    });

    if (node.id === selectedId) {
      group.appendChild(svgEl("circle", {
        class: "selection-ring",
        cx: 0, cy: 2, r: 54,
        fill: "#DFF1FA",
        "fill-opacity": .55,
        stroke: "#347FA7",
        "stroke-width": 2.5,
        "stroke-dasharray": "6 5"
      }));
    }

    addShape(node.type, node.color, group);

    const caption = svgEl("text", {
      x: 0,
      y: 67,
      "text-anchor": "middle",
      "font-family": "Segoe UI, Arial, sans-serif",
      "font-size": 15,
      "font-weight": 600,
      fill: "#294A65",
      stroke: "#FFFFFF",
      "stroke-width": 4,
      "paint-order": "stroke",
      "stroke-linejoin": "round",
      "pointer-events": "none"
    });
    caption.textContent = node.label || "Без подписи";
    group.appendChild(caption);

    return group;
  }

  function renderStage() {
    layer.innerHTML = "";
    currentScene().nodes.forEach(node => layer.appendChild(renderNode(node)));
    hint.style.display = currentScene().nodes.length ? "none" : "block";
    grid.setAttribute("opacity", gridOn ? "1" : "0");
  }

  function updateSelectionPanel() {
    const node = findSelected();

    if (!node) {
      selectionPanel.classList.remove("visible");
      return;
    }

    selectionPanel.classList.add("visible");
    document.getElementById("selection-title").textContent =
      `Выбрано: ${node.label || "Без подписи"}`;
    document.getElementById("node-label").value = node.label || "";
    document.getElementById("node-color").value = node.color || "#72A9C8";
    document.getElementById("node-size").value = node.size || 1;
    document.getElementById("node-rotation").value = node.rotation || 0;
  }

  function pointerToSvg(event) {
    const point = stage.createSVGPoint();
    point.x = event.clientX;
    point.y = event.clientY;
    const matrix = stage.getScreenCTM();
    if (!matrix) return {x: 600, y: 380};
    const local = point.matrixTransform(matrix.inverse());
    return {x: local.x, y: local.y};
  }

  stage.addEventListener("pointerdown", event => {
    const group = event.target.closest("[data-node-id]");
    if (!group) {
      selectedId = null;
      renderStage();
      updateSelectionPanel();
      return;
    }

    const nodeId = group.getAttribute("data-node-id");
    const node = currentScene().nodes.find(item => item.id === nodeId);
    if (!node) return;

    selectedId = nodeId;
    const point = pointerToSvg(event);
    dragState = {
      id: nodeId,
      offsetX: point.x - node.x,
      offsetY: point.y - node.y
    };

    stage.setPointerCapture(event.pointerId);
    renderStage();
    updateSelectionPanel();
    event.preventDefault();
  });

  stage.addEventListener("pointermove", event => {
    if (!dragState) return;

    const node = currentScene().nodes.find(item => item.id === dragState.id);
    if (!node) return;

    const point = pointerToSvg(event);
    node.x = Math.max(50, Math.min(1150, point.x - dragState.offsetX));
    node.y = Math.max(55, Math.min(705, point.y - dragState.offsetY));
    renderStage();
  });

  function stopDragging() {
    dragState = null;
  }

  stage.addEventListener("pointerup", stopDragging);
  stage.addEventListener("pointercancel", stopDragging);

  stage.addEventListener("keydown", event => {
    const group = event.target.closest("[data-node-id]");
    if (!group || !["Enter", " "].includes(event.key)) return;

    event.preventDefault();
    selectedId = group.getAttribute("data-node-id");
    renderStage();
    updateSelectionPanel();
  });

  const selectedLabel = document.getElementById("node-label");
  selectedLabel.addEventListener("input", () => {
    const node = findSelected();
    if (!node) return;
    node.label = selectedLabel.value;
    renderStage();
    document.getElementById("selection-title").textContent =
      `Выбрано: ${node.label || "Без подписи"}`;
  });

  document.getElementById("node-color").addEventListener("input", event => {
    const node = findSelected();
    if (!node) return;
    node.color = event.target.value;
    renderStage();
  });

  document.getElementById("node-size").addEventListener("input", event => {
    const node = findSelected();
    if (!node) return;
    node.size = Number(event.target.value);
    renderStage();
  });

  document.getElementById("node-rotation").addEventListener("input", event => {
    const node = findSelected();
    if (!node) return;
    node.rotation = Number(event.target.value);
    renderStage();
  });

  document.getElementById("delete-node").onclick = () => {
    if (!selectedId) return;
    currentScene().nodes = currentScene().nodes.filter(
      node => node.id !== selectedId
    );
    selectedId = null;
    renderStage();
    updateSelectionPanel();
    setStatus("Фигура удалена.");
  };

  document.getElementById("grid-toggle").onclick = event => {
    gridOn = !gridOn;
    event.target.textContent = `Сетка: ${gridOn ? "вкл." : "выкл."}`;
    renderStage();
  };

  document.getElementById("clear-scene").onclick = () => {
    if (!currentScene().nodes.length) return;
    if (!confirm("Очистить текущую сцену? Это действие нельзя отменить.")) return;
    currentScene().nodes = [];
    selectedId = null;
    renderStage();
    updateSelectionPanel();
    setStatus("Текущая сцена очищена.");
  };

  stage.addEventListener("dragover", event => {
    event.preventDefault();
    event.dataTransfer.dropEffect = "copy";
  });

  stage.addEventListener("drop", event => {
    event.preventDefault();
    const poolId = event.dataTransfer.getData("text/plain");
    const item = POOL.find(entry => entry.id === poolId);
    if (!item) return;
    addNode(item, pointerToSvg(event));
  });

  function makeExportSvg() {
    const clone = stage.cloneNode(true);
    clone.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    clone.setAttribute("width", "1600");
    clone.setAttribute("height", "1013");
    clone.querySelectorAll(".selection-ring").forEach(el => el.remove());

    const dropHint = clone.querySelector("#drop-hint");
    if (dropHint && currentScene().nodes.length) {
      dropHint.remove();
    }
    return new XMLSerializer().serializeToString(clone);
  }

  function downloadBlob(blob, filename) {
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1200);
  }

  document.getElementById("export-svg").onclick = () => {
    const data = makeExportSvg();
    downloadBlob(
      new Blob([data], {type: "image/svg+xml;charset=utf-8"}),
      "psychodrama_scene.svg"
    );
    setStatus("SVG-файл подготовлен для скачивания.");
  };

  document.getElementById("export-png").onclick = () => {
    const source = makeExportSvg();
    const url = URL.createObjectURL(
      new Blob([source], {type: "image/svg+xml;charset=utf-8"})
    );
    const image = new Image();

    image.onload = () => {
      const canvas = document.createElement("canvas");
      canvas.width = 1600;
      canvas.height = 1013;
      const context = canvas.getContext("2d");
      context.fillStyle = "#F8FCFF";
      context.fillRect(0, 0, canvas.width, canvas.height);
      context.drawImage(image, 0, 0, canvas.width, canvas.height);
      canvas.toBlob(blob => {
        if (blob) {
          downloadBlob(blob, "psychodrama_scene.png");
          setStatus("PNG-файл подготовлен для скачивания.");
        }
        URL.revokeObjectURL(url);
      }, "image/png");
    };

    image.onerror = () => {
      URL.revokeObjectURL(url);
      setStatus("Не удалось создать PNG. Попробуйте скачать SVG.");
    };

    image.src = url;
  };

  document.getElementById("export-json").onclick = () => {
    const data = {
      version: 1,
      scenes: scenes,
      activeScene: activeScene
    };
    downloadBlob(
      new Blob([JSON.stringify(data, null, 2)], {
        type: "application/json;charset=utf-8"
      }),
      "psychodrama_project.json"
    );
    setStatus("Файл проекта JSON подготовлен для скачивания.");
  };

  const importInput = document.getElementById("import-json");
  document.getElementById("import-json-btn").onclick = () => importInput.click();

  importInput.addEventListener("change", async event => {
    const file = event.target.files && event.target.files[0];
    if (!file) return;

    try {
      const data = JSON.parse(await file.text());
      if (!Array.isArray(data.scenes) || !data.scenes.length) {
        throw new Error("В файле нет списка сцен.");
      }

      const allowedTypes = new Set(POOL.map(item => item.type));
      const cleanScenes = data.scenes.slice(0, 6).map((scene, index) => ({
        name: String(scene.name || `Сцена ${index + 1}`).slice(0, 40),
        nodes: Array.isArray(scene.nodes)
          ? scene.nodes
              .filter(node => node && allowedTypes.has(node.type))
              .map(node => ({
                id: String(node.id || `figure_${nextId++}`),
                type: node.type,
                label: String(node.label || "").slice(0, 60),
                color: /^#[0-9A-Fa-f]{6}$/.test(node.color)
                  ? node.color
                  : "#72A9C8",
                size: Math.max(0.65, Math.min(1.6, Number(node.size) || 1)),
                rotation: Number(node.rotation) || 0,
                x: Math.max(50, Math.min(1150, Number(node.x) || 600)),
                y: Math.max(55, Math.min(705, Number(node.y) || 380))
              }))
          : []
      }));

      scenes = cleanScenes.length ? cleanScenes : [{name: "Сцена 1", nodes: []}];
      activeScene = Math.max(
        0,
        Math.min(scenes.length - 1, Number(data.activeScene) || 0)
      );
      selectedId = null;
      nextId += 1;
      renderSceneTabs();
      renderStage();
      updateSelectionPanel();
      setStatus("Проект загружен.");
    } catch (error) {
      setStatus(`Не удалось открыть проект: ${error.message}`);
    } finally {
      importInput.value = "";
    }
  });

  renderTabs();
  renderPool();
  renderSceneTabs();
  renderStage();
})();
</script>
</body>
</html>
"""


st.title("Психодрама: интерактивная сцена")
st.write(
    "Добавляйте фигуры, расставляйте их на сцене и создавайте собственную "
    "визуальную композицию."
)

st.info(
    "Это визуальный инструмент для исследования ситуации, а не диагностика. "
    "Положение, форма и цвет фигур не интерпретируются автоматически. "
    "Упражнение можно остановить в любой момент."
)

components.html(
    APP_HTML.replace(
        "__POOL_JSON__",
        json.dumps(POOL, ensure_ascii=False),
    ),
    height=1010,
    scrolling=False,
)
