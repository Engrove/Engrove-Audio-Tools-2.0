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
*   `full_instruction_preview` (String): En textrepresentation av den fullständiga, fristående AI-instruktionen som skapades i punkt 5 av Brainstorming_Protokoll.md. Denna text måste innehålla en fullständig och djupt detaljerad uppdragsbeskrivning, inklusive tekniska analyser och implementation-detaljer för varje delmoment, i enlighet med de skärpta kraven i brainstorming-protokollet. Detta ger en mänsklig förhandsgranskning av hela den verifierade uppgiften.
*   `filesToSelect` (Array of Strings): En komplett, platt lista med de relativa sökvägarna till **alla** filer som identifierats som nödvändiga (källkod, externa filer, styrdokument). Detta är nyckeln som AI Context Builder-verktyget använder för att automatiskt markera kryssrutorna.
*   `notes` (String, Optional): En valfri sträng för extra anteckningar eller påminnelser inför nästa session, t.ex. "Fokusera på felhanteringen i `fetchData.js`" eller "Kom ihåg att uppdatera versionsnumret i `package.json`".

**Exempel på genererad JSON:**

```json
{
  "task_summary": "Implement new file preview modal in the AI Context Builder.",
  "full_instruction_preview": "Idé: Implementera en modal för förhandsgranskning av filer i AI Context Builder. Plan: 1. Uppdatera HTML-strukturen i `wrap_json_in_html.py` med en dold modal-komponent. 2. Skriv JavaScript-logik för att fånga klick på filnamn. 3. Implementera `fetch` för att hämta filinnehåll från GitHub. 4. Visa bild- eller textinnehåll i modalen. 5. Styla modalen enligt UI-standard.",
  "filesToSelect": [
    "scripts/wrap_json_in_html.py",
    "docs/Global_UI-Standard_Komponentspecifikation.md"
  ],
  "notes": "Ensure the modal is fully responsive and handles both image and text files gracefully."
}
