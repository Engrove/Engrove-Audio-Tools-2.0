# scripts/modules/ui_styles.py
#
# === HISTORIK ===
# * v2.1 (2025-08-15): Korrigerat header-layout för att placera sökfältet
#   permanent till höger. Justerat positionering för ribbon-etiketter.
#
# === TILLÄMPADE REGLER (Frankensteen v5.4) ===
# - Fullständig kod, alltid.

CSS_STYLES = """
:root {
    --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    --font-mono: ui-monospace, "JetBrains Mono", "SF Mono", Consolas, Menlo, monospace;
    --bg-color: #f0f0f0;
    --panel-bg-color: #ffffff;
    --border-color: #cccccc;
    --text-color: #1a1a1a;
    --header-bg-color: #f0f0f0;
    --button-hover-bg: #e9e9e9;
    --input-bg-color: #ffffff;
    --input-border-color: #b0b0b0;
    --resizer-color: #dddddd;
    --resizer-hover-color: #0d6efd;
    --ribbon-tab-active-bg: #f9f9f9;
    --ribbon-content-bg: #f9f9f9;
}

* { box-sizing: border-box; }

body, html {
    margin: 0; padding: 0; height: 100vh; width: 100vw;
    font-family: var(--font-sans); font-size: 14px;
    background-color: var(--bg-color); color: var(--text-color);
    display: flex; flex-direction: column; overflow: hidden;
}

.main-container {
    display: flex; flex-grow: 1;
    height: calc(100% - 85px);
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

.ribbon-tabs {
    display: flex;
    gap: 4px;
}

.ribbon-tab {
    background: none;
    border: 1px solid transparent;
    border-bottom: none;
    padding: 6px 12px;
    border-radius: 4px 4px 0 0;
    cursor: pointer;
    font-size: 14px;
    margin-bottom: -1px; /* För att överlappa content-kanten */
}

.ribbon-tab.active {
    background-color: var(--ribbon-content-bg);
    border-color: var(--border-color);
    border-bottom-color: var(--ribbon-content-bg);
}

.search-container {
    padding-bottom: 4px;
}

.search-container input[type="search"] {
    border: 1px solid var(--input-border-color);
    background-color: var(--input-bg-color);
    border-radius: 4px; padding: 6px 8px; width: 250px; font-size: 14px;
}

.ribbon-content {
    background-color: var(--ribbon-content-bg);
    border-top: 1px solid var(--border-color);
    flex-grow: 1;
    display: flex;
    align-items: stretch; /* Se till att grupperna fyller höjden */
    padding: 4px 12px;
}

.ribbon-pane {
    display: none; width: 100%; height: 100%;
    align-items: stretch; gap: 16px;
}

.ribbon-pane.active { display: flex; }

.ribbon-group {
    display: flex;
    align-items: center; /* Centrera knapparna vertikalt */
    gap: 8px;
    height: 100%;
    padding: 0 16px 12px 16px; /* Padding i botten för etikett */
    border-right: 1px solid var(--border-color);
    position: relative;
}

.ribbon-group:first-child { padding-left: 4px; }

.ribbon-group-label {
    position: absolute;
    bottom: 2px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 12px;
    color: #666;
    white-space: nowrap;
}

.ribbon-group button, .ribbon-group input {
    background-color: var(--input-bg-color);
    border: 1px solid var(--input-border-color);
    border-radius: 4px;
    padding: 5px 8px;
    font-size: 14px;
    align-self: center; /* Håll element centrerade */
}

.ribbon-group button { cursor: pointer; }
.ribbon-group button:hover { background-color: var(--button-hover-bg); }

/* --- Main Panes --- */
.left-pane {
    width: 33.33%; max-width: 80%; min-width: 200px;
    background-color: var(--panel-bg-color); padding: 12px;
    overflow-y: auto; flex-shrink: 0;
}

.resizer {
    width: 5px; cursor: col-resize;
    background-color: var(--resizer-color); flex-shrink: 0;
    user-select: none; transition: background-color 0.2s ease;
}

.resizer:hover { background-color: var(--resizer-hover-color); }

.right-pane {
    flex-grow: 1;
    background-color: var(--panel-bg-color); padding: 12px;
    overflow-y: auto;
}
"""
# scripts/modules/ui_styles.py
