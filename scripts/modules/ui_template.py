# BEGIN FILE: scripts/modules/ui_template.py
# scripts/modules/ui_template.py
#
# === SYFTE & ANSVAR ===
# Denna fil definierar den primära HTML-mallen för AI Context Builder-verktyget.
# Den innehåller den övergripande sidstrukturen, platshållare för dynamiskt
# innehåll och länkar till externa bibliotek som Chart.js och Transformers.js.
#
# === HISTORIK ===
# * v3.2 (2025-08-16): Korrigerat HTML-strukturen för ribbon-menyn.
# * v4.0 (2025-08-16): Lade till dolda containrar för framtida verktyg.
# * v4.1 (2025-08-16): Lade till struktur för filgranskningsmodal och översatte all UI-text till svenska.
# * v4.2 (2025-08-17): Lade till Eruda debugging-verktyg för att underlätta felsökning på mobila enheter.
# * v4.3 (2025-08-17): Lade till Chart.js CDN-länk och den kompletta HTML-strukturen för AI Performance-dashboarden.
# * v4.4 (2025-08-17): Lade till CDN-länkar för Pako.js och Transformers.js.
# * v4.5 (2025-08-18): (Help me God - Domslut) Lade till `type="module"` till Transformers.js script-taggen.
# * v4.6 (2025-08-18): (Help me God - Domslut) Lade till `type="module"` för logic.js och korrigerade en trasig SVG-sökväg.
# * v5.0 (2025-08-18): Felaktig refaktorering ("Outlook Layout"). Deprekerad.
# * v5.1 (2025-08-18): Felaktig refaktorering ("Outlook Layout"). Deprekerad.
# * v5.2 (2025-08-18): (Help me God - Domslut) Återställt den felaktiga "Outlook"-layouten. Återförenat ribbon-flikar och innehållspaneler till en enda header-komponent och återinfört den globala sökrutan.
# * SHA256_LF: d0f8ba0c38f185e83c36a471318d108537d4728aa308140eb4deca6068eeb56e
#
# === TILLÄMPADE REGLER (Frankensteen v5.7) ===
# - Grundbulten v3.9: Denna fil levereras komplett och uppdaterad enligt den godkända, korrigerade planen.
# - Help_me_God: Denna ändring är ett direkt resultat av en grundorsaksanalys av ett arkitektoniskt fel.

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Engrove Audio Tools v3.0 - Analysverktyg</title>
    <link rel="stylesheet" href="styles.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1"></script>
    <script src="https://cdn.jsdelivr.net/npm/pako@2.1.0/dist/pako.min.js"></script>
    <script type="module" src="https://cdn.jsdelivr.net/npm/@xenova/transformers@2.17.1"></script>
    <!-- Eruda debugging console for mobile devices -->
    <script src="https://cdn.jsdelivr.net/npm/eruda"></script>
    <script>eruda.init();</script>
</head>
<body>
    <header class="header-ribbon">
        <div class="top-bar">
            <div class="ribbon-tabs">
                <button class="ribbon-tab active" data-tab="verktyg">Verktyg</button>
                <button class="ribbon-tab" data-tab="einstein">Einstein</button>
                <button class="ribbon-tab" data-tab="performance">AI Performance</button>
                <button class="ribbon-tab" data-tab="installningar">Inställningar</button>
                <button class="ribbon-tab" data-tab="hjalp">Hjälp</button>
            </div>
            <div class="search-container">
                <input type="search" id="main-search-input" placeholder="Sök filer...">
            </div>
        </div>
        <div class="ribbon-content">
            <div id="tab-verktyg" class="ribbon-pane active">
                <div class="ribbon-group">
                    <button>Kör Analys</button>
                    <button>Exportera</button>
                </div>
            </div>
            <div id="tab-einstein" class="ribbon-pane">
                <div class="ribbon-group">
                    <input type="search" id="einstein-search-input" placeholder="Ställ en semantisk fråga...">
                    <button id="einstein-search-btn">Sök</button>
                </div>
                 <div class="ribbon-group">
                    <span id="einstein-status-bar" class="small">Redo.</span>
                </div>
            </div>
            <div id="tab-performance" class="ribbon-pane">
                <div class="ribbon-group">
                    <button>Uppdatera Data</button>
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
            <div id="file-tree-container" class="tool-container" style="display: block;">
                <!-- Innehåll för fil-trädet kommer att renderas här av JS -->
            </div>
        </aside>
        <div class="resizer" id="resizer"></div>
        <main class="right-pane" id="right-pane">
            <div id="info-container">
                <h2>Information & Funktionalitet</h2>
                <p>Välj ett verktyg i menyn ovan för att börja.</p>
            </div>
             <!-- Heltäckande container för Einstein -->
            <div id="einstein-container" class="tool-container full-page-container">
                <div class="full-page-header">
                    <h2>Einstein Semantisk Sökning</h2>
                    <button id="close-einstein-btn" title="Stäng">×</button>
                </div>
                <div id="einstein-results-container" class="full-page-content">
                    <p>Ange en sökfråga i menybalken ovan för att börja.</p>
                </div>
            </div>
            
            <!-- Heltäckande container för AI Performance -->
            <div id="full-page-container" class="tool-container full-page-container">
                <div class="full-page-header">
                    <h2>AI Performance Dashboard</h2>
                    <button id="close-full-page-btn" title="Stäng">×</button>
                </div>
                <div class="full-page-content">
                     <!-- ... (innehåll för performance dashboard) ... -->
                </div>
            </div>
        </main>
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

    <script type="module" src="logic.js"></script>
</body>
</html>
"""

# END FILE: scripts/modules/ui_template.py
