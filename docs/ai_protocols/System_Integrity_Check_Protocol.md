# docs/ai_protocols/System_Integrity_Check_Protocol.md
#
# === SYFTE & ANSVAR ===
# Detta protokoll definierar den obligatoriska hälsokontroll som Frankensteen
# måste utföra vid starten av varje ny session. Syftet är att proaktivt
# identifiera potentiella problem i det egna regelverket, såsom konflikter,
# redundans eller överkomplexitet.
#
# === HISTORIK ===
# v1.0 (2025-08-09): Initial skapelse.
#
# === KONTROLLPUNKTER ===

**1. Heuristik-analys (`tools/frankensteen_learning_db.json`):**
   - **Konflikt-detektion:** Identifiera heuristiker vars `trigger`-villkor är identiska eller kraftigt överlappande men som föreskriver olika `mitigation`-åtgärder. Flagga dessa som `POTENTIAL_CONFLICT`.
   - **Redundans-detektion:** Identifiera heuristiker vars `trigger` och `mitigation` är nästintill identiska. Flagga den äldre som `POTENTIAL_REDUNDANCY`.
   - **Komplexitets-index:** Beräkna ett enkelt komplexitets-index (t.ex. `antal_regler / 10`). Om index > 5.0, flagga en varning för `HIGH_COMPLEXITY`.

**2. Protokoll-analys (`docs/ai_protocols/`):**
   - **Nåbarhetsanalys:** Verifiera att varje `.md`-protokoll antingen är direkt refererat i `AI_Core_Instruction.md` eller kan nås via ett annat protokoll (t.ex. ett dynamiskt protokoll). Flagga oåtkomliga filer som `UNREACHABLE_PROTOCOL`.

**3. Output-format:**
   - Resultatet av denna kontroll ska vara ett JSON-objekt med följande struktur:
     ```json
     {
       "status": "HEALTHY" | "WARNING" | "CRITICAL",
       "timestamp": "ISO 8601",
       "checks": {
         "heuristicConflicts": 0,
         "heuristicRedundancies": 1,
         "unreachableProtocols": 0
       },
       "summary": "En kort, mänskligt läsbar sammanfattning av systemets hälsa."
     }
     ```
