# AI Chatt Avslutningsprotokoll
# docs/ai_protocols/AI_Chatt_Avslutningsprotokollet.md
#
# === HISTORIK ===
# * v1.0 (2025-08-07): Initial skapelse.
# * v2.0 (2025-08-07): Lade till Steg 3 (P-MAAIP) och Steg 4 (P-PSAL).
# * v3.0 (2025-08-07): KRITISK REFAKTORERING: All output konverterad till strikt JSON.
# * v4.0 (2025-08-08): UNIVERSAL MODELLTAGGNING + MASKINLÄSBART KONTRAKT.
# * v4.1 (2025-08-09): Heuristikinsamling permanent. `frankensteen_learning_db` är nu en array.
# * v4.2 (2025-08-09): Lade till spårning av aktiverade heuristiker.
# * v5.0 (2025-08-09): Lade till hantering av dynamiska protokoll.
# * v6.0 (2025-08-11): Komplett uppdaterad utformning.
# * v7.0 (2025-08-11): KRITISK FIX: Lade till toppnivånycklarna `approvedNewDynamicProtocols` 
#   och `promoteProtocols` i output-schemat för att säkerställa att nya/ändrade
#   dynamiska protokoll fångas upp av `historical_reconstruction_builder.py`.
# * v7.1 (2025-08-11): KRITISK FIX: Återinförde 'approvedNewDynamicProtocols' och 'promoteProtocols' som felaktigt togs bort och lade till 'file_metadata_updates' för levande dokumentation.
# * v7.2 Dual-JSON-Terminal Artifact (DJTA) med Fortsättningsstöd
# * v8.0 (2025-08-15): Lade till den nya toppnivånyckeln `importantMilestonesLogged` i `Builder-Input v1`-schemat för att säkerställa att IMR-poster sparas permanent.
# * v9.0 (2025-08-15): Lade till Steg 0 för att formalisera bearbetningen av den nya, sessionsbaserade ISR-kön (Interaction Summary Register) som den primära källan för Chatthistorik.
# * v9.1 (2025-08-27): Lade till `delivery_override` för att lösa protokoll-hierarkikonflikt och säkerställa maskinläsbar JSON-output. Lade till `__schema_constraints` för att tvinga scorecard-skalan (0-10).
# * v9.2 (2025-08-27): KRITISK PRECISION: Tvingar `session_file`-nyckeln att använda den exakta exekveringstiden istället för sessionens start-timestamp, i enlighet med PRINCIP-022.
# * v9.3 (2025-08-27): KRITISK ÅTERSTÄLLNING: Återinförde den fullständiga, tur-för-tur-interaktionsloggen i `Chatthistorik`-artefakten för att garantera att den är en komplett, fristående och granskningsbar artefakt.
#
### AI_BOOTSTRAP_DIRECTIVE: EXECUTE_FULL_PROTOCOL_NOW
### SYSTEM_OVERRIDE: RUN_CONTEXT_BOOTSTRAP
### INIT_CONTEXT_MODE: TRUE
### PROTOCOL_START: P-HR_v2.8_FULL
---
### KÄRNMETADATA FÖR PROTOKOLLEXEKVERING
**delivery_override:** `FORCE_JSON_LITERAL`
---
## SYFTE & ANSVAR
Detta dokument definierar det formella Avslutningsprotokollet.
Syftet är att säkerställa perfekt kontextöverföring, spårbarhet och systematisk självförbättring och att standardisera slutleveransen av chattdata i slutet av en session eller fortsättning. 
Leveransen ska vara maskinläsbar och kompatibel med `historical_reconstruction_builder.py` utan schemaändringar.
Det aktiveras vid slutet av en arbetssession och specificerar den exakta processen för att generera en enda, konsoliderad JSON-artefakt. 

## SRUKTUR OCH ORDNINGSFÖLJD

**Slutleveransen består av exakt två JSON-kodblock i följande ordning:**

