// BEGIN FILE: scripts/modules/ui_protocol_packager.js
// scripts/modules/ui_protocol_packager.js
//
// === SYFTE & ANSVAR ===
// Denna modul skapar en PBF-bundle (Markdown-skal) i webbläsaren
// från valda filer i filträdet. Den LF-normaliserar innehåll, beräknar
// SHA-256 (LF), komprimerar med zlib (deflate via Pako) och base64-kodar
// nyttolasten. Modulen anpassar PBF-versionen (1.2/1.3) baserat på
// om en kärninstruktion inkluderas ("ad hoc"-läge).
//
// === HISTORIK ===
// * v1.0 (2025-08-23): Initial skapelse. Implementerar fullständig PBF v1.2-bundling,
//   progress-UI, deterministisk sortering och Markdown-skal med AI-instruktioner.
// * v1.1 (2025-08-23): Introducerar villkorlig PBF v1.3-generering ("ad hoc"). Om
//   AI_Core_Instruction.md väljs, skapas en själv-initialiserande bundle med ett
//   utökat bootstrap_directive-objekt och uppdaterade AI-instruktioner.
// * v1.2 (2025-08-24): Modifierat standard-bootstrap_directive (i 'else'-blocket) för att tvinga fram 
//   omedelbar exekvering av Stature_Report_Protocol.md. Detta replikerar det ideala 
//   startbeteendet för en session och gör PBF-metoden till den nya standarden för kontextleverans.
//   PBF-versionen för standardfallet är nu också 1.3.
// * SHA256_LF: UNVERIFIED
//
// === TILLÄMPADE REGLER (Frankensteen v5.7) ===
// - Grundbulten v3.9: Komplett, deterministisk, självständig och kontextmedveten (GR3) modul.
// - GR6 (Obligatorisk Refaktorisering): Isolerad från UI; exponerar endast en publikt API-funktion.
// - GR7 (Fullständig Historik): Historik och metadata uppdaterade.
// - PBF v1.2/v1.3-kontrakt: matchar Python-packern (payload=base64+zlib, hash på okomprimerad payload).
//
// === PUBLIKT API ===
// createProtocolBundle(selectedPaths: string[], onProgress?: (p)=>void) => Promise<{ blob, filename, pbf, stats }>
//
// === EXTERNA BEROENDEN ===
// - Pako (zlib/deflate) finns i HTML-mallen (global `pako`).
// - WebCrypto SubtleCrypto (för SHA-256).
//
// === SÄKERHET ===
// - Ingen HTML-injektion. Endast JSON → deflate → base64.
// - Hanterar </script>-sekvens i Markdown via kodblock.
//

// -- Hjälpfunktioner --

/**
 * Läser och parsar en JSON "Data Island" från DOM.
 * @param {string} id
 * @returns {object}
 */
function readDataIsland(id) {
  const el = document.getElementById(id);
  if (!el) throw new Error(`Data Island saknas: ${id}`);
  try {
    return JSON.parse(el.textContent);
  } catch (e) {
    console.error(`Fel vid JSON.parse för ${id}`, e);
    throw e;
  }
}

/**
 * Normaliserar text för deterministisk hashing (LF, trimma endast högerspalt per rad).
 * Motsvarar _norm_text i Python-packern.
 * @param {string} s
 * @returns {string}
 */
function canonText(s) {
  const lf = (s || '').replace(/\r\n?/g, '\n');
  return lf.split('\n').map(line => line.replace(/\s+$/u, '')).join('\n');
}

/**
 * SHA-256 (hex) på LF-normaliserad text.
 * @param {string} text
 * @returns {Promise<string>}
 */
async function sha256HexLF(text) {
  const enc = new TextEncoder().encode(canonText(text));
  const buf = await crypto.subtle.digest('SHA-256', enc);
  return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2,'0')).join('');
}

/**
 * Byte-längd i UTF-8.
 * @param {string} text
 * @returns {number}
 */
function utf8ByteLength(text) {
  return new TextEncoder().encode(text).length;
}

/**
 * Base64-koda en Uint8Array (chunkad för stora arrayer).
 * @param {Uint8Array} bytes
 * @returns {string}
 */
