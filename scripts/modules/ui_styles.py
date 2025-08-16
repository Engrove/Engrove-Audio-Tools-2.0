# scripts/modules/ui_styles.py
#
# === HISTORIK ===
# * v4.0 (2025-08-16): Lade till förberedande, initialt dolda stilar för
#   framtida verktyg enligt StigBritt-godkänd plan "Operation: Dold Grund".
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

h2 { font-weight: 500; }

.main-container {
    display: flex; flex-grow: 1;
    height: calc(100% - 85px);
    position: relative; /* Nödvändigt för full-page overlay */
}

/* --- Ribbon Header --- */
.header-ribbon {
    height: 85px; border-bottom: 1px solid var(--border-color);
    background-color: var(--header-bg-color); width: 100%;
    flex-shrink: 0; display: flex; flex-direction: column;
}
.top-bar {
    display: flex; justify-content: space-between;
    align-items: flex-end; padding: 0 12px;
}
.ribbon-tabs { display: flex; gap: 4px; }
.ribbon-tab {
    background: none; border: 1px solid transparent; border-bottom: none;
    padding: 6px 12px; border-radius: 4px 4px 0 0; cursor: pointer;
    font-size: 14px; margin-bottom: -1px; color: #666;
}
.ribbon-tab.active {
    background-color: var(--ribbon-content-bg); border-color: var(--border-color);
    border-bottom-color: var(--ribbon-content-bg); color: var(--text-color);
}
.search-container { padding-bottom: 4px; }
.ribbon-content {
    background-color: var(--ribbon-content-bg); border-top: 1px solid var(--border-color);
    flex-grow: 1; display: flex; align-items: stretch; padding: 4px 12px;
}
.ribbon-pane { display: none; width: 100%; height: 100%; align-items: center; gap: 16px; }
.ribbon-pane.active { display: flex; }
.ribbon-group {
    display: flex; align-items: center; gap: 8px; height: 100%;
    padding: 0 16px; border-right: 1px solid var(--border-color);
}
.ribbon-group:first-child { padding-left: 4px; }

/* --- Global Component Styles --- */
button, input[type="search"] {
    border: 1px solid var(--input-border-color); border-radius: 4px;
    padding: 5px 8px; font-size: 14px;
}
button { cursor: pointer; background-color: #f9f9f9; }
button:hover { background-color: var(--button-hover-bg); }

/* --- Main Panes --- */
.left-pane, .right-pane {
    background-color: var(--panel-bg-color); padding: 12px;
    overflow-y: auto;
}
.left-pane {
    width: 33.33%; max-width: 80%; min-width: 200px;
    border-right: 1px solid var(--border-color); flex-shrink: 0;
}
.right-pane { flex-grow: 1; }
.resizer {
    width: 5px; cursor: col-resize; background-color: var(--resizer-color);
    flex-shrink: 0; user-select: none; transition: background-color 0.2s ease;
}
.resizer:hover { background-color: var(--resizer-hover-color); }

/* --- Dolda Verktygs-Containrar (Operation: Dold Grund) --- */
.tool-container {
    display: none; /* Allt inuti detta är dolt som standard */
    height: 100%; width: 100%;
}
.full-page-container {
    position: absolute;
    inset: 0;
    background-color: var(--panel-bg-color);
    z-index: 100;
    padding: 12px;
    overflow-y: auto;
}
"""
# scripts/modules/ui_styles.py```

### **Fil 2: `scripts/modules/ui_template.py` (Uppdaterad)**

```python
# scripts/modules/ui_template.py
#
# === HISTORIK ===
# * v3.1 (2025-08-16): Lade till dolda containrar för framtida verktyg,
#   inklusive en heltäckande .full-page-container, enligt StigBritt-direktiv.
#
# === TILLÄMPADE REGLER (Frankensteen v5.4) ===
# - Fullständig kod, alltid.

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Engrove Audio Tools v3.0</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header class="header-ribbon">
        <!-- Ribbon-innehåll (oförändrat) -->
    </header>
    <div class="main-container">
        <aside class="left-pane" id="left-pane">
            <div id="navigation-container">
                <h2>Navigation</h2>
            </div>
            <div id="file-tree-container" class="tool-container">
                <!-- Framtida fil-träd renderas här -->
            </div>
        </aside>
        <div class="resizer" id="resizer"></div>
        <main class="right-pane" id="right-pane">
            <div id="info-container">
                <h2>Information & Funktionalitet</h2>
                <p>Välj ett verktyg i menyn ovan för att börja.</p>
            </div>
            <div id="data-viewer-container" class="tool-container">
                 <!-- Framtida datavisare renderas här -->
            </div>
        </main>
        
        <!-- Heltäckande container för verktyg som kräver hela ytan -->
        <div id="full-page-container" class="tool-container full-page-container">
            <!-- Framtida verktyg som AI Performance renderas här -->
        </div>
    </div>
    <script src="logic.js"></script>
</body>
</html>
"""
# scripts/modules/ui_template.py
