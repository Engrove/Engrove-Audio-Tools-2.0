#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wrap_json_in_html.py

AI Context Builder – v5.0 (Discovery/Implementation för "dum" första-session)
- Laddar context.json, renderar filträd, preview.
- Två knappar: “Skapa nästa arbete” (Steg A, K-MOD) och “Skapa uppgift” (Steg B).
- Steg A prompten bäddar in:
  * PROJECT_CAPSULE (syfte, stack, entry_points, kommandon, invariants)
  * FILE_ROLE_GUESSES (1 rad/fil, heuristik)
  * CANDIDATE_PATHS (hela indexet)
  * SCHEMA + HÅRDA REGLER
- Steg B bootstrap (OpenAI/Gemini) bäddar in:
  * === PROJECT_CAPSULE ===
  * === FILE_ROLES === (endast valda filer)
  * === KONTEXT (fulltext) === (default PÅ)
  * FILER-lista med (is_content_full, lang)
- Bildförbud injiceras alltid (obligatory_rules: forbid_image_generation).
- Validering av Discovery-JSON (inga placeholders, korrekta mängdrelationer).
- Hjälpmodal som förklarar sekvensen.

Körs av GitHub Actions och skriver ut en fristående HTML-fil.
"""

import sys
import os

def create_interactive_html(output_html_path: str) -> None:
    html = r"""<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="UTF-8" />
