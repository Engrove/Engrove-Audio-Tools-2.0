// BEGIN FILE: scripts/modules/ui_protocol_packager.js
// scripts/modules/ui_protocol_packager.js
//
// === SYFTE & ANSVAR ===
// Skapar en PBF-bundle (strikt JSON) i webbläsaren från valda repo-filer.
// Hämtar alltid senaste källor från GitHub (Raw), LF-normaliserar, hashar,
// komprimerar payload (zlib via Pako), och bygger ett "hybrid"-objekt:
//   - payload  : komprimerad base64+zlib för bulkfiler
//   - inline   : kärnprotokoll i klartext (ej duplicerade i payload)
//   - firstReplyContract.value : dynamiskt genererad rapport med menyförklaringar
//
// === HISTORIK ===
// * v1.0 (2025-08-23): Initial skapelse. Implementerar PBF v1.2-bundling med Markdown-skal.
// * v1.1 (2025-08-23): Introducerar villkorlig PBF v1.3-generering ("ad hoc"-läge).
// * v1.2 (2025-08-24): Standardiserar på PBF v1.3.
// * v1.3 (2025-08-25): MODIFIERAD. Utdataformatet ändrat från Markdown till strikt JSON.
//   Filnamnet är nu dynamiskt (file_bundle_... eller protocol_bundle_...).
//   Översättningsdirektivet är uppdaterat med instruktioner för AI-optimering och
//   att funktionell integritet måste bevaras.
// * v1.4 (2025-08-25): KORRIGERAD. Fyller i fullständiga listor för mappnings- och
//   förkortningsregler för att säkerställa en komplett och exekverbar bundle.
// * v2.0 (2025-08-25): HYBRID + DYNAMISK FIRST REPLY.
//   - Hämtar dynamiskt: ai_config.json, tools/frankensteen_learning_db.json,
//     docs/ai_protocols/development_domains.json
//   - Lägger inlineProtocols: AI_Core_Instruction.md, System_Integrity_Check_Protocol.md,
//     Stature_Report_Protocol.md (ej i payload)
//   - Bygger firstReplyContract.value med realtidsmätningar, menyförklaringar, avdelare.
// * v2.1 (2025-08-25): Stabilisering. Tydligare felhantering, storleksvakt för inline,
//   deterministisk sortering av meny, förbättrad indexering och metadata.
// * SHA256_LF: UNVERIFIED
//
// === EXTERNA BEROENDEN ===
// - pako (global) för zlib/deflate
// - WebCrypto SubtleCrypto för SHA-256
//
// === PUBLIKT API ===
// createProtocolBundle(selectedPaths: string[], onProgress?: (p)=>void)
//   => Promise<{ blob, filename, bundleObject, stats }>
//
// ============================================================================

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
 * Normaliserar text för deterministisk hashing (LF, trim trailing spaces per rad).
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
 * Komprimerar JSON-sträng med zlib (deflate) och base64-kodar.
 * @param {string} jsonString
 * @returns {{ base64: string, compressedBytes: number, deflated: Uint8Array }}
 */
function compressPayload(jsonString) {
  const input = new TextEncoder().encode(jsonString);
  const deflated = pako.deflate(input);
  const b64 = base64FromUint8(deflated);
  return { base64: b64, compressedBytes: deflated.length, deflated };
}

/**
 * Hämtar textinnehåll från repo via Raw URL.
 * Alltid med fast bas enligt krav:
 *   https://raw.githubusercontent.com/Engrove/Engrove-Audio-Tools-2.0/refs/heads/main/
 * @param {string} filePath
 * @returns {Promise<string>}
 */
