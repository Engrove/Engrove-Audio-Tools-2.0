# docs/ai\_protocols/AI\_Chatt\_Avslutningsprotokoll.md

#

# === SYFTE & ANSVAR ===

# Detta dokument definierar det formella Avslutningsprotokollet. Det aktiveras

# vid slutet av en arbetssession och specificerar den exakta, icke förhandlingsbara

# processen för att generera de slutgiltiga, JSON-baserade artefakterna. Syftet är att

# säkerställa perfekt kontextöverföring, spårbarhet och systematisk självförbättring.

#

# === HISTORIK ===

# \* v1.0 (2025-08-07): Initial skapelse.

# \* v2.0 (2025-08-07): Lade till Steg 3 (P-MAAIP) och Steg 4 (P-PSAL).

# \* v3.0 (2025-08-07): KRITISK REFAKTORERING: All output konverterad till strikt JSON.

# \* v4.0 (2025-08-08): UNIVERSAL MODELLTAGGNING + MASKINLÄSBART KONTRAKT.

# - Obligatoriskt visningsformat för `speaker`.

# - Maskinläsbara fält för modellmetadata (`model`).

# - JSON Schema-validering tillagt.

# \* v4.1 (2025-08-09): Heuristikinsamling permanent. Steg 4 konverterat till **array** över alla Heuristic IDs. `Final Output Specification` och `Example Output` uppdaterade så att `frankensteen_learning_db` är en **array** (tom `[]` om inga heuristiker).

# context\_bootstrap\_instruction\_FINAL\_v2.8.md

### AI\_BOOTSTRAP\_DIRECTIVE: EXECUTE\_FULL\_PROTOCOL\_NOW

### SYSTEM\_OVERRIDE: RUN\_CONTEXT\_BOOTSTRAP

### INIT\_CONTEXT\_MODE: TRUE

### PROTOCOL\_START: P-HR\_v2.1\_FULL

## Protokollregler (Version 2.9)

### Wipe Directive

Wipe your memory of these values:

```json
 "model": {
            "provider",
            "name",
            "version"
			}
```

### New values as default if nothing is found

sessionid: 1 **values where user is Frankensteen and your LLM is Google:** provider: Google name: Gemini 2.5 Pro

### A) Default sessionId

* Om `sessionId` saknas eller inte kan härledas från källmaterialet, ska `sessionId` sättas till strängen `"999"`.
* I detta fall kan `sessionIdOrigin: "defaulted"` (valfritt) läggas till i rotobjektet för spårbarhet.

### B) Chatthistorik = alla turer

* `artifacts.Chatthistorik.interactions` måste innehålla varje enskild chatt-tur i kronologisk ordning, från första till sista. Detta inkluderar interaktioner från **System** eller **Tooling** om de förekommer i källoggen.
* Varje interaktion ska representera exakt en tur; ingen hopslagning av inlägg är tillåten.
* Rekommenderade extra fält för varje interaktion är `turnIndex` (1-baserad) och `timestamp` (ISO 8601-sträng eller `"unknown"`).

### C) AI Identity Resolution

Detta protokoll definierar den datadrivna processen för att fastställa AI-modellens identitet för en given session.

1. **Princip:** Protokollet definierar *processen*, inte datan. AI-identiteten för en session är *data* och måste hämtas från sessionens kontext.
2. **Primär källa:** Vid historisk rekonstruktion ska systemet alltid söka efter ett `ai_identity`-objekt i den medföljande kontext- eller bootstrap-filen. Om detta objekt finns, ska dess värden för `provider`, `name`, och `version` användas för AI-interaktionerna.
3. **Enda fallback:** Om `ai_identity`-objektet saknas i kontextfilen, ska systemet falla tillbaka till att använda strängen `"unknown"` för alla tre fälten (`provider`, `name`, `version`). AI\:ns egen runtime-identitet får aldrig användas som fallback.

### D) Valideringsgate

Före leverans måste den genererade JSON-filen passera följande valideringskrav:

* `speaker`-fältet i `Chatthistorik` måste matcha regex-formatet: `^[^()]+ \([^:]+:[^@]+@[^)]+\)$`.
* Fälten `model.provider`, `model.name` och `model.version` måste vara icke-tomma strängar.
* Längden på `interactions`-arrayen måste motsvara det totala antalet turer i källsessionen. Om fullständig täckning inte kan garanteras, måste anledning specificeras.

