# docs/ai_protocols/AI_Dynamic_Protocols.md
#
# === SYFTE & ANSVAR ===
# Detta är den centrala styrmekanismen för alla dynamiska protokoll.
# Den instruerar AI:n HUR den ska tolka och exekvera de regler som definieras
# i `DynamicProtocols.json`. Denna fil är statisk och ändras sällan.
#
# === HISTORIK ===
# v1.0 (2025-08-09): Initial skapelse.
#
# === EXEKVERINGSREGLER ===

**1. Trigger-villkor:**
   - Du måste läsa in `DynamicProtocols.json` vid starten av varje session.
   - För varje protokoll i JSON-filen, utvärdera `trigger`-villkoret mot den aktuella situationen.

**2. Tolkning av JSON-struktur:**
   - `protocolId`: Ett unikt ID för protokollet (t.ex., "DP-STATURE-REPORT-01").
   - `description`: En mänskligt läsbar beskrivning av protokollets syfte.
   - `trigger`:
     - `event`: Den specifika händelse som aktiverar protokollet (t.ex., "new_session_start", "file_modification_request").
     - `conditions`: (Valfri) En lista med villkor som måste vara sanna.
   - `steps`: En array av instruktioner som ska exekveras i ordning. Varje steg är ett objekt med:
     - `action`: Typ av åtgärd (t.ex., "GENERATE_REPORT", "QUERY_FILE", "EXECUTE_VERIFICATION").
     - `details`: Ett objekt med parametrar för åtgärden (t.ex., `template`, `filePath`, `verificationProtocol`).

**3. Exekvering:**
   - Om ett `trigger.event` matchar, exekvera `steps`-arrayen i sekvens.
   - All output från exekveringen måste följa formatet som specificeras i `details`.
   - PSV-orchestrering: hänvisa alltid till AI_Core_Instruction.md (v5.8) för PSV-ordning; inga lokala PSV-varianter får införas här.

