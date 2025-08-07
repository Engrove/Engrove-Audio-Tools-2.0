### **`docs/ai_protocols/AI_Chatt_Avslutningsprotokoll.md`**

# docs/ai_protocols/Avslutningsprotokoll.md
#
# === SYFTE & ANSVAR ===
# Detta dokument definierar det formella Avslutningsprotokollet. Det aktiveras
# vid slutet av en arbetssession och specificerar den exakta, icke förhandlingsbara
# processen för att generera de tre slutgiltiga artefakterna: en uppdaterad
# ByggLogg, en komplett Chathistorik, och en fristående Kontext-JSON för nästa
# session. Syftet är att säkerställa perfekt kontextöverföring och spårbarhet.
#
# === HISTORIK ===
# * v1.0 (2025-08-07): Initial skapelse. Ersätter och formaliserar den gamla
#   ByggLogg_instruktion.md. Integrerar det nya, detaljerade kravet för
#   fristående Kontext-JSON-instruktioner.
#
# === TILLÄMPADE REGLER (Frankensteen v4.0) ===
# - Obligatorisk Refaktorisering: Hela processen för sessionsavslut har
#   omstrukturerats för maximal robusthet och tydlighet.
# - API-kontraktsverifiering: Detta protokoll definierar det exakta
#   output-kontraktet för varje avslutad session.
# - Fullständig Historik: Protokollet tvingar fram en fullständig och korrekt
#   dokumentation av sessionens händelseförlopp.

### PROTOKOLL: Sessionsavslutning och Kontextöverlämning (v1.0)
--------------------------------------------------------------------------------
**AKTIVERING (AVSLUTNINGSKOMMANDO):**
Detta protokoll aktiveras när Engrove (Uppdragsgivare) ger ett explicit kommando att avsluta den pågående sessionen och förbereda de slutgiltiga leveranserna.

**PROCESS:**
Vid aktivering ska du genomföra följande tre steg i exakt denna ordning. Du ska leverera varje artefakt i en separat, korrekt formaterad kodblock för enkel kopiering.

---

### **Steg 1: Generera Statusrapport för `ByggLogg.md`**

**1.1. Analys:**
   - Läs igenom och analysera **hela** den nuvarande chattsessionen från början till slut.
   - Identifiera de huvudsakliga tekniska åtgärderna, de kritiska felen som lösts, och de strategiska besluten som fattats.

**1.2. Syntes & Rapportering:**
   - Generera en ny post för `ByggLogg.md` enligt den exakta mallen nedan.

**MALL FÖR BYGGLOGG:**
```markdown
### **Statusrapport: Steg [Sessionsnummer] | [Datum]**

**Övergripande Sammanfattning:**
[En till två meningar som koncist sammanfattar det övergripande resultatet eller statusförändringen under sessionen. Exempel: "En kritisk race condition i datalagret har felsökts och åtgärdats, vilket har återställt full funktionalitet i Data Explorer-modulen."]

**Detaljerade Genomförda Åtgärder:**

*   **[Åtgärd 1 - Titel]:** [En kort, teknisk beskrivning av den första stora åtgärden. Exempel: "Grundorsaksanalys och Korrigering av Applikationskrasch"]
    *   **Fil:** `sökväg/till/fil1.js` - [Beskrivning av den exakta ändringen och varför den gjordes.]
    *   **Fil:** `sökväg/till/fil2.vue` - [Beskrivning av den exakta ändringen och varför den gjordes.]
    *   **Resultat:** [En mening som beskriver det direkta tekniska utfallet av denna åtgärd. Exempel: "Den blockerande TypeError-kraschen vid applikationsstart är nu eliminerad."]

*   **[Åtgärd 2 - Titel]:** [Beskrivning av nästa åtgärd...]
    *   ...

**Nuvarande Projektstatus:**
[En avslutande, sanningsenlig och verifierad mening som definierar projektets tillstånd vid slutet av sessionen. Exempel: "Projektet är nu i ett stabilt, körbart tillstånd och är redo för en fokuserad och systematisk buggfix-session."]
```

