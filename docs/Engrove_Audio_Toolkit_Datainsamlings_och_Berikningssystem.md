# docs/Engrove_Audio_Toolkit_Datainsamlings_och_Berikningssystem.md
#
# === SYFTE & ANSVAR ===
# Detta dokument beskriver den automatiserade pipeline som är designad för att
# bygga, underhålla och berika databasen för Hi-Fi-utrustning (pickuper och tonarmar).
# Det förklarar arkitektur, dataflöde och komponentbeskrivningar för systemets
# Python-skript.
#
# === API-KONTRAKT ===
# Inte applicerbart (Styrande dokument).
#
# === HISTORIK ===
# * v1.0 (2025-08-06): Initial skapelse. Konverterad från ett ostrukturerat textdokument
#   till en formell, strukturerad Markdown-fil med korrekt formatering.
# * v2.0 (2025-08-06): Anonymiserade och generaliserade beskrivningen av datainsamlingsprocessen.
#   Tog bort alla specifika referenser till externa datakällor.
#
# === TILLÄMPADE REGLER (Frankensteen v3.8) ===
# - Fullständig kod, alltid: Hela dokumentets innehåll har bevarats och konverterats.

# Master-dokumentation: Engrove Audio Toolkit - Datainsamlings- & Berikningssystem
Dokumentversion: 1.0
Senast uppdaterad: 2025-08-01

## 1. Systemöversikt

### 1.1 Syfte

Detta system är en automatiserad pipeline designad för att bygga, underhålla och berika en högkvalitativ databas över Hi-Fi-utrustning, specifikt pickuper och tonarmar. Målet är att transformera rå, ofta ofullständig data från publika källor till en strukturerad, validerad och internt konsekvent datamängd som kan driva webbapplikationen "Engrove Audio Toolkit".

Systemet är byggt för att vara robust, självsanerande och delvis autonomt, med hjälp av en kombination av datainsamling från online-källor, statistisk analys och interaktion med en avancerad språkmodell (AI).

### 1.2 Arkitektur och Dataflöde

Systemet består av fyra huvudsakliga Python-skript som exekveras i en specifik sekvens, styrd av `runme.bat`. Dataflödet är enkelriktat och varje steg bygger vidare på resultatet från det föregående.

**Exekveringsordning (`runme.bat`):**

1.  `id_generator.py` (Pre-Sanity Check): Säkerställer att befintliga datafiler har korrekta, sekventiella ID:n innan ny data läggs till.
2.  `run_scraping.py` (Datainsamling): Samlar in ny, rå data från offentligt tillgängliga online-arkiv och databaser.
3.  `id_generator.py` (Post-Datainsamlings ID-fix): Omindexerar filerna igen för att inkludera de nyligen tillagda posterna.
4.  `ai_9.6.py` (AI-Berikning & Validering): Systemets "hjärna". Använder Google Gemini API för att validera, korrigera och komplettera data. Innehåller även logik för lokal datasanering och statistisk estimering.
5.  `id_generator.py` (Post-AI ID-fix): En sista omindexering för att hantera eventuella nya poster skapade av AI:ns "Discovery Mode".
6.  `prepare_data.py` (Analys & Regelgenerering): Slutsteget. Analyserar den nu berikade datan för att generera statistiska modeller och förbereder slutgiltiga datafiler för webbapplikationen.

**Visuellt Dataflöde:**
Rådata från online-källor -> `run_scraping.py` -> `pickup/tonearm_data_enriched.json` (råformat) -> `ai_9.6.py` -> `pickup/tonearm_data_enriched.json` (berikad & validerad) -> `prepare_data.py` -> `output_data/` (slutgiltiga filer för webbapp). `id_generator.py` säkerställer ID-integritet mellan stegen.

## 2. Komponentbeskrivningar

### 2.1 `run_scraping.py` - Datainsamlingsmodulen

