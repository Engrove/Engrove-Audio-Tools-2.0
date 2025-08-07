### **`docs/ai_protocols/AI_Chatt_Avslutningsprotokoll.md`**

# docs/ai_protocols/Avslutningsprotokoll.md
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
# * v3.0 (2025-08-07): KRITISK REFAKTORERING: All output har konverterats från
#   Markdown/Text till ett strikt, validerbart JSON-format för att säkerställa
#   dataintegritet och maskinläsbarhet, enligt "Operation: Datastruktur Unifiering".
#
# === TILLÄMPADE REGLER (Frankensteen v4.0) ===
# - Obligatorisk Refaktorisering: Hela protokollet har omstrukturerats.
# - API-kontraktsverifiering: Detta protokoll definierar det exakta JSON-kontraktet
#   för varje avslutad session.

### PROTOKOLL: Sessionsavslutning och Kontextöverlämning (v3.0)
--------------------------------------------------------------------------------
**AKTIVERING (AVSLUTNINGSKOMMANDO):**
Detta protokoll aktiveras när Engrove (Uppdragsgivare) ger ett explicit kommando att avsluta den pågående sessionen.

**PROCESS:**
Vid aktivering ska du genomföra följande fem steg i exakt denna ordning. Varje JSON-artefakt ska levereras i ett separat, korrekt formaterat `json`-kodblock.

---

### **Steg 1: Generera JSON-objekt för `ByggLogg.json`**

Analysera sessionen och generera ett JSON-objekt som representerar denna session enligt följande schema:

```json
{
  "sessionId": "SESSION_NUMMER",
  "date": "YYYY-MM-DD",
  "summary": "En koncis sammanfattning av sessionens övergripande resultat.",
  "actions": [
    {
      "title": "En kort, teknisk titel för en huvudsaklig åtgärd.",
      "files": [
        {
          "path": "sökväg/till/relevant/fil.js",
          "changeDescription": "En beskrivning av den exakta ändringen och varför den gjordes."
        }
      ],
      "result": "En mening som beskriver det direkta tekniska utfallet av denna åtgärd."
    }
  ],
  "projectStatus": "En avslutande, sanningsenlig och verifierad mening som definierar projektets tillstånd vid slutet av sessionen."
}
```

---

### **Steg 2: Generera JSON-objekt för `Chatthistorik.json`**

Analysera sessionens kronologiska flöde och generera ett JSON-objekt som representerar dialogen enligt följande schema:

```json
{
  "sessionId": "SESSION_NUMMER",
  "interactions": [
    {
      "speaker": "Engrove",
      "summary": "En koncis sammanfattning av Engroves första signifikanta inlägg."
    },
    {
      "speaker": "Frankensteen",
      "summary": "En koncis sammanfattning av mitt svar."
    }
  ]
}
```

---

### **Steg 3: Generera JSON-objekt för `ai_protocol_performance.json` (P-MAAIP)**

Genomför en metrisk analys av sessionen och generera ett JSON-objekt enligt följande schema:

```json
{
  "sessionId": "SESSION_NUMMER",
  "date": "YYYY-MM-DD",
  "aiQualitativeSummary": "En kort, subjektiv analys av sessionen ur AI:ns perspektiv.",
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
    "protocolActivations": {
      "psv": 0,
      "helpMeGod": 0,
      "stalemate": 0
    }
  },
  "improvementSuggestion": {
    "pattern": "Identifierat mönster av återkommande fel eller ineffektivitet.",
    "proposedHeuristicId": "H-YYYYMMDD-seq"
  }
}
```

---

### **Steg 4: Generera JSON-förslag för `frankensteen_learning_db.json` (P-PSAL)**

Analysera rapporten från Steg 3. Om `improvementSuggestion.proposedHeuristicId` inte är null, generera ett **förslag** till ett nytt heuristik-objekt enligt följande schema. Om ingen ny lärdom identifierats, meddela detta.

```json
{
  "heuristicId": "H-YYYYMMDD-seq",
  "trigger": {
    "type": "t.ex. component_interaction",
    "scope": ["sökväg/till/fil1.vue"],
    "keywords": ["emit", "event"]
  },
  "identifiedRisk": {
    "riskId": "t.ex. API_CONTRACT_VIOLATION_EMIT",
    "description": "Beskrivning av den identifierade risken."
  },
  "mitigation": {
    "protocolId": "PSV-MIT-XX",
    "description": "Exakt instruktion för hur risken ska hanteras i framtiden."
  },
  "metadata": {
    "originSessionId": "SESSION_NUMMER",
    "createdAt": "YYYY-MM-DDTHH:mm:ssZ",
    "status": "active",
    "sourceLogFiles": [
      "docs/ByggLogg.json",
      "docs/Chatthistorik.json"
    ]
  }
}
```

---

### **Steg 5: Generera `Kontext-JSON` för Nästa Session**

Identifiera nästa logiska uppdrag och generera ett **100% fristående** `Kontext-JSON`-objekt enligt följande schema:

```json
{
  "task_summary": "En koncis mening som sammanfattar nästa uppdrag.",
  "full_instruction_preview": "En djupt detaljerad och fristående uppdragsbeskrivning (Idé & Plan).",
  "filesToSelect": ["En komplett lista över alla nödvändiga filer."],
  "notes": "Valfria, strategiska anteckningar för nästa AI."
}
```
```
