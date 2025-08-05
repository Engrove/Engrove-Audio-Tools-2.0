# docs/Teknisk_Beskrivning_Engrove_Audio_Toolkit.md
#
# === SYFTE & ANSVAR ===
# Detta dokument tillhandahåller en komplett teknisk beskrivning av projektet.
# Det fungerar som en grundinstruktion för att förstå den valda teknikstacken,
# arkitekturen, och den bakomliggande databehandlingskedjan.
#
# === API-KONTRAKT ===
# Inte applicerbart (Styrande dokument).
#
# === HISTORIK ===
# * v1.0 (2025-08-05): Initial skapelse. Konverterad från ett ostrukturerat textdokument
#   till en formell, strukturerad Markdown-fil med korrekt formatering för rubriker,
#   listor och kodtermer.
#
# === TILLÄMPADE REGLER (Frankensteen v3.7) ===
# - Fullständig kod, alltid: Hela dokumentets innehåll har bevarats och konverterats.

# Teknisk Beskrivning: Engrove Audio Toolkit

Projektet är en modern, statisk webbapplikation (Static Site Generation - SSG) byggd med ett komponentbaserat JavaScript-ramverk. Arkitekturen är designad för snabb prestanda, enkelt underhåll och kostnadseffektiv driftsättning på plattformar för statiska webbplatser.

## 1. Grundläggande Frontend-stack

Grunden för hela applikationen bygger på moderna och populära frontend-tekniker.

### Byggverktyg och Utvecklingsmiljö: `Vite`

*   **Vad det är:** `Vite` är ett blixtsnabbt byggverktyg som hanterar utvecklingsservern (`npm run dev`) och den slutgiltiga produktions-builden (`npm run build`).
*   **Varför det används:** Till skillnad från äldre verktyg använder Vite sig av webbläsarens inbyggda stöd för ES-moduler under utveckling, vilket leder till nästan omedelbar start och uppdatering av servern (Hot Module Replacement).
*   **Konfiguration:** Projektets Vite-konfiguration hittas i `vite.config.js`. Filen `package.json` definierar skripten som startar Vite.

### JavaScript-ramverk: `Vue.js 3`

*   **Vad det är:** Applikationens logik och gränssnitt är byggt med `Vue.js` (specifikt version 3).
*   **Varför det används:** Vue 3 möjliggör en reaktiv och komponentbaserad arkitektur. Filerna visar användning av Composition API med `<script setup>`, vilket är den moderna standarden för att skriva organiserad och återanvändbar Vue-kod.
*   **Struktur:** Applikationen är uppdelad i återanvändbara `.vue`-filer (Single-File Components) som `InputPanel.vue`, `ResultsPanel.vue`, etc. Varje fil innehåller sin egen HTML-mall, JavaScript-logik och CSS-stilar.

### Routing (Navigering): `Vue Router`

*   **Vad det är:** För att hantera navigering mellan de olika "sidorna" (Home, Resonance Calculator, Data Explorer) används den officiella `vue-router`-biblioteket.
*   **Hur det fungerar:** Routern mappar URL-sökvägar (t.ex. `/data-explorer`) till specifika Vue-komponenter (`DataExplorerView.vue`). Detta skapar en snabb Single-Page Application (SPA) där sidbyten sker direkt i webbläsaren utan att ladda om hela sidan.

### Statushantering (State Management): `Pinia`

*   **Vad det är:** `Pinia` är det officiella biblioteket för centraliserad datahantering i Vue.
*   **Varför det används:** I ett projekt med flera interaktiva komponenter, som kalkylatorerna, behövs ett sätt att dela och synkronisera data (t.ex. användarens inmatningar och beräknade resultat) mellan dem. Pinia-"stores" (som `tonearmStore.js` och `estimatorStore.js`) fungerar som en central "sanningskälla" för hela applikationen.
*   **Extra funktionalitet:** Projektet använder `pinia-plugin-persistedstate` för att automatiskt spara användarens inmatningar i webbläsarens `localStorage`. Detta gör att värdena finns kvar även om användaren stänger och öppnar fliken igen.

## 2. Datahantering och Visualisering

En stor del av projektet handlar om att presentera och bearbeta data.

### Datakällor: Statiska JSON-filer

