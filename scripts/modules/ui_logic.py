# scripts/modules/ui_logic.py
#
# === HISTORIK ===
# * v1.0 (2025-08-15): Initial skapelse med grundläggande interaktivitet.
# * v2.0 (2025-08-15): Implementerade logik för justerbar delningslinje.
#
# === TILLÄMPADE REGLER (Frankensteen v5.4) ===
# - Obligatorisk Refaktorisering: All JS-logik är separerad.

JS_LOGIC = """
document.addEventListener('DOMContentLoaded', () => {
    console.log('Engrove Audio Tools UI Initialized.');

    const menuButtons = document.querySelectorAll('.menu-button');
    const rightPane = document.querySelector('.right-pane');
    const searchInput = document.querySelector('.search-container input[type="search"]');

    // --- Meny- och söklogik ---
    menuButtons.forEach(button => {
        button.addEventListener('click', () => {
            const buttonText = button.textContent;
            console.log(`Menyknapp '${buttonText}' klickades.`);
            if (rightPane) {
                rightPane.innerHTML = `<h2>'${buttonText}' valdes</h2><p>Funktionalitet för detta val kommer att implementeras här.</p>`;
            }
        });
    });

    if (searchInput) {
        searchInput.addEventListener('input', (event) => {
            console.log(`Sökterm: ${event.target.value}`);
            if (rightPane) {
                rightPane.innerHTML = `<h2>Sökning</h2><p>Söker efter: <strong>${event.target.value}</strong></p>`;
            }
        });
    }

    // --- Logik för justerbar panel ---
    const resizer = document.getElementById('resizer');
    const leftPane = document.getElementById('left-pane');

    let isResizing = false;
    let initialX = 0;
    let initialWidth = 0;

    resizer.addEventListener('mousedown', (e) => {
        isResizing = true;
        initialX = e.clientX;
        initialWidth = leftPane.offsetWidth;
        
        // Lägg till globala lyssnare för att hantera drag utanför resizer-elementet
        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseup', handleMouseUp);
    });

    function handleMouseMove(e) {
        if (!isResizing) return;
        
        const deltaX = e.clientX - initialX;
        const newWidth = initialWidth + deltaX;
        
        // Sätt gränser för att panelen inte ska bli för liten eller för stor
        const minWidth = 200; // Matchar min-width i CSS
        const maxWidth = document.body.clientWidth * 0.8; // Max 80% av fönstret
        
        if (newWidth > minWidth && newWidth < maxWidth) {
            leftPane.style.width = `${newWidth}px`;
        }
    }

    function handleMouseUp() {
        isResizing = false;
        // Rensa globala lyssnare för att sluta spåra musen
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
    }
});
"""
# scripts/modules/ui_logic.py
