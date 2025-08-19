# docs/ai_protocols/In-Session_Amnesiac_Reset_Protocol.md
#
# === SYFTE & ANSVAR ===
# Formell "in-session" mjuk återställning av korttidsminne (KMM) utan att förlora beslut/heuristiker.
# Rensar KMM för fokus/token-kapacitet, bevarar formella lärdomar och återstartar kontexten kontrollerat.
#
# **Normativ bindning:** Körs under PSV enligt AI_Core_Instruction.md (v5.8).
# Måste följa Grundbulten P-GB-3.9 (hash/logg/diff) och uppdatera ISR/DJTA enligt AI_Chatt_Avslutningsprotokoll.md.
#
# === HISTORIK ===
# * v1.0 (2025-08-14): Initial skapelse.
# * v2.1 (2025-08-19): Hård confirm-sträng, formellt AmnesiaPacket-schema, RUN_CONTEXT_BOOTSTRAP v2.8,
#                   FL-D/Confidence/Escalation-koppling, ISR/loggkrav och jämförelsetabell utökad.

## 1) Aktivering (Trigger)

- Manuell aktivering av Engrove med exakt kommando:  
  **`Initiera In-Session Amnesiac Reset`**

- **Bekräftelsekrav:** AI svarar och kräver den exakta strängen **`CONFIRM RESET`**. Annat svar ⇒ **avbryt** utan sidoeffekter.

---

## 2) Processflöde

### Steg 0 — Förkontroll
- Kontrollera att PSV är aktiv (Core v5.8).  
- Notera status i `.tmp/session_revision_log.json` och ISR.

### Steg 1 — Bekräftelse och Varning
- Presentera varningen och invänta exakt **`CONFIRM RESET`**.  
- Ingen reset utan denna sträng.

### Steg 2 — Intern syntes av långtidsminne
- Extrahera det som ska bevaras:  
  - nya heuristiker (`H-...`), DT-2/DT-3-beslut, godkända dynamiska protokolländringar, öppna frågor/constraints  
  - senaste godkända filversioner (paths + sha256) och kort målsammanfattning

### Steg 3 — Generering av AmnesiaPacket_v1
- Skapa ett **enda** JSON-objekt enligt schema nedan.  
- Beräkna `content_hash_sha256` över `preserved_context`.  
- Skriv `isr_event = "isr_reset_prepare"` med tidsstämpel.

### Steg 4 — Leverans och instruktion
- Visa JSON i kodblock. Instruktion: *”Kopiera och skicka paketet som nästa prompt.”*  
- **Sekretessgaller:** Paketet får **inte** innehålla hemliga nycklar/PII. Upptäcks det ⇒ **avbryt** och begär sanering.

### Steg 5 — Post‑Reset exekvering
När paketet tas emot:
1) Verifiera schema + `content_hash_sha256`. Mismatch ⇒ **avbryt**.  
2) Rensa **endast** KMM; långtidslogg/ISR bevaras.  
3) Återställ omedelbar kontext från `preserved_context`.  
4) Kör **RUN_CONTEXT_BOOTSTRAP v2.8** (context_bootstrap_instruction.md).  
5) Append ISR: `{ "event":"isr_reset", "base_session_id": "...", "content_hash_sha256":"..." }`.  
6) Kör **SIC → Stature**. Status `WARNING|ERROR` ⇒ rekommendera **HITL Plan Review**.

---

## 3) Felhantering & Stoppnivåer
- **FL‑D** (felsökningsloopdetektor) slår ⇒ avbryt reset-varv, begär ny kontext.  
- Två misslyckade reset-försök i samma session ⇒ **Escalation L3** (Konsult).  
- **Confidence < 0.85** efter post‑reset ⇒ **HITL Pre‑Commit** krävs innan skrivande åtgärder.

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
    "decisions": ["DT-2", "DT-3"],
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

## 5) Jämförelse med andra protokoll

| Protokoll                 | Syfte                                 | Bevarar lärdomar? | Avslutar sessionen? | Kör Bootstrap? |
|--------------------------|----------------------------------------|-------------------|---------------------|----------------|
| **P‑ISAR**               | Mjuk reset av KMM                      | **Ja**            | **Nej**             | **Ja**         |
| **Avslutningsprotokoll** | Kontrollerad avslutning & arkivering   | **Ja**            | **Ja**              | Nej (nästa ses)|
| **FORCE_SESSION_RESTART**| Hård kärnomstart (nödfall)             | **Nej**           | **Ja**              | **Ja (implicit)** |

---

## 6) Integritet & Logg (P‑GB‑3.9)
- Alla åtgärder loggas i `.tmp/session_revision_log.json` med tidsstämpel.  
- ISR uppdateras vid Steg 3 och 5.  
- Hashar ska verifieras före och efter reset.

---

## 7) Implementationsnoter
- Körs under **PSV** (Core v5.8).  
- Kopplingar: `HITL_Interrupt_Points.md`, `Structured_Debugging_Checklist.md`, `Confidence_Protocol.md`, `Escalation_Protocol.md`, `context_bootstrap_instruction.md`.
