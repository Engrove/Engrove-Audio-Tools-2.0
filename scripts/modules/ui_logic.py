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
#
# === TILLÄMPADE REGLER (Frankensteen v5.6) ===
# - Grundbulten v3.3: Denna ändring följer den uppgraderade processen för transparens.
# - GR7 (Fullständig Historik): Historiken har uppdaterats korrekt.

JS_LOGIC = """
// Injektionspunkt för projektkonfiguration (repo/branch)
const ENGROVE_CONFIG = __INJECT_PROJECT_OVERVIEW__;

let currentModalFilePath = null;
let currentModalFileContent = null;

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
    modalContentPre.textContent = '';
    modalOverlay.classList.remove('hidden');

    const repo = ENGROVE_CONFIG.repository;
    const branch = ENGROVE_CONFIG.branch;
    const url = `https://raw.githubusercontent.com/${repo}/${branch}/${filePath}`;

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Nätverksfel: ${response.status} ${response.statusText}`);
        }
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

// Gör funktionen globalt tillgänglig för anrop från ui_file_tree.js
window.openFileModal = openFileModal;

document.addEventListener('DOMContentLoaded', () => {
    console.log('Engrove Audio Tools UI Initialized.');

    // --- Referenser till DOM-element ---
    const leftPane = document.getElementById('left-pane');
    const resizer = document.getElementById('resizer');
    const ribbonTabs = document.querySelectorAll('.ribbon-tab');
    const ribbonPanes = document.querySelectorAll('.ribbon-pane');
    const fullPageContainer = document.getElementById('full-page-container');
    const closeFullPageBtn = document.getElementById('close-full-page-btn');

    // Modal-element
    const modalOverlay = document.getElementById('file-modal-overlay');
    const modalCloseBtn = document.getElementById('modal-close-btn');
    const modalCopyPathBtn = document.getElementById('modal-copy-path');
    const modalCopyContentBtn = document.getElementById('modal-copy-content');
    const modalDownloadFileBtn = document.getElementById('modal-download-file');

    // --- Modal Logic ---
    if (modalOverlay) {
        modalCloseBtn.addEventListener('click', closeFileModal);
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) {
                closeFileModal();
            }
        });
        
        modalCopyPathBtn.addEventListener('click', () => {
            if (currentModalFilePath) {
                navigator.clipboard.writeText(currentModalFilePath).then(() => {
                    // Optional: Add user feedback
                });
            }
        });

        modalCopyContentBtn.addEventListener('click', () => {
            if (currentModalFileContent) {
                navigator.clipboard.writeText(currentModalFileContent).then(() => {
                    // Optional: Add user feedback
                });
            }
        });

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
    
    // --- Ribbon Menu Logic ---
    ribbonTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.dataset.tab;
            
            ribbonTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            ribbonPanes.forEach(pane => {
                pane.classList.toggle('active', 'tab-' + targetTab === pane.id);
            });

            // Hantera fullskärms-overlay
            if (targetTab === 'performance') {
                fullPageContainer.classList.add('active');
            } else {
                fullPageContainer.classList.remove('active');
            }
        });
    });

    if(closeFullPageBtn) {
        closeFullPageBtn.addEventListener('click', () => {
            fullPageContainer.classList.remove('active');
            // Återställ till 'Verktyg'-fliken
            const verktygTab = document.querySelector('.ribbon-tab[data-tab="verktyg"]');
            if (verktygTab) verktygTab.click();
        });
    }
    
    // --- Resizer Logic ---
    if(resizer && leftPane) {
        let isResizing = false;
        let initialX = 0;
        let initialWidth = 0;
        resizer.addEventListener('mousedown', (e) => {
            isResizing = true;
            initialX = e.clientX;
            initialWidth = leftPane.offsetWidth;
            document.addEventListener('mousemove', handleMouseMove);
            document.addEventListener('mouseup', handleMouseUp);
        });
        const handleMouseMove = (e) => {
            if (!isResizing) return;
            const deltaX = e.clientX - initialX;
            const newWidth = initialWidth + deltaX;
            const minWidth = 200;
            const maxWidth = document.body.clientWidth * 0.8;
            if (newWidth > minWidth && newWidth < maxWidth) {
                leftPane.style.width = `${newWidth}px`;
            }
        };
        const handleMouseUp = () => {
            isResizing = false;
            document.removeEventListener('mousemove', handleMouseMove);
            document.removeEventListener('mouseup', handleMouseUp);
        };
    }
});
"""
# scripts/modules/ui_logic.py
