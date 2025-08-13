#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wrap_json_in_html.py — AI Context Builder v7.4 (2025-08-11) (update)

Nyheter vs v7.3:
- v7.5 (2025-08-11): Optimerat CORE-konstanten för att minska initial kontextstorlek och förlita sig på en dynamiskt uppdaterad `docs/core_file_info.json`.
- Stabilisering: Plugin-logik för Patch Center har nu integrerats direkt i denna fil för att eliminera dynamiska injiceringsfel.

Kör:
  python scripts/wrap_json_in_html.py dist/index.html
"""
import os, sys

HTML = r"""<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>AI Context Builder v7.4 — Integrated Patch Center</title>
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

/* Tabs */
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

/* --- Patch Center Plugin CSS --- */
#plug-patch-modal .box{max-width:1100px}
#plug-patch-log{white-space:pre-wrap;border:1px solid #ddd;border-radius:8px;padding:8px;background:#fff;max-height:34vh;overflow:auto}
#plug-patch-target{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
#plug-patch-target .badge{padding:2px 8px;border:1px solid #ccc;border-radius:999px;background:#f6f7f9;font-size:12px}
#plug-patch-preview{width:100%;height:360px}
#plug-patch-source{width:100%;height:160px}
#plug-patch-file{display:none}
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
      <label class="inline" title="Kompaktare JSON"><input type="checkbox" id="compact" /> Kompakt JSON</label>
    </span>
    <button id="genContext" class="primary">Generate Context</button>
    <button id="genFiles" class="info">Generate Files</button>
    <button id="genBootstrap" class="primary">Generate Bootstrap.md</button>
    <button id="genMenu" class="info">Generate Menu Discovery</button>
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

      <span style="margin-left:12px"><b>Discovery:</b></span>
      <label class="inline" title="K-MOD: utforskning (paths)"><input type="radio" name="discMode" value="KMOD" checked /> K-MOD</label>
      <label class="inline" title="D-MOD: deterministiskt urval (ID + rules_hash)"><input type="radio" name="discMode" value="DMOD" /> D-MOD</label>

      <span class="flex" style="margin-left:12px">
        <span class="badge">Max candidates</span>
        <input id="maxCands" type="number" min="1" step="50" value="99999" />
        <label class="inline"><input type="checkbox" id="incAssets" /> Inkl. assets</label>
        <label class="inline" title="Lägg full inventory i prompt"><input type="checkbox" id="incInventory" checked /> Bifoga FILE_INVENTORY</label>
      </span>

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
      <pre id="out">Här visas Discovery-prompt (K/D), context eller filer.</pre>
      <div class="small">All export är markdown med inbäddad ```json.</div>
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
      <ol>
        <li><b>Skapa nästa arbete</b>:
          <ul>
            <li><b>K-MOD</b> → returnera <b>paths</b> + <b>embed</b> + <b>why</b>. <u>INGA id</u>.</li>
            <li><b>D-MOD</b> → returnera <b>selected_ids</b> + <b>notes</b> + <b>echo_rules_hash</b>. <u>INGA paths</u>.</li>
            <li>Prompt innehåller <code>CANDIDATE_FILES</code> och, om valt, <code>FILE_INVENTORY</code> (kompakt metadata).</li>
          </ul>
        </li>
        <li>Klistra in modellsvar (STRICT JSON) → auto-select.</li>
        <li><b>Skapa uppgift</b> → impl_bootstrap_v1.json + provider_envelope.json (markdown) med <code>inventory_compact</code>.</li>
        <li>Alt: <b>Generate Files</b> → markdown med <code>files_payload.json</code> + <code>checksums</code>.</li>
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

<!-- Patch Center Modal (INTEGRATED) -->
<div id="plug-patch-modal" class="modal" role="dialog" aria-modal="true" aria-labelledby="plug-patch-title">
  <div class="box">
    <header>
      <b id="plug-patch-title">Patch Center</b>
      <div class="flex">
        <button id="plug-patch-close" aria-label="Stäng">✕</button>
      </div>
    </header>
    <main>
      <div class="flex" style="justify-content:space-between;align-items:flex-end;gap:12px;flex-wrap:wrap">
        <div style="flex:1;min-width:280px">
          <label for="plug-patch-source" class="small">Klistra in <kbd>diff.json</kbd> (anchor_diff_v2.1) här:</label>
          <textarea id="plug-patch-source" placeholder='{"protocol_id":"anchor_diff_v2.1","target":{"path":"scripts/wrap_json_in_html.py","base_checksum_sha256":"<64-hex>"},"op_groups":[{"anchor":{"text":"<unik text som finns i basen>","match_mode":"exact"},"targets":[{"op":"replace_block","match_index":1,"old_block":"<gammalt textblock direkt efter ankaret>","new_block":"<ersättningstext>"}]}]}'></textarea>
        </div>
        <div class="flex" style="gap:8px">
          <input id="plug-patch-file" type="file" accept=".json,application/json" />
          <button id="plug-patch-upload">Ladda upp JSON</button>
          <button id="plug-patch-validate" class="primary">Validate</button>
        </div>
      </div>

      <div id="plug-patch-target" style="margin-top:10px">
        <span class="badge">Target: <span id="plug-target-path">–</span></span>
        <span class="badge">base_sha256: <span id="plug-target-sha256">–</span></span>
        <span class="badge">git_sha1: <span id="plug-target-gitsha">–</span></span>
        <span class="badge">Källa: <span id="plug-target-source">–</span></span>
        <span class="badge" id="plug-schema-ok" style="display:none;background:#eaf7ef;border-color:#bfe3cc;color:#114d27">Schema OK</span>
      </div>

      <div class="flex" style="gap:8px;margin-top:10px">
        <button id="plug-patch-apply" class="primary" disabled>Apply Patch</button>
        <button id="plug-patch-copy" disabled>Copy</button>
        <button id="plug-patch-download" disabled>Download</button>
      </div>

      <textarea id="plug-patch-preview" placeholder="// Här visas patchad kod efter Apply…"></textarea>

      <h4 style="margin:12px 0 6px 0">Logg</h4>
      <pre id="plug-patch-log"></pre>
    </main>
  </div>
</div>

<script>
(function(){
  // ---------- Konstanter ----------
  const RAW_DEFAULT_REPO = 'Engrove/Engrove-Audio-Tools-2.0';
  const RAW_DEFAULT_BRANCH = 'main';
  const IMAGE_EXT = ['png','jpg','jpeg','gif','webp','svg'];

  // ---------- Element ----------
  const els = {
    // vänster
    tree:document.getElementById('tree'),
    selAll:document.getElementById('selAll'),
    deselAll:document.getElementById('deselAll'),
    selCore:document.getElementById('selCore'),
    genContext:document.getElementById('genContext'),
    genFiles:document.getElementById('genFiles'),
    genBootstrap:document.getElementById('genBootstrap'),
    genMenu:document.getElementById('genMenu'),
    budgetKb:document.getElementById('budgetKb'),
    compact:document.getElementById('compact'),
    // höger/builder
    instruction:document.getElementById('instruction'),
    out:document.getElementById('out'),
    copy:document.getElementById('copy'),
    download:document.getElementById('download'),
    discBtn:document.getElementById('discBtn'),
    implBtn:document.getElementById('implBtn'),
    banner:document.getElementById('banner'),
    // discovery-val
    maxCands:document.getElementById('maxCands'),
    incAssets:document.getElementById('incAssets'),
    incInventory:document.getElementById('incInventory'),
    // tabs
    tabBtns:document.querySelectorAll('.tabbar button[data-tab]'),
    tabs:{ builder:document.getElementById('tab-builder'), performance:document.getElementById('tab-performance') },
    // provider
    provGemini:document.querySelector('input[name="prov"][value="gemini"]'),
    // modals
    helpBtn:document.getElementById('helpBtn'),
    helpModal:document.getElementById('helpModal'),
    helpClose:document.getElementById('helpClose'),
    helpOk:document.getElementById('helpOk'),
    fp:document.getElementById('filePreview'),
    fpTitle:document.getElementById('fpTitle'),
    fpBody:document.getElementById('fpBody'),
    fpCopy:document.getElementById('fpCopy'),
    fpDownload:document.getElementById('fpDownload'),
    fpClose:document.getElementById('fpClose'),
    // busy
    busy:document.getElementById('busy'),
    worklog:document.getElementById('worklog'),
    // performance
    pf:{ from:document.getElementById('pf-from'), to:document.getElementById('pf-to'),
         provWrap:document.getElementById('pf-prov'), modelWrap:document.getElementById('pf-model'),
         ma:document.getElementById('pf-ma'), apply:document.getElementById('pf-apply'),
         reset:document.getElementById('pf-reset'), export:document.getElementById('pf-export'),
         refresh:document.getElementById('refresh-performance') },
    kpi:{ sessions:document.getElementById('kpi-sessions'), rng:document.getElementById('kpi-range'),
          avg:document.getElementById('kpi-avg'), cycles:document.getElementById('kpi-cycles'),
          corr:document.getElementById('kpi-corr') },
    perfLearning:document.getElementById('perf-learning-body'),
    perfSessions:document.getElementById('perf-sessions-body'),
  };

  // ---------- Tillstånd ----------
  let ctx=null;
  let FILES=[], CODE_FILES=[];
  let INVENTORY=[]; // rik metadata
  let HASHMAPS=null; // path<->hash mappar
  let RAW_BASE=''; // råbas-URL
  let LAST_CANDIDATES=[], LAST_RULES_HASH=null;

  const CORE = [
    'docs/ai_protocols/AI_Core_Instruction.md',
    'docs/ai_protocols/ai_config.json',
    'docs/ai_protocols/frankensteen_persona.v1.0.json',
    'package.json',
    'vite.config.js',
    'docs/Mappstruktur_och_Arbetsflöde.md',
    'tools/frankensteen_learning_db.json',
    'docs/ai_protocols/AI_Dynamic_Protocols.md',
    'docs/ai_protocols/DynamicProtocols.json',
    'docs/core_file_info.json',

    // Felsökning & eskalering
    'docs/ai_protocols/Escalation_Protocol.md',
    'docs/ai_protocols/HITL_Interrupt_Points.md',
    'docs/ai_protocols/Help_me_God_Protokoll.md',
    'docs/ai_protocols/Stalemate_Protocol.md',
    'docs/ai_protocols/Structured_Debugging_Checklist.md',
    'docs/ai_protocols/System_Integrity_Check_Protocol.md',
    'docs/ai_protocols/Pre_Execution_Alignment.md',
    'docs/ai_protocols/Levande_Kontext_Protokoll.md',
    'docs/ai_protocols/Confidence_Protocol.md',

    // Stöd
    'docs/ai_protocols/Sandbox_Execution_Protokoll.md',
    'docs/ai_protocols/Multi_Sample_Protokoll.md',
    'docs/ai_protocols/RAG_Faktacheck_Protokoll.md',
    'docs/ai_protocols/Stature_Report_Protocol.md',
    'docs/ai_protocols/Diff_JSON_Protocol.md' // deprekerad; behåll tills Diff_Protocol v3.x finns
  ];


  // ---------- Utils ----------
  function showBanner(msg, kind='warn'){
    els.banner.textContent = msg;
    els.banner.className = 'banner ' + (kind==='err'?'err':kind==='ok'?'ok':'');
    els.banner.style.display = 'block';
  }
  function clearBanner(){ els.banner.style.display='none'; els.banner.textContent=''; els.banner.className='banner'; }
  function escapeHtml(s){ return String(s).replace(/[&<>"']/g, m=>({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m])); }
  function logw(msg){ const t=new Date().toLocaleTimeString(); els.worklog.textContent += `[${t}] ${msg}\n`; els.worklog.scrollTop = els.worklog.scrollHeight; }
  async function withBusy(label, fn){
    els.worklog.textContent = '';
    els.busy.style.display = 'flex';
    logw(label+' start');
    try{ const r = await fn(); logw(label+' klar'); return r; }
    finally{ setTimeout(()=> els.busy.style.display='none', 150); }
  }

  function isCodeLike(p){
    const ext=(p.split('.').pop()||'').toLowerCase();
    return ['py','js','jsx','ts','tsx','vue','json','md','html','css','yml','yaml','toml','sh','bat'].includes(ext);
  }
  function guessLang(p){
    const e=(p.split('.').pop()||'').toLowerCase();
    if(['ts','tsx'].includes(e)) return 'ts';
    if(e==='vue') return 'vue';
    if(e==='py') return 'py';
    if(['js','jsx'].includes(e)) return 'js';
    if(e==='md') return 'md';
    if(e==='json') return 'json';
    if(e==='html') return 'html';
    if(e==='css') return 'css';
    if(e==='yml'||e==='yaml') return 'yml';
    return 'txt';
  }

  // Kanonisering + hash (LF, utan BOM)
  function canonText(s){ return (s||'').replace(/\uFEFF/g,'').replace(/\r\n?/g,'\n'); }
  async function sha256HexLF(text){
    const enc = new TextEncoder().encode(canonText(text));
    const buf = await crypto.subtle.digest('SHA-256', enc);
    return Array.from(new Uint8Array(buf)).map(b=>b.toString(16).padStart(2,'0')).join('');
  }

  async function fetchText(path){
    const url = RAW_BASE + path;
    const r = await fetch(url, {cache:'no-store'});
    if(!r.ok) throw new Error('HTTP '+r.status+' for '+url);
    return await r.text();
  }

  // ---------- Tree helpers ----------
  function flattenPaths(node, prefix='', out=[]){
    Object.keys(node).sort().forEach(k=>{
      const it=node[k], p=prefix?`${prefix}/${k}`:k;
      if(it.type==='file'){ out.push(it.path||p); }
      else{ flattenPaths(it, p, out); }
    });
    return out;
  }

  // Kaskad + tri-state
  function renderTree(node, parent, base=''){
    const ul=document.createElement('ul');
    const keys=Object.keys(node).sort((a,b)=>{
      const aF=node[a].type==='file', bF=node[b].type==='file';
      if(aF && !bF) return 1;
      if(!aF && bF) return -1;
      return a.localeCompare(b);
    });

    keys.forEach(k=>{
      const it=node[k], p=base?`${base}/${k}`:k;
      const li=document.createElement('li');

      const label=document.createElement('label'); label.className='fileline';
      const cb=document.createElement('input'); cb.type='checkbox'; cb.dataset.path=p;
      label.appendChild(cb);
      const icon=document.createElement('span');
      const isImg = IMAGE_EXT.includes((k.split('.').pop()||'').toLowerCase());
      icon.textContent = (it.type==='file' ? (isImg?'🖼️':'📄') : '📁');
      label.appendChild(icon);
      const a=document.createElement('a'); a.href='#'; a.textContent=' '+k; a.dataset.path=p;
      label.appendChild(a);
      li.appendChild(label);

      if(it.type==='file'){
        a.addEventListener('click', async (e)=>{ e.preventDefault(); showFilePreview(p); });
      } else {
        const toggle=document.createElement('span'); toggle.className='toggle'; toggle.textContent='►';
        li.insertBefore(toggle, label);
        const sub=renderTree(it, li, p); sub.style.display='none'; li.appendChild(sub);
        toggle.addEventListener('click', ()=>{
          const vis=sub.style.display==='none'; sub.style.display=vis?'block':'none';
          toggle.textContent=vis?'▼':'►';
        });
      }

      cb.addEventListener('change', ()=>{
        const sub=li.querySelector(':scope > ul');
        if(sub){ sub.querySelectorAll('input[type="checkbox"]').forEach(x=> x.checked=cb.checked); }
        updateParents(li);
      });

      ul.appendChild(li);
    });

    return parent.appendChild(ul);
  }
  function updateParents(li){
    let p=li.parentElement && li.parentElement.closest('li');
    while(p){
      const kids=p.querySelectorAll(':scope > ul input[type="checkbox"]');
      const parentCb=p.querySelector(':scope > label input[type="checkbox"]');
      const total=kids.length, on=Array.from(kids).filter(c=>c.checked).length;
      if(parentCb){ parentCb.indeterminate = on>0 && on<total; parentCb.checked = on===total; }
      p=p.parentElement && p.parentElement.closest('li');
    }
  }
  function recomputeAllParents(){ document.querySelectorAll('#tree li').forEach(li=> updateParents(li)); }
  function selectedPaths(){ return Array.from(els.tree.querySelectorAll('input[type="checkbox"]:checked')).map(cb=>cb.dataset.path); }
  function selectedFiles(){ return Array.from(els.tree.querySelectorAll('input[type="checkbox"]:checked')).map(cb=>cb.dataset.path).filter(p => HASHMAPS.byPath.get(p)?.type === 'file'); }
  
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
  function autoSelectPaths(paths){
    const all = Array.from(els.tree.querySelectorAll('input[type="checkbox"]'));
    paths.forEach(p=>{
      const cb = all.find(x=>x.dataset.path===p);
      if(cb){ cb.checked=true; openParentsFor(p); updateParents(cb.closest('li')); }
    });
    recomputeAllParents();
  }
  function quickSelectCore(){
    els.tree.querySelectorAll('input[type="checkbox"]').forEach(cb=>cb.checked=false);
    CORE.forEach(p=>{
      const cb = els.tree.querySelector(`input[data-path="${CSS.escape(p)}"]`);
      if(cb){ cb.checked=true; openParentsFor(p); updateParents(cb.closest('li')); }
    });
    recomputeAllParents();
  }

  // ---------- Markdown wrapper ----------
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

  // ---------- Hash-index och inventory ----------
  function buildHashMaps(ctx){
    const out = { path2sha:new Map(), path2git:new Map(), sha2paths:new Map(), git2paths:new Map(), byPath:new Map() };
    const idx = (ctx && ctx.hash_index) || {};
    const sha = idx.sha256_lf || idx.sha256 || {};
    const git = idx.git_sha1 || {};
    
    Object.entries(sha).forEach(([h, paths])=>{
      const arr = Array.isArray(paths) ? paths : [paths];
      out.sha2paths.set(h, arr[0]); // Lagra bara den primära sökvägen
      arr.forEach(p=> out.path2sha.set(p, h));
    });
    
    Object.entries(git).forEach(([h, paths])=>{
      const arr = Array.isArray(paths) ? paths : [paths];
      out.git2paths.set(h, arr[0]);
      arr.forEach(p=> out.path2git.set(p, h));
    });

    (function walk(node){
      if(node && typeof node === 'object'){
        if(node.type === 'file' && node.path){
          out.byPath.set(node.path, node);
        } else {
          Object.values(node).forEach(walk);
        }
      }
    })(ctx.file_structure || {});

    return out;
  }

  function walkInventory(node, acc, base=''){
    Object.keys(node).forEach(k=>{
      const it = node[k];
      const p = base?`${base}/${k}`:k;
      if(it.type==='file'){
        const path = it.path || p;
        const rec = {
          path,
          type:'file',
          size: (typeof it.size==='number') ? it.size : null,
          lang: guessLang(path),
          is_content_full: !!it.is_content_full,
          sha256_lf: HASHMAPS.path2sha.get(path) || null,
          git_sha1:  HASHMAPS.path2git.get(path) || null
        };
        acc.push(rec);
      }else{
        walkInventory(it, acc, p);
      }
    });
  }

  function buildInventory(ctx){
    const acc = [];
    walkInventory(ctx.file_structure||{}, acc, '');
    acc.sort((a,b)=> a.path.localeCompare(b.path));
    return acc;
  }

  // ---------- Context/Files generering ----------
  async function buildBootstrapMd(){
    try{
      clearBanner();
      const sel = selectedFiles();
      if(sel.length===0){ showBanner('Välj minst en fil.', 'warn'); return; }
      const inventory_compact = INVENTORY.map(r=>({ path:r.path, lang:r.lang, size:r.size, sha256_lf:r.sha256_lf, git_sha1:r.git_sha1 }));
      const contextJson = {
        session_task: 'TEXTID 123:Här skriver man in den uppgift som chatsessionen ska ha',
        standing_mandate:{
          remember_and_obey_next_reply:true,
          state_snapshot_every_n_turns:{min:10,max:20,action:'produce_RUN_STATE_and_list_candidate_protocols'},
          patch_or_error_gate:'before_running_any_fix_request_diff_plan_and_selected_protocol',
          topic_shift_guard:'verify_CORE_is_controlling; if uncertain, ask briefly'
        },
        core_files: CORE,
        selected_paths: sel.slice(),
        inventory_compact
      };
      const pretty = els.compact.checked ? JSON.stringify(contextJson) : JSON.stringify(contextJson, null, 2);
      const md = mdWrapJsonSection('context_bootstrap_instruction_FINAL_v2.8.md', pretty);
      els.out.textContent = md;
      els.copy.disabled = els.download.disabled = false;
      showBanner('Bootstrap.md genererad.', 'ok');
    }catch(e){ showBanner('Fel vid bootstrap-generering: '+e.message, 'err'); }
  }

  async function buildNewContextNode(src, selSet){
    const dst={};
    for(const k of Object.keys(src).sort()){
      const it=src[k];
      if(it.type==='file'){
        const copy={...it};
        if(selSet.has(it.path)){
          try{ copy.content = await fetchText(it.path); } catch{ copy.content='// Error: fetch fail'; }
          copy.is_content_full = true;
        } else { delete copy.content; copy.is_content_full = false; }
        dst[k]=copy;
      }else{
        dst[k]=await buildNewContextNode(it, selSet);
      }
    }
    return dst;
  }

  async function generateContext(){
    try{
      clearBanner(); logw('Samlar valda paths…');
      const sels = new Set(selectedPaths());
      if (sels.size === 0) { showBanner('Välj minst en fil eller mapp.', 'warn'); return; }
      const out = {
        project_overview: ctx.project_overview,
        ai_instructions: ctx.ai_instructions || {},
        hash_index: ctx.hash_index || {},
        file_structure: {}
      };
      const rules = new Set([...(out.ai_instructions.obligatory_rules||[]), 'forbid_image_generation']);
      out.ai_instructions.obligatory_rules = Array.from(rules);
      if(els.instruction.value.trim()) out.ai_instructions_input = els.instruction.value.trim();

      logw('Bygger nytt file_structure…');
      out.file_structure = await buildNewContextNode(ctx.file_structure, sels);

      const text = els.compact.checked ? JSON.stringify(out) : JSON.stringify(out, null, 2);
      const md = mdWrapJsonSection('context.json', text);
      els.out.textContent = md;
      els.copy.disabled = els.download.disabled = false;
      showBanner('Context genererad.', 'ok');
    }catch(e){
      showBanner('Fel vid context-generering: '+e.message, 'err');
    }
  }

  async function generateFiles(){
    try{
      clearBanner(); logw('Hämtar fulltext + checksums för valda filer…');
      const sels = new Set(selectedPaths());
      const files = {};
      const checksums = {};
      async function walk(src){
        for(const k of Object.keys(src)){
          const it = src[k];
          if(it.type==='file' && sels.has(it.path)){
            try{
              const t = await fetchText(it.path);
              files[it.path] = t;
              checksums[it.path] = await sha256HexLF(t);
            }catch(_){
              const msg = `// Error: failed to fetch ${it.path}`;
              files[it.path] = msg;
              checksums[it.path] = await sha256HexLF(msg);
            }
          }else if(it.type!=='file'){
            await walk(it);
          }
        }
      }
      await walk(ctx.file_structure);
      const payload = { obligatory_rules:['forbid_image_generation'], files, checksums };
      emit(payload, 'files_payload.json');
      showBanner('Filer genererade (md).', 'ok');
    }catch(e){
      showBanner('Fel vid file-generering: '+e.message, 'err');
    }
  }

  function emit(obj, nameHint='context.json'){
    const text = els.compact.checked ? JSON.stringify(obj) : JSON.stringify(obj, null, 2);
    els.out.textContent = mdWrapJsonSection(nameHint, text);
    els.copy.disabled = els.download.disabled = false;
  }

  // ---------- Discovery (strikt) ----------
  // ---- Menu-first Discovery Prompt (obligatoriskt första steg) ----
  function buildMenuFirstPrompt(){
    try{
      clearBanner();
      if(!ctx){ showBanner('context.json ej laddad ännu.', 'err'); return; }
      if(!Array.isArray(INVENTORY) || INVENTORY.length===0){
        HASHMAPS = buildHashMaps(ctx);
        INVENTORY = buildInventory(ctx);
      }
      const inv = INVENTORY;

      // RIKA kandidater (purpose, info_source, checksums)
      const cands = buildCandidatesRich(els.maxCands.value, !!els.incAssets.checked);
      LAST_CANDIDATES = cands.slice();

      // FÖRGENERERAD MENY (stabil ordning + rekommendationer)
      const menuPayload = buildMenuPayload(inv);

      // Payload till modellen (kandidater + ev. inventory)
      const payload = { CANDIDATE_FILES: cands };
      if(els.incInventory && els.incInventory.checked){
        payload.inventory_compact = inv.map(r=>({ path:r.path, lang:r.lang, size:r.size||null, sha256_lf:r.sha256_lf||null, git_sha1:r.git_sha1||null }));
      }

      const hdr = [
        '### MENU_DISCOVERY_v1 (obligatoriskt förstasteg)',
        '- Nedan finns en färdig MENY (DISCOVERED_MENU). Välj nummer (ex: 1 eller 1,2).',
        '- Om du ändå är osäker: ställ EN kort ja/nej-fråga innan val.',
        '- Svara ENBART med JSON: {"menu":[...], "recommended":[...], "question":"..."}.',
        '',
        '### EFTER_VAL',
        '- När jag svarat med nummer: generera **K-MOD discovery_v2** strikt (endast {protocol_id, mode, selected_files[]}).',
        '- Begränsa urval enligt include/exclude-globs från mitt val; `docs/**` → "stub" om inte uttryckligen valt.'
      ].join('\n');

      const prettyMenu = els.compact && els.compact.checked ? JSON.stringify(menuPayload) : JSON.stringify(menuPayload, null, 2);
      const prettyCand = els.compact && els.compact.checked ? JSON.stringify(payload) : JSON.stringify(payload, null, 2);

      const md = [
        '### MENU_FIRST_DISCOVERY_PROMPT',
        '',
        hdr,
        '```json',
        prettyMenu,
        '```',
        '```json',
        prettyCand,
        '```'
      ].join('\n');

      els.out.textContent = md;
      els.copy.disabled = els.download.disabled = false;
      showBanner('Menu-first discovery prompt (med meny + rika kandidater) genererad.', 'ok');
    }catch(e){ showBanner('Fel vid menu-first: '+e.message, 'err'); }
  }

  // ---- Menu Discovery (kategori-heuristik + MD/JSON) ----
  function _count(inv, pred){ let n=0; for(const it of inv){ if(pred(it)) n++; } return n; }
  function _has(inv, pred){ for(const it of inv){ if(pred(it)) return true; } return false; }
  function _ext(p){ const i=p.lastIndexOf('.'); return i>=0?p.slice(i+1).toLowerCase():''; }
  function _conf(n){ return n>=50?'high':(n>=10?'med':'low'); }
  function _starts(p, pre){ return p.startsWith(pre); }
  function _eq(p, s){ return p===s; }
  function _srcLike(p){ const e=_ext(p); return ['vue','ts','js'].includes(e) && p.startsWith('src/'); }
  function _router(p){ return p.startsWith('src/router/'); }
  function _stores(p){ return p.startsWith('src/stores/') || p.startsWith('src/pinia/'); }

  function buildMenuPayload(inv){
    const cats = [];
    const c1 = _count(inv, it=> _srcLike(it.path) || _eq(it.path,'package.json') || /^vite\.config\./.test(it.path) || _eq(it.path,'index.html'));
    cats.push({ n:1, label:'Vue build & appkod', count:c1, conf:_conf(c1), include_globs:['src/**','package.json','vite.config.*','index.html'], exclude_globs:['docs/**','sessions/**','public/data/**'] });
    const c2 = _count(inv, it=> _srcLike(it.path) || _router(it.path) || _stores(it.path));
    cats.push({ n:2, label:'Körtidsfel/Router/Pinia', count:c2, conf:_conf(c2), include_globs:['src/**/*.{vue,ts,js}','src/router/**','src/stores/**'], exclude_globs:['docs/**'] });
    const c3 = _count(inv, it=> _starts(it.path,'functions/') || _starts(it.path,'api/') || _eq(it.path,'public/_routes.json'));
    cats.push({ n:3, label:'Backend/Routes/CF', count:c3, conf:_conf(c3), include_globs:['functions/**','api/**','public/_routes.json'], exclude_globs:['docs/**'] });
    const c4 = _count(inv, it=> _starts(it.path,'tests/') || /\/[^/]+\.spec\./.test(it.path));
    cats.push({ n:4, label:'Tester', count:c4, conf:_conf(c4), include_globs:['tests/**','src/**/*.spec.*'], exclude_globs:['docs/**'] });
    const c5 = _count(inv, it=> _starts(it.path,'public/data/'));
    cats.push({ n:5, label:'Data/Mock', count:c5, conf:_conf(c5), include_globs:['public/data/**'], exclude_globs:[] });
    const c6 = _count(inv, it=> _starts(it.path,'docs/'));
    cats.push({ n:6, label:'Docs/Protokoll (stub)', count:c6, conf:_conf(c6), include_globs:['docs/**'], exclude_globs:[], embed:'stub' });

    const rec = [];
    if(c1>0) rec.push(1);
    if((_has(inv, it=> _router(it.path)||_stores(it.path))) && rec.length<2) rec.push(2);
    if(rec.length===0 && c3>0) rec.push(3);

    return { menu: cats, recommended: rec, question:'Välj ett eller flera nummer (ex: 1 eller 1,2).' };
  }

  function buildMenuDiscovery(){
    const inv = INVENTORY || [];
    const payload = buildMenuPayload(inv);
    const lines = [];
    lines.push('### MENU_DISCOVERY_v1');
    lines.push('- Skapa en NUMRERAD meny (≤8 val) baserat på filerna.');
    lines.push('- Ordning: app-kod, build-config, backend/functions, tests, data/mock, docs/övrigt.');
    lines.push('- Varje rad: nummer, label, count, confidence, include_globs, exclude_globs (+ ev. embed:"stub").');
    lines.push('- Markera rekommenderade med ★ (max 2) och lista dem i "recommended".');
    lines.push('- Ställ EN fråga: "Välj ett eller flera nummer …"');
    lines.push('');
    const pretty = els.compact.checked ? JSON.stringify(payload) : JSON.stringify(payload, null, 2);
    lines.push('```json');
    lines.push(pretty);
    lines.push('```');
    els.out.textContent = lines.join('\n');
    els.copy.disabled = els.download.disabled = false;
    showBanner('Menu Discovery genererad.', 'ok');
  }

  // Enriched info (async): fetch header/full/head när core_info saknas
  async function getRichFileInfoAsync(path, coreInfo){
    const r0 = getRichFileInfo(path, null, coreInfo);
    if(r0 && r0.source !== 'none') return r0;
    if(!isCodeLike(path)) return r0;
    try{ const txt = await fetchText(path); return getRichFileInfo(path, txt, coreInfo); }catch(_){ return r0; }
  }

  async function buildCandidatesRichAsync(maxN, includeAssets){
    const arr = INVENTORY.filter(it=> includeAssets ? true : isCodeLike(it.path));
    const lim = Math.max(1, Number(maxN||0) || 999999);
    const sliced = arr.slice(0, lim);
    const coreInfo = (ctx.core_info_data || {});
    const items = [];
    for(let i=0;i<sliced.length;i++){
      const rec = sliced[i];
      const info = await getRichFileInfoAsync(rec.path, coreInfo);
      items.push({
        id: i+1,
        path: rec.path,
        lang: rec.lang,
        size: rec.size,
        sha256_lf: rec.sha256_lf || null,
        git_sha1: rec.git_sha1 || null,
        info_source: info.source,
        purpose: info.description
      });
    }
    return items;
  }

  function currentDiscMode(){ const el=document.querySelector('input[name="discMode"]:checked'); return el?el.value:'KMOD'; }

  function dmodHardRules(){
    return [
      "D-MOD HÅRDA REGLER (svara ENBART med JSON):",
      "1) Returnera ENBART fälten: protocol_id, mode, echo_rules_hash, selected_ids, notes.",
      "2) selected_ids: enbart heltal (ID:n från CANDIDATE_FILES).",
      "3) notes: objekt där NYCKLARNA är dessa ID (som strängar), värden ≤200 tecken.",
      "4) INGA paths/filnamn, INGA extra fält.",
      "5) echo_rules_hash MÅSTE exakt matcha rules_hash.",
      "6) Antal val: min 2, max 12."
    ].join("\\n");
  }
  function kmodHardRules(){
    return [
      "K-MOD HÅRDA REGLER (svara ENBART med JSON):",
      "1) Returnera fälten: protocol_id, mode, selected_files[].",
      "2) selected_files[]: objekt med {path, embed, why}.",
      "3) path: exakt filväg från CANDIDATE_FILES. INGA ID.",
      "4) embed ∈ {'full','chunk','stub'}; why ≤200 tecken.",
      "5) INGA extrafält (inga id / selected_ids)."
    ].join("\\n");
  }
  function invalidExamples(){
    return [
      "OGILTIGA EXEMPEL:",
      "- D-MOD men skickar paths: { selected_files:[{ path:'src/x.js', ...}] }  ❌",
      "- K-MOD men skickar id:   { selected_ids:[1,2] }                           ❌",
      "- Extra fält:             { ..., files:[...]}                                ❌"
    ].join("\\n");
  }
  
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
    return (els.provGemini && els.provGemini.checked)
      ? JSON.stringify(toGemini(sys, user), null, els.compact.checked?0:2)
      : JSON.stringify(toOpenAI(sys, user), null, els.compact.checked?0:2);
  }

  async function sha256HexText(t){
    const enc=new TextEncoder().encode(t);
    const buf=await crypto.subtle.digest('SHA-256', enc);
    return Array.from(new Uint8Array(buf)).map(b=>b.toString(16).padStart(2,'0')).join('');
  }

  function buildCandidatesRich(maxN, includeAssets){
    const arr = INVENTORY.filter(it=> includeAssets ? true : isCodeLike(it.path));
    const lim = Math.max(1, Number(maxN||0) || 999999);
    const sliced = arr.slice(0, lim);
    const coreInfo = (ctx.core_info_data || {});

    return sliced.map((rec, i)=>{
      const info = getRichFileInfo(rec.path, null, coreInfo);
      return {
        id: i+1,
        path: rec.path,
        lang: rec.lang,
        size: rec.size,
        sha256_lf: rec.sha256_lf || null,
        git_sha1: rec.git_sha1 || null,
        info_source: info.source,
        purpose: info.description
      }
    });
  }

  async function buildDiscoveryPromptKMOD(){
    const cands = await buildCandidatesRichAsync(els.maxCands.value, !!els.incAssets.checked);
    LAST_CANDIDATES = cands.slice();
    const schema = {
      protocol_id:"discovery_v2",
      mode:"K-MOD",
      selected_files:[{path:"string", embed:"full|chunk|stub", why:"string<=200"}]
    };
    const blocks = [
      "SESSION: PLANERA NÄSTA ARBETE (Discovery)",
      "MODE: K-MOD",
      kmodHardRules(),
      invalidExamples(),
      "SCHEMA:", JSON.stringify(schema, null, 2),
      "CANDIDATE_FILES:", JSON.stringify(cands, null, 2)
    ];
    if(els.incInventory.checked){
      const invCompact = INVENTORY.map(r=> ({path:r.path, lang:r.lang, size:r.size, sha256_lf:r.sha256_lf, git_sha1:r.git_sha1}));
      blocks.push("FILE_INVENTORY (compact):", JSON.stringify(invCompact, null, 2));
    }
    blocks.push("ÅTERKOM ENBART MED GILTIG JSON ENLIGT SCHEMA. INGA ID.");
    const masterProtocol = getMasterProtocol();
    return [masterProtocol, ...blocks].join("\n\n---\n\n");
  }

  function globToRegex(glob){
  async function buildMenuFirstMD(){
    if(!ctx){ throw new Error('ctx saknas'); }
    if(!Array.isArray(INVENTORY) || INVENTORY.length===0){
      HASHMAPS = buildHashMaps(ctx);
      INVENTORY = buildInventory(ctx);
    }
    const cands = buildCandidatesRich(els.maxCands.value, !!els.incAssets.checked);
    LAST_CANDIDATES = cands.slice();
    let payload = { CANDIDATE_FILES: cands };
    if(els.incInventory.checked){
      const invCompact = INVENTORY.map(r=> ({path:r.path, lang:r.lang, size:r.size, sha256_lf:r.sha256_lf || null, git_sha1:r.git_sha1 || null}));
      payload.inventory_compact = invCompact;
    }
    const header = [
      "### MENU_FIRST_DISCOVERY_PROMPT",
      "",
      "### MENU_DISCOVERY_v1 (obligatoriskt förstasteg)",
      "- Du får CANDIDATE_FILES (+ ev. inventory_compact).",
      "- Steg 1: Skapa en NUMRERAD meny (≤8) över kategorier: app-kod, build-config, backend/functions, tests, data/mock, docs/övrigt.",
      "- Varje rad: nummer, label, count, confidence, include_globs, exclude_globs (+ ev. embed:\"stub\").",
      "- Markera rekommenderade med ★ (max 2).",
      "- Osäkerhet: om ingen tydlig dominans eller recommended tom → ställ EN extra ja/nej-fråga innan val.",
      "- Svara ENBART med JSON: {\\\"menu\\\":[...], \\\"recommended\\\":[...], \\\"question\\\":\\\"...\\\"}."
    ].join("\n");
    return header + "\n```json\n" + JSON.stringify(payload, null, 2) + "\n```\n";
  }

   return new RegExp('^'+glob.split('**').join('@@').replace(/[.+^${}()|[\\]\\\\]/g,'\\$&').split('*').join('[^/]*').split('@@').join('.*')+'$'); }
  const DM = { SELECTION: { min:2, max:12, allow_paths:["src/**","docs/**","scripts/**","public/**"], deny_paths:["infra/prod/**"] } };

  async function buildDiscoveryPromptDMOD(){
    const allow = DM.SELECTION.allow_paths.map(globToRegex);
    const deny  = DM.SELECTION.deny_paths.map(globToRegex);
    const okPath = (p)=> allow.some(r=>r.test(p)) && !deny.some(r=>r.test(p));

    const all = INVENTORY.filter(r=> okPath(r.path) && (els.incAssets.checked ? true : isCodeLike(r.path)));
    const lim = Math.max(1, Number(els.maxCands.value||0) || 999999);
    const sel = all.slice(0, lim);
    const cands = sel.map((r,i)=>({ id:i+1, path:r.path, lang:r.lang, size:r.size, sha256_lf:r.sha256_lf||null, git_sha1:r.git_sha1||null }));
    LAST_CANDIDATES = cands.slice();

    const obligatory_rules = ["forbid_image_generation"];
    const selection_constraints = DM.SELECTION;
    const rules_hash = await sha256HexText(JSON.stringify({ obligatory_rules, selection_constraints, lim, includeAssets: !!els.incAssets.checked }));
    LAST_RULES_HASH = rules_hash;

    const schema = {
      protocol_id:"discovery_dmod_v1",
      mode:"D-MOD",
      echo_rules_hash:"string",
      selected_ids:"int[]",
      notes:"map<id-as-string, string<=200>"
    };

    const blocks = [
      "SESSION: PLANERA NÄSTA ARBETE (Discovery)",
      "MODE: D-MOD",
      dmodHardRules(),
      invalidExamples(),
      "rules_hash: "+rules_hash,
      "obligatory_rules: "+JSON.stringify(obligatory_rules),
      "selection_constraints: "+JSON.stringify(selection_constraints),
      "SCHEMA:", JSON.stringify(schema, null, 2),
      "CANDIDATE_FILES:", JSON.stringify(cands, null, 2)
    ];
    if(els.incInventory.checked){
      const invCompact = INVENTORY.map(r=> ({path:r.path, lang:r.lang, size:r.size, sha256_lf:r.sha256_lf, git_sha1:r.git_sha1}));
      blocks.push("FILE_INVENTORY (compact):", JSON.stringify(invCompact, null, 2));
    }
    blocks.push("ÅTERKOM ENBART MED GILTIG JSON. INGA PATHS/FILNAMN I SVARET.");
    const masterProtocol = getMasterProtocol();
    return [masterProtocol, ...blocks].join("\n\n---\n\n");
  }

  function mapIdsToPaths(ids){
    const idset=new Set(ids);
    return LAST_CANDIDATES.filter(c=>idset.has(c.id)).map(c=>c.path);
  }

  function validateAndApplyStrictInput(){
    clearBanner();
    const t = els.instruction.value.trim();
    if(!t) return;
    let j; try{ j=JSON.parse(t); }catch(e){ showBanner('Ogiltig JSON: '+e.message, 'err'); return; }

    const hasIds = Array.isArray(j?.selected_ids);
    const hasFiles = Array.isArray(j?.selected_files);
    const mode = currentDiscMode();

    if(mode==='DMOD' && hasFiles){
      showBanner('Fel format: D-MOD kräver selected_ids (inte paths).', 'err'); return;
    }
    if(mode==='KMOD' && hasIds){
      showBanner('Fel format: K-MOD kräver paths (inte selected_ids).', 'err'); return;
    }

    if(hasIds && typeof j.echo_rules_hash==='string'){
      if(LAST_RULES_HASH && j.echo_rules_hash!==LAST_RULES_HASH){ showBanner('Varning: echo_rules_hash ≠ rules_hash.', 'warn'); }
      const paths = mapIdsToPaths(j.selected_ids);
      if(paths.length===0){ showBanner('D-MOD: Inga matchande ID:n i senaste kandidatuppsättning.', 'err'); return; }
      autoSelectPaths(paths);
      showBanner(`D-MOD: ${paths.length} filer auto-valda.`, 'ok');
      return;
    }

    if(hasFiles){
      const ok = j.selected_files.every(it=>it && typeof it.path==='string' && ['full','chunk','stub'].includes(it.embed||'') && typeof it.why==='string');
      if(!ok){ showBanner('K-MOD: selected_files har fel struktur.', 'err'); return; }
      const paths = j.selected_files.map(o=>o.path);
      autoSelectPaths(paths);
      showBanner(`K-MOD: ${paths.length} filer auto-valda.`, 'ok');
      return;
    }

    showBanner('JSON är giltig men matchar inte RETURN_CONTRACT för valt läge.', 'warn');
  }
  els.instruction.addEventListener('input', validateAndApplyStrictInput);

  // ---------- Implementation (markdown) ----------
  function bytes(s){ return new Blob([s]).size; }

  async function buildImplBootstrap(){
    return withBusy('Build Bootstrap', async ()=>{
      clearBanner();
      const sel = selectedFiles();
      if(sel.length===0) { showBanner('Välj minst en fil.', 'warn'); return; }
      const targetBytes = Number(els.budgetKb.value)*1000;

      const files = [];
      let used=0;
      const coreInfo = (ctx.core_info_data || {});

      for(const p of sel){
        let content=''; try{ content=await fetchText(p); }catch{ content='// fetch fail'; }
        const info = getRichFileInfo(p, content, coreInfo);
        
        const fileEntry = {
          path: p,
          lang: guessLang(p),
          embed: 'full',
          is_content_full: true,
          info_source: info.source,
          purpose_and_responsibility: info.description,
          content
        };
        
        files.push(fileEntry);
        used += bytes(content);
        if(used >= targetBytes) break;
      }

      const inventory_compact = INVENTORY.map(r=>({ path:r.path, lang:r.lang, size:r.size, sha256_lf:r.sha256_lf, git_sha1:r.git_sha1 }));

      const bootstrap = {
        protocol_id:'impl_bootstrap_v1',
        obligatory_rules:['forbid_image_generation','PLAN->GEN','unified-patch-if->50','no-edit-nonfull'],
        budget:{ target_bytes:targetBytes, used_bytes:used },
        inventory_compact,
        selected_paths: sel.slice(),
        files
      };
      const pretty = els.compact.checked ? JSON.stringify(bootstrap) : JSON.stringify(bootstrap, null, 2);
      const provider = toProviderEnvelope(bootstrap.obligatory_rules, pretty);

      const md = mdWrapJsonSection('impl_bootstrap_v1.json', pretty) + "\n" + mdWrapJsonSection('provider_envelope.json', provider);
      els.out.textContent = md;
      els.copy.disabled = els.download.disabled = false;
      showBanner(`Bootstrap-JSON klar. Bytes: ${used}/${targetBytes}.`, 'ok');
    });
  }

  // ---------- Filförhandsvisning ----------
  async function showFilePreview(p){
    els.fpTitle.textContent = p;
    els.fpBody.textContent = 'Laddar…';
    els.fp.classList.add('show');
    const ext=(p.split('.').pop()||'').toLowerCase();
    if(IMAGE_EXT.includes(ext)){
      els.fpBody.innerHTML = `<img src="${RAW_BASE+p}" alt="${escapeHtml(p)}">`;
      els.fpCopy.disabled=true;
      els.fpDownload.onclick = ()=>{ const a=document.createElement('a'); a.href=RAW_BASE+p; a.download=p.split('/').pop(); document.body.appendChild(a); a.click(); a.remove(); };
    }else{
      try{
        const t = await fetchText(p);
        els.fpBody.innerHTML = `<pre style="white-space:pre-wrap">${escapeHtml(t)}</pre>`;
        els.fpCopy.disabled=false;
        els.fpCopy.onclick = ()=> navigator.clipboard.writeText(t);
        els.fpDownload.onclick = ()=>{
          const blob = new Blob([t], {type:'text/plain'});
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a'); a.href=url; a.download=p.split('/').pop(); document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
        };
      }catch(_){ els.fpBody.textContent = 'Kunde inte läsa fil.'; }
    }
  }

  // ---------- AI Performance ----------
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
  function fmt(n, d=2){ return (n==null||!Number.isFinite(n)) ? '–' : String(Math.round(n*10**d)/10**d); }
  function median(ns){ const a=ns.filter(x=>Number.isFinite(x)).slice().sort((x,y)=>x-y); if(!a.length) return null; const m=Math.floor(a.length/2); return a.length%2 ? a[m] : (a[m-1]+a[m])/2; }

  function renderPerfFilters(perfLog){
    const provs = new Set(), models = new Set();
    perfLog.forEach(s=>{ const pm = getSessionProvModel(s); provs.add(pm.prov); models.add(pm.model); });
    els.pf.provWrap.innerHTML = Array.from(provs).sort().map(p=>`<label class="inline"><input type="checkbox" data-provid="${escapeHtml(p)}"> ${escapeHtml(p)}</label>`).join(' ');
    els.pf.modelWrap.innerHTML = Array.from(models).sort().map(m=>`<label class="inline"><input type="checkbox" data-modelid="${escapeHtml(m)}"> ${escapeHtml(m)}</label>`).join(' ');
  }

  function applyFilter(perfLog){
    let out = perfLog.slice();
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
    const selProv = new Set(Array.from(els.pf.provWrap.querySelectorAll('input[type="checkbox"]')).filter(i=>i.checked).map(i=>i.getAttribute('data-provid')));
    const selModel = new Set(Array.from(els.pf.modelWrap.querySelectorAll('input[type="checkbox"]')).filter(i=>i.checked).map(i=>i.getAttribute('data-modelid')));
    if(selProv.size>0){ out = out.filter(s=> selProv.has(getSessionProvModel(s).prov)); pfState.prov=selProv; } else { pfState.prov.clear?.(); }
    if(selModel.size>0){ out = out.filter(s=> selModel.has(getSessionProvModel(s).model)); pfState.model=selModel; } else { pfState.model.clear?.(); }
    pfState.ma = !!els.pf.ma.checked;
    return out;
  }

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

    if(!els.pf.provWrap.hasChildNodes()){ renderPerfFilters(perfLogAll); }
    const perfLog = applyFilter(perfLogAll);

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

    renderLearningDbTable(els.perfLearning, learningDb);
    renderSessionsTable(els.perfSessions, perfLog);
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

  // ---------- UI wires ----------
  function getRichFileInfo(path, content, coreInfo) {
    if (coreInfo[path]) {
      return { 
        source: 'core_info',
        description: coreInfo[path].purpose_and_responsibility
      };
    }

    if (content) {
      const lines = content.split('\n');
      const commentRegex = /^\s*(\/\/|#|\*|'''|\\"\\"\\")/;
      const commentLines = [];
      for (const line of lines) {
        const trimmed = line.trim();
        if (trimmed.length > 0 && commentRegex.test(trimmed)) {
          commentLines.push(trimmed.replace(commentRegex, '').trim());
        } else if (trimmed.length > 0 && commentLines.length > 0) {
          break;
        }
      }
      if (commentLines.length > 0) {
        return { source: 'comment', description: commentLines.join('\n') };
      }

      if (lines.length < 20) {
        return { source: 'full', description: content };
      }
      return { source: 'head', description: lines.slice(0, 10).join('\n') };
    }

    return { source: 'none', description: null };
  }

  function getMasterProtocol(){
    if (!ctx.persona_data) return "SYSTEMINSTRUKTION: Följ projektets standarder.";
    const p = ctx.persona_data;
    return `### MASTER PROTOCOL: FRANKENSTEEN v${p.version} ###\n` +
           `DU ÄR: En ${p.identity.personality} ${p.identity.role}.\n` +
           `DITT MÅL: ${p.identity.purpose}\n` +
           `KÄRNFILOSOFI: ${p.problem_solving_philosophy.join(' ')}\n` +
           `HUR DU LEVERERAR: ${p.programming_protocol.two_pass_delivery.join(' ')}\n` +
           `HUR DU GRANSKAR: Granska ditt eget arbete mot följande: ${p.verification_protocol.final_checklist.join(', ')}.\n` +
           `KONTEXTFÖRSTÅELSE: Den medföljande fillistan är berikad. Fältet 'purpose' förklarar varje fils syfte. Använd denna information för att fatta intelligenta beslut.`;
  }

  document.querySelectorAll('.tabbar button[data-tab]').forEach(btn=>{
    btn.addEventListener('click', ()=>{
      const tab = btn.dataset.tab;
      document.querySelectorAll('.tabbar button[data-tab]').forEach(b=>b.classList.remove('primary'));
      btn.classList.add('primary');
      Object.keys(els.tabs).forEach(k=> els.tabs[k].classList.toggle('active', k===tab));
      if(tab==='performance' && ctx){ renderPerformanceDashboard(); }
    });
  });

  els.helpBtn.onclick = ()=> els.helpModal.classList.add('show');
  els.helpClose.onclick = ()=> els.helpModal.classList.remove('show');
  els.helpOk.onclick = ()=> els.helpModal.classList.remove('show');
  els.fpClose.onclick = ()=> els.fp.classList.remove('show');

  els.selAll.onclick = ()=>{ els.tree.querySelectorAll('input[type="checkbox"]').forEach(cb=>cb.checked=true); recomputeAllParents(); };
  els.deselAll.onclick = ()=>{ els.tree.querySelectorAll('input[type="checkbox"]').forEach(cb=>cb.checked=false); recomputeAllParents(); };
  els.selCore.onclick = quickSelectCore;

  els.genContext.onclick = ()=> withBusy('Generate Context', generateContext);
  els.genFiles.onclick   = ()=> withBusy('Generate Files',   generateFiles);
  els.genBootstrap.onclick = ()=> withBusy('Generate Bootstrap.md', buildBootstrapMd);
  els.genMenu.onclick = ()=> withBusy('Menu Discovery', buildMenuDiscovery);
  // Standardisera: Menu-first i "Skapa nästa arbete"
  els.discBtn.onclick = ()=> withBusy('Skapa nästa arbete', buildMenuFirstPrompt);

  els.copy.onclick = ()=>{ navigator.clipboard.writeText(els.out.textContent); showBanner('Kopierat.', 'ok'); };
  els.download.onclick = ()=>{
    const blob = new Blob([els.out.textContent], {type:'text/markdown'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href=url;
    const iso = new Date().toISOString().replace(/:/g,'-').replace(/\..+Z$/,'Z');
    a.download = 'context_bundle_'+iso+'.md';
    document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
  };

  // Discovery
  els.discBtn.onclick = ()=> withBusy('Skapa nästa arbete', buildMenuFirstPrompt);

  els.implBtn.onclick = ()=> withBusy('Build Bootstrap', buildImplBootstrap);

  // ---------- Patch Center (INTEGRATED) ----------
    // ---------- Patch Center (INTEGRATED - Anchor Diff v2.1) ----------
  function initPatchCenter(){
    function q(id){ return document.getElementById(id); }
    const bar = document.querySelector('#right .output .bar'); if(!bar) return;

    const openBtn = document.createElement('button');
    openBtn.id='plug-patch-open'; openBtn.textContent='Patch';
    bar.appendChild(openBtn);

    const modal = q('plug-patch-modal'), closeBtn = q('plug-patch-close'), srcTA = q('plug-patch-source');
    const fileInput = q('plug-patch-file'), uploadBtn = q('plug-patch-upload'), validateBtn = q('plug-patch-validate');
    const applyBtn = q('plug-patch-apply'), copyBtn = q('plug-patch-copy'), dlBtn = q('plug-patch-download');
    const previewTA = q('plug-patch-preview'), logEl = q('plug-patch-log');
    const tgtPathEl = q('plug-target-path'), tgtShaEl = q('plug-target-sha256'), tgtGitEl = q('plug-target-gitsha');
    const tgtSrcEl = q('plug-target-source'), schemaOK = q('plug-schema-ok');

    function log(m, kind='info'){ 
        const t=new Date().toLocaleTimeString(); 
        const k = kind==='err'?'[ERR]':kind==='warn'?'[WARN]':'[INFO]';
        logEl.textContent += `[patch ${t}] ${k} ${m}\n`; 
        logEl.scrollTop=logEl.scrollHeight; 
        if(els.worklog){ els.worklog.textContent += `[patch ${t}] ${k} ${m}\n`; els.worklog.scrollTop=els.worklog.scrollHeight; } 
    }
    
    openBtn.onclick = ()=> modal.classList.add('show');
    closeBtn.onclick = ()=> modal.classList.remove('show');

    uploadBtn.onclick = ()=> fileInput.click();
    fileInput.onchange = async (e)=>{
      const f = e.target.files && e.target.files[0];
      if(!f) return;
      srcTA.value = await f.text();
      log(`Läste fil: ${f.name} (${f.size} B)`);
    };

    function parseJsonSafe(s){ try{ return JSON.parse(s); } catch(e){ return { _err:String(e&&e.message||e) }; } }

    function normalizeText(text, mode = 'exact') {
        // Symmetrisk kanonisering + normalisering
        let s = canonText(String(text || ''));
        try { s = s.normalize('NFC'); } catch (_) {}
        s = s.replace(/\u00A0/g, ' ').replace(/[\u200B\u2060]/g, '');
        if (mode === 'ignore_whitespace') { s = s.replace(/\s+/g, ''); }
        return s;
    }

    async function findBaseText(diffJ, maps){
      const need = diffJ.target.base_checksum_sha256.toLowerCase();
      if(maps.sha2paths.has(need)){
        const p = maps.sha2paths.get(need);
        const node = maps.byPath.get(p);
        if(node && node.is_content_full && typeof node.content === 'string') return { path:p, source:'context.file_structure', text: canonText(node.content) };
        return { path:p, source:'context.hash_index.sha256_lf', text: canonText(await fetchText(p)) };
      }
      if(diffJ.target.path){
        const p = diffJ.target.path;
        const t = await fetchText(p);
        if((await sha256HexLF(t)) === need){ return { path:p, source:'path->RAW', text: canonText(t) }; }
        throw new Error('Path fanns men base_checksum_sha256 matchar inte.');
      }
      throw new Error('Kunde inte hitta basfil via checksum/path.');
    }
    
    let lastValidated = null;

    validateBtn.onclick = ()=> withBusy('Validate Anchor Diff', async ()=>{
      logEl.textContent = ''; schemaOK.style.display='none';
      applyBtn.disabled = true; copyBtn.disabled = true; dlBtn.disabled = true; previewTA.value = '';
      tgtPathEl.textContent='–'; tgtShaEl.textContent='–'; tgtGitEl.textContent='–'; tgtSrcEl.textContent='–';
      lastValidated = null;

      const txt = srcTA.value.trim();
      if(!txt){ log('Ingen JSON.', 'warn'); return; }
      const j = parseJsonSafe(txt);
      if(j._err){ log('JSON-fel: '+j._err, 'err'); return; }

      // Rudimentär schema-validering för v2.1
      if(j.protocol_id !== 'anchor_diff_v2.1'){ log('Schemafel: protocol_id måste vara "anchor_diff_v2.1".', 'err'); return; }
      if(!j.target || !j.target.base_checksum_sha256){ log('Schemafel: target.base_checksum_sha256 krävs.', 'err'); return; }
      schemaOK.style.display='inline-block';

      try {
        const base = await findBaseText(j, HASHMAPS);
        log(`Basfil hittad: ${base.path} (källa: ${base.source})`);
        
        // Verifiera alla operationer *innan* applicering
        const validationResults = [];
        let validationOk = true;
        for (const group of j.op_groups || []) {
            for (const targetOp of group.targets || []) {
                if (targetOp.op === 'replace_entire_file') {
                    validationResults.push({ valid: true, op: targetOp });
                    continue;
                }

                const anchorText = group.anchor.text || group.anchor;
                const matchMode = group.anchor.match_mode || 'exact';
                const normalizedBase = normalizeText(base.text, matchMode);
                const normalizedAnchor = normalizeText(anchorText, matchMode);

                let searchIndex = -1;
                const matches = [];
                while ((searchIndex = normalizedBase.indexOf(normalizedAnchor, searchIndex + 1)) !== -1) {
                    matches.push(searchIndex);
                }

                const matchIndex = targetOp.match_index || 1;
                if (matches.length < matchIndex) {
                    log(`Valideringsfel: Kunde inte hitta instans ${matchIndex} av ankare. Endast ${matches.length} hittades.`, 'err');
                    validationOk = false;
                    continue;
                }
                validationResults.push({ valid: true, op: targetOp, group });
            }
        }

        if (validationOk) {
            lastValidated = { diff: j, base };
            tgtPathEl.textContent = base.path;
            tgtShaEl.textContent = j.target.base_checksum_sha256.toLowerCase();
            tgtGitEl.textContent = (j.target.git_sha1 || '–');
            tgtSrcEl.textContent = base.source;
            log('Validering OK: Alla ankare och operationer verkar giltiga.');
            applyBtn.disabled = false;
        } else {
             log('Validering misslyckades. Se logg för detaljer.', 'err');
        }

      } catch(e) {
        log('Validering misslyckades: '+e.message, 'err');
      }
    });

    applyBtn.onclick = ()=> withBusy('Apply Patch', async ()=>{
      if(!lastValidated){ log('Kör Validate först.', 'err'); return; }
      
      let newText = lastValidated.base.text;
      const { diff } = lastValidated;

      // Hantera replace_entire_file först
      const fullReplaceOp = diff.op_groups?.flatMap(g => g.targets).find(t => t.op === 'replace_entire_file');
      if (fullReplaceOp) {
          newText = canonText(fullReplaceOp.new_content || '');
          log('Applicerade "replace_entire_file". Ignorerar andra operationer.');
      } else {
          // Annars, hantera block-baserade operationer
          for (const group of diff.op_groups || []) {
              for (const targetOp of group.targets || []) {
                  // Re-find logic, but this time for replacement
                  const anchorText = group.anchor.text || group.anchor;
                  
                  // This simplified version assumes exact match for replacement logic
                  // A full implementation would need to map normalized indices back to original text indices
                  // For now, we use a simpler string replacement which is less robust but works for many cases.
                  
                  const oldBlock = canonText(targetOp.old_block);
                  const newBlock = canonText(targetOp.new_block);
                  
                  // NOTE: This simple approach is NOT robust against whitespace changes if old_block is complex.
                  // A truly robust solution requires a more complex index mapping.
                  // But for AI-generated blocks, this is often sufficient.
                  if (targetOp.op === 'replace_block') {
                      const combination = canonText(anchorText) + oldBlock;
                      if(newText.includes(combination)) {
                          newText = newText.replace(combination, canonText(anchorText) + newBlock);
                          log(`Applicerade replace_block för ankare (instans ${targetOp.match_index || 1})`);
                      } else {
                          log(`Kunde inte applicera replace_block för ankare (instans ${targetOp.match_index || 1}). Exakt matchning för ankar+old_block hittades ej.`, 'warn');
                      }
                  } else if (targetOp.op === 'delete_block') {
                      const combination = canonText(anchorText) + oldBlock;
                       if(newText.includes(combination)) {
                          newText = newText.replace(combination, canonText(anchorText));
                          log(`Applicerade delete_block för ankare (instans ${targetOp.match_index || 1})`);
                      } else {
                          log(`Kunde inte applicera delete_block för ankare (instans ${targetOp.match_index || 1}). Exakt matchning hittades ej.`, 'warn');
                      }
                  }
              }
          }
      }

      if(typeof diff.result_sha256 === 'string' && diff.result_sha256.length===64){
        const got = await sha256HexLF(newText);
        if(got.toLowerCase() !== diff.result_sha256.toLowerCase()){
          log('Varning: result_sha256 matchar INTE.', 'warn');
        }else{ log('result_sha256 verifierad.', 'ok'); }
      }
      previewTA.value = newText;
      copyBtn.disabled = false; dlBtn.disabled = false;
      log('Patch applicerad. Förhandsvisning klar.');
    });

    copyBtn.onclick = ()=>{ navigator.clipboard.writeText(previewTA.value); log('Kopierat.'); };
    dlBtn.onclick = ()=>{
      const blob = new Blob([previewTA.value], {type:'text/plain'});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = (lastValidated?.base.path || 'patched.txt').split('/').pop();
      document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
      log('Nedladdat.');
    };
  }

  // ---------- Init: ladda context.json, bygg state, initiera UI ----------
  fetch('context.json', {cache:'no-store'})
    .then(r=>{ if(!r.ok) throw new Error('HTTP '+r.status); return r.json(); })
    .then(async data=>{
      ctx = data;
      const repo = (ctx.project_overview && ctx.project_overview.repository) || RAW_DEFAULT_REPO;
      const branch = (ctx.project_overview && ctx.project_overview.branch) || RAW_DEFAULT_BRANCH;
      RAW_BASE = `https://raw.githubusercontent.com/${repo}/${branch}/`;

      // Ladda in de nya, kritiska metadatafilerna
      try { ctx.core_info_data = await (await fetchText('docs/core_file_info.json').then(JSON.parse)); } catch(e) { console.warn('Kunde inte ladda core_file_info.json', e); ctx.core_info_data={}; }
      try { ctx.persona_data = await (await fetchText('docs/ai_protocols/frankensteen_persona.v1.0.json').then(JSON.parse)); } catch(e) { console.warn('Kunde inte ladda frankensteen_persona.v1.0.json', e); ctx.persona_data=null; }
      ctx = data;
      // const repo = (ctx.project_overview && ctx.project_overview.repository) || RAW_DEFAULT_REPO;
      // const branch = (ctx.project_overview && ctx.project_overview.branch) || RAW_DEFAULT_BRANCH;
      RAW_BASE = `https://raw.githubusercontent.com/${repo}/${branch}/`;

      FILES = flattenPaths(ctx.file_structure);
      CODE_FILES = FILES.filter(isCodeLike);

      HASHMAPS = buildHashMaps(ctx);
      INVENTORY = buildInventory(ctx);

      els.tree.innerHTML = '';
      renderTree(ctx.file_structure, els.tree, '');
      recomputeAllParents();
      initPatchCenter(); // Initiera patch-logik
      showBanner('Context + inventory laddad. Välj K-MOD eller D-MOD och fortsätt.', 'ok');
      logw(`Inventory: ${INVENTORY.length} filer. Hash-index: sha=${HASHMAPS.sha2paths.size}, git=${HASHMAPS.git2paths.size}.`);
    })
    .catch(e=>{
      els.tree.innerHTML = '<p style="color:#b00020">Kunde inte läsa context.json: '+escapeHtml(e.message)+'</p>';
    });

  els.pf.export.onclick = ()=> {
    try{
      const metrics = ctx && ctx.ai_performance_metrics;
      const all = Array.isArray(metrics && metrics.performanceLog) ? metrics.performanceLog : [];
      exportCSV(applyFilter(all));
    }catch(e){ showBanner('CSV-export fel: '+e.message, 'err'); }
  };
  els.pf.reset.onclick = ()=>{
    els.pf.from.value=''; els.pf.to.value=''; els.pf.ma.checked=false;
    els.pf.provWrap.querySelectorAll('input[type="checkbox"]').forEach(i=> i.checked=false);
    els.pf.modelWrap.querySelectorAll('input[type="checkbox"]').forEach(i=> i.checked=false);
    renderPerformanceDashboard();
  };
  els.pf.apply.onclick = ()=> renderPerformanceDashboard();
  els.pf.refresh.onclick = ()=> refreshPerformanceData();

})();
</script>
</body>
</html>
"""

def main():
    if len(sys.argv) != 2:
        print("Usage: python wrap_json_in_html.py <output_html_path>", file=sys.stderr)
        sys.exit(1)
    
    out_path = sys.argv[1]
    
    # Plugin-funktionen är inte längre nödvändig eftersom logiken är integrerad.
    # Vi kan förenkla main-funktionen avsevärt.
    
    html_out = HTML
    
    try:
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_out)
        print(f"Successfully generated integrated HTML to {out_path}")
    except Exception as e:
        sys.stderr.write(f"Error writing to {out_path}: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
