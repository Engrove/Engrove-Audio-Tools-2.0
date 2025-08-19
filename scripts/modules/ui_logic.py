# BEGIN FILE: scripts/modules/ui_logic.py
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
# * SHA256_LF: 2d89061efc7bcfba4969729601fd120ec911914ffbad544a53124f5a9cd72a42
#
# === TILLÄMPADE REGLER (Frankensteen v5.7) ===
# - Grundbulten v3.9: Denna fil levereras komplett och uppdaterad enligt den godkända, reviderade planen.
# - P-OKD-1.0: Nya funktioner har JSDoc-kommentarer.
# - GR6 (Obligatorisk Refaktorisering): Funktionaliteten har implementerats modulärt och återanvänder befintliga hjälpfunktioner.

JS_LOGIC = """
import { pipeline } from 'https://cdn.jsdelivr.net/npm/@xenova/transformers@2.17.1';

// Injektionspunkt för projektkonfiguration (repo/branch)
const ENGROVE_CONFIG = __INJECT_OVERVIEW_JSON_PAYLOAD__;
const FULL_CONTEXT = __INJECT_CONTEXT_JSON_PAYLOAD__; // Ny, komplett datakälla

// Statiska sökvägar för "Markera Kärndokument"
const STATIC_CORE_PATHS = [
    'docs/core_file_info.json',
    'docs/file_relations.json',
    'tools/frankensteen_learning_db.json',
    'package.json',
    'vite.config.js'
];
// Dynamiska mappsökvägar för "Markera Kärndokument"
const DYNAMIC_CORE_PATHS = [
    'docs/ai_protocols'
];

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
 * Genererar en files_payload.json baserat på användarens urval,
 * inklusive hash-verifiering och metadata-berikning.
 */
async function generateFiles() {
    const outputElement = document.getElementById('out');
    outputElement.textContent = 'Genererar payload...';
    document.getElementById('copy').disabled = true;
    document.getElementById('download').disabled = true;

    const selectedPaths = window.selectedFiles ? window.selectedFiles() : [];
    if (selectedPaths.length === 0) {
        outputElement.textContent = 'Fel: Inga filer valda.';
        alert('Välj minst en fil från trädet.');
        return;
    }

    const filesPayload = [];
    const validationReport = { status: 'OK', mismatches: [] };
    const coreInfo = FULL_CONTEXT.core_file_info || {};
    const relations = FULL_CONTEXT.file_relations?.graph_data?.nodes || {};
    const contextHashes = FULL_CONTEXT.hash_index?.sha256_lf || {};

    for (const path of selectedPaths) {
        try {
            const content = await fetchText(path);
            const actual_sha256 = await sha256HexLF(content);
            
            // P-HV: Jämför hash med den från den initiala kontexten
            const expected_sha256 = Object.keys(contextHashes).find(key => contextHashes[key].includes(path));

            if (expected_sha256 && actual_sha256 !== expected_sha256) {
                validationReport.mismatches.push({ path, expected_sha256, actual_sha256 });
            }

            // Berika med metadata
            const metadata = {
                purpose_and_responsibility: coreInfo[path]?.purpose_and_responsibility || 'N/A',
                criticality_score: relations[path]?.criticality_score || 0
            };

            filesPayload.push({ path, content, sha256_lf: actual_sha256, metadata });
        } catch (error) {
            console.error(`Kunde inte bearbeta ${path}:`, error);
            filesPayload.push({ path, content: `// ERROR: ${error.message}`, sha256_lf: null, metadata: {} });
        }
    }
    
    if (validationReport.mismatches.length > 0) {
        validationReport.status = 'WARNING';
    }

    const finalPayload = { files_payload: filesPayload, validation_report: validationReport };
    const isCompact = document.getElementById('compact-json')?.checked;
    const jsonString = isCompact ? JSON.stringify(finalPayload) : JSON.stringify(finalPayload, null, 2);

    outputElement.textContent = jsonString;
    document.getElementById('copy').disabled = false;
    document.getElementById('download').disabled = false;
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
    const createFilesBtn = document.getElementById('create-files-btn');
    const clearSessionBtn = document.getElementById('clear-session');
    const refreshDataBtn = document.getElementById('refresh-data');
    
    initializeEinstein();

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
    if(selectCoreBtn) selectCoreBtn.addEventListener('click', () => window.addPathsToSelection && window.addPathsToSelection(STATIC_CORE_PATHS, DYNAMIC_CORE_PATHS));
    if(createFilesBtn) createFilesBtn.addEventListener('click', generateFiles);
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

# END FILE: scripts/modules/ui_logic.py
