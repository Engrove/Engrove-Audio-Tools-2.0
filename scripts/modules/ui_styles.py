# scripts/modules/ui_styles.py
#
# === HISTORIK ===
# * v1.0 (2025-08-15): Initial skapelse.
# * v1.1 (2025-08-15): Lade till stilar för en justerbar delningslinje (.resizer).
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
    --header-bg-color: #f9f9f9;
    --button-hover-bg: #e9e9e9;
    --input-bg-color: #ffffff;
    --input-border-color: #b0b0b0;
    --resizer-color: #dddddd;
    --resizer-hover-color: #0d6efd;
}

* {
    box-sizing: border-box;
}

body, html {
    margin: 0; padding: 0; height: 100vh; width: 100vw;
    font-family: var(--font-sans); font-size: 14px;
    background-color: var(--bg-color); color: var(--text-color);
    display: flex; flex-direction: column; overflow: hidden;
}

.main-container {
    display: flex; flex-grow: 1; height: calc(100% - 40px);
}

.header {
    height: 40px; border-bottom: 1px solid var(--border-color);
    background-color: var(--header-bg-color); width: 100%;
    flex-shrink: 0; display: flex; align-items: center;
    justify-content: space-between; padding: 0 12px;
}

.menu-bar { display: flex; gap: 4px; }
.menu-button {
    background: none; border: none; padding: 6px 10px;
    border-radius: 4px; cursor: pointer; font-size: 14px;
    font-family: var(--font-sans);
}
.menu-button:hover { background-color: var(--button-hover-bg); }

.search-container input[type="search"] {
    border: 1px solid var(--input-border-color);
    background-color: var(--input-bg-color);
    border-radius: 4px; padding: 6px 8px; width: 250px; font-size: 14px;
}

.left-pane {
    width: 33.33%; max-width: 80%; min-width: 200px;
    background-color: var(--panel-bg-color); padding: 12px;
    overflow-y: auto; flex-shrink: 0; /* Viktigt för att inte krympa */
}

.resizer {
    width: 5px;
    cursor: col-resize;
    background-color: var(--resizer-color);
    flex-shrink: 0;
    user-select: none; /* Förhindra textmarkering vid drag */
    transition: background-color 0.2s ease;
}

.resizer:hover {
    background-color: var(--resizer-hover-color);
}

.right-pane {
    flex-grow: 1; /* Tar upp resterande utrymme */
    background-color: var(--panel-bg-color); padding: 12px;
    overflow-y: auto;
}
"""
# scripts/modules/ui_styles.py
