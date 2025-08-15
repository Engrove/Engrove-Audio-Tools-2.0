# scripts/modules/ui_template.py
#
# === SYFTE & ANSVAR ===
# Denna modul innehåller den grundläggande HTML-strukturen för det nya
# Engrove Audio Tools-gränssnittet. Den länkar till en extern CSS-fil.
#
# === HISTORIK ===
# * v1.0 (2025-08-15): Initial skapelse.
# * v1.1 (2025-08-15): All CSS borttagen och ersatt med en <link>-tagg.
#   Header-sektionen har byggts ut med meny och sökfält.
#
# === TILLÄMPADE REGLER (Frankensteen v5.4) ===
# - Obligatorisk Refaktorisering: UI-mallen är separerad från stilar.

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
    <header class="header">
        <nav class="menu-bar">
            <button class="menu-button">Verktyg</button>
            <button class="menu-button">Inställningar</button>
            <button class="menu-button">Hjälp</button>
        </nav>
        <div class="search-container">
            <input type="search" placeholder="Sök...">
        </div>
    </header>
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
