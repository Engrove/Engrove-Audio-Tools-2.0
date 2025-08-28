# scripts/modules/ui_logic.py
#
# === SYFTE & ANSVAR ===
# Denna modul innehåller den sammansatta JavaScript-logiken för AI Context Builder UI,
# inklusive hantering av ribbon-meny, filgranskning och den underliggande motorn
# för Einstein RAG-sökfunktionaliteten.
#
# === HISTORIK ===
# * v3.0 (2025-08-15): Lade till logik för ribbon-menyn och resizer.
# * v5.0 (2025-08-16): (Help me God) Återställd och verifierad. Lade till
#   förberedande, vilande funktioner för "Operation: Dold Grund".
# * v6.0 (2025-08-16): Refaktorerad för modularitet. All logik för filträdet har
#   flyttats till den dedikerade modulen `ui_file_tree.py`.
# * v6.1 (2025-08-16): Lade till fullständig logik för filgranskningsmodalen.
# * v6.2 (2025-08-17): Uppdaterat ribbon-logiken för att hantera visning av
#   den nya AI Performance-dashboarden som en fullskärms-overlay.
# * v7.0 (2025-08-17): Implementerat den fullständiga klient-sidiga logiken för "Einstein" RAG-systemet.
# * v7.1 (2025-08-18): (Help me God - Domslut) Korrigerat ett `ReferenceError`.
# * v7.2 (2025-08-18): (Help me God - Domslut) Infört `import` för att hantera ES-modul-scope.
# * v8.0 (2025-08-18): Felaktig refaktorering ("Outlook Layout"). Deprekerad.
# * v8.1 (2025-08-18): Felaktig refaktorering ("Outlook Layout"). Deprekerad.
# * v8.2 (2025-08-18): (Help me God - Domslut) Återställt ribbon-logiken. Hanterar nu korrekt växling av paneler (`.ribbon-pane`) inuti den enhetliga headern, istället för helsides-vyer.
# * v8.3 (2025-08-18): (Help me God - Domslut) Implementerat "Hybrid View Control". Ribbon-logiken hanterar nu korrekt både paneler i headern och växling till helsides-vyer i main-content.
# * v8.4 (2025-08-18): (Stalemate Protocol - Domslut) Korrigerat panel-växlingslogiken för att säkerställa att föräldern (`#right-pane`) förblir synlig när en overlay-vy (`#einstein-container`) aktiveras.
# * v8.5 (2025-08-18): (Engrove Mandate) Tog bort överflödig logik och event-lyssnare för de borttagna header-knapparna.
# * v9.0 (2025-08-18): (K-MOD Plan) Omarbetat flik- och panelhantering för att stödja den nya "Start"- och "Data"-layouten. Logiken är nu centraliserad i `handleViewSwitch`.
# * v9.1 (2025-08-18): Implementerat händelselyssnare för alla nya kontroller i "Start"- och "Data"-flikarna.
# * v9.2 (2025-08-18): Omarbetat "Markera Kärndokument" för att vara additivt och dynamiskt inkludera alla protokollfiler.
# * v10.0 (2025-08-19): Implementerat den fullständiga, robusta `generateFiles()`-funktionen, inklusive hash-verifiering och metadata-berikning.
# * v10.1 (2025-08-23): (Help me God - Domslut) Reintroducerade JSON.parse() för alla injicerade payloads för att åtgärda SyntaxError.
# * v11.0 (2025-08-23): (ARKITEKTURÄNDRING) Ersatt platshållarinjektion med robust "Data Island"-läsning från DOM.
# * v11.1 (2025-08-23): Knappbindning för “Skapa Filer” borttagen – ägs nu av protocol_packager.js.
# * v11.2 (2025-08-25): KRITISK FIX: Importerar och anropar `initProtocolPackager` för att binda händelselyssnare till bundle-knapparna, vilket löser felet där de var inaktiva.
# * v12.0 (2025-08-26): Lade till "Spara Markering"-funktion för att spara en anpassad lista med kärndokument till localStorage. Modifierade "Markera Kärndokument" för att använda denna sparade lista.
# * v12.1 (2025-08-28): Korrigerat felaktig implementation. Lade till `save-core-selection`-knapp och logik korrekt i JS/HTML-generatorn.
# * v12.2 (2025-08-28): Korrigerat bugg i `saveCoreSelection` som anropade en inkorrekt, icke-existerande global funktion.
# * SHA256_LF: [VERIFIERAS I CI/CD. Se context_bundle.json -> hash_index för slutgiltigt värde.]
#
# === TILLÄMPADE REGLER (Frankensteen v5.13) ===
# - Grundbulten v4.1: Denna fil levereras komplett och uppdaterad enligt den godkända, korrigerade planen.
# - Help me God: Grundorsaken till de inaktiva knapparna (saknat anrop av `init`-funktion) har identifierats och åtgärdats.

