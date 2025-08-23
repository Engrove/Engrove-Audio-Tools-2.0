# scripts/modules/ui_einstein_search.py
#
# === SYFTE & ANSVAR ===
# Denna modul innehåller all JavaScript-logik för den nya, fristående Einstein
# sökfunktionen. Den ansvarar för att hantera sökningar, rendera den strukturerade
# resultatlistan baserat på core_file_info.json, och hantera interaktivitet.
#
# === HISTORIK ===
# * v1.0 (2025-08-18): Initial skapelse som en del av arkitektonisk refaktorering av sök.
# * v1.1 (2025-08-23): (Help me God - Domslut) Reintroducerade JSON.parse() för injicerad payload för att åtgärda SyntaxError.
# * v2.0 (2025-08-23): (ARKITEKTURÄNDRING) Ersatt platshållarinjektion med robust "Data Island"-läsning från DOM.
# * SHA256_LF: UNVERIFIED
#
# === TILLÄMPADE REGLER (Frankensteen v5.7) ===
# - Grundbulten v3.8: Denna nya fil har skapats enligt gällande protokoll.
# - GR6 (Obligatorisk Refaktorisering): Söklogiken har isolerats i denna dedikerade modul.
# - GR7 (Fullständig Historik): Historiken har uppdaterats korrekt.

JS_EINSTEIN_LOGIC = """
// === Engrove Einstein Search Logic v2.0 ===

/**
 * Läser och parsar en JSON "Data Island" från en <script>-tagg i DOM.
 * @param {string} id - DOM ID för script-taggen.
 * @returns {object} Det parsade JavaScript-objektet.
 */
function readDataIsland(id) {
    const element = document.getElementById(id);
    if (!element) {
        console.error(`Data Island med ID "${id}" hittades inte i DOM.`);
        return null;
    }
    try {
        return JSON.parse(element.textContent);
    } catch (e) {
        console.error(`Kunde inte parsa JSON från Data Island "${id}":`, e);
        return null;
    }
}

// Läs in metadata från "Data Island".
const EINSTEIN_CORE_FILE_INFO = readDataIsland('data-island-core-info');

function renderEinsteinResults(container, results) {
    container.innerHTML = '';
    if (!results || results.length === 0) {
        container.innerHTML = '<p class=\\"einstein-no-results\\">Inga relevanta resultat hittades.</p>';
        return;
    }

    const fragment = document.createDocumentFragment();
    results.forEach(result => {
        const itemEl = document.createElement('div');
        itemEl.className = 'einstein-result-item';

        const fileInfo = EINSTEIN_CORE_FILE_INFO[result.chunk.source] || {
            purpose_and_responsibility: 'Ingen metadata hittades i core_file_info.json för denna fil.',
            usage_context: 'Informationen kan vara ofullständig.'
        };

        // En enkel escape-funktion för att förhindra XSS
        const escapeHtml = (unsafe) => {
            if (typeof unsafe !== 'string') return '';
            return unsafe
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }

        itemEl.innerHTML = `
            <div class=\\"einstein-result-header\\">
                <a href=\\"#\\" class=\\"einstein-result-path\\" data-path=\\"${escapeHtml(result.chunk.source)}\\">${escapeHtml(result.chunk.source)}</a>
                <span class=\\"einstein-result-score\\">Relevans: ${(result.similarity * 100).toFixed(1)}%</span>
            </div>
            <div class=\\"einstein-result-metadata\\">
                <p><strong>Syfte:</strong> ${escapeHtml(fileInfo.purpose_and_responsibility)}</p>
            </div>
            <details class=\\"einstein-result-details\\">
                <summary>Visa semantisk träff</summary>
                <pre>${escapeHtml(result.chunk.content)}</pre>
            </details>
        `;

        fragment.appendChild(itemEl);
    });

    container.appendChild(fragment);

    // Lägg till event listeners efter att elementen finns i DOM
    container.querySelectorAll('.einstein-result-path').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            if (window.openFileModal) {
                window.openFileModal(e.target.dataset.path);
            }
        });
    });
}

async function handleEinsteinSearch() {
    const queryInput = document.getElementById('einstein-search-input');
    const resultsContainer = document.getElementById('einstein-results-container');
    const statusEl = document.getElementById('einstein-status-bar');

    if (!queryInput || !resultsContainer || !statusEl) return;

    const query = queryInput.value.trim();
    if (!query) return;

    statusEl.textContent = 'Söker...';
    resultsContainer.innerHTML = '';

    try {
        // Förutsätter att performSemanticSearch är globalt tillgänglig från ui_logic.py
        const results = await window.performSemanticSearch(query);
        renderEinsteinResults(resultsContainer, results);
        statusEl.textContent = `Hittade ${results.length} resultat för \\"${query}\\"`;
    } catch (error) {
        console.error("Fel vid Einstein-sökning:", error);
        statusEl.textContent = `Sökningen misslyckades: ${error.message}`;
        resultsContainer.innerHTML = '<p class=\\"einstein-error\\">Ett fel uppstod. Kontrollera webbläsarkonsolen för mer information.</p>';
    }
}


function initEinsteinSearch() {
    const searchButton = document.getElementById('einstein-search-btn');
    const searchInput = document.getElementById('einstein-search-input');

    if (searchButton && searchInput) {
        searchButton.addEventListener('click', handleEinsteinSearch);
        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                handleEinsteinSearch();
            }
        });
        console.log('Einstein Search UI initialiserad.');
    }
}

// Körs när DOM är redo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initEinsteinSearch);
} else {
    initEinsteinSearch();
}
"""