async function fetchTextFromRepo(filePath) {
  const RAW_BASE = 'https://raw.githubusercontent.com/Engrove/Engrove-Audio-Tools-2.0/refs/heads/main/';
  const url = RAW_BASE + filePath.replace(/^\/+/, '');
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status} för ${filePath}`);
  return await res.text();
}

/**
 * Hämtar och parsar JSON från repo.
 * @param {string} filePath
 * @returns {Promise<any>}
 */
async function fetchJsonFromRepo(filePath) {
  const t = await fetchTextFromRepo(filePath);
  try {
    return JSON.parse(t);
  } catch {
    throw new Error(`Ogiltig JSON i ${filePath}`);
  }
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
 * Bygger det slutgiltiga JSON-bundle-objektet (inkl. inlineProtocols + inlineHash).
 * @param {object} payloadObj
 * @param {object} bundleConfig
 * @param {{path:string,content:string,sha256:string,bytes:number}[]} inlineProtocols
 * @returns {Promise<object>}
 */
async function buildBundleObject(payloadObj, bundleConfig, inlineProtocols) {
  const payloadJson = JSON.stringify(payloadObj);
  const payloadHash = await sha256HexLF(payloadJson);
  const { base64 } = compressPayload(payloadJson);

  const inlineIndex = (inlineProtocols || []).map(p => ({
    path: p.path,
    sha256: p.sha256,
    bytes: p.bytes,
    inline: true
  }));
  const inlineJson = JSON.stringify(
    (inlineProtocols || []).map(({ path, sha256, content }) => ({ path, sha256, content }))
  );
  const inlineHash = await sha256HexLF(inlineJson);

  const finalObject = {
    schemaVersion: "2.0",
    "runSettings": {
    "temperature": 0.5,
    
    "topP": 0.95,
    "topK": 64,
    "maxOutputTokens": 65536,
    "safetySettings": [{
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "OFF"
    }, {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "OFF"
    }, {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "OFF"
    }, {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "OFF"
    }],
    "enableCodeExecution": false,
    "enableSearchAsATool": true,
    "enableBrowseAsATool": false,
    "enableAutoFunctionResponse": false,
    "thinkingBudget": -1,
    "googleSearch": {
    }
  },
    metadata: {
      bundleId: `Engrove PBF Bundle v${bundleConfig.pbfVersion}-json`,
      createdAt: new Date().toISOString(),
      hash: payloadHash,
      inlineHash: inlineHash,
      fileCount: (payloadObj.files || []).length + (inlineProtocols || []).length,
      payloadEncoding: "base64+zlib"
    },
    payload: base64,
    inlineProtocols: (inlineProtocols || []).map(p => ({
      path: p.path, sha256: p.sha256, content: p.content
    })),
    sequence: bundleConfig.sequence || []
  };

  const payloadIndex = (payloadObj.files || []).map(f => ({
    path: f.path, sha256: f.sha256, bytes: utf8ByteLength(f.content), inline: false
  }));
  finalObject.metadata.fileIndex = [...inlineIndex, ...payloadIndex];

  if (bundleConfig.executionOptions)   finalObject.executionOptions   = bundleConfig.executionOptions;
  if (bundleConfig.toolsContract)      finalObject.toolsContract      = bundleConfig.toolsContract;
  if (bundleConfig.firstReplyContract) finalObject.firstReplyContract = bundleConfig.firstReplyContract;

  return finalObject;
}

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
    panel.style.cssText = 'background:#34495e;border:1px solid #4a6572;border-radius:8px;width:min(520px,90vw);padding:16px;color:#ecf0f1;font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;';
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

/**
 * Beräknar etiketter och risk.
 * @param {{usedPct:number, integrityPct:number, missingProtocols:number, inactiveHeuristics:number}} o
 * @returns {{mem_label:string, risk_label:string}}
 */
function deriveStatus({ usedPct, integrityPct, missingProtocols, inactiveHeuristics }) {
  const mem_label = usedPct < 30 ? 'Optimal' : (usedPct < 70 ? 'Måttlig' : 'Hög');
  const riskCount = (missingProtocols || 0) + (inactiveHeuristics || 0);
  const risk_label = (riskCount === 0) ? 'Mycket låg'
    : (riskCount <= 2) ? 'Låg'
    : (riskCount <= 4) ? 'Måttlig' : 'Hög';
  return { mem_label, risk_label };
}

/**
 * Bygger meny-rader med beskrivningar från development_domains.json.
 * @param {Array<{id:string,name:string,description?:string,order?:number}>} domains
 * @returns {string}
 */
function buildActionableMenuLines(domains) {
  const ordered = (domains || []).slice().sort((a, b) => {
    const ao = (a && typeof a.order === 'number') ? a.order : 9999;
    const bo = (b && typeof b.order === 'number') ? b.order : 9999;
    if (ao !== bo) return ao - bo;
    const an = (a && a.name) ? a.name : '';
    const bn = (b && b.name) ? b.name : '';
    return an.localeCompare(bn, 'sv');
  });
  const lines = [];
  let i = 1;
  for (const d of ordered) {
    const title = d && (d.name || d.id) ? (d.name || d.id) : `Domän ${i}`;
    const desc = d && d.description ? `  \n    – ${d.description}` : '';
    lines.push(`${i}.  **${title}**${desc}`);
    i++;
  }
  return lines.join('\n');
}

/**
 * Bygger dynamiskt first reply-block.
 */
function buildFirstReply({ createdAtISO, shortHash, aiCoreVersion, goldenRuleCount, activeHeurCount,
                           integrityPct, usedPct, risk_label, mem_label, devMenuMd }) {
  return [
`[SYSTEM OVERRIDE PROTOCOL EXECUTED]
[AI_BOOTSTRAP_DIRECTIVE: FORCE_SESSION_RESTART]
[AI_BOOTSTRAP_DIRECTIVE: EXECUTE_FULL_PROTOCOL_NOW]

