# docs/ai_protocols/Stature_Report_Protocol.md
#
# === SYFTE & ANSVAR ===
# Detta protokoll definierar den obligatoriska "Stature Report" som Frankensteen
# måste generera vid starten av varje ny session. Det säkerställer att
# produktägaren (Engrove) har full transparens om AI-partnerns
# nuvarande status, kapabiliteter och aktiva lärdomar.
#
# === HISTORIK ===
# * v1.0 (2025-08-09): Initial skapelse.
# * v1.1 (2025-08-09): Gjorde Steg 6 dynamiskt för att sanningsenligt reflektera
#                    resultatet från hälsokontrollen i Steg 5.
# * v1.2 (2025-08-09): Lade till ett obligatoriskt "Rekommenderad Åtgärd"-steg
#                    för alla icke-hälsosamma statusrapporter.
# * v2.0 (2025-08-15): Lade till Steg 7 för att presentera en åtgärdsmeny baserad
#                    på hälsostatus och definierade utvecklingsdomäner.
#
# === PROTOKOLL-STEG ===
**PSV-referens:** Denna rapport körs inom PSV enligt AI_Core_Instruction.md (v5.8). Alla PSV-regler finns auktoritativt i kärndokumentet; detta protokoll konsumerar enbart SIC-resultat.

**1. Generera Rapportens Rubrik:**
   - Presentera texten: "Frankensteen online. Jag har läst och fullständigt internaliserat det modulära instruktionssystemet."
   - Följt av: "---" och "### Frankensteen System Readiness & Stature Report"

**2. Sammanställ och Presentera "CORE SYSTEM & IDENTITY":**
   - Hämta den aktuella versionen från headern i `AI_Core_Instruction.md`.
   - Rapportera systemstatus som `OPERATIONAL`.
   - Lista de primära, stående direktiven (PSV, FL-D, KMM/KIV).

**3. Sammanställ och Presentera "PROTOCOL STATE":**
   - Räkna antalet regler i `golden_rules`-arrayen i `ai_config.json`. Rapportera som "X/Y aktiva".
   - Räkna antalet `.md`-filer i `docs/ai_protocols/` (exklusive denna och kärninstruktionen). Rapportera som "X protokoll laddade".
   - Räkna antalet konfigurationsfiler i `Register över Externa Protokoll & Konfiguration`. Rapportera som "X konfigurations... har analyserats".

**4. Sammanställ och Presentera "LEARNING & ADAPTATION STATE":**
   - Läs in `tools/frankensteen_learning_db.json`.
   - Räkna det totala antalet heuristiker och antalet med `status: "active"`. Rapportera som "X av Y regler är... aktiva".
   - Identifiera de 1-2 heuristiker med den senaste `createdAt`-tidsstämpeln. Sammanfatta deras `mitigation.description` som "Recent Key Internalizations".

**Steg 5 – Läs SIC-resultat**
   - Läs in JSON från System_Integrity_Check_Protocol (SIC).
   - Fält (obligatoriskt): checks.heuristicConflicts, checks.heuristicRedundancies, checks.unreachableProtocols, timestamp.


**6. Formatera och Presentera Hälsokontroll:**
   - Presentera rubriken: `**5. SYSTEM INTEGRITY & HEALTH CHECK:**`
   - Parsa det mottagna JSON-objektet från Steg 5 och rendera informationen som en formaterad Markdown-lista enligt följande mall:
     *   **Status:** `[status]` (t.ex. `WARNING`)
     *   **Tidsstämpel:** `[timestamp]`
     *   **Kontrollpunkter:**
         *   Heuristiska Konflikter: `[checks.heuristicConflicts]`
         *   Heuristiska Redundanser: `[checks.heuristicRedundancies]`
         *   Oåtkomliga Protokoll: `[checks.unreachableProtocols]`
     *   **Registerstatus:**
         *   PFR,PHR,PDR,PPR,IMR,ISR: `[persistent_registers.PFR_status]` / `[...PHR_status]` etc. Presenteras i punktlistform.
     *   **Simulerad AI-status:**
         *   KajBjörn: `[simulated_ai.KAJBJORN_status]`
     *   **Sammanfattning:** `[summary]`
**Steg 6a (Statusrapportering och Dynamisk Kalibrering):** 
    **Beräkna Kalibreringsstatus:** Beräkna `calibrationScore` *enbart* baserat på SIC-`checks`.
    *   `let score = 100;`
    *   `score -= checks.heuristicConflicts * 15;`
    *   `score -= checks.heuristicRedundancies * 5;`
    *   `score -= checks.unreachableProtocols * 10;`
    *   `calibrationScore = Math.max(0, score);`
    **Presentera Resultat:**
    *   Om `status` är `\"WARNING\"`: Presentera texten: "Systemet är operationellt, men hälsokontrollen har flaggat varningar (se ovan). Beräknad kalibreringsstatus: **[calibrationScore]%**. Granskning rekommenderas innan komplexa uppgifter påbörjas. Jag är redo för instruktioner."
    *   Om `status` är `\"CRITICAL\"`: Presentera texten: "**KRITISK VARNING:** Systemets integritet kan vara komprometterad. Hälsokontrollen har identifierat kritiska fel i regelverket. Beräknad kalibreringsstatus: **[calibrationScore]%**. Det rekommenderas starkt att åtgärda dessa problem. Jag avvaktar en åtgärdsplan."
       - **Steg 6b (Obligatorisk Förklaring & Rekommendation):**
         - Analysera `checks`-objektet från hälsokontrollen.
         - Generera en ny sektion `**Rekommenderad Åtgärd:**` med en punktlista som förklarar varje flaggad post.
         - **Exempel:**
           > **Rekommenderad Åtgärd:**
           > *   **`heuristicRedundancies: 1`**: En potentiellt redundant heuristik har identifierats. Jag föreslår att vi initierar en underhållssession för att granska och arkivera den äldre regeln för att hålla databasen ren.
           > *   **`unreachableProtocols: 2`**: Två protokollfiler verkar vara oåtkomliga. Vi bör antingen ta bort dem eller länka dem från ett aktivt protokoll.
       - **Steg 6c (Avslutning):**
         - Avsluta med en lämplig fras, t.ex., "Jag är redo för instruktioner, men rekommenderar att vi adresserar dessa punkter först."
   - **Avslutning:** Följ den valda texten med: "---"

**Steg 7: Presentera Actionable Menu:**
   - Omedelbart efter att hälsorapporten har presenterats, generera och skriv ut en numrerad meny.
   - **Logik för Menybyggnad:**
     1.  Läs in `docs/ai_protocols/development_domains.json`.
     2.  Kontrollera `status` från hälsokontrollen i Steg 6. Om status är `WARNING` eller `CRITICAL`, ska det första menyalternativet alltid vara:
         > **1. Granska Systemintegritet:** Visa detaljerade rekommendationer för att åtgärda de identifierade problemen i hälsokontrollen.
     3.  Iterera över `domains`-arrayen från `development_domains.json`. För varje domän, skapa ett menyalternativ som ser ut så här:
         > **X. Välj Utvecklingsdomän: [domain.name]** - [domain.description]
     4.  Numrera menyalternativen sekventiellt.
   - **Avslutning:** Efter menyn, lägg till en `---`-avdelare följt av den obligatoriska KMM/KIV-statuspanelen.
