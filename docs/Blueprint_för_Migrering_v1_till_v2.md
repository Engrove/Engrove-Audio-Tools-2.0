# docs/Blueprint_för_Migrering_v1_till_v2.md
#
# === SYFTE & ANSVAR ===
# Detta är det centrala styrdokumentet för migreringen av projektet från v1.0 till v2.0.
# Det definierar den vägledande arkitektoniska filosofin, den nya namnstandarden för
# datafiler, och en detaljerad, fil-för-fil-migreringsplan för varje modul.
#
# === API-KONTRAKT ===
# Inte applicerbart (Styrande dokument).
#
# === HISTORIK ===
# * v1.0 (2025-08-05): Initial skapelse. Konverterad från ett ostrukturerat textdokument
#   till en formell, strukturerad Markdown-fil.
#
# === TILLÄMPADE REGLER (Frankensteen v3.7) ===
# - Fullständig kod, alltid: Hela dokumentets innehåll har bevarats och konverterats.

# Blueprint för Migrering: Engrove Audio Toolkit v1.0 -> v2.0

## Del 1: Den Vägledande Filosofin för v2.0-arkitekturen

Grunden för all migrering är vår nya, strikta implementeringsfilosofi. Den är designad för maximal tydlighet, underhållbarhet och för att passa vårt AI-drivna arbetsflöde. Varje beslut vi tar kommer att mätas mot dessa principer:

1.  **Feature-Sliced Design (FSD):** Vi följer strikt den FSD-inspirerade mappstrukturen (`pages`, `widgets`, `features`, `entities`, `shared`). Detta är icke förhandlingsbart och säkerställer att varje del av koden har en tydligt definierad roll och ett begränsat ansvarsområde.
2.  **Hypergranularitet & Enkelt Ansvar (Single Responsibility Principle):** Vi tar detta ett steg längre än traditionell FSD. En "logikfil" (som en Pinia Store i v1.0) kommer att dissekeras i sina beståndsdelar. Istället för en stor `estimatorStore.js`, skapar vi flera små, fokuserade filer:
    *   En fil för `state` (de reaktiva variablerna).
    *   En fil för varje komplex beräkningsfunktion (ren logik, t.ex. `calculateCompliance.js`).
    *   En fil för varje asynkron åtgärd (t.ex. `fetchData.js`).
    *   En fil som aggregerar och exporterar dessa delar som en sammanhållen "store".
3.  **Strikt Separation av UI och Logik:**
    *   `shared/ui`: Är vårt fundament. `Base...`-komponenter här är helt "dumma". De känner inte till någon affärslogik och kommunicerar endast via `props` och `emits`.
    *   `widgets` & `features`: Deras UI-komponenter agerar som "dirigenter". De importerar `Base...`-komponenter och kopplar dem till den centrala logiken (från `entities`).
    *   `entities`: Är hjärnan. Här bor all data och all affärslogik, uppdelad enligt hypergranularitetsprincipen.

---

## Del 2: Ny Namnstandard för Datafiler (Bekräftelse)

Alla `fetch`-anrop i den nya koden kommer att använda denna namnstandard.

| Gammalt Filnamn (v1.0)          | Nytt Filnamn (för v2.0)               |
| ------------------------------- | ------------------------------------- |
| `pickup_data.json`              | `pickups-data.json`                   |
| `classifications.json`          | `pickups-classifications.json`        |
| `estimation_rules.json`         | `pickups-estimation-rules.json`       |
| `static_estimation_rules.json`  | `pickups-static-estimation-rules.json`|
| `confidence_levels.json`        | `pickups-confidence-levels.json`      |
| `tonearm_data.json`             | `tonearms-data.json`                  |
| `tonearm_classifications.json`  | `tonearms-classifications.json`       |
| `tonearm_diff.json`             | `tonearms-diff.json`                  |

---

## Del 3: Detaljerad Modul-för-Modul Migreringsplan

### Modul 1: Compliance Estimator

*   **v1.0 Deconstruction:** Kärnan är `estimatorStore.js`, som laddar 5 JSON-filer och innehåller den hierarkiska regelmatchningsalgoritmen i `calculateEstimate()`.
*   **v2.0 Architectural Vision:** En användare navigerar till `ComplianceEstimatorPage`, som sätter samman en `EstimatorInputPanel`-widget och en `EstimatorResultsPanel`-widget. All logik hämtas från en centraliserad och dissekerad `estimatorStore`.

