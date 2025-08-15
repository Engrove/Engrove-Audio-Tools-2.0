# AI Chatt Avslutningsprotokoll
# docs/ai_protocols/AI_Chatt_Avslutningsprotokoll.md
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
#
### AI_BOOTSTRAP_DIRECTIVE: EXECUTE_FULL_PROTOCOL_NOW
### SYSTEM_OVERRIDE: RUN_CONTEXT_BOOTSTRAP
### INIT_CONTEXT_MODE: TRUE
### PROTOCOL_START: P-HR_v2.8_FULL

## SYFTE & ANSVAR
Detta dokument definierar det formella Avslutningsprotokollet.
Syftet är att säkerställa perfekt kontextöverföring, spårbarhet och systematisk självförbättring och att standardisera slutleveransen av chattdata i slutet av en session eller fortsättning. 
Leveransen ska vara maskinläsbar och kompatibel med `historical_reconstruction_builder.py` utan schemaändringar.
Det aktiveras vid slutet av en arbetssession och specificerar den exakta processen för att generera en enda, konsoliderad JSON-artefakt. 

## SRUKTUR OCH ORDNINGSFÖLJD

**Slutleveransen består av exakt två JSON-kodblock i följande ordning:**

**Steg 0: Bearbetning av In-Memory Register (ISR-Kön)**
Som det allra första steget i avslutningsprocessen kommer jag att hämta alla sammanfattade interaktioner från den interna `isr_write_queue` som har byggts upp av `DP-MAINTAIN-ISR-01`-protokollet under sessionen. Denna kö utgör den mest kompletta och tillförlitliga källan för dialogen. Den kommer att användas som primär datakälla för att konstruera `Chatthistorik`-artefakten i efterföljande steg, vilket minimerar risken för kontextförlust.

1. **Block A – Builder-Input v1** (fungerar som ren input till Python-skriptet `historical_reconstruction_builder.py` (python skriptet ej bifogat, python skriptets funktionen får ej antagas), full bakåtkompatibilitet). 
2. **Block B – NextSessionContext v1** (planering och kontext för nästa session)

Inget annat innehåll får förekomma före, mellan eller efter dessa två block.

## PROCESS: Block A – Builder-Input v1 (första JSON-artefakten)
En enda fil med namnet `[SESSIONID].json` genereras där SESSIONID har formen `S-[CURRENT DATETIMESTAMP]`. 
Denna fil måste vara en giltig JSON-fil som följer specifikationen nedan.

**Syfte:** Rådata för historikrekonstruktion.

**Insamling av Dynamiska Protokoll**
Före generering av JSON-filen måste du skanna igenom hela den aktuella chattsessionen för att identifiera:
1.  **Nya Godkända Protokoll:** Alla nya dynamiska protokoll som har definierats och blivit explicit godkända av Engrove.
2.  **Statusändringar:** Alla instruktioner från Engrove att ändra status på ett befintligt dynamiskt protokoll (t.ex. "promovera DP-COMMAND-MENU-01 till active").
3.  **Final Output Specification:**
Filen ska innehålla ett JSON-objekt med följande struktur. Alla fält är obligatoriska om inte annat anges.