<title>AI Context Builder v5.0</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
#left{width:40%;min-width:340px}
#right{width:60%;gap:12px}
.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding-bottom:8px;margin-bottom:8px;border-bottom:1px solid var(--line)}
button{border:1px solid var(--line);background:var(--card);color:var(--fg);padding:8px 12px;border-radius:8px;cursor:pointer}
button:hover{background:#eef1f4}
button.primary{background:var(--accent);color:#fff;border-color:var(--accent)}
button.primary:hover{background:var(--accent-2)}
button.info{background:var(--info);color:#fff;border-color:var(--info)}
button.warn{background:var(--warn);color:#000;border-color:var(--warn)}
button:disabled{opacity:.6;cursor:not-allowed}
label.inline{display:inline-flex;align-items:center;gap:6px}

#tree ul{list-style:none;padding-left:18px;margin:0}
#tree li{padding:3px 0}
.toggle{cursor:pointer;user-select:none;display:inline-block;width:1em}
.fileline{display:flex;align-items:center;gap:6px}
pre,textarea{font-family:var(--mono);font-size:14px}
textarea#instruction{height:160px;resize:vertical;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px}
.output{display:flex;flex-direction:column;gap:8px;flex:1}
.output .bar{display:flex;gap:8px}
.output pre{flex:1;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px;white-space:pre-wrap}
.banner{padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:#fff8e1;color:#5c4600;display:none}
.banner.err{background:#fde7ea;color:#7a0e1a}
.banner.ok{background:#eaf7ef;color:#114d27}

.tabbar{display:flex;gap:8px;margin-bottom:10px}
.tabbar button{border-radius:8px}
.tabpanel{display:none}
.tabpanel.active{display:flex;flex-direction:column;gap:12px}

.modal{position:fixed;inset:0;background:rgba(0,0,0,.5);display:none;align-items:center;justify-content:center;z-index:1000}
.modal.show{display:flex}
.modal .box{background:#fff;border-radius:12px;max-width:980px;width:92%;max-height:88vh;display:flex;flex-direction:column}
.modal .box header{display:flex;align-items:center;justify-content:space-between;padding:12px 14px;border-bottom:1px solid var(--line)}
.modal .box main{padding:14px;overflow:auto}
.modal .box footer{padding:10px 14px;border-top:1px solid var(--line);display:flex;justify-content:flex-end;gap:8px}
kbd{background:#f1f3f5;border:1px solid #e9ecef;border-bottom-color:#dee2e6;border-radius:4px;padding:0 4px}
.small{font-size:12px;color:var(--muted)}
.help-steps ol{margin:0 0 0 20px;padding:0}
.help-steps li{margin-bottom:6px}
</style>
</head>
<body>

<section id="left" class="panel">
  <div class="controls">
    <button id="selAll">Select All</button>
    <button id="deselAll">Deselect All</button>
    <button id="selCore">Select Core Docs</button>
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
      <label class="inline" title="Kreativt discovery-läge (ingen kod) i Steg A"><input type="checkbox" id="kmod" checked /> K-MOD i Steg A</label>
      <label class="inline" title="Bäddar in full text för valda filer i bootstrap-prompten"><input type="checkbox" id="embed" checked /> Bädda in fulltext</label>
      <button id="discBtn">Skapa nästa arbete</button>
      <button id="implBtn" class="primary">Skapa uppgift</button>
    </div>

    <textarea id="instruction" placeholder="Skriv kort mål (≤200 tecken) ELLER klistra in Discovery-JSON här…"></textarea>
    <div id="banner" class="banner"></div>

    <div class="output">
      <div class="bar">
        <button id="copy" disabled>Copy JSON</button>
        <button id="download" disabled>Download JSON</button>
      </div>
      <pre id="out">Här visas genererad Discovery-prompt / bootstrap-JSON.</pre>
      <div class="small">JSON här är avsett som <b>första prompt</b> i en ny “dum” modelsession utan kontext.</div>
    </div>
  </div>

  <div id="tab-performance" class="tabpanel">
    <div class="small">Prestandaflik (oförändrad).</div>
  </div>
</section>

<!-- Hjälpmodal -->
<div id="helpModal" class="modal">
  <div class="box">
    <header>
      <b>Hjälp – Rätt arbetssekvens</b>
      <button id="helpClose">✕</button>
    </header>
    <main>
      <div class="help-steps">
        <h4>Steg A – <i>Skapa nästa arbete</i> (Discovery, K-MOD)</h4>
        <ol>
          <li>Skriv målet i en mening.</li>
          <li>Klicka <b>Skapa nästa arbete</b> → prompt med <b>PROJECT_CAPSULE</b>, <b>FILE_ROLE_GUESSES</b>, <b>CANDIDATE_PATHS</b> och schema.</li>
          <li>Kör prompten i modellen. Få <b>Discovery-JSON</b>. Klistra in i rutan → Buildern validerar och autoväljer filer.</li>
          <li>Justera val och kör <b>Generate Context</b> för `context_custom_*.json`.</li>
        </ol>
        <h4>Steg B – <i>Skapa uppgift</i> (Implementation)</h4>
        <ol>
          <li>Välj provider. <b>Bädda in fulltext</b> är PÅ som standard för helt tom session.</li>
          <li>Klicka <b>Skapa uppgift</b> → bootstrap-JSON skapas (system + user) inkl. kapsel, roller och ev. fulltext.</li>
          <li>Använd bootstrap som <b>första prompt</b> i ny session. Flöde: PLAN-JSON → “OK” → GEN-JSON (patch/tester).</li>
        </ol>
        <p class="small"><b>Bildpolicy:</b> aldrig generera bilder om det inte uttryckligen begärs.</p>
      </div>
    </main>
    <footer><button id="helpOk" class="primary">OK</button></footer>
  </div>
</div>

<!-- Förhandsvisning modal -->
<div id="filePreview" class="modal">
  <div class="box">
    <header>
      <b id="fpTitle">Förhandsgranskning</b>
      <div>
        <button id="fpCopy">Copy</button>
        <button id="fpDownload">Download</button>
        <button id="fpClose">✕</button>
      </div>
    </header>
    <main id="fpBody"><p>Laddar…</p></main>
  </div>
</div>

<script>
(function(){
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
    provOpenAI:document.querySelector('input[name="prov"][value="openai"]'),
    provGemini:document.querySelector('input[name="prov"][value="gemini"]'),
    kmod:      document.getElementById('kmod'),
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
  };

  let ctx = null;        // context.json
  let FILES = [];        // alla repo-paths
  let CODE_FILES = [];   // filtrerade (kod/text)

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

  // ---------- Utils ----------
  function showBanner(msg, kind='warn'){
    els.banner.textContent = msg;
    els.banner.className = 'banner ' + (kind==='err'?'err':kind==='ok'?'ok':'');
    els.banner.style.display = 'block';
  }
  function clearBanner(){ els.banner.style.display = 'none'; els.banner.textContent=''; els.banner.className='banner'; }

  function flattenPaths(node, prefix='', out=[]){
    Object.keys(node).sort().forEach(k=>{
      const it = node[k], p = prefix ? `${prefix}/${k}` : k;
      if(it.type==='file'){ out.push(it.path || p); }
      else { flattenPaths(it, p, out); }
    });
    return out;
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

  async function fetchText(path){
    const r = await fetch(RAW+path, {cache:'no-store'});
    if(!r.ok) throw new Error('HTTP '+r.status);
    return await r.text();
  }

  // ---------- Heuristik för roller ----------
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

  function buildFileRoleGuesses(paths, limit=60){
    const out=[];
    const pick = paths.filter(p=>isCodeLike(p)).slice(0, limit);
    pick.forEach(p=> out.push(`- ${p} (${guessLang(p)}): ${inferRole(p)}`));
    // säkerställ några nycklar alltid med:
    [
      'scripts/wrap_json_in_html.py',
      'scripts/generate_full_context.py',
      'package.json',
      'src/app/main.js',
      'src/main.js'
    ].forEach(p=>{
      if(paths.includes(p) && !out.find(line=>line.includes(p))){
        out.unshift(`- ${p} (${guessLang(p)}): ${inferRole(p)}`);
      }
    });
    return out.join("\n");
  }

  async function buildProjectCapsule(){
    // name/purpose/stack heuristik + kommandon från package.json om tillgänglig
    const has = (p)=> FILES.includes(p);
    let name='Engrove Audio Tools';
    let purpose='Webbapp med AI Context Builder (Vue/Vite) + protokollstyrt AI-flöde';
    let stack = [];
    if(has('vite.config.js')) stack.push('Vite');
    if(FILES.some(p=>p.endsWith('.vue'))) stack.push('Vue 3');
    if(FILES.some(p=>p.endsWith('.ts'))) stack.push('TypeScript'); else stack.push('JavaScript');
    if(FILES.some(p=>p.startsWith('scripts/')&&p.endsWith('.py'))) stack.push('Python-scripts');

    const entry = [];
    ['index.html','src/app/main.js','src/main.js','src/app/router.js'].forEach(p=>{ if(has(p)) entry.push(p); });

    // scripts från package.json
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

    const dirs = Array.from(new Set(FILES.map(p=>p.split('/')[0]))).filter(d=>!d.startsWith('.')).slice(0,8);

    const invariants = [
      "PLAN→GEN (PLAN-JSON → OK → GEN-JSON)",
      "Unified patch (>50 rader) när relevant",
      "Ändra ej filer med is_content_full=false",
      "ALDRIG generera bilder utan uttrycklig begäran"
    ];

    const lines = [];
    lines.push(`- name: ${name}`);
    lines.push(`- purpose: ${purpose}`);
    lines.push(`- stack: ${stack.join(', ')}`);
    if(entry.length) lines.push(`- entry_points: ${entry.join(', ')}`);
    lines.push(`- run_cmd: ${run_cmd}`);
    lines.push(`- build_cmd: ${build_cmd}`);
    lines.push(`- test_cmd: ${test_cmd}`);
    lines.push(`- lint_cmd: ${lint_cmd}`);
    lines.push(`- invariants: ${invariants.join(' | ')}`);
    lines.push(`- dirs: ${dirs.join(', ')}`);
    return lines.join("\n");
  }

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
      icon.innerHTML = (it.type==='file'
        ? (IMAGE_EXT.includes((k.split('.').pop()||'').toLowerCase())?'🖼️':'📄')
        : '📁');
      label.appendChild(icon);

      const txt = document.createElement('a'); txt.href='#'; txt.textContent = ' '+k; txt.dataset.path=p;
      label.appendChild(txt);

      li.appendChild(label);
      if(it.type==='file'){
        txt.addEventListener('click', async (e)=>{
          e.preventDefault();
          try{
            els.fpTitle.textContent = p;
            els.fpBody.textContent = 'Laddar…';
            els.fp.classList.add('show');
            const ext=(p.split('.').pop()||'').toLowerCase();
            if(IMAGE_EXT.includes(ext)){
              els.fpBody.innerHTML = `<img src="${RAW+p}" alt="${p}">`;
              els.fpCopy.disabled=true;
              els.fpDownload.onclick = ()=>{ const a=document.createElement('a'); a.href=RAW+p; a.download=p.split('/').pop(); document.body.appendChild(a); a.click(); a.remove(); };
            }else{
              const t = await fetchText(p);
              els.fpBody.innerHTML = `<pre style="white-space:pre-wrap">${escapeHtml(t)}</pre>`;
              els.fpCopy.disabled=false;
              els.fpCopy.onclick = ()=> navigator.clipboard.writeText(t);
              els.fpDownload.onclick = ()=>{
                const blob = new Blob([t], {type:'text/plain'});
                const url = URL.createObjectURL(blob);
                const a=document.createElement('a'); a.href=url; a.download=p.split('/').pop(); document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
              };
            }
          }catch(e){ els.fpBody.textContent = 'Kunde inte läsa fil.'; }
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
      ul.appendChild(li);
    });
    parent.appendChild(ul);
    return ul;
  }

  function escapeHtml(s){ return s.replace(/[&<>"']/g, m=>({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m])); }

  function selectedPaths(){
    return Array.from(els.tree.querySelectorAll('input[type="checkbox"]:checked')).map(cb=>cb.dataset.path);
  }

  function openParentsFor(path){
    const cb = els.tree.querySelector(`input[data-path="${path}"]`);
    if(!cb) return;
    let li = cb.closest('li');
    while(li){
      const parent = li.parentElement.closest('li');
      if(parent){
        const sub = parent.querySelector('ul');
        const toggle = parent.querySelector('.toggle');
        if(sub && toggle){ sub.style.display='block'; toggle.textContent='▼'; }
      }
      li = parent;
    }
  }

  // ---------- Core docs quick select ----------
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
    'docs/Blueprint_för_Migrering_v1_till_v2.md',
    'docs/Engrove_Audio_Toolkit_v2.0_Analys.md',
    'package.json',
    'vite.config.js',
    'scripts/generate_full_context.py',
    'scripts/wrap_json_in_html.py',
    'scripts/history/historical_reconstruction_builder.py'
  ];
  function quickSelectCore(){
    els.tree.querySelectorAll('input[type="checkbox"]').forEach(cb=>cb.checked=false);
    CORE.forEach(p=>{
      const cb = els.tree.querySelector(`input[data-path="${p}"]`);
      if(cb){ cb.checked = true; openParentsFor(p); }
    });
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
      clearBanner();
      const sels = new Set(selectedPaths());
      const out = {
        project_overview: ctx.project_overview,
        ai_instructions: ctx.ai_instructions || {},
        file_structure: {}
      };
      // injicera bildförbud
      const rules = new Set([...(out.ai_instructions.obligatory_rules||[]), 'forbid_image_generation']);
      out.ai_instructions.obligatory_rules = Array.from(rules);
      if(els.instruction.value.trim()) out.ai_instructions_input = els.instruction.value.trim();

      out.file_structure = await buildNewContextNode(ctx.file_structure, sels);
      els.out.textContent = JSON.stringify(out, null, 2);
      els.copy.disabled = els.download.disabled = false;
      showBanner('Context genererad.', 'ok');
    }catch(e){
      showBanner('Fel vid context-generering: '+e.message, 'err');
    }
  }

  async function generateFiles(){
    try{
      clearBanner();
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
      els.out.textContent = JSON.stringify(payload, null, 2);
      els.copy.disabled = els.download.disabled = false;
      showBanner('Filer genererade.', 'ok');
    }catch(e){
      showBanner('Fel vid file-generering: '+e.message, 'err');
    }
  }

  // ---------- Discovery prompt (med kapsel + roller + index + schema) ----------
  function buildDiscoverySchema(task){
    return {
      protocol_id:"discovery_v1",
      psv:["rules_rehearsed","risk_scan"],
      mode: els.kmod.checked ? "K-MOD" : undefined,
      obligatory_rules:["forbid_image_generation"],
      task,
      project_capsule:{},
      file_role_guesses:[],
      filesToSelect:[],
      requires_full_files:[],
      stubs_ok:[],
      requires_chunks:[],
      api_contracts_touched:[],
      risks:[],
      test_plan:[],
      done_when:["tests_green","lint_ok","types_ok"],
      _note:"Lista bara det som krävs. Motivera varje post i requires_full_files i notes (≤200 tecken)."
    };
  }
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
  function buildCandidateBlock(){
    return "CANDIDATE_PATHS:\n"+ FILES.map(p=>`- ${p}`).join("\n");
  }

  function validateDiscoveryJSON(obj){
    const err = [];
    const set = new Set(FILES);
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

  function autoSelectTree(paths){
    const all = Array.from(els.tree.querySelectorAll('input[type="checkbox"]'));
    paths.forEach(p=>{
      const cb = all.find(x=>x.dataset.path===p);
      if(cb){ cb.checked = true; openParentsFor(p); }
    });
  }

  // ---------- Bootstrap (Implementation) ----------
  function toOpenAI(systemText, userText){
    return {
      provider:"openai",
      model:"gpt-5",
      auto_start:true,
      messages:[
        {role:"system", content:systemText},
        {role:"user",   content:userText}
      ]
    };
  }
  function toGemini(systemText, userText){
    return {
      provider:"google",
      model:"gemini-2.5-pro",
      auto_start:true,
      system_instruction:systemText,
      contents:[{role:"user", parts:[{text:userText}]}]
    };
  }

  async function buildUserWithEmbeds(task, selected){
    const list = selected.map(p=>`- ${p} (is_content_full=true, lang=${guessLang(p)})`).join("\n");
    const capsule = await buildProjectCapsule();
    const roles = selected.map(p=>`- ${p}: ${inferRole(p)}`).join("\n");
    let body = `UPPGIFT: ${task}\nFILER:\n${list}\n\n=== PROJECT_CAPSULE ===\n${capsule}\n\n=== FILE_ROLES ===\n${roles}\n`;
    if(els.embed.checked){
      body += "\n=== KONTEXT (fulltext) ===\n";
      for(const p of selected){
        try{
          const t = await fetchText(p);
          body += `\n----- FILE: ${p} BEGIN -----\n${t}\n----- FILE: ${p} END -----\n`;
        }catch(_){
          body += `\n----- FILE: ${p} BEGIN -----\n// Failed to fetch ${p}\n----- FILE: ${p} END -----\n`;
        }
      }
    }
    return body + "PLANERA";
  }

  function getTask(){
    const t = els.instruction.value.trim();
    return (t && t.length<=200) ? t : "Beskriv kort mål i en mening.";
  }

  // ---------- Events ----------
  document.querySelectorAll('.tabbar button[data-tab]').forEach(btn=>{
    btn.addEventListener('click', ()=>{
      const tab = btn.dataset.tab;
      document.querySelectorAll('.tabbar button[data-tab]').forEach(b=>b.classList.remove('primary'));
      btn.classList.add('primary');
      Object.keys(els.tabs).forEach(k=> els.tabs[k].classList.toggle('active', k===tab));
    });
  });

  els.selAll.onclick = ()=> els.tree.querySelectorAll('input[type="checkbox"]').forEach(cb=>cb.checked=true);
  els.deselAll.onclick = ()=> els.tree.querySelectorAll('input[type="checkbox"]').forEach(cb=>cb.checked=false);
  els.selCore.onclick = quickSelectCore;

  els.genContext.onclick = generateContext;
  els.genFiles.onclick = generateFiles;

  els.copy.onclick = ()=>{ navigator.clipboard.writeText(els.out.textContent); showBanner('Kopierat.', 'ok'); };
  els.download.onclick = ()=>{
    const blob = new Blob([els.out.textContent], {type:'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href=url; a.download='context_custom_'+new Date().toISOString().slice(0,10)+'.json';
    document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
  };

  els.discBtn.onclick = async ()=>{
    clearBanner();
    if(!ctx){ showBanner('context.json ej laddad ännu.', 'err'); return; }
    const task = getTask();
    const schema = buildDiscoverySchema(task);
    if(!els.kmod.checked) delete schema.mode;

    // bygg kapsel + filroller + candidate-listr
    const capsule = await buildProjectCapsule();
    const roleGuesses = buildFileRoleGuesses(CODE_FILES, 60);

    const discoveryText = [
      "SESSION: PLANERA NÄSTA ARBETE (Discovery)",
      KMOD_BANNER,
      IMAGE_GUARD_BANNER,
      "KRAV: Svara ENBART med giltig JSON enligt schema. Ingen kod.",
      discoveryHardRules(),
      "SCHEMA:",
      JSON.stringify(schema, null, 2),
      "PROJECT_CAPSULE:",
      capsule,
      "FILE_ROLE_GUESSES:",
      roleGuesses,
      buildCandidateBlock(),
      "KONTEXT-RÅD:",
      "- Lista bara det som verkligen behövs för implementationen i nästa steg.",
      "- Motivera varje post i 'requires_full_files' kort i 'notes' (max 200 tecken)."
    ].join("\n");

    els.out.textContent = discoveryText;
    els.copy.disabled = els.download.disabled = false;
    showBanner('Discovery-prompt skapad. Kör i modell, klistra svaret här.', 'ok');
  };

  els.implBtn.onclick = async ()=>{
    try{
      clearBanner();
      if(!ctx){ showBanner('context.json ej laddad ännu.', 'err'); return; }
      const task = getTask();
      const sel = selectedPaths();
      if(sel.length===0){ showBanner('Välj minst 1 fil (fulltext) i trädet.', 'err'); return; }
      const user = await buildUserWithEmbeds(task, sel);
      const sys  = MUST_STRICT;
      const boot = (els.provGemini.checked) ? toGemini(sys,user) : toOpenAI(sys,user);
      els.out.textContent = JSON.stringify(boot, null, 2);
      els.copy.disabled = els.download.disabled = false;
      showBanner('Bootstrap-JSON klar. Använd som första prompt i en ny, tom session.', 'ok');
    }catch(e){
      showBanner('Fel vid bootstrap: '+e.message, 'err');
    }
  };

  els.instruction.addEventListener('input', ()=>{
    clearBanner();
    const text = els.instruction.value.trim();
    if(!text) return;
    try{
      const obj = JSON.parse(text);
      if(obj && Array.isArray(obj.filesToSelect)){
        const errs = validateDiscoveryJSON(obj);
        if(errs.length){ showBanner('Discovery-JSON varningar: '+errs.join(' | '), 'warn'); }
        autoSelectTree(obj.filesToSelect);
      }
    }catch(_){ /* fri text = task */ }
  });

  // Hjälpmodal
  els.helpBtn.onclick = ()=> els.helpModal.classList.add('show');
  els.helpClose.onclick = ()=> els.helpModal.classList.remove('show');
  els.helpOk.onclick = ()=> els.helpModal.classList.remove('show');
  els.fpClose.onclick = ()=> els.fp.classList.remove('show');

  // ---------- Hämta context.json ----------
  fetch('context.json', {cache:'no-store'})
    .then(r=>{ if(!r.ok) throw new Error('HTTP '+r.status); return r.json(); })
    .then(data=>{
      ctx = data;
      FILES = flattenPaths(ctx.file_structure);
      CODE_FILES = FILES.filter(p=>isCodeLike(p) && !IMAGE_EXT.includes((p.split('.').pop()||'').toLowerCase()));
      els.tree.innerHTML = '';
      renderTree(ctx.file_structure, els.tree, '');
      showBanner('Context laddad. Fortsätt med Steg A eller B.', 'ok');
    })
    .catch(e=>{
      els.tree.innerHTML = '<p style="color:#b00020">Kunde inte läsa context.json: '+e.message+'</p>';
    });

})();
</script>
</body>
</html>
"""
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python wrap_json_in_html.py <output_html_path>", file=sys.stderr)
        sys.exit(1)
    out = sys.argv[1]
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    create_interactive_html(out)
