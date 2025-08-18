# scripts/modules/ui_logic.py
#
# === SYFTE & ANSVAR ===
# Denna modul innehåller den sammansatta JavaScript-logiken för AI Context Builder UI,
# inklusive hantering av ribbon-meny, filgranskning och Einstein RAG-sökfunktionalitet.
#
# === HISTORIK ===
# * v3.0 (2025-08-15): Lade till logik för ribbon-menyn och resizer.
# * v5.0 (2025-08-16): (Help me God) Återställd och verifierad. Lade till
#   förberedande, vilande funktioner för "Operation: Dold Grund".
# * v6.0 (2025-08-16): Refaktorerad för modularitet. All logik för filträdet har
#   flyttats till den dedikerade modulen `ui_file_tree.py`. Denna fil
#   innehåller nu endast generell UI-logik.
# * v6.1 (2025-08-16): Lade till fullständig logik för filgranskningsmodalen,
#   inklusive realtidshämtning av filinnehåll från GitHub.
# * v6.2 (2025-08-17): Uppdaterat ribbon-logiken för att hantera visning av
#   den nya AI Performance-dashboarden som en fullskärms-overlay.
# * v7.0 (2025-08-17): Implementerat den fullständiga klient-sidiga logiken för "Einstein" RAG-systemet.
# * v7.1 (2025-08-18): (Help me God - Domslut) Korrigerat ett `ReferenceError` genom att anropa `Xenova.pipeline` istället för `pipeline`. Detta löser problemet med att Transformers.js, som en ES-modul, inte exponerar sina funktioner globalt.
# * v7.2 (2025-08-18): (Help me God - Domslut) Infört `import` för att hantera ES-modul-scope.
# * v8.0 (2025-08-18): (Engrove Mandate) Stor refaktorering. All specifik Einstein-logik för att rendera resultat har flyttats till `ui_einstein_search.py`. Denna fil hanterar nu endast anrop och visning av den nya Einstein-containern. Den gamla sökknappslogiken har tagits bort.
# * SHA256_LF: a528f870932c02118335359a9972b2505291b8a92357a9235c0211843b2b1a11
#
# === TILLÄMPADE REGLER (Frankensteen v5.7) ===
# - Grundbulten v3.8: Denna fil har modifierats enligt den godkända planen.
# - GR6 (Obligatorisk Refaktorisering): Logiken har delats upp enligt Single Responsibility Principle. Denna modul agerar nu som en orkestrerare istället för att innehålla all funktionalitet.

JS_LOGIC = """
import { pipeline } from 'https://cdn.jsdelivr.net/npm/@xenova/transformers@2.17.1';

// Injektionspunkt för projektkonfiguration (repo/branch)
const ENGROVE_CONFIG = __INJECT_PROJECT_OVERVIEW__;

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

document.addEventListener('DOMContentLoaded', () => {
    console.log('Engrove Audio Tools UI Initialized.');

    const leftPane = document.getElementById('left-pane');
    const resizer = document.getElementById('resizer');
    const ribbonTabs = document.querySelectorAll('.ribbon-tab');
    
    const performanceContainer = document.getElementById('full-page-container');
    const closePerformanceBtn = document.getElementById('close-full-page-btn');
    
    const einsteinContainer = document.getElementById('einstein-container');
    const closeEinsteinBtn = document.getElementById('close-einstein-btn');

    const modalOverlay = document.getElementById('file-modal-overlay');
    const modalCloseBtn = document.getElementById('modal-close-btn');
    const modalCopyPathBtn = document.getElementById('modal-copy-path');
    const modalCopyContentBtn = document.getElementById('modal-copy-content');
    const modalDownloadFileBtn = document.getElementById('modal-download-file');
    
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
    
    ribbonTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.dataset.tab;
            ribbonTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            performanceContainer.classList.remove('active');
            einsteinContainer.classList.remove('active');

            if (targetTab === 'performance') { performanceContainer.classList.add('active'); } 
            else if (targetTab === 'einstein') { einsteinContainer.classList.add('active'); }
        });
    });

    const closeAndSwitchToVerktyg = () => {
        performanceContainer.classList.remove('active');
        einsteinContainer.classList.remove('active');
        const verktygTab = document.querySelector('.ribbon-tab[data-tab="verktyg"]');
        if (verktygTab) verktygTab.click();
    };

    if(closePerformanceBtn) {
        closePerformanceBtn.addEventListener('click', closeAndSwitchToVerktyg);
    }
    if(closeEinsteinBtn) {
        closeEinsteinBtn.addEventListener('click', closeAndSwitchToVerktyg);
    }
    
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
});
"""

# scripts/modules/ui_logic.py