function base64FromUint8(bytes) {
  // Konvertera till binärsträng i chunkar (för att undvika stack/argument-limit)
  const chunkSize = 0x8000;
  let binary = '';
  for (let i = 0; i < bytes.length; i += chunkSize) {
    const sub = bytes.subarray(i, i + chunkSize);
    binary += String.fromCharCode.apply(null, sub);
  }
  // btoa kräver Latin1-binärsträng
  return btoa(binary);
}

/**
 * Hämtar textinnehåll från repo via Raw URL (spegel av fetchText i ui_logic.js).
 * @param {string} filePath
 * @returns {Promise<string>}
 */
async function fetchTextFromRepo(filePath) {
  const overview = readDataIsland('data-island-overview');
  const repo = overview.repository;
  const branch = overview.branch;
  const url = `https://raw.githubusercontent.com/${repo}/${branch}/${filePath}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status} för ${filePath}`);
  return await res.text();
}

// -- PBF-bygge --

/**
 * Skapar payload-objektet { files: [{path, sha256, content}...] }.
 * Deterministiskt sorterad på path.
 * @param {{path:string, content:string, sha256:string}[]} entries
 */
function buildPayload(entries) {
  const files = entries
    .slice()
    .sort((a, b) => a.path.localeCompare(b.path, 'sv'))
    .map(e => ({ path: e.path, sha256: e.sha256, content: e.content }));
  return { files };
}

/**
 * Komprimerar JSON-sträng med zlib (deflate) och base64-kodar.
 * @param {string} jsonString
 * @returns {{ base64: string, compressedBytes: number }}
 */
function compressPayload(jsonString) {
  const input = new TextEncoder().encode(jsonString);
  const deflated = pako.deflate(input);
  const b64 = base64FromUint8(deflated);
  return { base64: b64, compressedBytes: deflated.length };
}

/**
 * Bygger PBF-objektet (v1.2 eller v1.3).
 * @param {object} payloadObj
 * @param {{path:string, sha256:string, bytes:number}[]} fileIndex
 * @param {string} pbfVersion - '1.2' eller '1.3'
 * @param {string|object} bootstrapDirective - Direktivet att inkludera
 * @returns {Promise<object>}
 */
async function buildPbfObject(payloadObj, fileIndex, pbfVersion, bootstrapDirective) { // MODIFIED
  const payloadJson = JSON.stringify(payloadObj);
  const payloadHash = await sha256HexLF(payloadJson); // hash på okomprimerad payload
  const { base64 } = compressPayload(payloadJson);
  return {
    pbf_version: pbfVersion, // MODIFIED
    created_at: new Date().toISOString(),
    bootstrap_directive: bootstrapDirective, // MODIFIED
    hash: payloadHash,
    payload_encoding: "base64+zlib",
    payload: base64,
    file_count: fileIndex.length,
    file_index: fileIndex
  };
}

// -- Markdown-skal --

/**
 * Skapar Markdown med AI-instruktioner + inbäddat PBF JSON i fenced code block.
 * @param {object} pbf
 * @param {{fileCount:number, originalBytes:number, compressedBytes:number}} stats
 * @param {string[]} topPaths
 * @param {string} pbfVersion - '1.2' eller '1.3'
 * @param {string[]} aiInstructions - Lista med instruktionstexter.
 * @returns {string}
 */
function wrapMarkdown(pbf, stats, topPaths, pbfVersion, aiInstructions) { // MODIFIED
  const header = [
    `# Engrove PBF Bundle v${pbfVersion}`, // MODIFIED
    '',
    'Detta dokument innehåller en PBF-bundle med valda **textfiler** för AI-initialisering.',
    'Payload är JSON med `files[]`, komprimerad med **zlib (deflate)** och **base64**-kodad.',
    'Fältet `hash` är **SHA-256** av den **okomprimerade** payloaden för integritetsverifikation.',
    '',
    '## AI-instruktioner',
    ...aiInstructions.map((line, i) => `${i + 1}. ${line}`), // MODIFIED
    '',
    '## Sammanfattning',
    `- Antal filer: ${stats.fileCount}`,
    `- Okomprimerat: ${formatSize(stats.originalBytes)}`,
    `- Komprimerat: ${formatSize(stats.compressedBytes)}`,
    topPaths.length ? `- Urval (topp ${Math.min(5, topPaths.length)}):` : '',
    topPaths.slice(0,5).map(p => `  - ${p}`).join('\n'),
    '',
    '```json',
    JSON.stringify(pbf, null, 2),
    '```',
    ''
  ].filter(Boolean).join('\n');
  return header;
}

