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
    return sliced.map((rec, i)=>({
      id: i+1,
      path: rec.path,
      lang: rec.lang,
      size: rec.size,
      sha256_lf: rec.sha256_lf || null,
      git_sha1: rec.git_sha1 || null
    }));
  }

  async function buildDiscoveryPromptKMOD(){
    const cands = buildCandidatesRich(els.maxCands.value, !!els.incAssets.checked);
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
    return blocks.join("\n");
  }

  function globToRegex(glob){ return new RegExp('^'+glob.split('**').join('@@').replace(/[.+^${}()|[\\]\\\\]/g,'\\$&').split('*').join('[^/]*').split('@@').join('.*')+'$'); }
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
    return blocks.join("\n");
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
      const sel = selectedPaths();
      if(sel.length===0) throw new Error('Välj minst 1 fil.');
      const targetBytes = Number(els.budgetKb.value)*1000;

      const files = [];
      let used=0;
      for(const p of sel){
        let content=''; try{ content=await fetchText(p); }catch{ content='// fetch fail'; }
        files.push({ path:p, lang:guessLang(p), embed:'full', is_content_full:true, content });
        used += bytes(content);
        if(used>=targetBytes) break;
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
      showBanner('Discovery-fel: '+e.message, 'err');
    }
  });

  els.implBtn.onclick = ()=> withBusy('Build Bootstrap', buildImplBootstrap);

  // ---------- Patch Center (INTEGRATED) ----------
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

    function log(m){ const t=new Date().toLocaleTimeString(); logEl.textContent += `[patch ${t}] ${m}\n`; logEl.scrollTop=logEl.scrollHeight; if(els.worklog){ els.worklog.textContent += `[patch ${t}] ${m}\n`; els.worklog.scrollTop=els.worklog.scrollHeight; } }
    
    openBtn.onclick = ()=> modal.classList.add('show');
    closeBtn.onclick = ()=> modal.classList.remove('show');

    uploadBtn.onclick = ()=> fileInput.click();
    fileInput.onchange = async (e)=>{
      const f = e.target.files && e.target.files[0];
      if(!f) return;
      srcTA.value = await f.text();
      log(`Läste fil: ${f.name} (${f.size} B)`);
    };

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
          const typ = op.op, at = op.at;
          if(!isInt(at) || at<0) errs.push(`ops[${i}].at: int>=0`);
          if(at < lastAt && op.op !== 'delete') errs.push('ops måste vara sorterade i stigande at (undantag för efterföljande deletes)'); else if (at >= lastAt) lastAt = at;
          if(typ==='insert'){
            if(!('ins' in op) || typeof op.ins!=='string') errs.push(`ops[${i}].ins saknas (insert)`);
          }else if(typ==='delete'){
            if(!('del' in op) || !isInt(op.del) || op.del<=0) errs.push(`ops[${i}].del>0 krävs (delete)`);
          }else if(typ==='replace'){
            if(!('del' in op) || !isInt(op.del) || op.del<0) errs.push(`ops[${i}].del>=0 krävs (replace)`);
            if(!('ins' in op) || typeof op.ins!=='string') errs.push(`ops[${i}].ins saknas (replace)`);
          }else{ errs.push(`ops[${i}].op okänd: ${typ}`); }
        });
      }
      return errs;
    }

    function parseJsonSafe(s){ try{ return JSON.parse(s); } catch(e){ return { _err:String(e&&e.message||e) }; } }

    function checkOpsRanges(baseLen, ops){
      for(const op of ops){
        const at = op.at|0;
        if(at < 0 || at > baseLen) return `op.at utanför [0, ${baseLen}]`;
        if(op.op==='delete' || op.op==='replace'){
          const del = op.del|0;
          if(del < 0) return 'del negativ.';
          if(at+del > baseLen) return 'del räcker utanför bastext.';
        }
      }
      return null;
    }

    function applyOps(base, ops){
      let s = base, shift = 0;
      ops.sort((a,b)=>a.at - b.at);
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
        }else{ throw new Error('okänd op: '+op.op); }
      }
      return s;
    }

    function parseFilesPayloadFromOut(){
      const m = (els.out.textContent || '').match(/```json([\s\S]*?)```/);
      if(!m) return null;
      try{
        const obj = JSON.parse(m[1]);
        if(obj && obj.files && typeof obj.files==='object'){ return obj; }
      }catch(_){}
      return null;
    }

    async function findBaseText(diffJ, maps){
      const need = diffJ.target.base_checksum_sha256.toLowerCase();
      if(maps.sha2paths.has(need)){
        const p = maps.sha2paths.get(need);
        const node = maps.byPath.get(p);
        if(node && node.is_content_full && typeof node.content === 'string') return { path:p, source:'context.file_structure', text: canonText(node.content) };
        return { path:p, source:'context.hash_index.sha256_lf', text: await fetchText(p) };
      }
      const payload = parseFilesPayloadFromOut();
      if(payload && payload.files){
        const p = diffJ.target.path;
        if(p && payload.checksums && payload.checksums[p] && payload.checksums[p].toLowerCase()===need){
          return { path:p, source:'files_payload.checksums', text: canonText(String(payload.files[p]||'')) };
        }
        for(const path in payload.files){
          const t = canonText(String(payload.files[path]||''));
          if((await sha256HexLF(t)) === need){ return { path, source:'files_payload.computed', text:t }; }
        }
      }
      if(diffJ.target.path){
        const p = diffJ.target.path;
        const t = await fetchText(p);
        if((await sha256HexLF(t)) === need){ return { path:p, source:'path->RAW', text:t }; }
        throw new Error('Path fanns men base_checksum_sha256 matchar inte.');
      }
      throw new Error('Kunde inte hitta basfil via checksum/path.');
    }
    
    let lastDiff = null, lastBase = null, lastPath = null;

    validateBtn.onclick = ()=> withBusy('Validate diff.json', async ()=>{
      logEl.textContent = ''; schemaOK.style.display='none';
      applyBtn.disabled = true; copyBtn.disabled = true; dlBtn.disabled = true; previewTA.value = '';
      tgtPathEl.textContent='–'; tgtShaEl.textContent='–'; tgtGitEl.textContent='–'; tgtSrcEl.textContent='–';

      const txt = srcTA.value.trim();
      if(!txt){ log('Ingen JSON.'); return; }
      const j = parseJsonSafe(txt);
      if(j._err){ log('JSON-fel: '+j._err); return; }

      const schemaErrs = validateAgainstSchema(j);
      if(schemaErrs.length){ log('Schemafel:\n- '+schemaErrs.join('\n- ')); return; }
      schemaOK.style.display='inline-block';

      try{
        const target = await findBaseText(j, HASHMAPS);
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
      const rangeErr = checkOpsRanges(lastBase.length, lastDiff.ops);
      if(rangeErr){ log('Rangefel: '+rangeErr); return; }
      let out;
      try{ out = applyOps(lastBase, lastDiff.ops); }
      catch(e){ log('Apply-fel: '+e.message); return; }
      if(typeof lastDiff.result_sha256 === 'string' && lastDiff.result_sha256.length===64){
        const got = await sha256HexLF(out);
        if(got.toLowerCase() !== lastDiff.result_sha256.toLowerCase()){
          log('Varning: result_sha256 matchar INTE.');
        }else{ log('result_sha256 verifierad.'); }
      }
      previewTA.value = out;
      copyBtn.disabled = false; dlBtn.disabled = false;
      log('Patch applicerad. Förhandsvisning klar.');
    });

    copyBtn.onclick = ()=>{ navigator.clipboard.writeText(previewTA.value); log('Kopierat.'); };
    dlBtn.onclick = ()=>{
      const blob = new Blob([previewTA.value], {type:'text/plain'});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = (lastPath || 'patched.txt').split('/').pop();
      document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
      log('Nedladdat.');
    };
  }

  // ---------- Init: ladda context.json, bygg state, initiera UI ----------
  fetch('context.json', {cache:'no-store'})
    .then(r=>{ if(!r.ok) throw new Error('HTTP '+r.status); return r.json(); })
    .then(data=>{
      ctx = data;
      const repo = (ctx.project_overview && ctx.project_overview.repository) || RAW_DEFAULT_REPO;
      const branch = (ctx.project_overview && ctx.project_overview.branch) || RAW_DEFAULT_BRANCH;
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