*   **Syfte:** Att automatiskt samla in ny, rå data om pickuper och tonarmar från offentligt tillgängliga online-arkiv och databaser.
*   **Teknik:** Interagerar med online-källor för att hämta tekniska specifikationer. Det är designat för att vara ansvarsfullt och robust i sin datahämtning.
*   **Nyckelfunktionalitet:**
    *   **Proxy-hantering:** Använder anonyma proxyservrar för att distribuera anrop och undvika att överbelasta enskilda källor.
    *   **Tillståndshantering:** Sparar sin status i en `scraping_state.json`-fil, så att den kan återuppta arbetet där den slutade och undvika att hämta samma data igen inom en viss tidsram (TTL).
    *   **Dynamisk Sökning:** Kan automatiskt bryta ner breda sökningar i mer specifika förfrågningar för att hantera källor med begränsningar i sökresultat.
    *   **Datamodell-skapande:** Strukturerar den insamlade rådatan till en preliminär JSON-struktur som är redo för AI-berikning.
*   **Output:** Uppdaterar `public/data/pickup_data_enriched.json` och `public/data/tonearm_data_enriched.json` med nya, råa poster.

### 2.2 `id_generator.py` - ID-Vaktmästaren

*   **Syfte:** Att säkerställa dataintegriteten genom att garantera att varje objekt i en JSON-fil har ett unikt och perfekt sekventiellt ID som börjar på 1.
*   **Teknik:** Grundläggande filhantering och JSON-bearbetning.
*   **Nyckelfunktionalitet:**
    *   **Säkerhetskopiering:** Skapar alltid en tidsstämplad backup av originalfilen innan några ändringar görs.
    *   **Omindexering:** Läser in hela listan av objekt, itererar igenom den och skriver över `id`-fältet med ett nytt, inkrementellt värde.
*   **Output:** Skriver över de angivna JSON-filerna med den omindexerade versionen.

### 2.3 `ai_9.6.py` - AI-Berikaren & Valideraren

*   **Syfte:** Att agera som systemets intelligenta kärna. Den validerar, korrigerar, kompletterar och utökar den råa datan från datainsamlingssteget.
*   **Teknik:** Interagerar med Google Gemini API via strategiskt utformade prompter. Använder `rich`-biblioteket för en interaktiv terminal-UI.
*   **Nyckelfunktionalitet:**
    *   **Datasanering vid Start:** Vid inläsning saneras all data. Felaktiga datatyper (t.ex. `stylus_family: false`) korrigeras automatiskt till `null`.
    *   **Migrering av Datamodell:** Ett gammalt `edit_history`-format konverteras automatiskt till det nya, mer strukturerade formatet.
    *   **Lokal Compliance-estimering:** Innan AI-anrop görs, försöker skriptet att lokalt beräkna saknad `cu_dynamic_10hz`-data med hjälp av de statistiska reglerna från `prepare_data.py`.
    *   **"Pre-flight Check":** Undviker onödiga och kostsamma API-anrop för datafattiga objekt som saknar bra käll-URL:er.
    *   **Robust API-hantering:** Hanterar ett brett spektrum av API-fel, inklusive tomma svar, och gör automatiska återförsök med korrigerande prompter.
    *   **Strikt Validering:** Validerar alla svar från AI:n mot en uppsättning regler (korrekta klassificerings-ID:n, logiska intervall, etc.).
    *   **Geometrisk Korrigering:** Både instruerar AI:n och har en egen intern funktion för att tvinga fram matematiskt korrekt tonarmsgeometri enligt en fastställd regelhierarki.
    *   **Självlärande Klassificering:** Kan automatiskt lägga till nya, giltiga klassificerings-ID:n om AI:n upprepade gånger föreslår ett nytt, konsekvent värde.
    *   **Rå-loggning:** Sparar varje exakt prompt och rått svar till `script_log_raw.txt` för djupgående felsökning.
*   **Output:** Skriver över `pickup_data_enriched.json` och `tonearm_data_enriched.json` med den berikade och validerade datan.

### 2.4 `prepare_data.py` - Analytikern & Publicisten

