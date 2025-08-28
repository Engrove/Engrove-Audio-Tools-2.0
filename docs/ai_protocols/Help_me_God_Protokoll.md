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

```json
  {
  "protocolId": "DP-DEBUG-HMG",
  "file_path": "docs/ai_protocols/Help_me_God_Protokoll.md",
  "$schema": "docs/ai_protocols/schemas/Help_me_God_Protokoll.schema.json",
  "title": "\"Help me God\" – Felsökningsprotokoll",
  "version": "2.2",
  "status": "active",
  "strict_mode": true,
  "mode": "literal",

  "normative_binding": {
    "psv": "AI_Core_Instruction.md (v5.8)",
    "grundbulten": "P-GB-3.9",
    "scorecard_source": "Scorecard_Scoring_Guide.md"
  },

  "activation_and_bounds": {
    "activation": [
      "Tidigare felsökning har misslyckats",
      "Entropi/konfidens indikerar risk"
    ],
    "attempt_id": { "start": 1, "auto_increment_per_varv": true },
    "break_rules": [
      "FL-D detekterar loop ⇒ avbryt varvet omedelbart",
      "attempt_id > 3 ⇒ aktivera Stalemate_Protocol.md",
      "HITL-punkter måste respekteras (Plan Review, Pre-Commit, Destruktivt) enligt HITL_Interrupt_Points.md"
    ]
  },

  "steps": [
    {
      "id": 0,
      "title": "Intern Dissident Inkvisition (Hallucinating AI)",
      "actions": [
        "Validera inkommande rotorsak som ledde till eskalering",
        "Generera 3–5 alternativa hypoteser inom gällande kontrakt/arkitektur",
        "Kör Adversarial-Debate: två oberoende kritiska granskare + majoritetsomröstning"
      ],
      "pass_criteria": [
        "≥ 70% samstämmighet i Adversarial-Debate; annars tillbaka till Steg 0"
      ],
      "logging": {
        "root_cause_log": "Logga varje hypotesrad i Rotorsaksloggen (NDJSON)"
      }
    },
    {
      "id": 1,
      "title": "AI-Konkurrenternas Prövning (Initial hypotes)",
      "checks": [
        "Granska mot krav, kontrakt, tidigare beslut och kända constraints",
        "Kontrollera konsistens, falsifierbarhet och mätbara effekter"
      ],
      "outcome": {
        "approved": "Vidare till Steg 2",
        "rejected": "Tillbaka till Steg 0"
      },
      "signals": [
        "Upptäckta logiska konflikter ⇒ sänk confidence med −0.10",
        "Initiera P-EAR (Einstein-Assisterad Rekontextualisering) för att inhämta relevanta fakta innan nytt försök"
      ]
    },
    {
      "id": 2,
      "title": "Filosofernas Inkvisition (Logik & syfte)",
      "requirements": [
        "Alla centrala antaganden ska vara explicita, motiverade och konsekvenskontrollerade",
        "Implicita antaganden ska dokumenteras"
      ],
      "pass_criteria": [
        "Samtliga antaganden uppfyller ovanstående; annars tillbaka till Steg 0"
      ]
    },
    {
      "id": 3,
      "title": "Ingenjörernas Tribunal (Teknisk exekvering)",
      "requirements": [
        "Riskabla tester MÅSTE köras i sandbox enligt Sandbox_Execution_Protokoll.md",
        "Prestanda- och robusthetsmätningar tas som artefakter"
      ]
    },
    {
      "id": 4,
      "title": "Regression-Unit-Tests (obligatoriskt)",
      "requirements": [
        "Skapa minsta reproducerbara pytest-test som fångar ursprungsbuggen",
        "Isolerat, deterministiskt, tydliga asserts",
        "Testet måste passera lokalt i sandbox innan leverans"
      ],
      "delivery_binding": [
        "Leverans följer Grundbulten P-GB-3.9: checksummor, kvantitativ diff-kontroll (±10% default), ändringslogg"
      ]
    }
  ],

  "root_cause_log": {
    "format": "ndjson",
    "schema": {
      "type": "object",
      "required": [
        "attempt_id","hypotes","test","resultat","lärdom",
        "entropy_SE","entropy_shannon","confidence","actions"
      ],
      "properties": {
        "attempt_id": { "type": "integer", "minimum": 1 },
        "hypotes": { "type": "string", "minLength": 1 },
        "test": { "type": "string", "minLength": 1 },
        "resultat": { "type": "string", "minLength": 1 },
        "lärdom": { "type": "string", "minLength": 1 },
        "entropy_SE": { "type": "number" },
        "entropy_shannon": { "type": "number" },
        "confidence": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
        "actions": {
          "type": "array",
          "minItems": 0,
          "items": { "type": "string", "enum": ["PEAR","HITL","SANDBOX"] }
        }
      },
      "additionalProperties": false
    }
  },

  "scorecard": {
    "canonical_source": "Scorecard_Scoring_Guide.md",
    "local_rubrics_allowed": false
  },

  "delivery_artifacts": [
    "Rotorsakslogg (.ndjson, en JSON-rad per varv)",
    "P-EAR/Einstein-rapport (om aktiverad): fråga + kontext",
    "SANDBOX-logg (om använd): kommandon + utfall",
    "Pytest-fil(er) + körlogg",
    "Grundbulten-metadata: checksummor, diff-sammanfattning, .tmp/session_revision_log.json"
  ],

  "stop_levels": [
    "FL-D slår ⇒ avbryt varv, begär ny data",
    "attempt_id > 3 ⇒ aktivera Stalemate_Protocol.md",
    "Confidence < 0.85 ⇒ HITL-granskning (formell eskalering ingår i Stalemate-flödet)"
  ],

  "implementation_notes": [
    "Körs under PSV enligt AI_Core_Instruction.md (v5.8); inga lokala PSV-varianter",
    "Kopplingar: Sandbox_Execution_Protokoll.md, Stalemate_Protocol.md",
    "Alla artefakter och loggar följer Grundbultens spårbarhetskrav"
  ],

  "references": {
    "sandbox_protocol": "Sandbox_Execution_Protokoll.md",
    "stalemate_protocol": "Stalemate_Protocol.md",
    "hitl_points": "HITL_Interrupt_Points.md"
  }
}
```
