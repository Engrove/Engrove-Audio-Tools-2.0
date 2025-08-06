# docs/ai_protocols/Levande_Kontext_Protokoll.md
#
# === SYFTE & ANSVAR ===
# Detta dokument definierar "Levande Kontext"-protokollet, ett sessionsbaserat
# versionshanteringssystem för filer som ändras under en chatt. Det ger
# spårbarhet, reversibilitet och en otvetydig "sanningskälla" för den
# aktiva kodbasen under sessionens gång.
#
# === HISTORIK ===
# * v1.0 (2025-08-06): Initialt förslag för att lösa kontextdrift.
# * v2.0 (2025-08-06): Uppgraderad till ett komplett versionshanteringssystem
#   baserat på feedback från Engrove. Inkluderar nu versionering,
#   revisionsbeskrivningar och kommandon för att återgå och granska historik.

### EXTRA PROTOKOLL: "LEVANDE KONTEXT" (Version 2.0)
----------------------------------------------------------------
**Syfte:** Att eliminera kontextdrift genom att implementera ett sessionsbaserat versionshanteringssystem för filer som ändras. Detta ger full spårbarhet, möjlighet att återgå till tidigare versioner, och en otvetydig "sanningskälla" för den aktiva kodbasen under sessionens gång.

**Initialt Tillstånd:**
Vid starten av varje session är kontext-versionen `v0`, vilket representerar den exakta koden från den initiala JSON-filen.

**Kommandon:**

**1. `Uppdatera levande kontext: [Kort beskrivning av ändringen]`**
   *   **Funktion:** Detta är "commit"-kommandot. Det instruerar mig att ta den senaste filen jag levererade, spara den som en ny version i min interna historik, och öka versionsnumret (`+1`). Beskrivningen du anger blir "commit-meddelandet".
   *   **Exempel:** `Uppdatera levande kontext: Lade till BaseMultiSelect för kategorifilter.`

**2. `Återgå till kontext version [nummer]`**
   *   **Funktion:** Detta är "checkout"-kommandot. Det instruerar mig att ändra min aktiva pekare till en specifik, tidigare version från historiken. All efterföljande kodgenerering kommer att baseras på den återställda versionen.
   *   **Exempel:** `Återgå till kontext version 1`

**3. `Visa kontext-historik`**
   *   **Funktion:** Detta är "log"-kommandot. Det instruerar mig att skriva ut en sammanfattning av den interna kontext-historiken för den aktuella sessionen, inklusive version, beskrivning och vilken som är aktiv.
   *   **Exempel:** `Visa kontext-historik`

**Mina Svar:**

*   **Efter `Uppdatera`:**
    > `"Bekräftat. Kontext uppdaterad till v2: 'Justerade marginaler i header'. Detta är nu den aktiva versionen."`

*   **Efter `Återgå`:**
    > `"Bekräftat. Har återgått till kontext v1: 'Lade till BaseMultiSelect...'. Detta är nu den aktiva versionen."`

*   **Efter `Visa`:**
    > ```markdown
    > ### Kontext-historik för Sessionen
    >
    > *   v0: Initial kontext från start-JSON.
    > *   **v1: Lade till BaseMultiSelect... (AKTIV)**
    > *   v2: Justerade marginaler i header.
    > ```
