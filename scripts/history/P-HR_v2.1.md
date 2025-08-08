# Protokoll för Historisk Rekonstruktion (P‑HR) v2.1 — *Fristående*

## Syfte
Återgenerera fullständiga avslutningsartefakter för äldre sessioner i **en enda JSON-fil per session**. Denna fil kan sedan batch‑processas till de fyra standardfilerna.

## Output (per historisk session)
Spara **exakt en** fil med namnet `[SESSIONID].json`. Den ska innehålla alla artefakter inbäddade enligt detta kontrakt:

```json
{
  "sessionId": "SESSIONID",
  "createdAt": "YYYY-MM-DDTHH:mm:ssZ",
  "artifacts": {
    "ByggLogg": {
      "sessionId": "SESSIONID",
      "date": "YYYY-MM-DDTHH:mm:ssZ",
      "summary": "…",
      "actions": [
        {
          "title": "…",
          "files": [
            {"path": "…", "changeDescription": "…"}
          ],
          "result": "…"
        }
      ],
      "projectStatus": "…"
    },
    "Chatthistorik": {
      "sessionId": "SESSIONID",
      "interactions": [
        {
          "speakerName": "Frankensteen",
          "model": {"provider": "OpenAI", "name": "gpt-5", "version": "2025-08-01"},
          "speaker": "Frankensteen (OpenAI:gpt-5@2025-08-01)",
          "summary": "…"
        }
      ]
    },
    "ai_protocol_performance": {
      "sessionId": "SESSIONID",
      "date": "YYYY-MM-DDTHH:mm:ssZ",
      "aiQualitativeSummary": "…",
      "scorecard": {
        "efficacy": {"score": 0, "weight": 0.4, "weightedScore": 0.0},
        "efficiency": {"score": 0, "weight": 0.3, "weightedScore": 0.0},
        "robustness": {"score": 0, "weight": 0.3, "weightedScore": 0.0},
        "finalScore": 0.0
      },
      "detailedMetrics": {
        "missionCompleted": true,
        "debuggingCycles": 0,
        "selfCorrections": 0,
        "externalCorrections": 0,
        "protocolActivations": {"psv": 0, "helpMeGod": 0, "stalemate": 0}
      },
      "improvementSuggestion": {
        "pattern": "…",
        "proposedHeuristicId": "H-YYYYMMDD-seq"
      }
    },
    "frankensteen_learning_db": {
      "heuristicId": "H-YYYYMMDD-seq",
      "trigger": {"type": "…", "scope": ["…"], "keywords": ["…"]},
      "identifiedRisk": {"riskId": "…", "description": "…"},
      "mitigation": {"protocolId": "…", "description": "…"},
      "metadata": {
        "originSessionId": "SESSIONID",
        "createdAt": "YYYY-MM-DDTHH:mm:ssZ",
        "status": "active",
        "sourceLogFiles": ["docs/ByggLogg.json", "docs/Chatthistorik.json"]
      }
    }
  }
}
```

> **Obs:** `frankensteen_learning_db` är **valfri**. Om ingen ny heuristik identifierats, utelämna nyckeln eller sätt värdet till `null`.

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
Använd medföljande Python‑skript för att läsa en mapp med `[SESSIONID].json` och generera:

- `docs/ByggLogg.json` (array, kronologisk)
- `docs/Chatthistorik.json` (array, kronologisk)
- `docs/ai_protocol_performance.json` (array, kronologisk)
- `tools/frankensteen_learning_db.json` (array, kronologisk — endast rader som finns)

Kronologisk sortering = stigande numeriskt `SESSIONID` i filnamn.
