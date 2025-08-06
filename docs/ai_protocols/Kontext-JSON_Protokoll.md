# docs/ai_protocols/Kontext-JSON_Protokoll.md
#
# === SYFTE & ANSVAR ===
# Detta dokument definierar JSON-strukturen som ska genereras som en del av den
# slutgiltiga leveransen i en "Brainstorming next step"-session. Syftet är att
# agera som en portabel, maskinläsbar startkonfiguration för nästa arbetssession
# och för att automatisera filval i AI Context Builder-verktyget.
#
# === HISTORIK ===
# * v1.0 (2025-08-06): Initial skapelse. Extraherad från den monolitiska AI.md
#   som en del av "Operation: Modulär Instruktion".

### EXTRA PROTOKOLL: "KONTEXT-JSON FÖR NÄSTA SESSION" (Version 1.0)
-----------------------------------------------------------------
Detta protokoll definierar den JSON-struktur som ska genereras som en del av den slutgiltiga leveransen i en "Brainstorming next step"-session. Syftet med denna JSON-fil är att agera som en portabel, maskinläsbar startkonfiguration för nästa arbetssession.

JSON-objektet är designat för att klistras in direkt i "instruction-input"-rutan i AI Context Builder-verktyget, vilket automatiskt för-markerar alla relevanta filer för den kommande uppgiften.

**Integration med "Brainstorming next step":**
Denna JSON-fil utgör en ny, obligatorisk leveranspunkt (punkt 8) i "Slutgiltig Leverans"-sektionen av "Brainstorming next step"-protokollet.

**JSON-Struktur:**
Objektet måste innehålla följande nycklar:

*   `task_summary` (String): En koncis sammanfattning av den planerade uppgiften på en enda rad.
*   `full_instruction_preview` (String): En textrepresentation av den fullständiga, fristående AI-instruktionen som skapades i punkt 5 av Brainstorming_Protokoll.md. Denna text måste innehålla en **fullständig och djupt detaljerad uppdragsbeskrivning**, inklusive tekniska analyser och implementation-detaljer för varje delmoment, i enlighet med de skärpta kraven i brainstorming-protokollet. Detta ger en mänsklig förhandsgranskning av hela den verifierade uppgiften.
*   `filesToSelect` (Array of Strings): En komplett, platt lista med de relativa sökvägarna till **alla** filer som identifierats som nödvändiga (källkod, externa filer, styrdokument). Detta är nyckeln som AI Context Builder-verktyget använder för att automatiskt markera kryssrutorna.
*   `notes` (String, Optional): En valfri sträng för extra anteckningar eller påminnelser inför nästa session, t.ex. "Fokusera på felhanteringen i `fetchData.js`" eller "Kom ihåg att uppdatera versionsnumret i `package.json`".

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
