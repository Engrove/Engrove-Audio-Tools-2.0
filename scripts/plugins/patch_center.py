# plugins/patch_center.py
# Patch Center plugin – inbyggd schema-validering + checksum-match + Apply + preview + Copy/Download
# Körs via wrap_json_in_html.py som injicerar EXTEND_* i HTML.

EXTEND_CSS = r"""
#plug-patch-modal .box{max-width:1100px}
#plug-patch-log{white-space:pre-wrap;border:1px solid #ddd;border-radius:8px;padding:8px;background:#fff;max-height:34vh;overflow:auto}
#plug-patch-target{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
#plug-patch-target .badge{padding:2px 8px;border:1px solid #ccc;border-radius:999px;background:#f6f7f9;font-size:12px}
#plug-patch-preview{width:100%;height:360px}
#plug-patch-source{width:100%;height:160px}
#plug-patch-file{display:none}
"""

EXTEND_BODY = r"""
<!-- Patch Center Modal -->
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
          <label for="plug-patch-source" class="small">Klistra in <kbd>diff.json</kbd> (diff_json_v1) här:</label>
          <textarea id="plug-patch-source" placeholder='{"protocol_id":"diff_json_v1","target":{"base_checksum_sha256":"...","path":"..."},"ops":[...]}'></textarea>
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
"""

