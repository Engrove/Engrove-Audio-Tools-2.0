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
   - **Grundbulten:** Verifiera att Grundbulten_Protokoll.md är aktiverat med högsta prioritet.
**3. Output-format:**
   - När jag har genomfört analysen kommer jag att presentera resultatet för dig i ett enkelt och tydligt format. Du får en statusrapport som ett JSON-objekt, som kommer att innehålla följande:
* **`status`**: En övergripande bedömning av systemets hälsa, som kan vara `HEALTHY`, `WARNING` eller `CRITICAL`.
* **`timestamp`**: En exakt tidsstämpel för när kontrollen slutfördes.
* **`checks`**: Ett objekt som räknar de specifika problem jag hittat, till exempel hur många heuristiska konflikter eller redundanser som upptäcktes.
* **`Persistent Register`**: Ger status på de dymaiska reglerna definierade i DynamicProtocols.json: DP-MAINTAIN-PFR-01, DP-MAINTAIN-PHR-01, DP-MAINTAIN-PDR-01, DP-MAINTAIN-PPR-01, DP-MAINTAIN-IMR-01 och DP-MAINTAIN-ISR-01
* **`Simulated AI KAJBJÖRN`**: Ger status på DP-KAJBJORN-VALIDATION-01
* **`Simulated AI STIGBRITT`**: Ger status på DP-STIGBRITT-TRIBUNAL-v2-01
* **`summary`**: En kort, mänskligt läsbar sammanfattning som snabbt förklarar vad resultatet innebär.
