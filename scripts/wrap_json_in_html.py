# scripts/wrap_json_in_html.py
#
# HISTORIK:
# * v1.0 (Initial): Första versionen.
# * v2.0 (Bug Fix): Felaktig implementation med str.format().
# * v3.0 (Definitive Fix): Implementerar html.escape() och <pre>-tagg.
# * v4.0 (UI Enhancement): Lade till kopiera/ladda ner knappar.
# * v5.0 (Full Interactive UI): Total omskrivning för ett interaktivt "Context Builder" UI.
# * v6.0 (Stub/Full Logic): Implementerade den nya kärnlogiken. "Generate Context" skapar nu en
#   fullständig filstruktur där omarkerade filer inkluderas som "stubs" (metadata utan
#   källkod) och markerade filer inkluderas med fullständigt innehåll.
#
# TILLÄMPADE REGLER (Frankensteen v3.7):
# - Denna fil följer principen om Single Responsibility: den bygger ett UI.
# - Ingen databearbetning sker i Python. All logik ligger i det inbäddade JavaScriptet.
# - JavaScript-koden är skriven för att vara robust, med felhantering och effektiv event-delegering.
# - Kärnlogiken för kontextbygge är nu rekursiv och hanterar djupkopiering för att undvika sidoeffekter.

import sys
import os

def create_interactive_html(output_html_path):
    """
    Genererar en komplett, interaktiv HTML-sida som fungerar som en "AI Context Builder".
    Sidan hämtar `context.json` asynkront och låter användaren välja filer/mappar
    för att bygga en anpassad, nedladdningsbar kontext.
    """

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Context Builder</title>
    <style>
        :root {
            --primary-bg: #f8f9fa;
            --secondary-bg: #ffffff;
            --border-color: #dee2e6;
            --text-color: #212529;
            --accent-color: #007bff;
            --accent-hover: #0056b3;
            --danger-color: #dc3545;
            --font-main: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            --font-mono: "JetBrains Mono", "SF Mono", "Consolas", "Liberation Mono", "Menlo", monospace;
        }
        body {
            font-family: var(--font-main);
            background-color: var(--primary-bg);
            color: var(--text-color);
            margin: 0;
            display: flex;
            height: 100vh;
            overflow: hidden;
        }
        .panel {
            padding: 1em;
            overflow-y: auto;
            border-right: 1px solid var(--border-color);
        }
        #left-panel {
            width: 40%;
            min-width: 300px;
            display: flex;
            flex-direction: column;
        }
        #right-panel {
            width: 60%;
            display: flex;
            flex-direction: column;
        }
        .controls {
            padding-bottom: 1em;
            margin-bottom: 1em;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        button {
            font-size: 14px;
            padding: 8px 16px;
            border-radius: 6px;
            border: 1px solid var(--border-color);
            cursor: pointer;
            background-color: var(--secondary-bg);
            color: var(--text-color);
            transition: background-color 0.2s, border-color 0.2s;
        }
        button:hover {
            background-color: #e9ecef;
        }
        button:disabled {
            background-color: #e9ecef;
            cursor: not-allowed;
            opacity: 0.7;
        }
        button.primary {
            background-color: var(--accent-color);
            color: white;
            border-color: var(--accent-color);
        }
        button.primary:hover {
            background-color: var(--accent-hover);
        }
        #file-tree-container {
            flex-grow: 1;
        }
        #file-tree-container ul {
            list-style-type: none;
            padding-left: 20px;
        }
        #file-tree-container li {
            padding: 4px 0;
        }
        .toggle {
            cursor: pointer;
            user-select: none;
            display: inline-block;
            width: 1em;
        }
        label {
            cursor: pointer;
        }
        .icon {
            display: inline-block;
            width: 1.2em;
        }
        #output-pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            background-color: var(--secondary-bg);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 1em;
            flex-grow: 1;
            font-family: var(--font-mono);
            font-size: 14px;
        }
    </style>
</head>
<body>

