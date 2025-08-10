#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wrap_json_in_html.py

AI Context Builder – komplett:
- Laddar context.json och renderar filträd + förhandsvisning.
- Två knappar: “Skapa nästa arbete” (Discovery/K-MOD), “Skapa uppgift” (Implementation).
- Discovery-prompt innehåller HÅRDA REGLER + CANDIDATE_PATHS (repo-filindex).
- Validerar inklistrad Discovery-JSON (endast kända paths, korrekta mängdrelationer).
- Provider-bootstrap för ChatGPT 5 / Gemini 2.5 Pro.
- Global obligatorisk regel: ALDRIG generera bilder utan uttrycklig begäran.
- Val “Bädda in fulltext” för att bära kontext in i en helt tom chatsession.
- Hjälpmodal som beskriver rätt arbetssekvens.
"""

import sys
import os

def create_interactive_html(output_html_path):
    html_template = r"""<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="UTF-8">
<title>AI Context Builder v4.1</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
:root{
  --primary-bg:#f8f9fa; --secondary-bg:#ffffff; --tertiary-bg:#e9ecef;
  --border-color:#dee2e6; --text-color:#212529; --text-muted:#6c757d;
  --accent-color:#007bff; --accent-hover:#0056b3;
  --success-color:#28a745; --danger-color:#dc3545; --info-color:#17a2b8;
  --font-main:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --font-mono:ui-monospace,"JetBrains Mono","SF Mono","Consolas","Liberation Mono","Menlo",monospace;
}
*{box-sizing:border-box}
body{font-family:var(--font-main);background:var(--primary-bg);color:var(--text-color);margin:0;display:flex;height:100vh;overflow:hidden}
.panel{padding:1em;overflow-y:auto;border-right:1px solid var(--border-color);display:flex;flex-direction:column}
#left-panel{width:40%;min-width:350px}
#right-panel{width:60%;gap:1em}

