# scripts/modules/ui_template.py
#
# === HISTORIK ===
# * v3.2 (2025-08-16): Korrigerat HTML-strukturen för ribbon-menyn.
# * v4.0 (2025-08-16): Lade till dolda containrar för framtida verktyg,
#   inklusive en heltäckande .full-page-container, enligt "Operation: Dold Grund".
# * v4.1 (2025-08-16): Lade till struktur för filgranskningsmodal och översatte all UI-text till svenska.
# * v4.2 (2025-08-17): Lade till Eruda debugging-verktyg för att underlätta felsökning på mobila enheter.
# * v4.3 (2025-08-17): Lade till Chart.js CDN-länk och den kompletta HTML-strukturen för AI Performance-dashboarden.
# * v4.4 (2025-08-17): Lade till CDN-länkar för Pako.js och Transformers.js. Uppdaterade UI för att stödja "Einstein" RAG-systemets dubbelfunktions-sökruta.
# * SHA256_LF: 52f5313d4b6c1f1082d46e2978d33d7b695123b3207e3352723c3167f25902f2
#
# === TILLÄMPADE REGLER (Frankensteen v5.7) ===
# - Grundbulten v3.8: Denna ändring följer den uppgraderade processen för transparens och fullständighet.
# - GR7 (Fullständig Historik): Korrekt historik-header.

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
    <script src="https://cdn.jsdelivr.net/npm/@xenova/transformers@2.17.1"></script>
    <!-- Eruda debugging console for mobile devices -->
    <script src="https://cdn.jsdelivr.net/npm/eruda"></script>
    <script>eruda.init();</script>
</head>
<body>
    <header class="header-ribbon">
        <div class="top-bar">
            <div class="ribbon-tabs">
                <button class="ribbon-tab active" data-tab="verktyg">Verktyg</button>
                <button class="ribbon-tab" data-tab="performance">AI Performance</button>
                <button class="ribbon-tab" data-tab="installningar">Inställningar</button>
                <button class="ribbon-tab" data-tab="hjalp">Hjälp</button>
            </div>
            <div class="search-container">
                <input type="search" id="main-search-input" placeholder="Sök filer...">
                <button id="einstein-toggle-btn" title="Einstein-sökning (klicka för att klistra in & aktivera)">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a10 10 0 1 0 10 10_0_1_0-10-10Z"/><path d="M12 18a6 6 0 1 0 0-12 6 6 0 1 0 0 12Z"/><path d="M12 22a10 10 0 0 0 10-10"/><path d="M2 12a10 10 0 0 0 10 10"/></svg>
                </button>
            </div>
        </div>
        <div class="ribbon-content">
            <div id="tab-verktyg" class="ribbon-pane active">
                <div class="ribbon-group">
                    <button>Kör Analys</button>
                    <button>Exportera</button>
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
            <div class="full-page-header">
                <h2>AI Performance Dashboard</h2>
                <button id="close-full-page-btn" title="Stäng">×</button>
            </div>
            <div class="full-page-content">
                <div class="filter-bar">
                    <div class="filter-group"><label for="pf-from">Från datum (ISO)</label><input type="date" id="pf-from" /></div>
                    <div class="filter-group"><label for="pf-to">Till datum (ISO)</label><input type="date" id="pf-to" /></div>
                    <div class="filter-group" style="min-width:220px"><label>Provider</label><div id="pf-prov"></div></div>
                    <div class="filter-group" style="min-width:260px"><label>Modell</label><div id="pf-model"></div></div>
                    <div class="filter-group"><label>Alternativ</label><label class="inline"><input type="checkbox" id="pf-ma" /> MA(3)</label></div>
                    <div class="filter-group"><button id="pf-apply" class="primary">Tillämpa filter</button><button id="pf-reset">Återställ</button></div>
                    <div class="filter-group" style="margin-left:auto"><button id="pf-export" class="info">Exportera CSV</button><button id="refresh-performance">Uppdatera</button></div>
                </div>
                <div class="kpi-grid">
                    <div class="kpi"><h4>Antal sessioner</h4><div class="big" id="kpi-sessions">0</div><div class="sub" id="kpi-range"></div></div>
                    <div class="kpi"><h4>Medelpoäng</h4><div class="big" id="kpi-avg">–</div><div class="sub">Final Score (medel)</div></div>
                    <div class="kpi"><h4>Median cykler</h4><div class="big" id="kpi-cycles">–</div><div class="sub">Debugging cycles (median)</div></div>
                    <div class="kpi"><h4>Korrigeringsgrad</h4><div class="big" id="kpi-corr">–</div><div class="sub">Self/External ratio</div></div>
                </div>
                <div class="chart-grid">
                    <div class="chart-card"><h3>Final Score Over Time</h3><div class="chart-container"><canvas id="score-chart"></canvas></div></div>
                    <div class="chart-card"><h3>Session Metrics (Cycles)</h3><div class="chart-container"><canvas id="metrics-chart"></canvas></div></div>
                    <div class="chart-card"><h3>Sessions Per Provider</h3><div class="chart-container"><canvas id="provider-chart"></canvas></div></div>
                    <div class="chart-card"><h3>Sessions Per Model</h3><div class="chart-container"><canvas id="model-chart"></canvas></div></div>
                </div>
                <div class="table-card" style="margin-top:12px"><h3>Learning Database (Heuristics)</h3><div id="perf-learning-body">Ingen data.</div></div>
                <div class="table-card" style="margin-top:12px"><h3>Sessions</h3><div id="perf-sessions-body\">Ingen data.</div></div>
            </div>
        </div>
    </div>

    <!-- Modal för filgranskning -->
    <div id="file-modal-overlay" class="modal-overlay hidden">
        <div id="file-modal" class="modal-panel">
            <header class="modal-header">
                <span id="modal-loader-spinner" class="hidden" style="margin-right: 8px;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="animation: spin 1.5s linear infinite;"><circle cx="12" cy="12" r="10" stroke-opacity=".3"/><path d="M12 2a10 10 0 0 1 10 10"/></svg>
                </span>
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

    <script src="logic.js"></script>
</body>
</html>
"""
# scripts/modules/ui_template.py
