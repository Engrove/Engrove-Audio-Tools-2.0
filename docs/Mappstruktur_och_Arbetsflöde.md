# docs/Mappstruktur_och_Arbetsflöde.md
#
# === SYFTE & ANSVAR ===
# Detta dokument är den definitiva "ritningen" för projektets mappstruktur och det
# AI-drivna arbetsflödet. Det definierar var varje typ av kod ska placeras och hur
# nya funktioner ska byggas på ett systematiskt och granulärt sätt.
#
# === API-KONTRAKT ===
# Inte applicerbart (Styrande dokument).
#
# === HISTORIK ===
# * v1.0 (2025-08-05): Initial skapelse. Konverterad från ett ostrukturerat textdokument
#   till en formell, strukturerad Markdown-fil. Mappstrukturen har omvandlats till en
#   standardiserad Markdown-tabell.
# * v1.1 (2025-08-11): Lade till Steg 5 i arbetsflödet för att inkludera den nya, automatiserade dokumentationsprocessen via `core_file_info.json`.
#
# === TILLÄMPADE REGLER (Frankensteen v3.7) ===
# - Fullständig kod, alltid: Hela dokumentets innehåll har bevarats och konverterats.

## Del 1: Den Exakta Mappstrukturen (The Blueprint)

Detta är den definitiva mappstrukturen för projektet. Varje mapp och dess syfte är designat för att maximera modularitet och ge din AI-programmerare ett tydligt, avgränsat sammanhang för varje uppgift. Strukturen är inspirerad av Feature-Sliced Design men anpassad för er verktygslösa miljö.

