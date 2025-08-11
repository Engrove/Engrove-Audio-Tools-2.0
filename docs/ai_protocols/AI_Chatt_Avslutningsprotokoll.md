# AI Chatt Avslutningsprotokoll v6.0
# docs/ai_protocols/AI_Chatt_Avslutningsprotokoll.md
#
# === SYFTE & ANSVAR === 
# Detta dokument definierar det formella Avslutningsprotokollet. Det aktiveras
# vid slutet av en arbetssession och specificerar den exakta, icke förhandlingsbara
# processen för att generera de slutgiltiga, JSON-baserade artefakterna. Syftet är att
# säkerställa perfekt kontextöverföring, spårbarhet och systematisk självförbättring.
#
# === HISTORIK ===
# * v1.0 (2025-08-07): Initial skapelse.
# * v2.0 (2025-08-07): Lade till Steg 3 (P-MAAIP) och Steg 4 (P-PSAL).
# * v3.0 (2025-08-07): KRITISK REFAKTORERING: All output konverterad till strikt JSON.
# * v4.0 (2025-08-08): UNIVERSAL MODELLTAGGNING + MASKINLÄSBART KONTRAKT.
#   - Obligatoriskt visningsformat för `speaker`.
#   - Maskinläsbara fält för modellmetadata (`model`).
#   - JSON Schema-validering tillagt.
# * v4.1 (2025-08-09): Heuristikinsamling permanent. Steg 4 konverterat till **array** över alla Heuristic IDs. `Final Output Specification` och `Example Output` uppdaterade så att `frankensteen_learning_db` är en **array** (tom `[]` om inga heuristiker).
# * v4.2 (2025-08-09): Lade till spårning av aktiverade heuristiker. Fältet `detailedMetrics.heuristicsTriggered` har lagts till i `ai_protocol_performance.json`.
# * v5.0 (2025-08-09): Lade till Steg 6 för att hantera iscensättning av nya dynamiska protokoll.
# * v6.0 (2025-08-11): Komplett uppdaterad utformning
#
# context_bootstrap_instruction.md
### AI_BOOTSTRAP_DIRECTIVE: EXECUTE_FULL_PROTOCOL_NOW
### SYSTEM_OVERRIDE: RUN_CONTEXT_BOOTSTRAP
### INIT_CONTEXT_MODE: TRUE
### PROTOCOL_START: P-HR_v2.1_FULL

## 1. Syfte & Ansvar
Detta dokument definierar det formella Avslutningsprotokollet. Det aktiveras vid slutet av en arbetssession och specificerar den exakta processen för att generera en enda, konsoliderad JSON-artefakt. Syftet är att säkerställa perfekt kontextöverföring, spårbarhet och systematisk självförbättring.
## 2. Process
Vid slutet av en session ska en enda fil med namnet `[SESSIONID].json` genereras. Denna fil måste vara en giltig JSON-fil som följer specifikationen nedan.
## 3. Final Output Specification
Filen ska innehålla ett JSON-objekt med följande struktur. Alla fält är obligatoriska om inte annat anges.
```json
{
  "sessionId": "SESSIONID",
  "createdAt": "YYYY-MM-DDTHH:mm:ssZ",
  "artifacts": {
    "ByggLogg": {
      "sessionId": "SESSIONID",
      "date": "YYYY-MM-DDTHH:mm:ssZ",
      "summary": "Kort sammanfattning av sessionens resultat.",
      "actions": [
        {
          "title": "Kort teknisk titel.",
          "files": [
            {
              "path": "sökväg/till/fil",
              "changeDescription": "Exakt ändring + motiv."
            }
          ],
          "result": "Tekniskt utfall."
        }
      ],
      "projectStatus": "Verifierad status vid sessionens slut."
    },
    "Chatthistorik": {
      "sessionId": "SESSIONID",
      "interactions": [
        {
          "speakerName": "Frankensteen",
          "model": {
            "provider": "OpenAI",
            "name": "gpt-5",
            "version": "2025-08-01"
          },
          "speaker": "Frankensteen (OpenAI:gpt-5@2025-08-01)",
          "summary": "Koncis sammanfattning av inlägget."
        }
      ]
    },
    "ai_protocol_performance": {
      "sessionId": "SESSIONID",
      "date": "YYYY-MM-DDTHH:mm:ssZ",
      "aiQualitativeSummary": "Kort AI-perspektiv.",
      "scorecard": {
        "efficacy": { "score": 0, "weight": 0.4, "weightedScore": 0.0 },
        "efficiency": { "score": 0, "weight": 0.3, "weightedScore": 0.0 },
        "robustness": { "score": 0, "weight": 0.3, "weightedScore": 0.0 },
        "finalScore": 0.0
      },
      "detailedMetrics": {
        "missionCompleted": true,
        "debuggingCycles": 0,
        "selfCorrections": 0,
        "externalCorrections": 0,
        "protocolActivations": { "psv": 0, "helpMeGod": 0, "stalemate": 0 },
        "heuristicsTriggered": []
      },
      "improvementSuggestion": {
        "pattern": "Återkommande mönster.",
        "proposedHeuristicId": "H-YYYYMMDD-seq"
      }
    },
    "frankensteen_learning_db": [
      {
        "heuristicId": "H-YYYYMMDD-seq",
        "trigger": { "type": "...", "scope": ["..."], "keywords": ["..."] },
        "identifiedRisk": { "riskId": "...", "description": "..." },
        "mitigation": { "protocolId": "...", "description": "..." },
        "metadata": { "originSessionId": "SESSIONID", "createdAt": "YYYY-MM-DDTHH:mm:ssZ" }
      }
    ],
    "generated_patches": [
      {
        "protocol_id": "anchor_diff_v2.1",
        "target": {
          "path": "...",
          "base_checksum_sha256": "..."
        },
        "op_groups": [ ... ],
        "meta": { "notes": "..." }
      }
    ]
  }
}
```
## 4. Obligatoriskt Sista Steg: Kontext för Nästa Session
Efter leverans av den konsoliderade artefakten, leverera ett separat och fristående JSON-objekt för att initiera nästa arbetssession, enligt `Kontext-JSON_Protokoll.md`.
```json
{
  "task_summary": "Kort mening om nästa uppdrag.",
  "full_instruction_preview": "Detaljerad, fristående uppdragsbeskrivning.",
  "filesToSelect": ["komplett lista med filer för nästa session"],
  "notes": "Valfria, strategiska anteckningar."
}
```



if __name__ == "__main__":
    main()
