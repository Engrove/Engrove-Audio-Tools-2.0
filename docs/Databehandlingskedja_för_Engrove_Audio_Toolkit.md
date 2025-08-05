# docs/Databehandlingskedja_för_Engrove_Audio_Toolkit.md
#
# === SYFTE & ANSVAR ===
# Detta dokument beskriver den automatiserade processen för att bygga, underhålla
# och berika databaserna för pickuper och tonarmar. Det förklarar hela den
# sekventiella kedjan av Python-skript som utgör projektets offline-datapipeline.
#
# === API-KONTRAKT ===
# Inte applicerbart (Styrande dokument).
#
# === HISTORIK ===
# * v1.0 (2025-08-05): Initial skapelse. Konverterad från ett ostrukturerat textdokument
#   till en formell, strukturerad Markdown-fil med korrekt formatering.
# * v2.0 (2025-08-05): Anonymiserade och generaliserade beskrivningen av datainsamlingsprocessen.
#   Tog bort alla specifika referenser till externa datakällor.
#
# === TILLÄMPADE REGLER (Frankensteen v3.7) ===
# - Fullständig kod, alltid: Hela dokumentets innehåll har bevarats och uppdaterats.

# Dokumentation: Databehandlingskedja för Engrove Audio Toolkit

## Översikt

Detta dokument beskriver den automatiserade processen för att bygga, underhålla och berika databaserna för pickuper och tonarmar i Engrove Audio Toolkit. Processen är uppdelad i fyra huvudsakliga steg som körs sekventiellt via en batch-fil, `runme.bat`. Varje steg utförs av ett dedikerat Python-skript och är designat för att säkerställa hög datakvalitet, integritet och robusthet.

**Hela kedjans syfte:** Att omvandla rå, ofta ofullständig data från publika online-källor till en ren, strukturerad, berikad och produktionsklar datamängd.

**Tekniska beroenden:**
*   Python 3.x
*   Python-bibliotek: `pandas`, `scikit-learn`, `google-generativeai`, `beautifulsoup4`, `selenium`, `requests`, `dnspython`, `inputimeout`, `pyautogui`, `rich`

---

## Arbetsflöde: `runme.bat`

Batch-filen `runme.bat` är hjärtat i automatiseringen. Den orkestrerar körningen av de olika Python-skripten i en logisk och nödvändig ordning.

### Flödesbeskrivning:

1.  **ID-korrigering #1 (`id_generator.py`):**
    *   **Syfte:** Säkerställer att källdatafilerna har korrekta, sekventiella ID:n innan någon ny data läggs till. Detta förhindrar ID-konflikter.
2.  **Datainsamling (`run_scraping.py`):**
    *   **Syfte:** Samlar in ny, rå data från offentligt tillgängliga online-arkiv och databaser.
3.  **ID-korrigering #2 (`id_generator.py`):**
    *   **Syfte:** Efter att ny data har lagts till, körs ID-generatorn igen för att integrera de nya posterna och återställa en perfekt, sekventiell ID-ordning.
4.  **AI-berikning (`ai.py --unattended`):**
    *   **Syfte:** Tar den nu uppdaterade och omindexerade datan och skickar den till en AI (Google Gemini) för att fylla i luckor, verifiera fakta, skriva sammanfattningar och klassificera produkter. `--unattended`-flaggan ser till att skriptet körs automatiskt utan användarinteraktion.
5.  **ID-korrigering #3 (`id_generator.py`):**
    *   **Syfte:** Om AI:n har lagt till helt nya poster ("Discovery Mode"), körs ID-generatorn en sista gång för att säkerställa att ID-ordningen är perfekt.
6.  **Slutgiltig Datapreparation (`prepare_data.py`):**
    *   **Syfte:** Detta är det sista och viktigaste steget. Det tar den färdigberikade och ID-korrigerade datan och producerar de slutgiltiga, produktionsklara filerna.

---

## Detaljerad Beskrivning av Skript

### 1. `id_generator.py` (Underhållsverktyg)