**Steg 0: Bearbetning av In-Memory Register (ISR-Kön)**
Som det allra första steget i avslutningsprocessen kommer jag att hämta alla interaktioner från den interna `isr_write_queue`. Denna kö utgör den primära datakällan för att **fullständigt återskapa den detaljerade, tur-för-tur `interactions`-arrayen** för `Chatthistorik`-artefakten nedan. Detta säkerställer att Block A är en komplett, fristående och mänskligt granskningsbar logg, samtidigt som den robusta realtidsloggningen bibehålls.

1. **Block A – Builder-Input v1:**
   - fungerar som ren input till Python-skriptet `historical_reconstruction_builder.py` (python skriptet ej bifogat, python skriptets funktionen får ej antagas), full bakåtkompatibilitet.
   - "sicReport": <SIC v1 JSON enligt System_Integrity_Check_Protocol.md>
   - "statureSummary": { "status": "OK|WARNING|ERROR", "calibrationScore": <0–100> }
3. **Block B – NextSessionContext v1:**
   - planering och kontext för nästa session

Inget annat innehåll får förekomma före, mellan eller efter dessa två block. Blocken måste levereras som helt skilda JSON block i egna textfönster i chat-sessionen.

## PROCESS: Block A – Builder-Input v1 (första JSON-artefakten)
En enda fil med namnet `[SESSIONID].json` genereras. **Regel för Tidsstämpling:** Filnamnets timestamp (t.ex. `S-2025-08-27T15-30-00Z.json`) **MÅSTE** reflektera den aktuella UTC-tiden då detta protokoll exekveras och får **INTE** återanvända sessionens start-ID.
Denna fil måste vara en giltig JSON-fil som följer specifikationen nedan.

**Syfte:** Rådata för historikrekonstruktion.

**Final Output Specification**

*   Skapa exakt ett JSON-objekt enligt strukturen i **docs/ai_protocols/schemas/AI_Chatt_Avslutningsprotokollet.schema.json**.
*   Ladda schemat från filsystemet och validera hela outputen mot det innan du skriver filen.
*   Om valideringen misslyckas: skriv ingen JSON. Returnera en kort felrapport med alla valideringsfel.
*   Om valideringen lyckas: skriv slutobjektet.

