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
# * v9.2 (2025-08-18): Omarbetat "Markera Kärndokument" för att vara additiv och dynamiskt inkludera alla protokollfiler.
# * SHA256_LF: a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3
#
# === TILLÄMPADE REGLER (Frankensteen v5.7) ===
# - Grundbulten v3.9: Denna fil levereras komplett och uppdaterad enligt den godkända planen.
# - P-OKD-1.0: Funktioner och konstanter har tydliga kommentarer.

JS_LOGIC = """
import { pipeline } from 'https://cdn.jsdelivr.net/npm/@xenova/transformers@2.17.1';

// Injektionspunkt för projektkonfiguration (repo/branch)
const ENGROVE_CONFIG = __INJECT_PROJECT_OVERVIEW__;
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
    let dotProduct = 0;
    let normA = 0;
    let normB = 0;
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
        console.log('Laddar embedding-modell...');
        EINSTEIN_PIPELINE = await pipeline('feature-extraction', EINSTEIN_MODEL_NAME);
        if (statusEl) statusEl.textContent = 'Modell laddad. Beräknar...';
        console.log('Embedding-modell laddad.');
    }

    const queryEmbedding = await EINSTEIN_PIPELINE(query, { pooling: 'mean', normalize: true });
    const queryVector = queryEmbedding.data;

    const results = EINSTEIN_INDEX.chunks.map(chunk => ({
        chunk,
        similarity: cosineSimilarity(queryVector, chunk.vector)
    }));

    results.sort((a, b) => b.similarity - a.similarity);
    return results.slice(0, numResults);
}

// Exponera sökfunktionen globalt så att andra moduler kan anropa den.
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

    const repo = ENGROVE_CONFIG.repository;
    const branch = ENGROVE_CONFIG.branch;
    const url = `https://raw.githubusercontent.com/${repo}/${branch}/${filePath}`;

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Nätverksfel: ${response.status} ${response.statusText}`);
        const text = await response.text();
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
    if (modalOverlay) {
        modalOverlay.classList.add('hidden');
    }
}

window.openFileModal = openFileModal;

/**
 * Rensar det aktuella filurvalet och output-fönstret.
 */
function clearSession() {
    if (window.deselectAllInTree) {
        window.deselectAllInTree();
    }
    const outEl = document.getElementById('out');
    if (outEl) {
        outEl.textContent = 'Session rensad.';
    }
    console.log('Session rensad.');
}

/**
 * Laddar om sidan för att starta en ny session.
 */
function reloadData() {
    location.reload();
}

/**
 * @function handleViewSwitch
 * @description Centraliserad funktion för att hantera synligheten av applikationens huvudvyer baserat på den aktiva menyfliken.
 * @param {string} targetTab - ID:t för den valda fliken (t.ex. 'start', 'data', 'einstein').
 */
function handleViewSwitch(targetTab) {
    // Hämta referenser till alla paneler
    const leftPane = document.getElementById('left-pane');
    const rightPane = document.getElementById('right-pane');
    const resizer = document.getElementById('resizer');

    // Paneler inuti right-pane
    const startPanel = document.getElementById('start-panel');
    const infoContainer = document.getElementById('info-container');
    const einsteinContainer = document.getElementById('einstein-container');
    const performanceContainer = document.getElementById('full-page-container');

    // Nollställ alla vyer
    leftPane.style.display = 'none';
    rightPane.style.display = 'none';
    resizer.style.display = 'none';
    startPanel.style.display = 'none';
    infoContainer.style.display = 'none';
    einsteinContainer.classList.remove('active');
    performanceContainer.classList.remove('active');

    // Aktivera vyer baserat på vald flik
    switch (targetTab) {
        case 'start':
            leftPane.style.display = 'block';
            rightPane.style.display = 'block';
            resizer.style.display = 'block';
            startPanel.style.display = 'block';
            break;

        case 'data':
        case 'installningar':
        case 'hjalp':
            leftPane.style.display = 'block';
            rightPane.style.display = 'block';
            resizer.style.display = 'block';
            infoContainer.style.display = 'block';
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
            // Fallback till startvyn om något går fel
            leftPane.style.display = 'block';
            rightPane.style.display = 'block';
            resizer.style.display = 'block';
            startPanel.style.display = 'block';
            break;
    }
}


document.addEventListener('DOMContentLoaded', () => {
    console.log('Engrove Audio Tools UI Initialized.');

    // --- Main UI elements ---
    const ribbonTabs = document.querySelectorAll('.ribbon-tab');
    const ribbonPanes = document.querySelectorAll('.ribbon-pane');
    const resizer = document.getElementById('resizer');
    const leftPane = document.getElementById('left-pane');
    
    // --- Modal elements ---
    const modalOverlay = document.getElementById('file-modal-overlay');
    const modalCloseBtn = document.getElementById('modal-close-btn');
    const modalCopyPathBtn = document.getElementById('modal-copy-path');
    const modalCopyContentBtn = document.getElementById('modal-copy-content');
    const modalDownloadFileBtn = document.getElementById('modal-download-file');

    // --- New Control Buttons ---
    const selectAllBtn = document.getElementById('select-all');
    const deselectAllBtn = document.getElementById('deselect-all');
    const selectCoreBtn = document.getElementById('select-core');
    const createContextBtn = document.getElementById('create-context');
    const createFilesBtn = document.getElementById('create-files');
    const clearSessionBtn = document.getElementById('clear-session');
    const refreshDataBtn = document.getElementById('refresh-data');
    
    initializeEinstein();

    if (modalOverlay) {
        modalCloseBtn.addEventListener('click', closeFileModal);
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) closeFileModal();
        });
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
    
    // --- Event Listeners for controls ---
    if(selectAllBtn) selectAllBtn.addEventListener('click', () => window.selectAllInTree && window.selectAllInTree());
    if(deselectAllBtn) deselectAllBtn.addEventListener('click', () => window.deselectAllInTree && window.deselectAllInTree());
    if(selectCoreBtn) selectCoreBtn.addEventListener('click', () => window.addPathsToSelection && window.addPathsToSelection(STATIC_CORE_PATHS, DYNAMIC_CORE_PATHS));
    if(createContextBtn) createContextBtn.addEventListener('click', () => window.generateContext && window.generateContext());
    if(createFilesBtn) createFilesBtn.addEventListener('click', () => window.generateFiles && window.generateFiles());
    if(clearSessionBtn) clearSessionBtn.addEventListener('click', clearSession);
    if(refreshDataBtn) refreshDataBtn.addEventListener('click', reloadData);

    ribbonTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.dataset.tab;
            const targetPaneId = `tab-${targetTab}`;

            // 1. Hantera flikarnas och meny-panelernas utseende
            ribbonTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            ribbonPanes.forEach(pane => {
                pane.classList.toggle('active', pane.id === targetPaneId);
            });

            // 2. Anropa den centrala funktionen för att hantera vy-växling
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
    
    // Sätt startvyn vid laddning
    handleViewSwitch('start');
});
"""

# END FILE: scripts/modules/ui_logic.py