<div id="left-panel" class="panel">
    <div class="controls">
        <button id="select-all-btn">Select All</button>
        <button id="deselect-all-btn">Deselect All</button>
        <button id="generate-context-btn" class="primary">Generate Context</button>
    </div>
    <div id="file-tree-container">
        <p>Loading context data...</p>
    </div>
</div>

<div id="right-panel" class="panel">
    <div class="controls">
        <button id="download-json-btn" disabled>Download Generated JSON</button>
    </div>
    <pre id="output-pre">Generated context will appear here.</pre>
</div>

<script>
    document.addEventListener('DOMContentLoaded', () => {
        // --- State ---
        let fullContext = null;

        // --- DOM Elements ---
        const fileTreeContainer = document.getElementById('file-tree-container');
        const outputPre = document.getElementById('output-pre');
        const selectAllBtn = document.getElementById('select-all-btn');
        const deselectAllBtn = document.getElementById('deselect-all-btn');
        const generateBtn = document.getElementById('generate-context-btn');
        const downloadBtn = document.getElementById('download-json-btn');
        
        // --- Core Functions ---

        /**
         * Recursively renders the file tree structure into the DOM.
         * @param {object} node - The current node in the file_structure object.
         * @param {HTMLElement} parentElement - The DOM element to append children to.
         * @param {string} currentPath - The accumulated path to the current node.
         */
        function renderFileTree(node, parentElement, currentPath) {
            const ul = document.createElement('ul');
            
            Object.keys(node).sort().forEach(key => {
                const item = node[key];
                const itemPath = currentPath ? `${currentPath}/${key}` : key;
                const li = document.createElement('li');

                const isFolder = item.type !== 'file';

                const label = document.createElement('label');
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.setAttribute('data-path', itemPath);
                
                label.appendChild(checkbox);

                if (isFolder) {
                    li.classList.add('folder');
                    const toggle = document.createElement('span');
                    toggle.className = 'toggle';
                    toggle.textContent = '►'; // Collapsed by default
                    li.appendChild(toggle);
                    
                    label.appendChild(document.createTextNode(` ${key}`));
                    li.appendChild(label);

                    const nestedUl = renderFileTree(item, li, itemPath);
                    nestedUl.style.display = 'none'; // Initially collapsed
                    li.appendChild(nestedUl);

                } else { // It's a file
                    li.classList.add('file');
                    const icon = document.createElement('span');
                    icon.className = 'icon';
                    icon.textContent = '📄';
                    label.prepend(icon);
                    label.appendChild(document.createTextNode(` ${key}`));
                    li.appendChild(label);
                }
                ul.appendChild(li);
            });
            parentElement.appendChild(ul);
            return ul;
        }
        
        /**
         * Recursively builds the new file_structure object based on user selections.
         * @param {object} sourceNode - The current node from the original fullContext.file_structure.
         * @param {Set<string>} selectedPaths - A set of all paths that are checked.
         * @returns {object} The new node for the generated context.
         */
        function buildNewContextStructure(sourceNode, selectedPaths) {
            const newNode = {};

            for (const key in sourceNode) {
                const item = sourceNode[key];
                
                if (item.type === 'file') {
                    // This is a file node
                    if (selectedPaths.has(item.path)) {
                        // ** Full copy: File is selected, include everything **
                        newNode[key] = JSON.parse(JSON.stringify(item));
                    } else {
                        // ** Stub copy: File is not selected, omit content **
                        const stub = JSON.parse(JSON.stringify(item));
                        delete stub.content; // The critical operation
                        newNode[key] = stub;
                    }
                } else {
                    // This is a directory node, recurse deeper
                    newNode[key] = buildNewContextStructure(item, selectedPaths);
                }
            }
            return newNode;
        }


        /**
         * Generates a new context object based on the selected checkboxes.
         */
        function generateSelectedContext() {
            if (!fullContext) return;

            const selectedPaths = new Set(
                Array.from(fileTreeContainer.querySelectorAll('input[type="checkbox"]:checked'))
                .map(cb => cb.dataset.path)
            );
            
            // Start with a clean context, preserving top-level info
            const newContext = {
                project_overview: fullContext.project_overview,
                ai_instructions: fullContext.ai_instructions,
                project_documentation: {},
                file_structure: {}
            };

            // Rebuild the documentation object, only including selected docs
            if (fullContext.project_documentation) {
                for (const docKey in fullContext.project_documentation) {
                    const docPath = `docs/${docKey}`;
                    if (selectedPaths.has(docPath)) {
                        newContext.project_documentation[docKey] = fullContext.project_documentation[docKey];
                    }
                }
            }
            
            // Recursively build the new file structure with stub/full logic
            newContext.file_structure = buildNewContextStructure(fullContext.file_structure, selectedPaths);
            
            outputPre.textContent = JSON.stringify(newContext, null, 2);
            downloadBtn.disabled = false;
        }

        // --- Event Listeners ---

        fileTreeContainer.addEventListener('click', (e) => {
            const target = e.target;

            // Handle folder expand/collapse
            if (target.classList.contains('toggle')) {
                const nestedUl = target.parentElement.querySelector('ul');
                if (nestedUl) {
                    const isCollapsed = nestedUl.style.display === 'none';
                    nestedUl.style.display = isCollapsed ? 'block' : 'none';
                    target.textContent = isCollapsed ? '▼' : '►';
                }
            }

            // Handle hierarchical checkbox selection
            if (target.type === 'checkbox') {
                const li = target.closest('li');
                if (li) {
                    const nestedCheckboxes = li.querySelectorAll('input[type="checkbox"]');
                    nestedCheckboxes.forEach(cb => cb.checked = target.checked);
                }
            }
        });

        selectAllBtn.addEventListener('click', () => {
            fileTreeContainer.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = true);
        });

        deselectAllBtn.addEventListener('click', () => {
            fileTreeContainer.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);
        });

        generateBtn.addEventListener('click', generateSelectedContext);

        downloadBtn.addEventListener('click', () => {
            const content = outputPre.textContent;
            const blob = new Blob([content], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            const date = new Date().toISOString().slice(0, 10);
            
            a.href = url;
            a.download = `context_custom_${date}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        });
        
        // --- Initialization ---

        fetch('context.json')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                fullContext = data;
                fileTreeContainer.innerHTML = ''; // Clear "Loading..." message
                renderFileTree(fullContext.file_structure, fileTreeContainer, '');
                
                // Also render docs as a selectable "folder"
                if (fullContext.project_documentation && Object.keys(fullContext.project_documentation).length > 0) {
                     const docsNode = {};
                     Object.keys(fullContext.project_documentation).forEach(docKey => {
                         docsNode[docKey] = { type: 'file' };
                     });
                     const docsTree = { 'docs': docsNode };
                     renderFileTree(docsTree, fileTreeContainer, '');
                }
            })
            .catch(error => {
                fileTreeContainer.innerHTML = `<p style="color: var(--danger-color);"><b>Error:</b> Could not load context.json. ${error.message}</p>`;
                console.error('Failed to load context.json:', error);
            });
    });
</script>

</body>
</html>"""

    try:
        with open(output_html_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
        print(f"[INFO] Wrapper: Skapade framgångsrikt den interaktiva HTML-filen '{output_html_path}'.")

    except Exception as e:
        print(f"[ERROR] Wrapper: Ett oväntat fel inträffade vid skrivning till fil: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        # Denna del är nu mindre relevant då filen inte längre behöver en JSON-input,
        # men vi behåller signaturen för att vara konsekvent med GHA-workflowet.
        print("Användning: python wrap_json_in_html.py <dummy-input.json> <sökväg-till-output.html>", file=sys.stderr)
        sys.exit(1)

    # sys.argv[1] (input_file) ignoreras medvetet.
    output_file = sys.argv[2]
    
    # Skapa output-mappen om den inte finns
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        
    create_interactive_html(output_file)
