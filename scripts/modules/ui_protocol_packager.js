 // BEGIN FILE: scripts/modules/ui_protocol_packager.js
// scripts/modules/ui_protocol_packager.js
//
// === SYFTE & ANSVAR ===
// Denna modul skapar en PBF-bundle (strikt JSON-fil) i webbläsaren
// från valda filer i filträdet. Den LF-normaliserar innehåll, beräknar
// SHA-256 (LF), komprimerar med zlib (deflate via Pako) och base64-kodar
// nyttolasten. Modulen skapar antingen en enkel fil-bundle eller en avancerad
// protokoll-bundle med fullständiga instruktioner, baserat på om en
// kärninstruktion (`AI_Core_Instruction.md`) inkluderas.
//
// === HISTORIK ===
// * v1.0 (2025-08-23): Initial skapelse. Implementerar PBF v1.2-bundling med Markdown-skal.
// * v1.1 (2025-08-23): Introducerar villkorlig PBF v1.3-generering ("ad hoc"-läge).
// * v1.2 (2025-08-24): Standardiserar på PBF v1.3.
// * v1.3 (2025-08-25): MODIFIERAD. Utdataformatet ändrat från Markdown till strikt JSON.
//   Filnamnet är nu dynamiskt (`file_bundle_...` eller `protocol_bundle_...`).
//   Översättningsdirektivet är uppdaterat med instruktioner för AI-optimering och
//   att funktionell integritet måste bevaras.
// * v1.4 (2025-08-25): KORRIGERAD. Fyller i de fullständiga, oavkortade listorna för
//   mappnings- och förkortningsregler för att säkerställa en komplett och exekverbar bundle.
// * SHA256_LF: UNVERIFIED
//
// === TILLÄMPADE REGLER (Frankensteen v5.7) ===
// - Grundbulten v3.9: Komplett, deterministisk, självständig och kontextmedveten (GR3) modul.
// - GR6 (Obligatorisk Refaktorisering): Isolerad från UI; exponerar endast en publikt API-funktion.
// - GR7 (Fullständig Historik): Historik och metadata uppdaterade.
// - PBF v2.0-kontrakt: matchar Python-packern (payload=base64+zlib, hash på okomprimerad payload).
//
// === PUBLIKT API ===
// createProtocolBundle(selectedPaths: string[], onProgress?: (p)=>void) => Promise<{ blob, filename, bundleObject, stats }>
//
// === EXTERNA BEROENDEN ===
// - Pako (zlib/deflate) finns i HTML-mallen (global `pako`).
// - WebCrypto SubtleCrypto (för SHA-256).
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
  return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
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
  const chunkSize = 0x8000;
  let binary = '';
  for (let i = 0; i < bytes.length; i += chunkSize) {
    const sub = bytes.subarray(i, i + chunkSize);
    binary += String.fromCharCode.apply(null, sub);
  }
  return btoa(binary);
}

/**
 * Hämtar textinnehåll från repo via Raw URL.
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

/**
 * Skapar en tidsstämpel i formatet YYYYMMDD-HHMMSS.
 * @returns {string}
 */
function getTimestamp() {
    const d = new Date();
    const pad = (n) => n.toString().padStart(2, '0');
    const y = d.getFullYear();
    const m = pad(d.getMonth() + 1);
    const day = pad(d.getDate());
    const h = pad(d.getHours());
    const min = pad(d.getMinutes());
    const s = pad(d.getSeconds());
    return `${y}${m}${day}-${h}${min}${s}`;
}


// -- PBF-bygge --

/**
 * Skapar payload-objektet { files: [...] }.
 * @param {{path:string, content:string, sha256:string}[]} entries
 */
