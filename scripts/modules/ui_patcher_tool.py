/**
 * Patch Center Plugin (Standalone) — json_diff
 *
 * Detta skript skapar ett modal-gränssnitt för att applicera json_diff-patchar.
 * Migrerad från anchor_diff_v2.1/v3.0 till json_diff enligt protokollet.
 *
 * @version 2.0.0
 *
 * ÄNDRINGSHISTORIK:
 * - 2.0.0: Migrering till json_diff. Validering mot protocol_id='json_diff'.
 *          Stöd för operations: replace_block, delete_block, replace_entire_file.
 *          match_index (1-baserat) implementerat efter ankarets slut.
 *          Resultatverifiering via result_sha256 om angivet.
 * - 1.0.0: Första fristående versionen med anchor_diff_v2.1/v3.0-stöd.
 *
 * ANVÄNDNING:
 * 1. Inkludera filen i din HTML.
 * 2. Anropa PatchCenterPlugin.init({ hashMaps, rawBaseUrl, onBusyStart, onBusyEnd }).
 * 3. Anropa PatchCenterPlugin.open() för att visa modalen.
 */
const PatchCenterPlugin = {
  // Konfiguration
  config: {
    hashMaps: null,
    rawBaseUrl: '',
    onBusyStart: () => {},
    onBusyEnd: () => {},
  },

  // DOM-referenser
  els: {},

  // Senaste validerade diff + bas
  lastValidated: null,

  /**
   * Initierar pluginet (injekterar CSS/HTML, binder events).
   * @param {object} config
   *  - hashMaps: { sha2paths: Map<sha256,path>, byPath: Map<path,{is_content_full,content,...}> }
   *  - rawBaseUrl: string
   *  - onBusyStart?: fn
   *  - onBusyEnd?: fn
   */
  init(config) {
    if (document.getElementById('plug-patch-modal')) {
      console.warn('PatchCenterPlugin: Already initialized.');
      return;
    }
    this.config = { ...this.config, ...config };
    if (!this.config.hashMaps || !this.config.rawBaseUrl) {
      console.error('PatchCenterPlugin: `hashMaps` och `rawBaseUrl` krävs i konfigurationen.');
      return;
    }
    this._injectCSS();
    this._injectHTML();
    this._cacheDOMElements();
    this._attachEventListeners();
    console.log('Patch Center Plugin Initialized (json_diff).');
  },

  /** Öppnar modalen. */
  open() {
    if (this.els.modal) this.els.modal.classList.add('show');
    else console.error('PatchCenterPlugin: Inte initierad. Anropa init() först.');
  },

  // ===== Interna hjälpmetoder =====

  _injectCSS() {
    const style = document.createElement('style');
    style.id = 'patch-center-plugin-styles';
    style.textContent = `
      :root {
        --pcp-bg: #fff;
        --pcp-fg: #212529;
        --pcp-border: #dee2e6;
        --pcp-muted: #6c757d;
        --pcp-primary: #0d6efd;
        --pcp-primary-hover: #0b5ed7;
        --pcp-mono: ui-monospace, "JetBrains Mono", Consolas, Menlo, monospace;
        --pcp-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      }
      #plug-patch-modal .box { max-width: 1100px; width: 95%; }
      #plug-patch-log { white-space: pre-wrap; border: 1px solid var(--pcp-border); border-radius: 8px; padding: 8px; background: #f8f9fa; max-height: 34vh; overflow: auto; font-size: 12px; }
      #plug-patch-target { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
      #plug-patch-target .badge { padding: 2px 8px; border: 1px solid #ccc; border-radius: 999px; background: #f6f7f9; font-size: 12px; font-family: var(--pcp-mono); }
      #plug-patch-preview { width: 100%; height: 360px; }
      #plug-patch-source { width: 100%; height: 160px; }
      #plug-patch-file { display: none; }
      .patch-center-modal-plugin { position: fixed, inset: 0; background: rgba(0,0,0,.5); display: none; align-items: center; justify-content: center; z-index: 1000; }
      .patch-center-modal-plugin.show { display: flex; }
      .patch-center-modal-plugin .box { background: var(--pcp-bg); border-radius: 12px; max-height: 88vh; display: flex; flex-direction: column; }
      .patch-center-modal-plugin .box header { display: flex; align-items: center; justify-content: space-between; padding: 12px 14px; border-bottom: 1px solid var(--pcp-border); }
      .patch-center-modal-plugin .box main { padding: 14px; overflow: auto; }
      #plug-patch-modal kbd { background: #f1f3f5; border: 1px solid #e9ecef; border-bottom-color: #dee2e6; border-radius: 4px; padding: 0 4px; font-family: var(--pcp-mono); }
      #plug-patch-modal .small { font-size: 12px; color: var(--pcp-muted); }
      #plug-patch-modal .flex { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
      #plug-patch-modal button { border: 1px solid var(--pcp-border); background: var(--pcp-bg); color: var(--pcp-fg); padding: 8px 12px; border-radius: 8px; cursor: pointer; font-family: var(--pcp-sans); font-size: 14px; }
      #plug-patch-modal button:hover { background: #eef1f4; }
      #plug-patch-modal button.primary { background: var(--pcp-primary); color: #fff; border-color: var(--pcp-primary); }
      #plug-patch-modal button.primary:hover { background: var(--pcp-primary-hover); }
      #plug-patch-modal button:disabled { opacity: .6; cursor: not-allowed; }
      #plug-patch-modal textarea { font-family: var(--pcp-mono); font-size: 13.5px; border: 1px solid var(--pcp-border); border-radius: 8px; padding: 8px; resize: vertical; }
    `;
    document.head.appendChild(style);
  },

  _injectHTML() {
    const html = `
      <div id="plug-patch-modal" class="patch-center-modal-plugin" role="dialog" aria-modal="true" aria-labelledby="plug-patch-title">
        <div class="box">
          <header>
            <b id="plug-patch-title">Patch Center</b>
            <button id="plug-patch-close" aria-label="Stäng" style="border:0;background:transparent;font-size:1.2rem;cursor:pointer;">✕</button>
          </header>
          <main>
            <div class="flex" style="justify-content:space-between;align-items:flex-end;gap:12px;flex-wrap:wrap">
              <div style="flex:1;min-width:280px">
                <label for="plug-patch-source" class="small">Klistra in <kbd>diff.json</kbd> (<kbd>json_diff</kbd>) här:</label>
                <textarea id="plug-patch-source" placeholder='{"protocol_id":"json_diff","target":{"base_checksum_sha256":"..."},"op_groups":[...],"result_sha256":"..."}'></textarea>
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
            <h4 style="margin:12px 0 6px 0; font-weight: 600;">Logg</h4>
            <pre id="plug-patch-log"></pre>
          </main>
        </div>
      </div>
    `;
    document.body.insertAdjacentHTML('beforeend', html);
  },

  _cacheDOMElements() {
    const q = (id) => document.getElementById(id);
    this.els = {
      modal: q('plug-patch-modal'), closeBtn: q('plug-patch-close'), srcTA: q('plug-patch-source'),
      fileInput: q('plug-patch-file'), uploadBtn: q('plug-patch-upload'), validateBtn: q('plug-patch-validate'),
      applyBtn: q('plug-patch-apply'), copyBtn: q('plug-patch-copy'), dlBtn: q('plug-patch-download'),
      previewTA: q('plug-patch-preview'), logEl: q('plug-patch-log'),
      tgtPathEl: q('plug-target-path'), tgtShaEl: q('plug-target-sha256'), tgtGitEl: q('plug-target-gitsha'),
      tgtSrcEl: q('plug-target-source'), schemaOK: q('plug-schema-ok'),
    };
  },

  _log(m, kind = 'info') {
    const t = new Date().toLocaleTimeString();
    const tag = kind === 'err' ? '[ERR]' : kind === 'warn' ? '[WARN]' : '[INFO]';
    if (this.els.logEl) {
      this.els.logEl.textContent += `[${t}] ${tag} ${m}\n`;
      this.els.logEl.scrollTop = this.els.logEl.scrollHeight;
    }
  },

  async _withBusy(fn) {
    this.config.onBusyStart();
    try { await fn(); }
    catch (e) {
      this._log(`Operation misslyckades: ${e.message}`, 'err');
      console.error(e);
    }
    finally { this.config.onBusyEnd(); }
  },

  _canonText(s) { return (s || '').replace(/\uFEFF/g, '').replace(/\r\n?/g, '\n'); },

  async _sha256HexLF(text) {
    const enc = new TextEncoder().encode(this._canonText(text));
    const buf = await crypto.subtle.digest('SHA-256', enc);
    return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
  },

  async _fetchText(path) {
    const url = this.config.rawBaseUrl + path;
    const r = await fetch(url, { cache: 'no-store' });
    if (!r.ok) throw new Error(`HTTP ${r.status} för ${url}`);
    return await r.text();
  },

  async _findBaseText(diffJ) {
    const need = String(diffJ.target.base_checksum_sha256 || '').toLowerCase();
    if (!/^[a-f0-9]{64}$/.test(need)) throw new Error('Ogiltig base_checksum_sha256.');
    const maps = this.config.hashMaps;
    if (maps && maps.sha2paths && maps.sha2paths.has(need)) {
      const p = maps.sha2paths.get(need);
      const node = maps.byPath && maps.byPath.get ? maps.byPath.get(p) : null;
      if (node && node.is_content_full && typeof node.content === 'string') {
        return { path: p, source: 'context.file_structure', text: this._canonText(node.content) };
      }
      return { path: p, source: 'context.hash_index', text: this._canonText(await this._fetchText(p)) };
    }
    if (diffJ.target.path) {
      const p = diffJ.target.path;
      const t = await this._fetchText(p);
      const got = await this._sha256HexLF(t);
      if (got === need) return { path: p, source: 'path->RAW', text: this._canonText(t) };
      throw new Error('Sökväg fanns men base_checksum_sha256 matchade inte.');
    }
    throw new Error('Kunde inte hitta basfil via checksumma eller sökväg.');
  },

  _attachEventListeners() {
    this.els.closeBtn.onclick = () => this.els.modal.classList.remove('show');
    this.els.uploadBtn.onclick = () => this.els.fileInput.click();
    this.els.fileInput.onchange = async (e) => {
      const f = e.target.files && e.target.files[0];
      if (!f) return;
      this.els.srcTA.value = await f.text();
      this._log(`Läste fil: ${f.name} (${f.size} B)`);
    };
    this.els.validateBtn.onclick = () => this._withBusy(this._onValidate.bind(this));
    this.els.applyBtn.onclick = () => this._withBusy(this._onApply.bind(this));
    this.els.copyBtn.onclick = this._onCopy.bind(this);
    this.els.dlBtn.onclick = this._onDownload.bind(this);
  },

  async _onValidate() {
    this.els.logEl.textContent = '';
    this.els.schemaOK.style.display = 'none';
    this.els.applyBtn.disabled = true; this.els.copyBtn.disabled = true; this.els.dlBtn.disabled = true;
    this.els.previewTA.value = '';
    this.els.tgtPathEl.textContent = '–'; this.els.tgtShaEl.textContent = '–'; this.els.tgtGitEl.textContent = '–'; this.els.tgtSrcEl.textContent = '–';
    this.lastValidated = null;

    const txt = this.els.srcTA.value.trim();
    if (!txt) { this._log('Ingen JSON angiven.', 'warn'); return; }

    let j;
    try { j = JSON.parse(txt); }
    catch (e) { this._log(`JSON-tolkningsfel: ${e.message}`, 'err'); return; }

    // json_diff enligt schema (protocol_id === 'json_diff')
    if (j.protocol_id !== 'json_diff') {
      this._log('Schemafel: protocol_id måste vara "json_diff".', 'err'); return;
    }
    if (!j.target || !j.target.base_checksum_sha256) {
      this._log('Schemafel: target.base_checksum_sha256 krävs.', 'err'); return;
    }
    this.els.schemaOK.style.display = 'inline-block';

    try {
      const base = await this._findBaseText(j);
      this._log(`Basfil hittad: ${base.path} (källa: ${base.source})`);
      this.lastValidated = { diff: j, base };
      this.els.tgtPathEl.textContent = base.path;
      this.els.tgtShaEl.textContent = String(j.target.base_checksum_sha256).substring(0, 12) + '...';
      this.els.tgtGitEl.textContent = (j.target.git_sha1 ? String(j.target.git_sha1).substring(0,7) + '...' : '–');
      this.els.tgtSrcEl.textContent = base.source;
      this._log('Validering OK: Basfil hittad och checksumma matchar.');
      this.els.applyBtn.disabled = false;
    } catch(e) {
      this._log(`Validering misslyckades: ${e.message}`, 'err');
    }
  },

  _findNthOccurrence(haystack, needle, startIndex, n) {
    // Returnerar index för n:te förekomsten av needle i haystack efter startIndex. 1-baserat n.
    if (n < 1) return -1;
    let idx = startIndex;
    for (let i = 0; i < n; i++) {
      idx = haystack.indexOf(needle, idx);
      if (idx === -1) return -1;
      if (i < n - 1) idx = idx + needle.length;
    }
    return idx;
  },

  async _onApply() {
    if (!this.lastValidated) { this._log('Kör Validate först.', 'err'); return; }
    let newText = this.lastValidated.base.text;
    const { diff } = this.lastValidated;

    // Iterera op_groups
    for (const group of (diff.op_groups || [])) {
      if (!group || !group.anchor || typeof group.anchor.text !== 'string') {
        this._log('Schemafel: group.anchor.text saknas.', 'err'); return;
      }
      const anchorText = this._canonText(group.anchor.text);
      const anchorIndex = newText.indexOf(anchorText);
      if (anchorIndex === -1) { this._log('Ankartext kunde inte hittas i basfilen.', 'err'); return; }
      const afterAnchorIndex = anchorIndex + anchorText.length;
      let appliedInGroup = 0;

      for (const target of (group.targets || [])) {
        const op = target && target.op;
        if (!op) { this._log('Schemafel: target.op saknas.', 'err'); return; }

        if (op === 'replace_entire_file') {
          const content = this._canonText(String(target.new_content || ''));
          newText = content;
          appliedInGroup++;
          this._log('Applicerade "replace_entire_file". Andra operationer ignoreras i denna grupp.');
          break; // Inom gruppen är hela filen redan ersatt
        }

        if (op === 'replace_block' || op === 'delete_block') {
          const oldBlock = this._canonText(String(target.old_block || ''));
          if (!oldBlock) { this._log(`Schemafel: old_block krävs för ${op}.`, 'err'); return; }
          const matchIndex = Number.isInteger(target.match_index) && target.match_index >= 1 ? target.match_index : 1;

          // Sök efter n:te förekomsten i textdelen efter ankaret
          const tail = newText.substring(afterAnchorIndex);
          const localIdx = this._findNthOccurrence(tail, oldBlock, 0, matchIndex);
          if (localIdx === -1) {
            this._log(`${op}: old_block förekomst #${matchIndex} hittades inte efter ankaret.`, 'warn');
            continue;
          }
          const globalIdx = afterAnchorIndex + localIdx;
          const before = newText.substring(0, globalIdx);
          const after = newText.substring(globalIdx + oldBlock.length);

          if (op === 'replace_block') {
            const newBlock = this._canonText(String(target.new_block || ''));
            newText = before + newBlock + after;
            this._log(`replace_block: ersatte förekomst #${matchIndex} efter ankare.`);
          } else {
            // delete_block
            newText = before + after;
            this._log(`delete_block: tog bort förekomst #${matchIndex} efter ankare.`);
          }
          appliedInGroup++;
        } else {
          this._log(`Okänd operation: ${op}`, 'err'); return;
        }
      }

      if (appliedInGroup === 0) this._log('Varning: Inga operationer applicerades i gruppen.', 'warn');
    }

    if (typeof diff.result_sha256 === 'string' && /^[a-f0-9]{64}$/.test(diff.result_sha256)) {
      const got = await this._sha256HexLF(newText);
      if (got.toLowerCase() !== String(diff.result_sha256).toLowerCase()) this._log('Varning: result_sha256 matchar INTE.', 'warn');
      else this._log('result_sha256 verifierad.', 'ok');
    }
    this.els.previewTA.value = newText;
    this.els.copyBtn.disabled = false; this.els.dlBtn.disabled = false;
    this._log('Patch applicerad. Förhandsvisning klar.');
  },

  _onCopy() {
    navigator.clipboard.writeText(this.els.previewTA.value);
    this._log('Kopierat till urklipp.');
  },

  _onDownload() {
    const blob = new Blob([this.els.previewTA.value], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = (this.lastValidated?.base.path || 'patched.txt').split('/').pop();
    document.body.appendChild(a); a.click(); a.remove();
    URL.revokeObjectURL(url);
    this._log('Nedladdning startad.');
  }
};
