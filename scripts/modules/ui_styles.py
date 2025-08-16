# scripts/modules/ui_styles.py
#
# === HISTORIK ===
# * v3.0 (2025-08-15): Total visuell omdesign. Implementerade ett nytt mörkt
#   tema med blåa accenter. Knappstilar har omarbetats för att matcha
#   den nya designriktningen. Alla ribbon-etiketter har tagits bort.
#
# === TILLÄMPADE REGLER (Frankensteen v5.4) ===
# - Obligatorisk Refaktorisering: Hela CSS-arkitekturen har uppdaterats.

CSS_STYLES = """
:root {
    --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
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
}

* { box-sizing: border-box; }

body, html {
    margin: 0; padding: 0; height: 100vh; width: 100vw;
    font-family: var(--font-sans); font-size: 14px;
    background-color: var(--bg-color); color: var(--text-color);
    display: flex; flex-direction: column; overflow: hidden;
}

h2 {
    color: var(--text-color);
    font-weight: 500;
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
    margin-bottom: -1px;
    color: var(--text-color-muted);
}

.ribbon-tab.active {
    background-color: var(--panel-bg-color);
    border-color: var(--border-color);
    border-bottom-color: var(--panel-bg-color);
    color: var(--text-color);
}

.search-container { padding-bottom: 4px; }

.ribbon-content {
    background-color: var(--panel-bg-color);
    border-top: 1px solid var(--border-color);
    flex-grow: 1;
    display: flex;
    align-items: stretch;
    padding: 4px 12px;
}

.ribbon-pane {
    display: none; width: 100%; height: 100%;
    align-items: center; gap: 16px;
}

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
button, input[type="search"], .ribbon-group button {
    background-color: var(--button-bg);
    color: var(--button-text);
    border: 1px solid transparent;
    border-radius: 5px;
    padding: 8px 16px;
    font-size: 14px;
    font-weight: 500;
    transition: background-color 0.2s ease, border-color 0.2s ease;
    cursor: pointer;
}

button:hover, .ribbon-group button:hover {
    background-color: var(--button-hover-bg);
}

.ribbon-tab:hover {
    background-color: var(--panel-bg-color);
    color: var(--text-color);
}

input[type="search"] {
    background-color: var(--input-bg-color);
    border-color: var(--input-border-color);
    color: var(--text-color);
    padding: 8px;
    width: 250px;
}

input[type="search"]:focus {
    outline: none;
    border-color: var(--resizer-hover-color);
}

/* --- Main Panes --- */
.left-pane, .right-pane {
    background-color: var(--panel-bg-color);
    border-color: var(--border-color);
    padding: 12px;
    overflow-y: auto;
}
.left-pane {
    width: 33.33%; max-width: 80%; min-width: 200px;
    border-right: 1px solid var(--border-color);
    flex-shrink: 0;
}
.right-pane { flex-grow: 1; }

.resizer {
    width: 5px; cursor: col-resize;
    background-color: var(--resizer-color); flex-shrink: 0;
    user-select: none; transition: background-color 0.2s ease;
}
.resizer:hover { background-color: var(--resizer-hover-color); }
"""
# scripts/modules/ui_styles.py
