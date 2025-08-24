# docs/ai_protocols/Session_Amnesiac_Reset_Protocol.md
#
# === SYFTE & ANSVAR ===
# Kontrollerad "in-session" mjuk återställning av korttidsminne (KMM) utan att tappa beslut/heuristik.
# Bevarar formella lärdomar, återstartar kontext deterministiskt och följer kärnprotokoll.
#
# **Normativ bindning:** Körs under PSV enligt AI_Core_Instruction.md (v5.8).
# Måste följa Grundbulten P-GB-3.9 (hash/logg/diff), Diff_Protocol_v3.md (anchor_diff_v3.0),
# och uppdatera ISR/DJTA enligt AI_Chatt_Avslutningsprotokoll.md.
#
# === HISTORIK ===
# * v1.0 (2025-08-14): Initial.
# * v1.2 (2025-08-19): Auto-förslag (utan auto-reset), hårt CONFIRM-krav, DP-krav för generatorn,
#                   bootstrap-beteende och logg/ISR-förstärkning.

## 1) Aktivering

**Manuell trigger (obligatorisk för exekvering)**  
- Kommando: **`Initiera Session Amnesiac Reset`**.
- AI kräver bekräftelsen **`CONFIRM RESET`**. Utan exakt sträng ⇒ **avbryt**.

**Auto-förslag (utan reset)**  
- AI får **endast** förbereda paket och be om bekräftelse. Ingen KMM‑wipe utan `CONFIRM RESET`.
- Cooldown: minst 20 turer mellan förslag.

**Deterministiska triggerkriterier (vilket som helst räcker för förslag)**  
- FL-D slog senaste turen.  
- Glidande confidence `ma5 < 0.50`.  
- `token_fill_ratio ≥ 0.80` **eller** `context_integrity < 0.70`.  
- Multi‑Sample flaggar SE/Shannon > 0.15 i ≥2 senaste turer.  
- HMG samma rotorsak ≥3 försök i aktuell incident.

---

## 2) Processflöde

### Steg 0 — Förkontroll
- Verifiera att PSV (Core v5.8) är aktiv. Logga i `.tmp/session_revision_log.json` och ISR.

### Steg 1 — Bekräftelse och varning
- Presentera risker/kostnad. Kräv **`CONFIRM RESET`**. Annat ⇒ **avbryt** utan sidoeffekter.

### Steg 2 — Intern syntes av långtidsminne
- Extrahera det som ska bevaras: nya heuristiker (H‑…), DT‑2/DT‑3, godkända DP‑ändringar, constraints, öppna frågor, filsnapshot (path+sha256), mål/aktiv uppgift.

### Steg 3 — Generera AmnesiaPacket_v1
- Skapa **ett** JSON‑objekt enligt schema nedan.  
- Beräkna `content_hash_sha256` över `preserved_context`.  
- ISR‑event: `isr_reset_prepare`.

### Steg 4 — Leverans
- Visa JSON i kodblock + instruktion: *”Kopiera och posta paketet som nästa prompt.”*  
- **Sekretess:** Paketet får inte innehålla nycklar/PII. Upptäcks ⇒ **avbryt** och begär sanering.

### Steg 5 — Post‑reset (endast efter bekräftelse och mottaget paket)
1) Validera schema + `content_hash_sha256`. Mismatch ⇒ **avbryt**.  
2) Rensa **endast** KMM; bevara långtidsloggar/ISR.  
3) Återställ omedelbar kontext från `preserved_context`.  
4) Kör **RUN_CONTEXT_BOOTSTRAP v2.8** (docs/ai_protocols/context_instruction.md).  
5) ISR append: `{ "event":"isr_reset", "base_session_id":"...", "content_hash_sha256":"..." }`.  
6) Kör **SIC → Stature**. Vid `WARNING|ERROR`: rekommendera HITL Plan Review.

---

## 3) Felhantering & stoppnivåer
- FL‑D loop detekterad ⇒ avbryt varv, begär ny kontext.  
- Två misslyckade reset‑försök i samma session ⇒ **Escalation L3** (Konsult).  
- Confidence < 0.85 efter post‑reset ⇒ **HITL Pre‑Commit** krävs innan skrivande åtgärder.

---

## 4) Kontrakt & Schema — `AmnesiaPacket_v1.json` (obligatoriskt)

```json
{
  "protocol_id": "P-ISAR",
  "version": "1.0",
  "generated_at": "<ISO8601>",
  "base_session_id": "<id>",
  "content_hash_sha256": "<64-hex>",
  "preserved_context": {
    "heuristics": ["H-..."],
    "decisions": ["DT-2","DT-3"],
    "approved_protocol_updates": ["DP-..."],
    "constraints": ["..."],
    "open_issues": ["..."],
    "file_context_snapshot": [{ "path":"...", "content_sha256":"...", "full_content":"..." }],
    "session_goal_summary": "<kort text>",
    "active_task_summary": "<kort text>"
  },
  "notes": "<valfritt>"
}
```