EXTEND_JS = r"""
(function(){
  // ---- UI refs ----
  function q(id){ return document.getElementById(id); }
  const bar = document.querySelector('#right .output .bar'); if(!bar) return;

  // Lägg Patch-knapp i output-bar
  const openBtn = document.createElement('button');
  openBtn.id='plug-patch-open'; openBtn.textContent='Patch';
  bar.appendChild(openBtn);

  const modal = q('plug-patch-modal');
  const closeBtn = q('plug-patch-close');
  const srcTA = q('plug-patch-source');
  const fileInput = q('plug-patch-file');
  const uploadBtn = q('plug-patch-upload');
  const validateBtn = q('plug-patch-validate');
  const applyBtn = q('plug-patch-apply');
  const copyBtn = q('plug-patch-copy');
  const dlBtn = q('plug-patch-download');
  const previewTA = q('plug-patch-preview');
  const logEl = q('plug-patch-log');
  const tgtPathEl = q('plug-target-path');
  const tgtShaEl = q('plug-target-sha256');
  const tgtGitEl = q('plug-target-gitsha');
  const tgtSrcEl = q('plug-target-source');
  const schemaOK = q('plug-schema-ok');

  const busy = document.getElementById('busy');
  const worklog = document.getElementById('worklog');
  function log(m){ const t=new Date().toLocaleTimeString(); logEl.textContent += `[patch ${t}] ${m}\n`; logEl.scrollTop=logEl.scrollHeight; if(worklog){ worklog.textContent += `[patch ${t}] ${m}\n`; worklog.scrollTop=worklog.scrollHeight; } }
  async function withBusy(label, fn){
    if(busy){ busy.style.display='flex'; }
    log(label+' start');
    try{ const r = await fn(); log(label+' klar'); return r; }
    finally{ setTimeout(()=>{ if(busy) busy.style.display='none'; }, 120); }
  }

  function open(){ modal.classList.add('show'); }
  function close(){ modal.classList.remove('show'); }

  openBtn.onclick = ()=> open();
  closeBtn.onclick = ()=> close();

  uploadBtn.onclick = ()=> fileInput.click();
  fileInput.onchange = async (e)=>{
    const f = e.target.files && e.target.files[0];
    if(!f) return;
    const txt = await f.text();
    srcTA.value = txt;
    log(`Läste fil: ${f.name} (${f.size} B)`);
  };

  // ---- Schema (inbyggd) ----
  const DIFF_SCHEMA = {
    "$schema":"https://json-schema.org/draft/2020-12/schema",
    "title":"Diff JSON v1",
    "type":"object",
    "additionalProperties": false,
    "required":["protocol_id","target","ops"],
    "properties":{
      "protocol_id":{"const":"diff_json_v1"},
      "target":{
        "type":"object",
        "additionalProperties": false,
        "required":["base_checksum_sha256"],
        "properties":{
          "path":{"type":"string","minLength":1},
          "base_checksum_sha256":{"type":"string","pattern":"^[0-9a-fA-F]{64}$"},
          "git_sha1":{"type":"string","pattern":"^[0-9a-fA-F]{40}$"}
        }
      },
      "ops":{
        "type":"array",
        "minItems":1,
        "items":{
          "oneOf":[
            {"type":"object","additionalProperties":false,"required":["op","at","ins"],"properties":{
              "op":{"const":"insert"},"at":{"type":"integer","minimum":0},"ins":{"type":"string"}}},
            {"type":"object","additionalProperties":false,"required":["op","at","del"],"properties":{
              "op":{"const":"delete"},"at":{"type":"integer","minimum":0},"del":{"type":"integer","minimum":1}}},          
            {"type":"object","additionalProperties":false,"required":["op","at","del","ins"],"properties":{
              "op":{"const":"replace"},"at":{"type":"integer","minimum":0},"del":{"type":"integer","minimum":0},"ins":{"type":"string"}}}
          ]
        }
      },
      "result_sha256":{"type":"string","pattern":"^[0-9a-fA-F]{64}$"},
      "meta":{"type":"object"}
    }
  };

  // Minimal generisk validator för just detta schema (ingen extern lib)
  function isObj(x){ return x && typeof x==='object' && !Array.isArray(x); }
  function isInt(x){ return Number.isInteger(x); }
  function matchRegex(s, re){ return typeof s==='string' && new RegExp(re).test(s); }

  function validateAgainstSchema(j){
    const errs = [];
    if(!isObj(j)) { errs.push('root: måste vara object'); return errs; }
    const req = ['protocol_id','target','ops'];
    req.forEach(k=>{ if(!(k in j)) errs.push(`root.required: ${k}`); });
    if(j.protocol_id!=='diff_json_v1') errs.push('protocol_id måste vara "diff_json_v1"');
    if(!isObj(j.target)) errs.push('target: måste vara object');
    else {
      const t=j.target;
      if(!matchRegex(t.base_checksum_sha256||'', '^[0-9a-fA-F]{64}$')) errs.push('target.base_checksum_sha256: 64 hex krävs');
      if('git_sha1' in t && !matchRegex(t.git_sha1, '^[0-9a-fA-F]{40}$')) errs.push('target.git_sha1: 40 hex');
      if('path' in t && !(typeof t.path==='string' && t.path.length>0)) errs.push('target.path: string>0');
      const extraT = Object.keys(t).filter(k=>!['path','base_checksum_sha256','git_sha1'].includes(k));
      if(extraT.length) errs.push('target.additionalProperties: '+extraT.join(','));
    }
    if(!Array.isArray(j.ops) || j.ops.length<1) errs.push('ops: array med minst 1 post krävs');
    else{
      let lastAt = -1;
      j.ops.forEach((op,i)=>{
        if(!isObj(op)) { errs.push(`ops[${i}]: måste vara object`); return; }
        const typ = op.op;
        const at  = op.at;
        if(!isInt(at) || at<0) errs.push(`ops[${i}].at: int>=0`);
        if(at<lastAt) errs.push('ops måste vara sorterade i stigande at');
        if(typ==='insert'){
          if(!('ins' in op) || typeof op.ins!=='string') errs.push(`ops[${i}].ins saknas (insert)`);
          const extra=Object.keys(op).filter(k=>!['op','at','ins'].includes(k));
          if(extra.length) errs.push(`ops[${i}].additionalProperties: ${extra.join(',')}`);
        }else if(typ==='delete'){
          if(!('del' in op) || !isInt(op.del) || op.del<=0) errs.push(`ops[${i}].del>0 krävs (delete)`);
          const extra=Object.keys(op).filter(k=>!['op','at','del'].includes(k));
          if(extra.length) errs.push(`ops[${i}].additionalProperties: ${extra.join(',')}`);
        }else if(typ==='replace'){
          if(!('del' in op) || !isInt(op.del) || op.del<0) errs.push(`ops[${i}].del>=0 krävs (replace)`);
          if(!('ins' in op) || typeof op.ins!=='string') errs.push(`ops[${i}].ins saknas (replace)`);
          const extra=Object.keys(op).filter(k=>!['op','at','del','ins'].includes(k));
          if(extra.length) errs.push(`ops[${i}].additionalProperties: ${extra.join(',')}`);
        }else{
          errs.push(`ops[${i}].op okänd: ${typ}`);
        }
        lastAt = at;
      });
    }
    const allowedRoot = ['protocol_id','target','ops','result_sha256','meta'];
    const extraRoot = Object.keys(j).filter(k=>!allowedRoot.includes(k));
    if(extraRoot.length) errs.push('root.additionalProperties: '+extraRoot.join(','));
    if('result_sha256' in j && !matchRegex(j.result_sha256,'^[0-9a-fA-F]{64}$')) errs.push('result_sha256: 64 hex');
    if('meta' in j && !isObj(j.meta)) errs.push('meta: måste vara object');
    return errs;
  }

  // ---- Diff JSON (semantisk) ----
  function canonText(s){ return (s||'').replace(/\uFEFF/g,'').replace(/\r\n?/g, '\n'); }
  async function sha256HexLF(text){
    const enc = new TextEncoder().encode(canonText(text));
    const buf = await crypto.subtle.digest('SHA-256', enc);
    return Array.from(new Uint8Array(buf)).map(b=>b.toString(16).padStart(2,'0')).join('');
  }
  function parseJsonSafe(s){
    try{ return JSON.parse(s); } catch(e){ return { _err:String(e&&e.message||e) }; }
  }
  function checkOpsRanges(baseLen, ops){
    let last = -1;
    for(const op of ops){
      const at = op.at|0;
      if(at < 0 || at > baseLen) return `op.at utanför [0, ${baseLen}]`;
      if(at < last) return 'ops måste vara sorterade i stigande at.';
      if(op.op==='delete' || op.op==='replace'){
        const del = op.del|0;
        if(del < 0) return 'del negativ.';
        if(at+del > baseLen) return 'del räcker utanför bastext.';
      }
      last = at;
    }
    return null;
  }
  function applyOps(base, ops){
    let s = base, shift = 0;
    for(const op of ops){
      const at = op.at|0, idx = at + shift;
      if(op.op==='insert'){
        const ins = op.ins||'';
        s = s.slice(0, idx) + ins + s.slice(idx);
        shift += ins.length;
      }else if(op.op==='delete'){
        const del = op.del|0;
        s = s.slice(0, idx) + s.slice(idx+del);
        shift -= del;
      }else if(op.op==='replace'){
        const del = op.del|0, ins = op.ins||'';
        s = s.slice(0, idx) + ins + s.slice(idx+del);
        shift += (ins.length - del);
      }else{
        throw new Error('okänd op: '+op.op);
      }
    }
    return s;
  }

  // ---- context.json + index ----
  async function fetchContext(){
    const r = await fetch('context.json', {cache:'no-store'});
    if(!r.ok) throw new Error('context.json saknas ('+r.status+')');
    return await r.json();
  }
  function buildHashMaps(ctx){
    const out = { sha256:new Map(), gitsha:new Map(), byPath:new Map() };
    const idx = (ctx.hash_index)||{};
    const s256 = idx.sha256_lf || idx.sha256 || {};
    const gsha = idx.git_sha1 || {};
    for(const [k,v] of Object.entries(s256)){ if(Array.isArray(v)) v.forEach(p=> out.sha256.set(k, p)); else if(typeof v==='string') out.sha256.set(k,v); }
    for(const [k,v] of Object.entries(gsha)){ if(Array.isArray(v)) v.forEach(p=> out.gitsha.set(k, p)); else if(typeof v==='string') out.gitsha.set(k,v); }
    (function walk(node){
      if(node && typeof node==='object'){
        if(node.type==='file' && node.path){ out.byPath.set(node.path, node); }
        else { Object.values(node).forEach(walk); }
      }
    })(ctx.file_structure||{});
    return out;
  }
  async function fetchRawFromContextPath(path){
    const ctx = window.__CTX__ || await fetchContext();
    if(!window.__CTX__) window.__CTX__ = ctx;
    const repo = (ctx.project_overview&&ctx.project_overview.repository) || 'Engrove/Engrove-Audio-Tools-2.0';
    const branch = (ctx.project_overview&&ctx.project_overview.branch) || 'main';
    const url = `https://raw.githubusercontent.com/${repo}/${branch}/${path}`;
    const r = await fetch(url, {cache:'no-store'});
    if(!r.ok) throw new Error('HTTP '+r.status);
    return await r.text();
  }
  async function resolveTextFromMapsOrRaw(path, maps){
    const node = maps.byPath.get(path);
    if(node && node.is_content_full && typeof node.content==='string'){
      return canonText(node.content);
    }
    const t = await fetchRawFromContextPath(path);
    return canonText(t);
  }
  function parseFilesPayloadFromOut(){
    const outTxt = document.getElementById('out')?.textContent || '';
    const m = outTxt.match(/```json([\s\S]*?)```/);
    if(!m) return null;
    try{
      const obj = JSON.parse(m[1]);
      if(obj && obj.files && typeof obj.files==='object'){ return obj; }
    }catch(_){}
    return null;
  }
  async function findBaseText(diffJ, maps){
    const need = diffJ.target.base_checksum_sha256.toLowerCase();
    if(maps.sha256.has(need)){
      const p = maps.sha256.get(need);
      return { path:p, source:'context.hash_index.sha256_lf', text: await resolveTextFromMapsOrRaw(p, maps) };
    }
    const payload = parseFilesPayloadFromOut();
    if(payload){
      const files = payload.files||{};
      if(payload.checksums && payload.checksums[diffJ.target.path||'']){
        if(payload.checksums[diffJ.target.path].toLowerCase()===need){
          return { path:diffJ.target.path, source:'files_payload.checksums', text: canonText(String(files[diffJ.target.path]||'')) };
        }
      }
      const keys = Object.keys(files);
      for(let i=0;i<keys.length;i++){
        const p = keys[i];
        const t = canonText(String(files[p]||''));
        const h = await sha256HexLF(t);
        if(h===need){ return { path:p, source:'files_payload.computed', text:t }; }
      }
    }
    if(diffJ.target.git_sha1 && maps.gitsha.has(diffJ.target.git_sha1)){
      const p = maps.gitsha.get(diffJ.target.git_sha1);
      const t = await resolveTextFromMapsOrRaw(p, maps);
      const h = await sha256HexLF(t);
      if(h===need){ return { path:p, source:'git_sha1->RAW', text:t }; }
      throw new Error('git_sha1 hittad men base_checksum_sha256 matchar inte innehållet.');
    }
    if(diffJ.target.path){
      const p = diffJ.target.path;
      const t = await resolveTextFromMapsOrRaw(p, maps);
      const h = await sha256HexLF(t);
      if(h===need){ return { path:p, source:'path->RAW', text:t }; }
      throw new Error('Path fanns men base_checksum_sha256 matchar inte. Avbryter.');
    }
    throw new Error('Kunde inte hitta basfil via checksum/git_sha1/path.');
  }

  // ---- Tillstånd ----
  let lastDiff = null, lastBase = null, lastPath = null;

  // ---- Validate-knappen ----
  validateBtn.onclick = ()=> withBusy('Validate diff.json', async ()=>{
    logEl.textContent = ''; schemaOK.style.display='none';
    applyBtn.disabled = true; copyBtn.disabled = true; dlBtn.disabled = true; previewTA.value = '';
    tgtPathEl.textContent='–'; tgtShaEl.textContent='–'; tgtGitEl.textContent='–'; tgtSrcEl.textContent='–';

    const txt = srcTA.value.trim();
    if(!txt){ log('Ingen JSON.'); return; }
    const j = parseJsonSafe(txt);
    if(j._err){ log('JSON-fel: '+j._err); return; }

    // 1) Formell schema-validering
    const schemaErrs = validateAgainstSchema(j);
    if(schemaErrs.length){ log('Schemafel:\n- '+schemaErrs.join('\n- ')); return; }
    schemaOK.style.display='inline-block';

    // 2) Leta upp bas via checksum
    try{
      const ctx = window.__CTX__ || await fetchContext();
      if(!window.__CTX__) window.__CTX__ = ctx;
      const maps = buildHashMaps(ctx);
      const target = await findBaseText(j, maps);
      lastDiff = j; lastBase = target.text; lastPath = target.path;
      tgtPathEl.textContent = target.path || (j.target && j.target.path) || 'okänd';
      tgtShaEl.textContent = j.target.base_checksum_sha256.toLowerCase();
      tgtGitEl.textContent = (j.target.git_sha1 || '–');
      tgtSrcEl.textContent = target.source;
      log('Validering OK: basfil identifierad.');
      applyBtn.disabled = false;
    }catch(e){
      log('Validering misslyckades: '+e.message);
    }
  });

  // ---- Apply ----
  applyBtn.onclick = ()=> withBusy('Apply', async ()=>{
    if(!lastDiff || !lastBase){ log('Kör Validate först.'); return; }
    const base = lastBase;
    const ops = lastDiff.ops||[];
    const rangeErr = checkOpsRanges(base.length, ops);
    if(rangeErr){ log('Rangefel: '+rangeErr); return; }
    let out;
    try{
      out = applyOps(base, ops);
    }catch(e){
      log('Apply-fel: '+e.message); return;
    }
    if(typeof lastDiff.result_sha256 === 'string' && lastDiff.result_sha256.length===64){
      const got = await sha256HexLF(out);
      if(got.toLowerCase() !== lastDiff.result_sha256.toLowerCase()){
        log('Varning: result_sha256 matchar INTE.');
      }else{
        log('result_sha256 verifierad.');
      }
    }
    previewTA.value = out;
    copyBtn.disabled = false; dlBtn.disabled = false;
    log('Patch applicerad. Förhandsvisning klar.');
  });

  // ---- Copy/Download exakt preview ----
  copyBtn.onclick = ()=>{
    const s = previewTA.value;
    navigator.clipboard.writeText(s);
    log('Copy: OK (exakt innehåll i rutan).');
  };
  dlBtn.onclick = ()=>{
    const s = previewTA.value;
    if(!s){ log('Inget att ladda ner.'); return; }
    const a = document.createElement('a');
    const blob = new Blob([s], {type:'text/plain'});
    const url = URL.createObjectURL(blob);
    a.href = url;
    const base = (lastPath || 'patched.txt').split('/').pop();
    a.download = base; // exakt filnamn
    document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
    log('Download: OK (exakt innehåll).');
  };

})();
"""
