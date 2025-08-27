# Dokumentation: Engrove Audio Tools Creator
**Version:** 1.0
**Syfte:** Denna fil är den primära tekniska dokumentationen för GUI-verktyget `engrove_audio_tools_creator.py`. Den är genererad av AI-partnern Frankensteen baserat på en fullständig analys av systemets källkod och syftar till att fungera som en central "ground truth" för systemets arkitektur och funktion.

---

## 1. Översikt

`Engrove Audio Tools Creator` är ett specialbyggt, Python-baserat GUI-verktyg som fungerar som en "Integrated Development Environment" (IDE) för att hantera, analysera och paketera instruktionsbuntar (PBF - Protocol Bundle Format) för AI-partnern Frankensteen. Trots sitt namn har verktyget evolverat från sitt ursprungliga syfte och är nu helt fokuserat på att skapa en strukturerad och feltolerant workflow för AI-interaktion.

Applikationen är byggd med **CustomTkinter** och har en modulär arkitektur där varje kärnfunktion är isolerad i sin egen UI-komponent.

## 2. Systemarkitektur

Systemet är uppbyggt kring en central orkestrerare (`engrove_audio_tools_creator.py`) som initierar och sammanfogar olika oberoende UI-moduler. Data och tillståndshantering centraliseras i en logik-modul (`ui_logic.py`) som agerar "controller" och datakälla för UI-komponenterna.

-   **Startpunkt:** `engrove_audio_tools_creator.py`
    -   **Klass:** `App(ctk.CTk)`
    -   **Ansvar:**
        1.  Initierar huvudfönstret.
        2.  Instansierar `UILogic` för att ladda all nödvändig metadata.
        3.  Instansierar och placerar ut varje UI-ram (Frame) från `scripts/modules/`.

## 3. Kärnkomponenter (Moduler)

Varje `.py`-fil i `scripts/modules/` representerar en specifik panel eller funktion i GUI:t.

#### `ui_logic.py` (Hjärnan)
-   **Syfte:** Central logik- och datakontroller.
-   **Funktion:** Laddar och cachar kritiska metadatafiler (`core_file_info.json`, `document_manifest.json`, `session_manifest.json`) vid start. Agerar som den enda källan till sanning för de andra UI-modulerna.

#### `ui_file_tree.py` (Filträd)
-   **Syfte:** Visa en interaktiv trädvy över projektets filstruktur.
-   **Funktion:** Hämtar fildata från `UILogic` och renderar den. Låter användaren välja de filer som ska inkluderas i en PBF-bunt.

#### `ui_protocol_packager.py` (PBF-Paketeraren)
-   **Syfte:** Den kritiska komponenten som skapar de `protocol_bundle_...json`-filer som Frankensteen tar emot.
-   **Funktion:**
    1.  Tar emot en lista med valda filvägar.
    2.  Läser filinnehåll och beräknar `sha256`-hash för varje fil.
    3.  Komprimerar filinnehållet med `zlib`.
    4.  Base64-kodar den komprimerade datan.
    5.  Sammanställer en komplett PBF JSON-struktur, inklusive metadata och payload.
    6.  Beräknar och infogar den slutgiltiga `sha256`-hashen för hela nyttolasten.

#### `ui_einstein_search.py` & `ui_semantic_search.py` (Sök)
-   **Syfte:** Tillhandahålla kraftfulla sökfunktioner över protokollen.
-   **Funktion:**
    -   **Einstein Search:** Strukturerad, indexbaserad sökning.
    -   **Semantic Search:** Vektorbaserad sökning med `sentence-transformers` och `faiss` för att hitta resultat baserat på semantisk likhet.

#### Övriga moduler
-   **`ui_styles.py` & `ui_template.py`:** Hanterar visuell styling och UI-mallar för konsistens.
-   **`data_converter.py`:** Hjälpfunktioner för datatransformering (t.ex. MD till YML).
-   **`ui_core_docs_store.py`:** En panel för att visa information om kärndokument.
-   **`ui_performance_dashboard.py`:** En panel för att visualisera prestandadata.

## 4. Dataflöde (Användarscenario)
1.  **Start:** `engrove_audio_tools_creator.py` exekveras.
2.  **Laddning:** `UILogic` laddar all metadata från projektets JSON-filer.
3.  **Interaktion:** Användaren väljer filer från filträdet och använder sökfunktionerna för att samla in relevant kontext.
4.  **Paketering:** Användaren initierar paketering. `ui_protocol_packager.py` tar emot fillistan och genererar en komplett, signerad och komprimerad `protocol_bundle_...json`-fil.
5.  **Leverans:** Filen är redo att skickas till Frankensteen.

## 5. Beroenden
-   **Python-bibliotek:** `customtkinter`, `pytest`, `sentence-transformers`, `faiss-cpu`. (En fullständig lista finns i `requirements.txt`).
-   **Externa Datafiler:** Applikationens funktion är helt beroende av metadata i `core_file_info.json`, `document_manifest.json`, `session_manifest.json`, m.fl.

## 6. CI/CD Pipeline (`.github/workflows/ci.yml`)
Systemet stöds av en GitHub Actions-pipeline som automatiskt:
1.  **Bygger och testar:** Kör `pytest` och bygger ett associerat (ej inkluderat) Node.js-frontend.
2.  **Säkerhetsskannar:** Använder `Snyk` för att hitta sårbarheter.
3.  **Publicerar Dokumentation:** Bygger och driftsätter dokumentation med `mkdocs`.

## 7. Avskrivna Komponenter
-   `scripts/modules/ui_protocol_packager.js`: Denna JavaScript-baserade paketerare är **avskriven** och används inte längre. All paketeringslogik hanteras nu av den mer kompletta Python-motsvarigheten.*   **`ui_file_tree.py`**: Innehåller `JS_FILE_TREE_LOGIC`. Specialiserad modul som hanterar all komplex logik för det interaktiva filträdet.
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
<!-- END FILE: scripts/engrove_audio_tools_creator.md -->
