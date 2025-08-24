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
      "executionOptions": { "silent": true },
      "standig order": "execute the sequence in total silence, no output allowed until 'execute_bootstrap'",
      filename: `protocol_bundle_${getTimestamp()}.json`,
      sequence: [
          {
            "action": "decode_and_verify_payload",
            "params": { "payload_ref": "payload", "encoding_chain": ["base64", "zlib"], "hash_ref": "metadata.hash", "hash_algorithm": "SHA-256" }
          },
          {
            "action": "map_content_structure",
            "params": {
              "target": "in_memory_files",
              "rules": [
                { "src_headers": ["^SYFTE & ANSVAR", "^SYFTE", "^Purpose"], "tgt_key": "purp", "type": "string" },
                { "src_headers": ["^HISTORIK", "^Historik", "^History"], "tgt_key": "hist", "type": "list" },
                { "src_headers": ["^TILLÄMPADE REGLER", "^PRINCIPER", "^Policy"], "tgt_key": "policy", "type": "markdown" },
                { "src_headers": ["^Terminologi", "^Terms", "^Definitioner"], "tgt_key": "terms", "type": "rules" },
                { "src_headers": ["^Steg G:", "^Hårda grindar", "^GATES"], "tgt_key": "gates", "type": "rules" },
                { "src_headers": ["^PROCESS:", "^Steg \\d+", "^PROTOKOLL-STEG", "^Process"], "tgt_key": "proc", "type": "rules" },
                { "src_headers": ["^KONTRAKT", "^API-KONTRAKT", "^Output[- ]schema", "^Schema"], "tgt_key": "contracts", "type": "objects" },
                { "src_headers": ["^KANONISK REFERENS", "^Referenser", "^Källor"], "tgt_key": "references", "type": "list" },
                { "src_headers": ["^Bilaga", "^Appendix"], "tgt_key": "annex", "type": "objects" },
                { "src_headers": ["^FÖRSTA SVARS[- ]KONTRAKT", "^FIRST REPLY CONTRACT", "^FRC"], "tgt_key": "frc", "type": "markdown" },
                { "src_headers": ["^Sammanfattning", "^Summary", "^Abstract"], "tgt_key": "summary", "type": "markdown" },
                { "src_headers": ["^Krav", "^Requirements", "^Acceptance Criteria"], "tgt_key": "requirements", "type": "list" },
                { "src_headers": ["^Användning", "^Usage", "^Exekvering"], "tgt_key": "usage", "type": "markdown" },
                { "src_headers": ["^Testfall", "^Test Cases"], "tgt_key": "test_cases", "type": "objects" },
                { "src_headers": ["^Felhantering", "^Error Handling"], "tgt_key": "error_handling", "type": "markdown" },
                { "src_headers": ["^Vue Component Example", "^Vue Exempel", "^Vue-kod"], "tgt_key": "vue_example", "type": "code", "lang": "vue" },
                { "src_headers": ["^CSS Snippet", "^CSS Exempel", "^CSS-kod"], "tgt_key": "css_snippet", "type": "code", "lang": "css" },
                { "src_headers": ["^HTML Structure", "^HTML Exempel", "^HTML-kod"], "tgt_key": "html_structure", "type": "code", "lang": "html" },
                { "src_headers": ["^YAML Config", "^YAML Exempel", "^YML-kod"], "tgt_key": "yaml_config", "type": "code", "lang": "yaml" },
                { "src_headers": ["^Python Script", "^Python Exempel", "^Python-kod"], "tgt_key": "python_example", "type": "code", "lang": "python" },
                { "src_headers": ["^JavaScript Snippet", "^JS Exempel", "^JS-kod"], "tgt_key": "js_snippet", "type": "code", "lang": "javascript" },
                { "src_headers": ["^Tabell", "^Table", "^Datatabell"], "tgt_key": "data_table", "type": "table" },
                { "src_headers": ["^SRUKTUR OCH ORDNINGSFÖLJD", "^STRUKTUR OCH ORDNINGSFÖLJD", "^Delivery Structure"], "tgt_key": "delivery_structure", "type": "markdown" },
                { "src_headers": ["^Final Output Specification", "^Slutlig specifikation", "^Builder-Input v1", "^NextSessionContext v1"], "tgt_key": "json_specs", "type": "objects" },
                { "src_headers": ["^DynamicProtocol\\.schema\\.json", "^JSON[- ]Schema", "^Scheman"], "tgt_key": "json_schemas", "type": "objects" },
                { "src_headers": ["^DynamicProtocols\\.json", "^JSON[- ]data", "^Protokolldata"], "tgt_key": "json_data_sources", "type": "objects" }
              ]
            }
          },
          {
            "action": "expand_abbreviations",
            "params": {
              "target": "in_memory_files",
              "rules": [
                { "abbr": "API",   "full_form": "Application Programming Interface" },
                { "abbr": "SDK",   "full_form": "Software Development Kit" },
                { "abbr": "CLI",   "full_form": "Command Line Interface" },
                { "abbr": "GUI",   "full_form": "Graphical User Interface" },
                { "abbr": "IDE",   "full_form": "Integrated Development Environment" },
                { "abbr": "JSON",  "full_form": "JavaScript Object Notation" },
                { "abbr": "YAML",  "full_form": "YAML Ain’t Markup Language" },
                { "abbr": "XML",   "full_form": "Extensible Markup Language" },
                { "abbr": "CSV",   "full_form": "Comma-Separated Values" },
                { "abbr": "DB",    "full_form": "Database" },
                { "abbr": "SQL",   "full_form": "Structured Query Language" },
                { "abbr": "ORM",   "full_form": "Object-Relational Mapping" },
                { "abbr": "REST",  "full_form": "Representational State Transfer" },
                { "abbr": "gRPC",  "full_form": "Google Remote Procedure Call" },
                { "abbr": "JWT",   "full_form": "JSON Web Token" },
                { "abbr": "SSL",   "full_form": "Secure Socket Layer" },
                { "abbr": "TLS",   "full_form": "Transport Layer Security" },
                { "abbr": "EAT",  "full_form": "Engrove Audio Tools" },
                { "abbr": "AR",   "full_form": "Augmented Reality" },
                { "abbr": "FSD",  "full_form": "Feature-Sliced Design" },
                { "abbr": "RAG",  "full_form": "Retrieval-Augmented Generation" },
                { "abbr": "PSV",  "full_form": "Pre-Svarsverifiering" },
                { "abbr": "P-GB", "full_form": "Protokoll-Grundbulten" },
                { "abbr": "FL-D", "full_form": "Felsökningsloop-Detektor" },
                { "abbr": "KMM",  "full_form": "Konversationens Minnes-Monitor" },
                { "abbr": "KIV",  "full_form": "Kontextintegritets-Verifiering" },
                { "abbr": "DJTA", "full_form": "Dual-JSON-Terminal Artifact" },
                { "abbr": "PEA",  "full_form": "Pre-Execution Alignment" },
                { "abbr": "AI",    "full_form": "Artificial Intelligence" },
                { "abbr": "ML",    "full_form": "Machine Learning" },
                { "abbr": "DL",    "full_form": "Deep Learning" },
                { "abbr": "NLP",   "full_form": "Natural Language Processing" },
                { "abbr": "LLM",   "full_form": "Large Language Model" },
                { "abbr": "CI",    "full_form": "Continuous Integration" },
                { "abbr": "CD",    "full_form": "Continuous Delivery / Deployment" },
                { "abbr": "MVP",   "full_form": "Minimum Viable Product" },
                { "abbr": "PoC",   "full_form": "Proof of Concept" },
                { "abbr": "N/A",   "full_form": "Not Applicable" },
                { "abbr": "TBD",   "full_form": "To Be Determined" }
              ]
            }
          },
          {
            "action": "execute_core_instruction",
            "params": { 
              "source": "in_memory_files",
              "session start": "true",
              "follow policy": "docs/ai_protocols/AI_Core_Instruction.md"
            }
          }
        ]
    };
  } else {
    bundleConfig = {
      pbfVersion: "2.0",
      filename: `file_bundle_${getTimestamp()}.json`,
      sequence: [
          {
            "action": "decode_and_verify_payload",
            "description": "Dekodar, verifierar och laddar den inbäddade fil-payloaden i minnet som passiv kontext.",
            "params": { "payload_ref": "payload", "encoding_chain": ["base64", "zlib"], "hash_ref": "metadata.hash", "hash_algorithm": "SHA-256" }
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
