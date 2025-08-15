# scripts/modules/ui_template.py
#
# === SYFTE & ANSVAR ===
# Denna modul innehåller den grundläggande HTML- och CSS-mallen för det nya
# Engrove Audio Tools-gränssnittet. Den fungerar som en ren presentationskomponent
# utan någon logik.
#
# === HISTORIK ===
# * v1.0 (2025-08-15): Initial skapelse.
#
# === TILLÄMPADE REGLER (Frankensteen v5.4) ===
# - Obligatorisk Refaktorisering: UI-mallen är separerad från huvudlogiken.

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Engrove Audio Tools v3.0</title>
    <style>
        :root {
            --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            --font-mono: ui-monospace, "JetBrains Mono", "SF Mono", Consolas, Menlo, monospace;
            --bg-color: #f0f0f0;
            --panel-bg-color: #ffffff;
            --border-color: #cccccc;
            --text-color: #1a1a1a;
            --header-bg-color: #f9f9f9;
        }
        
        * {
            box-sizing: border-box;
        }

        body, html {
            margin: 0;
            padding: 0;
            height: 100vh;
            width: 100vw;
            font-family: var(--font-sans);
            font-size: 14px;
            background-color: var(--bg-color);
            color: var(--text-color);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .main-container {
            display: flex;
            flex-grow: 1;
            height: calc(100% - 40px); /* Justera för header-höjd */
        }

        .header {
            height: 40px;
            border-bottom: 1px solid var(--border-color);
            background-color: var(--header-bg-color);
            width: 100%;
            flex-shrink: 0;
            /* TODO: Lägg till header-innehåll här */
        }

        .left-pane {
            width: 33.33%;
            max-width: 400px;
            min-width: 250px;
            border-right: 1px solid var(--border-color);
            background-color: var(--panel-bg-color);
            padding: 12px;
            overflow-y: auto;
        }

        .right-pane {
            width: 66.67%;
            background-color: var(--panel-bg-color);
            padding: 12px;
            overflow-y: auto;
        }
    </style>
</head>
<body>
    <div class="header">
        <!-- Placeholder för framtida meny/verktygsfält -->
    </div>
    <div class="main-container">
        <aside class="left-pane">
            <h2>Navigation</h2>
            <!-- Framtida nav-träd här -->
        </aside>
        <main class="right-pane">
            <h2>Information & Funktionalitet</h2>
            <!-- Framtida innehåll här -->
        </main>
    </div>
</body>
</html>
"""
# scripts/modules/ui_template.py
