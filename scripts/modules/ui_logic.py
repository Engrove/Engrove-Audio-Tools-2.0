# scripts/modules/ui_logic.py
#
# === HISTORIK ===
# * v3.0 (2025-08-15): Lade till logik för ribbon-menyn och resizer.
# * v5.0 (2025-08-16): (Help me God) Återställd och verifierad. Lade till
#   förberedande, vilande funktioner för "Operation: Dold Grund".
# * v6.0 (2025-08-16): Refaktorerad för modularitet. All logik för filträdet har
#   flyttats till den dedikerade modulen `ui_file_tree.py`. Denna fil
#   innehåller nu endast generell UI-logik.
#
# === TILLÄMPADE REGLER (Frankensteen v5.6) ===
# - Obligatorisk Refaktorisering: Logiken är nu uppdelad i separata, ansvarsfulla moduler.
# - Fullständig Kod: Verifierat komplett.

JS_LOGIC = """
document.addEventListener('DOMContentLoaded', () => {
    console.log('Engrove Audio Tools UI Initialized.');

    // --- Referenser till DOM-element ---
    const leftPane = document.getElementById('left-pane');
    const resizer = document.getElementById('resizer');
    const ribbonTabs = document.querySelectorAll('.ribbon-tab');
    const ribbonPanes = document.querySelectorAll('.ribbon-pane');
    
    // --- Ribbon Menu Logic ---
    ribbonTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetPaneId = 'tab-' + tab.dataset.tab;
            ribbonTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            ribbonPanes.forEach(pane => {
                pane.classList.toggle('active', pane.id === targetPaneId);
            });
        });
    });
    
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
