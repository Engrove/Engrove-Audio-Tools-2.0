# scripts/modules/ui_template.py
# === HISTORIK ===
# v3.2 (2025-08-16): Korrigerat HTML-strukturen för ribbon-menyn.
# v4.0 (2025-08-16): Lade till dolda containrar för framtida verktyg,
#                    inklusive en heltäckande .full-page-container, enligt "Operation: Dold Grund".
# v4.1 (2025-08-16): Lade till struktur för filgranskningsmodal och översatte all UI-text till svenska.
# v4.2 (2025-08-17): Lade till Eruda debugging-verktyg för att underlätta felsökning på mobila enheter.
# v4.3 (2025-08-17): Lade till Chart.js CDN-länk och den kompletta HTML-strukturen för AI Performance-dashboarden.
# v5.0 (2025-08-17): Ersatt den statiska HTML-titeln med en dynamisk platshållare '{version}' för att tillåta versionshantering från byggskriptet. detta ledde till att sidan inte längre fungerar.
# === TILLÄMPADE REGLER (Frankensteen v5.6) ===
# Grundbulten v3.4: Denna ändring följer den uppgraderade processen för transparens och fullständighet.
# GR6 (Obligatorisk Refaktorisering): Titeln är nu dynamisk och mer underhållbar.
# GR7 (Fullständig Historik): Korrekt historik-header.

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Context Builder</title>
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

                <!-- Dold container för framtida fil-träd -->
                <div class="tool-container" id="file-tree-tool-container">
                    <h2>Filträd</h2>
                    <div id="file-tree-output">
                        <!-- Innehåll för fil-trädet kommer att renderas här av JS -->
                    </div>
                </div>

                <!-- Dold container för framtida datavisare -->
                <div class="tool-container" id="data-viewer-container">
                    <h2>Datavisare</h2>
                    <!-- Innehåll för datavisaren kommer att renderas här av JS -->
                </div>

                <!-- Heltäckande container för verktyg som kräver hela ytan -->
                <div class="full-page-container" id="performance-container">
                    <button class="close-full-page-btn" data-target="performance-container">×</button>
                    <div class="dashboard">
                        <div class="dashboard-header">
                            <h1>AI Performance Dashboard</h1>
                            <div class="filters">
                                <select id="time-range-filter">
                                    <option value="7d">Senaste 7 dagarna</option>
                                    <option value="30d">Senaste 30 dagarna</option>
                                    <option value="all">All tid</option>
                                </select>
                            </div>
                        </div>
                        <div class="dashboard-grid">
                            <div class="card kpi-card">
                                <h3>Total Score (Avg)</h3>
                                <p class="kpi-value" id="kpi-avg-score">82.5</p>
                                <div class="kpi-trend">▲ 2.1%</div>
                            </div>
                            <div class="card kpi-card">
                                <h3>Heuristics Triggered</h3>
                                <p class="kpi-value" id="kpi-heuristics">128</p>
                                <div class="kpi-trend">▼ 5.4%</div>
                            </div>
                            <div class="card kpi-card">
                                <h3>'Help me God' Events</h3>
                                <p class="kpi-value" id="kpi-hmg">4</p>
                                <div class="kpi-trend">⎯</div>
                            </div>
                            <div class="card chart-card">
                                <h3>Score Over Time</h3>
                                <canvas id="score-chart"></canvas>
                            </div>
                            <div class="card table-card">
                                <h3>Recent Sessions</h3>
                                <table id="sessions-table">
                                    <thead>
                                        <tr>
                                            <th>Session ID</th>
                                            <th>Date</th>
                                            <th>Score</th>
                                            <th>Status</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <!-- Rows will be injected by JS -->
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </main>
    </div>

    <!-- Modal för filgranskning -->
    <div id="file-viewer-modal" class="modal-overlay">
        <div class="modal-content">
            <div class="modal-header">
                <h3 id="modal-title">Filgranskning</h3>
                <div class="modal-actions">
                    <button id="modal-copy-path" class="button icon-only" title="Kopiera sökväg">📋</button>
                    <button id="modal-close-btn" class="button icon-only" title="Stäng">×</button>
                </div>
            </div>
            <div class="modal-body">
                <pre id="modal-code-content"><code>Laddar innehåll...</code></pre>
            </div>
        </div>
    </div>

    <script src="logic.js"></script>
</body>
</html>
"""
# scripts/modules/ui_template.py
