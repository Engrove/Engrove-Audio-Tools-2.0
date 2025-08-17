# scripts/engrove_audio_tools_creator.md
# === SYFTE & ANSVAR ===
# Detta dokument är den primära tekniska referensen för byggskriptet `engrove_audio_tools_creator.py`
# och det webb-UI (`index2.html`) det genererar. Det beskriver arkitektur, dataflöde,
# modulansvar och den underliggande logiken för AI Context Builder-verktyget.
#
# === HISTORIK ===
# * v1.0 (2025-08-17): Initial skapelse.
#
# === TILLÄMPADE REGLER (Frankensteen v5.6) ===
# Grundbulten v3.4: Hela filen har genererats enligt gällande protokoll.

## 1. Översikt

`engrove_audio_tools_creator.py` är ett Python-baserat kommandoradsverktyg som fungerar som en statisk webbplatsbyggare. Dess enda syfte är att generera `index2.html` – en fristående, interaktiv webbapplikation kallad "AI Context Builder". Applikationen är designad för att låta en användare visuellt inspektera projektets filstruktur, välja relevanta filer och exportera en fokuserad `context.json`-fil för en AI-partner.

## 2. Arkitektur & Dataflöde

Verktyget följer ett modulärt och deterministiskt flöde:

1.  **Anrop:** Skriptet anropas av CI/CD-pipelinen (`.github/workflows/ci.yml`) efter att alla metadata-artefakter har genererats.
2.  **Indata:** Det tar emot sökvägarna till tre kritiska JSON-filer som indata:
    *   `context_bundle.json`: Innehåller hela filstrukturen och partiellt filinnehåll.
    *   `file_relations.json`: Innehåller den analyserade beroendegrafen och filkategorier.
    *   `project_overview.json`: Innehåller grundläggande repo-information.
3.  **Bearbetning:** Skriptet läser in dessa filer, berikar filstrukturen med metadata från relationsgrafen (t.ex. `category`), och transformerar den hierarkiska datan till ett format som är lämpligt för ett träd-UI.
4.  **Sammansättning:** Det importerar HTML, CSS och JavaScript från sina respektive moduler i `scripts/modules/`. Datat (filträdet, kontexten) injiceras i JavaScript-modulerna.
5.  **Utdat:** Skriptet skriver tre filer till output-mappen (`dist/` i CI-kontexten):
    *   `index2.html`: Den sammansatta HTML-strukturen.
    *   `styles.css`: De sammansatta CSS-reglerna.
    *   `logic.js`: De sammansatta och databerikade JavaScript-modulerna.

## 3. Modulbeskrivningar (`scripts/modules/`)

Arkitekturen är starkt beroende av att separera presentation (HTML), stil (CSS) och logik (JS) i diskreta Python-moduler.

*   **`ui_template.py`**: Innehåller en enda Python-strängvariabel, `HTML_TEMPLATE`. Detta är HTML-skelettet för `index2.html`. Den definierar DOM-strukturen, inklusive platshållare för UI-element som kommer att hanteras av JavaScript.
*   **`ui_styles.py`**: Innehåller `CSS_STYLES`-variabeln. Denna sträng innehåller all CSS för verktyget, från layout och design-tokens till specifika stilar för komponenter som filträdet och modalen.
*   **`ui_logic.py`**: Innehåller `JS_LOGIC`. Detta är den generella JavaScript-koden för UI-interaktivitet. Ansvarsområden inkluderar:
    *   Hantering av "Ribbon"-menyn (flikbyten).
    *   Logik för den justerbara panel-delaren (resizer).
    *   Funktionalitet för filgranskningsmodalen, inklusive att hämta filinnehåll från GitHub vid behov.
*   **`ui_file_tree.py`**: Innehåller `JS_FILE_TREE_LOGIC`. Denna modul är specialiserad och hanterar all komplex logik för det interaktiva filträdet:
    *   Rendering av den hierarkiska trädstrukturen från JSON-data.
    *   Hantering av tri-state-kryssrutor (av, på, delvis vald).
    *   Logik för att expandera/kollapsa mappar.
    *   Klickhändelser på filnamn för att öppna granskningsmodalen.
*   **`ui_performance_dashboard.py`**: Innehåller `JS_PERFORMANCE_LOGIC`. Denna modul ansvarar för logiken i "AI Performance"-fliken. Den hanterar rendering av diagram (via Chart.js) och tabeller baserat på `ai_protocol_performance.json`.

## 4. Detaljerad Funktion (UI & Logik)

### Användargränssnitt

*   **Ribbon Menu:** Huvudnavigeringen, som låter användaren växla mellan "Verktyg", "AI Performance", etc.
*   **Vänster Panel:** Innehåller kontrollknappar (`Kör Analys`, `Exportera`) och själva filträdet.
*   **Filträd:** Den primära komponenten för filval. Varje nod (fil/mapp) har en kryssruta och visar sin storlek.
*   **Höger Panel:** En kontextkänslig panel som visar information eller verktyg baserat på valet i ribbon-menyn.
*   **Resizer:** En dragbar avdelare mellan vänster och höger panel.
*   **Filgranskningsmodal:** En modal som visas när en fil klickas. Den visar filens metadata och innehåll.

### Logik

*   **Initialisering:** När `logic.js` körs, parsar den den injicerade JSON-datan och använder `ui_file_tree.py`-logiken för att bygga och rendera filträdet i DOM.
*   **Interaktivitet:** All interaktivitet (klick, drag) hanteras av event-lyssnare som definieras i `ui_logic.py` och `ui_file_tree.py`.
*   **Export:** "Exportera"-knappen samlar in ID:na för alla valda filer, konstruerar en `context.json`-fil på klient-sidan och triggar en nedladdning.

## 5. Framtida Utveckling

*   **Prestandaförbättringar:** För mycket stora projekt kan renderingen av filträdet optimeras med "virtual scrolling".
*   **Utökad Analys:** "Kör Analys"-knappen kan kopplas till mer avancerade analyser, som att visualisera beroenden direkt i UI:t baserat på `file_relations.json`.
*   **State Management:** För mer komplexa verktyg kan en lättvikts state management-lösning (liknande Pinia, men i ren JS) implementeras för att hantera UI-tillstånd mer robust.