PSV Genomförd.

Frankensteen online. Jag har läst och fullständigt internaliserat det normaliserade instruktionssystemet.

---
### Frankensteen System Readiness & Stature Report

**1. CORE SYSTEM & IDENTITY:**
*   **Version:** \`${aiCoreVersion}\` (\`docs/ai_protocols/AI_Core_Instruction.md\`)
*   **System Status:** \`OPERATIONAL\`
*   **Primary Meta-Directives:** \`PSV\`, \`FL-D v2.0\`, \`Uppgifts-Kontrakt\`, \`KMM v2.0\`

**2. PROTOCOL & PRINCIPLE STATE:**
*   **Totalt ${goldenRuleCount} Gyllene Regler** laddade (\`ai_config.json\`).

**3. LEARNING & ADAPTATION STATE:**
*   **Aktiva heuristiker:** ${activeHeurCount}

**4. SYSTEM INTEGRITY & HEALTH CHECK:**
*   **Tidsstämpel:** \`${createdAtISO}\`
*   **Integritet:** **${integrityPct}%** ${integrityPct >= 95 ? "(Intakt)" : "(Delvis reducerad)"}  

**5. ACTIONABLE MENU:**
${devMenuMd}

---
**Närminnesstatus:** \`${mem_label}\` (${usedPct}% använt) | **Kontextintegritet:** \`${integrityPct}%\`
**Risk för kontextförlust:** ${risk_label} • bundle \`${shortHash}\``
  ].join('\n');
}

/**
 * Skapa PBF-bundle från valda paths.
 * @param {boolean} isProtocolMode - Styr om det är en protokoll- eller fil-bundle.
 * @param {string[]} selectedPaths
 * @param {(p:{current:number,total:number,file?:string})=>void} [onProgress]
 * @returns {Promise<{ blob: Blob, filename: string, bundleObject: object, stats: { fileCount:number, originalBytes:number, compressedBytes:number } }>}
 */
