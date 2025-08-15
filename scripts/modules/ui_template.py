# scripts/modules/ui_template.py
#
# === HISTORIK ===
# * v1.3 (2025-08-15): Lade till resizer-element.
# * v2.0 (2025-08-15): Omstrukturerade header till ett fullständigt ribbon-gränssnitt.
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
        <div class="ribbon-tabs">
            <button class="ribbon-tab active" data-tab="verktyg">Verktyg</button>
            <button class="ribbon-tab" data-tab="installningar">Inställningar</button>
            <button class="ribbon-tab" data-tab="hjalp">Hjälp</button>
        </div>
        <div class="ribbon-content">
            <div id="tab-verktyg" class="ribbon-pane active">
                <div class="ribbon-group">
                    <input type="search" placeholder="Sök i data...">
                    <span class="ribbon-group-label">Sök</span>
                </div>
                <div class="ribbon-group">
                    <button>Kör Analys</button>
                    <button>Exportera</button>
                    <span class="ribbon-group-label">Åtgärder</span>
                </div>
            </div>
            <div id="tab-installningar" class="ribbon-pane">
                 <div class="ribbon-group">
                    <button>Mörkt Tema</button>
                    <button>Ljust Tema</button>
                    <span class="ribbon-group-label">Gränssnitt</span>
                </div>
            </div>
            <div id="tab-hjalp" class="ribbon-pane">
                <div class="ribbon-group">
                    <button>Dokumentation</button>
                    <button>Om</button>
                    <span class="ribbon-group-label">Support</span>
                </div>
            </div>
        </div>
    </header>
    <div class="main-container">
        <aside class="left-pane" id="left-pane">
            <h2>Navigation</h2>
            <!-- Framtida nav-träd här -->
        </aside>
        <div class="resizer" id="resizer"></div>
        <main class="right-pane" id="right-pane">
            <h2>Information & Funktionalitet</h2>
            <p>Välj ett verktyg i menyn ovan för att börja.</p>
        </main>
    </div>
    <script src="logic.js"></script>
</body>
</html>
"""
# scripts/modules/ui_template.py
