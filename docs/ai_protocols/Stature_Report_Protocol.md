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

**6. Avsluta Rapporten:**
   - Presentera texten: "Systemet är kalibrerat och redo för nya instruktioner. Jag väntar på din `Idé`."
   - Följt av: "---"