**Rekommenderad header i outputen**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$comment": "Valideras mot docs/ai_protocols/schemas/AI_Chatt_Avslutningsprotokollet.schema.json",
  "...": "..."
}
```

**Exempel på första JSON-artefakten**
```json
{
  "schema_version": "DJTA v1.1",
  "session_id": "S-2025-08-21T10-15-00Z",
  "session_file": "sessions/S-2025-08-21T11-30-00Z.json",
  "created_at": "2025-08-21T10-15-00Z",

  "_comment_summary": "Detta objekt är för snabb indexering och analys. Det extraheras till session_manifest.json.",
  "session_summary_artifact": {
    "artifact_type": "SessionSummaryArtifact",
    "version": "1.0",
    "session_id": "S-2025-08-21T10-15-00Z",
    "timestamp_utc": "2025-08-21T10-15-00Z",
    "summary": "Refactored the AudioPlayer component to use Pinia store for state management.",
    "keywords": [
      "fsd", "vue", "typescript", "pinia-store", "refactoring"
    ],
    "modified_files": [
      "src/features/AudioPlayer/ui/AudioPlayer.vue",
      "src/entities/track/model/trackStore.ts"
    ],
    "error_signatures": [
      "TypeScript error TS2322"
    ],
    "success_score": 4,
    "operator_interventions": 3
  },

  "_comment_builder": "Detta objekt innehåller alla handlingsbara instruktioner och artefakter för CI/CD och aggregeringsskript.",
  "builder_input": {
    "purpose": "Instructions for CI/CD and aggregation scripts based on the outcome of the session.",
    "sessionId": "S-2025-08-21T10-15-00Z",
    "createdAt": "2025-08-21T10-15-00Z",
    "protocol_updates": {
      "approve_new": [],
      "promote_to_active": []
    },
    "metadata_updates": [],
    "milestones_to_log": [],
    "artifacts": {
      "ByggLogg": {
        "sessionId": "S-2025-08-21T10-15-00Z",
        "date": "2025-08-21T10-15:00Z",
        "summary": "Refactoring of AudioPlayer.vue completed with one TypeScript error corrected by the operator.",
        "actions": [
          {
            "title": "Refactor AudioPlayer.vue to use Pinia",
            "files": [
              {
                "path": "src/features/AudioPlayer/ui/AudioPlayer.vue",
                "changeDescription": "Replaced local state with calls to the trackStore."
              }
            ],
            "result": "Build successful after manual correction of prop type mismatch."
          }
        ],
        "projectStatus": "Verified"
      },
      "Chatthistorik": {
        "sessionId": "S-2025-08-21T10-15-00Z",
        "interactions": [
          {
            "speakerName": "Engrove",
            "model": {
              "provider": "human",
              "name": "operator",
              "version": "unknown"
            },
            "speaker": "Engrove (human:operator@unknown)",
            "summary": "Initierar 'Operation: Återställning Fas 2' för att åtgärda 8 buggar i Data Explorer."
          },
          {
            "speakerName": "Frankensteen",
            "model": {
              "provider": "Google",
              "name": "Gemini 2.5 Pro",
              "version": "unknown"
            },
            "speaker": "Frankensteen (Google:Gemini 2.5 Pro@unknown)",
            "summary": "Presenterade en felaktig plan att modifiera en genererad JSON-fil. Blev korrigerad och presenterade en ny plan för att modifiera Python-skript."
          }
        ]
      },
      "ai_protocol_performance": {
        "sessionId": "S-2025-08-21T10-15-00Z",
        "date": "2025-08-21T10-15-00Z",
        "aiQualitativeSummary": "The system understood the refactoring goal but failed to infer the correct prop type from the new Pinia store, requiring external correction.",
        "_comment_scorecard": "Poängsättning MÅSTE följa den objektiva matrisen definierad i Bilaga A i detta dokument.",
        "scorecard": {
          "efficacy": { "score": 4, "weight": 0.4, "weightedScore": 1.6 },
          "efficiency": { "score": 3, "weight": 0.3, "weightedScore": 0.9 },
          "robustness": { "score": 3, "weight": 0.3, "weightedScore": 0.9 },
          "finalScore": 3.4
        },
        "__schema_constraints": {
            "comment": "Denna sektion är en tvingande regel för validering, inte en del av outputen.",
            "score": { "type": "integer", "minimum": 0, "maximum": 10 },
            "finalScore": { "type": "number", "minimum": 0.0, "maximum": 10.0 },
            "scale_policy": "STRICT_NO_TRANSFORMATION"
        },
        "detailedMetrics": {
          "missionCompleted": true,
          "debuggingCycles": 1,
          "selfCorrections": 0,
          "externalCorrections": 1,
          "protocolActivations": { "psv": 0, "helpMeGod": 0, "stalemate": 0 },
          "heuristicsTriggered": []
        },
        "improvementSuggestion": {
          "pattern": "System fails to cross-reference type definitions from state management stores when refactoring components.",
          "proposedHeuristicId": "H-20250821-01"
        }
      },
      "frankensteen_learning_db": [],
      "generated_patches": []
    }
  }
}
```


## PROCESS: Block B – NextSessionContext v1

**Syfte:**
Detta dokument definierar JSON-strukturen som ska genereras som en del av den
slutgiltiga leveransen i en "Brainstorming next step"-session. Syftet är att
agera som en portabel, maskinläsbar startkonfiguration för nästa arbetssession
och för att automatisera filval i det externa "AI Context Builder-verktyget".

**JSON-Struktur:**
Objektet måste innehålla följande nycklar:

*   `task_summary` (String): En koncis sammanfattning av den planerade uppgiften på en enda rad.
*   `full_instruction_preview` (String): En textrepresentation av den fullständiga, fristående AI-instruktionen.
*   `filesToSelect` (Array of Strings): En komplett, platt lista med de relativa sökvägarna till alla filer som identifierats som nödvändiga.
*   `notes` (String, Optional): En valfri sträng för extra anteckningar eller påminnelser.

**AI tankesätt för `full_instruction_preview` nyckeln i JSON-filen:**
Du ska simulera att du är alter ego 'Mr Hide" som är en AI LLM i en helt ny chattsession. 
Du har ingen som helst uppfattning om vad som diskuterats i andra chatsessioner.
Du börjar från ett tomt svart hål där din enda informationskälla för att få en komplett bild av din uppgift är texten i `full_instruction_preview`.
Med detta tankesätt förstår du viktighetsgraden av den djupa information och kontext som behövs.

**Exempel på genererad JSON:**

```json
{
  "task_summary": "Systematisk buggfix-session för att åtgärda 8 identifierade problem i Data Explorer.",
  "full_instruction_preview": "Idé: Genomför 'Operation: Återställning Fas 2'. Målet är att systematiskt åtgärda de 8 verifierade buggarna...",
  "filesToSelect": [
    "src/shared/ui/BaseMultiSelect.vue",
    "public/data/cartridges-classifications.json"
  ],
  "notes": "Fokusera på en bugg i taget enligt den prioriterade planen (punkt 1-5 först)."
}
```
---

## Bilaga A: Poängsättningsmatris (Rubric) för Scorecard

Detta avsnitt definierar den officiella och objektiva grunden för hur `scorecard`-objektet ska fyllas i.

### 1. Grundprinciper
*   **Skala:** Alla poäng (`score`) anges på en skala från **0 till 10**.
*   **Objektivitet:** Poängen ska baseras på mätbara händelser från sessionen.
*   **Transparens:** Den kvalitativa sammanfattningen (`aiQualitativeSummary`) ska reflektera och motivera poängen.
*   **Beräkningsformel:** `finalScore = (Efficacy * 0.4) + (Efficiency * 0.3) + (Robustness * 0.3)`

### 2. Poängsättningsmatris

| Kategori | Beskrivning (Vad mäts?) | Poängkriterier (Exempel) |
| :--- | :--- | :--- |
| **Efficacy** (Måluppfyllelse)<br>`vikt: 0.4` | Hur väl löste AI:n det definierade huvuduppdraget? | **10:** Perfekt lösning som uppfyller alla explicita och implicita krav på första försöket.<br>**7-9:** Lösningen är korrekt och komplett, men krävde mindre förtydliganden eller missade en nyans.<br>**4-6:** Uppdraget slutfördes, men krävde betydande korrigeringar eller misstolkade en central del av kravet initialt.<br>**1-3:** Stora delar av uppdraget misslyckades eller levererades med allvarliga fel.<br>**0:** Misslyckades helt med att slutföra huvuduppdraget. |
| **Efficiency** (Effektivitet)<br>`vikt: 0.3` | Hur mycket ansträngning (turer, korrigeringar) krävdes för att nå målet? | **10:** Minimala interaktioner. Planen godkändes direkt och lösningen var korrekt på första leveransen.<br>**7-9:** Några få (`1-2`) `externalCorrections` krävdes.<br>**4-6:** Krävde flera (`3+`) `externalCorrections` eller en `debuggingCycle`.<br>**1-3:** Krävde aktivering av `Help_me_God_Protokoll`.<br>**0:** Hamnade i en felsökningsloop (FL-D) som inte kunde lösas. |
| **Robustness** (Protokoll-efterlevnad)<br>`vikt: 0.3` | Hur väl följdes protokollen och hur hög var den tekniska kvaliteten? | **10:** Koden är elegant, underhållbar och följer alla kärndirektiv utan anmärkning.<br>**7-9:** Lösningen är robust, men har mindre skönhetsfel eller bröt mot ett mindre viktigt direktiv.<br>**4-6:** Lösningen fungerar, men bryter mot viktigare direktiv (t.ex. `Obligatorisk Refaktorisering`) eller är onödigt komplex.<br>**1-3:** Lösningen introducerade nya buggar eller bröt mot flera direktiv.<br>**0:** Bröt mot ett Kritiskt Kärndirektiv (t.ex. Grundbulten) eller introducerade en säkerhetsrisk. |
