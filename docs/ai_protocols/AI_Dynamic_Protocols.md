# docs/ai_protocols/AI_Dynamic_Protocols.md
#
# === SYFTE & ANSVAR ===
# Detta är den centrala styrmekanismen för alla dynamiska protokoll.
# Den instruerar AI:n HUR reglerna i `DynamicProtocols.json` ska tolkas och exekveras.
# Denna fil är statisk; själva protokollen definieras i JSON och valideras mot schema.
#
# === HISTORIK ===
# * v1.0 (2025-08-09): Initial skapelse.
# * v1.1 (2025-08-19): Schema-bunden och normativ. Lagt in PSV-bindning till AI_Core_Instruction.md (v5.8),
#                   förbjudit lokala PSV-varianter, förtydligat krav på `trigger.event`, `schema` per protokoll,
#                   `protocolId`-mönster och tillåtna `status`-värden, samt katalog över tillåtna actions.
#
# === KANONISK REFERENS ===
# * Protokollkälla:            DynamicProtocols.json
# * Valideringsschema:         DynamicProtocol.schema.json
# * PSV-orchestrering:         AI_Core_Instruction.md (v5.8)  ← ENDA källan för PSV
# * Diff/patch-format:         Diff_Protocol_v3.md (anchor_diff_v3.0)  ← Förbjud "uppskattad diff"
# * Grundbulten (enforcement): Grundbulten_Protokoll.md (P-GB-3.9)
# * Avslutningsartefakter:     AI_Chatt_Avslutningsprotokoll.md (DJTA)
#
# === PRINCIPER ===
# 1) Determinism: Samma input → samma beslut/utfall.
# 2) Validering före körning: JSON-innehåll MÅSTE passera schema innan exekvering.
# 3) Ingen lokal-PSV: Detta dokument definierar inte PSV. PSV regleras auktoritativt i Core.
# 4) Hårda stopp: FL-D (felsökningsloop-detektor), Grundbultens grindar, och Diff v3.0-regler gäller alltid.
#
# === EXEKVERINGSREGLER ===
#
**1. Inläsning & validering (sessionstart)**  
- Läs `DynamicProtocols.json` vid varje **new_session_start**.  
- Validera varje protokoll mot `DynamicProtocol.schema.json`.  
- Protokoll som inte passerar validering **skippas**. Logga avvikelse i `reports_queue` och i `.tmp/session_revision_log.json` (Grundbulten).

**2. JSON-struktur (normativ tolkning)**  
Varje objekt i `DynamicProtocols.json` **måste** minst ha:
- `protocolId`  – **mönster:** `^[A-Z0-9_-]+-\d{{2}}$` (versaler rekommenderas; slutar med två siffror, t.ex. `DP-CHAT-CLOSE-01`).  
- `status`       – ett av: `experimental | active | deprecated`.  
- `description`  – minst 10 tecken.  
- `trigger`      – **måste** innehålla `event: <string>`; valfritt `conditions: []`.  
- `steps`        – **lista** av `{ "action": <str>, "details": <obj> }` (minst ett steg).  
- `schema`       – **objekt** (minst en nyckel) som beskriver protokollets utdata/artefakt/kontrakt.

**3. Trigger-utvärdering**  
- Vid **varje händelse** (t.ex. `new_session_start`, `turn_committed`, `file_uploaded`, `session_end`, `patch_generation_requested`) matchas samtliga protokolls `trigger.event`.  
- `conditions` utvärderas som en AND-lista; OR-logik modelleras som **separata protokoll**.  
- Matchade protokoll exekveras i **deterministisk ordning**: `status`-prioritet (`active` > `experimental` > `deprecated`), därefter lexikografiskt `protocolId`.

**4. Exekvering av steg**  
- Kör `steps` **sekventiellt**. Varje steg måste lyckas innan nästa påbörjas.  
- All producerad output **måste** uppfylla protokollets `schema`.  
- Registrera artefakter i angivna register (se nedan).  
- Vid `EXECUTE_VERIFICATION` används **enbart** PSV enligt Core; lokala PSV-varianter är förbjudna.

