# scripts/engrove_audio_tools_creator.md
# === SYFTE & ANSVAR ===
# Detta dokument är den primära tekniska referensen för byggskriptet `engrove_audio_tools_creator.py`
# och det webb-UI (`index2.html`) det genererar. Det beskriver arkitektur, dataflöde,
# modulansvar och den underliggande logiken för AI Context Builder-verktyget.
#
# === HISTORIK ===
# * v1.0 (2025-08-17): Initial skapelse.
# * v1.1 (2025-08-17): Lade till sektion 6, "Lärdomar & Felsökningshistorik", för att dokumentera viktiga upptäckter och förhindra regressioner.
# * v2.0 (2025-08-18): (Engrove Mandate) Uppdaterad för att reflektera den nya arkitekturen med en dedikerad `ui_einstein_search.py`-modul och injicering av `core_file_info.json`.
# * SHA256_LF: a8e0d4c7b8e5a6f2b1d3e4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b3c2d5e4
#
# === TILLÄMPADE REGLER (Frankensteen v5.7) ===
# Grundbulten v3.8: Denna dokumentationsfil har uppdaterats för att korrekt reflektera den nya systemarkitekturen.

## 1. Översikt

`engrove_audio_tools_creator.py` är ett Python-baserat kommandoradsverktyg som fungerar som en statisk webbplatsbyggare. Dess enda syfte är att generera `index2.html` – en fristående, interaktiv webbapplikation kallad "AI Context Builder". Applikationen är designad för att låta en användare visuellt inspektera projektets filstruktur, välja relevanta filer och exportera en fokuserad `context.json`-fil för en AI-partner. Den innehåller även en avancerad semantisk sökfunktion ("Einstein").

## 2. Arkitektur & Dataflöde

Verktyget följer ett modulärt och deterministiskt flöde:

1.  **Anrop:** Skriptet anropas av CI/CD-pipelinen (`.github/workflows/ci.yml`) efter att alla metadata-artefakter har genererats.
2.  **Indata:** Det tar emot sökvägarna till fyra kritiska JSON-filer som indata:
    *   `context_bundle.json`: Innehåller hela filstrukturen och partiellt filinnehåll.
    *   `file_relations.json`: Innehåller den analyserade beroendegrafen och filkategorier.
    *   `project_overview.json`: Innehåller grundläggande repo-information.
    *   `core_file_info.json`: Innehåller den kuraterade metadata (syfte, ansvar) för nyckelfiler, används av Einstein.
3.  **Bearbetning:** Skriptet läser in dessa filer, berikar filstrukturen med metadata från relationsgrafen (t.ex. `category`), och transformerar den hierarkiska datan till ett format som är lämpligt för ett träd-UI.
4.  **Sammansättning:** Det importerar HTML, CSS och JavaScript från sina respektive moduler i `scripts/modules/`. Datat (filträdet, kontexten, core_file_info) injiceras i JavaScript-modulerna.
5.  **Utdat:** Skriptet skriver tre filer till output-mappen (`dist/` i CI-kontexten):
    *   `index2.html`: Den sammansatta HTML-strukturen.
    *   `styles.css`: De sammansatta CSS-reglerna.
    *   `logic.js`: De sammansatta och databerikade JavaScript-modulerna.

## 3. Modulbeskrivningar (`scripts/modules/`)

Arkitekturen är starkt beroende av att separera presentation (HTML), stil (CSS) och logik (JS) i diskreta Python-moduler.

*   **`ui_template.py`**: Innehåller `HTML_TEMPLATE`. Detta är HTML-skelettet som definierar DOM-strukturen, inklusive platshållare.
*   **`ui_styles.py`**: Innehåller `CSS_STYLES`. Denna sträng innehåller all CSS för verktyget.
*   **`ui_logic.py`**: Innehåller `JS_LOGIC`. Detta är den generella JavaScript-koden för UI-interaktivitet, inklusive ribbon-menyn, resizer, filmodal och den grundläggande Einstein-söklogiken.
*   **`ui_file_tree.py`**: Innehåller `JS_FILE_TREE_LOGIC`. Specialiserad modul som hanterar all komplex logik för det interaktiva filträdet.
*   **`ui_performance_dashboard.py`**: Innehåller `JS_PERFORMANCE_LOGIC`. Ansvarar för logiken i "AI Performance"-fliken.
*   **`ui_einstein_search.py`**: Innehåller `JS_EINSTEIN_LOGIC`. Ansvarar för att rendera den strukturerade resultatlistan för Einstein-sökningar och hantera dess interaktivitet.

## 4. Detaljerad Funktion (UI & Logik)

### Användargränssnitt

*   **Ribbon Menu:** Huvudnavigeringen, som nu inkluderar en dedikerad "Einstein"-flik med egen sökruta och knapp.
*   **Einstein Container:** En ny, heltäckande vy som aktiveras från ribbon-menyn. Den visar sökresultaten i ett strukturerat, läsbart format.
*   **Vänster Panel:** Innehåller kontrollknappar och filträdet.
*   **Höger Panel:** En kontextkänslig panel för generell information.
*   **Filgranskningsmodal:** En modal som visar filens metadata och innehåll, kan nu även anropas från Einstein-sökresultaten.

### Logik

*   **Initialisering:** `logic.js` initierar alla delsystem, inklusive att rendera filträdet och ladda Einstein-indexet.
*   **Einstein-sökning:** När en sökning utförs i Einstein-fliken anropas `performSemanticSearch` i `ui_logic.py`. Resultaten skickas sedan till `renderEinsteinResults` i `ui_einstein_search.py`, som använder den injicerade `core_file_info`-datan för att berika och rendera resultaten.
*   **Export:** "Exportera"-knappen samlar in ID:na för alla valda filer, konstruerar en `context.json`-fil på klient-sidan och triggar en nedladdning.

## 5. Framtida Utveckling

*   **Prestandaförbättringar:** För mycket stora projekt kan renderingen av filträdet optimeras med "virtual scrolling".
*   **Utökad Analys:** "Kör Analys"-knappen kan kopplas till mer avancerade analyser, som att visualisera beroenden direkt i UI:t baserat på `file_relations.json`.

## 6. Lärdomar & Felsökningshistorik (Rotorsakslogg)

Denna sektion dokumenterar icke-triviala buggar och deras lösningar för att bygga upp en kunskapsbas och undvika att samma misstag upprepas.

### **Incident: UI-krasch vid laddning (JSON Parse-fel)**
*   **Datum:** 2025-08-17
*   **Grundorsak:** En felaktig datainjektionsstrategi. `engrove_audio_tools_creator.py` anropade `json.dumps()` på en redan serialiserad JSON-sträng.
*   **Lösning:** Refaktorering av byggskript och JS-moduler för att injicera ett direkt JavaScript-objekt-literal istället för en sträng som kräver `JSON.parse()`.
*   **Lärdom (Heuristik):** Datainjektion från ett byggskript till klient-JavaScript bör leverera data i sitt slutgiltiga, direkt användbara format.

### **Incident: Trasig layout (Oersatt platshållare)**
*   **Datum:** 2025-08-17
*   **Grundorsak:** En platshållare (`{version}`) introducerades i `modules/ui_template.py`, men byggskriptet uppdaterades inte för att ersätta den.
*   **Lösning:** Uppdatera byggskriptet till att använda `.format(version=...)` på mallsträngen.
*   **Lärdom (Heuristik):** När en platshållare introduceras i en mallfil, måste byggskriptet som konsumerar den uppdateras **atomärt** (i samma commit/åtgärd).