JS_LOGIC = """
import { pipeline } from 'https://cdn.jsdelivr.net/npm/@xenova/transformers@2.17.1';
import { initProtocolPackager } from './protocol_packager.js';

/**
 * Läser och parsar en JSON "Data Island" från en <script>-tagg i DOM.
 * @param {string} id - DOM ID för script-taggen.
 * @returns {object} Det parsade JavaScript-objektet.
 * @throws {Error} Om elementet inte hittas eller om JSON-datan är ogiltig.
 */
function readDataIsland(id) {
    const element = document.getElementById(id);
    if (!element) {
        throw new Error(`Data Island med ID "${id}" hittades inte i DOM.`);
    }
    try {
        return JSON.parse(element.textContent);
    } catch (e) {
        console.error(`Kunde inte parsa JSON från Data Island "${id}":`, e);
        throw e;
    }
}

// Läs in all data från "Data Islands" i DOM:en.
const ENGROVE_CONFIG = readDataIsland('data-island-overview');
const FULL_CONTEXT = readDataIsland('data-island-context');
const RELATIONS_DATA = readDataIsland('data-island-relations');

// --- Einstein RAG State ---
let EINSTEIN_INDEX = null;
let EINSTEIN_PIPELINE = null;
const EINSTEIN_MODEL_NAME = 'Xenova/all-MiniLM-L6-v2';

// --- File Modal State ---
let currentModalFilePath = null;
let currentModalFileContent = null;

// --- Utility Functions ---
/**
 * Kanoniserar text genom att normalisera radslut och ta bort BOM.
 * @param {string} s - Input-strängen.
 * @returns {string} Den kanoniserade strängen.
 */
function canonText(s) { return (s || '').replace(/\\uFEFF/g, '').replace(/\\r\\n?/g, '\\n'); }

/**
 * Beräknar SHA-256-hash för en textsträng med LF-radslut.
 * @param {string} text - Input-texten.
 * @returns {Promise<string>} Hex-hashen som en sträng.
 */
async function sha256HexLF(text) {
    const enc = new TextEncoder().encode(canonText(text));
    const buf = await crypto.subtle.digest('SHA-256', enc);
    return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
}

/**
 * Hämtar textinnehåll från en fil i repot via GitHub Raw URL.
 * @param {string} filePath - Den relativa sökvägen till filen.
 * @returns {Promise<string>} Filens textinnehåll.
 */
async function fetchText(filePath) {
    const repo = ENGROVE_CONFIG.repository;
    const branch = ENGROVE_CONFIG.branch;
    const url = `https://raw.githubusercontent.com/${repo}/${branch}/${filePath}`;
    const response = await fetch(url);
    if (!response.ok) throw new Error(`Nätverksfel: ${response.status} för ${filePath}`);
    return await response.text();
}

// --- Einstein Logic ---
async function initializeEinstein() {
    const statusEl = document.getElementById('einstein-status-bar');
    if (statusEl) statusEl.textContent = 'Laddar index...';
    try {
        const response = await fetch('einstein_index.json.gz');
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const compressed = await response.arrayBuffer();
        const decompressed = pako.inflate(compressed, { to: 'string' });
        EINSTEIN_INDEX = JSON.parse(decompressed);
        if (statusEl) statusEl.textContent = `Redo (${EINSTEIN_INDEX.chunks.length} textfragment indexerade).`;
        console.log('Einstein RAG index loaded successfully.');
    } catch (e) {
        if (statusEl) statusEl.textContent = 'Fel vid laddning av index.';
        console.error("Kunde inte ladda Einstein RAG index:", e);
    }
}

function cosineSimilarity(vecA, vecB) {
    let dotProduct = 0, normA = 0, normB = 0;
    for (let i = 0; i < vecA.length; i++) {
        dotProduct += vecA[i] * vecB[i];
        normA += vecA[i] * vecA[i];
        normB += vecB[i] * vecB[i];
    }
    return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}

async function performSemanticSearch(query, numResults = 10) {
    if (!EINSTEIN_INDEX) throw new Error("Einstein-index är inte laddat.");
    const statusEl = document.getElementById('einstein-status-bar');
    if (!EINSTEIN_PIPELINE) {
        if (statusEl) statusEl.textContent = 'Laddar AI-modell (första sökningen)...';
        EINSTEIN_PIPELINE = await pipeline('feature-extraction', EINSTEIN_MODEL_NAME);
        if (statusEl) statusEl.textContent = 'Modell laddad. Beräknar...';
    }
    const queryEmbedding = await EINSTEIN_PIPELINE(query, { pooling: 'mean', normalize: true });
    const results = EINSTEIN_INDEX.chunks.map(chunk => ({ chunk, similarity: cosineSimilarity(queryEmbedding.data, chunk.vector) }));
    results.sort((a, b) => b.similarity - a.similarity);
    return results.slice(0, numResults);
}
window.performSemanticSearch = performSemanticSearch;


// --- File Modal Logic ---
async function openFileModal(filePath) {
    const modalOverlay = document.getElementById('file-modal-overlay');
    const modalTitle = document.getElementById('modal-title');
    const modalLoader = document.getElementById('modal-loader');
    const modalError = document.getElementById('modal-error');
    const modalContentPre = document.getElementById('modal-content-pre');
    if (!modalOverlay || !modalTitle) return;
    currentModalFilePath = filePath;
    currentModalFileContent = null;
    modalTitle.textContent = filePath;
    modalLoader.classList.remove('hidden');
    modalError.classList.add('hidden');
    modalContentPre.innerHTML = '';
    modalOverlay.classList.remove('hidden');
    try {
        const text = await fetchText(filePath);
        currentModalFileContent = text;
        modalContentPre.textContent = text;
    } catch (error) {
        console.error("Fel vid hämtning av fil:", error);
        modalError.textContent = `Kunde inte hämta filens innehåll. Fel: ${error.message}`;
        modalError.classList.remove('hidden');
    } finally {
        modalLoader.classList.add('hidden');
    }
}
function closeFileModal() {
    const modalOverlay = document.getElementById('file-modal-overlay');
    if (modalOverlay) { modalOverlay.classList.add('hidden'); }
}
window.openFileModal = openFileModal;

// --- Core Functionality ---

/**
 * Sparar de för närvarande markerade filernas sökvägar till webbläsarens localStorage.
 */
function saveCoreSelection() {
    const selectedPaths = window.selectedFiles ? window.selectedFiles() : [];
    if (selectedPaths.length === 0) {
        alert('Inga filer är markerade. Markera de filer du vill spara som ditt "Core val".');
        return;
    }
    try {
        localStorage.setItem('engrove.customCoreDocs', JSON.stringify(selectedPaths));
        console.log('Anpassat "Core val" sparat till localStorage.', selectedPaths);
        alert(`Sparade ${selectedPaths.length} fil(er) som ditt anpassade "Core val".`);
    } catch (e) {
        console.error('Kunde inte spara "Core val" till localStorage:', e);
        alert('Ett fel uppstod när ditt "Core val" skulle sparas.');
    }
}


/**
 * Sparar de för närvarande markerade filernas sökvägar till webbläsarens localStorage.
 */
function saveCustomCoreSelection() {
     const selectedPaths = window.selectedFiles ? window.selectedFiles() : [];
     if (selectedPaths.length === 0) {
        alert('Inga filer är markerade. Markera de filer du vill spara som kärndokument.');
        return;
    }
    try {
        localStorage.setItem('engrove.customCoreDocs', JSON.stringify(selectedPaths));
        console.log('Anpassat urval av kärndokument sparat.', selectedPaths);
        const btn = document.getElementById('save-core-docs-btn');
        const originalText = btn.textContent;
        btn.textContent = 'Sparat!';
        setTimeout(() => { btn.textContent = originalText; }, 1500);
    } catch (e) {
        console.error('Kunde inte spara till localStorage:', e);
        alert('Ett fel uppstod när markeringen skulle sparas.');
    }
}

/**
 * Returnerar den hårdkodade standardlistan över kärndokument.
 * @returns {string[]} En array med filsökvägar.
 */
function getHardcodedCoreDocs() {
     return [
        'docs/ai_protocols/AI_Core_Instruction.md',
        'docs/ai_protocols/Grundbulten_Protokoll.md',
        'docs/ai_protocols/Help_me_God_Protokoll.md',
        'docs/ai_protocols/Stature_Report_Protocol.md',
        'docs/ai_protocols/System_Integrity_Check_Protocol.md',
        'docs/ai_protocols/K-MOD_Protokoll.md',
        'docs/ai_protocols/Beroendeanalys_Protokoll.md',
        'docs/ai_protocols/Uppgifts-Kontrakt_Protokoll.md',
        'docs/ai_protocols/ai_config.json',
        'docs/ai_protocols/DynamicProtocols.json',
        'tools/frankensteen_learning_db.json',
        'package.json',
    ];
}


/**
 * Markerar kärndokument. Prioriterar en anpassad lista från localStorage,
 * annars används en fördefinierad, hårdkodad lista. Funktionen är strikt additiv.
 */
function markCoreDocuments() {
    const customCoreDocsJSON = localStorage.getItem('engrove.customCoreDocs');
    let pathsToSelect = [];

    if (customCoreDocsJSON) {
        try {
            pathsToSelect = JSON.parse(customCoreDocsJSON);
            console.log('Laddar anpassad lista med kärndokument från localStorage.');
        } catch (e) {
            console.error('Kunde inte parsa anpassad lista, återgår till standard:', e);
            pathsToSelect = getHardcodedCoreDocs();
        }
    } else {
        console.log('Ingen anpassad lista hittades, använder standardlista.');
        pathsToSelect = getHardcodedCoreDocs();
    }
    
    if (window.addPathsToSelection) {
        // Skickar en tom array för dynamiska sökvägar då den nya logiken hanterar specifika filer.
        window.addPathsToSelection(pathsToSelect, []);
    }
}


function clearSession() {
    if (window.deselectAllInTree) { window.deselectAllInTree(); }
    const outEl = document.getElementById('out');
    if (outEl) { outEl.textContent = 'Session rensad.'; }
    console.log('Session rensad.');
}

function reloadData() { location.reload(); }

function handleViewSwitch(targetTab) {
    const leftPane = document.getElementById('left-pane');
    const rightPane = document.getElementById('right-pane');
    const resizer = document.getElementById('resizer');
    const startPanel = document.getElementById('start-panel');
    const infoContainer = document.getElementById('info-container');
    const einsteinContainer = document.getElementById('einstein-container');
    const performanceContainer = document.getElementById('full-page-container');

    [leftPane, rightPane, resizer, startPanel, infoContainer].forEach(el => el.style.display = 'none');
    [einsteinContainer, performanceContainer].forEach(el => el.classList.remove('active'));

    switch (targetTab) {
        case 'start':
            [leftPane, rightPane, resizer, startPanel].forEach(el => el.style.display = 'block');
            break;
        case 'data':
        case 'installningar':
        case 'hjalp':
            [leftPane, rightPane, resizer, infoContainer].forEach(el => el.style.display = 'block');
            break;
        case 'einstein':
            rightPane.style.display = 'block';
            einsteinContainer.classList.add('active');
            break;
        case 'performance':
            rightPane.style.display = 'block';
            performanceContainer.classList.add('active');
            break;
        default:
            [leftPane, rightPane, resizer, startPanel].forEach(el => el.style.display = 'block');
            break;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    console.log('Engrove Audio Tools UI Initialized.');

    const ribbonTabs = document.querySelectorAll('.ribbon-tab');
    const ribbonPanes = document.querySelectorAll('.ribbon-pane');
    const resizer = document.getElementById('resizer');
    const leftPane = document.getElementById('left-pane');
    
    const modalOverlay = document.getElementById('file-modal-overlay');
    const modalCloseBtn = document.getElementById('modal-close-btn');
    const modalCopyPathBtn = document.getElementById('modal-copy-path');
    const modalCopyContentBtn = document.getElementById('modal-copy-content');
    const modalDownloadFileBtn = document.getElementById('modal-download-file');

    const selectAllBtn = document.getElementById('select-all');
    const deselectAllBtn = document.getElementById('deselect-all');
    const selectCoreBtn = document.getElementById('select-core');
    const saveCoreBtn = document.getElementById('save-core-docs-btn'); // Ny knapp
    const saveCoreSelectionBtn = document.getElementById('save-core-selection');
    const clearSessionBtn = document.getElementById('clear-session');
    const refreshDataBtn = document.getElementById('refresh-data');
    
    initializeEinstein();
    initProtocolPackager();

    if (modalOverlay) {
        modalCloseBtn.addEventListener('click', closeFileModal);
        modalOverlay.addEventListener('click', (e) => { if (e.target === modalOverlay) closeFileModal(); });
        modalCopyPathBtn.addEventListener('click', () => { if (currentModalFilePath) navigator.clipboard.writeText(currentModalFilePath); });
        modalCopyContentBtn.addEventListener('click', () => { if (currentModalFileContent) navigator.clipboard.writeText(currentModalFileContent); });
        modalDownloadFileBtn.addEventListener('click', () => {
            if (currentModalFileContent && currentModalFilePath) {
                const blob = new Blob([currentModalFileContent], { type: 'text/plain' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = currentModalFilePath.split('/').pop();
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }
        });
    }
    
    if(selectAllBtn) selectAllBtn.addEventListener('click', () => window.selectAllInTree && window.selectAllInTree());
    if(deselectAllBtn) deselectAllBtn.addEventListener('click', () => window.deselectAllInTree && window.deselectAllInTree());
    if(selectCoreBtn) selectCoreBtn.addEventListener('click', markCoreDocuments); // Ändrad
    if(saveCoreBtn) saveCoreBtn.addEventListener('click', saveCustomCoreSelection); // Ny
    if(saveCoreSelectionBtn) saveCoreSelectionBtn.addEventListener('click', saveCoreSelection);
    if(clearSessionBtn) clearSessionBtn.addEventListener('click', clearSession);
    if(refreshDataBtn) refreshDataBtn.addEventListener('click', reloadData);

    ribbonTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.dataset.tab;
            const targetPaneId = `tab-${targetTab}`;
            ribbonTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            ribbonPanes.forEach(pane => { pane.classList.toggle('active', pane.id === targetPaneId); });
            handleViewSwitch(targetTab);
        });
    });
    
    if(resizer && leftPane) {
        let isResizing = false;
        resizer.addEventListener('mousedown', () => { isResizing = true; });
        document.addEventListener('mousemove', (e) => {
            if (!isResizing) return;
            const newWidth = e.clientX;
            const minWidth = 200;
            const maxWidth = document.body.clientWidth * 0.8;
            if (newWidth > minWidth && newWidth < maxWidth) { leftPane.style.width = `${newWidth}px`; }
        });
        document.addEventListener('mouseup', () => { isResizing = false; });
    }
    
    handleViewSwitch('start');
});
"""