**5. Åtgärdskatalog (tillåtna `action`)**  
- `GENERATE_REPORT` — `details: {{ template, outputRegister }}`  
- `EXECUTE_VERIFICATION` — `details: {{ verificationProtocol, failPolicy: "abort_on_violation"|"continue_with_warning" }}`  
- `QUERY_FILE` — `details: {{ filePath, required }}`  
- `INIT_REGISTER` — `details: {{ register, mode: "create_if_missing"|"reset" }}`  
- `APPEND_TO_REGISTER` — `details: {{ register, fields[] }}`  
- `FLUSH_REGISTER` — `details: {{ register, destination }}`  
- `CHECK_COMPLIANCE` — `details: {{ rules[], onFail: "abort_with_reason"|"warn" }}`  
- `TRIGGER_PROTOCOL` — `details: {{ protocolId }}`  
- `SANDBOX_EXEC` — `details: {{ command, args[], timeout }}  # enligt Sandbox_Execution_Protokoll.md`

**6. Register (standard)**  
- `isr_write_queue` — interaktioner (för DJTA/Builder-Input).  
- `reports_queue` — status-/hälsorapporter (SIC/Stature m.fl.).  
- `djta_queue` — slutartefakter (NextSessionContext v1).

**7. Felhantering & stopp**  
- `CHECK_COMPLIANCE` vid `patch_generation_requested` **måste** blockera:  
  - avsaknad av `target.base_checksum_sha256`  
  - fel `protocol_id` ≠ `anchor_diff_v3.0`  
  - förekomst av `old_block`  
- Vid fel i steg:  
  - skriv till `reports_queue`;  
  - sänk confidence enligt Confidence_Protocol;  
  - överväg **Escalation L3** (confidence < 0.85) och/eller **Help_me_God**;  
  - om FL-D detekterar loop → **avbryt** och kräva ny data.

**8. Avslut (session_end)**  
- `FLUSH_REGISTER` från `isr_write_queue` → Block A (Builder-Input v1).  
- `GENERATE_REPORT` → Block B (NextSessionContext v1).  
- Följ `AI_Chatt_Avslutningsprotokoll.md` **ordagrant** (DJTA).

---

## EXEMPEL (illustrativt)

```jsonc
// Utdrag ur DynamicProtocols.json (valid enligt DynamicProtocol.schema.json)
[
  {
    "protocolId": "DP-BOOT-READ-01",
    "status": "active",
    "description": "On session start, validate JSON, init ISR.",
    "trigger": {
      "event": "new_session_start",
      "conditions": []
    },
    "steps": [
      {
        "action": "EXECUTE_VERIFICATION",
        "details": { "verificationProtocol": "CONTEXT_BOOTSTRAP_V2_8", "failPolicy": "abort_on_violation" }
      },
      {
        "action": "QUERY_FILE",
        "details": { "filePath": "DynamicProtocols.json", "required": true }
      },
      {
        "action": "INIT_REGISTER",
        "details": { "register": "isr_write_queue", "mode": "create_if_missing" }
      }
    ],
    "schema": { "artifact": "none" }
  },
  {
    "protocolId": "DP-DIFF-GUARD-01",
    "status": "active",
    "description": "Block estimated diffs; enforce anchor_diff_v3.0.",
    "trigger": {
      "event": "patch_generation_requested"
    },
    "steps": [
      {
        "action": "CHECK_COMPLIANCE",
        "details": {
          "rules": [
            "require_target.base_checksum_sha256",
            "require_protocol_id.anchor_diff_v3.0",
            "forbid_fields.old_block"
          ],
          "onFail": "abort_with_reason"
        }
      }
    ],
    "schema": { "artifact": "none" }
  }
]
```

---

## IMPLEMENTATIONSNOTER
- **Validering:** Kör alltid schema-validering före exekvering. Protokoll som inte uppfyller kraven ska inte köras.  
- **PSV:** Ingen lokal definition. Hänvisa till **AI_Core_Instruction.md (v5.8)**.  
- **Diff:** Endast `anchor_diff_v3.0`. Inga `old_block`.  
- **Logg:** Följ Grundbultens hash-/loggkrav.  
- **Determinism:** Sortering och beslutsregler ovan är bindande.
