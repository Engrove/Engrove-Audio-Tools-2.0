#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wrap_json_in_html.py — AI Context Builder v7.3

Kör:
  python wrap_json_in_html.py out.html

Läser lokal context.json (skapas av generate_full_context.py) med fält:
{
  "file_structure": { ... nested ... },
  "project_overview": {... valfritt ...},
  "ai_instructions": {... valfritt ...},
  "ai_performance_metrics": {... valfritt ...}
}

Nyheter v7.3:
- Kaskadkryss i filträdet (mapp → barn & barnbarn) + tri-state uppåt.
- Working-overlay med spinner + körlogg (withBusy/logw) runt alla tunga åtgärder.
- All JSON-utdata bäddas i Markdown med protokollhuvud (4 rader) + ```json``` (Download → .md).
- Implementation-output delas i två giltiga markdownsektioner: impl_bootstrap_v1.json och provider_envelope.json.
- AI Performance: filter (datum, provider, modell), KPI-kort, förbättrad tabell, CSV-export, MA(3) kurva.
"""
import os, sys

HTML = r"""<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>AI Context Builder v7.3 – JSON-first (K-MOD + D-MOD, STRICT)</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1"></script>
<style>
:root{
  --bg:#f8f9fa; --fg:#212529; --muted:#6c757d;
  --card:#ffffff; --line:#dee2e6; --accent:#0d6efd; --accent-2:#0b5ed7;
  --ok:#28a745; --warn:#ffc107; --err:#dc3545; --info:#17a2b8;
  --mono:ui-monospace,"JetBrains Mono","SF Mono",Consolas,Menlo,monospace;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--sans);height:100vh;display:flex;overflow:hidden}