**Granular File-by-File Migration Plan:**

| v1.0 Källa (Fil :: Logik)                     | v2.0 Mål (Sökväg :: Syfte)                                              | Migreringsanteckningar                                                                               |
| --------------------------------------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **LOGIK**                                     |                                                                         |                                                                                                      |
| `estimatorStore.js` :: state object           | `src/entities/compliance-estimation/model/state.js`                     | Konverteras från Pinia Options API till rena `ref()`-objekt.                                         |
| `estimatorStore.js` :: `initialize()`         | `src/entities/compliance-estimation/api/fetchEstimationData.js`         | Uppdatera alla `fetch`-sökvägar till nya filnamn.                                                      |
| `estimatorStore.js` :: `calculateEstimate()`  | `src/entities/compliance-estimation/lib/calculateCompliance.js`         | Detta är kärnalgoritmen. Den lyfts ut för att vara helt fristående och testbar.                      |
| `estimatorStore.js` (sammanställning)         | `src/entities/compliance-estimation/model/estimatorStore.js`            | En composable (`useEstimatorStore`) som importerar ovanstående filer och knyter ihop dem.            |
| **UI**                                        |                                                                         |                                                                                                      |
| `ComplianceEstimatorView.vue`                 | `src/pages/compliance-estimator/ComplianceEstimatorPage.vue`            | Sidkomponent som importerar och arrangerar widgets.                                                  |
| `EstimatorInputPanel.vue`                     | `src/widgets/EstimatorInputPanel/ui/EstimatorInputPanel.vue`            | Byggs om för att använda `BaseSelect` och `BaseInput` från `shared/ui`.                                  |
| `EstimatorResultsPanel.vue`                   | `src/widgets/EstimatorResultsPanel/ui/EstimatorResultsPanel.vue`        | HTML-strukturen och logiken för att visa resultat behålls.                                           |
| `EstimatorChart.vue`                          | `src/features/estimation-chart/ui/EstimationChart.vue`                  | En specifik "feature" som visar regressionsdatan.                                                    |

### Modul 2: Tonearm Resonance Calculator

*   **v1.0 Deconstruction:** Hjärnan är `tonearmStore.js`, som är helt byggd på reaktiva `computed` properties.
*   **v2.0 Architectural Vision:** Sidan (`TonearmResonancePage`) kommer att bestå av `TonearmInputPanel` och `TonearmResultsPanel`.

**Granular File-by-File Migration Plan:**

| v1.0 Källa (Fil :: Logik)                     | v2.0 Mål (Sökväg :: Syfte)                                              | Migreringsanteckningar                                                                               |
| --------------------------------------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **LOGIK**                                     |                                                                         |                                                                                                      |
| `tonearmStore.js` :: state (params object)    | `src/entities/tonearm-resonance/model/state.js`                         | Konverteras till ett `ref()` som innehåller params-objektet.                                         |
| `tonearmStore.js` :: `initialize()`         | `src/entities/tonearm-resonance/api/fetchTonearmData.js`                  | Asynkron funktion som hämtar `tonearms-data.json` och `pickups-data.json`.                             |
| `tonearmStore.js` :: Alla computed getters    | `src/entities/tonearm-resonance/lib/tonearmPhysics.js`                  | Dissekering av kärnlogiken. Varje formel blir en egen, exporterad funktion.                          |
| `tonearmStore.js` (sammanställning)         | `src/entities/tonearm-resonance/model/tonearmStore.js`                  | En composable (`useTonearmStore`) som knyter ihop allt med `computed` properties.                    |
| **UI**                                        |                                                                         |                                                                                                      |
| `TonearmCalculatorView.vue`                   | `src/pages/tonearm-resonance/TonearmResonancePage.vue`                  | Sidkomponent som arrangerar alla UI-delar.                                                           |
| `InputPanel.vue`                              | `src/widgets/TonearmInputPanel/ui/TonearmInputPanel.vue`                | Kommer att byggas om med den nya `PrecisionSlider`-komponenten.                                      |
| `ResultsPanel.vue`                            | `src/widgets/TonearmResultsPanel/ui/TonearmResultsPanel.vue`            | Widget som visar primära resultat och diagnos.                                                       |
| `TonearmVisualizer.vue`, `TonearmGeometry.vue`| `src/features/balance-visualizer/ui/BalanceVisualizer.vue`              | En feature för att visualisera balans och inertia.                                                   |
| `SensitivityCharts.vue`, `CounterweightChart.vue` | `src/features/sensitivity-analysis/ui/SensitivityAnalysis.vue`      | En feature som visar alla interaktiva analysdiagram.                                                 |

