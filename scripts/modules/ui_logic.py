# scripts/modules/ui_logic.py
#
# === HISTORIK ===
# * v1.0 (2025-08-15): Initial skapelse med grundläggande interaktivitet.
# * v2.0 (2025-08-15): Implementerade logik för justerbar delningslinje.
# * v3.0 (2025-08-15): Lade till logik för att hantera ribbon-menyns flikar.
#
# === TILLÄMPADE REGLER (Frankensteen v5.4) ===
# - Obligatorisk Refaktorisering: Logiken är uppdelad i tydliga sektioner.

JS_LOGIC = """
document.addEventListener('DOMContentLoaded', () => {
    console.log('Engrove Audio Tools UI Initialized with Ribbon Menu.');

    // --- Ribbon Menu Logic ---
    const ribbonTabs = document.querySelectorAll('.ribbon-tab');
    const ribbonPanes = document.querySelectorAll('.ribbon-pane');
    const rightPane = document.getElementById('right-pane'); // Referens till högerpanelen

    ribbonTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetPaneId = 'tab-' + tab.dataset.tab;

            // Uppdatera aktiv status för flikar
            ribbonTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            // Visa/dölj ribbon-paneler
            ribbonPanes.forEach(pane => {
                pane.classList.toggle('active', pane.id === targetPaneId);
            });
            
            console.log(`Ribbon tab '${tab.dataset.tab}' selected.`);
            if(rightPane){
                 rightPane.innerHTML = `<h2>Vy för '${tab.textContent}'</h2><p>Innehållet för detta verktyg visas här.</p>`;
            }
        });
    });
    
    // Initialisera logik för knappar i ribbon (exempel)
    document.body.addEventListener('click', event => {
        const target = event.target;
        if(target.tagName === 'BUTTON' && target.closest('.ribbon-group')) {
            console.log(`Ribbon button '${target.textContent}' clicked.`);
            if(rightPane){
                 rightPane.innerHTML = `<h2>Åtgärd: ${target.textContent}</h2><p>Visar resultat för denna åtgärd.</p>`;
            }
        }
    });


    // --- Resizer Logic (oförändrad) ---
    const resizer = document.getElementById('resizer');
    const leftPane = document.getElementById('left-pane');

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
