# scripts/modules/ui_styles.py
#
# === HISTORIK ===
# * v4.0 (2025-08-16): Total visuell omdesign till ett mörkblått tema.
# * v4.1 (2025-08-16): Lade till dolda containrar för framtida verktyg.
# * v5.0 (2025-08-16): Lade till CSS-regler för det interaktiva filträdet.
# * v5.1 (2025-08-16): Implementerat anpassade tri-state kryssrutor.
# * v5.2 (2025-08-16): Korrigerat layout och indentering för filträdet.
# * v5.3 (2025-08-16): Lade till stilar för filgranskningsmodalen.
# * v5.4 (2025-08-17): Lade till en `.size-tag`-klass för att visa filstorlekar.
# * v5.5 (2025-08-17): Lade till fullständig styling för AI Performance-dashboarden.
# * v5.6 (2025-08-17): (Help me God - Domslut) Korrigerat en CSS-specificitetskonflikt.
#   `.full-page-container` är nu `display: none` som standard och visas endast
#   med `.active`-klassen, vilket löser buggen där den alltid var synlig.
#
# === TILLÄMPADE REGLER (Frankensteen v5.6) ===
# - Grundbulten v3.3: Denna ändring följer den uppgraderade processen för transparens.
# - Help me God: Denna korrigering är resultatet av en grundorsaksanalys.

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
.inline { display: inline-flex; align-items: center; gap: 6px; }

.main-container {
    display: flex; flex-grow: 1;
    height: calc(100% - 85px);
    position: relative;
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
button.primary { background-color: var(--button-bg); }
button.info { background-color: var(--info-color, #17a2b8); }

input[type="search"], input[type="date"] {
    background-color: var(--input-bg-color);
    border: 1px solid var(--input-border-color);
    color: var(--text-color);
    padding: 8px;
    border-radius: 5px;
}
input[type="search"] { width: 250px; }
input[type="search"]:focus, input[type="date"]:focus {
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
    display: none; 
    height: 100%;
    width: 100%;
}
.tool-container.active {
    display: block;
}
.full-page-container {
    position: absolute;
    inset: 0;
    background-color: var(--bg-color);
    z-index: 100;
    display: none; /* KORRIGERING: Dold som standard */
}
.full-page-container.active {
    display: flex; /* KORRIGERING: Visas endast när aktiv */
    flex-direction: column;
}
.full-page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px;
    border-bottom: 1px solid var(--border-color);
    flex-shrink: 0;
}
#close-full-page-btn {
    background: none; border: none; font-size: 1.5rem; color: var(--text-color-muted);
}
#close-full-page-btn:hover { color: var(--text-color); }

.full-page-content {
    flex-grow: 1;
    overflow-y: auto;
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

/* --- AI Performance Styles --- */
.filter-bar { display: flex; gap: 10px; align-items: flex-end; flex-wrap: wrap; }
.filter-group { display: flex; flex-direction: column; gap: 4px; }
.filter-group label { font-size: .85rem; color: var(--text-color-muted); }
.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }
.kpi { border: 1px solid var(--border-color); border-radius: 8px; background: var(--panel-bg-color); padding: 10px; }
.kpi h4 { margin: 0 0 6px 0; font-size: 0.95rem; color: var(--text-color-muted); }
.kpi .big { font-size: 1.6rem; font-weight: 700; color: var(--text-color); }
.kpi .sub { font-size: .85rem; color: var(--text-color-muted); }
.chart-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 12px; }
.chart-card { border: 1px solid var(--border-color); border-radius: 8px; background: var(--panel-bg-color); padding: 10px; display: flex; flex-direction: column; gap: 6px; }
.chart-card h3 { margin: 0 0 4px 0; font-size: 1.05rem; border-bottom: 1px solid var(--border-color); padding-bottom: 6px; }
.chart-container { position: relative; height: 300px; }
.table-card { border: 1px solid var(--border-color); border-radius: 8px; background: var(--panel-bg-color); padding: 10px; }
.table-card table { width: 100%; border-collapse: collapse; font-size: .9rem; }
.table-card th, .table-card td { border: 1px solid var(--border-color); padding: 6px; text-align: left; }
.table-card th { background: var(--bg-color); }

/* --- File Tree --- */
.file-tree, .file-tree ul {
    list-style: none;
    padding-left: 0;
    margin: 0;
    font-family: var(--font-mono);
    font-size: 13px;
}
.file-tree li {
    padding: 1px 0;
}
.file-tree ul {
    padding-left: 20px;
}
.tree-node.collapsed > ul {
    display: none;
}
.node-label {
    display: flex;
    align-items: center;
    gap: 6px;
    cursor: pointer;
    padding: 2px 4px;
    border-radius: 3px;
    width: 100%;
}
.node-label:hover {
    background-color: rgba(255,255,255,0.05);
}
.toggle-icon {
    cursor: pointer; user-select: none;
    width: 18px; height: 18px; text-align: center; line-height: 18px;
    color: var(--text-color-muted); flex-shrink: 0;
}
.toggle-icon:hover {
    color: var(--text-color);
}
.node-icon {
    font-style: normal;
}
.node-text {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

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
.metadata-tag, .size-tag {
    padding: 1px 6px; border-radius: 99px; font-size: 10px;
    background-color: var(--bg-color); border: 1px solid var(--border-color);
    color: var(--text-color-muted); white-space: nowrap;
}
.size-tag {
    min-width: 45px;
    text-align: right;
}


/* --- File Viewer Modal --- */
.modal-overlay {
    position: fixed;
    inset: 0;
    background-color: rgba(0, 0, 0, 0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}
.modal-overlay.hidden {
    display: none;
}
.modal-panel {
    background-color: var(--panel-bg-color);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    width: 90vw;
    max-width: 1200px;
    height: 85vh;
    display: flex;
    flex-direction: column;
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}
.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    border-bottom: 1px solid var(--border-color);
    flex-shrink: 0;
}
.modal-header h3 {
    margin: 0;
    font-size: 1.1rem;
    font-family: var(--font-mono);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.modal-actions {
    display: flex;
    gap: 8px;
    align-items: center;
}
.modal-actions button {
    padding: 6px 12px;
}
#modal-copy-path, #modal-close-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    padding: 0 8px;
    color: var(--text-color-muted);
}
#modal-copy-path:hover, #modal-close-btn:hover {
    color: var(--text-color);
}
.modal-content {
    flex-grow: 1;
    overflow-y: auto;
    padding: 16px;
}
.modal-content pre {
    margin: 0;
    font-family: var(--font-mono);
    white-space: pre-wrap;
    word-break: break-all;
}
.modal-state {
    padding: 20px;
    text-align: center;
    color: var(--text-color-muted);
}
.modal-state.hidden {
    display: none;
}
"""
# scripts/modules/ui_styles.py
