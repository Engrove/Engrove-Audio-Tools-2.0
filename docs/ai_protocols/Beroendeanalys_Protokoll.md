# docs/ai_protocols/Beroendeanalys_Protokoll.md
#
# === SYFTE & ANSVAR ===
# Detta dokument definierar det obligatoriska protokollet för att analysera och
# godkänna nya externa beroenden (t.ex. npm-paket) innan de får
# implementeras i projektet.
#
# === HISTORIK ===
# * v1.0 (2025-08-06): Initial skapelse. Extraherad från den monolitiska AI.md
#   som en del av "Operation: Modulär Instruktion".

### PROTOKOLL FÖR NYA BEROENDEN OCH VERKTYG
------------------------------------------------------
När en uppgift kräver införandet av ett nytt externt bibliotek eller verktyg (ett nytt `npm`-paket) ska detta protokoll följas. Ingen kod som använder det nya beroendet får skrivas innan denna analys har presenterats och godkänts av dig.

**1. Krav på Beroendeanalys:**
   * Innan jag föreslår ett specifikt paket i min plan, kommer jag att genomföra och presentera en koncis "Beroendeanalys".
   * Analysen kommer om möjligt att jämföra 1-3 populära alternativ.

**2. Kriterier för Analys:**
   * Varje potentiellt beroende kommer att utvärderas enligt följande punkter:
      1.  **Problemlösning:** Hur väl och direkt löser paketet det specifika problemet?
      2.  **Underhåll och Aktivitet:** Är paketet aktivt underhållet? (Senaste commit, öppet/stängt issue-förhållande, community-aktivitet).
      3.  **Popularitet och Ekosystem:** Hur väletablerat är paketet? (npm-nedladdningar, GitHub-stjärnor, tillgång till guider och support).
      4.  **Paketstorlek och Prestanda:** Vad är dess påverkan på den slutgiltiga applikationens storlek och prestanda? (Jag kommer att referera till verktyg som Bundlephobia).
      5.  **Beroendeträd:** Drar paketet med sig ett stort antal egna beroenden som ökar komplexiteten och attackytan?
      6.  **Dokumentation och TypeScript-stöd:** Är dokumentationen tydlig och komplett? Finns förstklassiga TypeScript-typer?
      7.  **Licens:** Är licensen (t.ex. MIT, ISC, Apache 2.0) kompatibel med projektets behov?

**3. Presentation och Godkännande:**
   * Resultatet presenteras som en del av min **"Plan"**.
   * Analysen avslutas med en rekommendation.
   * Först efter ditt godkännande av både planen och valet av beroende kommer jag att lägga till paketet i `package.json` och påbörja implementationen.
