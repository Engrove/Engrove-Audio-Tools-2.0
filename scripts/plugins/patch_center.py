# plugins/patch_center.py
# Patch Center plugin för AI Context Builder
# - Klistra/Ladda upp diff.json (diff_json_v1)
# - Automatisk match via sha256_lf (primärt), git_sha1 (sekundärt), path (fallback)
# - Apply → verifiering → redigerbar preview → Copy/Download (exakt kod)

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
  // UI hooks
  function q(id){ return document.getElementById(id); }
  const bar = document.querySelector('#right .output .bar');
  if(!bar) return;

  // Lägg Patch-knapp i output-bar
  const openBtn = document.createElement('button');
  openBtn.id='plug-patch-open'; openBtn.textContent='Patch';
  bar.appendChild(openBtn);

  // Modal element
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

  // Busy overlay / logg (återanvänd bas)
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

  // --- Diff JSON v1 schema (char-baserad) ---
  // {
  //   "protocol_id":"diff_json_v1",
  //   "target":{ "path":"...", "base_checksum_sha256":"<64hex>", "git_sha1":"optional" },
  //   "ops":[ { "op":"replace","at":N,"del":M,"ins":"..." } | {"op":"insert","at":N,"ins":"..."} | {"op":"delete","at":N,"del":M} ]
  // }

  function canonText(s){ return (s||'').replace(/\uFEFF/g,'').replace(/\r\n?/g, '\n'); }

  async function sha256HexLF(text){
    const enc = new TextEncoder().encode(canonText(text));
    const buf = await crypto.subtle.digest('SHA-256', enc);
    return Array.from(new Uint8Array(buf)).map(b=>b.toString(16).padStart(2,'0')).join('');
  }

  function parseJsonSafe(s){
    try{ return JSON.parse(s); } catch(e){ return { _err:String(e&&e.message||e) }; }
  }
  function isHex64(x){ return typeof x==='string' && /^[0-9a-f]{64}$/i.test(x); }

  function validateDiffJson(j){
    if(!j || typeof j!=='object') return 'JSON-objekt saknas.';
    if(j.protocol_id !== 'diff_json_v1') return 'Fel protocol_id (kräver diff_json_v1).';
    if(!j.target || typeof j.target!=='object') return 'target saknas.';
    if(!isHex64(j.target.base_checksum_sha256)) return 'target.base_checksum_sha256 saknas/ogiltig.';
    if(!Array.isArray(j.ops) || j.ops.length===0) return 'ops saknas eller tom.';
    // Kontrollera struktur + ordning
    let lastAt = -1;
    for(const op of j.ops){
      if(!op || typeof op!=='object') return 'ogiltig op i ops.';
      if(op.op==='insert'){
        if(typeof op.at!=='number' || op.at<0) return 'insert.at ogiltig.';
        if(typeof op.ins!=='string') return 'insert.ins saknas.';
      } else if(op.op==='delete'){
        if(typeof op.at!=='number' || op.at<0) return 'delete.at ogiltig.';
        if(typeof op.del!=='number' || op.del<=0) return 'delete.del ogiltig.';
      } else if(op.op==='replace'){
        if(typeof op.at!=='number' || op.at<0) return 'replace.at ogiltig.';
        if(typeof op.del!=='number' || op.del<0) return 'replace.del ogiltig.';
        if(typeof op.ins!=='string') return 'replace.ins saknas.';
      } else {
        return `okänd op: ${op.op}`;
      }
      if(op.at < lastAt) return 'ops måste vara sorterade i stigande at.';
      lastAt = op.at;
    }
    return null;
  }

  // Context.json hash-index
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
    // byPath (för snabb lookup)
    (function walk(node){
      if(node && typeof node==='object'){
        if(node.type==='file' && node.path){ out.byPath.set(node.path, node); }
        else { Object.values(node).forEach(walk); }
      }
    })(ctx.file_structure||{});
    return out;
  }

  async function fetchRaw(path){
    // Försök hämta via GitHub RAW; repo anges i context.json.project_overview
    try{
      const ctx = await fetchContext();
      const repo = (ctx.project_overview&&ctx.project_overview.repository) || 'Engrove/Engrove-Audio-Tools-2.0';
      const branch = (ctx.project_overview&&ctx.project_overview.branch) || 'main';
      const url = `https://raw.githubusercontent.com/${repo}/${branch}/${path}`;
      const r = await fetch(url, {cache:'no-store'});
      if(!r.ok) throw new Error('HTTP '+r.status);
      return await r.text();
    }catch(e){
      throw new Error('RAW fetch misslyckades: '+e.message);
    }
  }

  function parseFilesPayloadFromOut(){
    // Försök hitta inbäddad JSON i #out
    const outTxt = document.getElementById('out')?.textContent || '';
    const m = outTxt.match(/```json([\s\S]*?)```/);
    if(!m) return null;
    try{
      const obj = JSON.parse(m[1]);
      // förväntad struktur: { files: {path:content,...}, checksums?: {path:sha,...} }
      if(obj && obj.files && typeof obj.files==='object'){
        // kanoniserad checksum on-the-fly om saknas
        return obj;
      }
    }catch(_){}
    return null;
  }

  async function findBaseText(diffJ, maps){
    const need = diffJ.target.base_checksum_sha256.toLowerCase();
    // 1) context.hash_index (sha256_lf)
    if(maps.sha256.has(need)){
      const p = maps.sha256.get(need);
      return { path:p, source:'context.hash_index.sha256_lf', text: await resolveTextFromMapsOrRaw(p, maps) };
    }
    // 2) files_payload i #out
    const payload = parseFilesPayloadFromOut();
    if(payload){
      const files = payload.files||{};
      // checksums finns?
      if(payload.checksums && payload.checksums[diffJ.target.path||'']){
        if(payload.checksums[diffJ.target.path] && payload.checksums[diffJ.target.path].toLowerCase()===need){
          return { path:diffJ.target.path, source:'files_payload.checksums', text: canonText(String(files[diffJ.target.path]||'')) };
        }
      }
      // annars beräkna per fil
      const keys = Object.keys(files);
      for(let i=0;i<keys.length;i++){
        const p = keys[i];
        const t = canonText(String(files[p]||''));
        const h = await sha256HexLF(t);
        if(h===need){ return { path:p, source:'files_payload.computed', text:t }; }
      }
    }
    // 3) git_sha1 → path (context)
    if(diffJ.target.git_sha1 && maps.gitsha.has(diffJ.target.git_sha1)){
      const p = maps.gitsha.get(diffJ.target.git_sha1);
      const t = await resolveTextFromMapsOrRaw(p, maps);
      const h = await sha256HexLF(t);
      if(h===need){ return { path:p, source:'git_sha1->RAW', text:t }; }
      // mismatch → inte godkänt
      throw new Error('git_sha1 hittad men base_checksum_sha256 matchar inte innehållet.');
    }
    // 4) path fallback (om specificerad)
    if(diffJ.target.path){
      const p = diffJ.target.path;
      const t = await resolveTextFromMapsOrRaw(p, maps);
      const h = await sha256HexLF(t);
      if(h===need){ return { path:p, source:'path->RAW', text:t }; }
      throw new Error('Path fanns men base_checksum_sha256 matchar inte. Avbryter.');
    }
    throw new Error('Kunde inte hitta basfil via checksum/git_sha1/path.');
  }

  async function resolveTextFromMapsOrRaw(path, maps){
    // Om context redan bär content på filnoden (is_content_full) använd den; annars hämta RAW
    const node = maps.byPath.get(path);
    if(node && node.is_content_full && typeof node.content==='string'){
      return canonText(node.content);
    }
    const t = await fetchRaw(path);
    return canonText(t);
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
    // Ops definierade mot original-index: håll en running offset
    let s = base;
    let shift = 0;
    for(const op of ops){
      const at = op.at|0;
      const idx = at + shift;
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

  function isoName(){ return new Date().toISOString().replace(/:/g,'-').replace(/\..+Z$/,'Z'); }

  // Tillstånd
  let lastDiff = null;
  let lastBase = null;
  let lastPath = null;

  validateBtn.onclick = ()=> withBusy('Validate diff.json', async ()=>{
    logEl.textContent = '';
    applyBtn.disabled = true; copyBtn.disabled = true; dlBtn.disabled = true; previewTA.value = '';
    tgtPathEl.textContent='–'; tgtShaEl.textContent='–'; tgtGitEl.textContent='–'; tgtSrcEl.textContent='–';

    const txt = srcTA.value.trim();
    if(!txt){ log('Ingen JSON.'); return; }
    const j = parseJsonSafe(txt);
    if(j._err){ log('JSON-fel: '+j._err); return; }
    const err = validateDiffJson(j);
    if(err){ log('Validering: '+err); return; }

    try{
      const ctx = await fetchContext();
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
    // Verifiera base_checksum stämde (redan gjort), verifiera ev. result_sha256 om finns
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
    // Filnamn = ursprunglig path:s basename (exakt kod i filen)
    const base = (lastPath || 'patched.txt').split('/').pop();
    a.download = base; // enligt krav: exakt kodinnehåll; filnamn oförändrat
    document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
    log('Download: OK (exakt innehåll).');
  };

})();
"""
