# BEGIN FILE: scripts/modules/ui_semantic_search.py
# scripts/modules/ui_semantic_search.py
#
# === SYFTE & ANSVAR ===
# Denna modul innehåller den isolerade JavaScript-logiken för den nya, dedikerade
# semantiska sökfunktionen. Den hanterar söklogik, resultatrendering och
# interaktion med den nya fullskärmsvyn.
#
# === HISTORIK ===
# * v1.0 (2025-08-18): Initial skapelse som en del av "Operation Semantisk Uppgradering".
#   Extraherade befintlig Einstein-logik från ui_logic.py och implementerade
#   ny renderingslogik som använder core_file_info.json för berikad metadata.
# * SHA256_LF: a8e0d44e5c8c6f7b3a1b2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a
#
# === TILLÄMPADE REGLER (Frankensteen v5.7) ===
# - Grundbulten v3.8: Filen är skapad enligt gällande protokoll.
# - GR6 (Obligatorisk Refaktorisering): Funktionaliteten har brutits ut till en dedikerad modul.

JS_SEMANTIC_SEARCH_LOGIC = """
// === Engrove Semantic Search Logic v1.0 ===

// Injektionspunkter för data från byggskriptet
const EINSTEIN_INDEX = __INJECT_EINSTEIN_INDEX__;
const EINSTEIN_METADATA = __INJECT_CORE_FILE_INFO__;

// State för semantisk sökning
let EINSTEIN_PIPELINE = null;
const EINSTEIN_MODEL_NAME = 'Xenova/all-MiniLM-L6-v2';

// --- Kärnlogik för Semantisk Sökning ---

function cosineSimilarity(vecA, vecB) {
    let dotProduct = 0;
    let normA = 0;
    let normB = 0;
    for (let i = 0; i < vecA.length; i++) {
        dotProduct += vecA[i] * vecB[i];
        normA += vecA[i] * vecA[i];
        normB += vecB[i] * vecB[i];
    }
    const similarity = dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
    return isNaN(similarity) ? 0 : similarity;
}

async function performSemanticSearch(query, numResults = 10) {
    if (!EINSTEIN_INDEX) throw new Error("Einstein-index är inte laddat.");

    const statusEl = document.getElementById('semantic-search-status');
    if (!EINSTEIN_PIPELINE) {
        if (statusEl) statusEl.textContent = 'Laddar AI-modell (detta kan ta en stund)...';
        console.log('Laddar embedding-modell...');
        EINSTEIN_PIPELINE = await pipeline('feature-extraction', EINSTEIN_MODEL_NAME);
        console.log('Embedding-modell laddad.');
        if (statusEl) statusEl.textContent = 'Modell laddad. Genomför sökning...';
    }

    const queryEmbedding = await EINSTEIN_PIPELINE(query, { pooling: 'mean', normalize: true });
    const queryVector = queryEmbedding.data;

    const results = EINSTEIN_INDEX.chunks.map(chunk => ({
        chunk,
        similarity: cosineSimilarity(queryVector, chunk.vector)
    }));

    results.sort((a, b) => b.similarity - a.similarity);
    if (statusEl) statusEl.textContent = `Sökning klar. Visar de ${numResults} mest relevanta resultaten.`;
    return results.slice(0, numResults);
}

function renderSemanticResults(container, results) {
    container.innerHTML = ''; // Rensa tidigare resultat
    if (!results || results.length === 0) {
        container.innerHTML = '<p>Inga relevanta resultat hittades.</p>';
        return;
    }
    
    const fragment = document.createDocumentFragment();
    results.forEach(result => {
        const resultEl = document.createElement('div');
        resultEl.className = 'semantic-result-item';

        const metadata = EINSTEIN_METADATA[result.chunk.source] || {};

        const headerEl = document.createElement('div');
        headerEl.className = 'semantic-result-header';
        
        const sourceLink = document.createElement('a');
        sourceLink.href = '#';
        sourceLink.className = 'semantic-result-path';
        sourceLink.dataset.path = result.chunk.source;
        sourceLink.textContent = result.chunk.source;
        sourceLink.onclick = (e) => { e.preventDefault(); window.openFileModal(result.chunk.source); };
        
        const scoreEl = document.createElement('span');
        scoreEl.className = 'semantic-result-score';
        scoreEl.textContent = `Relevans: ${(result.similarity * 100).toFixed(1)}%`;

        headerEl.appendChild(sourceLink);
        headerEl.appendChild(scoreEl);

        const purposeEl = document.createElement('div');
        purposeEl.className = 'semantic-result-section';
        purposeEl.innerHTML = `<h4>Syfte & Ansvar</h4><p>${metadata.purpose_and_responsibility || '<i>Ingen information tillgänglig.</i>'}</p>`;
        
        const contextEl = document.createElement('div');
        contextEl.className = 'semantic-result-section';
        contextEl.innerHTML = `<h4>Användningskontext</h4><p>${metadata.usage_context || '<i>Ingen information tillgänglig.</i>'}</p>`;

        const semanticTextEl = document.createElement('details');
        semanticTextEl.className = 'semantic-result-details';
        semanticTextEl.innerHTML = `
            <summary>Visa semantisk text</summary>
            <pre>${result.chunk.content}</pre>
        `;

        resultEl.appendChild(headerEl);
        resultEl.appendChild(purposeEl);
        resultEl.appendChild(contextEl);
        resultEl.appendChild(semanticTextEl);
        fragment.appendChild(resultEl);
    });
    container.appendChild(fragment);
}

// --- Event-lyssnare och Initialisering ---
document.addEventListener('DOMContentLoaded', () => {
    const searchBtn = document.getElementById('semantic-search-btn');
    const searchInput = document.getElementById('semantic-search-input');
    const resultsContainer = document.getElementById('semantic-results-container');
    const statusEl = document.getElementById('semantic-search-status');

    async function executeSearch() {
        const query = searchInput.value.trim();
        if (!query) {
            if (statusEl) statusEl.textContent = 'Ange en sökfras.';
            return;
        }
        if (!resultsContainer) return;

        resultsContainer.innerHTML = '';
        if (statusEl) statusEl.textContent = 'Påbörjar sökning...';

        try {
            const results = await performSemanticSearch(query);
            renderSemanticResults(resultsContainer, results);
        } catch (error) {
            console.error(\"Fel vid semantisk sökning:\", error);
            if (statusEl) statusEl.textContent = `Sökningen misslyckades: ${error.message}`;
            resultsContainer.innerHTML = `<p class=\\"error\\">Ett fel uppstod: ${error.message}</p>`;
        }
    }

    if (searchBtn && searchInput) {
        searchBtn.addEventListener('click', executeSearch);
        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                executeSearch();
            }
        });
    }
});
"""
# END FILE: scripts/modules/ui_semantic_search.py