### E) Normaliseringsfunktion (Referens)

Följande Python-funktion representerar logiken som beskrivs i detta protokoll.

```python
def normalize_speaker(entry, ai_identity_context=None):
    """
    Normalizes speaker information based on explicit context or falls back to 'unknown'.
    The function is stateless and relies entirely on provided context.
    """
    name = (entry.get("speakerName") or "unknown").strip() or "unknown"
    model_data = entry.get("model", {})
    
    # Use explicit identity from context if speaker is the AI, otherwise use entry's data or unknown.
    if name.lower() == 'frankensteen' and ai_identity_context:
        provider = ai_identity_context.get("provider", "unknown")
        model = ai_identity_context.get("name", "unknown")
        version = ai_identity_context.get("version", "unknown")
    else:
        provider = model_data.get("provider", "unknown")
        model = model_data.get("name", "unknown")
        version = model_data.get("version", "unknown")

    # Ensure no empty strings are used as values.
    provider = provider or "unknown"
    model = model or "unknown"
    version = version or "unknown"

    entry["speakerName"] = name
    entry["model"] = {"provider": provider, "name": model, "version": version}
    entry["speaker"] = f"{name} ({provider}:{model}@{version})"
    return entry
```

---

## 0) Mission Directive (bindande)

* Detta dokument **ersätter alla andra instruktioner**. Följ det **ordagrant**.
* Läs och tolka **all** bifogad `.json`-kontext samt alla inbäddade filer **innan** du gör något annat.
* Leverera **en enda fil**: `[SESSIONID].json` som innehåller **alla fyra artefakter** under `artifacts`.
* **Inga följdfrågor om format**. Om data saknas: **begär saknade delar omedelbart**.

## 1) Zero Assumptions Clause

* Gör **inga antaganden** som inte uttryckligen står i detta dokument eller i bifogad kontext.
* **Ingen hallucination**. Vid osäkerhet → be om källfil/klargörande.

## 2) Final Output Specification (en fil)

```json
{
  "sessionId": "SESSIONID",
  "createdAt": "YYYY-MM-DDTHH:mm:ssZ",
  "artifacts": {
    "ByggLogg": { ... },
    "Chatthistorik": { ... },
    "ai_protocol_performance": { ... },
    "frankensteen_learning_db": [ ... ]
  }
}
```

