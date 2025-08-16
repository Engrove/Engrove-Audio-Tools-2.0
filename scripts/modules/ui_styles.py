# scripts/modules/ui_styles.py
#
# === HISTORIK ===
# * v4.1 (2025-08-16): (Help me God - Rotorsaksanalys) Korrigerat CSS för att
#   ta bort motstridiga regler och korrekt stilsätta ribbon-menyn.
#
# === TILLÄMPADE REGLER (Frankensteen v5.4) ===
# - Fullständig Kod: Verifierat komplett.
# - Syntax- & Linter-simulering: Validerad CSS.

CSS_STYLES = """
:root {
    --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    --bg-color: #ffffff;
    --panel-bg-color: #ffffff;
    --border-color: #e0e0e0;
    --text-color: #1a1a1a;
    --header-bg-color: #f0f0f0;
    --button-hover-bg: #e9e9e9;
    --input-bg-color: #ffffff;
    --input-border-color: #b0b0b0;
    --resizer-color: #dddddd;
    --resizer-hover-color: #0d6efd;
    --ribbon-tab-active-bg: #ffffff;
    --ribbon-content-bg: #f9f9f9;
}

* { box-sizing: border-box; }

body, html {
    margin: 0; padding: 0; height: 100vh; width: 100vw;
    font-family: var(--font-sans); font-size: 14px;
    background-color: var(--bg-color); color: var(--text-color);
    display: flex; flex-direction: column; overflow: hidden;
}

h2 { font-weight: 500; }

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

.ribbon-tabs { display: flex; gap: 4px; }
.ribbon-tab {
    background: none; border: 1px solid transparent; border-bottom: none;
    padding: 6px 12px; border-radius: 4px 4px 0 0; cursor: pointer;
    font-size: 14px; margin-bottom: -1px; color: #666;
}
.ribbon-tab.active {
    background-color: var(--ribbon-content-bg);
    border-color: var(--border-color);
    border-bottom-color: var(--ribbon-content-bg);
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
button, input[type="search"] {
    border: 1px solid var(--input-border-color);
    border-radius: 4px;
    padding: 5px 8px;
    font-size: 14px;
    background-color: #ffffff;
}
button { cursor: pointer; }
button:hover { background-color: var(--button-hover-bg); }
.ribbon-tab:hover { background-color: #e9e9e9; }
input[type="search"] { width: 250px; }
input[type="search"]:focus { outline: none; border-color: var(--resizer-hover-color); }

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
"""
# scripts/modules/ui_styles.py