| Sökväg                 | Förklaring och Syfte för AI-interaktion                                                                                                                                                                                |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/public/`             | Statisk fil-hosting. Här placeras filer som inte processas av byggverktyget.                                                                                                                                             |
| `└── showcase.html`    | Den manuella stilguiden. Detta är er "KISS"-ersättning för Storybook. En enkel HTML-fil som laddar en Vue-app för att visa upp alla era baskomponenter i deras olika tillstånd.                                          |
| `└── data/`            | Rådata. Här ligger alla statiska JSON-filer (t.ex. `tonearm_data.json`) som applikationen använder.                                                                                                                      |
| `/src/`                | Huvudkällkoden. All er Vue-applikationskod bor här.                                                                                                                                                                      |
| `└── app/`             | Global App-konfiguration. Denna mapp initierar och konfigurerar hela applikationen.                                                                                                                                      |
| `├── styles/`          | Globala Stilar & Design Tokens. Här definieras alla CSS Custom Properties baserade på er UI-standard.                                                                                                                   |
| `└── main.js`          | Applikationens Startpunkt. Filen som skapar Vue-appen, monterar den och sätter upp globala plugins som Vue Router och Pinia.                                                                                              |
| `└── pages/`           | Sidor (Views). Varje mapp här representerar en unik "sida" eller vy i applikationen. Sidorna är kompositionslager som sätter samman widgets och features.                                                                |
| `└── ar-protractor/`   | Exempel: AR Protractor-sidan. En "skiva" för en specifik huvudfunktion.                                                                                                                                                  |
| `└── ARProtractorPage.vue` | Själva sidkomponenten som importerar och arrangerar de widgets och features som utgör AR Protractor-verktyget.                                                                                                          |
| `└── widgets/`         | Sammansatta UI-block. Stora, återanvändbara delar av gränssnittet som består av flera mindre komponenter.                                                                                                                |
| `└── GlobalHeader/`    | Exempel: Global Header. En widget som innehåller logotyp, navigation och temaväxlare.                                                                                                                                    |
| `└── GlobalHeader.vue` | Komponenten för headern. Den importerar `features/theme-toggle` och `shared/ui/Logo`.                                                                                                                                 |
| `└── features/`        | Användarfunktioner (Appens "Verb"). Detta är den viktigaste mappen för interaktivitet. Varje mapp här representerar en specifik, isolerad affärsfunktion.                                                                  |
| `└── theme-toggle/`    | Exempel: Temaväxlare.                                                                                                                                                                                                  |
| `├── ui/`              | Innehåller Vue-komponenten för själva knappen/växlaren (`ThemeToggle.vue`).                                                                                                                                              |
| `└── model/`           | Innehåller den rena logiken. T.ex. `useTheme.js` (en composable som hanterar tillståndet).                                                                                                                               |
| `└── entities/`        | Affärsobjekt (Appens "Substantiv"). Representerar de centrala datastrukturerna i er applikation.                                                                                                                         |
| `└── calculation-result/` | Exempel: Beräkningsresultat.                                                                                                                                                                                         |
| `├── ui/`              | Komponenter för att visa ett resultat, t.ex. `ResultCard.vue`.                                                                                                                                                           |
| `└── model/`           | Definitionen av datan. T.ex. `types.ts` (TypeScript-interface) och `resultStore.js` (en Pinia-store).                                                                                                                  |
| `└── shared/`          | Delad, Agnostisk Kod. Koden här får aldrig känna till någon specifik affärslogik från `features` eller `entities`.                                                                                                         |
| `├── ui/`              | Det Centrala UI-biblioteket. Här bor alla era grundläggande, återanvändbara "Base"-komponenter (`BaseButton.vue`, etc.).                                                                                                  |
| `├── lib/`             | Generella Hjälpfunktioner. Små, rena JavaScript-funktioner som kan användas överallt (t.ex. `formatDate.js`).                                                                                                            |
| `├── api/`             | API-kommunikation. Grundläggande konfiguration för att prata med externa tjänster.                                                                                                                                       |
| `└── assets/`          | Delade Resurser. Ikoner (som SVG-filer), logotyper och andra bilder som används på flera ställen i appen.                                                                                                                 |

## Del 2: Det Förenklade Utförandet (AI-First Workflow)

Detta är den praktiska guiden för hur du och din AI-programmerare arbetar med mappstrukturen ovan. Processen är designad för att vara repetitiv, förutsägbar och minimera risken för att AI:n "hallucinerar" genom att ge den extremt små och fokuserade uppgifter.

### Scenario: Bygga en ny feature - "Nollställ Beräkning"

**Steg 1: Skapa Mapparna (Din uppgift)**

Du navigerar till `src/features/` i GitHubs webbgränssnitt och skapar manuellt den nya mappstrukturen:
1.  Skapa mappen `reset-calculation`.
2.  Inuti den, skapa mapparna `ui` och `model`.

*Resultat: Du har skapat en isolerad "sandlåda" för den nya funktionen.*

**Steg 2: Skapa UI-komponenten (AI:s uppgift)**

Du öppnar `src/features/reset-calculation/ui/` och skapar en ny fil, `ResetButton.vue`. Sedan ger du AI:n en precis prompt:

> **Prompt:** "I filen `ResetButton.vue`, skriv koden för en Vue 3-komponent med `<script setup>`. Den ska importera och använda `BaseButton.vue` från `src/shared/ui/`. Knappen ska vara en 'Sekundär Knapp' med texten 'Nollställ'. När man klickar på den ska den emittera en händelse som heter `reset-confirmed`."

*Resultat: En "dum" presentationskomponent som bara kan visa sig själv och signalera en avsikt.*

**Steg 3: Skapa den Granulära Logiken (AI:s uppgift)**

Nu till kärnan i metoden. Du går till `src/features/reset-calculation/model/` och instruerar AI:n att skapa två separata, små filer:

1.  **Fil 1: `getResetState.js`**
    > **Prompt:** "Skapa en ren JavaScript-funktion i filen `getResetState.js`. Funktionen ska heta `getInitialCalculationState` och ska inte ta några argument. Den ska returnera ett objekt med standardvärdena för en beräkning, t.ex. `{ inputA: 0, inputB: 0, result: null }`."
2.  **Fil 2: `useResetAction.js`**
    > **Prompt:** "Skapa en Vue 3 composable i filen `useResetAction.js`. Den ska heta `useResetAction`. Den ska importera den relevanta Pinia-storen (t.ex. `calculationStore`) och funktionen `getInitialCalculationState`. Den ska returnera en enda asynkron funktion som heter `performReset`. När `performReset` anropas ska den anropa `getInitialCalculationState` och sedan uppdatera Pinia-storen med det returnerade objektet."

*Resultat: Du har separerat "vad" (standardvärdena) från "hur" (handlingen att återställa). Varje fil har ett enda, testbart ansvar.*

**Steg 4: Koppla ihop Allt (AI:s uppgift)**

Slutligen går du tillbaka till `ResetButton.vue` och ger en sista, sammankopplande instruktion:

> **Prompt:** "Uppdatera `ResetButton.vue`. Importera `useResetAction` från `../model/useResetAction.js`. Anropa den i `<script setup>` för att få tillgång till `performReset`-funktionen. Ändra klick-hanteraren så att den anropar `performReset` istället för att emittera en händelse."

*Resultat: En fullt fungerande, inkapslad och modulär feature, byggd av små, logiska och AI-vänliga delar.*

**Steg 5: Automatiserad Dokumentation (AI:s uppgift)**

Efter att all kod för en session är levererad och godkänd, avslutas processen med ett sista, obligatoriskt steg. Du instruerar mig att aktivera `AI_Chatt_Avslutningsprotokoll.md`.

> **Prompt:** "Avsluta sessionen och generera artefakterna."

Jag kommer då att analysera alla nya eller ändrade filer och, som en del av den slutgiltiga JSON-artefakten, generera ett `file_metadata_updates`-block. Detta block innehåller en sammanfattning av varje fils syfte och ansvarsområde.

*Resultat: En maskinläsbar logg över alla ändringar skapas. Denna logg används sedan av ett automatiserat GitHub Actions-skript för att uppdatera den centrala kunskapsbasen (`docs/core_file_info.json`), vilket säkerställer att vår projektdokumentation alltid är uppdaterad.*

## Del 3: Hyper-Granularitet i Praktiken

För att ytterligare illustrera kraften i att dela upp logik för AI-interaktion, här är en jämförelse.

**Traditionell Metod (Svårt för AI):**

En enda stor `useCalculation.js`-fil som hanterar allt:
*   Reaktiva variabler för indata.
*   Validering av indata.
*   Beräkningslogik.
*   Formatering av utdata.
*   API-anrop för att spara resultat.

**AI-First Granular Metod (Lätt för AI):**

Fem separata, små filer i `model`-mappen:
1.  `calculationState.js`: Exporterar bara de reaktiva `ref()`-variablerna.
2.  `validateInput.js`: En ren funktion som tar ett värde och returnerar `true` eller `false`.
3.  `computeResult.js`: En ren funktion som tar indata och returnerar ett resultat.
4.  `formatResult.js`: En ren funktion som tar ett resultat och returnerar en formaterad sträng.
5.  `saveResultApi.js`: En funktion som bara innehåller `fetch`-anropet för att spara.

Denna extrema uppdelning är nyckeln. När AI:n gör ett misstag i `validateInput.js`, är det isolerat till just den filen och påverkar inte beräkningslogiken. Du kan ge AI:n en mycket enkel korrigeringsprompt: "Regeln i `validateInput.js` är fel, den ska vara X istället." Detta minimerar risken för oförutsedda sidoeffekter och gör felsökning trivial.