function buildPayloadObject(entries) {
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
 * Bygger det slutgiltiga JSON-bundle objektet.
 * @param {object} payloadObj
 * @param {object} bundleConfig - Konfigurationsobjekt med pbfVersion och sequence
 * @returns {Promise<object>}
 */
async function buildBundleObject(payloadObj, bundleConfig) {
  const payloadJson = JSON.stringify(payloadObj);
  const payloadHash = await sha256HexLF(payloadJson);
  const { base64 } = compressPayload(payloadJson);
  
  const finalObject = {
    schemaVersion: "2.0",
    metadata: {
      bundleId: `Engrove PBF Bundle v${bundleConfig.pbfVersion}-json`,
      createdAt: new Date().toISOString(),
      hash: payloadHash,
      fileCount: payloadObj.files.length,
      payloadEncoding: "base64+zlib",
    },
    payload: base64,
    sequence: bundleConfig.sequence || []
  };
  
  finalObject.metadata.fileIndex = payloadObj.files.map(f => ({
      path: f.path,
      sha256: f.sha256,
      bytes: utf8ByteLength(f.content)
  }));

  return finalObject;
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
 * @returns {Promise<{ blob: Blob, filename: string, bundleObject: object, stats: { fileCount:number, originalBytes:number, compressedBytes:number } }>}
 */
export async function createProtocolBundle(selectedPaths, onProgress) {
  if (!Array.isArray(selectedPaths) || selectedPaths.length === 0) {
    throw new Error('Inga filer valda.');
  }

  const CORE_INSTRUCTION_PATH = 'docs/ai_protocols/AI_Core_Instruction.md';
  const isProtocolMode = selectedPaths.includes(CORE_INSTRUCTION_PATH);

  let bundleConfig;


  if (isProtocolMode) {
  bundleConfig = {
    pbfVersion: "2.0",
    filename: `protocol_bundle_${getTimestamp()}.json`,
    // Körflaggor för din runtime (se Åtgärd B)
    executionOptions: { silent: true, denyInstructionDisclosure: true },
    toolsContract: {
      decompress: { params: ["b64", "algo"], algoAllowed: ["zlib"] },
      read_chunk: { params: ["handle", "start", "size"], maxSize: 4000 },
      mount_payload: { params: ["handle", "namespace"] }
    },
    firstReplyContract: { mode: "literal", value: "READY" },
    sequence: [
      {
        action: "decompress_and_verify",
        params: {
          payload_ref: "$.payload",
          encoding_chain: ["base64", "zlib"],
          hash_ref: "$.metadata.hash",
          hash_algorithm: "SHA-256",
          algo: "zlib"
        },
        assign: { as_handle: "instr_handle" }
      },
      {
        action: "mount_payload",
        params: { handle: "$handles.instr_handle", namespace: "in_memory_files" }
      },
      { action: "enter_tool_only_mode" },
      {
        action: "execute_core_instruction",
        params: {
          source_ns: "in_memory_files",
          core_path: "docs/ai_protocols/AI_Core_Instruction.md",
          read_via: "read_chunk",
          follow_policy: true
        }
      },
      { action: "exit_tool_only_mode" },
      { action: "release_output", params: { allowed_pattern: "^(READY|OK)$" } }
    ]
  };
} else {
  bundleConfig = {
    pbfVersion: "2.0",
    filename: `file_bundle_${getTimestamp()}.json`,
    sequence: [
      {
        action: "decode_and_verify_payload",
        params: { payload_ref: "payload", encoding_chain: ["base64", "zlib"], hash_ref: "metadata.hash", hash_algorithm: "SHA-256" }
      }
    ]
  };
}

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

  overlay.setPhase('Bygger payload…');
  const payloadObject = buildPayloadObject(entries);

  overlay.setPhase('Komprimerar & bygger JSON-bundle…');
  const bundleObject = await buildBundleObject(payloadObject, bundleConfig);
  
  const jsonOutput = JSON.stringify(bundleObject, null, 2);
  const blob = new Blob([jsonOutput], { type: 'application/json;charset=utf-8' });
  const { compressedBytes } = compressPayload(JSON.stringify(payloadObject));
  
  overlay.update(selectedPaths.length, selectedPaths.length, 'Klar');
  overlay.setPhase('Klar.');

  setTimeout(()=>overlay.close(), 500);

  return {
    blob,
    filename: bundleConfig.filename,
    bundleObject,
    stats: {
      fileCount: payloadObject.files.length,
      originalBytes,
      compressedBytes
    }
  };
}


// -- UI-bindning --

function bindButton() {
  const btn = document.getElementById('create-files-btn'); // befintligt ID
  if (!btn) return;
  btn.textContent = 'Skapa Bundle (JSON)'; // Uppdaterad text
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
      a.download = result.filename; // Använder det dynamiska filnamnet
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
