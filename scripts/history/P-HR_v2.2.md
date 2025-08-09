# Protokoll för Historisk Rekonstruktion (P‑HR) v2.2 — *Fristående, v4.1-kompatibel*

## Syfte
Återgenerera fullständiga avslutningsartefakter för äldre sessioner i **en enda JSON-fil per session**. Filen kan senare batch‑processas till de fyra standardfilerna.

## Output (per historisk session)
Spara **exakt en** fil med namnet `[SESSIONID].json`. Den ska innehålla alla artefakter inbäddade enligt detta kontrakt:

```json
{
  "sessionId": "SESSIONID",
  "createdAt": "YYYY-MM-DDTHH:mm:ssZ",
  "artifacts": {
    "ByggLogg": { ... },
    "Chatthistorik": { ... },
    "ai_protocol_performance": { ... },
    "frankensteen_learning_db": [
      {
        "heuristicId": "H-YYYYMMDD-seq",
        "trigger": { "type": "…", "scope": ["…"], "keywords": ["…"] },
        "identifiedRisk": { "riskId": "…", "description": "…" },
        "mitigation": { "protocolId": "…", "description": "…" },
        "metadata": {
          "originSessionId": "SESSIONID",
          "createdAt": "YYYY-MM-DDTHH:mm:ssZ",
          "status": "active",
          "sourceLogFiles": ["docs/ByggLogg.json", "docs/Chatthistorik.json"]
        }
      }
    ]
  }
}
```
> **Not:** `frankensteen_learning_db` är **obligatorisk** som **array**. Om inga heuristiker skapades: använd tom array `[]`.

## Universell modelltaggning (obligatorisk)
- `speaker` måste vara: `"<speakerName> (<provider>:<model>@<version>)"`
- Maskinläsbart fält **måste** medfölja:
  ```json
  {"speakerName":"…","model":{"provider":"…","name":"…","version":"…"}}
  ```
- Okända värden ersätts med `"unknown"`.

## Leveranskrav
- Endast **en** JSON per session (`[SESSIONID].json`).
- 100 % giltig JSON, UTF‑8, LF‑radbrytning.

## Exekvering
1) Läs hela historiska chatten.  
2) Bygg artefakterna enligt ovanstående kontrakt.  
3) Skriv **en** fil: `[SESSIONID].json`.

---

## Batch‑konsolidering (körs separat)
Verktyg: `historical_reconstruction_builder.py` (v2). Skriptet konsoliderar flera sessioner till:

- `docs/ByggLogg.json` (array, kronologisk)
- `docs/Chatthistorik.json` (array, kronologisk)
- `docs/ai_protocol_performance.json` (array, kronologisk)
- `tools/frankensteen_learning_db.json` (array, kronologisk — **flatten** av alla heuristikobjekt över sessioner)

Kronologisk sortering = stigande numeriskt `SESSIONID` i filnamn.
