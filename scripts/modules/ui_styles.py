# scripts/modules/ui_styles.py
#
# === HISTORIK ===
# * v4.0 (2025-08-16): Total visuell omdesign till ett mörkblått tema.
# * v4.1 (2025-08-16): Lade till förberedande, initialt dolda stilar för
#   framtida verktyg enligt "Operation: Dold Grund".
# * v5.0 (2025-08-16): Lade till CSS-regler för det nya interaktiva filträdet,
#   inklusive styling för noder, ikoner, taggar och indrag.
# * v5.1 (2025-08-16): Implementerat fullständigt anpassade (custom) tri-state
#   kryssrutor för att matcha den visuella specifikationen.
#
# === TILLÄMPADE REGLER (Frankensteen v5.6) ===
# - Fullständig Kod: Verifierat komplett.
# - API-kontraktsverifiering: Alla färg- och fontvariabler följer `:root`-kontraktet.

CSS_STYLES = """
:root {
    --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    --font-mono: ui-monospace, "JetBrains Mono", "SF Mono", Consolas, Menlo, monospace;
    --bg-color: #2c3e50;
    --panel-bg-color: #34495e;
    --border-color: #4a6572;
    --text-color: #ecf0f1;
    --text-color-muted: #bdc3c7;
    --header-bg-color: #2c3e50;
    --button-bg: #3498db;
    --button-hover-bg: #2980b9;
    --button-text: #ffffff;
    --input-bg-color: #2c3e50;
    --input-border-color: #4a6572;
    --resizer-color: #4a6572;
    --resizer-hover-color: #3498db;
    --ribbon-tab-active-bg: #34495e;
    --ribbon-content-bg: #34495e;
    --cb-checked-bg: #2ecc71;
    --cb-indeterminate-bg: #f39c12;
    --cb-border-color: #7f8c8d;
    --cb-focus-ring: #3498db;
}

* { box-sizing: border-box; }

body, html {
    margin: 0; padding: 0; height: 100vh; width: 100vw;
    font-family: var(--font-sans); font-size: 14px;
    background-color: var(--bg-color); color: var(--text-color);
    display: flex; flex-direction: column; overflow: hidden;
}

h2 { font-weight: 500; color: var(--text-color); }

.main-container {
    display: flex; flex-grow: 1;
    height: calc(100% - 85px);
    position: relative; /* Nödvändigt för full-page overlay */
}

/* --- Ribbon Header --- */
.header-ribbon {
    height: 85px;
    border-bottom: 1px solid var(--border-color);
    background-color: var(--header-bg-color);
    width: 100%;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
}

.top-bar {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding: 0 12px;
}

.ribbon-tabs { display: flex; gap: 4px; }
.ribbon-tab {
    background: none; border: 1px solid transparent; border-bottom: none;
    padding: 6px 12px; border-radius: 4px 4px 0 0; cursor: pointer;
    font-size: 14px; margin-bottom: -1px; color: var(--text-color-muted);
    transition: background-color 0.2s ease, color 0.2s ease;
}
.ribbon-tab.active {
    background-color: var(--ribbon-content-bg);
    border-color: var(--border-color);
    border-bottom-color: var(--ribbon-content-bg);
    color: var(--text-color);
}
.ribbon-tab:hover {
    background-color: var(--panel-bg-color);
    color: var(--text-color);
}
.search-container { padding-bottom: 4px; }

.ribbon-content {
    background-color: var(--ribbon-content-bg);
    border-top: 1px solid var(--border-color);
    flex-grow: 1;
    display: flex;
    align-items: stretch;
    padding: 4px 12px;
}
.ribbon-pane { display: none; width: 100%; height: 100%; align-items: center; gap: 16px; }
.ribbon-pane.active { display: flex; }
.ribbon-group {
    display: flex;
    align-items: center;
    gap: 8px;
    height: 100%;
    padding: 0 16px;
    border-right: 1px solid var(--border-color);
}
.ribbon-group:first-child { padding-left: 4px; }

/* --- Global Component Styles --- */
button, .ribbon-group button {
    background-color: var(--button-bg);
    color: var(--button-text);
    border: 1px solid var(--button-hover-bg);
    border-radius: 5px;
    padding: 8px 16px;
    font-size: 14px;
    font-weight: 500;
    transition: background-color 0.2s ease;
    cursor: pointer;
}
button:hover, .ribbon-group button:hover {
    background-color: var(--button-hover-bg);
}

input[type="search"] {
    background-color: var(--input-bg-color);
    border: 1px solid var(--input-border-color);
    color: var(--text-color);
    padding: 8px;
    width: 250px;
    border-radius: 5px;
}
input[type="search"]:focus {
    outline: none;
    border-color: var(--resizer-hover-color);
}

/* --- Main Panes --- */
.left-pane, .right-pane {
    background-color: var(--panel-bg-color);
    padding: 12px;
    overflow-y: auto;
}
.left-pane {
    width: 33.33%; max-width: 80%; min-width: 200px;
    border-right: 1px solid var(--border-color); flex-shrink: 0;
}
.right-pane { flex-grow: 1; }
.resizer {
    width: 5px; cursor: col-resize;
    background-color: var(--resizer-color);
    flex-shrink: 0; user-select: none;
    transition: background-color 0.2s ease;
}
.resizer:hover { background-color: var(--resizer-hover-color); }

/* --- Dolda Verktygs-Containrar (Operation: Dold Grund) --- */
.tool-container {
    display: none; /* Allt inuti detta är dolt som standard */
    height: 100%;
    width: 100%;
}
.full-page-container {
    position: absolute;
    inset: 0;
    background-color: var(--panel-bg-color);
    z-index: 100;
    padding: 12px;
    overflow-y: auto;
}

/* --- File Tree --- */
.file-tree, .file-tree ul {
    list-style: none;
    padding-left: 0;
    margin: 0;
    font-family: var(--font-mono);
    font-size: 13px;
}
.file-tree li { padding: 1px 0; }
.tree-node > ul { padding-left: 20px; }
.toggle-icon {
    cursor: pointer; user-select: none;
    width: 18px; height: 18px; text-align: center; line-height: 18px;
    color: var(--text-color-muted); flex-shrink: 0;
}
.toggle-icon:hover { color: var(--text-color); }
.tree-node.collapsed > ul { display: none; }
.node-label {
    display: flex; align-items: center; gap: 6px;
    cursor: pointer; padding: 2px 4px; border-radius: 3px;
}
.node-label:hover { background-color: rgba(0,0,0,0.1); }
.node-icon { font-style: normal; }
.node-text { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* --- Custom Tri-state Checkbox Styles --- */
.node-label input[type="checkbox"] {
    appearance: none; -webkit-appearance: none;
    margin: 0; flex-shrink: 0;
    width: 16px; height: 16px;
    border: 1.5px solid var(--cb-border-color);
    border-radius: 3px;
    background-color: transparent;
    cursor: pointer;
    position: relative;
    transition: background-color 0.15s ease-in-out, border-color 0.15s ease-in-out;
}
.node-label input[type="checkbox"]:focus-visible {
    outline: 2px solid var(--cb-focus-ring);
    outline-offset: 1px;
}
.node-label input[type="checkbox"]:checked {
    background-color: var(--cb-checked-bg);
    border-color: var(--cb-checked-bg);
}
.node-label input[type="checkbox"]:checked::before {
    content: '✔';
    position: absolute;
    color: white;
    font-size: 12px;
    line-height: 14px;
    left: 2px;
    top: -1px;
}
.node-label input[type="checkbox"]:indeterminate {
    background-color: var(--cb-indeterminate-bg);
    border-color: var(--cb-indeterminate-bg);
}
.node-label input[type="checkbox"]:indeterminate::before {
    content: '';
    position: absolute;
    background-color: white;
    width: 8px;
    height: 2px;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
}
/* --- End Custom Checkbox --- */

.metadata-tags {
    display: flex; gap: 4px;
    margin-left: auto; padding-left: 8px;
}
.metadata-tag {
    padding: 1px 6px; border-radius: 99px; font-size: 10px;
    background-color: var(--bg-color); border: 1px solid var(--border-color);
    color: var(--text-color-muted); white-space: nowrap;
}
"""
# scripts/modules/ui_styles.py
