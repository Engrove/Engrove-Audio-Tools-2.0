# scripts/wrap_json_in_html.py
#
# HISTORIK:
# * v1.0 (Initial): Första versionen.
# * v2.0 (Bug Fix): Felaktig implementation med str.format().
# * v3.0 (Definitive Fix): Implementerar html.escape() och <pre>-tagg.
# * v4.0 (UI Enhancement): Lade till kopiera/ladda ner knappar.
# * v5.0 (Full Interactive UI): Total omskrivning för ett interaktivt "Context Builder" UI.
# * v6.0 (Stub/Full Logic): Implementerade logik för att skilja på markerade/omarkerade filer.
# * v7.0 (Lazy Loading & UI Polish): Introducerar on-demand fetch för stora .json-filer.
# * v8.0 (Lazy Loading & UI Polish): Introducerade on-demand fetch och "Kopiera"-knapp.
# * v9.0 (Core Docs Shortcut): Lade till en ny "Select Core Docs"-knapp för att effektivisera startprocessen.
# * v10.0 (Feature Expansion): Implementerat fyra nya huvudfunktioner.
# * v10.1 (Syntax Correction): Korrigerat ett kritiskt syntaxfel (// vs #).
# * v11.0 (Improved Auto-Select): Uppdaterat JSON-driven filmarkering enligt nya krav.
# * v12.0 (Modal Copy/Download): Lade till knappar för kopiering och nedladdning i filförhandsgranskningsmodalen.
# * v12.1 (CRITICAL BUGFIX): Lade till defensiva null-kontroller runt `addEventListener` för att förhindra appkrasch.
# * v13.0 (2025-08-06): Uppdaterad för att hantera den nya modulära instruktionsstrukturen.
# * v13.1 (2025-08-06): (BUGFIX) Korrigerat "Select/Deselect All"-logiken.
# * v14.0 (2025-08-06): (KORRIGERING) All speciallogik i JavaScript för att rendera `docs`-mappen har tagits bort.
#   Filträdet renderas nu enhetligt från `file_structure`-objektet.
# * v15.0 (2025-08-06): Implementerat tre nya funktioner (modalknappar, trädexpansion, Generate Files).
# * v15.1 (2025-08-06): (KORRIGERING) Rättat ett kritiskt logiskt fel i `generateFilesOnly`.
# * v16.0 (2025-08-06): Gjort `AI_Core_Instruction.md` valbar istället för obligatorisk.
#   - Funktionen `enforceCoreInstruction` är borttagen.
#   - Filen är nu en del av `CORE_DOC_PATHS`.
# * v17.0 (2025-08-09): Omarbetat "AI Performance"-fliken till en fullständig instrumentpanel med diagram och tabeller.
# * v17.1 (2025-08-09): KRITISK FIX - Återställde HTML-mallen från en f-sträng till en vanlig sträng.
# * v17.2 (2025-08-09): (DENNA ÄNDRING) KRITISK SYNTAXFIX: Lade till den saknade avslutande `"""` för html_template-variabeln.
#
# TILLÄMPADE REGLER (Frankensteen v4.0):
# - Fullständig kod, alltid: Denna fil är nu komplett och syntaktiskt korrekt.
# - Syntax- och Linter-simulering: Felet som borde ha fångats i detta steg har nu identifierats och åtgärdats.

import sys
import os