def get_ui_logic():
    """
    Genererar och returnerar en sträng som innehåller HTML-strukturen och
    JavaScript-logiken för verktygets användargränssnitt.
    """
    html = f'''
    <div class="container">
        <header>
            <div id="ribbon-tabs">
                <button class="ribbon-tab active" data-tab="start">Start</button>
                <button class="ribbon-tab" data-tab="data">Data</button>
                <button class="ribbon-tab" data-tab="einstein">Einstein</button>
                <button class="ribbon-tab" data-tab="performance">AI Performance</button>
                <button class="ribbon-tab" data-tab="installningar">Inställningar</button>
                <button class="ribbon-tab" data-tab="hjalp">Hjälp</button>
            </div>
             <div id="ribbon-panes">
                <div class="ribbon-pane active" id="tab-start">
                    <button id="refresh-data">Ladda Om Data</button>
                </div>
                <div class="ribbon-pane" id="tab-data">
                    <button id="select-all">Markera Alla</button>
                    <button id="deselect-all">Avmarkera Alla</button>
                    <button id="select-core">Markera Kärndokument</button>
                    <button id="save-core-docs-btn" class="btn">Spara Markering</button>
                    <button id="save-core-selection">Spara Core val</button>
                    <button id="create-files-payload" class="primary">Skapa Fil-bundle</button>
                    <button id="create-protocol-bundle" class="primary">Skapa Protokoll-bundle</button>
                    <label><input type="checkbox" id="compact-json" checked> Kompakt JSON</label>
                </div>
                <div class="ribbon-pane" id="tab-einstein">
                    <input type="text" id="einstein-search-input" placeholder="Sök i projektet...">
                    <button id="einstein-search-btn">Sök</button>
                    <span id="einstein-status-bar">Redo</span>
                </div>
                <div class="ribbon-pane" id="tab-performance"></div>
                <div class="ribbon-pane" id="tab-installningar">
                     <button id="clear-session">Rensa Session</button>
                </div>
                <div class="ribbon-pane" id="tab-hjalp"></div>
            </div>
        </header>

        <main id="main-content">
            <div id="left-pane">
                <div id="file-tree"></div>
            </div>
            <div id="resizer"></div>
            <div id="right-pane">
                <div id="start-panel">
                    <h1>Frankensteen File & Context Manager</h1>
                </div>
                <div id="info-container" style="display:none;">
                    <pre id="out"></pre>
                    <div class="output-toolbar">
                        <button id="copy" disabled>Kopiera</button>
                        <button id="download" disabled>Ladda ner</button>
                    </div>
                </div>
                <div id="einstein-container"></div>
                <div id="full-page-container"></div>
            </div>
        </main>
    </div>

    <div id="file-modal-overlay" class="hidden">
        <div id="file-modal">
            <div id="modal-header">
                <span id="modal-title"></span>
                <div id="modal-actions">
                    <button id="modal-copy-path">Kopiera Sökväg</button>
                    <button id="modal-copy-content">Kopiera Innehåll</button>
                    <button id="modal-download-file">Ladda ner Fil</button>
                    <button id="modal-close-btn">Stäng</button>
                </div>
            </div>
            <div id="modal-loader">Laddar...</div>
            <div id="modal-error" class="hidden"></div>
            <pre id="modal-content-pre"><code></code></pre>
        </div>
    </div>
    <script type="module">{JS_LOGIC}</script>
    '''
    return html
# END FILE: scripts/modules/ui_logic.py
