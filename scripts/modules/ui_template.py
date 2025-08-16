# scripts/modules/ui_template.py
#
# === HISTORIK ===
# * v3.2 (2025-08-16): Korrigerat HTML-strukturen för ribbon-menyn.
# * v4.0 (2025-08-16): Lade till dolda containrar för framtida verktyg,
#   inklusive en heltäckande .full-page-container, enligt "Operation: Dold Grund".
#
# === TILLÄMPADE REGLER (Frankensteen v5.4) ===
# - Fullständig Kod: Verifierat komplett.

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
        <div class="top-bar">
            <div class="ribbon-tabs">
                <button class="ribbon-tab active" data-tab="verktyg">Verktyg</button>
                <button class="ribbon-tab" data-tab="installningar">Inställningar</button>
                <button class="ribbon-tab" data-tab="hjalp">Hjälp</button>
            </div>
            <div class="search-container">
                <input type="search" placeholder="Sök...">
            </div>
        </div>
        <div class="ribbon-content">
            <div id="tab-verktyg" class="ribbon-pane active">
                <div class="ribbon-group">
                    <button>Kör Analys</button>
                    <button>Exportera</button>
                </div>
            </div>
            <div id="tab-installningar" class="ribbon-pane">
                 <div class="ribbon-group">
                    <button>Mörkt Tema</button>
                    <button>Ljust Tema</button>
                </div>
            </div>
            <div id="tab-hjalp" class="ribbon-pane">
                <div class="ribbon-group">
                    <button>Dokumentation</button>
                    <button>Om</button>
                </div>
            </div>
        </div>
    </header>
    <div class="main-container">
        <aside class="left-pane" id="left-pane">
            <div id="navigation-container">
                <h2>Navigation</h2>
            </div>
            <!-- Dold container för framtida fil-träd -->
            <div id="file-tree-container" class="tool-container">
                <!-- Innehåll för fil-trädet kommer att renderas här av JS -->
            </div>
        </aside>
        <div class="resizer" id="resizer"></div>
        <main class="right-pane" id="right-pane">
            <div id="info-container">
                <h2>Information & Funktionalitet</h2>
                <p>Välj ett verktyg i menyn ovan för att börja.</p>
            </div>
            <!-- Dold container för framtida datavisare -->
            <div id="data-viewer-container" class="tool-container">
                 <!-- Innehåll för datavisaren kommer att renderas här av JS -->
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