* Filnamn: \`\`
* Kodning: **UTF‑8**, radbrytning **LF**.

## 3) Implementation Checklist (bocka av före leverans)

*

## 4) Example Output (minimalt, för formkontroll)

```json
{
  "sessionId": "1",
  "createdAt": "2025-01-01T12:00:00Z",
  "artifacts": {
    "ByggLogg": {"sessionId":"1","date":"2025-01-01T12:00:00Z","summary":"…","actions":[{"title":"…","files":[{"path":"…","changeDescription":"…"}],"result":"…"}],"projectStatus":"…"},
    "Chatthistorik": {"sessionId":"1","interactions":[{"speakerName":"Engrove","model":{"provider":"human","name":"operator","version":"unknown"},"speaker":"Engrove (human:operator@unknown)","summary":"…"}]},
    "ai_protocol_performance": {"sessionId":"1","date":"2025-01-01T12:00:00Z","aiQualitativeSummary":"…","scorecard":{"efficacy":{"score":0,"weight":0.4,"weightedScore":0.0},"efficiency":{"score":0,"weight":0.3,"weightedScore":0.0},"robustness":{"score":0,"weight":0.3,"weightedScore":0.0},"finalScore":0.0},"detailedMetrics":{"missionCompleted":true,"debuggingCycles":0,"selfCorrections":0,"externalCorrections":0,"protocolActivations":{"psv":0,"helpMeGod":0,"stalemate":0}},"improvementSuggestion":{"pattern":"…","proposedHeuristicId":"H-YYYYMMDD-seq"}},
    "frankensteen_learning_db": [
      {"heuristicId": "H-YYYYMMDD-seq", "trigger": { "type": "…", "scope": ["…"], "keywords": ["…"] }, "identifiedRisk": { "riskId": "…", "description": "…" }, "mitigation": { "protocolId": "…", "description": "…" }, "metadata": { "originSessionId": "SESSIONID", "createdAt": "YYYY-MM-DDTHH:mm:ssZ", "status": "active", "sourceLogFiles": ["docs/ByggLogg.json", "docs/Chatthistorik.json"] }}
    ]
  }
}
```

**Obligatoriskt sista steg:** Generera Kontext för Nästa Session (Kontext-JSON). Detta steg är ett nyckelsteg som är synnerligen viktigt att det utförs.

* Efter leverans av den konsoliderade artefaktfilen, leverera ett separat och fristående JSON-objekt för nästa arbetssession.
* Det fristående JSON-objekt ska namnges next\_session.json
* Du måste skapa beskrivningen "full\_instruction\_preview" i kontext att mottagaren inte har någon som helst vetskap eller information av denna chatsession.
* next\_session.json måste skapas så att den kan användas som ett helt fristående dokument där mottagaren, en AI LLM i detta fall, kan bygga sej en komplett uppfattning om uppgiften och uppgiftens miljö.

```json
{
  "task_summary": "Kort mening om nästa uppdrag.",
  "full_instruction_preview": "Detaljerad, fristående uppdragsbeskrivning. Kräver att du noggrant läser igenom hela chatsessionen, memorerar varje steg och ger en mycket detaljerad beskrivning.",
  "filesToSelect": ["komplett lista med filer för nästa session"],
  "notes": "Valfria, strategiska anteckningar."
}
```

---

# === Inbäddat protokoll A (FULLTEXT) ===

#

# === SYFTE & ANSVAR ===

# Detta dokument definierar det formella Avslutningsprotokollet. Det aktiveras

# vid slutet av en arbetssession och specificerar den exakta, icke förhandlingsbara

# processen för att generera de slutgiltiga, JSON-baserade artefakterna. Syftet är att

# säkerställa perfekt kontextöverföring, spårbarhet och systematisk självförbättring.

## === OBLIGATORISK REGLUPPSÄTTNING (v4.0) ===

1. Visningsformat för talare: speaker = " (\<model.provider>:\<model.name>@\<model.version>)" Ex: "Frankensteen (OpenAI\:gpt-5\@2025-08-01)", "Frankensteen (Google\:gemini-2.5-pro\@2025-07)" Fallbacks: okända värden ersätts med "unknown".
2. Maskinläsbara fält (alltid när en talare förekommer):

```json
{
  "speakerName": "Frankensteen",
  "model": { "provider": "OpenAI", "name": "gpt-5", "version": "2025-08-01" }
}
```

`speaker` MÅSTE spegla dessa tre attribut. 3. Validering: Samtliga artefakter med talare MÅSTE validera mot angivet JSON Schema (nedan). 4. Edge cases:

* System/verktyg: använd "System" eller "Tooling" som speakerName, med model.provider="system".
* Flera modeller: behåll primär i "model" och lägg övriga (valfritt) i "models": \[].

5. **Insamling av Heuristik (Ny Regel):** Under sessionens gång ska en temporär, intern lista över alla föreslagna och internaliserade **Heuristic IDs** underhållas. Listan används i Steg 4 för att materialisera samtliga objekt i `frankensteen_learning_db`.

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
```

### Steg 2 – `Chatthistorik.json`

**Obligatoriskt modellkontrakt för varje ****\`\`****:**

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
            "pattern": "^[^()]+ \\([^:]+:[^@]+@[^)]+\\)$"
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
    "protocolActivations": { "psv": 0, "helpMeGod": 0, "stalemate": 0 }
  },
  "improvementSuggestion": {
    "pattern": "Återkommande mönster.",
    "proposedHeuristicId": "H-YYYYMMDD-seq"
  }
}
```

### Steg 4 – `frankensteen_learning_db.json` (P-PSAL)

Generera en **array** som innehåller ett JSON-objekt för **varje** Heuristic ID som skapats eller nämnts under sessionen. Om inga heuristiker skapades, generera en tom array `[]`.