/**
 * Formaterar bytes som sträng.
 * @param {number} bytes
 * @returns {string}
 */
function formatSize(bytes) {
  if (!Number.isFinite(bytes) || bytes < 0) return '0 B';
  const units = ['B','kB','MB','GB'];
  let i = 0, v = bytes;
  while (v >= 1024 && i < units.length - 1) { v /= 1024; i++; }
  return `${v.toFixed(1)} ${units[i]}`;
}

// -- Progress UI --

/**
 * Skapar (eller återanvänder) ett overlay för progress.
 * @returns {{update: (n:number,d:number,file?:string,extra?:string)=>void, close:()=>void, setPhase:(s:string)=>void}}
 */
function createProgressOverlay() {
  let overlay = document.getElementById('pbf-progress-overlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.id = 'pbf-progress-overlay';
    overlay.style.cssText = [
      'position:fixed','inset:0','background:rgba(0,0,0,0.55)','z-index:2000',
      'display:flex','align-items:center','justify-content:center'
    ].join(';');
    const panel = document.createElement('div');
    panel.style.cssText = 'background:#34495e;border:1px solid #4a6572;border-radius:8px;width:min(520px,90vw);padding:16px;color:#ecf0f1;font-family:system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;';
    panel.innerHTML = [
      '<h3 style="margin:0 0 8px 0;font-weight:600">Skapar bundle…</h3>',
      '<div id="pbf-phase" style="font-size:12px;color:#bdc3c7;margin-bottom:8px">Initierar…</div>',
      '<div style="height:10px;background:#2c3e50;border-radius:6px;overflow:hidden;border:1px solid #4a6572">',
      '  <div id="pbf-bar" style="height:100%;width:0%;background:#3498db;transition:width .15s ease"></div>',
      '</div>',
      '<div id="pbf-meta" style="margin-top:8px;font-size:12px;color:#bdc3c7"></div>'
    ].join('');
    overlay.appendChild(panel);
    document.body.appendChild(overlay);
  }
  const bar = overlay.querySelector('#pbf-bar');
  const meta = overlay.querySelector('#pbf-meta');
  const phase = overlay.querySelector('#pbf-phase');
  return {
    setPhase: (s)=>{ phase.textContent = s || ''; },
    update: (n, d, file, extra) => {
      const pct = d ? Math.floor((n/d)*100) : 0;
      bar.style.width = pct + '%';
      meta.textContent = `${pct}% • ${n}/${d}${file ? ` • ${file}` : ''}${extra?` • ${extra}`:''}`;
    },
    close: () => { overlay.remove(); }
  };
}

// -- Huvudfunktion --

/**
 * Skapa PBF-bundle från valda paths.
 * @param {string[]} selectedPaths
 * @param {(p:{current:number,total:number,file?:string})=>void} [onProgress]
 * @returns {Promise<{ blob: Blob, filename: string, pbf: object, stats: { fileCount:number, originalBytes:number, compressedBytes:number } }>}
 */
