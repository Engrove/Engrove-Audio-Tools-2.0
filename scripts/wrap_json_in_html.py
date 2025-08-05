# scripts/wrap_json_in_html.py
#
# HISTORIK:
# * v1.0 (Initial): Första versionen.
# * v2.0 (Bug Fix): Felaktig implementation med str.format().
# * v3.0 (Definitive Fix): Implementerar html.escape() och <pre>-tagg.
# * v4.0 (UI Enhancement): Lade till kopiera/ladda ner knappar.
# * v5.0 (Full Interactive UI): Total omskrivning för ett interaktivt "Context Builder" UI.
# * v6.0 (Stub/Full Logic): Implementerade logik för att skilja på markerade/omarkerade filer.
# * v7.0 (Lazy Loading & UI Polish): Introducerar on-demand fetch för stora .json-filer för att
#   undvika minnesproblem i byggsteget. Lade till en "Kopiera"-knapp för genererad kontext.
#
# TILLÄMPADE REGLER (Frankensteen v3.7):
# - Denna fil följer principen om Single Responsibility: den bygger ett UI.
# - JavaScript-koden är nu asynkron för att hantera on-demand datahämtning (lazy loading).
# - Använder moderna webb-API:er (`fetch`, `Promise.all`, `navigator.clipboard`) för en robust lösning.
# - UI/UX har förbättrats med tydlig feedback på knappar (laddning, kopierat, fel).

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
            --success-color: #28a745;
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
            transition: background-color 0.2s, border-color 0.2s, color 0.2s;
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
        button.primary:hover:not(:disabled) {
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
        <button id="copy-json-btn" disabled>Copy JSON</button>
        <button id="download-json-btn" disabled>Download JSON</button>
    </div>
    <pre id="output-pre">Generated context will appear here.</pre>
</div>

<script>
    document.addEventListener('DOMContentLoaded', () => {
        // --- State ---
        let fullContext = null;
        const REPO_RAW_URL = 'https://raw.githubusercontent.com/Engrove/Engrove-Audio-Tools-2.0/main/';

        // --- DOM Elements ---
        const fileTreeContainer = document.getElementById('file-tree-container');
        const outputPre = document.getElementById('output-pre');
        const selectAllBtn = document.getElementById('select-all-btn');
        const deselectAllBtn = document.getElementById('deselect-all-btn');
        const generateBtn = document.getElementById('generate-context-btn');
        const copyBtn = document.getElementById('copy-json-btn');
        const downloadBtn = document.getElementById('download-json-btn');
        
        // --- Core Functions ---

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
                    toggle.textContent = '►';
                    li.appendChild(toggle);
                    label.appendChild(document.createTextNode(` ${key}`));
                    li.appendChild(label);
                    const nestedUl = renderFileTree(item, li, itemPath);
                    nestedUl.style.display = 'none';
                    li.appendChild(nestedUl);
                } else {
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
        
        async function fetchFileContent(path) {
            try {
                const response = await fetch(`${REPO_RAW_URL}${path}`);
                if (!response.ok) {
                    throw new Error(`HTTP error ${response.status}`);
                }
                // Om det är en JSON-fil, försök att parsa den. Annars, returnera som text.
                if (path.endsWith('.json')) {
                    return await response.json();
                } else {
                    return await response.text();
                }
            } catch (error) {
                console.error(`Failed to fetch content for ${path}:`, error);
                return `// Error: Failed to fetch content for ${path}`;
            }
        }

        async function buildNewContextStructure(sourceNode, selectedPaths) {
            const newNode = {};
            const contentPromises = [];
            const itemsToPopulate = [];

            function traverse(source, dest) {
                for (const key in source) {
                    const item = source[key];
                    if (item.type === 'file') {
                        const isSelected = selectedPaths.has(item.path);
                        const stub = JSON.parse(JSON.stringify(item));
                        
                        if (isSelected && item.content === null) {
                            // On-demand fetch
                            contentPromises.push(fetchFileContent(item.path));
                            itemsToPopulate.push({ a: stub, b: item.path });
                        } else if (!isSelected) {
                            delete stub.content;
                        }
                        dest[key] = stub;
                    } else {
                        // Directory
                        dest[key] = {};
                        traverse(item, dest[key]);
                    }
                }
            }

            traverse(sourceNode, newNode);
            
            const fetchedContents = await Promise.all(contentPromises);

            itemsToPopulate.forEach((item, index) => {
                item.a.content = fetchedContents[index];
            });

            return newNode;
        }

        async function generateSelectedContext() {
            if (!fullContext) return;

            generateBtn.disabled = true;
            generateBtn.textContent = 'Generating...';

            try {
                const selectedPaths = new Set(Array.from(fileTreeContainer.querySelectorAll('input[type="checkbox"]:checked')).map(cb => cb.dataset.path));
                const newContext = {
                    project_overview: fullContext.project_overview,
                    ai_instructions: fullContext.ai_instructions,
                    project_documentation: {},
                    file_structure: {}
                };

                if (fullContext.project_documentation) {
                    for (const docKey in fullContext.project_documentation) {
                        if (selectedPaths.has(`docs/${docKey}`)) {
                            newContext.project_documentation[docKey] = fullContext.project_documentation[docKey];
                        }
                    }
                }
                
                newContext.file_structure = await buildNewContextStructure(fullContext.file_structure, selectedPaths);
                
                outputPre.textContent = JSON.stringify(newContext, null, 2);
                copyBtn.disabled = false;
                downloadBtn.disabled = false;

            } catch (error) {
                outputPre.textContent = `An error occurred during context generation: ${error.message}`;
                console.error(error);
            } finally {
                generateBtn.disabled = false;
                generateBtn.textContent = 'Generate Context';
            }
        }

        // --- Event Listeners ---

        fileTreeContainer.addEventListener('click', (e) => {
            const target = e.target;
            if (target.classList.contains('toggle')) {
                const nestedUl = target.parentElement.querySelector('ul');
                if (nestedUl) {
                    const isCollapsed = nestedUl.style.display === 'none';
                    nestedUl.style.display = isCollapsed ? 'block' : 'none';
                    target.textContent = isCollapsed ? '▼' : '►';
                }
            }
            if (target.type === 'checkbox') {
                const li = target.closest('li');
                if (li) {
                    li.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = target.checked);
                }
            }
        });

        selectAllBtn.addEventListener('click', () => fileTreeContainer.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = true));
        deselectAllBtn.addEventListener('click', () => fileTreeContainer.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false));
        generateBtn.addEventListener('click', generateSelectedContext);

        copyBtn.addEventListener('click', () => {
            navigator.clipboard.writeText(outputPre.textContent).then(() => {
                const originalText = copyBtn.textContent;
                copyBtn.textContent = 'Copied!';
                copyBtn.style.backgroundColor = 'var(--success-color)';
                copyBtn.style.color = 'white';
                setTimeout(() => {
                    copyBtn.textContent = originalText;
                    copyBtn.style.backgroundColor = '';
                    copyBtn.style.color = '';
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy text: ', err);
                copyBtn.textContent = 'Error!';
                copyBtn.style.backgroundColor = 'var(--danger-color)';
                copyBtn.style.color = 'white';
            });
        });

        downloadBtn.addEventListener('click', () => {
            const blob = new Blob([outputPre.textContent], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `context_custom_${new Date().toISOString().slice(0, 10)}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        });
        
        // --- Initialization ---

        fetch('context.json')
            .then(response => { if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`); return response.json(); })
            .then(data => {
                fullContext = data;
                fileTreeContainer.innerHTML = '';
                renderFileTree(fullContext.file_structure, fileTreeContainer, '');
                if (fullContext.project_documentation && Object.keys(fullContext.project_documentation).length > 0) {
                    const docsNode = {};
                    Object.keys(fullContext.project_documentation).forEach(docKey => { docsNode[docKey] = { type: 'file' }; });
                    renderFileTree({ 'docs': docsNode }, fileTreeContainer, '');
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
        print("Användning: python wrap_json_in_html.py <dummy-input.json> <sökväg-till-output.html>", file=sys.stderr)
        sys.exit(1)

    output_file = sys.argv[2]
    
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        
    create_interactive_html(output_file)
