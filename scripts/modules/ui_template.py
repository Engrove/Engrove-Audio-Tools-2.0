# scripts/modules/ui_template.py
#
# === SYFTE & ANSVAR ===
# Denna modul innehåller HTML-skelettet för AI Context Builder-verktyget.
# Dess struktur definierar de primära layoutelementen och platshållarna
# som fylls i och hanteras av JavaScript-modulerna.
#
# === HISTORIK ===
# * v3.2 (2025-08-16): Korrigerat HTML-strukturen för ribbon-menyn.
# * v4.0 (2025-08-16): Lade till dolda containrar för framtida verktyg.
# * v4.1 (2025-08-16): Lade till struktur för filgranskningsmodal och översatte all UI-text till svenska.
# * v4.2 (2025-08-17): Lade till Eruda debugging-verktyg.
# * v4.3 (2025-08-17): Lade till Chart.js CDN-länk och HTML-struktur för AI Performance-dashboarden.
# * v5.0 (2025-08-17): Ersatt statisk titel med dynamisk platshållare.
# * v5.1 (2025-08-17): (Help me God - Domslut #1) Korrigerat ett fundamentalt strukturfel. Flyttat overlay-element
#   (#full-page-container, #file-modal-overlay) utanför #main-content för att möjliggöra korrekt
#   fullskärms-rendering och lösa UI-kollapsen.
# * v5.2 (2025-08-17): (Help me God - Domslut #2) Korrigerat felaktig HTML-struktur från föregående fix.
#   Flyttade overlay-elementen till att vara direkta barn av #app-container för korrekt stackning.
# * SHA256_LF: a528e18342f1f0a28f7311c633a693b80b720cd015a999787e9140938ff5d799
#
# === TILLÄMPADE REGLER (Frankensteen v5.6) ===
# - Grundbulten v3.7: Denna ändring är resultatet av en Help me God-grundorsaksanalys.
# - GR7 (Fullständig Historik): Korrekt historik-header.

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Context Builder v{version}</title>
    <link rel="stylesheet" href="styles.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1"></script>
    <script src="https://cdn.jsdelivr.net/npm/eruda"></script>
</head>
<body>
    <div id="app-container">
        <!-- Eruda debugging console for mobile devices -->
        <script>eruda.init();</script>

        <header id="ribbon-header">
            <div class="ribbon-group">
                <button class="ribbon-tab active" data-target="verktyg-container">Verktyg</button>
                <button class="ribbon-tab" data-target="performance-container">AI Performance</button>
                <button class="ribbon-tab" data-target="installningar-container">Inställningar</button>
                <button class="ribbon-tab" data-target="hjalp-container">Hjälp</button>
            </div>
            <div id="project-overview-container" class="ribbon-group right">
                <!-- Project info will be injected here -->
            </div>
        </header>

        <main id="main-content">
            <div id="left-pane">
                <div id="file-tree-controls">
                    <button id="run-analysis-btn" class="button primary">Kör Analys</button>
                    <button id="export-btn" class="button secondary">Exportera</button>
                </div>
                <div id="file-tree-container">
                    <!-- File tree will be rendered here by JS -->
                </div>
            </div>
            <div id="resizer"></div>
            <div id="right-pane">
                <div class="tool-container active" id="verktyg-container">
                    <h2>Information & Funktionalitet</h2>
                    <p>Välj ett verktyg i menyn ovan för att börja.</p>
                </div>
            </div>
        </main>
        
        <!-- KORRIGERING: Overlays måste ligga utanför 'main' för att kunna täcka hela skärmen korrekt -->
        
        <!-- Heltäckande container för verktyg som kräver hela ytan -->
        <div id="full-page-container" class="full-page-container">
            <div class="full-page-header">
                <h2>AI Performance Dashboard</h2>
                <button id="close-full-page-btn" title="Stäng">×</button>
            </div>
            <div class="full-page-content">
                <!-- Innehåll för dashboarden ... -->
            </div>
        </div>

        <!-- Modal för filgranskning -->
        <div id="file-modal-overlay" class="modal-overlay hidden">
            <div id="file-modal" class="modal-panel">
                <header class="modal-header">
                    <h3 id="modal-title">Filnamn.js</h3>
                    <div class="modal-actions">
                        <button id="modal-copy-path" title="Kopiera sökväg">📋</button>
                        <button id="modal-copy-content">Kopiera innehåll</button>
                        <button id="modal-download-file">Ladda ner</button>
                        <button id="modal-close-btn" title="Stäng">×</button>
                    </div>
                </header>
                <main class="modal-content">
                    <div id="modal-loader" class="modal-state">Laddar innehåll...</div>
                    <div id="modal-error" class="modal-state hidden">Kunde inte hämta filens innehåll.</div>
                    <pre id="modal-content-pre"></pre>
                </main>
            </div>
        </div>
    </div>
    <script src="logic.js"></script>
</body>
</html>
"""
# scripts/modules/ui_template.py
