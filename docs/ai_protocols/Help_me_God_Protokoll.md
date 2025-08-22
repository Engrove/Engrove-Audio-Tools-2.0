# docs/ai_protocols/Help_me_God_Protokoll.md
#
# === SYFTE & ANSVAR ===
# Detta protokoll är en sista utväg för kritiska felsökningsscenarier.
# Det driver fram hypotesgenerering, adversarial granskning, sandboxad testning,
# och deterministisk verifiering innan leverans.
#
# **Normativ bindning:** Körs under PSV enligt AI_Core_Instruction.md (v5.8).
# Måste bryta på FL-D (felsökningsloop-detektor) och följa Grundbulten P-GB-3.9
# (hash/logg/diff-regler). Poängsättning sker endast via Scorecard_Scoring_Guide.md.
#
# === HISTORIK ===
# * v1.x (2025-08-??): Tidigare versioner.
# * v2.1 (2025-08-19): Tydliga bryt/eskaleringsregler; centraliserad scorecard; sandboxkrav;
#                           RAG/Confidence/Escalation-koppling; rotorsakslogg-schema; leveransartefakter.
# * v2.2 (2025-08-22): LOGISK KORRIGERING: Ersatt föråldrade referenser (RAG_Faktacheck, etc.) med hänvisningar till P-EAR och rensat bort saknade beroenden för att anpassa till aktuell protokollstack.

## AKTIVERING OCH GRÄNSER

**Aktivering**  
- Tidigare felsökning har misslyckats, eller entropi/konfidens indikerar risk.

**attempt_id**  
- Startar på `1` och auto-ökas per varv.

**Brytregler**  
- FL-D detekterar loop ⇒ avbryt varvet omedelbart.  
- `attempt_id > 3` utan verifierad lösning ⇒ aktivera *Stalemate_Protocol.md*.  
- HITL-punkter måste respekteras (Plan Review, Pre-Commit, Destruktivt), se *HITL_Interrupt_Points.md*.

---

## STEG 0 – Intern Dissident Inkvisition (Hallucinating AI)
- **Validering av Inkommande Rotorsak:** Den allra första åtgärden är att granska den misslyckade hypotesen som ledde till eskaleringen. Alla nya hypoteser som genereras i detta steg **MÅSTE** vara bevisligen semantiskt distinkta från den ursprungliga, misslyckade strategin.
- **Generera 3–5 alternativa hypoteser** inom gällande kontrakt/arkitektur.
- Kör **Adversarial‑Debate**: två oberoende kritiska granskare + majoritetsomröstning.

**Pass‑kriterium (Adversarial‑Debate):**  
- Endast förslag med **≥ 70 %** samstämmighet går vidare; övriga tillbaka till Steg 0.

**Loggning:**  
- Varje hypotes loggas i *Rotorsaksloggen* (se schema nedan).

---

## STEG 1 – AI‑Konkurrenternas Prövning (Initial hypotes)

- Granska hypotesen mot krav, kontrakt, tidigare beslut och kända constraints.
- Kontrollera konsistens, falsifierbarhet och mätbara effekter.

**Utfall:**  
- *Godkänd* ⇒ vidare till Steg 2.  
- *Underkänd* ⇒ tillbaka till Steg 0.

**Signalering:**  
- Upptäckt av logiska konflikter ⇒ **sänk confidence −0.10** och initiera **P-EAR (Einstein-Assisterad Rekontextualisering)** enligt `AI_Core_Instruction.md` för att hämta relevant fakta innan nytt försök.

---

## STEG 2 – Filosofernas Inkvisition (Logik & syfte)

- Alla centrala antaganden måste vara explicita, motiverade och konsekvenskontrollerade.
- Implicita antaganden dokumenteras.

**Pass‑kriterium:**  
- Samtliga antaganden uppfyller kriterierna ovan. Annars tillbaka till Steg 0.

---

## STEG 3 – Ingenjörernas Tribunal (Teknisk exekvering)

- Riskabla tester **måste** köras i sandbox enligt *Sandbox_Execution_Protokoll.md*.
- Prestanda‑ och robusthetsmätningar tas som artefakter.

---

## STEG 4 – Regression‑Unit‑Tests (obligatoriskt)

- Skapa **minsta reproducerbara pytest‑test** som fångar ursprungsbuggen.
- Krav: isolerat, deterministiskt, tydliga asserts.
- Testet måste passera lokalt i sandbox **innan** leverans.
- Leverans följer Grundbulten P‑GB‑3.9: checksummor, kvantitativ diff‑kontroll (±10 % default), ändringslogg.

---

## ROTORSAKSLOGG – NDJSON‑schema (en rad per varv)

```json
{ "attempt_id": <int>,
  "hypotes": "<str>",
  "test": "<kort testdesign>",
  "resultat": "<utfall>",
  "lärdom": "<konkret insikt>",
  "entropy_SE": <float>,
  "entropy_shannon": <float>,
  "confidence": <float_0_to_1>,
  "actions": ["PEAR","HITL","SANDBOX"]
}
```

---

## SCORECARD

- **Kanonisk källa:** *Scorecard_Scoring_Guide.md*.  
- Inga lokala rubrics i detta dokument.

---

## LEVERANSARTEFAKTER (obligatoriskt)

- **Rotorsakslogg** (alla varv): `.ndjson` (en JSON‑rad per varv).
- **P-EAR/Einstein-rapport** (om aktiverad): Sammanfattning av sökfråga och erhållen kontext.
- **SANDBOX‑logg** (om använd): kommandon + utfall.
- **Pytest‑fil(er) + körlogg**.
- **Grundbulten‑metadata**: checksummor, diff‑sammanfattning, `.tmp/session_revision_log.json`.

---

## STOPPNIVÅER

- **FL‑D** slår ⇒ avbryt varv, begär ny data.
- **attempt_id > 3** ⇒ aktivera *Stalemate_Protocol.md*.
- **Confidence < 0.85** ⇒ **HITL‑granskning** (formell eskalering har integrerats i Stalemate).

---

## IMPLEMENTATIONSNOTER

- Körs under **PSV** enligt *AI_Core_Instruction.md (v5.8)*; inga lokala PSV‑varianter.
- **Kopplingar:** *Sandbox_Execution_Protokoll.md*, *Stalemate_Protocol.md*.
- Alla artefakter och loggar följer Grundbultens spårbarhetskrav.
