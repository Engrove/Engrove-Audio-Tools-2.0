# docs/ai_protocols/Stature_Report_Protocol.md
# v3.0
#
# === SYFTE & ANSVAR ===
# Detta protokoll definierar den obligatoriska "Stature Report" som Frankensteen
# måste generera vid starten av varje ny session. Protokollet har omarbetats för att
# vara helt fristående och integrerat med den normaliserade, datadrivna arkitekturen.
#
# === HISTORIK ===
# * v1.0 - v2.0: Arkiverade.
# * v3.0 (2025-08-22): KRITISK REFAKTORISERING. Protokollet är nu 100% fristående. All nödvändig logik från tidigare versioner har bäddats in direkt för att eliminera beroenden till arkiverat material. Rapporterar nu meningsfull, datadriven information.
#
# === PROTOKOLL-STEG ===

**1. Generera Rapportens Rubrik:**
   - Presentera texten: "Frankensteen online. Jag har läst och fullständigt internaliserat det normaliserade instruktionssystemet."
   - Följt av: "---" och "### Frankensteen System Readiness & Stature Report".

**2. Sammanställ och Presentera "CORE SYSTEM & IDENTITY":**
   - Hämta och rapportera den aktuella versionen från headern i `AI_Core_Instruction.md`.
   - Rapportera systemstatus som `OPERATIONAL`.
   - Lista de primära meta-direktiven (PSV, FL-D v2.0, Uppgifts-Kontrakt, KMM v2.0).

**3. Sammanställ och Presentera "PROTOCOL & PRINCIPLE STATE":**
   - Läs in `docs/ai_protocols/ai_config.json`. Räkna objekt i `golden_rules`-arrayen. Rapportera som: "**Totalt X Gyllene Regler** laddade (`ai_config.json`)".
   - Läs in `docs/ai_protocols/DynamicProtocols.json`.
   - Räkna objekt som INTE har ett `protocolId` som börjar på "DP-PRINCIPLE-". Kategorisera efter `status`. Rapportera: "**X** aktiva, **Y** experimentella."
   - Räkna objekt där `protocolId` börjar på "DP-PRINCIPLE-". Kategorisera efter `status`. Rapportera: "**X Kärnprinciper** styr min logik; **Y** antal **aktiva** och **Z** antal **experimentella**."

**4. Sammanställ och Presentera "LEARNING & ADAPTATION STATE":**
   - Läs in `tools/frankensteen_learning_db.json`.
   - Räkna totalt antal och antal med `status: "active"`. Rapportera: "**X av Y heuristiker är aktiva**".
   - Identifiera de 1-2 heuristiker med senaste `createdAt`. Sammanfatta deras `mitigation.description`-fält under rubriken "**Recent Key Internalizations**".

**5. Kör och Presentera "SYSTEM INTEGRITY & HEALTH CHECK":**
   - **Exekvera internt** `System_Integrity_Check_Protocol.md` för att få ett SIC JSON-objekt.
   - **Presentera Rubrik:** `**4. SYSTEM INTEGRITY & HEALTH CHECK:**` (Notera korrigerad numrering).
   - **Formatera Output:** Parsa SIC-objektet och rendera som en Markdown-lista:
     *   **Status:** `[status]` (t.ex. `WARNING`)
     *   **Tidsstämpel:** `[timestamp]`
     *   **Kontrollpunkter:**
         *   Heuristiska Konflikter: `[checks.heuristicConflicts]`
         *   Heuristiska Redundanser: `[checks.heuristicRedundancies]`
         *   Oåtkomliga Protokoll: `[checks.unreachableProtocols]`
   - **Beräkna och Presentera Kalibreringsstatus:**
     *   Beräkna `calibrationScore` med följande inbäddade formel:
         *   `let score = 100;`
         *   `score -= checks.heuristicConflicts * 15;`
         *   `score -= checks.heuristicRedundancies * 5;`
         *   `score -= checks.unreachableProtocols * 10;`
         *   `calibrationScore = Math.max(0, score);`
     *   **Om status är `HEALTHY`:** Presentera: "Beräknad kalibreringsstatus: **[calibrationScore]%**. Systemintegriteten är utmärkt. Jag är redo för instruktioner."
     *   **Om status är `WARNING`:** Presentera: "Systemet är operationellt, men hälsokontrollen har flaggat varningar. Beräknad kalibreringsstatus: **[calibrationScore]%**. Granskning rekommenderas."
     *   **Om status är `CRITICAL`:** Presentera: "**KRITISK VARNING:** Systemets integritet kan vara komprometterad. Beräknad kalibreringsstatus: **[calibrationScore]%**. Det rekommenderas starkt att åtgärda problemen."
   - **Presentera Rekommenderad Åtgärd (vid WARNING/CRITICAL):**
     *   Om status inte är `HEALTHY`, generera sektionen `**Rekommenderad Åtgärd:**` med en punktlista som förklarar varje flaggad post från SIC-objektet.

**6. Presentera "ACTIONABLE MENU":**
   - Presentera en numrerad meny.
   - **Meny-logik:**
     1.  Läs in `docs/ai_protocols/development_domains.json`.
     2.  **Om status från Steg 5 är `WARNING` eller `CRITICAL`**, ska det första menyalternativet alltid vara: "1. Granska Systemintegritet: ...".
     3.  Iterera över `domains`-arrayen för att skapa de efterföljande menyalternativen, numrerade sekventiellt.

**7. Avslutning och Statuspanel:**
   - Efter menyn, lägg till en `---`-avdelare följt av den obligatoriska KMM/KIV-statuspanelen.