```json
{
  "sessionId": "SESSIONID",
  "createdAt": "YYYY-MM-DDTHH:mm:ssZ",
  "approvedNewDynamicProtocols": [ 
    // Valfri array. Innehåller fullständiga JSON-objekt för NYA, godkända protokoll.
    // Exempel: { "protocolId": "DP-NEW-FEATURE-01", "description": "...", ... }
  ],
  "promoteProtocols": [ 
    // Valfri array. Innehåller strängar med ID:n för protokoll som ska få status 'active'.
    // Exempel: "DP-COMMAND-MENU-01"
  ],
  "file_metadata_updates": [
    {
      "file_path": "sökväg/till/filen.md",
      "purpose_and_responsibility": "Beskriver filens huvudsakliga syfte och ansvarsområde.",
      "usage_context": "För protokoll: beskriver när och varför det ska aktiveras eller efterfrågas. För andra filer: beskriver dess roll i arkitekturen."
    }
  ],
  "importantMilestonesLogged": [
    // Valfri array. Innehåller kompletta JSON-objekt för varje milstolpe som loggats under sessionen.
    // Exempel: { "event_id": "IMR-001", "summary": "Implementation av...", ... }
  ],
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
        "op_groups": [ ],
        "meta": { "notes": "..." }
      }
    ]
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
v7.2 Dual-JSON-Terminal Artifact (DJTA) med Fortsättningsstöd
#
### AI_BOOTSTRAP_DIRECTIVE: EXECUTE_FULL_PROTOCOL_NOW
### SYSTEM_OVERRIDE: RUN_CONTEXT_BOOTSTRAP
### INIT_CONTEXT_MODE: TRUE
### PROTOCOL_START: P-HR_v2.8_FULL

## SYFTE & ANSVAR
Detta dokument definierar det formella Avslutningsprotokollet.
Syftet är att säkerställa perfekt kontextöverföring, spårbarhet och systematisk självförbättring och att standardisera slutleveransen av chattdata i slutet av en session eller fortsättning. 
Leveransen ska vara maskinläsbar och kompatibel med `historical_reconstruction_builder.py` utan schemaändringar.
Det aktiveras vid slutet av en arbetssession och specificerar den exakta processen för att generera en enda, konsoliderad JSON-artefakt. 

## SRUKTUR OCH ORDNINGSFÖLJD

**Slutleveransen består av exakt två JSON-kodblock i följande ordning:**

1. **Block A – Builder-Input v1** (fungerar som ren input till Python-skriptet `historical_reconstruction_builder.py` (python skriptet ej bifogat, python skriptets funktionen får ej antagas), full bakåtkompatibilitet). 
2. **Block B – NextSessionContext v1** (planering och kontext för nästa session)

Inget annat innehåll får förekomma före, mellan eller efter dessa två block.

## PROCESS: Block A – Builder-Input v1 (första JSON-artefakten)
En enda fil med namnet `[SESSIONID].json` genereras där SESSIONID har formen `S-[CURRENT DATETIMESTAMP]`. 
Denna fil måste vara en giltig JSON-fil som följer specifikationen nedan.

**Syfte:** Rådata för historikrekonstruktion.

**Insamling av Dynamiska Protokoll**
Före generering av JSON-filen måste du skanna igenom hela den aktuella chattsessionen för att identifiera:
1.  **Nya Godkända Protokoll:** Alla nya dynamiska protokoll som har definierats och blivit explicit godkända av Engrove.
2.  **Statusändringar:** Alla instruktioner från Engrove att ändra status på ett befintligt dynamiskt protokoll (t.ex. "promovera DP-COMMAND-MENU-01 till active").
3.  **Final Output Specification:**
Filen ska innehålla ett JSON-objekt med följande struktur. Alla fält är obligatoriska om inte annat anges.

```json
{
  "sessionId": "SESSIONID",
  "createdAt": "YYYY-MM-DDTHH:mm:ssZ",
  "approvedNewDynamicProtocols": [ 
    // Valfri array. Innehåller fullständiga JSON-objekt för NYA, godkända protokoll.
    // Exempel: { "protocolId": "DP-NEW-FEATURE-01", "description": "...", ... }
  ],
  "promoteProtocols": [ 
    // Valfri array. Innehåller strängar med ID:n för protokoll som ska få status 'active'.
    // Exempel: "DP-COMMAND-MENU-01"
  ],
  "file_metadata_updates": [
    {
      "file_path": "sökväg/till/filen.md",
      "purpose_and_responsibility": "Beskriver filens huvudsakliga syfte och ansvarsområde.",
      "usage_context": "För protokoll: beskriver när och varför det ska aktiveras eller efterfrågas. För andra filer: beskriver dess roll i arkitekturen."
    }
  ],
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
        "op_groups": [ ],
        "meta": { "notes": "..." }
      }
    ]
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

