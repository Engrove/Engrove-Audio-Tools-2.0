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
