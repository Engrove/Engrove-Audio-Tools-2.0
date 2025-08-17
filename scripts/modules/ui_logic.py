# scripts/modules/ui_logic.py
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
# * SHA256_LF: d5a0d33e8a7c2b0e6f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e
#
# === TILLÄMPADE REGLER (Frankensteen v5.7) ===
# - Grundbulten v3.8: Denna ändring följer den uppgraderade processen för transparens och fullständighet.
# - GR7 (Fullständig Historik): Korrekt historik-header.

JS_LOGIC = """
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
    const statusEl = document.getElementById('einstein-status');
    if (statusEl) statusEl.textContent = 'Laddar index...';
    try {
        const response = await fetch('einstein_index.json.gz');
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const compressed = await response.arrayBuffer();
        const decompressed = pako.inflate(compressed, { to: 'string' });
        EINSTEIN_INDEX = JSON.parse(decompressed);
        if (statusEl) statusEl.textContent = `Index laddat (${EINSTEIN_INDEX.chunks.length} chunks)`;
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

async function performSemanticSearch(query, numResults = 5) {
    if (!EINSTEIN_INDEX) throw new Error("Einstein-index är inte laddat.");

    if (!EINSTEIN_PIPELINE) {
        console.log('Laddar embedding-modell...');
        EINSTEIN_PIPELINE = await pipeline('feature-extraction', EINSTEIN_MODEL_NAME);
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

function renderEinsteinResults(container, results) {
    container.innerHTML = ''; // Rensa tidigare resultat
    if (results.length === 0) {
        container.textContent = 'Inga relevanta resultat hittades.';
        return;
    }
    
    const fragment = document.createDocumentFragment();
    results.forEach(result => {
        const resultEl = document.createElement('div');
        resultEl.className = 'einstein-result-item';

        const headerEl = document.createElement('div');
        headerEl.className = 'einstein-result-header';
        
        const sourceLink = document.createElement('a');
        sourceLink.href = '#';
        sourceLink.dataset.path = result.chunk.source;
        sourceLink.textContent = result.chunk.source;
        sourceLink.onclick = (e) => { e.preventDefault(); openFileModal(result.chunk.source); };
        
        const scoreEl = document.createElement('span');
        scoreEl.className = 'einstein-result-score';
        scoreEl.textContent = `Relevans: ${(result.similarity * 100).toFixed(1)}%`;

        headerEl.appendChild(sourceLink);
        headerEl.appendChild(scoreEl);

        const contentEl = document.createElement('pre');
        contentEl.className = 'einstein-result-content';
        contentEl.textContent = result.chunk.content;

        resultEl.appendChild(headerEl);
        resultEl.appendChild(contentEl);
        fragment.appendChild(resultEl);
    });
    container.appendChild(fragment);
}


// --- File Modal Logic ---
async function openFileModal(filePath) {
    const modalOverlay = document.getElementById('file-modal-overlay');
    const modal = document.getElementById('file-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalLoader = document.getElementById('modal-loader');
    const modalSpinner = document.getElementById('modal-loader-spinner');
    const modalError = document.getElementById('modal-error');
    const modalContentPre = document.getElementById('modal-content-pre');

    if (!modalOverlay || !modalTitle) return;

    modal.classList.remove('einstein-mode');
    modalSpinner.classList.add('hidden');
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

async function openEinsteinModal(query) {
    const modalOverlay = document.getElementById('file-modal-overlay');
    const modal = document.getElementById('file-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalLoader = document.getElementById('modal-loader');
    const modalSpinner = document.getElementById('modal-loader-spinner');
    const modalError = document.getElementById('modal-error');
    const modalContentPre = document.getElementById('modal-content-pre');

    modal.classList.add('einstein-mode');
    modalTitle.textContent = `Fråga: "${query}"`;
    modalLoader.classList.remove('hidden');
    modalSpinner.classList.remove('hidden');
    modalError.classList.add('hidden');
    modalContentPre.innerHTML = '';
    modalOverlay.classList.remove('hidden');

    try {
        const results = await performSemanticSearch(query);
        renderEinsteinResults(modalContentPre, results);
    } catch (error) {
        console.error("Fel vid semantisk sökning:", error);
        modalError.textContent = `Sökningen misslyckades: ${error.message}`;
        modalError.classList.remove('hidden');
    } finally {
        modalLoader.classList.add('hidden');
        modalSpinner.classList.add('hidden');
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
    const ribbonPanes = document.querySelectorAll('.ribbon-pane');
    const fullPageContainer = document.getElementById('full-page-container');
    const closeFullPageBtn = document.getElementById('close-full-page-btn');
    const modalOverlay = document.getElementById('file-modal-overlay');
    const modalCloseBtn = document.getElementById('modal-close-btn');
    const modalCopyPathBtn = document.getElementById('modal-copy-path');
    const modalCopyContentBtn = document.getElementById('modal-copy-content');
    const modalDownloadFileBtn = document.getElementById('modal-download-file');
    const einsteinBtn = document.getElementById('einstein-toggle-btn');
    const searchInput = document.getElementById('main-search-input');
    
    initializeEinstein();

    if (einsteinBtn && searchInput) {
        einsteinBtn.addEventListener('click', async () => {
            if (einsteinBtn.classList.contains('active')) {
                const query = searchInput.value.trim();
                if (query) {
                    await openEinsteinModal(query);
                }
            } else {
                try {
                    const text = await navigator.clipboard.readText();
                    if (text.trim()) {
                        searchInput.value = text.trim();
                    }
                    searchInput.placeholder = "Ange semantisk fråga...";
                    einsteinBtn.classList.add('active');
                    searchInput.focus();
                } catch (err) {
                    console.warn('Kunde inte läsa från urklipp:', err);
                    searchInput.placeholder = "Kunde inte läsa urklipp. Skriv fråga...";
                    einsteinBtn.classList.add('active');
                    searchInput.focus();
                }
            }
        });
        
        searchInput.addEventListener('blur', () => {
             if (!searchInput.value.trim()) {
                einsteinBtn.classList.remove('active');
                searchInput.placeholder = "Sök filer...";
            }
        });

        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && einsteinBtn.classList.contains('active')) {
                e.preventDefault();
                const query = searchInput.value.trim();
                if (query) {
                    openEinsteinModal(query);
                }
            }
        });
    }

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
            ribbonPanes.forEach(pane => { pane.classList.toggle('active', 'tab-' + targetTab === pane.id); });
            if (targetTab === 'performance') { fullPageContainer.classList.add('active'); } 
            else { fullPageContainer.classList.remove('active'); }
        });
    });

    if(closeFullPageBtn) {
        closeFullPageBtn.addEventListener('click', () => {
            fullPageContainer.classList.remove('active');
            const verktygTab = document.querySelector('.ribbon-tab[data-tab=\"verktyg\"]');
            if (verktygTab) verktygTab.click();
        });
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