export async function createProtocolBundle(selectedPaths, onProgress) {
  if (!Array.isArray(selectedPaths) || selectedPaths.length === 0) {
    throw new Error('Inga filer valda.');
  }

  // --- START: MODIFIED LOGIC FOR AD-HOC v1.3 ---
  const CORE_INSTRUCTION_PATH = 'docs/ai_protocols/AI_Core_Instruction.md';
  const isAdHocMode = selectedPaths.includes(CORE_INSTRUCTION_PATH);

  let pbfConfig;
  if (isAdHocMode) {
    pbfConfig = {
      pbfVersion: "1.5",
    "bootstrap_directive": {
      "sequence": [
          {
            "action": "internal_system_check",
            "description": "Verifierar PBF-hash och filintegritet. Sätter resultatet i session.bootstrap_result.",
            "mode": "silent"
          },
          {
            "action": "execute_protocol",
            "path": "docs/ai_protocols/Stature_Report_Protocol.md",
            "description": "Genererar den initiala statusrapporten, vilket är det första synliga svaret."
          }
        ]
        }
      },
      aiInstructions: [
        'Dekoda `payload` (base64 → zlib → JSON).',
        'Verifiera `hash` (SHA-256) mot dekodad payload.',
        'Ladda `files[]` i arbetsminnet; bevara lexikografisk ordning.',
        'Utför åtgärder specificerade i `bootstrap_directive`-objektet.',
        'Svara enbart utifrån dessa filer och **citera `path`** per referens.',
        'Rapportera mismatch mellan `hash` och payload eller saknade filer.'
      ]
    };
  } else {
    pbfConfig = {
      pbfVersion: "1.3",
      "bootstrap_directive": {
        "action": "execute_protocol",
        "path": "docs/ai_protocols/Stature_Report_Protocol.md"
      },
      aiInstructions: [
        'Dekoda `payload` (base64 → zlib → JSON).',
        'Verifiera `hash` (SHA-256) mot dekodad payload.',
        'Ladda `files[]` i arbetsminnet; bevara lexikografisk ordning.',
        'Utför åtgärder specificerade i `bootstrap_directive`-objektet.',
        'Svara enbart utifrån dessa filer och **citera `path`** per referens.',
        'Rapportera mismatch mellan `hash` och payload eller saknade filer.'
      ]
    };
  }
  // --- END: MODIFIED LOGIC ---

  const overlay = createProgressOverlay();
  overlay.setPhase('Läser filer…');
  const entries = [];
  let processed = 0;
  let originalBytes = 0;

  for (const path of selectedPaths) {
    try {
      const raw = await fetchTextFromRepo(path);
      const normalized = canonText(raw);
      const sha = await sha256HexLF(normalized);
      const bytes = utf8ByteLength(normalized);
      originalBytes += bytes;
      entries.push({ path, content: normalized, sha256: sha, bytes });
    } catch (e) {
      // Fortsätt, men markera fel i innehåll
      const msg = `// ERROR: ${e.message || e}`;
      const normalized = canonText(msg);
      const bytes = utf8ByteLength(normalized);
      originalBytes += bytes;
      entries.push({ path, content: normalized, sha256: null, bytes });
    } finally {
      processed += 1;
      overlay.update(processed, selectedPaths.length, path);
      if (onProgress) onProgress({ current: processed, total: selectedPaths.length, file: path });
    }
  }

  // Bygg payload och PBF
  overlay.setPhase('Bygger payload…');
  const payload = buildPayload(entries);
  const fileIndex = entries
    .slice()
    .sort((a,b)=> a.path.localeCompare(b.path,'sv'))
    .map(e => ({ path: e.path, sha256: e.sha256, bytes: e.bytes }));

  overlay.setPhase('Komprimerar & skriver metadata…');
  // MODIFIED: Passar PBF-konfigurationen
  const pbf = await buildPbfObject(payload, fileIndex, pbfConfig.pbfVersion, pbfConfig.bootstrapDirective);

  // Skapa Markdown
  overlay.setPhase('Skapar Markdown…');
  const { compressedBytes } = compressPayload(JSON.stringify(payload));
  const stats = {
    fileCount: fileIndex.length,
    originalBytes,
    compressedBytes
  };
  // MODIFIED: Passar PBF-konfigurationen
  const md = wrapMarkdown(pbf, stats, fileIndex.map(f=>f.path), pbfConfig.pbfVersion, pbfConfig.aiInstructions);

  const blob = new Blob([md], { type: 'text/markdown;charset=utf-8' });
  overlay.update(selectedPaths.length, selectedPaths.length, 'Klar');
  overlay.setPhase('Klar.');

  setTimeout(()=>overlay.close(), 500);

  return {
    blob,
    filename: 'protocol_bundle.md',
    pbf,
    stats: {
      fileCount: stats.fileCount,
      originalBytes: stats.originalBytes,
      compressedBytes: stats.compressedBytes
    }
  };
}

// -- UI-bindning (återanvänd befintlig knapp) --

function bindButton() {
  const btn = document.getElementById('create-files-btn'); // befintligt ID
  if (!btn) return;
  btn.textContent = 'Skapa Bundle (PBF)';
  btn.addEventListener('click', async () => {
    try {
      if (typeof window.selectedFiles !== 'function') {
        alert('Filträdet är inte redo. Försök igen.');
        return;
      }
      const paths = window.selectedFiles();
      const result = await createProtocolBundle(paths);
      const url = URL.createObjectURL(result.blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = result.filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error('Bundle-misslyckades:', e);
      alert('Misslyckades att skapa bundle: ' + (e.message || e));
    }
  }, { once: false });
}

// Init på DOMContentLoaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', bindButton);
} else {
  bindButton();
}

// END FILE: scripts/modules/ui_protocol_packager.js