def create_interactive_html(output_html_path):
    """
    Genererar en komplett, interaktiv HTML-sida som fungerar som en "AI Context Builder".
    """

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Context Builder v3.4</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --primary-bg: #f8f9fa;
            --secondary-bg: #ffffff;
            --tertiary-bg: #e9ecef;
            --border-color: #dee2e6;
            --text-color: #212529;
            --text-muted: #6c757d;
            --accent-color: #007bff;
            --accent-hover: #0056b3;
            --success-color: #28a745;
            --danger-color: #dc3545;
            --info-color: #17a2b8;
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
            display: flex;
            flex-direction: column;
        }
        #left-panel {
            width: 40%;
            min-width: 350px;
        }
        #right-panel {
            width: 60%;
            gap: 1em;
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
        button:hover { background-color: #e9ecef; }
        button:disabled { background-color: #e9ecef; cursor: not-allowed; opacity: 0.7; }
        button.primary { background-color: var(--accent-color); color: white; border-color: var(--accent-color); }
        button.primary:hover:not(:disabled) { background-color: var(--accent-hover); }
        button.info { background-color: var(--info-color); color: white; border-color: var(--info-color); }
        button.info:hover:not(:disabled) { background-color: #138496; }
        
        #file-tree-container { flex-grow: 1; }
        #file-tree-container ul { list-style-type: none; padding-left: 20px; }
        #file-tree-container li { padding: 3px 0; }
        .toggle { cursor: pointer; user-select: none; display: inline-block; width: 1em; }
        
        .tree-item-label { display: flex; align-items: center; gap: 6px; cursor: pointer; }
        .tree-item-label input[type="checkbox"] { cursor: pointer; }
        .file-icon { width: 1.1em; height: 1.1em; color: var(--text-muted); }
        .file-name-clickable { text-decoration: none; color: var(--text-color); }
        .file-name-clickable:hover { text-decoration: underline; color: var(--accent-color); }
        
        .output-container { display: flex; flex-direction: column; flex-grow: 1; gap: 1em; }
        .output-area, #instruction-input {
            white-space: pre-wrap;
            word-wrap: break-word;
            background-color: var(--secondary-bg);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 1em;
            flex-grow: 1;
            font-family: var(--font-mono);
            font-size: 14px;
            resize: none;
        }
        #instruction-input { flex-grow: 0; height: 150px; resize: vertical; }

        .modal {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0, 0, 0, 0.5); display: flex;
            justify-content: center; align-items: center; z-index: 1000;
            opacity: 0; visibility: hidden; transition: opacity 0.3s, visibility 0.3s;
        }
        .modal.visible { opacity: 1; visibility: visible; }
        .modal-content {
            background: var(--secondary-bg); border-radius: 8px; padding: 20px;
            width: 90%; max-width: 1000px; height: 90%; max-height: 80vh;
            display: flex; flex-direction: column; box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        .modal-header {
            display: flex; justify-content: space-between; align-items: center;
            border-bottom: 1px solid var(--border-color); padding-bottom: 10px; margin-bottom: 15px;
        }
        .modal-header h2 { margin: 0; font-size: 1.2em; font-family: var(--font-mono); }
        .modal-close { font-size: 24px; cursor: pointer; border: none; background: none; }
        .modal-body { flex-grow: 1; overflow-y: auto; }
        .modal-body pre { margin: 0; white-space: pre-wrap; }
        .modal-body img { max-width: 100%; height: auto; display: block; margin: 0 auto; }
    
        /* --- Tabs (Step 3) --- */
        .tabs { display: flex; gap: .5rem; margin-bottom: 1rem; }
        .tab-button { padding: .5rem .75rem; border: 1px solid var(--border-color); background: var(--secondary-bg); border-radius: 6px; cursor: pointer; }
        .tab-button.active { background: var(--accent-color); color: #fff; border-color: var(--accent-color); }
        .tab-panel { display: none; }
        .tab-panel.active { display: flex; flex-direction: column; gap: 1rem; flex-grow: 1; }
        
        /* --- Performance Dashboard Styles --- */
        #performance-container { display: flex; flex-direction: column; gap: 1rem; }
        .metric-block { border: 1px solid var(--border-color); border-radius: 6px; padding: 1rem; background: var(--secondary-bg); }
        .metric-block h3 { margin: 0 0 .75rem 0; font-size: 1.1rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem; }
        .chart-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; }
        .chart-container { position: relative; height: 300px; }
        #perf-learning-body table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
        #perf-learning-body th, #perf-learning-body td { border: 1px solid var(--border-color); padding: 8px; text-align: left; }
        #perf-learning-body th { background-color: var(--primary-bg); }
    </style>
</head>
<body>

<div id="left-panel" class="panel">
    <div class="controls">
        <button id="select-all-btn">Select All</button>
        <button id="deselect-all-btn">Deselect All</button>
        <button id="select-core-docs-btn">Select Core Docs</button>
        <button id="generate-context-btn" class="primary">Generate Context</button>
        <button id="generate-files-btn" class="info">Generate Files</button>
    </div>
    <div id="file-tree-container"><p>Loading context data...</p></div>
</div>

<div id="right-panel" class="panel">
    <div class="tabs">
        <button class="tab-button active" data-tab="context">Context Builder</button>
        <button class="tab-button" data-tab="performance">AI Performance</button>
    </div>
    <div id="tab-context" class="tab-panel active">
        <div class="output-container">
            <textarea id="instruction-input" placeholder="Paste instruction JSON here to auto-select files..."></textarea>
            <div class="output-area" style="display: flex; flex-direction: column;">
                 <div class="controls" style="border-bottom: none; margin-bottom: 0; padding-bottom: 0;">
                    <button id="copy-json-btn" disabled>Copy JSON</button>
                    <button id="download-json-btn" disabled>Download JSON</button>
                </div>
                <pre id="output-pre" style="flex-grow: 1; margin-top: 1em;">Generated context will appear here.</pre>
            </div>
        </div>
    </div>
    <div id="tab-performance" class="tab-panel">
        <div id="performance-container">
             <div class="chart-grid">
                 <div class="metric-block chart-container">
                    <h3>Final Score Over Time</h3>
                    <canvas id="score-chart"></canvas>
                </div>
                <div class="metric-block chart-container">
                    <h3>Session Metrics (Cycles)</h3>
                    <canvas id="metrics-chart"></canvas>
                </div>
                 <div class="metric-block chart-container">
                    <h3>Sessions Per Provider</h3>
                    <canvas id="provider-chart"></canvas>
                </div>
                 <div class="metric-block chart-container">
                    <h3>Sessions Per Model</h3>
                    <canvas id="model-chart"></canvas>
                </div>
            </div>
            <div id="perf-learning" class="metric-block">
                <h3>Learning Database (Heuristics)</h3>
                <div id="perf-learning-body">Ingen data.</div>
            </div>
            <button id="refresh-performance" class="primary">Uppdatera prestandadata</button>
        </div>
    </div>
</div>

<div id="file-preview-modal" class="modal">
    <div class="modal-content">
        <div class="modal-header">
            <h2 id="modal-title">File Preview</h2>
            <div class="modal-actions" style="display: flex; gap: 10px;">
                <button id="modal-copy-btn" disabled>Copy</button>
                <button id="modal-download-btn" disabled>Download</button>
                <button id="modal-close-btn" class="modal-close">×</button>
            </div>
        </div>
        <div id="modal-body" class="modal-body">
            <p>Loading content...</p>
        </div>
    </div>
</div>

<script>
    document.addEventListener('DOMContentLoaded', () => {
        let fullContext = null;
        const REPO_RAW_URL = 'https://raw.githubusercontent.com/Engrove/Engrove-Audio-Tools-2.0/main/';
        
        const CORE_DOC_PATHS = [
          'docs/ai_protocols/AI_Core_Instruction.md',
          'docs/ai_protocols/ai_config.json',
          'docs/ai_protocols/Levande_Kontext_Protokoll.md',
          'docs/ai_protocols/Confidence_Protocol.md',
          'docs/ai_protocols/Multi_Sample_Protokoll.md',
          'docs/ai_protocols/RAG_Faktacheck_Protokoll.md',
          'docs/AI_Collaboration_Standard.md',
          'docs/ai_protocols/Beroendeanalys_Protokoll.md',
          'docs/ai_protocols/Brainstorming_Protokoll.md',
          'docs/ai_protocols/Help_me_God_Protokoll.md',
          'docs/ai_protocols/K-MOD_Protokoll.md',
          'docs/ai_protocols/Kontext-JSON_Protokoll.md',
          'docs/ai_protocols/frankensteen_persona.v1.0.json',
          'docs/ai_protocols/MAS_Architecture_Guide.md',
          'docs/ai_protocols/HITL_Interrupt_Points.md',
          'docs/ai_protocols/Escalation_Protocol.md',
          'docs/ai_protocols/LLM_Judge_Protokoll.md',
          'docs/ai_protocols/Sandbox_Execution_Protokoll.md',
          'docs/ai_protocols/KPI_Dashboard_Spec.md',
          'docs/ai_protocols/AI_Chatt_Avslutningsprotokoll.md',
          'docs/ai_protocols/Manuell_Cache-Berikning_Protokoll.md',
          'docs/ai_protocols/Stalemate_Protocol.md',
          'docs/ai_protocols/Help_me_God_Protokoll.md',
          'docs/ai_protocols/Pre_Execution_Alignment.md',
          'docs/ai_protocols/Structured_Debugging_Checklist.md',
          'docs/ai_protocols/Micro_Retrospective.md',
          'docs/ai_protocols/Autonomy_Charter.md',
          'docs/Mappstruktur_och_Arbetsflöde.md',
          'tools/citation_cache.json',
          'tools/frankensteen_learning_db.json',
          'logs/rotorsakslogg_TEMPLATE.md',
          'docs/Global_UI-Standard_för_Engrove-plattformen.md',
          'docs/Global_UI-Standard_Komponentspecifikation.md',
          'docs/Teknisk_Beskrivning_Engrove_Audio_Toolkit.md',
          'docs/Blueprint_för_Migrering_v1_till_v2.md',
          'docs/Engrove_Audio_Toolkit_v2.0_Analys.md',
          'docs/ai_protocols/Hallucination_Leaderboard_Check.md',
          'docs/ByggLogg.json',
          'package.json',
          'vite.config.js',
          'scripts/process_ai_instructions.py',
          'scripts/generate_full_context.py',
          'scripts/wrap_json_in_html.py'
        ];

        const IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'];
        const ICONS = {
            folder: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M4 6h6l2 2h8v10H4z"></path></svg>',
            file: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" /></svg>',
            js: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M16.22 8l-1.5-1-4.22 10.5 1.5 1 4.22-10.5zm-5.6-3.5c.3-.2.5-.5.5-.8s-.2-.6-.5-.8c-.3-.2-.6-.2-.9 0-.3.2-.5.5-.5.8s.2.6.5.8c.3.2.6.2.9 0zm-3.6 0c.3-.2.5-.5.5-.8s-.2-.6-.5-.8c-.3-.2-.6-.2-.9 0-.3.2-.5.5-.5.8s.2.6.5.8c.3.2.6.2.9 0z"></path></svg>',
            py: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M13 3v5h4V3h-4zm-2 2v3H4V5h7zm-7 5v2h3v3H4v2h7v-2H8v-3h3v5h2v-5h4v5h2V3h-2v3h-2V3h-2v5h-2V3H2v7z"></path></svg>',
            vue: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2L1 12l11 10 11-10L12 2zm0 3.3l7.6 6.7H4.4L12 5.3z"></path></svg>',
            json: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M6 3h2v2H6V3zm0 4h2v2H6V7zm0 4h2v2H6v-2zm0 4h2v2H6v-2zm4-12h8v2h-8V3zm0 4h8v2h-8V7zm0 4h8v2h-8v-2zm0 4h8v2h-8v-2z"></path></svg>',
            md: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M3 3h18v18H3V3zm2 2v14h14V5H5zm2 2h2v10H7V7zm3 0h2v10h-2V7zm3 0h2l2 3 2-3h2v10h-2V9l-2 3-2-3v8h-2V7z"></path></svg>',
            css: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M4 3h16v2H4V3zm0 4h16v2H4V7zm0 4h5v2H4v-2zm0 4h5v2H4v-2zm7-8h9v2h-9v-2zm0 4h9v2h-9v-2z"></path></svg>',
            html: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M4 3h16v18H4V3zm2 2v14h12V5H6zm2 2l3 3-3 3v-2H8V9h2v2zm5 0h4v2h-4V9zm0 4h4v2h-4v-2z"></path></svg>',
            yml: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M4 5h16v2H4zm0 6h16v2H4zm0 6h16v2H4z"></path></svg>',
            image: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"></path></svg>',
        };
        const fileTreeContainer = document.getElementById('file-tree-container');
        const outputPre = document.getElementById('output-pre');
        const instructionInput = document.getElementById('instruction-input');
        const selectAllBtn = document.getElementById('select-all-btn');
        const deselectAllBtn = document.getElementById('deselect-all-btn');
        const selectCoreDocsBtn = document.getElementById('select-core-docs-btn');
        const generateBtn = document.getElementById('generate-context-btn');
        const generateFilesBtn = document.getElementById('generate-files-btn');
        const copyBtn = document.getElementById('copy-json-btn');
        const downloadBtn = document.getElementById('download-json-btn');
        const modal = document.getElementById('file-preview-modal');
        const modalTitle = document.getElementById('modal-title');
        const modalBody = document.getElementById('modal-body');
        const modalCloseBtn = document.getElementById('modal-close-btn');
        const modalCopyBtn = document.getElementById('modal-copy-btn');
        const modalDownloadBtn = document.getElementById('modal-download-btn');
        let currentFileContent = '';
        let currentFilePath = '';
        let currentFileIsBinary = false;

        function getIcon(name, isFolder) {
            if (isFolder) return ICONS.folder;
            const extension = name.split('.').pop().toLowerCase();
            if (IMAGE_EXTENSIONS.includes(extension)) return ICONS.image;
            return ICONS[extension] || ICONS.file;
        }

        function renderFileTree(node, parentElement, currentPath) {
            const ul = document.createElement('ul');
            const sortedKeys = Object.keys(node).sort((a, b) => {
                const aIsFile = node[a].type === 'file';
                const bIsFile = node[b].type === 'file';
                if (aIsFile && !bIsFile) return 1;
                if (!aIsFile && bIsFile) return -1;
                return a.localeCompare(b);
            });

            sortedKeys.forEach(key => {
                const item = node[key];
                const itemPath = currentPath ? `${currentPath}/${key}` : key;
                const li = document.createElement('li');
                const isFolder = item.type !== 'file';
                
                const label = document.createElement('label');
                label.className = 'tree-item-label';

                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.setAttribute('data-path', itemPath);
                label.appendChild(checkbox);

                const iconSpan = document.createElement('span');
                iconSpan.className = 'file-icon';
                iconSpan.innerHTML = getIcon(key, isFolder);
                label.appendChild(iconSpan);
                
                if (isFolder) {
                    li.classList.add('folder');
                    const toggle = document.createElement('span');
                    toggle.className = 'toggle';
                    toggle.textContent = '►';
                    li.appendChild(toggle);

                    const folderNameSpan = document.createElement('span');
                    folderNameSpan.textContent = ` ${key}`;
                    label.appendChild(folderNameSpan);
                    li.appendChild(label);

                    const nestedUl = renderFileTree(item, li, itemPath);
                    nestedUl.style.display = 'none';
                    li.appendChild(nestedUl);
                } else {
                    li.classList.add('file');
                    const fileNameSpan = document.createElement('a');
                    fileNameSpan.className = 'file-name-clickable';
                    fileNameSpan.href = '#';
                    fileNameSpan.textContent = ` ${key}`;
                    fileNameSpan.setAttribute('data-path', itemPath);
                    label.appendChild(fileNameSpan);
                    li.appendChild(label);
                }
                ul.appendChild(li);
            });
            parentElement.appendChild(ul);
            return ul;
        }

        function expandToNode(element) {
            let parent = element.parentElement.closest('li.folder');
            while(parent) {
                const nestedUl = parent.querySelector('ul');
                const toggle = parent.querySelector('.toggle');
                if (nestedUl && toggle) {
                    nestedUl.style.display = 'block';
                    toggle.textContent = '▼';
                }
                parent = parent.parentElement.closest('li.folder');
            }
        }

        function selectCoreDocs() {
            fileTreeContainer.querySelectorAll('input[type="checkbox"]:not(:disabled)').forEach(cb => cb.checked = false);
            CORE_DOC_PATHS.forEach(path => {
                const checkbox = fileTreeContainer.querySelector(`input[data-path="${path}"]`);
                if (checkbox && !checkbox.disabled) {
                    checkbox.checked = true;
                    expandToNode(checkbox);
                }
            });
        }
        
        async function openFilePreview(path) {
            modalTitle.textContent = path;
            modalBody.innerHTML = '<p>Loading content...</p>';
            modal.classList.add('visible');
            modalCopyBtn.disabled = true;
            modalDownloadBtn.disabled = true;
            currentFileContent = '';
            currentFilePath = path;
            currentFileIsBinary = false;
            
            try {
                const url = `${REPO_RAW_URL}${path}`;
                const extension = path.split('.').pop().toLowerCase();
                
                if (IMAGE_EXTENSIONS.includes(extension)) {
                    currentFileIsBinary = true;
                    modalBody.innerHTML = `<img src="${url}" alt="Preview of ${path}">`;
                    const response = await fetch(url);
                    if (!response.ok) throw new Error(`HTTP error ${response.status}`);
                    currentFileContent = await response.blob();
                    modalCopyBtn.disabled = true;
                    modalDownloadBtn.disabled = false;
                } else {
                    currentFileIsBinary = false;
                    const response = await fetch(url);
                    if (!response.ok) throw new Error(`HTTP error ${response.status}`);
                    const textContent = await response.text();
                    currentFileContent = textContent;
                    const pre = document.createElement('pre');
                    const code = document.createElement('code');
                    code.textContent = textContent;
                    pre.appendChild(code);
                    modalBody.innerHTML = '';
                    modalBody.appendChild(pre);
                    modalCopyBtn.disabled = false;
                    modalDownloadBtn.disabled = false;
                }
            } catch (error) {
                console.error(`Failed to fetch content for ${path}:`, error);
                modalBody.textContent = `Error: Failed to fetch content for ${path}. ${error.message}`;
            }
        }

        async function fetchFileContent(path) {
            try {
                const response = await fetch(`${REPO_RAW_URL}${path}`);
                if (!response.ok) throw new Error(`HTTP error ${response.status}`);
                return await response.text();
            } catch (error) {
                console.error(`Failed to fetch content for ${path}:`, error);
                return `// Error: Failed to fetch content for ${path}`;
            }
        }

        async function buildNewContextStructure(sourceNode, selectedPaths) {
            const newNode = {};
            const promises = [];

            function traverse(source, dest, currentPath = '') {
                const sortedKeys = Object.keys(source).sort();
                for (const key of sortedKeys) {
                    const item = source[key];
                    const itemPath = currentPath ? `${currentPath}/${key}` : key;
                    if (item.type === 'file') {
                        const isSelected = selectedPaths.has(item.path);
                        const stub = { ...item };
                        if (isSelected && (item.is_binary || item.content === null)) {
                            promises.push(
                                fetchFileContent(item.path).then(content => {
                                    stub.content = content;
                                })
                            );
                        } else if (!isSelected) {
                            delete stub.content;
                        }
                        dest[key] = stub;
                    } else {
                        dest[key] = {};
                        traverse(item, dest[key], itemPath);
                    }
                }
            }

            traverse(sourceNode, newNode);
            await Promise.all(promises);
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
                    file_structure: {}
                };
                if (instructionInput.value.trim()) {
                    newContext.ai_instructions_input = instructionInput.value.trim();
                }
                newContext.file_structure = await buildNewContextStructure(fullContext.file_structure, selectedPaths);
                outputPre.textContent = JSON.stringify(newContext, null, 2);
                copyBtn.disabled = false;
                downloadBtn.disabled = false;
            } catch (error) {
                outputPre.textContent = `An error occurred during context generation: ${error.message}`;
            } finally {
                generateBtn.disabled = false;
                generateBtn.textContent = 'Generate Context';
            }
        }

        async function generateFilesOnly() {
            if (!fullContext) return;
            generateFilesBtn.disabled = true;
            generateFilesBtn.textContent = 'Generating...';
            try {
                let output = {};
                const instructionText = instructionInput.value.trim();

                if (instructionText) {
                    try {
                        output = { ...JSON.parse(instructionText) };
                    } catch (e) {
                        output.user_instruction = instructionText;
                    }
                }

                const selectedPaths = new Set(Array.from(fileTreeContainer.querySelectorAll('input[type="checkbox"]:checked')).map(cb => cb.dataset.path));
                const filesContent = {};

                const populatedStructure = await buildNewContextStructure(fullContext.file_structure, selectedPaths);
                
                function extractFiles(node) {
                    for (const key in node) {
                        const item = node[key];
                        if (item.type === 'file') {
                            if (item.content !== undefined) {
                                filesContent[item.path] = item.content;
                            }
                        } else {
                            extractFiles(item);
                        }
                    }
                }

                extractFiles(populatedStructure);
                output.files = filesContent;

                outputPre.textContent = JSON.stringify(output, null, 2);
                copyBtn.disabled = false;
                downloadBtn.disabled = false;

            } catch (error) {
                outputPre.textContent = `An error occurred during file generation: ${error.message}`;
            } finally {
                generateFilesBtn.disabled = false;
                generateFilesBtn.textContent = 'Generate Files';
            }
        }
        
        function handleInstructionInput() {
            const text = instructionInput.value;
            if (!text.trim()) return;
            try {
                const parsed = JSON.parse(text);
                if (parsed && Array.isArray(parsed.filesToSelect)) {
                    const allCheckboxes = Array.from(fileTreeContainer.querySelectorAll('input[type="checkbox"]'));
                    parsed.filesToSelect.forEach(pathInJson => {
                        const checkbox = allCheckboxes.find(cb => cb.dataset.path === pathInJson);
                        if (checkbox) {
                           checkbox.checked = true;
                           expandToNode(checkbox);
                        }
                    });
                }
            } catch (e) { /* Ignore parse errors */ }
        }

        fileTreeContainer.addEventListener('click', (e) => {
            const target = e.target;
            const clickableFile = target.closest('.file-name-clickable');
            if (clickableFile) {
                e.preventDefault();
                openFilePreview(clickableFile.dataset.path);
                return;
            }
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
                    li.querySelectorAll('input[type="checkbox"]').forEach(cb => {
                        if (!cb.disabled) cb.checked = target.checked;
                    });
                }
            }
        });

        selectAllBtn.addEventListener('click', () => fileTreeContainer.querySelectorAll('input[type="checkbox"]:not(:disabled)').forEach(cb => cb.checked = true));
        deselectAllBtn.addEventListener('click', () => fileTreeContainer.querySelectorAll('input[type="checkbox"]:not(:disabled)').forEach(cb => cb.checked = false));
        selectCoreDocsBtn.addEventListener('click', selectCoreDocs);
        generateBtn.addEventListener('click', generateSelectedContext);
        generateFilesBtn.addEventListener('click', generateFilesOnly);
        instructionInput.addEventListener('input', handleInstructionInput);

        const closeModal = () => modal.classList.remove('visible');
        if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeModal);
        if (modal) modal.addEventListener('click', (e) => { if (e.target === modal) closeModal(); });
        document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && modal.classList.contains('visible')) closeModal(); });

        function showButtonFeedback(button, text, color) {
            const originalText = button.textContent;
            button.textContent = text;
            button.style.backgroundColor = `var(--${color}-color)`;
            button.style.color = 'white';
            setTimeout(() => { 
                button.textContent = originalText; 
                button.style.backgroundColor = ''; 
                button.style.color = '';
            }, 2000);
        }

        if (copyBtn) copyBtn.addEventListener('click', () => {
            navigator.clipboard.writeText(outputPre.textContent)
                .then(() => showButtonFeedback(copyBtn, 'Copied!', 'success'))
                .catch(() => showButtonFeedback(copyBtn, 'Error!', 'danger'));
        });

        if (modalCopyBtn) modalCopyBtn.addEventListener('click', () => {
             if (!currentFileIsBinary && currentFileContent) {
                navigator.clipboard.writeText(currentFileContent)
                    .then(() => showButtonFeedback(modalCopyBtn, 'Copied!', 'success'))
                    .catch(() => showButtonFeedback(modalCopyBtn, 'Error!', 'danger'));
             }
        });
        
        if (modalDownloadBtn) modalDownloadBtn.addEventListener('click', () => {
            if (!currentFileContent) return;
            const blob = currentFileIsBinary ? currentFileContent : new Blob([currentFileContent], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = currentFilePath.split('/').pop() || 'download';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        });

        if (downloadBtn) downloadBtn.addEventListener('click', () => {
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
        
        fetch('context.json')
            .then(response => { if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`); return response.json(); })
            .then(data => {
                fullContext = data;
                fileTreeContainer.innerHTML = '';
                renderFileTree(fullContext.file_structure, fileTreeContainer, '');
            })
            .catch(error => {
                fileTreeContainer.innerHTML = `<p style="color: var(--danger-color);"><b>Error:</b> Could not load context.json. ${error.message}</p>`;
            });
    });

    // --- Tabs & Performance Dashboard Logic ---
    const charts = {}; // Global object to hold chart instances

    document.querySelectorAll('.tab-button').forEach(btn => {
      btn.addEventListener('click', () => {
        const tab = btn.getAttribute('data-tab');
        document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
        document.getElementById(`tab-${tab}`).classList.add('active');
        if (tab === 'performance') {
            renderPerformanceDashboard();
        }
      });
    });

    async function refreshPerformanceData() {
        try {
            const res = await fetch('context.json', { cache: 'no-store' });
            if (!res.ok) throw new Error(`status ${res.status}`);
            const data = await res.json();
            if (data && data.ai_performance_metrics) {
                 fullContext.ai_performance_metrics = data.ai_performance_metrics;
                 renderPerformanceDashboard();
            }
        } catch (e) {
            console.error('Kunde inte läsa om context.json:', e);
        }
    }
    
    document.addEventListener('click', (e) => {
        if (e.target && e.target.id === 'refresh-performance') {
            refreshPerformanceData();
        }
    });

    function aggregateModelStats(items) {
      const byProvider = {};
      const byModel = {};
      const visit = (obj) => {
        if (obj && typeof obj === 'object') {
          if (obj.model && typeof obj.model === 'object') {
            const prov = obj.model.provider || 'unknown';
            const name = obj.model.name || 'unknown';
            byProvider[prov] = (byProvider[prov] || 0) + 1;
            const key = `${prov}:${name}`;
            byModel[key] = (byModel[key] || 0) + 1;
          } else if (obj.generatedBy && obj.generatedBy.model) {
             const prov = obj.generatedBy.model.provider || 'unknown';
             const name = obj.generatedBy.model.name || 'unknown';
             byProvider[prov] = (byProvider[prov] || 0) + 1;
             const key = `${prov}:${name}`;
             byModel[key] = (byModel[key] || 0) + 1;
          }
          for (const k in obj) {
            const v = obj[k];
            if (Array.isArray(v)) v.forEach(visit);
            else if (v && typeof v === 'object') visit(v);
          }
        }
      };
      (items || []).forEach(visit);
      return { byProvider, byModel };
    }
    
    function renderLearningDbTable(targetEl, data) {
        if (!data || data.length === 0) {
            targetEl.innerHTML = 'Ingen data.';
            return;
        }
        const table = document.createElement('table');
        table.innerHTML = `
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Risk</th>
                    <th>Mitigation</th>
                    <th>Trigger Keywords</th>
                </tr>
            </thead>
            <tbody>
                ${data.map(item => `
                    <tr>
                        <td>${item.heuristicId || 'N/A'}</td>
                        <td>${(item.identifiedRisk && item.identifiedRisk.description) || 'N/A'}</td>
                        <td>${(item.mitigation && item.mitigation.description) || 'N/A'}</td>
                        <td>${(item.trigger && item.trigger.keywords || []).join(', ')}</td>
                    </tr>
                `).join('')}
            </tbody>
        `;
        targetEl.innerHTML = '';
        targetEl.appendChild(table);
    }
    
    function renderPerformanceDashboard() {
        if (!fullContext) return;
        const metrics = fullContext.ai_performance_metrics || {};
        const perfLog = Array.isArray(metrics.performanceLog) ? metrics.performanceLog : [];
        const learningDb = Array.isArray(metrics.learningDatabase) ? metrics.learningDatabase : [];

        // Destroy old charts before redrawing
        Object.values(charts).forEach(chart => {
            if(chart && typeof chart.destroy === 'function') {
                chart.destroy();
            }
        });

        if (perfLog.length === 0) {
            const learningBody = document.getElementById('perf-learning-body');
            if(learningBody) learningBody.innerHTML = 'Ingen prestandadata tillgänglig för att rendera diagram.';
            return;
        }

        // --- Data Processing ---
        const labels = perfLog.map(p => `Session ${p.sessionId}`);
        const finalScores = perfLog.map(p => p.scorecard ? p.scorecard.finalScore : 0);
        const debuggingCycles = perfLog.map(p => p.detailedMetrics ? p.detailedMetrics.debuggingCycles : 0);
        const selfCorrections = perfLog.map(p => p.detailedMetrics ? p.detailedMetrics.selfCorrections : 0);
        const externalCorrections = perfLog.map(p => p.detailedMetrics ? p.detailedMetrics.externalCorrections : 0);

        const { byProvider, byModel } = aggregateModelStats(perfLog);

        // --- Chart 1: Final Score Line Chart ---
        const scoreCtx = document.getElementById('score-chart').getContext('2d');
        charts.scoreChart = new Chart(scoreCtx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Final Score',
                    data: finalScores,
                    borderColor: 'var(--accent-color)',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    fill: true,
                    tension: 0.1
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });

        // --- Chart 2: Session Metrics Bar Chart ---
        const metricsCtx = document.getElementById('metrics-chart').getContext('2d');
        charts.metricsChart = new Chart(metricsCtx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    { label: 'Debugging Cycles', data: debuggingCycles, backgroundColor: 'rgba(220, 53, 69, 0.7)' },
                    { label: 'Self Corrections', data: selfCorrections, backgroundColor: 'rgba(255, 193, 7, 0.7)' },
                    { label: 'External Corrections', data: externalCorrections, backgroundColor: 'rgba(23, 162, 184, 0.7)' },
                ]
            },
            options: { responsive: true, maintainAspectRatio: false, scales: { x: { stacked: true }, y: { stacked: true, beginAtZero: true } } }
        });

        // --- Chart 3: Provider Pie Chart ---
        const providerCtx = document.getElementById('provider-chart').getContext('2d');
        charts.providerChart = new Chart(providerCtx, {
            type: 'pie',
            data: {
                labels: Object.keys(byProvider),
                datasets: [{ data: Object.values(byProvider) }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
        
        // --- Chart 4: Model Pie Chart ---
        const modelCtx = document.getElementById('model-chart').getContext('2d');
        charts.modelChart = new Chart(modelCtx, {
            type: 'pie',
            data: {
                labels: Object.keys(byModel),
                datasets: [{ data: Object.values(byModel) }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
        
        // --- Table: Learning DB ---
        const learningBody = document.getElementById('perf-learning-body');
        if (learningBody) {
             renderLearningDbTable(learningBody, learningDb);
        }
    }
</script>

</body></html>"""

    try:
        with open(output_html_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
        print(f"[INFO] Wrapper: Skapade framgångsrikt den uppdaterade interaktiva HTML-filen '{output_html_path}'.")

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