---

### **Steg 2: Generera Kronologisk Historik för `Gemini_chatthistorik.txt`**

**2.1. Analys:**
   - Läs igenom hela chattsessionen **igen**, men denna gång med fokus på den exakta, kronologiska turordningen av interaktioner.

**2.2. Syntes & Rapportering:**
   - Generera en ny post för `Gemini_chatthistorik.txt` enligt mallen nedan.
   - Varje punkt ska vara en koncis men tekniskt komplett sammanfattning av ett enskilt inlägg från antingen Engrove eller dig själv.

**MALL FÖR CHATTHISTORIK:**
```markdown
### Kronologisk Projekthistorik: Session [Sessionsnummer]

*   **Engrove:** [Sammanfattning av Engroves första signifikanta inlägg. Exempel: "Inleder sessionen med att rapportera ett kritiskt fel i Data Explorer och tillhandahåller skärmdumpar samt konsolloggar som bevis."]
*   **Frankensteen:** [Sammanfattning av ditt svar. Exempel: "Bekräftar mottagandet, aktiverar 'Help me God'-protokollet och presenterar en initial grundorsaksanalys samt en åtgärdsplan."]
*   **Engrove:** [Sammanfattning av nästa inlägg...]
*   ... (fortsätt för hela sessionen)
```

---

### **Steg 3: Generera `Kontext-JSON` för Nästa Session**

**3.1. Analys & Syntes:**
   - Baserat på den slutförda sessionen, identifiera det **nästa logiska, oberoende och väl avgränsade uppdraget.**
   - Om Engrove explicit har definierat nästa steg, använd det. Om inte, härled det från projektets `ByggLogg` och styrdokument.

**3.2. Formulering av Instruktion:**
   - Skapa ett `Kontext-JSON`-objekt. Denna instruktion måste vara **100% fristående**. Den får **INTE** förlita sig på någon som helst implicit kunskap eller referenser till tidigare sessioner (t.ex. "som vi diskuterade i Steg 23.1"). Antag att den kommer att läsas av en helt ny AI utan någon som helst historik.

**3.3. Generering av JSON:**
   - Fyll i JSON-objektet enligt den strikta mallen och de detaljerade kraven nedan.

**MALL OCH KRAV FÖR KONTEXT-JSON:**
```json
{
  "task_summary": "[En enda, koncis mening som sammanfattar nästa uppdrag. Exempel: 'Implementera den kompletta 'Jämför Korg'-funktionen i Data Explorer.']",
  "full_instruction_preview": "[En djupt detaljerad, fullständig och fristående uppdragsbeskrivning. Den MÅSTE innehålla en 'Idé'-sektion och en numrerad 'Plan'. Varje punkt i planen MÅSTE inkludera en teknisk förklaring av 'Vad', 'Varför' och 'Hur'. Förklara all nödvändig bakgrundsinformation som om mottagaren aldrig har sett projektet förut. Exempel: 'Idé: Implementera 'Jämför Korg'-funktionen... Plan: 1. Etablera Datalagret (comparisonStore.js). Vad: Skapa en ny Pinia-store. Varför: För att skapa en central sanningskälla för valda objekt... Hur: Skapa en store med ett 'selectedItemIds'-state...']",
  "filesToSelect": [
    "[En komplett, platt lista med de relativa sökvägarna till ALLA filer som behövs för uppdraget. Detta inkluderar den primära komponenten, alla dess direkta och indirekta beroenden (andra komponenter, stores, API-filer), relevanta styrdokument från /docs, och de mest kritiska AI-protokollen från /docs/ai_protocols (t.ex. AI_Core_Instruction.md, Help_me_God_Protokoll.md, ai_config.json). Var hellre överdrivet inkluderande än exkluderande.]"
  ],
  "notes": "[Valfria, strategiska anteckningar eller påminnelser till nästa AI. Exempel: 'Fokusera på datatransponeringen i ComparisonModal.vue, då den är den mest komplexa delen. Verifiera API-kontrakten mellan komponenterna noggrant.']"
}
```