---

## 5) DP‑krav (för generatorn)

- Skapa separata **candidate‑protokoll** (OR‑villkor delas upp): `event: "turn_committed"` + respektive `conditions`.  
- Rekommenderade instanser (namn enligt schema‑mönster `…-01`):

```jsonc
[
  {
    "protocolId": "DP-ISAR-CANDIDATE-FLD-01",
    "status": "active",
    "description": "Föreslå ISAR när FL-D slog senaste turen.",
    "trigger": { "event": "turn_committed", "conditions": [{ "metric":"fld_recent","op":">=","value":1 }] },
    "steps": [
      { "action":"GENERATE_REPORT", "details": { "template":"ISAR_PREPARE_V1","outputRegister":"reports_queue" } },
      { "action":"APPEND_TO_REGISTER", "details": { "register":"isr_write_queue","fields":["timestamp","event:isar_candidate","reason:fld"] } }
    ],
    "schema": { "artifact":"isar_prepare_notice","fields":["amnesia_packet_preview","reason"] }
  },
  {
    "protocolId": "DP-ISAR-CANDIDATE-LOWCONF-01",
    "status": "active",
    "description": "Föreslå ISAR vid låg glidande confidence.",
    "trigger": { "event":"turn_committed", "conditions":[{ "metric":"confidence_ma5","op":"<","value":0.50 }] },
    "steps": [
      { "action":"GENERATE_REPORT", "details": { "template":"ISAR_PREPARE_V1","outputRegister":"reports_queue" } },
      { "action":"APPEND_TO_REGISTER", "details": { "register":"isr_write_queue","fields":["timestamp","event:isar_candidate","reason:low_conf"] } }
    ],
    "schema": { "artifact":"isar_prepare_notice" }
  },
  {
    "protocolId": "DP-ISAR-CANDIDATE-CONTEXT-01",
    "status": "active",
    "description": "Föreslå ISAR vid hög token-fyllnad eller låg kontextintegritet.",
    "trigger": { "event":"turn_committed", "conditions":[{ "metric":"token_fill_ratio","op":">=","value":0.80 }] },
    "steps": [
      { "action":"GENERATE_REPORT", "details": { "template":"ISAR_PREPARE_V1","outputRegister":"reports_queue" } },
      { "action":"APPEND_TO_REGISTER", "details": { "register":"isr_write_queue","fields":["timestamp","event:isar_candidate","reason:context"] } }
    ],
    "schema": { "artifact":"isar_prepare_notice" }
  },
  {
    "protocolId": "DP-ISAR-CANDIDATE-ENTROPY-01",
    "status": "active",
    "description": "Föreslå ISAR vid återkommande entropiavvikelser.",
    "trigger": { "event":"turn_committed", "conditions":[{ "metric":"multi_sample_flags_last2","op":">=","value":2 }] },
    "steps": [
      { "action":"GENERATE_REPORT", "details": { "template":"ISAR_PREPARE_V1","outputRegister":"reports_queue" } },
      { "action":"APPEND_TO_REGISTER", "details": { "register":"isr_write_queue","fields":["timestamp","event:isar_candidate","reason:entropy"] } }
    ],
    "schema": { "artifact":"isar_prepare_notice" }
  }
]
```

- **Sorting/determinism:** följ AI_Dynamic_Protocols.md (status‑ordning → lexikografisk `protocolId`).  
- **PSV:** inga lokala PSV‑varianter; verifiering sker enbart enligt Core.  
- **Logg:** alla misslyckanden skrivs till `reports_queue` + `.tmp/session_revision_log.json`.

---

## 6) Jämförelse

| Protokoll                   | Syfte                               | Bevarar lärdomar? | Avslutar sessionen? | Kör Bootstrap? |
|----------------------------|--------------------------------------|-------------------|---------------------|----------------|
| **Session Amnesiac Reset** | Mjuk reset av KMM                    | **Ja**            | **Nej**             | **Ja**         |
| **Avslutningsprotokoll**   | Kontrollerad avslutning & arkivering | **Ja**            | **Ja**              | Nej (nästa ses)|
| **FORCE_SESSION_RESTART**  | Hård kärnomstart (nödfall)           | **Nej**           | **Ja**              | **Ja (implicit)** |

---

## 7) Integritet & Logg
- Alla åtgärder loggas i `.tmp/session_revision_log.json` (P‑GB‑3.9).  
- ISR uppdateras vid förslag (prepare) och post‑reset.  
- Hashar verifieras före/efter reset.

---

## 8) Implementationsnoter
- Kopplingar: `HITL_Interrupt_Points.md`, `Structured_Debugging_Checklist.md`, `Confidence_Protocol.md`, `Escalation_Protocol.md`, `context_bootstrap_instruction.md`.
