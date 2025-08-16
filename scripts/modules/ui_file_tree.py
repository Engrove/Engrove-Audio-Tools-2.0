# scripts/modules/ui_file_tree.py
#
# === SYFTE & ANSVAR ===
# Denna modul innehåller den isolerade JavaScript-logiken för att rendera och
# hantera det interaktiva, hierarkiska filträdet med tri-state-kryssrutor.
# Den exporterar en strängvariabel som kan databerikas av ett byggskript.
#
# === HISTORIK ===
# * v1.0 (2025-08-16): Initial skapelse som en del av Operation: Modularitet.
# * v1.1 (2025-08-16): KRITISK FIX: Ändrat datainjektionen till att använda JSON.parse()
#   för att förhindra syntaxfel från specialtecken i datan.
#
# === TILLÄMPADE REGLER (Frankensteen v5.6) ===
# - Help me God: Grundorsaksanalys av ett SyntaxError ledde till denna robustare design.
# - API-kontraktsverifiering: Modulen använder nu en säkrare metod för datainjektion.

JS_FILE_TREE_LOGIC = """
// === Engrove File Tree Logic v1.1 ===

// JSON-datan injiceras som en sträng och parsas säkert.
const FILE_TREE_DATA = JSON.parse(`${file_tree_json}`);

/**
 * Uppdaterar alla föräldrars kryssrutor uppåt i trädet.
 * @param {HTMLElement} element - Det <li>-element vars barn har ändrats.
 */
function updateParents(element) {
    const parentLi = element.parentElement.closest('li.tree-node');
    if (!parentLi) return;

    const parentCheckbox = parentLi.querySelector(':scope > .node-label > input[type="checkbox"]');
    const childCheckboxes = Array.from(parentLi.querySelectorAll(':scope > ul > li > .node-label > input[type="checkbox"]'));

    if (childCheckboxes.length === 0) return;

    const checkedCount = childCheckboxes.filter(cb => cb.checked).length;
    const indeterminateCount = childCheckboxes.filter(cb => cb.indeterminate).length;
    
    if (checkedCount === 0 && indeterminateCount === 0) {
        parentCheckbox.checked = false;
        parentCheckbox.indeterminate = false;
    } else if (checkedCount === childCheckboxes.length) {
        parentCheckbox.checked = true;
        parentCheckbox.indeterminate = false;
    } else {
        parentCheckbox.checked = false;
        parentCheckbox.indeterminate = true;
    }
    updateParents(parentLi);
}

/**
 * Uppdaterar alla barns kryssrutor nedåt i trädet.
 * @param {HTMLElement} element - Det <li>-element vars kryssruta har klickats.
 * @param {boolean} isChecked - Den nya statusen för kryssrutan.
 */
function updateChildren(element, isChecked) {
    const childCheckboxes = element.querySelectorAll('li > .node-label > input[type="checkbox"]');
    childCheckboxes.forEach(cb => {
        cb.checked = isChecked;
        cb.indeterminate = false;
    });
}

/**
 * Skapar och returnerar ett HTML-element för en enskild nod i trädet.
 * @param {object} nodeData - Dataobjektet för noden.
 * @returns {HTMLLIElement} Det färdiga <li>-elementet.
 */
function renderNode(nodeData) {
    const isDir = nodeData.type === 'directory';
    
    const li = document.createElement('li');
    li.className = 'tree-node';
    if (!isDir) li.style.paddingLeft = '20px';

    const label = document.createElement('label');
    label.className = 'node-label';

    if (isDir) {
        const toggle = document.createElement('span');
        toggle.className = 'toggle-icon';
        toggle.textContent = '►';
        toggle.onclick = (e) => {
            e.stopPropagation();
            li.classList.toggle('collapsed');
            toggle.textContent = li.classList.contains('collapsed') ? '►' : '▼';
        };
        li.appendChild(toggle);
        li.classList.add('collapsed');
    }

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.dataset.path = nodeData.path;
    checkbox.onclick = (e) => {
        // Stoppa eventet från att bubbla till label, vilket skulle trigga det två gånger.
        e.stopPropagation();
        updateChildren(li, checkbox.checked);
        updateParents(li);
    };

    const icon = document.createElement('span');
    icon.className = 'node-icon';
    icon.textContent = isDir ? '📁' : '📄';

    const text = document.createElement('span');
    text.className = 'node-text';
    text.textContent = nodeData.name;
    
    label.appendChild(checkbox);
    label.appendChild(icon);
    label.appendChild(text);
    label.onclick = () => checkbox.click(); // Gör hela raden klickbar

    if (nodeData.tags && nodeData.tags.length > 0) {
        const tagsContainer = document.createElement('div');
        tagsContainer.className = 'metadata-tags';
        nodeData.tags.forEach(tag => {
            const tagEl = document.createElement('span');
            tagEl.className = 'metadata-tag';
            tagEl.textContent = tag;
            tagsContainer.appendChild(tagEl);
        });
        label.appendChild(tagsContainer);
    }

    li.appendChild(label);

    if (isDir && nodeData.children && nodeData.children.length > 0) {
        const ul = document.createElement('ul');
        nodeData.children.forEach(childNode => {
            ul.appendChild(renderNode(childNode));
        });
        li.appendChild(ul);
    }
    
    return li;
}

/**
 * Initialiserar och renderar hela filträdet.
 */
function initializeFileTree() {
    const container = document.getElementById('file-tree-container');
    const navContainer = document.getElementById('navigation-container');
    if (!container || typeof FILE_TREE_DATA === 'undefined') {
        console.error("Filträdets container eller data saknas.");
        return;
    }
    
    if(navContainer) navContainer.style.display = 'none';
    container.innerHTML = '<h2>Filträd</h2>';
    container.style.display = 'block';

    const rootUl = document.createElement('ul');
    rootUl.className = 'file-tree';
    
    // Anta att FILE_TREE_DATA är rot-objektet
    if (FILE_TREE_DATA.children) {
        FILE_TREE_DATA.children.forEach(node => {
            rootUl.appendChild(renderNode(node));
        });
    }
    container.appendChild(rootUl);
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeFileTree);
} else {
    initializeFileTree();
}
"""
# scripts/modules/ui_file_tree.py
