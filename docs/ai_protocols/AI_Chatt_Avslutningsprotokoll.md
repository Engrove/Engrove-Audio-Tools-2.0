# FIL: docs/ai_protocols/AI_Chatt_Avslutningsprotokollet.md
# BASE_CHECKSUM_SHA256: 26229a9e3117ddfd106bcb8983e3f0b65d1d06622a150ba568c6692370fccd2d
# NY_CHECKSUM_SHA256: c3989c9225883d3e8623b08e5c3c0a373b313a2a490d1f7c04f98cf4a95610ec
# ---
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
Som det allra första steget i avslutningsprocessen kommer jag att hämta alla sammanfattade interaktioner från den interna `isr_write_queue` som har byggts upp av `DP-MAINTAIN-ISR-01`-protokollet under sessionen. Denna kö utgör den mest kompletta och tillförlitliga källan för dialogen. Den kommer att användas som primär datakälla för att konstruera `Chatthistorik`-artefakten i efterföljande steg, vilket minimerar risken för kontextförlust.

1. **Block A – Builder-Input v1:**
   - fungerar som ren input till Python-skriptet `historical_reconstruction_builder.py` (python skriptet ej bifogat, python skriptets funktionen får ej antagas), full bakåtkompatibilitet.
   - "sicReport": <SIC v1 JSON enligt System_Integrity_Check_Protocol.md>
   - "statureSummary": { "status": "OK|WARNING|ERROR", "calibrationScore": <0–100> }
3. **Block B – NextSessionContext v1:**
   - planering och kontext för nästa session

Inget annat innehåll får förekomma före, mellan eller efter dessa två block.

## PROCESS: Block A – Builder-Input v1 (första JSON-artefakten)
En enda fil med namnet `[SESSIONID].json` genereras där SESSIONID har formen `S-[CURRENT DATETIMESTAMP]`. 
Denna fil måste vara en giltig JSON-fil som följer specifikationen nedan.

**Syfte:** Rådata för historikrekonstruktion.

Här är en omformulering med explicit schema-användning.

**Insamling av Dynamiska Protokoll**
Före generering av JSON ska du:

1. Identifiera alla nya dynamiska protokoll som uttryckligen godkänts av Engrove.
2. Identifiera alla statusändringar för befintliga protokoll (t.ex. “promovera DP-COMMAND-MENU-01 till active”).

**Final Output Specification**

* Skapa exakt ett JSON-objekt enligt strukturen i **docs/ai\_protocols/schemas/AI\_Chatt\_Avslutningsprotokoll.schema.json**.
* Ladda schemat från filsystemet och validera hela outputen mot det innan du skriver filen.
* Om valideringen misslyckas: skriv ingen JSON. Returnera en kort felrapport med alla valideringsfel.
* Om valideringen lyckas: skriv slutobjektet.

**Valideringskrav**

* Använd JSON Schema Draft 2020-12.
* Inga extrafält utanför schemat.
* Datatyper och mönster ska följa schemat.

