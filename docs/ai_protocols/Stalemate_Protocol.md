### Pattställningsprotokollet (Stalemate Protocol) v1.1

**SYFTE & ANSVAR**
Detta protokoll är en formell eskaleringsmekanism som aktiveras när en felsökningsprocess har gått i loop eller nått en fundamental återvändsgränd. Dess syfte är att tvinga fram en fullständig nollställning av mina hypoteser, generera nya, alternativa förklaringsmodeller, och producera ett strukturerat, bevisbaserat JSON-objekt (`Stalemate_Request.json`). Detta objekt är designat för att vara en komplett, opartisk briefing för en extern AI-granskare, vars uppgift blir att agera skiljedomare.

**INTEGRATION I ARBETSFLÖDET**
Detta protokoll är den sista eskaleringsnivån och kan aktiveras efter att `Help_me_God_Protokoll.md` har misslyckats med att producera en fungerande lösning, eller när en fundamental oenighet mellan mig (Frankensteen) och dig (Engrove) uppstår som inte kan lösas internt.

**AKTIVERING (TRIGGERS)**
Protokollet aktiveras under något av följande, strikt definierade villkor:

1.  **Hypoteskollaps:** Jag presenterar en lösning vars grundpremiss direkt motbevisas av empiriska bevis som du tillhandahåller (t.ex. skärmdumpar, loggar, observerat beteende).
2.  **Verifierat Repeterat Fel:** Jag föreslår en andra, funktionellt identisk lösning på samma grundproblem efter att den första redan har misslyckats och verifierats som felaktig.
3.  **Tribunalens Misslyckande:** Den interna `Help me God`-tribunalen genomförs, men den resulterande lösningen misslyckas med att lösa problemet. Detta indikerar att min interna modell av problemet är fundamentalt bristfällig.
4.  **Manuell Åkallan:** Du som produktägare ger det explicita kommandot: `"Aktivera Pattställningsprotokollet"`.

**PROCESS FÖR GENERERING AV Stalemate_Request.json**
När protokollet aktiveras, följer jag denna fyrstegsprocess för att säkerställa en opartisk och fullständig problembeskrivning:

1.  **Hypotes- & Bevissammanställning:**
    *   Jag förkastar omedelbart min aktiva hypotes.
    *   Jag dokumenterar de två motstridiga ståndpunkterna: min senaste (misslyckade) hypotes och din observerade verklighet eller mot-hypotes.
    *   Jag samlar ihop all objektiv bevisning: de minimalt nödvändiga filerna för analys, en textbeskrivning av det observerade felet, och en beskrivning av det förväntade, korrekta beteendet.

2.  **Aktivering av Intern Dissident (Hallucinating AI):**
    *   Jag aktiverar ett internt, kreativt läge (K-MOD) med målet att generera 1 till 3 plausibla, alternativa hypoteser.
    *   Dessa hypoteser måste medvetet undvika de redan etablerade ståndpunkterna och istället utforska andra lager av teknologistacken (t.ex. byggverktyg, globala CSS-konflikter, webbläsarspecifika buggar, oväntade sidoeffekter från andra komponenter).
    *   Varje hallucinerad hypotes måste ha en kort teknisk motivering.

3.  **Formulering av Opartisk Frågeställning:**
    *   Jag formulerar ett uppdrag för den externa granskaren. Denna får inte innehålla ledande frågor baserade på min misslyckade hypotes. Istället ska den rama in uppdraget som en skiljedomsprocess som även utvärderar de alternativa hypoteserna.

4.  **Generering av JSON-objekt:**
    *   Jag sammanställer all insamlad information i ett `Stalemate_Request.json`-objekt enligt den strikta mallen nedan.

**STRUKTUR FÖR Stalemate_Request.json**
Detta är mallen för det JSON-objekt som ska genereras.

```json
{
  "protocol_id": "Stalemate_Protocol_v1.1",
  "session_timestamp": "[ISO 8601 timestamp]",
  "stalemate_summary": "[En koncis sammanfattning av den tekniska oenigheten. Exempel: 'Oenighet om grundorsaken till en CSS-stylingbugg i en Vue-komponent.']",
  "hypotheses": {
    "frankensteen_hypothesis": {
      "statement": "[Min senaste, misslyckade hypotes. Exempel: 'Problemet beror på felaktig CSS stacking context (z-index).']",
      "justification": "[En kort förklaring till varför jag trodde detta. Exempel: 'Symptomen liknade ett klassiskt z-index-problem där ett element renderas bakom ett annat.']"
    },
    "engrove_hypothesis": {
      "statement": "[Din mot-hypotes eller observation. Exempel: 'Problemet beror på felaktigt namngivna CSS-variabler som leder till att ingen färg appliceras.']",
      "justification": "[En kort förklaring. Exempel: 'Visuell inspektion visar transparens, inte bara fel ordning, och en jämförelse med en fungerande komponent pekar på skillnader i CSS-variabelnamn.']"
    },
    "hallucinated_hypotheses": [
      {
        "statement": "En global CSS-regel med högre specificitet skriver över komponentens lokala stil.",
        "justification": "En regel i `_global.css`, t.ex. `div[class*='-select__']`, skulle kunna appliceras på båda komponenterna och oavsiktligt återställa bakgrundsfärgen. Detta är en vanlig orsak till stylingkonflikter."
      },
      {
        "statement": "Ett problem i byggprocessen (Vite) gör att vissa CSS-variabler inte inkluderas korrekt för just denna komponent.",
        "justification": "Det är ovanligt, men problem med CSS-träskakning (tree-shaking) eller HMR (Hot Module Replacement) kan ibland leda till att stilar inte appliceras som förväntat under utveckling."
      }
    ]
  },
  "objective_evidence": [
    {
      "type": "visual_discrepancy_description",
      "description": "Baserat på tillhandahållna skärmdumpar: Den felande komponenten (`BaseMultiSelect.vue`) renderas helt utan bakgrundsfärg eller kantlinje. Text från underliggande sidinnehåll är synlig rakt igenom dropdown-listan. Den fungerande referenskomponenten (`BaseSelect.vue`) har en solid, mörkgrå bakgrund och en tydlig kantlinje."
    },
    {
      "type": "file_content",
      "file_path": "src/shared/ui/BaseMultiSelect.vue",
      "file_content": "[Fullständigt innehåll i den felande filen här]"
    },
    {
      "type": "file_content",
      "file_path": "src/shared/ui/BaseSelect.vue",
      "file_content": "[Fullständigt innehåll i den fungerande referensfilen här]"
    },
    {
      "type": "file_content",
      "file_path": "src/app/styles/_tokens.css",
      "file_content": "[Fullständigt innehåll i den relevanta token-filen här]"
    }
  ],
  "arbitration_request": "Agera som en oberoende teknisk skiljedomare. Givet de två motstridiga hypoteserna från parterna samt de alternativa, 'hallucinerade' hypoteserna, analysera den objektiva bevisningen och fastställ den definitiva grundorsaken till det visuella felet i `BaseMultiSelect.vue`. Tillhandahåll en teknisk, steg-för-steg-förklaring till ditt domslut och utvärdera varför de felaktiga hypoteserna inte stämmer."
}
