# scripts/modules/ui_file_tree.py
#
# === SYFTE & ANSVAR ===
# Denna modul innehåller den isolerade JavaScript-logiken för att rendera och
# hantera det interaktiva, hierarkiska filträdet med tri-state-kryssrutor.
# Den exporterar en strängvariabel som kan databerikas av ett byggskript.
#
# === HISTORIK ===
# * v1.0 (2025-08-16): Initial skapelse som en del av Operation: Modularitet.
# * v1.1 (2025-08-16): KRITISK FIX: Ändrat datainjektion till att använda JSON.parse().
# * v1.2 (2025-08-16): (Help me God - Domslut) Ersatt den osäkra platshållaren med en
#   syntaktiskt giltig, citerad dummy-sträng för att förhindra parse-fel.
# * v2.0 (2025-08-16): Implementerat tri-state kryssrutor och auto-expandering.
# * v2.1 (2025-08-16): Separerade klickhändelser för filnamn.
# * v2.2 (2025-08-17): Lade till rendering av fil- och mappstorlekar.
# * v2.3 (2025-08-17): Tog bort den hårdkodade <h2>Filträd</h2>-rubriken för ett renare UI.
#
# === TILLÄMPADE REGLER (Frankensteen v5.6) ===
# - Grundbulten v3.2: Denna ändring följer den uppgraderade processen för transparens.

JS_FILE_TREE_LOGIC = """
// === Engrove File Tree Logic v2.3 ===

const FILE_TREE_DATA = JSON.parse(__INJECT_FILE_TREE__);

function formatSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'kB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    const num = parseFloat((bytes / Math.pow(k, i)).toFixed(1));
    return `${num} ${sizes[i]}`;
}

function updateParents(element) {
    const parentLi = element.parentElement.closest('li.tree-node');
    if (!parentLi) return;

    const parentCheckbox = parentLi.querySelector(':scope > .node-label > input[type="checkbox"]');
    if (!parentCheckbox) return;
    
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

function updateChildren(element, isChecked) {
    const childCheckboxes = element.querySelectorAll('li .node-label > input[type="checkbox"]');
    childCheckboxes.forEach(cb => {
        cb.checked = isChecked;
        cb.indeterminate = false;
    });
}

function renderNode(nodeData) {
    const isDir = nodeData.type === 'directory';
    
    const li = document.createElement('li');
    li.className = 'tree-node';

    const label = document.createElement('label');
    label.className = 'node-label';

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.dataset.path = nodeData.path;
    
    checkbox.addEventListener('click', (e) => {
        e.stopPropagation();
        updateChildren(li, checkbox.checked);
        updateParents(li);
        
        if (isDir && checkbox.checked) {
            const toggle = li.querySelector(':scope > .toggle-icon');
            if (toggle && li.classList.contains('collapsed')) {
                li.classList.remove('collapsed');
                toggle.textContent = '▼';
            }
        }
    });

    label.appendChild(checkbox);

    if (isDir) {
        const toggle = document.createElement('span');
        toggle.className = 'toggle-icon';
        toggle.textContent = '►';
        toggle.addEventListener('click', (e) => {
            e.stopPropagation();
            li.classList.toggle('collapsed');
            toggle.textContent = li.classList.contains('collapsed') ? '►' : '▼';
        });
        li.appendChild(toggle);
        li.classList.add('collapsed');
    }

    const icon = document.createElement('span');
    icon.className = 'node-icon';
    icon.textContent = isDir ? '📁' : '📄';
    label.appendChild(icon);

    const text = document.createElement('span');
    text.className = 'node-text';
    text.textContent = nodeData.name;
    
    if (isDir) {
        text.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            const toggle = li.querySelector(':scope > .toggle-icon');
            if (toggle) toggle.click();
        });
    } else {
        text.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            if (window.openFileModal) {
                window.openFileModal(nodeData.path);
            }
        });
    }
    
    label.appendChild(text);
    
    const tagsContainer = document.createElement('div');
    tagsContainer.className = 'metadata-tags';

    if (typeof nodeData.size === 'number') {
        const sizeTag = document.createElement('span');
        sizeTag.className = 'size-tag';
        sizeTag.textContent = formatSize(nodeData.size);
        tagsContainer.appendChild(sizeTag);
    }
    
    if (nodeData.tags && nodeData.tags.length > 0) {
        nodeData.tags.forEach(tag => {
            const tagEl = document.createElement('span');
            tagEl.className = 'metadata-tag';
            tagEl.textContent = tag;
            tagsContainer.appendChild(tagEl);
        });
    }
    
    if (tagsContainer.hasChildNodes()) {
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

function initializeFileTree() {
    const container = document.getElementById('file-tree-container');
    const navContainer = document.getElementById('navigation-container');
    if (!container || typeof FILE_TREE_DATA === 'undefined' || FILE_TREE_DATA === '__INJECT_FILE_TREE__') {
        if(container) container.innerHTML = '<h2>Filträd</h2><p style="color: #ffc107;">Data-injektion misslyckades under bygget.</p>';
        console.error("Filträdets data saknas eller blev inte injicerad.");
        return;
    }
    
    if(navContainer) navContainer.style.display = 'none';
    // KORRIGERING: Ta bort den hårdkodade rubriken
    container.innerHTML = '';
    container.style.display = 'block';

    const rootUl = document.createElement('ul');
    rootUl.className = 'file-tree';
    
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