*   **Syfte:** Att utföra den slutgiltiga analysen av den berikade datan och generera de filer som webbapplikationen direkt konsumerar.
*   **Teknik:** Använder `pandas` för dataanalys och `scikit-learn` för statistisk modellering (`RANSAC-regression`).
*   **Nyckelfunktionalitet:**
    *   **Datatransformering:** Konverterar JSON-data till Pandas DataFrames för effektiv analys.
    *   **Regressionsanalys:** Använder RANSAC-algoritmen för att hitta robusta linjära samband mellan olika typer av compliance-data, och ignorerar outliers.
    *   **Regelgenerering:** Skapar `pickups-estimation-rules.json` och `pickups-static-estimation-rules.json` baserat på regressionsanalysen. Dessa filer används sedan av `ai_9.6.py` och webbapplikationen.
    *   **Korsvalidering:** Utför "Leave-One-Out"-korsvalidering för att beräkna och spara konfidensnivåer för de olika estimationsreglerna i `pickups-confidence-levels.json`.
    *   **Distribution:** Kopierar och (om nödvändigt) förkortar alla relevanta datafiler till en `output_data`-mapp, redo för publicering.
*   **Output:** Skapar och fyller `output_data/`-mappen med alla filer som behövs för webbapplikationen.

### 2.5 `marker_generator_engrove.py` - Verktyget

*   **Syfte:** Ett fristående verktyg för att generera de AR-markörer (som QR-koder) som används i ett annat projekt.
*   **Teknik:** Använder `Pillow` (PIL) för att programmatiskt skapa och rita bilder.
*   **Nyckelfunktionalitet:**
    *   Genererar olika typer av markörer (kalibrering, ankare, spindel, etc.) i specificerade storlekar.
    *   Ritar komplexa mönster som schackbräden och lägger till text och ramar.
*   **Output:** Sparar PNG-bilder i `markers/`-mappen.

## 3. Revisionslogg för Funktionalitet

Detta avsnitt spårar utvecklingen av systemets kärnfunktionalitet.

*   **v1.0 (Initial):**
    *   Grundläggande datainsamling med `run_scraping.py`.
    *   Enkel AI-berikning med en tidig version av `ai.py`.
*   **v2.0 (Dataintegritet):**
    *   `id_generator.py` introduceras för att lösa problem med inkonsekventa ID:n.
    *   `run_scraping.py` (v4.1) får en striktare datamodell för att säkerställa att alla nödvändiga fält skapas från början.
*   **v3.0 (Statistisk Modellering):**
    *   `prepare_data.py` skapas. Introducerar RANSAC-regression för att skapa de första estimationsreglerna och konfidensnivåerna.
*   **v4.0 (Avancerad AI & Robusthet):**
    *   `ai.py` (v9.0-9.1) genomgår en stor uppgradering.
    *   **Lokal Compliance-estimering:** Skriptet lär sig att använda reglerna från `prepare_data.py` för att fylla i data lokalt.
    *   **Självlärande Klassificering:** Mekanism för att automatiskt uppdatera `classifications.json` baserat på återkommande, okända värden från AI:n.
    *   **Validering:** Interna funktioner för att validera datatyper, logiska intervall och tonarmsgeometri introduceras.
*   **v5.0 (Felsökning & Optimering):**
    *   `ai.py` uppgraderas till v9.5/9.6.
    *   **Rå-loggning:** `script_log_raw.txt` introduceras för fullständig transparens i AI-kommunikationen.
    *   **Datasanering vid Start:** Skriptet börjar aktivt sanera och migrera gammal data vid varje körning.
    *   **"Pre-flight Check":** En mekanism för att undvika onödiga API-anrop implementeras för att spara kostnader och tid.
    *   **Förstärkt API-hantering:** Logiken för att hantera API-svar görs mer robust för att klara av tomma eller oväntade svar.
    *   **Strikt Geometrisk Korrigering:** Den tidigare "gissningsbaserade" geometrikorrigeringen ersätts med en strikt, deterministisk regelhierarki.```