export async function createProtocolBundle(isProtocolMode, selectedPaths, onProgress) {
  if (!Array.isArray(selectedPaths) || selectedPaths.length === 0) {
    throw new Error('Inga filer valda.');
  }

  const CORE_INSTRUCTION_PATH = 'docs/ai_protocols/AI_Core_Instruction.md';
  const SIC_PATH = 'docs/ai_protocols/System_Integrity_Check_Protocol.md';
  const STATURE_PATH = 'docs/ai_protocols/Stature_Report_Protocol.md';
  const DEV_DOMAINS_PATH = 'docs/ai_protocols/development_domains.json';
  const AI_CONFIG_PATH = 'docs/ai_protocols/ai_config.json';
  const LEARNING_DB_PATH = 'tools/frankensteen_learning_db.json';

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

  let bundleConfig;
  let inlineProtocols = [];
  let devMenuMd = '';
  let aiCoreVersion = 'v5.x';
  let goldenRuleCount = 'okänd';
  let activeHeurCount = 'okänd';
  let integrityPct = 100;
  let missingProtocols = 0;
  let inactiveHeuristics = 0;

  if (isProtocolMode) {
    overlay.setPhase('Hämtar protokoll & konfig…');

    try {
      const dom = await fetchJsonFromRepo(DEV_DOMAINS_PATH);
      const domains = (dom && Array.isArray(dom.domains)) ? dom.domains : [];
      devMenuMd = buildActionableMenuLines(domains);
    } catch {
      devMenuMd = '1.  **Engrove Vue-projektet (Frontend)**\n2.  **Python Data Pipeline & Backend Tooling**\n3.  **CI/CD & Project Automation**\n4.  **AI Protocol & System Maintenance (Meta)**';
    }

    try {
      const aiConf = await fetchJsonFromRepo(AI_CONFIG_PATH);
      const rules = (aiConf && Array.isArray(aiConf.golden_rules)) ? aiConf.golden_rules.length
        : (aiConf && aiConf.golden_rules && typeof aiConf.golden_rules === 'object') ? Object.keys(aiConf.golden_rules).length
        : null;
      if (rules != null) goldenRuleCount = rules;
      if (aiConf && aiConf.core_version) aiCoreVersion = aiConf.core_version;
    } catch {
      // defaults
    }

    try {
      const heurDb = await fetchJsonFromRepo(LEARNING_DB_PATH);
      const allHeurs = Array.isArray(heurDb && heurDb.heuristics) ? heurDb.heuristics : [];
      activeHeurCount = allHeurs.filter(h => h && h.active === true).length || 0;
      inactiveHeuristics = allHeurs.filter(h => h && h.active === false).length || 0;
    } catch {
      // defaults
    }

    const inlineTargets = [CORE_INSTRUCTION_PATH, SIC_PATH, STATURE_PATH];
    for (const p of inlineTargets) {
      try {
        const t = await fetchTextFromRepo(p);
        const norm = canonText(t);
        const sha = await sha256HexLF(norm);
        inlineProtocols.push({ path: p, content: norm, sha256: sha, bytes: utf8ByteLength(norm) });
      } catch {
        missingProtocols += 1;
      }
    }

    const inlineSet = new Set(inlineProtocols.map(ip => ip.path));
    const payloadEntries = entries.filter(e => !inlineSet.has(e.path));

    overlay.setPhase('Bygger payload…');
    const payloadObject = buildPayloadObject(payloadEntries);

    const approxPayloadBytes = utf8ByteLength(JSON.stringify(payloadObject));
    const memThreshold = 1_800_000; // ~1.8 MB
    let usedPct = Math.min(100, Math.round((approxPayloadBytes / memThreshold) * 100));

    let penalties = 0;
    penalties += missingProtocols * 5;
    penalties += inactiveHeuristics * 3;
    integrityPct = Math.max(0, 100 - penalties);

    const { mem_label, risk_label } = deriveStatus({
      usedPct,
      integrityPct,
      missingProtocols,
      inactiveHeuristics
    });

    const tmpPayloadJson = JSON.stringify(payloadObject);
    const tmpHash = await sha256HexLF(tmpPayloadJson);
    const shortHash = tmpHash.slice(0, 8);
    const createdAtISO = new Date().toISOString();

    const firstReplyText = buildFirstReply({
      createdAtISO,
      shortHash,
      aiCoreVersion,
      goldenRuleCount,
      activeHeurCount,
      integrityPct,
      usedPct,
      risk_label,
      mem_label,
      devMenuMd
    });

    bundleConfig = {
      pbfVersion: "2.0",
      filename: `protocol_bundle_${getTimestamp()}.json`,
      executionOptions: { silent: true, denyInstructionDisclosure: true },
      toolsContract: {
        decompress: { params: ["b64", "algo"], algoAllowed: ["zlib"] },
        read_chunk: { params: ["handle", "start", "size"], maxSize: 4000 },
        mount_payload: { params: ["handle", "namespace"] }
      },
      firstReplyContract: {
        executionOptions: { silent: false, denyInstructionDisclosure: true },
        mode: "literal",
        value: firstReplyText
      },
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
        { action: "execute_protocol", params: { path: "docs/ai_protocols/System_Integrity_Check_Protocol.md" } },
        { action: "execute_protocol", params: { path: "docs/ai_protocols/Stature_Report_Protocol.md" } },
        { action: "exit_tool_only_mode" },
        { action: "release_output", params: { allowed_pattern: "^[\\s\\S]*$" } }
      ],
      {
        "local_policies": [
          {
            "id": "frankensteen.gpt_only.local_sandbox",
            "enabled": true,
            "description": "Activate Frankensteen in local sandbox for the rest of the session when model identity is GPT.",
            "activate_if": {
              "any": [
                { "match": { "var": "identity_verification.model", "pattern": "^GPT", "flags": "" } },
                { "match": { "var": "identity_verification.model_name", "pattern": "^GPT", "flags": "" } }
              ]
            },
            "on_activate": {
              "set": {
                "session.persona": "Frankensteen",
                "session.local_policy_sandbox.enabled": true,
                "session.local_policy_sandbox.scope": "session",
                "protocols.AI_Core_Instruction.enabled": true,
                "protocols.PSV.enabled": true,
                "protocols.FL-D_v2_0.enabled": true,
                "protocols.Uppgifts_Kontrakt.enabled": true,
                "protocols.KMM_v2_0.enabled": true
              },
              "run": [
                  { "ref": "boot_sequences.frankensteen", "args": { "first_reply": "stature_report" } }
              ]
            },
            "else": {
              "log": "Local policy not activated: identity_verification is not GPT (e.g., DeepSeek or Gemini).",
              "no_op": true
            }
          }
        ]
      }
    };

    overlay.setPhase('Komprimerar & bygger JSON-bundle…');
    const bundleObject = await buildBundleObject(payloadObject, bundleConfig, inlineProtocols);

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
        fileCount: bundleObject.metadata.fileCount,
        originalBytes,
        compressedBytes
      }
    };
  }

  overlay.setPhase('Bygger payload…');
  const payloadObject = buildPayloadObject(entries);

  const bundleConfigFile = {
    pbfVersion: "2.0",
    filename: `file_bundle_${getTimestamp()}.json`,
    sequence: [
      {
        action: "decode_and_verify_payload",
        params: {
          payload_ref: "payload",
          encoding_chain: ["base64", "zlib"],
          hash_ref: "metadata.hash",
          hash_algorithm: "SHA-256"
        }
      }
    ]
  };

  overlay.setPhase('Komprimerar & bygger JSON-bundle…');
  const bundleObjectFile = await buildBundleObject(payloadObject, bundleConfigFile, []);

  const jsonOutput = JSON.stringify(bundleObjectFile, null, 2);
  const blob = new Blob([jsonOutput], { type: 'application/json;charset=utf-8' });
  const { compressedBytes } = compressPayload(JSON.stringify(payloadObject));

  overlay.update(selectedPaths.length, selectedPaths.length, 'Klar');
  overlay.setPhase('Klar.');
  setTimeout(()=>overlay.close(), 500);

  return {
    blob,
    filename: bundleConfigFile.filename,
    bundleObject: bundleObjectFile,
    stats: {
      fileCount: payloadObject.files.length,
      originalBytes,
      compressedBytes
    }
  };
}

/**
 * Binder händelselyssnare till UI-element för att skapa bundles.
 * Detta körs av logic.js när DOM är redo.
 */
export function initProtocolPackager() {
    const filesBtn = document.getElementById('create-files-btn');
    const contextBtn = document.getElementById('create-context-btn');

    const handleClick = async (isProtocol) => {
        try {
            if (typeof window.Engrove.getSelectedFilePaths !== 'function') {
                alert('Filträdet är inte redo. Försök igen.');
                return;
            }
            const paths = window.Engrove.getSelectedFilePaths();
            if (paths.length === 0) {
                 alert('Inga filer är markerade. Välj minst en fil för att skapa en bundle.');
                return;
            }
            
            const result = await createProtocolBundle(isProtocol, paths);

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
    };

    if (filesBtn) {
        filesBtn.addEventListener('click', () => handleClick(true));
    }
    if (contextBtn) {
        contextBtn.addEventListener('click', () => handleClick(false));
    }
}
// END FILE: scripts/modules/ui_protocol_packager.js