*   **Funktion:** Ett robust verktyg för dataintegritet. Det läser specificerade JSON-filer, skapar en säkerhetskopia med tidsstämpel, och skriver sedan om filen där varje objekt har fått ett nytt, sekventiellt ID som börjar på 1.
*   **Nyckelprocesser:**
    *   Skapar automatiskt backup för säkerhet.
    *   Läser in en lista med JSON-objekt.
    *   Itererar och skriver över `id`-fältet för varje objekt.
*   **Roll i kedjan:** Fungerar som ett "städverktyg" mellan huvudstegen för att garantera att databasens primärnycklar (`id`) alltid är konsekventa.

### 2. `run_scraping.py` (Datainsamlare)

*   **Funktion:** Ett avancerat skript för automatiserad datainsamling som interagerar med online-källor för att hämta tekniska specifikationer. Det är designat för att vara ansvarsfullt och robust.
*   **Nyckelprocesser:**
    *   **Proxy-hantering:** Använder anonyma proxyservrar för att distribuera anrop och undvika att överbelasta enskilda källor.
    *   **Tillståndshantering:** Sparar sin status i en `scraping_state.json`-fil, så att den kan återuppta arbetet där den slutade och undvika att hämta samma data igen inom en viss tidsram (TTL).
    *   **Dynamisk Sökning:** Kan automatiskt bryta ner breda sökningar i mer specifika förfrågningar för att hantera källor med begränsningar i sökresultat.
    *   **Datamodellering:** Strukturerar den insamlade rådatan till en preliminär JSON-struktur som är redo för AI-berikning.

### 3. `ai.py` (Databerikare)

*   **Funktion:** Använder en generativ AI-modell (Google Gemini) för att systematiskt förbättra och komplettera den data som samlats in.
*   **Nyckelprocesser:**
    *   **Bearbetningskö:** Identifierar alla poster som ännu inte har bearbetats av AI:n.
    *   **AI-prompter:** Använder sofistikerade, token-optimerade prompter för två huvuduppgifter:
        1.  **Berikning (Enrichment):** Förbättrar en befintlig post genom att verifiera teknisk data, skriva sammanfattningar och klassificera produkten enligt fördefinierade regler.
        2.  **Upptäckt (Discovery):** Upptäcker och skapar helt nya poster för modeller eller tillverkare som saknas i databasen.
    *   **Källhantering:** Anonymiserar automatiskt källor från mindre tillförlitliga domäner (som forum).
    *   **Robust Felhantering:** Har inbyggda återförsök och en "självkorrigerande" prompt som skickas till AI:n om den returnerar felaktig eller ogiltig JSON.
    *   **Kvot-hantering:** Håller reda på API-användning för att inte överskrida API-leverantörens gränser.

### 4. `prepare_data.py` (Slutproducent)

*   **Funktion:** Det sista, sammanslagna master-skriptet som utför all slutgiltig datatransformation och analys.
*   **Nyckelprocesser:**
    1.  **Kopiering & Namnbyte:** Tar de "berikade" filerna och kopierar dem till `output_data`-mappen med rena, produktionsklara filnamn.
    2.  **Skapande av preview-data:** Skapar en lättviktsversion av databaserna, perfekt för utveckling och testning.
    3.  **Datasanering:** Innan analys, körs en robust saneringsfunktion som filtrerar och normaliserar data för att säkerställa tillförlitliga resultat.
    4.  **Regelgenerering:** Använder `RANSACRegressor` (en regressionsmodell som är okänslig för outliers) för att analysera samband i datan och genererar JSON-filer med estimationsregler.
    5.  **Konfidensvalidering:** Kör en "Leave-One-Out" korsvalidering för att testa hur tillförlitliga de genererade reglerna är.
    6.  **Distribution:** Placerar alla färdiga filer i `main`- och `preview`-mapparna.

---

## Slutresultat

Efter att `runme.bat` har slutförts, innehåller mappen `output_data` två kompletta och fristående dataset som är redo att publiceras:

*   `output_data/main/`: Den fullständiga, produktionsklara datan för Engrove Audio Toolkit.
*   `output_data/preview/`: En identiskt strukturerad men mycket mindre version, idealisk för snabb utveckling.