.controls{padding-bottom:1em;margin-bottom:1em;border-bottom:1px solid var(--border-color);display:flex;gap:10px;flex-wrap:wrap;align-items:center}
button{font-size:14px;padding:8px 16px;border-radius:6px;border:1px solid var(--border-color);cursor:pointer;background:var(--secondary-bg);color:var(--text-color);transition:.2s}
button:hover{background:#e9ecef}
button:disabled{background:#e9ecef;cursor:not-allowed;opacity:.7}
button.primary{background:var(--accent-color);color:#fff;border-color:var(--accent-color)}
button.primary:hover:not(:disabled){background:var(--accent-hover)}
button.info{background:var(--info-color);color:#fff;border-color:var(--info-color)}
button.info:hover:not(:disabled){background:#138496}
label.inline{display:inline-flex;align-items:center;gap:6px}

#file-tree-container{flex-grow:1}
#file-tree-container ul{list-style:none;padding-left:20px}
#file-tree-container li{padding:3px 0}
.toggle{cursor:pointer;user-select:none;display:inline-block;width:1em}
.tree-item-label{display:flex;align-items:center;gap:6px;cursor:pointer}
.tree-item-label input[type="checkbox"]{cursor:pointer}
.file-icon{width:1.1em;height:1.1em;color:var(--text-muted)}
.file-name-clickable{text-decoration:none;color:var(--text-color)}
.file-name-clickable:hover{text-decoration:underline;color:var(--accent-color)}

.output-container{display:flex;flex-direction:column;flex-grow:1;gap:1em}
.output-area, #instruction-input{
  white-space:pre-wrap;word-wrap:break-word;background:var(--secondary-bg);
  border:1px solid var(--border-color);border-radius:6px;padding:1em;flex-grow:1;
  font-family:var(--font-mono);font-size:14px;resize:none
}
#instruction-input{flex-grow:0;height:150px;resize:vertical}

.banner{display:none;padding:.6em .8em;border:1px solid var(--border-color);border-radius:6px}
.banner.ok{display:block;background:#eaf7ef;color:#114d27}
.banner.warn{display:block;background:#fff8e1;color:#5c4600}
.banner.err{display:block;background:#fde7ea;color:#7a0e1a}

.modal{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.5);display:flex;justify-content:center;align-items:center;z-index:1000;opacity:0;visibility:hidden;transition:.3s}
.modal.visible{opacity:1;visibility:visible}
.modal-content{background:var(--secondary-bg);border-radius:8px;padding:20px;width:90%;max-width:1000px;height:90%;max-height:80vh;display:flex;flex-direction:column;box-shadow:0 5px 15px rgba(0,0,0,.3)}
.modal-header{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--border-color);padding-bottom:10px;margin-bottom:15px}
.modal-header h2{margin:0;font-size:1.2em;font-family:var(--font-mono)}
.modal-close{font-size:24px;cursor:pointer;border:none;background:none}
.modal-body{flex-grow:1;overflow-y:auto}
.modal-body pre{margin:0;white-space:pre-wrap}
.modal-body img{max-width:100%;height:auto;display:block;margin:0 auto}

.tabs{display:flex;gap:.5rem;margin-bottom:1rem}
.tab-button{padding:.5rem .75rem;border:1px solid var(--border-color);background:var(--secondary-bg);border-radius:6px;cursor:pointer}
.tab-button.active{background:var(--accent-color);color:#fff;border-color:var(--accent-color)}
.tab-panel{display:none}
.tab-panel.active{display:flex;flex-direction:column;gap:1rem;flex-grow:1}

#performance-container{display:flex;flex-direction:column;gap:1rem}
.metric-block{border:1px solid var(--border-color);border-radius:6px;padding:1rem;background:var(--secondary-bg)}
.metric-block h3{margin:0 0 .75rem 0;font-size:1.1rem;border-bottom:1px solid var(--border-color);padding-bottom:.5rem}
.chart-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:1rem}
.chart-container{position:relative;height:300px}
#perf-learning-body table{width:100%;border-collapse:collapse;font-size:.85rem}
#perf-learning-body th,#perf-learning-body td{border:1px solid var(--border-color);padding:8px;text-align:left}
#perf-learning-body th{background-color:var(--primary-bg)}
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

  <!-- Bootstrap controls -->
  <div class="controls" id="bootstrap-controls" style="border-bottom:1px solid var(--border-color);">
    <span style="font-weight:600">Provider:</span>
    <label class="inline"><input type="radio" name="provider" value="openai" checked> ChatGPT 5 (OpenAI)</label>
    <label class="inline"><input type="radio" name="provider" value="gemini"> Gemini 2.5 Pro (Google)</label>
    <span style="flex:0 0 16px"></span>
    <label class="inline" title="Kreativt discovery-läge (ingen kod) i Steg A"><input type="checkbox" id="kmod-toggle" checked> K-MOD i Steg A</label>
    <label class="inline" title="Bäddar in full text för valda filer i bootstrap-prompten"><input type="checkbox" id="embed-toggle"> Bädda in fulltext</label>
    <span style="flex:1"></span>
    <button id="help-button" class="info">Hjälp</button>
    <button id="make-discovery">Skapa nästa arbete</button>
    <button id="make-implementation" class="primary">Skapa uppgift</button>
  </div>

  <div id="tab-context" class="tab-panel active">
    <div class="output-container">
      <textarea id="instruction-input" placeholder="Skriv kort mål (≤200 tecken) ELLER klistra in Discovery-JSON här…"></textarea>
      <div id="status-banner" class="banner"></div>
      <div class="output-area" style="display:flex;flex-direction:column;">
        <div class="controls" style="border-bottom:none;margin-bottom:0;padding-bottom:0;">
          <button id="copy-json-btn" disabled>Copy JSON</button>
          <button id="download-json-btn" disabled>Download JSON</button>
        </div>
        <pre id="output-pre" style="flex-grow:1;margin-top:1em;">Generated context or bootstrap JSON will appear here.</pre>
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

<!-- Preview modal -->
<div id="file-preview-modal" class="modal">
  <div class="modal-content">
    <div class="modal-header">
      <h2 id="modal-title">File Preview</h2>
      <div class="modal-actions" style="display:flex;gap:10px;">
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

<!-- Help modal -->
<div id="help-modal" class="modal">
  <div class="modal-content" style="max-width:900px;">
    <div class="modal-header">
      <h2>Hjälp – Rätt arbetssekvens</h2>
      <button id="help-close" class="modal-close">×</button>
    </div>
    <div class="modal-body">
      <h4>Steg A – Skapa nästa arbete (Discovery, K-MOD)</h4>
      <ol>
        <li>Skriv målet i en mening i rutan ovan.</li>
        <li>Klicka <b>Skapa nästa arbete</b> → prompt med <b>HÅRDA REGLER</b> + <b>CANDIDATE_PATHS</b> visas.</li>
        <li>Kör prompten i modellen. Få tillbaka <b>Discovery-JSON</b>.</li>
        <li>Klistra in Discovery-JSON i rutan. Buildern validerar och autoväljer filer.</li>
        <li>Justera val vid behov, klicka <b>Generate Context</b> för context_custom.json.</li>
      </ol>
      <h4>Steg B – Skapa uppgift (Implementation)</h4>
      <ol>
        <li>Välj provider. Kryssa <b>Bädda in fulltext</b> om ny session saknar all kontext.</li>
        <li>Klicka <b>Skapa uppgift</b> → bootstrap-JSON (system+user) skapas med bildförbud och PLAN→GEN.</li>
        <li>Använd bootstrap som <b>första prompt</b> i ny “dum” chatsession.</li>
        <li>Följ: PLAN-JSON → “OK” → GEN-JSON (patch/tester).</li>
      </ol>
      <p><b>Bildpolicy:</b> inga bilder genereras om det inte uttryckligen begärs.</p>
    </div>
  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', () => {
  let fullContext = null;
  let ALL_PATHS = [];
  const charts = {};

  const REPO_RAW_URL = 'https://raw.githubusercontent.com/Engrove/Engrove-Audio-Tools-2.0/main/';
  const IMAGE_EXTENSIONS = ['png','jpg','jpeg','gif','webp','svg'];

  const CORE_DOC_PATHS = [
    'docs/ai_protocols/AI_Core_Instruction.md',
    'docs/ai_protocols/ai_config.json',
    'docs/ai_protocols/frankensteen_persona.v1.0.json',
    'docs/ai_protocols/AI_Dynamic_Protocols.md',
    'docs/ai_protocols/DynamicProtocols.json',
    'docs/ai_protocols/DynamicProtocol.schema.json',
    'docs/ai_protocols/System_Integrity_Check_Protocol.md',
    'docs/ai_protocols/Stature_Report_Protocol.md',
    'docs/ai_protocols/AI_Chatt_Avslutningsprotokoll.md',
    'docs/ai_protocols/Help_me_God_Protokoll.md',
    'docs/ai_protocols/Stalemate_Protocol.md',
    'docs/ai_protocols/Levande_Kontext_Protokoll.md',
    'docs/ai_protocols/context_bootstrap_instruction.md',
    'docs/AI_Collaboration_Standard.md',
    'docs/Mappstruktur_och_Arbetsflöde.md',
    'docs/Blueprint_för_Migrering_v1_till_v2.md',
    'docs/Engrove_Audio_Toolkit_v2.0_Analys.md',
    'docs/Global_UI-Standard_för_Engrove-plattformen.md',
    'docs/Global_UI-Standard_Komponentspecifikation.md',
    'docs/Teknisk_Beskrivning_Engrove_Audio_Toolkit.md',
    'docs/ByggLogg.json',
    'tools/frankensteen_learning_db.json',
    'tools/citation_cache.json',
    'logs/rotorsakslogg_TEMPLATE.md',
    'docs/ai_protocols/Beroendeanalys_Protokoll.md',
    'docs/ai_protocols/Brainstorming_Protokoll.md',
    'docs/ai_protocols/K-MOD_Protokoll.md',
    'docs/ai_protocols/Kontext-JSON_Protokoll.md',
    'docs/ai_protocols/Structured_Debugging_Checklist.md',
    'docs/ai_protocols/Micro_Retrospective.md',
    'package.json',
    'vite.config.js',
    'scripts/generate_full_context.py',
    'scripts/wrap_json_in_html.py',
    'scripts/history/historical_reconstruction_builder.py'
  ];

  const ICONS = {
    folder:'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M4 6h6l2 2h8v10H4z"></path></svg>',
    file:'<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" /></svg>',
    image:'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"></path></svg>'
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
  const btnDisc = document.getElementById('make-discovery');
  const btnImpl = document.getElementById('make-implementation');
  const kmodToggle = document.getElementById('kmod-toggle');
  const embedToggle = document.getElementById('embed-toggle');
  const helpButton = document.getElementById('help-button');
  const helpModal  = document.getElementById('help-modal');
  const helpClose  = document.getElementById('help-close');
  const statusBanner = document.getElementById('status-banner');

  let currentFileContent = '';
  let currentFilePath = '';
  let currentFileIsBinary = false;

  // MUST-regler inkl. bildförbud
  const NO_IMAGE_RULE = "[MUST] ALDRIG generera bilder om inte användaren uttryckligen begär bildgenerering. Inga bildverktyg, inga Markdown-bilder, inga data-URI.";
  const MUST_STRICT = [
    "[MUST] Diff om >50 rader → unified patch",
    "[MUST] Full historik i filhuvud (ingen trunkering)",
    "[MUST] Ändra ej filer med is_content_full=false",
    "[MUST] Lista berörda API-kontrakt",
    "[MUST] Lägg till/uppdatera tester + körkommandon",
    NO_IMAGE_RULE,
    "Svar ENBART i PLAN-JSON → (OK) → GEN-JSON"
  ].join("\n");

  const KMOD_BANNER = "MODE: K-MOD (Brainstorming/Discovery). Ingen kod. Endast JSON enligt schema.";
  const IMAGE_GUARD_BANNER = "BILDREGEL: ALDRIG generera bilder i denna session om det inte uttryckligen efterfrågas.";

  // ---------- Helpers ----------
  function showBanner(msg, kind='warn'){
    statusBanner.textContent = msg;
    statusBanner.className = 'banner ' + (kind==='ok'?'ok':kind==='err'?'err':'warn');
    statusBanner.style.display = 'block';
  }
  function clearBanner(){
    statusBanner.style.display = 'none';
    statusBanner.textContent = '';
    statusBanner.className = 'banner';
  }

  function getIcon(name,isFolder){
    if(isFolder) return ICONS.folder;
    const ext = name.split('.').pop().toLowerCase();
    if(IMAGE_EXTENSIONS.includes(ext)) return ICONS.image;
    return ICONS.file;
  }

  function renderFileTree(node, parentElement, currentPath){
    const ul = document.createElement('ul');
    const sorted = Object.keys(node).sort((a,b)=>{
      const af = node[a].type==='file', bf = node[b].type==='file';
      if(af && !bf) return 1;
      if(!af && bf) return -1;
      return a.localeCompare(b);
    });
    sorted.forEach(key=>{
      const item = node[key];
      const itemPath = currentPath ? `${currentPath}/${key}` : key;
      const li = document.createElement('li');
      const isFolder = item.type!=='file';

      const label = document.createElement('label');
      label.className = 'tree-item-label';

      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.setAttribute('data-path', itemPath);
      label.appendChild(checkbox);

      const iconSpan = document.createElement('span');
      iconSpan.className = 'file-icon';
      iconSpan.innerHTML = getIcon(key,isFolder);
      label.appendChild(iconSpan);

      if(isFolder){
        li.classList.add('folder');
        const toggle = document.createElement('span');
        toggle.className = 'toggle'; toggle.textContent = '►';
        li.appendChild(toggle);

        const folderNameSpan = document.createElement('span');
        folderNameSpan.textContent = ` ${key}`;
        label.appendChild(folderNameSpan);
        li.appendChild(label);

        const nested = renderFileTree(item, li, itemPath);
        nested.style.display = 'none';
        li.appendChild(nested);

        toggle.addEventListener('click', ()=>{
          const isCollapsed = nested.style.display==='none';
          nested.style.display = isCollapsed ? 'block':'none';
          toggle.textContent = isCollapsed ? '▼':'►';
        });
      }else{
        li.classList.add('file');
        const fileNameSpan = document.createElement('a');
        fileNameSpan.className = 'file-name-clickable'; fileNameSpan.href = '#';
        fileNameSpan.textContent = ` ${key}`; fileNameSpan.setAttribute('data-path', itemPath);
        label.appendChild(fileNameSpan);
        li.appendChild(label);

        fileNameSpan.addEventListener('click', async (e)=>{
          e.preventDefault(); await openFilePreview(itemPath);
        });
      }
      ul.appendChild(li);
    });
    parentElement.appendChild(ul);
    return ul;
  }

  function expandToNode(element){
    let parent = element.parentElement.closest('li.folder');
    while(parent){
      const nestedUl = parent.querySelector('ul');
      const toggle = parent.querySelector('.toggle');
      if(nestedUl && toggle){ nestedUl.style.display='block'; toggle.textContent='▼'; }
      parent = parent.parentElement.closest('li.folder');
    }
  }

  function flattenPaths(node, prefix='', out=[]){
    Object.keys(node).sort().forEach(k=>{
      const it = node[k], p = prefix ? `${prefix}/${k}` : k;
      if(it.type==='file'){ out.push(it.path || p); }
      else { flattenPaths(it, p, out); }
    });
    return out;
  }

  function selectCoreDocs(){
    fileTreeContainer.querySelectorAll('input[type="checkbox"]:not(:disabled)').forEach(cb=>cb.checked=false);
    CORE_DOC_PATHS.forEach(path=>{
      const checkbox = fileTreeContainer.querySelector(`input[data-path="${path}"]`);
      if(checkbox && !checkbox.disabled){ checkbox.checked = true; expandToNode(checkbox); }
    });
  }

  async function openFilePreview(path){
    const modalTitle = document.getElementById('modal-title');
    const modalBody = document.getElementById('modal-body');
    const modalCopyBtn = document.getElementById('modal-copy-btn');
    const modalDownloadBtn = document.getElementById('modal-download-btn');

    modalTitle.textContent = path;
    modalBody.innerHTML = '<p>Loading content...</p>';
    document.getElementById('file-preview-modal').classList.add('visible');
    modalCopyBtn.disabled = true; modalDownloadBtn.disabled = true;
    currentFileContent = ''; currentFilePath = path; currentFileIsBinary = false;

    try{
      const url = `${REPO_RAW_URL}${path}`;
      const ext = path.split('.').pop().toLowerCase();
      if(IMAGE_EXTENSIONS.includes(ext)){
        currentFileIsBinary = true;
        modalBody.innerHTML = `<img src="${url}" alt="Preview of ${path}">`;
        const r = await fetch(url); if(!r.ok) throw new Error(`HTTP ${r.status}`);
        currentFileContent = await r.blob();
        modalDownloadBtn.disabled = false;
      }else{
        const r = await fetch(url); if(!r.ok) throw new Error(`HTTP ${r.status}`);
        const text = await r.text();
        currentFileContent = text;
        const pre = document.createElement('pre'); const code = document.createElement('code');
        code.textContent = text; pre.appendChild(code);
        modalBody.innerHTML = ''; modalBody.appendChild(pre);
        modalCopyBtn.disabled = false; modalDownloadBtn.disabled = false;
      }
    }catch(e){
      console.error('Preview failed', e);
      modalBody.textContent = `Error: Failed to fetch content for ${path}. ${e.message}`;
    }
  }

  async function fetchFileContent(path){
    try{
      const r = await fetch(`${REPO_RAW_URL}${path}`); if(!r.ok) throw new Error(`HTTP ${r.status}`);
      return await r.text();
    }catch(e){
      console.error('fetchFileContent', e);
      return `// Error: Failed to fetch content for ${path}`;
    }
  }

  async function buildNewContextStructure(sourceNode, selectedPaths){
    const newNode = {}; const promises = [];
    function traverse(src, dst, cur=''){
      const keys = Object.keys(src).sort();
      for(const key of keys){
        const item = src[key];
        const itemPath = cur ? `${cur}/${key}` : key;
        if(item.type==='file'){
          const isSelected = selectedPaths.has(item.path);
          const stub = { ...item };
          if(isSelected && (item.is_binary || item.content === null)){
            promises.push(fetchFileContent(item.path).then(c => { stub.content = c; }));
          }else if(!isSelected){
            delete stub.content;
          }
          dst[key] = stub;
        }else{
          dst[key] = {}; traverse(item, dst[key], itemPath);
        }
      }
    }
    traverse(sourceNode, newNode);
    await Promise.all(promises);
    return newNode;
  }

  async function generateSelectedContext(){
    if(!fullContext) return;
    generateBtn.disabled = true; const old = generateBtn.textContent; generateBtn.textContent = 'Generating...';
    try{
      clearBanner();
      const selectedPaths = new Set(Array.from(fileTreeContainer.querySelectorAll('input[type="checkbox"]:checked')).map(cb=>cb.dataset.path));
      const newContext = {
        project_overview: fullContext.project_overview,
        ai_instructions: fullContext.ai_instructions,
        file_structure: {}
      };
      if(instructionInput.value.trim()){ newContext.ai_instructions_input = instructionInput.value.trim(); }
      try{
        if(typeof newContext.ai_instructions === 'object' && newContext.ai_instructions){
          newContext.ai_instructions.obligatory_rules = Array.from(new Set([...(newContext.ai_instructions.obligatory_rules || []), "forbid_image_generation"]));
        }else{
          newContext.ai_instructions = {"obligatory_rules":["forbid_image_generation"]};
        }
      }catch(_){}

      newContext.file_structure = await buildNewContextStructure(fullContext.file_structure, selectedPaths);
      outputPre.textContent = JSON.stringify(newContext, null, 2);
      copyBtn.disabled = false; downloadBtn.disabled = false;
      showBanner('Context genererad.', 'ok');
    }catch(e){
      outputPre.textContent = `An error occurred during context generation: ${e.message}`;
      showBanner('Fel vid context-generering: '+e.message, 'err');
    }finally{
      generateBtn.disabled = false; generateBtn.textContent = old;
    }
  }

  async function generateFilesOnly(){
    if(!fullContext) return;
    generateFilesBtn.disabled = true; const old = generateFilesBtn.textContent; generateFilesBtn.textContent='Generating...';
    try{
      clearBanner();
      let output = {};
      const instructionText = instructionInput.value.trim();
      if(instructionText){
        try{ output = { ...JSON.parse(instructionText) }; }
        catch(_){ output.user_instruction = instructionText; }
      }
      if(typeof output === 'object' && output){
        if(!output.obligatory_rules) output.obligatory_rules = [];
        if(!output.obligatory_rules.includes("forbid_image_generation")){
          output.obligatory_rules.push("forbid_image_generation");
        }
      }
      const selectedPaths = new Set(Array.from(fileTreeContainer.querySelectorAll('input[type="checkbox"]:checked')).map(cb=>cb.dataset.path));
      const filesContent = {};
      const populated = await buildNewContextStructure(fullContext.file_structure, selectedPaths);
      (function extract(node){
        for(const k in node){
          const it = node[k];
          if(it.type==='file'){
            if(it.content !== undefined){ filesContent[it.path] = it.content; }
          }else extract(it);
        }
      })(populated);
      output.files = filesContent;
      outputPre.textContent = JSON.stringify(output, null, 2);
      copyBtn.disabled = false; downloadBtn.disabled = false;
      showBanner('Filer genererade.', 'ok');
    }catch(e){
      outputPre.textContent = `An error occurred during file generation: ${e.message}`;
      showBanner('Fel vid file-generering: '+e.message, 'err');
    }finally{
      generateFilesBtn.disabled = false; generateFilesBtn.textContent = old;
    }
  }

  // Provider bootstrap
  function toOpenAI(systemText, userText){
    return { provider:"openai", model:"gpt-5", auto_start:true, messages:[
      {role:"system",content:systemText}, {role:"user",content:userText}
    ]};
  }
  function toGemini(systemText, userText){
    return { provider:"google", model:"gemini-2.5-pro", auto_start:true,
      system_instruction:systemText, contents:[{role:"user",parts:[{text:userText}]}]
    };
  }

  function guessLang(path){
    const ext=(path.split('.').pop()||'').toLowerCase();
    if(['ts','tsx'].includes(ext)) return 'ts';
    if(ext==='vue') return 'vue';
    if(ext==='py') return 'py';
    if(['js','jsx'].includes(ext)) return 'js';
    if(ext==='md') return 'md';
    return 'txt';
  }

  async function buildUserWithEmbeds(task, selected){
    const list = selected.map(p=>`- ${p} (is_content_full=true, lang=${guessLang(p)})`).join("\n");
    let body = `UPPGIFT: ${task}\nFILER:\n${list}\n`;
    if(embedToggle.checked){
      body += "\n=== KONTEXT (fulltext) ===\n";
      for(const p of selected){
        try{
          const t = await fetchFileContent(p);
          body += `\n----- FILE: ${p} BEGIN -----\n${t}\n----- FILE: ${p} END -----\n`;
        }catch(_){
          body += `\n----- FILE: ${p} BEGIN -----\n// Failed to fetch ${p}\n----- FILE: ${p} END -----\n`;
        }
      }
    }
    return body + "PLANERA";
  }

  function getTask(){
    const t = instructionInput.value.trim();
    return (t && t.length < 200) ? t : "Beskriv kort mål i en mening.";
  }
  function currentProvider(){
    return (document.querySelector('input[name="provider"]:checked')?.value || "openai");
  }

  // Discovery schema + Hårda regler + Candidate paths
  function buildDiscoveryPrompt(task){
    return {
      protocol_id:"discovery_v1",
      psv:["rules_rehearsed","risk_scan"],
      mode: kmodToggle?.checked ? "K-MOD" : undefined,
      obligatory_rules:["forbid_image_generation"],
      task, filesToSelect:[], requires_full_files:[], stubs_ok:[],
      requires_chunks:[], api_contracts_touched:[], risks:[], test_plan:[],
      done_when:["tests_green","lint_ok","types_ok"],
      _note:"Lista bara det som krävs. Motivera varje post i requires_full_files i notes (≤200 tecken)."
    };
  }
  function buildCandidateBlock(){ return ["CANDIDATE_PATHS:", ...ALL_PATHS.map(p=>`- ${p}`)].join("\n"); }
  function discoveryHardRules(){
    return [
      "HÅRDA REGLER:",
      "- Välj ENDAST paths från CANDIDATE_PATHS.",
      "- Inga placeholders eller påhittade vägar.",
      "- 'requires_full_files' ⊆ 'filesToSelect'.",
      "- 'stubs_ok' ⊆ 'filesToSelect' och disjunkta mot 'requires_full_files'.",
      "- Minst 2 paths i 'filesToSelect'."
    ].join("\n");
  }

  function makeDiscoveryText(){
    const task = getTask();
    const disc = buildDiscoveryPrompt(task);
    const parts = [
      "SESSION: PLANERA NÄSTA ARBETE (Discovery)",
      KMOD_BANNER, IMAGE_GUARD_BANNER,
      "KRAV: Svara ENBART med giltig JSON enligt schema. Ingen kod.",
      discoveryHardRules(),
      "SCHEMA:", JSON.stringify(disc, null, 2),
      buildCandidateBlock(),
      "KONTEXT-RÅD:",
      "- Lista bara det som verkligen behövs för implementationen i nästa steg.",
      "- Motivera varje post i 'requires_full_files' kort i 'notes' (max 200 tecken)."
    ];
    return parts.join("\n");
  }

  // Validering av inklistrad Discovery-JSON
  function validateDiscoveryJSON(obj){
    const err = [];
    const set = new Set(ALL_PATHS);
    const sel = new Set(obj.filesToSelect||[]);
    const full = new Set(obj.requires_full_files||[]);
    const stub = new Set(obj.stubs_ok||[]);
    const inIndex = arr => (arr||[]).every(p => set.has(p));

    if((obj.filesToSelect||[]).length < 2) err.push("Minst 2 paths i filesToSelect.");
    if(!inIndex(obj.filesToSelect)) err.push("Okänd path i filesToSelect.");
    if(!inIndex(obj.requires_full_files)) err.push("Okänd path i requires_full_files.");
    if(!inIndex(obj.stubs_ok)) err.push("Okänd path i stubs_ok.");
    for(const p of full) if(!sel.has(p)) err.push(`Full men ej vald: ${p}`);
    for(const p of stub) if(!sel.has(p)) err.push(`Stub men ej vald: ${p}`);
    for(const p of full) if(stub.has(p)) err.push(`Samma path i full & stub: ${p}`);
    return err;
  }

  function autoSelectFromDiscovery(obj){
    const all = Array.from(fileTreeContainer.querySelectorAll('input[type="checkbox"]'));
    (obj.filesToSelect||[]).forEach(p=>{
      const cb = all.find(x=>x.dataset.path===p);
      if(cb){ cb.checked = true; expandToNode(cb); }
    });
  }

  // Events
  selectAllBtn.addEventListener('click', ()=> fileTreeContainer.querySelectorAll('input[type="checkbox"]:not(:disabled)').forEach(cb=>cb.checked=true));
  deselectAllBtn.addEventListener('click', ()=> fileTreeContainer.querySelectorAll('input[type="checkbox"]:not(:disabled)').forEach(cb=>cb.checked=false));
  selectCoreDocsBtn.addEventListener('click', selectCoreDocs);

  generateBtn.addEventListener('click', generateSelectedContext);
  generateFilesBtn.addEventListener('click', generateFilesOnly);

  function showButtonFeedback(button, text, color){
    const orig = button.textContent;
    const obg = button.style.backgroundColor; const oc = button.style.color;
    button.textContent = text; button.style.backgroundColor = `var(--${color}-color)`; button.style.color = (color==='warn')?'#000':'#fff';
    setTimeout(()=>{ button.textContent = orig; button.style.backgroundColor = obg; button.style.color = oc; }, 1500);
  }

  if(copyBtn) copyBtn.addEventListener('click', ()=>{ navigator.clipboard.writeText(outputPre.textContent).then(()=>showButtonFeedback(copyBtn,'Copied!','success')).catch(()=>showButtonFeedback(copyBtn,'Error!','danger')); });
  if(downloadBtn) downloadBtn.addEventListener('click', ()=>{
    const blob = new Blob([outputPre.textContent], {type:'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href=url; a.download=`context_custom_${new Date().toISOString().slice(0,10)}.json`;
    document.body.appendChild(a); a.click(); document.body.removeChild(a); URL.revokeObjectURL(url);
  });

  document.getElementById('modal-close-btn').addEventListener('click', ()=> document.getElementById('file-preview-modal').classList.remove('visible'));
  document.addEventListener('keydown', (e)=>{ if(e.key==='Escape'){ document.getElementById('file-preview-modal').classList.remove('visible'); helpModal.classList.remove('visible'); } });
  document.getElementById('modal-copy-btn').addEventListener('click', ()=>{
    if(!currentFileIsBinary && currentFileContent){
      navigator.clipboard.writeText(currentFileContent).then(()=>showButtonFeedback(document.getElementById('modal-copy-btn'),'Copied!','success')).catch(()=>showButtonFeedback(document.getElementById('modal-copy-btn'),'Error!','danger'));
    }
  });
  document.getElementById('modal-download-btn').addEventListener('click', ()=>{
    if(!currentFileContent) return;
    const blob = currentFileIsBinary ? currentFileContent : new Blob([currentFileContent], {type:'text/plain'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href=url; a.download=currentFilePath.split('/').pop()||'download';
    document.body.appendChild(a); a.click(); document.body.removeChild(a); URL.revokeObjectURL(url);
  });

  helpButton.addEventListener('click', ()=> helpModal.classList.add('visible'));
  helpClose.addEventListener('click', ()=> helpModal.classList.remove('visible'));

  // Discovery
  btnDisc.addEventListener('click', ()=>{
    clearBanner();
    if(!fullContext){ showBanner('context.json ej laddad ännu.', 'err'); return; }
    const discoveryText = makeDiscoveryText();
    outputPre.textContent = discoveryText;
    copyBtn.disabled = false; downloadBtn.disabled = false;
    showButtonFeedback(btnDisc,"Skapad!","success");
    showBanner('Discovery-prompt skapad. Kör i modellen och klistra in svaret här.', 'ok');
  });

  // Implementation
  btnImpl.addEventListener('click', async ()=>{
    clearBanner();
    const task = getTask();
    const selected = Array.from(fileTreeContainer.querySelectorAll('input[type="checkbox"]:checked')).map(cb=>cb.dataset.path).filter(Boolean);
    if(selected.length===0){ showBanner('Välj minst 1 fil (fulltext) i trädet.', 'err'); return; }
    const userText = await buildUserWithEmbeds(task, selected);
    const systemText = MUST_STRICT;
    const provider = currentProvider();
    const bootstrap = (provider === "gemini") ? toGemini(systemText, userText) : toOpenAI(systemText, userText);
    outputPre.textContent = JSON.stringify(bootstrap, null, 2);
    copyBtn.disabled = false; downloadBtn.disabled = false;
    showButtonFeedback(btnImpl,"Skapad!","success");
    showBanner('Bootstrap-JSON klar. Använd som första prompt i en ny, tom session.', 'ok');
  });

  // Instruction input (task eller Discovery-JSON)
  instructionInput.addEventListener('input', ()=>{
    clearBanner();
    const text = instructionInput.value.trim();
    if(!text) return;
    try{
      const parsed = JSON.parse(text);
      if(parsed && Array.isArray(parsed.filesToSelect)){
        const errs = validateDiscoveryJSON(parsed);
        if(errs.length) showBanner('Discovery-JSON varningar: '+errs.join(' | '), 'warn');
        autoSelectFromDiscovery(parsed);
      }
    }catch(_){ /* tolka som task-text */ }
  });

  // Tabs & performance
  function setupPerformanceDashboard(){
    document.querySelectorAll('.tab-button').forEach(btn=>{
      btn.addEventListener('click', ()=>{
        const tab = btn.getAttribute('data-tab');
        document.querySelectorAll('.tab-button').forEach(b=>b.classList.remove('active'));
        btn.classList.add('active');
        document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));
        document.getElementById(`tab-${tab}`).classList.add('active');
        if(tab==='performance' && fullContext){ renderPerformanceDashboard(); }
      });
    });
    document.addEventListener('click', (e)=>{
      if(e.target && e.target.id === 'refresh-performance'){ refreshPerformanceData(); }
    });
  }

  async function refreshPerformanceData(){
    try{
      const res = await fetch('context.json', {cache:'no-store'});
      if(!res.ok) throw new Error(`status ${res.status}`);
      const data = await res.json();
      if(data && data.ai_performance_metrics){
        fullContext.ai_performance_metrics = data.ai_performance_metrics;
        renderPerformanceDashboard();
      }
    }catch(e){ console.error('Kunde inte läsa om context.json:', e); }
  }

  function aggregateModelStats(items){
    const byProvider = {}; const byModel = {};
    const visit = (obj)=>{
      if(obj && typeof obj === 'object'){
        if(obj.model && typeof obj.model === 'object'){
          const prov = obj.model.provider || 'unknown';
          const name = obj.model.name || 'unknown';
          byProvider[prov] = (byProvider[prov] || 0) + 1;
          const key = `${prov}:${name}`; byModel[key] = (byModel[key] || 0) + 1;
        }else if(obj.generatedBy && obj.generatedBy.model){
          const prov = obj.generatedBy.model.provider || 'unknown';
          const name = obj.generatedBy.model.name || 'unknown';
          byProvider[prov] = (byProvider[prov] || 0) + 1;
          const key = `${prov}:${name}`; byModel[key] = (byModel[key] || 0) + 1;
        }
        for(const k in obj){
          const v = obj[k];
          if(Array.isArray(v)) v.forEach(visit);
          else if(v && typeof v === 'object') visit(v);
        }
      }
    };
    (items || []).forEach(visit);
    return { byProvider, byModel };
  }

  function renderLearningDbTable(targetEl, data){
    if(!data || data.length===0){ targetEl.innerHTML = 'Ingen data.'; return; }
    const rows = data.map(item=>`
      <tr>
        <td>${item.heuristicId || 'N/A'}</td>
        <td>${(item.identifiedRisk && item.identifiedRisk.description) || 'N/A'}</td>
        <td>${(item.mitigation && item.mitigation.description) || 'N/A'}</td>
        <td>${(item.trigger && item.trigger.keywords || []).join(', ')}</td>
      </tr>`).join('');
    targetEl.innerHTML = `<table><thead><tr><th>ID</th><th>Risk</th><th>Mitigation</th><th>Trigger Keywords</th></tr></thead><tbody>${rows}</tbody></table>`;
  }

  function renderPerformanceDashboard(){
    if(!fullContext || !fullContext.ai_performance_metrics) return;
    const metrics = fullContext.ai_performance_metrics;
    const perfLog = Array.isArray(metrics.performanceLog) ? metrics.performanceLog : [];
    const learningDb = Array.isArray(metrics.learningDatabase) ? metrics.learningDatabase : [];

    Object.values(charts).forEach(c=>{ if(c && typeof c.destroy==='function') c.destroy(); });
    if(perfLog.length===0){
      const learningBody = document.getElementById('perf-learning-body');
      if(learningBody) learningBody.innerHTML = 'Ingen prestandadata tillgänglig.';
      return;
    }

    const labels = perfLog.map(p => `Session ${p.sessionId}`);
    const finalScores = perfLog.map(p => p.scorecard ? p.scorecard.finalScore : 0);
    const debuggingCycles = perfLog.map(p => p.detailedMetrics ? p.detailedMetrics.debuggingCycles : 0);
    const selfCorrections = perfLog.map(p => p.detailedMetrics ? p.detailedMetrics.selfCorrections : 0);
    const externalCorrections = perfLog.map(p => p.detailedMetrics ? p.detailedMetrics.externalCorrections : 0);

    const { byProvider, byModel } = aggregateModelStats(perfLog);

    charts.scoreChart = new Chart(document.getElementById('score-chart').getContext('2d'), {
      type:'line',
      data:{ labels, datasets:[{ label:'Final Score', data:finalScores, borderColor:'var(--accent-color)', backgroundColor:'rgba(0,123,255,.1)', fill:true, tension:.1 }] },
      options:{ responsive:true, maintainAspectRatio:false }
    });
    charts.metricsChart = new Chart(document.getElementById('metrics-chart').getContext('2d'), {
      type:'bar',
      data:{ labels, datasets:[
        { label:'Debugging Cycles', data:debuggingCycles, backgroundColor:'rgba(220,53,69,.7)' },
        { label:'Self Corrections', data:selfCorrections, backgroundColor:'rgba(255,193,7,.7)' },
        { label:'External Corrections', data:externalCorrections, backgroundColor:'rgba(23,162,184,.7)' },
      ]},
      options:{ responsive:true, maintainAspectRatio:false, scales:{ x:{stacked:true}, y:{stacked:true, beginAtZero:true} } }
    });
    charts.providerChart = new Chart(document.getElementById('provider-chart').getContext('2d'), {
      type:'pie',
      data:{ labels:Object.keys(byProvider), datasets:[{ data:Object.values(byProvider) }] },
      options:{ responsive:true, maintainAspectRatio:false }
    });
    charts.modelChart = new Chart(document.getElementById('model-chart').getContext('2d'), {
      type:'pie',
      data:{ labels:Object.keys(byModel), datasets:[{ data:Object.values(byModel) }] },
      options:{ responsive:true, maintainAspectRatio:false }
    });

    const learningBody = document.getElementById('perf-learning-body');
    if(learningBody) renderLearningDbTable(learningBody, learningDb);
  }

  // Load context.json
  fetch('context.json')
    .then(r=>{ if(!r.ok) throw new Error(`HTTP status ${r.status}`); return r.json(); })
    .then(data=>{
      fullContext = data;
      ALL_PATHS = flattenPaths(fullContext.file_structure);
      fileTreeContainer.innerHTML = '';
      renderFileTree(fullContext.file_structure, fileTreeContainer, '');
      setupPerformanceDashboard();
      showBanner('Context laddad. Fortsätt med Steg A eller B.', 'ok');
    })
    .catch(e=>{
      fileTreeContainer.innerHTML = `<p style="color: var(--danger-color);"><b>Error:</b> Could not load context.json. ${e.message}</p>`;
    });
});
</script>

</body>
</html>"""
    try:
        with open(output_html_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
        print(f"Successfully generated {output_html_path}")
    except Exception as e:
        print(f"Error writing to {output_html_path}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python wrap_json_in_html.py <output_html_path>", file=sys.stderr)
        sys.exit(1)
    output_file_path = sys.argv[1]
    output_dir = os.path.dirname(output_file_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    create_interactive_html(output_file_path)
