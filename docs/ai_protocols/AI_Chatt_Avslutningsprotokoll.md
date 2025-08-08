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
#   - Obligatoriskt visningsformat för `speaker`.
#   - Maskinläsbara fält för modellmetadata (`model`).
#   - JSON Schema-validering tillagt.

 ## === OBLIGATORISK REGLUPPSÄTTNING (v4.0) === 
 1) Visningsformat för talare:
    speaker = "<speakerName> (<model.provider>:<model.name>@<model.version>)"
    Ex: "Frankensteen (OpenAI:gpt-5@2025-08-01)", "Frankensteen (Google:gemini-2.5-pro@2025-07)"
    Fallbacks: okända värden ersätts med "unknown".
 2) Maskinläsbara fält (alltid när en talare förekommer):
```json
    {
      "speakerName": "Frankensteen",
      "model": { "provider": "OpenAI", "name": "gpt-5", "version": "2025-08-01" }
    }
````
    `speaker` MÅSTE spegla dessa tre attribut.
 3) Validering:
    Samtliga artefakter med talare MÅSTE validera mot angivet JSON Schema (nedan).
 4) Edge cases:
    - System/verktyg: använd "System" eller "Tooling" som speakerName, med model.provider="system".
    - Flera modeller: behåll primär i "model" och lägg övriga (valfritt) i "models": [].

## PROTOKOLL: Sessionsavslutning och kontextöverlämning (v4.0)

**AKTIVERING:** När uppdragsgivaren explicit begär avslutning.
**PROCESS:** Kör följande fem steg i exakt ordning. Varje artefakt levereras som ett separat, giltigt `json`-objekt.

### Steg 1 – `ByggLogg.json`
Schema (exempelstruktur, utökad med modellkontrakt där talare används):
```json
{
  "sessionId": "SESSION_NUMMER",

  "date": "YYYY-MM-DDTHH:mm:ssZ",

  "summary": "Kort sammanfattning av sessionens resultat.",

  "actions": [

    {

      "title": "Kort teknisk titel.",

      "files": [

        { "path": "sökväg/till/fil", "changeDescription": "Exakt ändring + motiv." }

      ],

      "result": "Tekniskt utfall."

    }

  ],

  "projectStatus": "Verifierad status vid sessionens slut."

}

````



### Steg 2 – `Chatthistorik.json`



**Obligatoriskt modellkontrakt för varje `speaker`:**



```json

{

  "sessionId": "SESSION_NUMMER",

  "interactions": [

    {

      "speakerName": "Frankensteen",

      "model": { "provider": "OpenAI", "name": "gpt-5", "version": "2025-08-01" },

      "speaker": "Frankensteen (OpenAI:gpt-5@2025-08-01)",

      "summary": "Koncis sammanfattning av inlägget."

    }

  ]

}

```



**JSON Schema-krav för talare i Chatthistorik:**



```json

{

  "type": "object",

  "required": ["sessionId", "interactions"],

  "properties": {

    "sessionId": { "type": "string", "minLength": 1 },

    "interactions": {

      "type": "array",

      "items": {

        "type": "object",

        "required": ["speakerName", "model", "speaker", "summary"],

        "properties": {

          "speakerName": { "type": "string", "minLength": 1 },

          "model": {

            "type": "object",

            "required": ["provider", "name", "version"],

            "properties": {

              "provider": { "type": "string", "minLength": 1 },

              "name": { "type": "string", "minLength": 1 },

              "version": { "type": "string", "minLength": 1 }

            }

          },

          "speaker": {

            "type": "string",

            "pattern": "^[^()]+ \([^:]+:[^@]+@[^)]+\)$"

          },

          "summary": { "type": "string", "minLength": 1 }

        }

      }

    }

  }

}

```



### Steg 3 – `ai_protocol_performance.json` (P-MAAIP)



Bevara modellkontrakt där talare förekommer (t.ex. om kommentarer eller utsagor loggas):



```json

{

  "sessionId": "SESSION_NUMMER",

  "generatedBy": {

    "speakerName": "Frankensteen",

    "model": {

      "provider": "Google",

      "name": "gemini-2.5-pro",

      "version": "2025-08-08"

    },

    "speaker": "Frankensteen (Google:gemini-2.5-pro@2025-08-08)"

  },

  "date": "YYYY-MM-DDTHH:mm:ssZ",

  "aiQualitativeSummary": "Kort AI-perspektiv.",

  "scorecard": {

    "efficacy": {

      "score": 0,

      "weight": 0.4,

      "weightedScore": 0.0

    },

    "efficiency": {

      "score": 0,

      "weight": 0.3,

      "weightedScore": 0.0

    },

    "robustness": {

      "score": 0,

      "weight": 0.3,

      "weightedScore": 0.0

    },

    "finalScore": 0.0

  },

  "detailedMetrics": {

    "missionCompleted": true,

    "debuggingCycles": 0,

    "selfCorrections": 0,

    "externalCorrections": 0,

    "protocolActivations": {

      "psv": 0,

      "helpMeGod": 0,

      "stalemate": 0

    }

  },

  "improvementSuggestion": {

    "pattern": "Återkommande mönster.",

    "proposedHeuristicId": "H-YYYYMMDD-seq"

  }

}

```



### Steg 4 – Förslag till `frankensteen_learning_db.json` (P-PSAL)



Generera förslag endast om `proposedHeuristicId` finns:



```json

{

  "heuristicId": "H-YYYYMMDD-seq",

  "trigger": { "type": "t.ex. component_interaction", "scope": ["sökväg/till/fil.vue"], "keywords": ["emit","event"] },

  "identifiedRisk": { "riskId": "API_CONTRACT_VIOLATION_EMIT", "description": "Beskrivning av risk." },

  "mitigation": { "protocolId": "PSV-MIT-XX", "description": "Exakt åtgärd." },

  "metadata": {

    "originSessionId": "SESSION_NUMMER",

    "createdAt": "YYYY-MM-DDTHH:mm:ssZ",

    "status": "active",

    "sourceLogFiles": ["docs/ByggLogg.json","docs/Chatthistorik.json"]

  }

}

```



### Steg 5 – `Kontext-JSON` för nästa session



Oförändrat krav, fristående objekt:



```json

{

  "task_summary": "Kort mening om nästa uppdrag.",

  "full_instruction_preview": "Detaljerad, fristående uppdragsbeskrivning.",

  "filesToSelect": ["komplett lista med filer"],

  "notes": "Valfria, strategiska anteckningar."

}

```



---



## Normaliseringsfunktion (normativt exempel)



```python

def normalize_speaker(speaker_name, provider=None, model=None, version=None):

    provider = provider or "unknown"

    model = model or "unknown"

    version = version or "unknown"

    display = f'{speaker_name} ({provider}:{model}@{version})'

    return {

        "speakerName": speaker_name,

        "model": {"provider": provider, "name": model, "version": version},

        "speaker": display

    }

```



## Valideringskrav (gate)



* Alla artefakter som innehåller `speaker` MÅSTE först passera JSON Schema-validering (ovanför).

* Vid valideringsfel: skriv inte fil; logga fel och begär korrigeringar.
