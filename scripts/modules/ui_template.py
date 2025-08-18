<!-- BEGIN FILE: scripts/modules/ui_template.py -->
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
            <!-- Omarbetade flikar -->
            <div class="ribbon-tabs">
                <button class="ribbon-tab active" data-tab="start">Start</button>
                <button class="ribbon-tab" data-tab="data">Data</button>
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
            <!-- Start-flikens panel -->
            <div id="tab-start" class="ribbon-pane active">
                <div class="ribbon-group">
                    <button id="clear-session">Töm Val & Output</button>
                    <button id="refresh-data">Ladda om Data</button>
                </div>
                <div class="ribbon-group">
                    <button id="run-analysis">Kör Analys</button>
                    <button id="export-overview">Exportera Projektöversikt</button>
                </div>
            </div>
            <!-- Data-flikens panel (Ny) -->
            <div id="tab-data" class="ribbon-pane">
                 <div class="ribbon-group">
                    <button id="select-all">Markera Alla</button>
                    <button id="deselect-all">Avmarkera Alla</button>
                    <button id="select-core">Markera Kärndokument</button>
                </div>
                <div class="ribbon-group">
                    <button id="create-context">Skapa Kontext</button>
                    <button id="create-files-btn">Skapa Filer</button>
                    <label class="inline"><input type="checkbox" id="compact-json" checked> Kompakt JSON</label>
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
            <!-- Start Panel - Visas som standard -->
            <div id="start-panel">
                <h2>AI Context Builder v{version}</h2>
                <p>Detta verktyg hjälper dig att inspektera projektets filstruktur, välja relevanta filer och generera en fokuserad kontext för en AI-partner.</p>
                <h4>Funktionsöversikt</h4>
                <ul>
                    <li><strong>Start:</strong> Generella projekt- och sessionsåtgärder.</li>
                    <li><strong>Data:</strong> Välj filer och generera kontext- eller fil-paket.</li>
                    <li><strong>Einstein:</strong> Utför semantisk sökning i projektets kodbas.</li>
                    <li><strong>AI Performance:</strong> Analysera och visualisera AI-prestanda över tid.</li>
                </ul>
            </div>

            <!-- Denna container visas för "Data"-fliken och andra vyer -->
            <div id="info-container" style="display: none;">
                <h2>Output</h2>
                <pre id="out">Genererad data kommer att visas här.</pre>
            </div>
            
             <!-- Heltäckande container för Einstein -->
            <div id="einstein-container" class="tool-container full-page-container">
                <div id="einstein-results-container" class="full-page-content">
                    <p>Ange en sökfråga i menybalken ovan för att börja.</p>
                </div>
            </div>
            
            <!-- Heltäckande container för AI Performance -->
            <div id="full-page-container" class="tool-container full-page-container">
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
<!-- END FILE: scripts/modules/ui_template.py -->
