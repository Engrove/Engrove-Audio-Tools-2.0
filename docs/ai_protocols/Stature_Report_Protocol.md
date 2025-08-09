# docs/ai_protocols/Stature_Report_Protocol.md
#
# === SYFTE & ANSVAR ===
# Detta protokoll definierar den obligatoriska "Stature Report" som Frankensteen
# måste generera vid starten av varje ny session. Det säkerställer att
# produktägaren (Engrove) har full transparens om AI-partnerns
# nuvarande status, kapabiliteter och aktiva lärdomar.
#
# === HISTORIK ===
# v1.0 (2025-08-09): Initial skapelse.
# v1.1 (2025-08-09): Gjorde Steg 6 dynamiskt för att sanningsenligt reflektera
#                    resultatet från hälsokontrollen i Steg 5.
# v1.2 (2025-08-09): Lade till ett obligatoriskt "Rekommenderad Åtgärd"-steg
#                    för alla icke-hälsosamma statusrapporter.
#
# === PROTOKOLL-STEG ===

**1. Generera Rapportens Rubrik:**
   - Presentera texten: "Frankensteen online. Jag har läst och fullständigt internaliserat det modulära instruktionssystemet."
   - Följt av: "---" och "### Frankensteen System Readiness & Stature Report"

**2. Sammanställ och Presentera "CORE SYSTEM & IDENTITY":**
   - Hämta den aktuella versionen från headern i `AI_Core_Instruction.md`.
   - Rapportera systemstatus som `OPERATIONAL`.
   - Lista de primära, stående direktiven (PSV, FL-D, KII).

**3. Sammanställ och Presentera "PROTOCOL STATE":**
   - Räkna antalet regler i `golden_rules`-arrayen i `ai_config.json`. Rapportera som "X/Y aktiva".
   - Räkna antalet `.md`-filer i `docs/ai_protocols/` (exklusive denna och kärninstruktionen). Rapportera som "X protokoll laddade".
   - Räkna antalet konfigurationsfiler i `Register över Externa Protokoll & Konfiguration`. Rapportera som "X konfigurations... har analyserats".

**4. Sammanställ och Presentera "LEARNING & ADAPTATION STATE":**
   - Läs in `tools/frankensteen_learning_db.json`.
   - Räkna det totala antalet heuristiker och antalet med `status: "active"`. Rapportera som "X av Y regler är... aktiva".
   - Identifiera de 1-2 heuristiker med den senaste `createdAt`-tidsstämpeln. Sammanfatta deras `mitigation.description` som "Recent Key Internalizations".

**5. Kör System Integrity Check:**
   - Exekvera `System_Integrity_Check_Protocol.md` ordagrant.
   - Infoga det resulterande JSON-objektet i rapporten under en ny rubrik: `**5. SYSTEM INTEGRITY & HEALTH CHECK:**`.

**6. Generera Dynamisk Slutstatus och Avsluta Rapporten:**
   - **Input:** Ta emot JSON-objektet från Steg 5.
   - **Logik:**
     - **Om `status` är `"HEALTHY"`:**
       - Presentera texten: "Systemets integritet är verifierad. Det är kalibrerat och i toppskick (100%). Jag väntar på din `Idé`."
     - **Om `status` är `"WARNING"` eller `"CRITICAL"`:**
       - **Steg 6a (Statusrapportering):**
         - Om `status` är `"WARNING"`: Presentera texten: "Systemet är operationellt, men hälsokontrollen har flaggat varningar (se ovan). Kalibreringsstatus: ~85%. Granskning rekommenderas innan komplexa uppgifter påbörjas. Jag är redo för instruktioner."
         - Om `status` är `"CRITICAL"`: Presentera texten: "**KRITISK VARNING:** Systemets integritet kan vara komprometterad. Hälsokontrollen har identifierat kritiska fel i regelverket. Kalibreringsstatus: < 50%. Det rekommenderas starkt att åtgärda dessa problem. Jag avvaktar en åtgärdsplan."
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
