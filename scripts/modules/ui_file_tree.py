# BEGIN FILE: scripts/modules/ui_file_tree.py
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
# * v3.0 (2025-08-17): (Help me God - Grundorsaksanalys) Refaktorerat för att ta bort `JSON.parse`.
#   Förlitar sig nu på att byggskriptet injicerar ett direkt JavaScript-objekt-literal.
# * v4.0 (2025-08-18): Exponerat kontrollfunktioner (selectAll, deselectAll, selectCore) på window-objektet för extern åtkomst.
# * v4.1 (2025-08-18): Omarbetat `selectCoreInTree` till `addPathsToSelection` för additivt och dynamiskt urval.
# * v4.2 (2025-08-18): (Help me God - Grundorsaksanalys) Helt omskriven `findPathsUnder`-funktion för robusthet.
# * v4.3 (2025-08-23): (Help me God - Domslut) Reintroducerade JSON.parse() för injicerad payload för att åtgärda SyntaxError.
# * v5.0 (2025-08-23): (ARKITEKTURÄNDRING) Ersatt platshållarinjektion med robust "Data Island"-läsning från DOM.
# * SHA256_LF: UNVERIFIED
#
# === TILLÄMPADE REGLER (Frankensteen v5.7) ===
# - Grundbulten v3.9: Denna fil har modifierats enligt en grundorsaksanalys.
# - Help me God: Den felaktiga logiken har ersatts med en bevisat robustare algoritm.
# - GR7 (Fullständig Historik): Historiken har uppdaterats korrekt.

JS_FILE_TREE_LOGIC = """
// === Engrove File Tree Logic v5.0 ===

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

const FILE_TREE_DATA = readDataIsland('data-island-file-tree');

/**
 * Formaterar bytes till en läsbar sträng (kB, MB, etc.).
 * @param {number} bytes Antalet bytes.
 * @returns {string} Den formaterade storleken.
 */
function formatSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'kB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    const num = parseFloat((bytes / Math.pow(k, i)).toFixed(1));
    return `${num} ${sizes[i]}`;
}

/**
 * Uppdaterar rekurvisivt checkboxtillståndet för alla föräldraelement.
 * @param {HTMLElement} element Det element vars föräldrar ska uppdateras.
 */
function updateParents(element) {
    const parentLi = element.parentElement.closest('li.tree-node');
    if (!parentLi) return;

    const parentCheckbox = parentLi.querySelector(':scope > .node-label > input[type=\\"checkbox\\"]');
    if (!parentCheckbox) return;
    
    const childCheckboxes = Array.from(parentLi.querySelectorAll(':scope > ul > li > .node-label > input[type=\\"checkbox\\"]'));

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
 * Uppdaterar alla underliggande checkboxes till ett specifikt tillstånd.
 * @param {HTMLElement} element Förälderelementet.
 * @param {boolean} isChecked Om checkboxes ska vara markerade eller ej.
 */
function updateChildren(element, isChecked) {
    const childCheckboxes = element.querySelectorAll('li .node-label > input[type=\\"checkbox\\"]');
    childCheckboxes.forEach(cb => {
        cb.checked = isChecked;
        cb.indeterminate = false;
    });
}

/**
 * Renderar en enskild nod (fil eller mapp) i trädet.
 * @param {object} nodeData Datan för noden.
 * @returns {HTMLLIElement} Det skapade LI-elementet.
 */
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

/**
 * Global funktion för att markera alla checkboxes i trädet.
 */
window.selectAllInTree = function() {
    const container = document.getElementById('file-tree-container');
    container.querySelectorAll('input[type=\\"checkbox\\\"]').forEach(cb => {
        cb.checked = true;
        cb.indeterminate = false;
    });
}

/**
 * Global funktion för att avmarkera alla checkboxes i trädet.
 */
window.deselectAllInTree = function() {
    const container = document.getElementById('file-tree-container');
    container.querySelectorAll('input[type=\\"checkbox\\\"]').forEach(cb => {
        cb.checked = false;
        cb.indeterminate = false;
    });
}

/**
 * Hittar rekursivt alla filsökvägar under en given mapp i trädstrukturen.
 * Denna robusta version hittar först startnoden och samlar sedan in alla barn.
 * @param {string} directoryPath - Sökvägen till mappen att söka i (utan avslutande /).
 * @returns {string[]} En array med alla funna filsökvägar.
 */
function findPathsUnder(directoryPath) {
    if (!FILE_TREE_DATA) return [];
    let startNode = null;
    
    function findStartNode(nodes, pathParts) {
        if (!pathParts.length) return null;
        const part = pathParts.shift();
        const node = nodes.find(n => n.name === part);
        if (!node) return null;
        if (pathParts.length === 0) return node;
        return findStartNode(node.children || [], pathParts);
    }

    startNode = findStartNode(FILE_TREE_DATA.children, directoryPath.split('/'));

    if (!startNode || startNode.type !== 'directory') {
        return [];
    }
    
    const paths = [];
    function collectPaths(node) {
        if (node.type === 'file') {
            paths.push(node.path);
        } else if (node.type === 'directory' && node.children) {
            node.children.forEach(collectPaths);
        }
    }
    collectPaths(startNode);
    return paths;
}

/**
 * Global funktion för att lägga till ett urval av filer (statiska och dynamiska) i det nuvarande urvalet.\\
 * @param {string[]} staticPaths - En array av explicita filsökvägar som ska markeras.\\
 * @param {string[]} dynamicPaths - En array av mappsökvägar vars innehåll ska markeras.\\
 */
window.addPathsToSelection = function(staticPaths = [], dynamicPaths = []) {
    let pathsToSelect = [...staticPaths];

    dynamicPaths.forEach(dirPath => {
        const foundPaths = findPathsUnder(dirPath);
        pathsToSelect.push(...foundPaths);
    });

    const container = document.getElementById('file-tree-container');
    const allCheckboxes = Array.from(container.querySelectorAll('input[type=\\"checkbox\\\"]'));
    
    const selectionSet = new Set(pathsToSelect);

    selectionSet.forEach(p => {
        const cb = allCheckboxes.find(x => x.dataset.path === p);
        if (cb && !cb.checked) {
            cb.checked = true;
            let li = cb.closest('li.tree-node');
            while(li) {
                const parent = li.parentElement.closest('li.tree-node');
                if(parent) {
                    const toggle = parent.querySelector(':scope > .toggle-icon');
                    if(toggle && parent.classList.contains('collapsed')) {
                        parent.classList.remove('collapsed');
                        toggle.textContent = '▼';
                    }
                }
                li = parent;
            }
        }
    });

    allCheckboxes.forEach(cb => {
        if (cb.checked) {
            updateParents(cb.closest('li.tree-node'));
        }
    });
}

/**
 * Initialiserar och renderar hela filträdet.\\
 */
function initializeFileTree() {
    const container = document.getElementById('file-tree-container');
    if (!container || !FILE_TREE_DATA) {
        if(container) container.innerHTML = '<p style=\\"color: #ffc107;\\">Kunde inte ladda filträdets data.</p>';
        console.error("Filträdets data kunde inte läsas från DOM.");
        return;
    }
    
    container.innerHTML = '';
    
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