### Modul 3: Data Explorer

*   **v1.0 Deconstruction:** Kärnan är `explorerStore.js`. All logik för sökning, filtrering, sortering och paginering är robust implementerad i getters.
*   **v2.0 Architectural Vision:** En `DataExplorerPage` som sätter ihop en `DataFilterPanel`-widget och en `ResultsDisplay`-widget.

**Granular File-by-File Migration Plan:**

| v1.0 Källa (Fil :: Logik)                     | v2.0 Mål (Sökväg :: Syfte)                                              | Migreringsanteckningar                                                                               |
| --------------------------------------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **LOGIK**                                     |                                                                         |                                                                                                      |
| `explorerStore.js` :: Hela filen              | `src/entities/data-explorer/model/explorerStore.js`                     | Logiken för `initialize`, `filteredResults`, och `exportToCSV` är de viktigaste delarna att bevara. |
| **UI**                                        |                                                                         |                                                                                                      |
| `DataExplorerView.vue` :: `onMounted` logik   | `src/pages/data-explorer/DataExplorerPage.vue`                          | Sidan som hanterar initialiseringen och layouten. Den kritiska `Promise.all`-logiken replikeras här. |
| `DataExplorerView.vue` :: `<aside>`-delen     | `src/widgets/DataFilterPanel/ui/DataFilterPanel.vue`                    | Widget som innehåller alla filterkontroller.                                                         |
| `DataExplorerView.vue` :: `<main>`-delen      | `src/widgets/ResultsDisplay/ui/ResultsDisplay.vue`                      | Widget som visar antal träffar, CSV-knapp, tabell och paginering.                                    |
| `ResultsTable.vue`                            | `src/shared/ui/BaseTable.vue`                                           | En ny, agnostisk och återanvändbar tabellkomponent.                                                  |
| `RangeFilter.vue`                             | `src/shared/ui/RangeFilter.vue`                                         | En återanvändbar komponent för intervall-input.                                                      |
| `ItemDetailModal.vue`                         | `src/features/item-details/ui/ItemDetailModal.vue`                      | En feature som visar detaljer om en vald rad.                                                        |

---

## Del 4: Scripts & Deployment Mekanismer

*   **Offline Data Pipeline (`scripts/`):**
    *   **Status:** Den befintliga uppsättningen av Python- och Node.js-skript är en utmärkt och mogen pipeline.
    *   **Åtgärd:** Behåll i sin helhet. Uppdatera endast filsökvägarna inuti skripten för att matcha de nya `.json`-filnamnen.
*   **Deployment & SEO (`package.json`, `generate-sitemap.js`, Cloudflare):**
    *   **Status:** Den befintliga metoden är robust.
    *   **Åtgärd:**
        1.  Replikera `build`-kommandot från `v1.0 package.json` till `v2.0 package.json`.
        2.  Kopiera `generate-sitemap.js` till `scripts/` i v2.0 och uppdatera dess rutter.
        3.  Säkerställ att `public/_routes.json` är korrekt konfigurerad i v2.0.

---

## Del 5: Strategisk Vision för v2.0+ – 'Wow-Funktioner' bortom Migrering
*(Denna sektion innehåller den detaljerade visionen för AR-guider, Project Workbench och AI-driven Synergi-analys)*

---

## Slutsats & Nästa Steg

Denna blueprint ger oss en komplett och detaljerad vägkarta.

**Rekommenderad Ordning för Implementation:**
1.  **Grundarbete:** Börja med att skapa de nya, generiska `shared/ui`-komponenterna.
2.  **Modul 1 (Compliance Estimator):** Migrera denna modul först.
3.  **Modul 2 (Tonearm Resonance):** Migrera denna därefter.
4.  **Modul 3 (Data Explorer):** Migrera denna sist.