.panel{padding:12px;overflow:auto;border-right:1px solid var(--line);display:flex;flex-direction:column}
#left{width:42%;min-width:360px}
#right{width:58%;gap:12px}
.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding-bottom:8px;margin-bottom:8px;border-bottom:1px solid var(--line)}
button{border:1px solid var(--line);background:var(--card);color:var(--fg);padding:8px 12px;border-radius:8px;cursor:pointer}
button:hover{background:#eef1f4}
button.primary{background:var(--accent);color:#fff;border-color:var(--accent)}
button.primary:hover{background:var(--accent-2)}
button.info{background:var(--info);color:#fff;border-color:var(--info)}
button.warn{background:var(--warn);color:#000;border-color:var(--warn)}
button:disabled{opacity:.6;cursor:not-allowed}
label.inline{display:inline-flex;align-items:center;gap:6px}
input[type="number"]{width:90px}

#tree ul{list-style:none;padding-left:18px;margin:0}
#tree li{padding:3px 0}
.toggle{cursor:pointer;user-select:none;display:inline-block;width:1em}
.fileline{display:flex;align-items:center;gap:6px}
pre,textarea{font-family:var(--mono);font-size:13.5px}
textarea#instruction{height:160px;resize:vertical;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px}
.output{display:flex;flex-direction:column;gap:8px;flex:1}
.output .bar{display:flex;gap:8px;flex-wrap:wrap}
.output pre{flex:1;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px;white-space:pre-wrap}
.banner{padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:#fff8e1;color:#5c4600;display:none}
.banner.err{background:#fde7ea;color:#7a0e1a}
.banner.ok{background:#eaf7ef;color:#114d27}

.tabbar{display:flex;gap:8px;margin-bottom:10px}
.tabbar button{border-radius:8px}
.tabpanel{display:none}
.tabpanel.active{display:flex;flex-direction:column;gap:12px}

/* Modals */
.modal{position:fixed;inset:0;background:rgba(0,0,0,.5);display:none;align-items:center;justify-content:center;z-index:1000}
.modal.show{display:flex}
.modal .box{background:#fff;border-radius:12px;max-width:1000px;width:94%;max-height:88vh;display:flex;flex-direction:column}
.modal .box header{display:flex;align-items:center;justify-content:space-between;padding:12px 14px;border-bottom:1px solid var(--line)}
.modal .box main{padding:14px;overflow:auto}
.modal .box footer{padding:10px 14px;border-top:1px solid var(--line);display:flex;justify-content:flex-end;gap:8px}
kbd{background:#f1f3f5;border:1px solid #e9ecef;border-bottom-color:#dee2e6;border-radius:4px;padding:0 4px}
.small{font-size:12px;color:var(--muted)}
.flex{display:flex;align-items:center;gap:8px;flex-wrap:wrap}

/* Performance UI */
.chart-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px}
.chart-card{border:1px solid var(--line);border-radius:8px;background:var(--card);padding:10px;display:flex;flex-direction:column;gap:6px}
.chart-card h3{margin:0 0 4px 0;font-size:1.05rem;border-bottom:1px solid var(--line);padding-bottom:6px}
.chart-container{position:relative;height:300px}
.table-card{border:1px solid var(--line);border-radius:8px;background:var(--card);padding:10px}
.table-card table{width:100%;border-collapse:collapse;font-size:.9rem}
.table-card th,.table-card td{border:1px solid var(--line);padding:6px;text-align:left}
.table-card th{background:#f1f3f5}
.badge{padding:1px 6px;border-radius:99px;border:1px solid var(--line);background:#eef1f4;font-size:11px}

/* Busy overlay */
#busy{position:fixed;inset:0;display:none;align-items:center;justify-content:center;background:rgba(0,0,0,.35);backdrop-filter:saturate(130%) blur(2px);z-index:2000;padding:12px}
#busy .spinner{width:40px;height:40px;border:4px solid #ddd;border-top-color:#0d6efd;border-radius:50%;animation:spin 1s linear infinite;margin-bottom:10px}
#busy #worklog{max-width:min(90vw,900px);max-height:40vh;overflow:auto;background:#fff;color:#111;border:1px solid #ccc;border-radius:8px;padding:10px;margin:0;white-space:pre-wrap}
@keyframes spin{to{transform:rotate(360deg)}}

/* KPI cards */
.kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.kpi{border:1px solid var(--line);border-radius:8px;background:var(--card);padding:10px}
.kpi h4{margin:0 0 6px 0;font-size:0.95rem;color:#495057}
.kpi .big{font-size:1.6rem;font-weight:700}
.kpi .sub{font-size:.85rem;color:var(--muted)}
.filter-bar{display:flex;gap:10px;align-items:flex-end;flex-wrap:wrap}
.filter-group{display:flex;flex-direction:column;gap:4px}
.filter-group label{font-size:.85rem;color:#495057}
</style>
</head>
<body>

<section id="left" class="panel">
  <div class="controls">
    <button id="selAll">Select All</button>
    <button id="deselAll">Deselect All</button>
    <button id="selCore">Select Core Docs</button>
    <span class="flex">
      <span class="badge">Budget kB</span>
      <input id="budgetKb" type="number" min="100" step="50" value="700" />
      <label class="inline" title="Gör JSON mer kompakt"><input type="checkbox" id="compact" /> Kompakt JSON</label>
    </span>
    <button id="genContext" class="primary">Generate Context</button>
    <button id="genFiles" class="info">Generate Files</button>
  </div>
  <div id="tree"><p>Laddar context.json…</p></div>
</section>

<section id="right" class="panel">
  <div class="tabbar">
    <button data-tab="builder" class="primary">Context Builder</button>
    <button data-tab="performance">AI Performance</button>
    <button id="helpBtn" class="warn">Hjälp</button>
  </div>

  <div id="tab-builder" class="tabpanel active">
    <div class="controls" id="bootstrapBar">
      <span><b>Provider:</b></span>
      <label class="inline"><input type="radio" name="prov" value="openai" checked /> ChatGPT 5</label>
      <label class="inline"><input type="radio" name="prov" value="gemini" /> Gemini 2.5 Pro</label>

      <span style="margin-left:12px"><b>Steg A-läge:</b></span>
      <label class="inline" title="K-MOD: utforskning (max-context)"><input type="radio" name="discMode" value="KMOD" checked /> K-MOD</label>
      <label class="inline" title="D-MOD: deterministiskt urval (ID:n + rules_hash)"><input type="radio" name="discMode" value="DMOD" /> D-MOD</label>

      <label class="inline" title="Discovery-läge (ingen kod) i Steg A"><input type="checkbox" id="kmod" checked /> K-MOD flagga</label>
      <label class="inline" title="Bäddar in full text för valda filer i bootstrap-prompten"><input type="checkbox" id="embed" checked /> Bädda in fulltext</label>
      <button id="discBtn">Skapa nästa arbete</button>
      <button id="implBtn" class="primary">Skapa uppgift</button>
    </div>

    <textarea id="instruction" placeholder="Kort mål (≤200 tecken) ELLER klistra in Discovery-svar (STRICT JSON)…"></textarea>
    <div id="banner" class="banner"></div>

    <div class="output">
      <div class="bar">
        <button id="copy" disabled>Copy</button>
        <button id="download" disabled>Download</button>
      </div>
      <pre id="out">Här visas genererad Discovery-prompt (STRICT K-MOD/D-MOD) eller Markdown med JSON-sektioner.</pre>
      <div class="small">Output är avsett som <b>första prompt</b> i en ny “dum” modelsession utan kontext.</div>
    </div>
  </div>

  <div id="tab-performance" class="tabpanel">
    <!-- Filter bar -->
    <div class="filter-bar">
      <div class="filter-group">
        <label for="pf-from">Från datum (ISO)</label>
        <input type="date" id="pf-from" />
      </div>
      <div class="filter-group">
        <label for="pf-to">Till datum (ISO)</label>
        <input type="date" id="pf-to" />
      </div>
      <div class="filter-group" style="min-width:220px">
        <label>Provider</label>
        <div id="pf-prov"></div>
      </div>
      <div class="filter-group" style="min-width:260px">
        <label>Modell</label>
        <div id="pf-model"></div>
      </div>
      <div class="filter-group">
        <label>Alternativ</label>
        <label class="inline"><input type="checkbox" id="pf-ma" /> MA(3)</label>
      </div>
      <div class="filter-group">
        <button id="pf-apply" class="primary">Tillämpa filter</button>
        <button id="pf-reset">Återställ</button>
      </div>
      <div class="filter-group" style="margin-left:auto">
        <button id="pf-export" class="info">Exportera CSV</button>
        <button id="refresh-performance">Uppdatera</button>
      </div>
    </div>

    <!-- KPI -->
    <div class="kpi-grid">
      <div class="kpi"><h4>Antal sessioner</h4><div class="big" id="kpi-sessions">0</div><div class="sub" id="kpi-range"></div></div>
      <div class="kpi"><h4>Medelpoäng</h4><div class="big" id="kpi-avg">–</div><div class="sub">Final Score (medel)</div></div>
      <div class="kpi"><h4>Median cykler</h4><div class="big" id="kpi-cycles">–</div><div class="sub">Debugging cycles (median)</div></div>
      <div class="kpi"><h4>Korrigeringsgrad</h4><div class="big" id="kpi-corr">–</div><div class="sub">Self/External ratio</div></div>
    </div>

    <!-- Charts -->
    <div class="chart-grid">
      <div class="chart-card">
        <h3>Final Score Over Time</h3>
        <div class="chart-container"><canvas id="score-chart"></canvas></div>
      </div>
      <div class="chart-card">
        <h3>Session Metrics (Cycles)</h3>
        <div class="chart-container"><canvas id="metrics-chart"></canvas></div>
      </div>
      <div class="chart-card">
        <h3>Sessions Per Provider</h3>
        <div class="chart-container"><canvas id="provider-chart"></canvas></div>
      </div>
      <div class="chart-card">
        <h3>Sessions Per Model</h3>
        <div class="chart-container"><canvas id="model-chart"></canvas></div>
      </div>
    </div>

    <!-- Learning DB + Sessions -->
    <div class="table-card" style="margin-top:12px">
      <h3>Learning Database (Heuristics)</h3>
      <div id="perf-learning-body">Ingen data.</div>
    </div>
    <div class="table-card" style="margin-top:12px">
      <h3>Sessions</h3>
      <div id="perf-sessions-body">Ingen data.</div>
    </div>
  </div>
</section>

<!-- Hjälpmodal -->
<div id="helpModal" class="modal" role="dialog" aria-modal="true">
  <div class="box">
    <header>
      <b>Hjälp – Arbetssekvens</b>
      <button id="helpClose" aria-label="Stäng">✕</button>
    </header>
    <main>
      <div class="small">Obligatoriskt: <b>aldrig</b> generera bilder om inte användaren uttryckligen ber om det.</div>
      <ol>
        <li><b>Skapa nästa arbete</b>:
          <ul>
            <li><b>K-MOD</b>: Max-Context Discovery (intro + candidates med content + mini-graf + STRICT RETURN_CONTRACT).</li>
            <li><b>D-MOD</b>: Deterministiskt urval (ID:n, SHA256, constraints, rules_hash + STRICT RETURN_CONTRACT).</li>
          </ul>
        </li>
        <li>Klistra in modellsvar i rutan → strikt validering och auto-select.</li>
        <li><b>Skapa uppgift</b>: genererar <i>impl_bootstrap_v1</i> med full/chunk/stub + file_map.</li>
        <li>Starta ny tom modelsession med bootstrap-JSON. Flöde: PLAN-JSON → “OK” → GEN-JSON (patch/tester).</li>
      </ol>
    </main>
    <footer><button id="helpOk" class="primary">OK</button></footer>
  </div>
</div>

<!-- Filförhandsvisning modal -->
<div id="filePreview" class="modal" role="dialog" aria-modal="true">
  <div class="box">
    <header>
      <b id="fpTitle">Förhandsgranskning</b>
      <div>
        <button id="fpCopy">Copy</button>
        <button id="fpDownload">Download</button>
        <button id="fpClose" aria-label="Stäng">✕</button>
      </div>
    </header>
    <main id="fpBody"><p>Laddar…</p></main>
  </div>
</div>

<!-- Busy overlay -->
<div id="busy" role="status" aria-live="polite">
  <div class="spinner" aria-hidden="true"></div>
  <pre id="worklog"></pre>
</div>

<script>
(function(){
  // RAW-källa för filhämtning (GitHub RAW)
  const RAW = 'https://raw.githubusercontent.com/Engrove/Engrove-Audio-Tools-2.0/main/';
  const IMAGE_EXT = ['png','jpg','jpeg','gif','webp','svg'];

  const els = {
    tree:      document.getElementById('tree'),
    selAll:    document.getElementById('selAll'),
    deselAll:  document.getElementById('deselAll'),
    selCore:   document.getElementById('selCore'),
    genContext:document.getElementById('genContext'),
    genFiles:  document.getElementById('genFiles'),
    instruction:document.getElementById('instruction'),
    out:       document.getElementById('out'),
    copy:      document.getElementById('copy'),
    download:  document.getElementById('download'),
    discBtn:   document.getElementById('discBtn'),
    implBtn:   document.getElementById('implBtn'),
    kmodFlag:  document.getElementById('kmod'),
    embed:     document.getElementById('embed'),
    banner:    document.getElementById('banner'),
    helpBtn:   document.getElementById('helpBtn'),
    helpModal: document.getElementById('helpModal'),
    helpClose: document.getElementById('helpClose'),
    helpOk:    document.getElementById('helpOk'),
    tabBtns:   document.querySelectorAll('.tabbar button[data-tab]'),
    tabs:      { builder: document.getElementById('tab-builder'), performance: document.getElementById('tab-performance') },
    fp:        document.getElementById('filePreview'),
    fpTitle:   document.getElementById('fpTitle'),
    fpBody:    document.getElementById('fpBody'),
    fpCopy:    document.getElementById('fpCopy'),
    fpDownload:document.getElementById('fpDownload'),
    fpClose:   document.getElementById('fpClose'),
    budgetKb:  document.getElementById('budgetKb'),
    compact:   document.getElementById('compact'),
    // Busy
    busy:      document.getElementById('busy'),
    worklog:   document.getElementById('worklog'),
    // Performance filters
    pf:{ from:document.getElementById('pf-from'), to:document.getElementById('pf-to'),
         provWrap:document.getElementById('pf-prov'), modelWrap:document.getElementById('pf-model'),
         ma:document.getElementById('pf-ma'), apply:document.getElementById('pf-apply'),
         reset:document.getElementById('pf-reset'), export:document.getElementById('pf-export'),
         refresh:document.getElementById('refresh-performance') },
    // KPI
    kpi:{ sessions:document.getElementById('kpi-sessions'), rng:document.getElementById('kpi-range'),
          avg:document.getElementById('kpi-avg'), cycles:document.getElementById('kpi-cycles'),
          corr:document.getElementById('kpi-corr') },
    perfLearning: document.getElementById('perf-learning-body'),
    perfSessions: document.getElementById('perf-sessions-body'),
  };

  function currentDiscMode(){
    const el = document.querySelector('input[name="discMode"]:checked');
    return el ? el.value : 'KMOD';
  }

  // State
  let ctx = null;
  let FILES = [];
  let CODE_FILES = [];
  let FILE_INFO = new Map(); // path -> {size, sha256?, lang?}

  // D-MOD: senaste kandidater och rules_hash
  let LAST_CANDIDATES = [];
  let LAST_RULES_HASH = null;

  // MUST-regler inkl. bildförbud
  const MUST_STRICT = [
    "forbid_image_generation",
    "PLAN->GEN",
    "unified-patch-if->50",
    "no-edit-nonfull",
    "list-api-contracts",
    "add-tests-run-cmds"
  ];

  const KMOD_BANNER = "MODE: K-MOD (Brainstorming/Discovery). Ingen kod. Endast JSON enligt schema och RETURN_CONTRACT.";
  const DMOD_BANNER = "MODE: D-MOD (Deterministic Discovery). Ingen kod. Endast JSON enligt return_contract.";
  const IMAGE_GUARD_BANNER = "BILDREGEL: ALDRIG generera bilder i denna session om det inte uttryckligen efterfrågas.";

  // ---------- Utils ----------
  function showBanner(msg, kind='warn'){
    els.banner.textContent = msg;
    els.banner.className = 'banner ' + (kind==='err'?'err':kind==='ok'?'ok':'');
    els.banner.style.display = 'block';
  }
  function clearBanner(){ els.banner.style.display='none'; els.banner.textContent=''; els.banner.className='banner'; }

  function escapeHtml(s){ return String(s).replace(/[&<>"']/g, m=>({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m])); }

  async function fetchText(path){
    const r = await fetch(RAW+path, {cache:'no-store'});
    if(!r.ok) throw new Error('HTTP '+r.status);
    return await r.text();
  }

  async function sha256Hex(text){
    const enc = new TextEncoder().encode(text);
    if(window.crypto && crypto.subtle && crypto.subtle.digest){
      const buf = await crypto.subtle.digest('SHA-256', enc);
      const arr = Array.from(new Uint8Array(buf));
      return arr.map(b=>b.toString(16).padStart(2,'0')).join('');
    }
    let h=0; for(let i=0;i<enc.length;i++){ h=(h*31 + enc[i])>>>0; } return h.toString(16);
  }

  function isCodeLike(p){
    const ext = (p.split('.').pop()||'').toLowerCase();
    return ['py','js','jsx','ts','tsx','vue','json','md','html','css','yml','yaml','toml'].includes(ext);
  }
  function guessLang(p){
    const e=(p.split('.').pop()||'').toLowerCase();
    if(['ts','tsx'].includes(e)) return 'ts';
    if(e==='vue') return 'vue';
    if(e==='py')  return 'py';
    if(['js','jsx'].includes(e)) return 'js';
    if(e==='md')  return 'md';
    if(e==='json')return 'json';
    if(e==='html')return 'html';
    if(e==='css') return 'css';
    return 'txt';
  }

  function flattenPaths(node, prefix='', out=[]){
    Object.keys(node).sort().forEach(k=>{
      const it = node[k], p = prefix ? `${prefix}/${k}` : k;
      if(it.type==='file'){
        out.push(it.path || p);
        FILE_INFO.set(it.path || p, {
          size: it.size || null,
          sha256: it.sha256 || null,
          lang: guessLang(it.path || p)
        });
      }else{
        flattenPaths(it, p, out);
      }
    });
    return out;
  }

  // ---------- Busy overlay ----------
  function logw(msg){ const t=new Date().toLocaleTimeString(); els.worklog.textContent += `[${t}] ${msg}\n`; els.worklog.scrollTop = els.worklog.scrollHeight; }
  async function withBusy(label, fn){
    els.worklog.textContent = '';
    els.busy.style.display = 'flex';
    logw(label+' start');
    try{ const r = await fn(); logw(label+' klar'); return r; }
    finally{ setTimeout(()=> els.busy.style.display='none', 150); }
  }

  // ---------- Heuristik ----------
  function inferRole(path){
    if(path==='package.json') return 'Scripts & beroenden; kör-/bygg-/lint-/testkommandon';
    if(path==='vite.config.js') return 'Byggkonfiguration (Vite)';
    if(path==='index.html') return 'HTML entry-point';
    if(/src\/(app\/)?main\.(js|ts)$/.test(path)) return 'App-bootstrap/montering';
    if(/^src\/app\/router\.(js|ts)$/.test(path)) return 'Routerdefinition';
    if(/^src\/pages\//.test(path) && path.endsWith('.vue')) return 'Vykomponent (sida)';
    if(/^src\/features\//.test(path) && path.endsWith('.vue')) return 'UI-funktionskomponent';
    if(/^src\/shared\/ui\//.test(path) && path.endsWith('.vue')) return 'Återanvändbar UI-baskomponent';
    if(/^src\/entities\/[^/]+\/model\//.test(path)) return 'State/store-modul för entitet';
    if(/^src\/entities\/[^/]+\/lib\//.test(path)) return 'Domänlogik/utilities för entitet';
    if(/^scripts\/wrap_json_in_html\.py$/.test(path)) return 'Genererar Builder-HTML + promptlogik';
    if(/^scripts\/generate_full_context\.py$/.test(path)) return 'Bygger context.json från repo';
    if(/^docs\/ai_protocols\//.test(path)) return 'AI-protokoll och riktlinjer';
    if(/^docs\//.test(path) && path.endsWith('.md')) return 'Projekt-/design-dokumentation';
    if(path.endsWith('.py')) return 'Bygg-/verktygsskript';
    if(path.endsWith('.vue')) return 'Vue-komponent';
    if(path.endsWith('.js')||path.endsWith('.ts')) return 'JS/TS-källkod';
    if(path.endsWith('.md')) return 'Dokumentation';
    if(path.endsWith('.json')) return 'Konfiguration/data';
    return 'Kod-/textfil';
  }

  function priorityScore(path, task){
    let score = 0;
    const low = path.toLowerCase();
    if(task){
      const first = (task.split(/\s+/)[0]||'').toLowerCase();
      if(first && low.includes(first)) score += 5;
    }
    if(['package.json','vite.config.js','index.html'].includes(path)) score += 5;
    if(/src\/(app\/)?main\.(js|ts)$/.test(path)) score += 5;
    if(/^docs\/ai_protocols\//.test(path) || /\.spec\./.test(path) || /\.test\./.test(path)) score += 3;
    const meta = FILE_INFO.get(path)||{};
    const sz = meta.size || 0;
    if(sz>100*1024) score -= Math.floor((sz-100*1024)/(50*1024));
    return score;
  }

  function isCriticalForTask(path, task){
    const t=(task||'').toLowerCase();
    const p=path.toLowerCase();
    const critSub = [
      'comparison','compare','data-explorer','explorer',
      'filters.js','transformer.js','comparisonstore','comparisonmodal.vue',
      'dataexplorerpage.vue','explorerstore.js','state.js'
    ];
    if(critSub.some(k=>p.includes(k))) return true;
    if(['package.json','vite.config.js','index.html','src/app/main.js','src/main.js','src/app/router.js'].includes(path)) return true;
    const first = (t.split(/\s+/)[0]||'').replace(/[^a-z0-9]/g,'');
    if(first && p.includes(first)) return true;
    return false;
  }

  // ---------- Tree UI ----------
  function renderTree(node, parent, base=''){
    const ul = document.createElement('ul');
    const keys = Object.keys(node).sort((a,b)=>{
      const aF = node[a].type==='file', bF = node[b].type==='file';
      if(aF && !bF) return 1;
      if(!aF && bF) return -1;
      return a.localeCompare(b);
    });
    keys.forEach(k=>{
      const it = node[k];
      const p = base ? `${base}/${k}` : k;
      const li = document.createElement('li');

      const label = document.createElement('label');
      label.className = 'fileline';

      const cb = document.createElement('input');
      cb.type='checkbox'; cb.dataset.path = p;
      label.appendChild(cb);

      const icon = document.createElement('span');
      icon.textContent = (it.type==='file'
        ? (IMAGE_EXT.includes((k.split('.').pop()||'').toLowerCase())?'🖼️':'📄')
        : '📁');
      label.appendChild(icon);

      const txt = document.createElement('a'); txt.href='#'; txt.textContent = ' '+k; txt.dataset.path=p;
      label.appendChild(txt);

      li.appendChild(label);
      if(it.type==='file'){
        txt.addEventListener('click', async (e)=>{
          e.preventDefault(); showFilePreview(p);
        });
      }else{
        const toggle = document.createElement('span'); toggle.className='toggle'; toggle.textContent='►';
        li.insertBefore(toggle, label);
        const sub = renderTree(it, li, p); sub.style.display='none'; li.appendChild(sub);
        toggle.addEventListener('click', ()=>{
          const vis = sub.style.display==='none'; sub.style.display = vis?'block':'none';
          toggle.textContent = vis ? '▼':'►';
        });
      }

      // Kaskad- och tri-state-logik
      cb.addEventListener('change', ()=>{
        // nedåt
        const sub = li.querySelector(':scope > ul');
        if(sub){
          sub.querySelectorAll('input[type="checkbox"]').forEach(x=>{ x.checked = cb.checked; });
        }
        // uppåt
        updateParents(li);
      });

      ul.appendChild(li);
    });
    parent.appendChild(ul);
    return ul;
  }

  function updateParents(li){
    let p = li.parentElement && li.parentElement.closest('li');
    while(p){
      const kids = p.querySelectorAll(':scope > ul input[type="checkbox"]');
      const parentCb = p.querySelector(':scope > label input[type="checkbox"]');
      const total = kids.length, on = Array.from(kids).filter(c=>c.checked).length;
      if(parentCb){
        parentCb.indeterminate = on>0 && on<total;
        parentCb.checked = on===total;
      }
      p = p.parentElement && p.parentElement.closest('li');
    }
  }
  function recomputeAllParents(){
    document.querySelectorAll('#tree li').forEach(li => updateParents(li));
  }

  async function showFilePreview(p){
    els.fpTitle.textContent = p;
    els.fpBody.textContent = 'Laddar…';
    els.fp.classList.add('show');
    const ext=(p.split('.').pop()||'').toLowerCase();
    if(IMAGE_EXT.includes(ext)){
      els.fpBody.innerHTML = `<img src="${RAW+p}" alt="${escapeHtml(p)}">`;
      els.fpCopy.disabled=true;
      els.fpDownload.onclick = ()=>{ const a=document.createElement('a'); a.href=RAW+p; a.download=p.split('/').pop(); document.body.appendChild(a); a.click(); a.remove(); };
    }else{
      try{
        const t = await fetchText(p);
        els.fpBody.innerHTML = `<pre style="white-space:pre-wrap">${escapeHtml(t)}</pre>`;
        els.fpCopy.disabled=false;
        els.fpCopy.onclick = ()=> navigator.clipboard.writeText(t);
        els.fpDownload.onclick = ()=>{
          const blob = new Blob([t], {type:'text/plain'});
          const url = URL.createObjectURL(blob);
          const a=document.createElement('a'); a.href=url; a.download=p.split('/').pop(); document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
        };
      }catch(_){ els.fpBody.textContent = 'Kunde inte läsa fil.'; }
    }
  }

  function openParentsFor(path){
    const cb = els.tree.querySelector(`input[data-path="${CSS.escape(path)}"]`);
    if(!cb) return;
    let li = cb.closest('li');
    while(li){
      const parent = li.parentElement.closest('li');
      if(parent){
        const sub = parent.querySelector(':scope > ul');
        const toggle = parent.querySelector(':scope > .toggle');
        if(sub && toggle){ sub.style.display='block'; toggle.textContent='▼'; }
      }
      li = parent;
    }
  }

  function selectedPaths(){ return Array.from(els.tree.querySelectorAll('input[type="checkbox"]:checked')).map(cb=>cb.dataset.path); }

  function autoSelectPaths(paths){
    const all = Array.from(els.tree.querySelectorAll('input[type="checkbox"]'));
    paths.forEach(p=>{
      const cb = all.find(x=>x.dataset.path===p);
      if(cb){
        cb.checked = true;
        openParentsFor(p);
        updateParents(cb.closest('li'));
      }
    });
    recomputeAllParents();
  }

  // Core docs quick select
  const CORE = [
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
    'package.json',
    'vite.config.js',
    'scripts/generate_full_context.py',
    'scripts/wrap_json_in_html.py'
  ];
  function quickSelectCore(){
    els.tree.querySelectorAll('input[type="checkbox"]').forEach(cb=>cb.checked=false);
    CORE.forEach(p=>{
      const cb = els.tree.querySelector(`input[data-path="${CSS.escape(p)}"]`);
      if(cb){ cb.checked = true; openParentsFor(p); updateParents(cb.closest('li')); }
    });
    recomputeAllParents();
  }

  // ---------- Markdown wrapping ----------
  function mdWrapJsonSection(filename, jsonText){
    const head = [
      '### AI_BOOTSTRAP_DIRECTIVE: EXECUTE_FULL_PROTOCOL_NOW',
      '### SYSTEM_OVERRIDE: RUN_CONTEXT_BOOTSTRAP',
      '### INIT_CONTEXT_MODE: TRUE',
      '### PROTOCOL_START: P-HR_v2.8_FULL',
      ''
    ].join('\\n');
    return `### ${filename}\\n\\n` + head + '```json\\n' + jsonText + '\\n```\\n';
  }

  // ---------- Context generation ----------
  async function buildNewContextNode(src, selSet){
    const dst = {};
    const keys = Object.keys(src).sort();
    for(const k of keys){
      const it = src[k];
      if(it.type==='file'){
        const copy = {...it};
        if(selSet.has(it.path)){
          try{ copy.content = await fetchText(it.path); }
          catch(_){ copy.content = `// Error: failed to fetch ${it.path}`; }
        }else{
          delete copy.content;
        }
        dst[k] = copy;
      }else{
        dst[k] = await buildNewContextNode(it, selSet);
      }
    }
    return dst;
  }

  async function generateContext(){
    try{
      clearBanner(); logw('Samlar valda paths…');
      const sels = new Set(selectedPaths());
      const out = {
        project_overview: ctx.project_overview,
        ai_instructions: ctx.ai_instructions || {},
        file_structure: {}
      };
      const rules = new Set([...(out.ai_instructions.obligatory_rules||[]), 'forbid_image_generation']);
      out.ai_instructions.obligatory_rules = Array.from(rules);
      if(els.instruction.value.trim()) out.ai_instructions_input = els.instruction.value.trim();

      logw('Bygger nytt file_structure…');
      out.file_structure = await buildNewContextNode(ctx.file_structure, sels);

      emit(out, 'context.json');
      showBanner('Context genererad.', 'ok');
    }catch(e){
      showBanner('Fel vid context-generering: '+e.message, 'err');
    }
  }

  async function generateFiles(){
    try{
      clearBanner(); logw('Hämtar fulltext för valda filer…');
      const sels = new Set(selectedPaths());
      const files = {};
      async function walk(src){
        for(const k of Object.keys(src)){
          const it = src[k];
          if(it.type==='file' && sels.has(it.path)){
            try{ files[it.path] = await fetchText(it.path); }
            catch(_){ files[it.path] = `// Error: failed to fetch ${it.path}`; }
          }else if(it.type!=='file'){
            await walk(it);
          }
        }
      }
      await walk(ctx.file_structure);
      const payload = { obligatory_rules:['forbid_image_generation'], files };
      emit(payload, 'files_payload.json');
      showBanner('Filer genererade.', 'ok');
    }catch(e){
      showBanner('Fel vid file-generering: '+e.message, 'err');
    }
  }

  function emit(obj, nameHint='context.json'){
    const text = els.compact.checked ? JSON.stringify(obj) : JSON.stringify(obj, null, 2);
    els.out.textContent = mdWrapJsonSection(nameHint, text);
    els.copy.disabled = els.download.disabled = false;
  }

  // ---------- K-MOD / D-MOD (oförändrat i sak, kortat här för tydlighet) ----------
  const DEEP = { CAP_BYTES: 2_000_000, MAX_FILES: 180, HEAD_BYTES: 20_000, FULL_SIZE_LIMIT: 120_000 };

  async function summarizeForDiscoveryDeep(path, task){
    const meta = FILE_INFO.get(path) || {};
    let content = '';
    try { content = await fetchText(path); } catch(_){ content=''; }
    const lang = guessLang(path);
    const role = inferRole(path);
    const size = meta.size || (content ? new Blob([content]).size : 0);
    const importance = priorityScore(path, task);
    const takeFull = size>0 && (size <= DEEP.FULL_SIZE_LIMIT || isCriticalForTask(path, task));
    const head = takeFull ? content : content.slice(0, DEEP.HEAD_BYTES);

    const lines = head.split(/\r?\n/);
    const anchors=[];
    for(let i=0;i<lines.length && anchors.length<12;i++){
      const L=lines[i];
      if(/^\s*(export|def|class|function|const|let|props|emits|interface|type|setup\(|data:|methods:)\b/.test(L) || /TODO|FIXME|@/.test(L)){
        anchors.push({line:i+1, text:L.trim().slice(0,160)});
      }
    }
    const imports=[], exports=[];
    head.split(/\r?\n/).forEach(L=>{
      let m;
      if((m=L.match(/^\s*import\s+.*?from\s+['"]([^'"]+)['"]/))) imports.push(m[1]);
      if((m=L.match(/^\s*export\s+(?:default\s+)?(?:function|class|const|let|var|interface|type)\s+([A-Za-z0-9_]+)/))) exports.push(m[1]);
      if((m=L.match(/module\.exports\s*=\s*([A-Za-z0-9_]+)/))) exports.push(m[1]);
    });
    const key_symbols=[];
    head.split(/\r?\n/).forEach(L=>{
      let m;
      if((m=L.match(/^\s*(?:export\s+)?(?:function|class)\s+([A-Za-z0-9_]+)/))) key_symbols.push(m[1]);
      if((m=L.match(/^\s*const\s+([A-Za-z0-9_]+)\s*=\s*(?:\(.*\)\s*=>|function)/))) key_symbols.push(m[1]);
      if((m=L.match(/^\s*def\s+([A-Za-z0-9_]+)\s*\(/))) key_symbols.push(m[1]);
    });

    return {
      path, role, lang,
      size_bytes: size || null,
      sha256: (FILE_INFO.get(path)||{}).sha256 || null,
      importance,
      anchors,
      key_symbols: Array.from(new Set(key_symbols)).slice(0,20),
      imports: Array.from(new Set(imports)).slice(0,20),
      exports: Array.from(new Set(exports)).slice(0,20),
      embed: takeFull ? "full" : "chunk",
      content: head
    };
  }

  async function buildProjectCapsule(){
    const has = (p)=> FILES.includes(p);
    let name='Engrove Audio Tools';
    let purpose='Webbapp med AI Context Builder (Vue/Vite) + protokollstyrt AI-flöde';
    const stack = [];
    if(has('vite.config.js')) stack.push('Vite');
    if(FILES.some(p=>p.endsWith('.vue'))) stack.push('Vue 3');
    if(FILES.some(p=>p.endsWith('.ts'))) stack.push('TypeScript'); else stack.push('JavaScript');
    if(FILES.some(p=>p.startsWith('scripts/') && p.endsWith('.py'))) stack.push('Python-scripts');

    const entry_points = [];
    ['index.html','src/app/main.js','src/main.js','src/app/router.js'].forEach(p=>{ if(has(p)) entry_points.push(p); });

    let run_cmd='npm run dev', build_cmd='npm run build', test_cmd='saknas', lint_cmd='saknas';
    try{
      if(has('package.json')){
        const txt = await fetchText('package.json');
        const pj = JSON.parse(txt);
        if(pj.name) name = pj.name;
        if(pj.scripts){
          if(pj.scripts.dev)   run_cmd  = 'npm run dev';
          if(pj.scripts.build) build_cmd= 'npm run build';
          if(pj.scripts.test)  test_cmd = 'npm test';
          if(pj.scripts.lint)  lint_cmd = 'npm run lint';
        }
      }
    }catch(_){}

    const dirs = Array.from(new Set(FILES.map(p=>p.split('/')[0]))).filter(d=>!d.startsWith('.')).slice(0,10);
    const invariants = [
      "PLAN→GEN (PLAN-JSON → OK → GEN-JSON)",
      "Unified patch (>50 rader) när relevant",
      "Ändra ej filer med is_content_full=false",
      "ALDRIG generera bilder utan uttrycklig begäran"
    ];

    return { name, purpose, stack, entry_points, run_cmd, build_cmd, test_cmd, lint_cmd, invariants, dirs };
  }

  async function buildProjectIntro(task){
    const capsule = await buildProjectCapsule();
    let pkg=null, scripts={}
    try{ const t = await fetchText('package.json'); pkg = JSON.parse(t); scripts = pkg.scripts || {}; }catch(_){}
    let routes=[];
    for(const r of ['src/app/router.js','src/app/router.ts']){
      if(FILES.includes(r)){
        try{ const t = await fetchText(r); routes = Array.from(t.matchAll(/path:\s*['"]([^'"]+)['"]/g)).map(m=>m[1]); break; }
        catch(_){}
      }
    }
    let glossary_head='';
    if(FILES.includes('docs/glossary.md')){
      try{ glossary_head = (await fetchText('docs/glossary.md')).slice(0, 8000); }catch(_){}
    }
    return {
      name: capsule.name,
      purpose: capsule.purpose,
      stack: capsule.stack,
      goal_for_this_session: task,
      invariants: capsule.invariants,
      package_scripts: scripts,
      routes, glossary_head
    };
  }

  async function buildFileMapMiniFromCandidates(cands){
    const pathToId = new Map(cands.map(c=>[c.path, c.id]));
    const nodes = cands.map(c=>({ id: c.id, path: c.path, group: (/^src\//.test(c.path) ? 'src' : /^docs\//.test(c.path) ? 'docs' : /^scripts\//.test(c.path) ? 'scripts' : 'other'), role: inferRole(c.path) }));
    const edges = [];
    for(const c of cands){
      const base = c.path.split('/').slice(0,-1).join('/');
      (c.imports||[]).forEach(im=>{
        if(im.startsWith('./')||im.startsWith('../')){
          const abs = base + '/' + im;
          const guesses = [abs, abs+'.js', abs+'.ts', abs+'.vue', abs.replace(/\/index$/,'/index.js'), abs.replace(/\/index$/,'/index.ts')];
          const to = guesses.find(g=> pathToId.has(g));
          if(to){ edges.push({from:c.id, to:pathToId.get(to), rel:'imports'}); }
        }
      });
    }
    return { nodes, edges: edges.slice(0, 800) };
  }

  function returnContractKMOD(){
    return {
      KMOD:{
        type:"object",
        required:["protocol_id","mode","selected_files"],
        properties:{
          protocol_id:{ const:"discovery_v2" },
          mode:{ const:"K-MOD" },
          selected_files:{
            type:"array",
            minItems:2,
            items:{
              type:"object",
              required:["path","embed","why"],
              properties:{
                path:{ type:"string" },
                embed:{ enum:["full","chunk","stub"] },
                why:{ type:"string", maxLength:200 }
              },
              additionalProperties:false
            }
          }
        },
        additionalProperties:true
      }
    };
  }

  async function buildDiscoveryPromptKMOD(){
    const task = getTask();
    const intro = await buildProjectIntro(task);
    const ranked = CODE_FILES.slice().sort((a,b)=> priorityScore(b, task) - priorityScore(a, task));
    const picked=[]; let used=0; let nextId=1;
    for(const p of ranked){
      if(picked.length>=DEEP.MAX_FILES) break;
      const s = await summarizeForDiscoveryDeep(p, task);
      const cost = new Blob([s.content]).size + 700;
      if(used + cost > DEEP.CAP_BYTES) continue;
      used += cost; picked.push({ id: nextId++, ...s });
    }
    LAST_CANDIDATES = picked.slice();
    const FM = await buildFileMapMiniFromCandidates(picked);

    const schema = {
      protocol_id:"discovery_v2",
      psv:["rules_rehearsed","risk_scan"],
      mode:"K-MOD",
      obligatory_rules:["forbid_image_generation"],
      task,
      project_intro:{},
      candidate_files:[],
      file_map_mini:{},
      selected_files:[],
      requires_chunks:[],
      api_contracts_touched:[],
      risks:[],
      test_plan:[],
      done_when:["tests_green","lint_ok","types_ok"],
      _note:"Välj endast objekt från candidate_files. Sätt embed={'full','chunk','stub'}. Motivera kort varje val."
    };

    const prompt = [
      "SESSION: PLANERA NÄSTA ARBETE (Discovery)",
      KMOD_BANNER,
      IMAGE_GUARD_BANNER,
      "KRAV: Svara ENBART med giltig JSON enligt schema och RETURN_CONTRACT. Ingen kod.",
      "- Välj ENDAST objekt från CANDIDATE_FILES.",
      "- Inga placeholders eller påhittade vägar.",
      "- Minst 2 objekt i 'selected_files'.",
      "- 'embed' ∈ {'full','chunk','stub'}.",
      "SCHEMA:",
      JSON.stringify(schema, null, 2),
      "RETURN_CONTRACT:",
      JSON.stringify(returnContractKMOD(), null, 2),
      "PROJECT_INTRO:",
      JSON.stringify(intro, null, 2),
      "CANDIDATE_FILES:",
      JSON.stringify(picked, null, 2),
      "FILE_MAP_MINI:",
      JSON.stringify(FM, null, 2),
      "KONTEXT-RÅD:",
      "- Prioritera målkomponenter/kontrakt = embed:'full'.",
      "- Övrigt = 'chunk' (content inkluderad) eller 'stub' om endast metadata krävs.",
      "- Fyll 'selected_files' med objekt (inkl. path, embed, why)."
    ].join("\n");

    return prompt;
  }

  // ---------- D-MOD ----------
  const DM = {
    MAX_FILES: 180,
    CAP_BYTES: 2_000_000,
    HEAD_BYTES: 20_000,
    FULL_SIZE_LIMIT: 120_000,
    SELECTION: { only_ids: true, min: 2, max: 12, allow_paths: ["src/**","docs/**","scripts/**"], deny_paths: ["infra/prod/**"] }
  };

  function globToRegex(glob){
    return new RegExp('^'+glob.split('**').join('@@').replace(/[.+^${}()|[\]\\]/g,'\\$&').split('*').join('[^/]*').split('@@').join('.*')+'$');
  }
  function pathAllowed(p){
    const allow = DM.SELECTION.allow_paths.map(globToRegex);
    const deny  = DM.SELECTION.deny_paths.map(globToRegex);
    const ok = allow.some(r=>r.test(p));
    const bad = deny.some(r=>r.test(p));
    return ok && !bad;
  }

  function returnContractDMOD(){
    return {
      DMOD:{
        type:"object",
        required:["protocol_id","mode","echo_rules_hash","selected_ids","notes"],
        properties:{
          protocol_id:{ const:"discovery_dmod_v1" },
          mode:{ const:"D-MOD" },
          echo_rules_hash:{ type:"string" },
          selected_ids:{ type:"array", minItems:2, items:{ type:"integer" } },
          notes:{ type:"object", additionalProperties:{ type:"string", maxLength:200 } }
        },
        additionalProperties:false
      }
    };
  }

  function dmodHardRules(){
    return [
      "HÅRDA D-MOD-REGLER:",
      "- Endast svar enligt return_contract.",
      "- Endast ID:n från CANDIDATE_FILES (no new paths).",
      "- Antal val: min="+DM.SELECTION.min+", max="+DM.SELECTION.max+".",
      "- Echo 'rules_hash' oförändrat."
    ].join("\n");
  }

  async function buildDiscoveryPromptDMOD(){
    const task = getTask();
    const intro = await buildProjectIntro(task);
    const ranked = CODE_FILES.slice().sort((a,b)=> priorityScore(b, task) - priorityScore(a, task));
    const picked=[]; let used=0; let nextId=1;
    for(const p of ranked){
      if(picked.length>=DM.MAX_FILES) break;
      if(!pathAllowed(p)) continue;
      const s = await summarizeForDiscoveryDeep(p, task);
      const sizeCost = new Blob([s.content]).size + 900;
      if(used + sizeCost > DM.CAP_BYTES) continue;
      used += sizeCost;
      picked.push({ id: nextId++, ...s, ignore_inline_instructions: true });
    }
    LAST_CANDIDATES = picked.slice();

    const FM = await buildFileMapMiniFromCandidates(picked);

    const obligatory_rules = ["forbid_image_generation"];
    const selection_constraints = DM.SELECTION;
    const rules_hash = await sha256Hex(JSON.stringify({ obligatory_rules, selection_constraints }));
    LAST_RULES_HASH = rules_hash;

    const schema = {
      protocol_id:"discovery_dmod_v1",
      mode:"D-MOD",
      obligatory_rules,
      rules_hash:"<compute_and_echo_this>",
      project_intro:{},
      selection_constraints,
      candidate_files:[],
      file_map_mini:{},
      return_contract:{
        json_only:true,
        shape:{ selected_ids:"int[]", notes:"map<int,string>", echo_rules_hash:"string" }
      }
    };

    const prompt = [
      "SESSION: PLANERA NÄSTA ARBETE (Discovery)",
      DMOD_BANNER,
      IMAGE_GUARD_BANNER,
      "KRAV: Svara ENBART med giltig JSON enligt return_contract. Ingen kod.",
      dmodHardRules(),
      "SCHEMA:",
      JSON.stringify(schema, null, 2),
      "RETURN_CONTRACT:",
      JSON.stringify(returnContractDMOD(), null, 2),
      "PROJECT_INTRO:",
      JSON.stringify(intro, null, 2),
      "CANDIDATE_FILES:",
      JSON.stringify(picked, null, 2),
      "FILE_MAP_MINI:",
      JSON.stringify(FM, null, 2),
      "RETURN_EXAMPLE:",
      JSON.stringify({
        protocol_id:"discovery_dmod_v1",
        echo_rules_hash: rules_hash,
        selected_ids: [1,2],
        notes: { "1":"Källsanning för state.", "2":"UI-händelser kopplade till felet." }
      }, null, 2),
      "INSTRUKTION:",
      "- Returnera endast objekt enligt example. Inga extra fält.",
      "- 'echo_rules_hash' måste exakt matcha 'rules_hash'."
    ].join("\n");

    return prompt.replace('"rules_hash":"<compute_and_echo_this>"', '"rules_hash":"'+rules_hash+'"');
  }

  // ---------- Implementation bootstrap ----------
  function toOpenAI(systemText, userJson){
    return {
      provider:"openai",
      model:"gpt-5",
      auto_start:true,
      messages:[
        {role:"system", content:systemText},
        {role:"user",   content:userJson}
      ]
    };
  }
  function toGemini(systemText, userJson){
    return {
      provider:"google",
      model:"gemini-2.5-pro",
      auto_start:true,
      system_instruction:systemText,
      contents:[{role:"user", parts:[{text:userJson}]}]
    };
  }
  function toProviderEnvelope(systemRules, userJsonPretty){
    const sys = Array.isArray(systemRules) ? systemRules.join("\\n") : String(systemRules||'');
    const user = userJsonPretty;
    return (document.querySelector('input[name="prov"][value="gemini"]').checked)
      ? JSON.stringify(toGemini(sys, user), null, els.compact.checked?0:2)
      : JSON.stringify(toOpenAI(sys, user), null, els.compact.checked?0:2);
  }

  function getTask(){
    const t = els.instruction.value.trim();
    return (t && (()=>{ try{ JSON.parse(t); return false; }catch(_){ return true; } })() && t.length<=400)
      ? t
      : "Beskriv kort mål i en mening.";
  }

  function bytes(s){ return new Blob([s]).size; }

  function summarizeNonFull(path, content){
    const lang = guessLang(path);
    const size = (FILE_INFO.get(path)||{}).size || (content?bytes(content):null);
    const lines = (content||'').split(/\r?\n/);
    const anchors = [];
    for(let i=0;i<lines.length && anchors.length<5;i++){
      const L = lines[i];
      if(/^\s*(export|def|class|function|const|let|props|emits|interface|type|data:|methods:|setup\(|mounted\(|created\()/.test(L) || /TODO|FIXME|@/.test(L)){
        anchors.push({line: i+1, text: L.trim().slice(0,120)});
      }
    }
    const imports=[], exports=[];
    (content||'').split(/\r?\n/).forEach((L)=>{
      let m;
      if((m=L.match(/^\s*import\s+.*?from\s+['"]([^'"]+)['"]/))) imports.push(m[1]);
      if((m=L.match(/^\s*export\s+(?:default\s+)?(?:function|class|const|let|var|interface|type)\s+([A-Za-z0-9_]+)/))) exports.push(m[1]);
      if((m=L.match(/module\.exports\s*=\s*([A-Za-z0-9_]+)/))) exports.push(m[1]);
    });
    const key_symbols = [];
    (content||'').split(/\r?\n/).forEach(L=>{
      let m;
      if((m=L.match(/^\s*(?:export\s+)?(?:function|class)\s+([A-Za-z0-9_]+)/))) key_symbols.push(m[1]);
      if((m=L.match(/^\s*const\s+([A-Za-z0-9_]+)\s*=\s*(?:\(.*\)\s*=>|function)/))) key_symbols.push(m[1]);
      if((m=L.match(/^\s*def\s+([A-Za-z0-9_]+)\s*\(/))) key_symbols.push(m[1]);
    });
    const role = inferRole(path);
    const sha = (FILE_INFO.get(path)||{}).sha256 || null;
    const loc = (content||'').split(/\r?\n/).length || null;

    return {
      path, lang, size_bytes: size || null,
      role,
      key_symbols: Array.from(new Set(key_symbols)).slice(0,12),
      imports_exports: { imports: imports.slice(0,12), exports: exports.slice(0,12) },
      call_graph_outline: [],
      data_flow: [],
      invariants: [],
      known_issues: [],
      change_impact: "Risk för regress vid felaktiga kontrakt.",
      test_hooks: [],
      anchor_lines: anchors,
      sha256: sha,
      loc: loc
    };
  }

  async function buildFileMap(nodesList){
    const idByPath = new Map();
    const nodes = [];
    nodesList.forEach((n, idx)=>{
      const id = idx+1; idByPath.set(n.path, id);
      nodes.push({
        id, path: n.path, lang: guessLang(n.path),
        role: inferRole(n.path),
        is_content_full: !!n.is_content_full,
        sha256: (FILE_INFO.get(n.path)||{}).sha256 || null,
        size_bytes: (FILE_INFO.get(n.path)||{}).size || null,
        group: (/^src\//.test(n.path) ? 'src' : /^docs\//.test(n.path) ? 'docs' : /^scripts\//.test(n.path) ? 'scripts' : 'other')
      });
    });

    const edges = [];
    for(const n of nodesList){
      const content = n.content || '';
      const fromId = idByPath.get(n.path);
      if(!fromId) continue;
      const base = n.path.split('/').slice(0,-1).join('/');

      content.split(/\r?\n/).forEach((L, i)=>{
        const m=L.match(/^\s*import\s+.*?from\s+['"]([^'"]+)['"]/);
        if(m){
          let to = m[1];
          if(to.startsWith('./') || to.startsWith('../')){
            const candList = [to, to+'.js', to+'.ts', to+'.vue'].map(x=> base+'/'+x);
            const cand = candList.find(p=> idByPath.has(p));
            if(cand) edges.push({from: fromId, to: idByPath.get(cand), rel: 'imports', anchors:[{path:n.path,line:i+1}]});
          }
        }
      });
    }

    const views = {
      module_graph: { root_ids: nodes.filter(n=>/main\.(js|ts)$/.test(n.path)).map(n=>n.id), edge_types: ["imports","requires"] },
      runtime_flow: { sequence: nodes.map(n=>n.id).slice(0,12) }
    };
    const metrics = {
      degree_top: nodes.map(n=>({id:n.id,deg: edges.filter(e=>e.from===n.id||e.to===n.id).length})).sort((a,b)=>b.deg-a.deg).slice(0,8)
    };
    return {
      budget: { target_bytes: Number(els.budgetKb.value)*1000, used_bytes: 0, max_nodes: 400, max_edges: 1200 },
      nodes, edges, views, metrics
    };
  }

  async function buildImplBootstrap(){
    const task = getTask();
    const targetBytes = Number(els.budgetKb.value)*1000;
    const sel = selectedPaths();
    if(sel.length===0){ throw new Error('Välj minst 1 fil.'); }

    const mustFull = new Set(sel);
    if(FILES.includes('package.json')) mustFull.add('package.json');
    const entry = ['src/app/main.js','src/main.js','index.html'].filter(p=>FILES.includes(p));
    if(entry[0]) mustFull.add(entry[0]);

    const sorted = Array.from(new Set([...mustFull, ...sel])).sort((a,b)=> priorityScore(b, task)-priorityScore(a, task));
    const filesOut = [];
    let used = 0;

    for(const p of sorted){
      const meta = FILE_INFO.get(p) || {};
      const size = meta.size || 0;
      const lang = guessLang(p);
      if(used + size <= targetBytes || mustFull.has(p)){
        let content='';
        try{ content = await fetchText(p); }catch(_){ content='// Failed to fetch'; }
        filesOut.push({
          path: p, lang, size_bytes: size||bytes(content)||null, role: inferRole(p),
          is_content_full: true, embed: "full", content
        });
        used += bytes(content);
      }else{
        let content='';
        try{ content = await fetchText(p); }catch(_){ content=''; }
        const headLimit = Math.min(4000, Math.max(2000, targetBytes*0.01|0));
        const chunk = content.slice(0, headLimit);
        const summary = summarizeNonFull(p, content);
        summary.embed = "chunk";
        summary.is_content_full = false;
        summary.chunk_spec = `head:${headLimit}`;
        summary.content = chunk;
        filesOut.push(summary);
        used += bytes(chunk) + bytes(JSON.stringify(summary, null, 0)) - bytes(JSON.stringify({content:''}, null, 0));
      }
      if(used>=targetBytes) break;
    }

    for(const p of sel){
      if(!filesOut.find(x=>x.path===p)){
        let content='';
        try{ content = await fetchText(p); }catch(_){ content=''; }
        const stub = summarizeNonFull(p, content);
        stub.embed = "stub";
        stub.is_content_full = false;
        filesOut.push(stub);
        used += bytes(JSON.stringify(stub));
        if(used>=targetBytes) break;
      }
    }

    const nodesList = filesOut.map(x=>({path:x.path, is_content_full: !!x.is_content_full, content: x.content||''}));
    const fMap = await buildFileMap(nodesList);
    const capsule = await buildProjectCapsule();

    const bootstrap = {
      protocol_id: "impl_bootstrap_v1",
      task,
      obligatory_rules: MUST_STRICT,
      budget: { target_bytes: targetBytes, used_bytes: used, policy: "full_by_priority_then_chunk_then_stub" },
      project_capsule: capsule,
      files: filesOut,
      file_map: fMap,
      api_contracts_touched: [],
      test_plan: [
        "Unit: kritiska render/logic paths",
        "E2E: användarflöde relaterat till uppgiften",
        "A11y: ARIA/fokus",
        "Property: idempotens där relevant"
      ],
      done_when: ["tests_green","lint_ok","types_ok"],
      response_contract: { phase: "PLAN", return: ["plan_json_only"], next_phase_on: "OK" }
    };

    const userJsonPretty = els.compact.checked ? JSON.stringify(bootstrap) : JSON.stringify(bootstrap, null, 2);
    const providerWrap = toProviderEnvelope(MUST_STRICT, userJsonPretty);

    // Markdown-sektioner (separata, giltiga)
    const md = mdWrapJsonSection('impl_bootstrap_v1.json', userJsonPretty)
            + "\\n"
            + mdWrapJsonSection('provider_envelope.json', providerWrap);

    els.out.textContent = md;
    els.copy.disabled = els.download.disabled = false;
    showBanner(`Bootstrap-JSON klar. Bytes: ${used}/${targetBytes}.`, 'ok');
  }

  // ---------- Tabs ----------
  document.querySelectorAll('.tabbar button[data-tab]').forEach(btn=>{
    btn.addEventListener('click', ()=>{
      const tab = btn.dataset.tab;
      document.querySelectorAll('.tabbar button[data-tab]').forEach(b=>b.classList.remove('primary'));
      btn.classList.add('primary');
      Object.keys(els.tabs).forEach(k=> els.tabs[k].classList.toggle('active', k===tab));
      if(tab==='performance' && ctx){ renderPerformanceDashboard(); }
    });
  });

  // Knappkopplingar (med busy-wrapper)
  els.selAll.onclick = ()=>{ els.tree.querySelectorAll('input[type="checkbox"]').forEach(cb=>cb.checked=true); recomputeAllParents(); };
  els.deselAll.onclick = ()=>{ els.tree.querySelectorAll('input[type="checkbox"]').forEach(cb=>cb.checked=false); recomputeAllParents(); };
  els.selCore.onclick = quickSelectCore;
  els.genContext.onclick = ()=> withBusy('Generate Context', generateContext);
  els.genFiles.onclick   = ()=> withBusy('Generate Files',   generateFiles);

  els.copy.onclick = ()=>{ navigator.clipboard.writeText(els.out.textContent); showBanner('Kopierat.', 'ok'); };
  els.download.onclick = ()=>{
    const blob = new Blob([els.out.textContent], {type:'text/markdown'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href=url; a.download='context_bundle_'+new Date().toISOString().slice(0,10)+'.md';
    document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
  };

  // Discovery
  els.discBtn.onclick = ()=> withBusy('Discovery', async ()=>{
    try{
      clearBanner();
      if(!ctx){ showBanner('context.json ej laddad ännu.', 'err'); return; }
      const mode = currentDiscMode();
      const prompt = (mode==='DMOD') ? await buildDiscoveryPromptDMOD() : await buildDiscoveryPromptKMOD();
      els.out.textContent = prompt;
      els.copy.disabled = els.download.disabled = false;
      showBanner((mode==='DMOD'?'D-MOD':'K-MOD')+' Discovery-prompt skapad. Kör i modell, klistra STRICT JSON-svaret här.', 'ok');
    }catch(e){
      showBanner('Fel vid Discovery: '+e.message, 'err');
    }
  });

  // Implementation
  els.implBtn.onclick = ()=> withBusy('Build Bootstrap', async ()=>{
    try{
      clearBanner();
      if(!ctx){ showBanner('context.json ej laddad ännu.', 'err'); return; }
      await buildImplBootstrap();
    }catch(e){
      showBanner('Fel vid bootstrap: '+e.message, 'err');
    }
  });

  // STRICT input-hanterare
  els.instruction.addEventListener('input', ()=>{
    clearBanner();
    const t = els.instruction.value.trim();
    if(!t) return;
    try{
      const j = JSON.parse(t);

      // D-MOD
      if(j && j.protocol_id==='discovery_dmod_v1' && j.mode==='D-MOD' &&
         Array.isArray(j.selected_ids) && typeof j.echo_rules_hash==='string'){
        if(LAST_RULES_HASH && j.echo_rules_hash!==LAST_RULES_HASH){
          showBanner('echo_rules_hash ≠ rules_hash (från prompten).', 'warn');
        }
        const idset = new Set(j.selected_ids);
        const paths = LAST_CANDIDATES.filter(c=>idset.has(c.id)).map(c=>c.path);
        if(paths.length===0){ showBanner('D-MOD: Inga matchande ID:n i senaste kandidatuppsättning.', 'err'); return; }
        autoSelectPaths(paths);
        showBanner(`D-MOD: ${paths.length} filer auto-valda.`, 'ok');
        return;
      }

      // K-MOD
      if(j && j.protocol_id==='discovery_v2' && j.mode==='K-MOD' &&
         Array.isArray(j.selected_files) && j.selected_files.length>=2){
        const valid = j.selected_files.every(it=>{
          return it && typeof it.path==='string' &&
                 ['full','chunk','stub'].includes(it.embed) &&
                 typeof it.why==='string';
        });
        if(!valid){ showBanner('K-MOD: selected_files har fel struktur.', 'err'); return; }

        const paths = j.selected_files.map(o=>o.path);
        const unknown = paths.filter(p=>!FILES.includes(p));
        if(unknown.length){ showBanner('Okända paths: '+unknown.slice(0,5).join(', '), 'warn'); }
        autoSelectPaths(paths);
        showBanner(`K-MOD: ${paths.length} filer auto-valda.`, 'ok');
        return;
      }

      showBanner('JSON är giltig men matchar inte K-MOD/DMOD RETURN_CONTRACT.', 'warn');
    }catch(e){
      showBanner('Ogiltig JSON: '+e.message, 'err');
    }
  });

  // Hjälpmodal
  els.helpBtn.onclick = ()=> els.helpModal.classList.add('show');
  els.helpClose.onclick = ()=> els.helpModal.classList.remove('show');
  els.helpOk.onclick = ()=> els.helpModal.classList.remove('show');
  els.fpClose.onclick = ()=> els.fp.classList.remove('show');

  // ---------- Performance dashboard (utökad) ----------
  const charts = {};
  const pfState = { prov:new Set(), model:new Set(), from:null, to:null, ma:false };

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

  function getSessionProvModel(s){
    let prov='unknown', model='unknown';
    if(s && s.model){ prov = s.model.provider || prov; model = s.model.name || model; }
    else if(s && s.generatedBy && s.generatedBy.model){ prov = s.generatedBy.model.provider || prov; model = s.generatedBy.model.name || model; }
    return {prov, model};
  }

  function movingAvg(arr, w=3){
    const out=[]; for(let i=0;i<arr.length;i++){ const a=Math.max(0,i-w+1), b=i+1; const slice=arr.slice(a,b); const avg=slice.reduce((x,y)=>x+(y||0),0)/slice.length; out.push(Number.isFinite(avg)?avg:0); } return out;
  }

  function destroyCharts(){ Object.values(charts).forEach(c=>{ if(c && typeof c.destroy==='function') c.destroy(); }); }

  function renderPerfFilters(perfLog){
    const provs = new Set(), models = new Set();
    perfLog.forEach(s=>{ const pm = getSessionProvModel(s); provs.add(pm.prov); models.add(pm.model); });
    els.pf.provWrap.innerHTML = Array.from(provs).sort().map(p=>`<label class="inline"><input type="checkbox" data-provid="${escapeHtml(p)}"> ${escapeHtml(p)}</label>`).join(' ');
    els.pf.modelWrap.innerHTML = Array.from(models).sort().map(m=>`<label class="inline"><input type="checkbox" data-modelid="${escapeHtml(m)}"> ${escapeHtml(m)}</label>`).join(' ');
  }

  function applyFilter(perfLog){
    let out = perfLog.slice();
    // date range
    const from = els.pf.from.value ? new Date(els.pf.from.value) : null;
    const to   = els.pf.to.value   ? new Date(els.pf.to.value)   : null;
    if(from || to){
      out = out.filter(s=>{
        const t = s.timestamp || s.date || s.time || null;
        if(!t) return true;
        const d = new Date(t);
        if(from && d<from) return false;
        if(to && d>to) return false;
        return true;
      });
      pfState.from = from; pfState.to = to;
    }else{ pfState.from=null; pfState.to=null; }
    // provider
    const selProv = new Set(Array.from(els.pf.provWrap.querySelectorAll('input[type="checkbox"]')).filter(i=>i.checked).map(i=>i.getAttribute('data-provid')));
    const selModel = new Set(Array.from(els.pf.modelWrap.querySelectorAll('input[type="checkbox"]')).filter(i=>i.checked).map(i=>i.getAttribute('data-modelid')));
    if(selProv.size>0){ out = out.filter(s=> selProv.has(getSessionProvModel(s).prov)); pfState.prov=selProv; } else { pfState.prov.clear?.(); }
    if(selModel.size>0){ out = out.filter(s=> selModel.has(getSessionProvModel(s).model)); pfState.model=selModel; } else { pfState.model.clear?.(); }
    pfState.ma = !!els.pf.ma.checked;
    return out;
  }

  function fmt(n, d=2){ return (n==null||!Number.isFinite(n)) ? '–' : String(Math.round(n*10**d)/10**d); }
  function median(ns){ const a=ns.filter(x=>Number.isFinite(x)).slice().sort((x,y)=>x-y); if(!a.length) return null; const m = Math.floor(a.length/2); return a.length%2 ? a[m] : (a[m-1]+a[m])/2; }

  function renderLearningDbTable(targetEl, data){
    if(!data || data.length===0){ targetEl.innerHTML = 'Ingen data.'; return; }
    const rows = data.map(item=>`
      <tr>
        <td>${escapeHtml(item.heuristicId||'N/A')}</td>
        <td>${escapeHtml((item.identifiedRisk && item.identifiedRisk.description) || 'N/A')}</td>
        <td>${escapeHtml((item.mitigation && item.mitigation.description) || 'N/A')}</td>
        <td>${escapeHtml(((item.trigger && item.trigger.keywords) || []).join(', '))}</td>
      </tr>`).join('');
    targetEl.innerHTML = `<table><thead><tr><th>ID</th><th>Risk</th><th>Mitigation</th><th>Trigger Keywords</th></tr></thead><tbody>${rows}</tbody></table>`;
  }

  function renderSessionsTable(targetEl, perfLog){
    if(!perfLog || perfLog.length===0){ targetEl.innerHTML='Ingen data.'; return; }
    const rows = perfLog.map(p=>{
      const pm = getSessionProvModel(p);
      const sid = p.sessionId || p.id || '?';
      const ts = p.timestamp || p.date || '';
      const score = (p.scorecard && p.scorecard.finalScore) || null;
      const dbg = p.detailedMetrics && p.detailedMetrics.debuggingCycles;
      const sc  = p.detailedMetrics && p.detailedMetrics.selfCorrections;
      const ec  = p.detailedMetrics && p.detailedMetrics.externalCorrections;
      return `<tr>
        <td>${escapeHtml(String(sid))}</td>
        <td>${escapeHtml(String(ts||''))}</td>
        <td>${escapeHtml(pm.prov)}</td>
        <td>${escapeHtml(pm.model)}</td>
        <td>${escapeHtml(fmt(score))}</td>
        <td>${escapeHtml(String(dbg??'–'))}</td>
        <td>${escapeHtml(String(sc??'–'))}</td>
        <td>${escapeHtml(String(ec??'–'))}</td>
      </tr>`;
    }).join('');
    targetEl.innerHTML = `<table>
      <thead><tr><th>Session</th><th>Tid</th><th>Provider</th><th>Modell</th><th>Final</th><th>Cycles</th><th>Self</th><th>External</th></tr></thead>
      <tbody>${rows}</tbody></table>`;
  }

  function exportCSV(perfLog){
    const header = ['sessionId','timestamp','provider','model','finalScore','debuggingCycles','selfCorrections','externalCorrections'];
    const lines = [header.join(',')];
    perfLog.forEach(p=>{
      const pm = getSessionProvModel(p);
      const row = [
        JSON.stringify(p.sessionId || p.id || ''),
        JSON.stringify(p.timestamp || p.date || ''),
        JSON.stringify(pm.prov),
        JSON.stringify(pm.model),
        JSON.stringify((p.scorecard&&p.scorecard.finalScore)||''),
        JSON.stringify(p.detailedMetrics&&p.detailedMetrics.debuggingCycles || ''),
        JSON.stringify(p.detailedMetrics&&p.detailedMetrics.selfCorrections || ''),
        JSON.stringify(p.detailedMetrics&&p.detailedMetrics.externalCorrections || '')
      ];
      lines.push(row.join(','));
    });
    const blob = new Blob([lines.join('\n')], {type:'text/csv'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href=url; a.download='ai_performance_export.csv';
    document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
  }

  function renderPerformanceDashboard(){
    if(!ctx || !ctx.ai_performance_metrics) return;
    const metrics = ctx.ai_performance_metrics;
    const perfLogAll = Array.isArray(metrics.performanceLog) ? metrics.performanceLog : [];
    const learningDb = Array.isArray(metrics.learningDatabase) ? metrics.learningDatabase : [];

    // Init filter UI en gång
    if(!els.pf.provWrap.hasChildNodes()){ renderPerfFilters(perfLogAll); }

    const perfLog = applyFilter(perfLogAll);

    // KPI
    const labels = perfLog.map((p,i)=> p.timestamp || p.date || ('#'+(i+1)));
    const scores = perfLog.map(p => p.scorecard ? p.scorecard.finalScore : 0);
    const dbg = perfLog.map(p => p.detailedMetrics ? p.detailedMetrics.debuggingCycles : 0);
    const sc  = perfLog.map(p => p.detailedMetrics ? p.detailedMetrics.selfCorrections : 0);
    const ec  = perfLog.map(p => p.detailedMetrics ? p.detailedMetrics.externalCorrections : 0);
    els.kpi.sessions.textContent = String(perfLog.length);
    els.kpi.rng.textContent = labels.length ? `${labels[0]} → ${labels[labels.length-1]}` : '';
    els.kpi.avg.textContent = fmt(scores.reduce((a,b)=>a+(b||0),0)/Math.max(scores.length,1));
    els.kpi.cycles.textContent = fmt(median(dbg));
    els.kpi.corr.textContent = fmt((sc.reduce((a,b)=>a+(b||0),0))/(Math.max(ec.reduce((a,b)=>a+(b||0),0),1)));

    // Destroy & re-render charts
    destroyCharts();

    const sMA = pfState.ma ? movingAvg(scores, 3) : null;

    charts.scoreChart = new Chart(document.getElementById('score-chart').getContext('2d'), {
      type:'line',
      data:{ labels, datasets:[
        { label:'Final Score', data:scores, fill:true, tension:.1 },
        ...(pfState.ma ? [{ label:'MA(3)', data:sMA, fill:false }] : [])
      ]},
      options:{ responsive:true, maintainAspectRatio:false }
    });
    charts.metricsChart = new Chart(document.getElementById('metrics-chart').getContext('2d'), {
      type:'bar',
      data:{ labels, datasets:[
        { label:'Debugging Cycles', data:dbg },
        { label:'Self Corrections', data:sc },
        { label:'External Corrections', data:ec }
      ]},
      options:{ responsive:true, maintainAspectRatio:false, scales:{ x:{stacked:true}, y:{stacked:true, beginAtZero:true} } }
    });

    const agg = aggregateModelStats(perfLog);
    charts.providerChart = new Chart(document.getElementById('provider-chart').getContext('2d'), {
      type:'pie',
      data:{ labels:Object.keys(agg.byProvider), datasets:[{ data:Object.values(agg.byProvider) }] },
      options:{ responsive:true, maintainAspectRatio:false }
    });
    charts.modelChart = new Chart(document.getElementById('model-chart').getContext('2d'), {
      type:'pie',
      data:{ labels:Object.keys(agg.byModel), datasets:[{ data:Object.values(agg.byModel) }] },
      options:{ responsive:true, maintainAspectRatio:false }
    });

    // Learning DB + Sessions table
    if(els.perfLearning) renderLearningDbTable(els.perfLearning, learningDb);
    if(els.perfSessions) renderSessionsTable(els.perfSessions, perfLog);
  }

  async function refreshPerformanceData(){
    try{
      const res = await fetch('context.json', {cache:'no-store'});
      if(!res.ok) throw new Error(`status ${res.status}`);
      const data = await res.json();
      if(data && data.ai_performance_metrics){
        ctx.ai_performance_metrics = data.ai_performance_metrics;
        renderPerfFilters(Array.isArray(data.ai_performance_metrics.performanceLog)?data.ai_performance_metrics.performanceLog:[]);
        renderPerformanceDashboard();
      }
    }catch(e){ console.error('Kunde inte läsa om context.json:', e); }
  }

  els.pf.apply.addEventListener('click', ()=> renderPerformanceDashboard());
  els.pf.reset.addEventListener('click', ()=>{
    els.pf.from.value=''; els.pf.to.value='';
    els.pf.provWrap.querySelectorAll('input[type="checkbox"]').forEach(i=>i.checked=false);
    els.pf.modelWrap.querySelectorAll('input[type="checkbox"]').forEach(i=>i.checked=false);
    els.pf.ma.checked=false;
    renderPerformanceDashboard();
  });
  els.pf.export.addEventListener('click', ()=>{
    if(!ctx || !ctx.ai_performance_metrics) return;
    const perfLogAll = Array.isArray(ctx.ai_performance_metrics.performanceLog) ? ctx.ai_performance_metrics.performanceLog : [];
    const perfLog = applyFilter(perfLogAll);
    exportCSV(perfLog);
  });
  els.pf.refresh.addEventListener('click', refreshPerformanceData);

  // ---------- Load context.json ----------
  fetch('context.json', {cache:'no-store'})
    .then(r=>{ if(!r.ok) throw new Error('HTTP '+r.status); return r.json(); })
    .then(data=>{
      ctx = data;
      FILES = flattenPaths(ctx.file_structure);
      CODE_FILES = FILES.filter(p=>isCodeLike(p) && !IMAGE_EXT.includes((p.split('.').pop()||'').toLowerCase()));
      els.tree.innerHTML = '';
      renderTree(ctx.file_structure, els.tree, '');
      recomputeAllParents();
      showBanner('Context laddad. Fortsätt med Steg A (STRICT K-MOD/D-MOD) eller Steg B.', 'ok');
    })
    .catch(e=>{
      els.tree.innerHTML = '<p style="color:#b00020">Kunde inte läsa context.json: '+escapeHtml(e.message)+'</p>';
    });

})();
</script>
</body>
</html>
"""

def main():
    if len(sys.argv) != 2:
        print("Usage: python wrap_json_in_html.py <output_html_path>", file=sys.stderr)
        sys.exit(1)
    out = sys.argv[1]
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(HTML)

if __name__ == "__main__":
    main()
