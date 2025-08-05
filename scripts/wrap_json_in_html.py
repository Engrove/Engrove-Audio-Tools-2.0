# scripts/wrap_json_in_html.py
#
# HISTORIK:
# * v1.0 - v4.0: Tidigare versioner för att visa statisk JSON.
# * v5.0 (Context Builder): Total omarbetning. Genererar en interaktiv, fristående
#   webbapplikation för att bygga anpassade AI-kontexter.
#   - Implementerar den av "Help me God"-tribunalen godkända arkitekturen.
#   - Frikopplar UI från data genom att asynkront hämta `context.json`.
#   - Renderar en dynamisk, interaktiv fil-trädvy med checkboxar.
#   - Bygger ett nytt, anpassat JSON-objekt baserat på användarens val.
#
# TILLÄMPADE REGLER (Frankensteen v3.7):
# - Denna fil följer principen om Single Responsibility (dess enda ansvar är att
#   bygga en specifik HTML-artefakt).
# - Robust felhantering.
# - Inbäddad JS är strukturerad och kommenterad för maximal läsbarhet.

import sys
import html

def generate_builder_html(output_html_path):
    """
    Genererar en komplett, fristående HTML-fil som fungerar som ett interaktivt
    "Context Builder"-verktyg. Sidan hämtar `context.json` asynkront.
    """
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Context Builder</title>
    <style>
        :root {{
            --bg-color: #1e1e1e;
            --text-color: #e0e0e0;
            --primary-color: #58a6ff;
            --border-color: #3c3c3c;
            --surface-color: #2a2a2a;
            --surface-hover: #3c3c3c;
            --font-main: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            --font-mono: "JetBrains Mono", "SF Mono", "Consolas", "Liberation Mono", "Menlo", monospace;
        }}
        body {{
            margin: 0;
            font-family: var(--font-main);
            background-color: var(--bg-color);
            color: var(--text-color);
            display: flex;
            height: 100vh;
            overflow: hidden;
        }}
        .sidebar {{
            width: 40%;
            min-width: 300px;
            max-width: 600px;
            display: flex;
            flex-direction: column;
            border-right: 1px solid var(--border-color);
        }}
        .main-content {{
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }}
        .controls, .output-controls {{
            padding: 12px;
            background-color: var(--surface-color);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            flex-shrink: 0;
        }}
        button {{
            font-size: 14px;
            padding: 8px 16px;
            border-radius: 6px;
            border: 1px solid var(--border-color);
            cursor: pointer;
            background-color: var(--surface-hover);
            color: var(--text-color);
            transition: background-color 0.2s;
        }}
        button:hover {{ background-color: #4a4a4a; }}
        button:active {{ background-color: #5a5a5a; }}
        button.primary {{
            background-color: var(--primary-color);
            color: var(--bg-color);
            font-weight: bold;
        }}
        button.primary:hover {{ background-color: #82baff; }}
        #file-tree-container {{
            overflow-y: auto;
            flex-grow: 1;
            padding: 10px;
        }}
        #file-tree ul {{
            list-style: none;
            padding-left: 20px;
            margin: 0;
        }}
        #file-tree li {{ margin: 4px 0; }}
        #file-tree label {{
            cursor: pointer;
            display: flex;
            align-items: center;
        }}
        #file-tree label:hover {{ background-color: rgba(255, 255, 255, 0.05); }}
        .folder-toggle {{
            cursor: pointer;
            margin-right: 5px;
            width: 1em;
            display: inline-block;
        }}
        .file-icon {{ margin-right: 5px; width: 1em; display: inline-block; opacity: 0.6; }}
        #output-container {{
            flex-grow: 1;
            position: relative;
        }}
        #output-pre {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            margin: 0;
            padding: 1em;
            font-family: var(--font-mono);
            white-space: pre-wrap;
            word-wrap: break-word;
            background-color: var(--bg-color);
            overflow-y: auto;
            border: none;
            color: var(--text-color);
        }}
        .status {{ padding: 10px; font-style: italic; color: #aaa; }}
        .hidden {{ display: none; }}
    </style>
</head>
<body>

<aside class="sidebar">
    <div class="controls">
        <button id="select-all-btn">Select All</button>
        <button id="deselect-all-btn">Deselect All</button>
        <button id="generate-btn" class="primary">Generate Context</button>
    </div>
    <div id="file-tree-container">
        <div id="status" class="status">Loading context.json...</div>
        <div id="file-tree" class="hidden"></div>
    </div>
</aside>

<main class="main-content">
    <div class="output-controls">
        <button id="copy-btn">Copy to Clipboard</button>
    </div>
    <div id="output-container">
        <pre id="output-pre">Generated context will appear here...</pre>
    </div>
</main>

<script>
    document.addEventListener('DOMContentLoaded', () => {{
        // Global state
        let fullContext = null;

        // DOM elements
        const statusEl = document.getElementById('status');
        const fileTreeContainer = document.getElementById('file-tree');
        const outputPre = document.getElementById('output-pre');
        
        // --- 1. Data Fetching ---
        async function fetchContext() {{
            try {{
                const response = await fetch('context.json');
                if (!response.ok) {{
                    throw new Error(`HTTP error! status: ${{response.status}}`);
                }}
                fullContext = await response.json();
                statusEl.classList.add('hidden');
                fileTreeContainer.classList.remove('hidden');
                renderFileTree();
            }} catch (e) {{
                statusEl.textContent = `Failed to load context.json: ${{e.message}}`;
                statusEl.style.color = '#ff8a8a';
            }}
        }}

        // --- 2. UI Rendering ---
        function renderFileTree() {{
            const treeRoot = document.createElement('ul');
            
            // First, add docs
            const docsNode = createNode('project_documentation', fullContext.project_documentation, 'docs');
            treeRoot.appendChild(docsNode);

            // Then, add file structure
            const filesNode = createNode('file_structure', fullContext.file_structure, 'files');
            treeRoot.appendChild(filesNode);
            
            fileTreeContainer.innerHTML = '';
            fileTreeContainer.appendChild(treeRoot);
        }}
        
        function createNode(rootKey, obj, displayName) {{
            const li = document.createElement('li');
            const isRootFolder = true;

            const label = document.createElement('label');
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.dataset.path = rootKey;
            
            const toggle = document.createElement('span');
            toggle.className = 'folder-toggle';
            toggle.textContent = '▼';
            
            const name = document.createElement('span');
            name.textContent = displayName;
            
            label.appendChild(checkbox);
            label.appendChild(toggle);
            label.appendChild(name);
            li.appendChild(label);

            const childrenUl = document.createElement('ul');
            for (const key in obj) {{
                const path = `${{rootKey}}.${{key}}`;
                childrenUl.appendChild(createTreeElement(key, obj[key], path));
            }}
            li.appendChild(childrenUl);
            
            toggle.addEventListener('click', (e) => {{
                e.stopPropagation();
                childrenUl.classList.toggle('hidden');
                toggle.textContent = childrenUl.classList.contains('hidden') ? '►' : '▼';
            }});

            checkbox.addEventListener('change', (e) => {{
                childrenUl.querySelectorAll('input[type="checkbox"]').forEach(child => {{
                    child.checked = e.target.checked;
                }});
            }});

            return li;
        }}

        function createTreeElement(name, node, path) {{
            const li = document.createElement('li');
            const label = document.createElement('label');
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.dataset.path = path;
            
            label.appendChild(checkbox);

            if (node.type === 'file') {{
                const icon = document.createElement('span');
                icon.className = 'file-icon';
                icon.textContent = '📄';
                label.appendChild(icon);
            }} else {{ // It's a folder (nested object)
                const toggle = document.createElement('span');
                toggle.className = 'folder-toggle';
                toggle.textContent = '►'; // Start collapsed
                label.appendChild(toggle);

                const childrenUl = document.createElement('ul');
                childrenUl.classList.add('hidden'); // Start collapsed
                for (const key in node) {{
                    childrenUl.appendChild(createTreeElement(key, node[key], `${{path}}.${{key}}`));
                }}
                li.appendChild(childrenUl);

                toggle.addEventListener('click', (e) => {{
                    e.stopPropagation();
                    childrenUl.classList.toggle('hidden');
                    toggle.textContent = childrenUl.classList.contains('hidden') ? '►' : '▼';
                }});
                
                checkbox.addEventListener('change', (e) => {{
                    childrenUl.querySelectorAll('input[type="checkbox"]').forEach(child => {{
                        child.checked = e.target.checked;
                    }});
                }});
            }}
            
            const nameSpan = document.createElement('span');
            nameSpan.textContent = name;
            label.appendChild(nameSpan);
            li.appendChild(label);

            return li;
        }}
        
        // --- 3. Context Generation Logic ---
        function generateSelectedContext() {{
            if (!fullContext) {{
                outputPre.textContent = 'Error: Full context not loaded.';
                return;
            }}

            const selectedPaths = Array.from(fileTreeContainer.querySelectorAll('input[type="checkbox"]:checked'))
                .map(cb => cb.dataset.path);

            const newContext = {{
                project_overview: fullContext.project_overview,
                ai_instructions: fullContext.ai_instructions,
                project_documentation: {{}},
                file_structure: {{}}
            }};

            for (const path of selectedPaths) {{
                const parts = path.split('.');
                const rootKey = parts[0];
                
                if (rootKey === 'project_documentation' && parts.length > 1) {{
                    const docKey = parts[1];
                    if (fullContext.project_documentation[docKey]) {{
                       newContext.project_documentation[docKey] = fullContext.project_documentation[docKey];
                    }}
                }}

                if (rootKey === 'file_structure' && parts.length > 1) {{
                    const filePathParts = parts.slice(1);
                    let sourcePointer = fullContext.file_structure;
                    let destPointer = newContext.file_structure;

                    for (let i = 0; i < filePathParts.length; i++) {{
                        const part = filePathParts[i];
                        if (!sourcePointer[part]) break; // Path is invalid, skip

                        if (i === filePathParts.length - 1) {{ // It's the file/end node
                            destPointer[part] = sourcePointer[part];
                        }} else {{
                            if (!destPointer[part]) {{
                                destPointer[part] = {{}};
                            }}
                            destPointer = destPointer[part];
                            sourcePointer = sourcePointer[part];
                        }}
                    }}
                }}
            }}
            
            outputPre.textContent = JSON.stringify(newContext, null, 2);
        }}

        // --- 4. Event Listeners ---
        document.getElementById('generate-btn').addEventListener('click', generateSelectedContext);
        
        document.getElementById('select-all-btn').addEventListener('click', () => {{
            fileTreeContainer.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = true);
        }});
        
        document.getElementById('deselect-all-btn').addEventListener('click', () => {{
            fileTreeContainer.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);
        }});
        
        document.getElementById('copy-btn').addEventListener('click', function() {{
            const button = this;
            navigator.clipboard.writeText(outputPre.textContent).then(() => {{
                button.textContent = 'Copied!';
                setTimeout(() => {{ button.textContent = 'Copy to Clipboard'; }}, 2000);
            }}, (err) => {{
                button.textContent = 'Failed!';
                console.error('Copy failed', err);
                setTimeout(() => {{ button.textContent = 'Copy to Clipboard'; }}, 2000);
            }});
        }});

        // --- 5. Initialisation ---
        fetchContext();
    }});
</script>
</body>
</html>"""
    try:
        with open(output_html_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
        print(f"[INFO] Builder: Skapade framgångsrikt '{output_html_path}'.")

    except Exception as e:
        print(f"[ERROR] Builder: Ett oväntat fel inträffade vid skrivning till fil: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Användning: python wrap_json_in_html.py <sökväg-till-input.json> <sökväg-till-output.html>", file=sys.stderr)
        print("Notera: Indata-JSON ignoreras i denna version men argumentet krävs för pipeline-kompatibilitet.", file=sys.stderr)
        sys.exit(1)

    output_file = sys.argv[2]
    generate_builder_html(output_file)