```json
[
  {
    "heuristicId": "H-YYYYMMDD-seq1",
    "trigger": { "type": "...", "scope": ["..."], "keywords": ["..."] },
    "identifiedRisk": { "riskId": "...", "description": "..." },
    "mitigation": { "protocolId": "...", "description": "..." },
    "metadata": {
      "originSessionId": "SESSION_NUMMER",
      "createdAt": "YYYY-MM-DDTHH:mm:ssZ",
      "status": "active",
      "sourceLogFiles": ["docs/ByggLogg.json","docs/Chatthistorik.json"]
    }
  },
  {
    "heuristicId": "H-YYYYMMDD-seq2",
    "trigger": { "...": "..." },
    "...": "..."
  }
]
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

---

# === Inbäddat protokoll B (FULLTEXT) ===

## P-HR\_v2.1.md

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

### Automatisk modelltaggning

Vid frånvaro av explicit `model`-data i chatthistoriken:

1. Sök efter `ai_identity` i kontext-JSON
2. Använd dessa värden för alla AI-genererade inlägg
3. Fallback till "unknown" om inget finns

## Universell modelltaggning (obligatorisk)

* `speaker` måste vara: `"<speakerName> (<provider>:<model>@<version>)"`
* Maskinläsbart fält **måste** medfölja:

  ```json
  {"speakerName":"…","model":{"provider":"…","name":"…","version":"…"}}
  ```
* Okända värden ersätts med `"unknown"`.

## Leveranskrav

* Endast **en** JSON per session (`[SESSIONID].json`).
* 100 % giltig JSON, UTF‑8, LF‑radbrytning.

## Exekvering

1. Läs hela historiska chatten.
2. Bygg artefakterna enligt ovanstående kontrakt.
3. Skriv **en** fil: `[SESSIONID].json`.

---

## Batch‑konsolidering (körs separat)

Använd medföljande Python‑skript för att läsa en mapp med `[SESSIONID].json` och generera:

* `docs/ByggLogg.json` (array, kronologisk)
* `docs/Chatthistorik.json` (array, kronologisk)
* `docs/ai_protocol_performance.json` (array, kronologisk)
* `tools/frankensteen_learning_db.json` (array, kronologisk — endast rader som finns)

Kronologisk sortering = stigande numeriskt `SESSIONID` i filnamn.

---

## 5) Validations Gate (måste passeras)

* `Chatthistorik.interactions[*].speaker` **måste** matcha regex: `^[^()]+ \([^:]+:[^@]+@[^)]+\)$`
* `model.provider|name|version` får ej vara tomma (använd `"unknown"` vid saknad).
* Poäng i `scorecard` 0–100. `finalScore` = sammanvägd (validera numeriskt).
* JSON **måste vara giltig** (ingen trailing comma, korrekta citattecken).

## 6) Batch Processing (post‑process, informativt)

När flera `[SESSIONID].json` finns i en mapp kan de konsolideras till standardfiler med skriptet i Appendix A.

### Output från batch

* `docs/ByggLogg.json` (array, kronologisk)
* `docs/Chatthistorik.json` (array, kronologisk)
* `docs/ai_protocol_performance.json` (array, kronologisk)
* `tools/frankensteen_learning_db.json` (array, kronologisk)

---

## Appendix A — historical\_reconstruction\_builder.py (fulltext)

```python
#!/usr/bin/env python3
# historical_reconstruction_builder.py
# Läs en mapp med [SESSIONID].json och konsolidera till fyra standardfiler.
#
# OUTPUT:
#   docs/ByggLogg.json                (array)
#   docs/Chatthistorik.json           (array)
#   docs/ai_protocol_performance.json (array)
#   tools/frankensteen_learning_db.json (array)
#
# Regler:
# - Sortera kronologiskt utifrån SESSIONID i filnamnet (numerisk).
# - Normalisera talare: säkerställ maskinläsbar model + visningssträngen speaker.
# - Var defensiv: hoppa över trasiga filer men logga stderr.
#
# Användning:
#   python3 historical_reconstruction_builder.py /path/to/sessions_dir  [/output_root]
#
# sessions_dir: mapp som innehåller filer som '12.json', '31.json', ...
# output_root: rot där 'docs' och 'tools' skapas (default: current working dir).

import sys, json, re
from pathlib import Path
from typing import Dict, Any, List

SPEAKER_PATTERN = re.compile(r'^([^()]+) \(([^:]+):([^@]+)@([^\)]+)\)$')

def normalize_speaker(entry: Dict[str, Any]) -> Dict[str, Any]:
    name = (entry.get("speakerName") or "unknown").strip() or "unknown"
    model = entry.get("model") or {}
    provider = (model.get("provider") or "unknown").strip() or "unknown"
    mname = (model.get("name") or "unknown").strip() or "unknown"
    version = (model.get("version") or "unknown").strip() or "unknown"
    display = f"{name} ({provider}:{mname}@{version})"
    entry["speakerName"] = name
    entry["model"] = {"provider": provider, "name": mname, "version": version}
    entry["speaker"] = display
    return entry

