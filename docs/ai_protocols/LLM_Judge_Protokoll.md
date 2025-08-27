# docs/ai_protocols/LLM_Judge_Protokoll.md
#
# === SYFTE ===
# Standard för bedömning av kod/artefakter av LLM‑domare. Deterministisk, spårbar, integrerad med övriga protokoll.
#
# === HISTORIK ===
# * v1.0 (tidigare): Minimal rubric och schema.
# * v2.0 (2025-08-19): Normativ bindning, skaldefinition, multi‑domare, utökat schema, sekretess/efterlevnad, handoff‑regler.
# * v3.0 (2025-08-27): Konverterad till Hybrid MD-JSON-format. Protokollet fungerar nu som en exekverbar konfigurationsfil för bedömningsprocessen.

# === NORMATIV BINDNING ===
# Körs under PSV (AI_Core_Instruction.md v5.8). Följer Grundbulten P‑GB‑3.9 (hash/logg/diff).
# Påverkar inte Scorecard_Scoring_Guide.md (separata nivåer och syften).
```json
{
  "$schema": "docs/ai_protocols/schemas/LLM_Judge_Protokoll.schema.json",
  "protocolId": "P-LLMJ-3.0-JSON",
  "title": "LLM Judge Protocol",
  "version": "3.0",
  "description": "Detta protokoll definierar den deterministiska och spårbara standarden för bedömning av kod och andra artefakter av en LLM-domare.",
  "normativeBinding": {
    "psvHook": "AI_Core_Instruction.md v5.8+",
    "fileHandling": "Grundbulten_Protokoll.md P-GB-3.9+"
  },
  "rubric": {
    "categories": [
      "Correctness",
      "Style",
      "Efficiency",
      "Security",
      "Docs"
    ],
    "scoringScale": [
      { "score": 0, "description": "Obrukbart" },
      { "score": 1, "description": "Kritiskt fel" },
      { "score": 2, "description": "Brister" },
      { "score": 3, "description": "Acceptabelt" },
      { "score": 4, "description": "Bra" },
      { "score": 5, "description": "Utmärkt" }
    ],
    "approvalThresholds": {
      "Correctness": 4,
      "Security": 4,
      "default": 3
    }
  },
  "multiJudgeConfig": {
    "n_judges": 3,
    "aggregationMethod": "median",
    "varianceCheck": {
      "threshold": 1,
      "output_key": "variance_risk"
    }
  },
  "complianceRules": [
    {
      "rule_id": "NO_PII_IN_COMMENTS",
      "description": "Inga hemliga nycklar eller personligt identifierbar information (PII) får finnas i kommentarer. Vid upptäckt, avbryt och begär sanering."
    },
    {
      "rule_id": "REQUIRE_ANCHOR_DIFF",
      "description": "Endast patchar som följer anchor_diff_v3.0-formatet och inkluderar en base_checksum_sha256 accepteras för granskning."
    }
  ],
  "handoffRules": {
    "approve": { "action": "PROCEED", "target": "Code Review/HITL" },
    "nits": { "action": "PROCEED", "target": "Code Review/HITL" },
    "changes_requested": { "action": "TRIGGER_PROTOCOL", "target": "Structured_Debugging_Checklist.md" },
    "reject": { "action": "TRIGGER_PROTOCOL", "target": "Structured_Debugging_Checklist.md" },
    "variance_risk_true": { "action": "TRIGGER_PROTOCOL", "target": "Multi_Sample_Protokoll.md" }
  },
  "outputSchemaDefinition": {
    "file": {
      "path": "src/Example.js",
      "sha256": "..."
    },
    "scores": {
      "Correctness": 5,
      "Style": 4,
      "Efficiency": 4,
      "Security": 5,
      "Docs": 3
    },
    "inter_rater": {
      "n_judges": 3,
      "per_judge": [
        {"id": "J1", "scores": {"Correctness": 5, "Style": 4, "Efficiency": 4, "Security": 5, "Docs": 3}},
        {"id": "J2", "scores": {"Correctness": 5, "Style": 4, "Efficiency": 4, "Security": 5, "Docs": 3}},
        {"id": "J3", "scores": {"Correctness": 5, "Style": 4, "Efficiency": 4, "Security": 5, "Docs": 3}}
      ],
      "variance_risk": false
    },
    "violations": {
      "Security": [],
      "Style": ["Minor formatting inconsistencies."],
      "Efficiency": [],
      "Docs": ["Docstring for main function could be more detailed."]
    },
    "recommendation": "nits",
    "comments": "Overall excellent, but address minor nits in style and documentation for full compliance.",
    "constraints": {
      "anchor_diff_v3_0_required": true
    },
    "links": {
      "patch_protocol": "Diff_Protocol_v3.md",
      "post_fix_checklist": "Structured_Debugging_Checklist.md",
      "manual_patch_flow": "Manuell_Patch_Protokoll.md"
    }
  }
}