*   **Arkitektur:** All primärdata för tonarmar (`tonearm_data.json`) och pickuper (`pickup_data.json`) lagras som statiska JSON-filer i `/public/data`-mappen. Applikationen hämtar dessa filer vid start. Detta är en typisk och effektiv metod för statiska webbplatser, då ingen databas behövs.

### Datavisualisering: `Chart.js`

*   **Vad det är:** Alla diagram och grafer i projektet (resonanskurvor, spårfelsgrafer etc.) renderas med hjälp av biblioteket `Chart.js`.
*   **Implementation:** Vue-komponenter som `TrackingErrorChart.vue` agerar som "wrappers" kring en `<canvas>`-tagg och använder `Chart.js` för att rita upp datan som skickas in som `props`.
*   **Plugin:** `chartjs-plugin-annotation` används specifikt för att rita de färgade "ideal/varning/fara"-zonerna i bakgrunden på vissa diagram.

### Innehållshantering: `Markdown`

*   **Vad det är:** Förklarande texter och guider (som i `src/content/tonearmResonance.md`) skrivs i Markdown-format.
*   **Implementation:** Med hjälp av `vite-plugin-markdown` kan `.md`-filerna importeras direkt in i Vue-komponenter som HTML, vilket gör det mycket enkelt att underhålla längre textinnehåll utan att blanda in det i komponentens logik.

## 3. Dataanalys (Offline-process)

En unik och avancerad del av projektet är hur estimationsreglerna för "Compliance Estimator" skapas. Detta sker inte i realtid i webbläsaren.

### Teknik: Python-skript

*   **Bibliotek:** Skripten (`scripts/generate_rules.py` och `scripts/generate_static_rules.py`) använder `pandas` för datamanipulation och `scikit-learn` för att utföra linjär regression.

### Process:

1.  Ett Python-skript körs manuellt av utvecklaren.
2.  Skriptet läser in `pickup_data.json`.
3.  Det utför statistisk analys och regressionsmodellering på datan för att hitta korrelationer mellan t.ex. 100Hz och 10Hz compliance.
4.  Resultaten (regressionskoefficienter, R²-värden, etc.) sparas som nya, färdigberäknade JSON-filer (`estimation_rules.json`).
5.  Vue-applikationen laddar sedan dessa färdiga regel-filer och använder dem för att göra sina estimeringar, vilket är extremt snabbt för slutanvändaren.

## 4. Bygge, Testning och Driftsättning (DevOps)

### Beroendehantering:

*   Projektet använder `Node.js` och `npm` (Node Package Manager) för att hantera alla bibliotek och beroenden som listas i `package.json`.

### Testning:

*   `Vitest` används som testramverk. Det är ett modernt testverktyg som är byggt för att fungera sömlöst med Vite. `jsdom` används för att simulera en webbläsarmiljö så att tester kan köras i terminalen.

### Driftsättning (Deployment):

*   **Plattformar:** Webbplatsen driftsätts på `Netlify` och `Cloudflare Pages`.
*   **Konfiguration:** `netlify.toml` och `wrangler.toml` innehåller de specifika instruktionerna för varje plattform.
*   **Manuell Bygg-trigger:** En mekanism har implementerats där en ny build-process endast startas när filen `buildtrigger.txt` ändras. Detta konfigureras med ett `git diff`-kommando.

## Sammanfattning & Grundinstruktion för ett Eget Projekt

För att starta ett liknande projekt behöver du:
1.  Installera `Node.js` och `npm`.
2.  Välj `Vite` som byggverktyg: `npm create vite@latest my-project -- --template vue`
3.  Installera kärnbiblioteken: `npm install vue-router pinia chart.js chartjs-plugin-annotation`
4.  Strukturera projektet:
    *   Skapa en `/src/views`-mapp för dina sidkomponenter.
    *   Skapa en `/src/components`-mapp för återanvändbara komponenter.
    *   Skapa en `/src/store`-mapp för dina `Pinia`-stores.
    *   Lägg statisk data (JSON) i `/public/data`.
5.  Sätt upp `Vue Router` för att hantera navigering mellan dina vyer.
6.  Skapa `Pinia`-stores för att hantera den globala datan.
7.  Bygg komponenter med `Vue 3`:s Composition API (`<script setup>`).
8.  (Valfritt) Skapa separata `Python`-skript för tung dataanalys som kan köras offline.