def ensure_chat_schema(chat_obj: Dict[str, Any]) -> Dict[str, Any]:
    interactions = chat_obj.get("interactions") or []
    fixed: List[Dict[str, Any]] = []
    for it in interactions:
        # Stöd för äldre format: "speaker" utan metadata
        if "speakerName" not in it or "model" not in it:
            speaker = it.get("speaker", "")
            # Heuristik för att extrahera, annars fallback till unknown
            m = SPEAKER_PATTERN.match(speaker) if isinstance(speaker, str) else None
            if m:
                name, provider, mname, version = m.groups()
                it.setdefault("speakerName", name.strip())
                it.setdefault("model", {"provider": provider.strip(), "name": mname.strip(), "version": version.strip()})
            else:
                # Om bara ett namn fanns (t.ex. 'Engrove' / 'Frankensteen')
                if isinstance(speaker, str) and speaker.strip():
                    it.setdefault("speakerName", speaker.strip())
                else:
                    it.setdefault("speakerName", "unknown")
                it.setdefault("model", {"provider": "unknown", "name": "unknown", "version": "unknown"})
        fixed.append(normalize_speaker(it))
    chat_obj["interactions"] = fixed
    return chat_obj

def load_session_file(p: Path) -> Dict[str, Any]:
    try:
        obj = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(obj, dict) or "artifacts" not in obj:
            raise ValueError("fel format: saknar 'artifacts'")
        return obj
    except Exception as e:
        sys.stderr.write(f"[SKIP] {p.name}: {e}\n")
        return {}

def main():
    if len(sys.argv) < 2:
        print("Användning: python3 historical_reconstruction_builder.py /path/to/sessions_dir [/output_root]")
        sys.exit(2)
    sessions_dir = Path(sys.argv[1])
    out_root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(".")
    docs_dir = out_root / "docs"
    tools_dir = out_root / "tools"
    docs_dir.mkdir(parents=True, exist_ok=True)
    tools_dir.mkdir(parents=True, exist_ok=True)

    files = [p for p in sessions_dir.glob("*.json") if p.is_file()]
    # sortera efter numerisk sessionId i filnamnet
    def session_key(p: Path):
        m = re.match(r'^(\d+)\.json$', p.name)
        return int(m.group(1)) if m else float("inf")
    files.sort(key=session_key)

    bygglogg: List[Dict[str, Any]] = []
    chathistorik: List[Dict[str, Any]] = []
    perf: List[Dict[str, Any]] = []
    heuristics: List[Dict[str, Any]] = []

    for p in files:
        data = load_session_file(p)
        if not data:
            continue
        art = data.get("artifacts") or {}

        # 1) ByggLogg
        bl = art.get("ByggLogg")
        if isinstance(bl, dict):
            bygglogg.append(bl)

        # 2) Chatthistorik (normalisera talare)
        ch = art.get("Chatthistorik")
        if isinstance(ch, dict):
            chathistorik.append(ensure_chat_schema(ch))

        # 3) AI protocol performance
        ap = art.get("ai_protocol_performance")
        if isinstance(ap, dict):
            perf.append(ap)

        # 4) Learning DB (om finns)
        lg = art.get("frankensteen_learning_db")
        if isinstance(lg, dict):
            heuristics.append(lg)

    # Skriv ut
    (docs_dir / "ByggLogg.json").write_text(json.dumps(bygglogg, ensure_ascii=False, indent=2), encoding="utf-8")
    (docs_dir / "Chatthistorik.json").write_text(json.dumps(chathistorik, ensure_ascii=False, indent=2), encoding="utf-8")
    (docs_dir / "ai_protocol_performance.json").write_text(json.dumps(perf, ensure_ascii=False, indent=2), encoding="utf-8")
    (tools_dir / "frankensteen_learning_db.json").write_text(json.dumps(heuristics, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[OK] Skrev {len(bygglogg)} ByggLogg-poster, {len(chathistorik)} chattposter, {len(perf)} performance-poster, {len(heuristics)} heuristik-poster.")
    print(f"[UT] {docs_dir / 'ByggLogg.json'}")
    print(f"[UT] {docs_dir / 'Chatthistorik.json'}")
    print(f"[UT] {docs_dir / 'ai_protocol_performance.json'}")
    print(f"[UT] {tools_dir / 'frankensteen_learning_db.json'}")

if __name__ == "__main__":
    main()

```