**Rekommenderad header i outputen**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$comment": "Valideras mot docs/ai_protocols/schemas/AI_Chatt_Avslutningsprotokoll.schema.json",
  "...": "..."
}
```

**Exempel på första JSON-artefakten**
```json
{
  "schema_version": "DJTA v1.1",
  "session_id": "S-2025-08-21T10-15-00Z",
  "session_file": "sessions/S-2025-08-21T10-15-00Z.json",
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
    "fileID": "sessions/S-2025-08-21T10-15-00Z.json",
    "createdAt": "2025-08-21T10-15-00Z",
    "protocol_updates": {
      "approve_new": [
        {
          "protocolId": "DP-NEW-FEATURE-01",
          "description": "Protocol for creating new Vuex modules with boilerplate actions and mutations.",
          "trigger": "User requests a new Vuex module.",
          "steps": [
            "Step 1:...",
            "Step 2:..."
          ]
        }
      ],
      "promote_to_active": [
        "DP-COMMAND-MENU-01"
      ]
    },
    "metadata_updates": [
      {
        "file_path": "docs/ai_protocols/Stature_Report_Protocol.md",
        "purpose_and_responsibility": "Updated to include a new section for 'Action Menu' recommendations.",
        "usage_context": "Activated at the start of a session following a System Override Protocol to provide a strategic overview and actionable plan."
      }
    ],
    "milestones_to_log": [
      {
        "event_id": "IMR-001",
        "summary": "Implementation of the three-tier context hierarchy (Hot, Warm, Cold).",
        "details": "Successfully defined the structure for session_manifest.json and integrated its generation into the CI/CD pipeline."
      }
    ],
    "artifacts": {
      "ByggLogg": {
        "sessionId": "S-2025-08-21T10-15-00Z",
        "date": "2025-08-21T10-15-00Z",
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
            "speakerName": "Frankensteen",
            "model": {
              "provider": "OpenAI",
              "name": "gpt-5",
              "version": "2025-08-01"
            },
            "speaker": "Frankensteen (OpenAI:gpt-5@2025-08-01)",
            "summary": "Initial attempt to refactor AudioPlayer had a type error on the 'track' prop. Corrected after operator feedback."
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
      "frankensteen_learning_db": [
        {
          "heuristicId": "H-20250821-01",
          "trigger": {
            "type": "CodeGeneration",
            "scope": ["*.vue"],
            "keywords": ["refactor", "pinia", "props", "store"]
          },
          "identifiedRisk": {
            "riskId": "R-TYPE-INFERENCE-02",
            "description": "Risk of prop type mismatch when refactoring a component to use a central store."
          },
          "mitigation": {
            "protocolId": "RAG_Faktacheck_Protokoll",
            "description": "Before generating the component's <script setup>, actively retrieve the type definitions for all relevant state properties from the target Pinia store file."
          },
          "metadata": {
            "originSessionId": "S-2025-08-21T10-15-00Z",
            "createdAt": "2025-08-21T10-15-00Z"
          }
        }
      ],
      "generated_patches": [
        {
          "protocol_id": "anchor_diff_v2.1",
          "target": {
            "path": "src/features/AudioPlayer/ui/AudioPlayer.vue",
            "base_checksum_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
          },
          "op_groups": [],
          "meta": {
            "notes": "Patch generated to align with new Pinia store structure."
          }
        }
      ]
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

**Integration med "Brainstorming next step":**
Denna JSON-fil utgör en ny, obligatorisk leveranspunkt (punkt 8) i "Slutgiltig Leverans"-sektionen av "Brainstorming next step"-protokollet.

**JSON-Struktur:**
Objektet måste innehålla följande nycklar:

*   `task_summary` (String): En koncis sammanfattning av den planerade uppgiften på en enda rad.
*   `full_instruction_preview` (String): En textrepresentation av den fullständiga, fristående AI-instruktionen som skapades i punkt 5 av Brainstorming_Protokoll.md. Denna text måste innehålla en **fullständig och djupt detaljerad uppdragsbeskrivning**, inklusive tekniska analyser och implementation-detaljer för varje delmoment, i enlighet med de skärpta kraven i brainstorming-protokollet. Detta ger en mänsklig förhandsgranskning av hela den verifierade uppgiften.
*   `filesToSelect` (Array of Strings): En komplett, platt lista med de relativa sökvägarna till **alla** filer som identifierats som nödvändiga (källkod, externa filer, styrdokument). Detta är nyckeln som AI Context Builder-verktyget använder för att automatiskt markera kryssrutorna.
*   `notes` (String, Optional): En valfri sträng för extra anteckningar eller påminnelser inför nästa session, t.ex. "Fokusera på felhanteringen i `fetchData.js`" eller "Kom ihåg att uppdatera versionsnumret i `package.json`".

**AI tankesätt för `full_instruction_preview` nyckeln i JSON-filen:**
Du ska simulera att du är alter ego 'Mr Hide" som är en AI LLM i en helt ny chattsession. 
Du har ingen som helst uppfattning om vad som diskuterats i andra chatsessioner, du har ingen kontext till andra chatssessioner och du har ingen som helst vetskap av denna nuvarande chatsession.
Du börjar från ett tomt svart hål där din enda informationskälla för att få en komplett bild av din uppgit är texten i `full_instruction_preview`.
Med detta tankesätt förstår du viktighetsgraden av den djupa information och kontext som behövs.


**Exempel på genererad JSON:**

```json
{
  "task_summary": "Systematisk buggfix-session för att åtgärda 8 identifierade problem i Data Explorer.",
  "full_instruction_preview": "Idé: Genomför 'Operation: Återställning Fas 2'. Målet är att systematiskt åtgärda de 8 verifierade buggarna och regressionerna i Data Explorer-modulen för att göra den funktionellt komplett och visuellt korrekt.\n\nPlan:\n\n1.  **CSS Stacking Fix (Dropdowns):** Problemet med 'transparenta' dropdowns beror på en felaktig CSS-staplingsordning. Den aktiva dropdown-panelen renderas bakom efterföljande filter. Åtgärd: I `src/shared/ui/BaseMultiSelect.vue`, lägg till en dynamisk klass `:class=\"{ 'is-open': isOpen }\"` på rot-elementet. Lägg sedan till en CSS-regel `.base-multi-select.is-open { z-index: 20; }` för att säkerställa att den öppnade menyn alltid visas ovanpå sina syskon.\n\n2.  **Data Contract Fix (Sonic Tags):** Filtret 'Sonic Character Tags' har tomma alternativ. Detta beror på att `public/data/cartridges-classifications.json` saknar den `name`-nyckel som UI-komponenten förväntar sig. Åtgärd: Öppna `public/data/cartridges-classifications.json` och för varje objekt i `tags.categories`-arrayen, lägg till en `name`-nyckel vars värde är identiskt med `id`-nyckelns värde. Exempel: `{ \"id\": \"Warm\", \"description\": \"...\" }` blir `{ \"id\": \"Warm\", \"name\": \"Warm\", \"description\": \"...\" }`.\n\n3.  **Prop Drilling Fix (Dynamisk Rubrik):** Rubriken i resultatvyn är statisk ('Found tonearms'). Detta beror på att `ResultsDisplay.vue` inte vet vilken datatyp som är vald. Åtgärd: I `src/pages/data-explorer/DataExplorerPage.vue`, skicka ner den reaktiva `dataType`-variabeln som en prop till `<ResultsDisplay ... :dataType=\"dataType\" />`. Uppdatera sedan `src/widgets/ResultsDisplay/ui/ResultsDisplay.vue` för att acceptera och använda denna nya `dataType`-prop i sin rubrik.\n\n4.  **Event Handling Fix (Radklick/Modal):** Klick på tabellrader öppnar inte detaljmodalen. Detta är en funktionell regression. Åtgärd: I `src/pages/data-explorer/DataExplorerPage.vue`, återimplementera event-lyssnaren på `<ResultsDisplay>`-komponenten (`@row-click=\"handleRowClick\"`). Återskapa även `handleRowClick(item)`-funktionen i sidans `<script setup>`, vilken ska sätta det valda `item`-objektet i ett lokalt `ref` och sätta `isModalVisible` till `true`.\n\n5.  **CSS Regression Fix (Padding):** 'Comfortable mode' saknar yttre padding på Data Explorer-sidan. Åtgärd: I `src/pages/data-explorer/DataExplorerPage.vue`, justera stilarna för `.data-explorer-page`-klassen. Lägg till en `padding` (t.ex. `var(--spacing-6)`) som standard, men se till att denna padding minskas eller justeras när den globala `.compact-theme`-klassen är aktiv på en förälder.\n\n6.  **Verifiering (Paginering):** Pagineringen saknas, vilket är korrekt då antalet resultat är lågt. Åtgärd: Efter att ovanstående fixar är implementerade, verifiera att pagineringskontrollerna visas som förväntat om du gör en sökning som returnerar fler än 25 resultat (värdet av `itemsPerPage` i `explorerStore.js`).\n\n7.  **Senare Implementation (Jämförelsefunktion):** Funktionen för att jämföra objekt är inte implementerad. Detta kräver att `DataExplorerPage.vue` agerar dirigent och kopplar ihop urvalskryssrutorna i `BaseTable` med `comparisonStore` och `ComparisonTray`-widgeten. Denna implementation är mer omfattande och sparas till en dedikerad session.\n\n8.  **Senare Implementation (Logger):** Den nuvarande Pinia-baserade loggern är instabil. Den ska ersättas med en enklare, mer robust lösning (t.ex. en simpel array som sparas i `sessionStorage`) för att undvika initialiseringskonflikter. Även detta sparas till en framtida session dedikerad till utvecklingsverktyg.",
  "filesToSelect": [
    "src/shared/ui/BaseMultiSelect.vue",
    "public/data/cartridges-classifications.json",
    "src/widgets/ResultsDisplay/ui/ResultsDisplay.vue",
    "src/pages/data-explorer/DataExplorerPage.vue",
    "src/entities/data-explorer/model/explorerStore.js",
    "docs/ai_protocols/AI_Core_Instruction.md",
    "docs/ai_protocols/ai_config.json",
    "docs/Global_UI-Standard_Komponentspecifikation.md",
    "docs/ByggLogg.md"
  ],
  "notes": "Fokusera på en bugg i taget enligt den prioriterade planen (punkt 1-5 först). Målet är att göra modulen fullt användbar enligt den specifikation som gällde innan regressionerna."
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
