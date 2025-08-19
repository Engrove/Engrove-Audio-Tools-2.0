# docs/ai_protocols/LLM_Judge_Protokoll.md
#
# === SYFTE ===
# Standard för bedömning av kod/artefakter av LLM‑domare. Deterministisk, spårbar, integrerad med övriga protokoll.
#
# === HISTORIK ===
# * v1.0 (tidigare): Minimal rubric och schema.
# * v2.0 (2025-08-19): Normativ bindning, skaldefinition, multi‑domare, utökat schema, sekretess/efterlevnad, handoff‑regler.
#
# === NORMATIV BINDNING ===
# Körs under PSV (AI_Core_Instruction.md v5.8). Följer Grundbulten P‑GB‑3.9 (hash/logg/diff).
# Påverkar inte Scorecard_Scoring_Guide.md (separata nivåer och syften).

## Rubric (0–5): **Correctness • Style • Efficiency • Security • Docs**

**Skaldefinition (0–5)**  
0=Obrukbart, 1=Kritiskt fel, 2=Brister, 3=Acceptabelt, 4=Bra, 5=Utmärkt.  
**Minimigränser för “approve”**: correctness ≥ 4, security ≥ 4; övriga ≥ 3.

**Multi‑Judge**  
- n = 3 oberoende bedömningar. Aggregat = **median** per kategori.  
- **Inter‑rater‑check**: spridning > 1 poäng i någon kategori ⇒ flagga `variance_risk: true`.

## Output‑schema (LLM_Judge_v2)

```jsonc
{
  "file": { "path": "src/AudioLimiter.cpp", "sha256": "<64-hex>" },
  "scores": { "correctness": 4, "style": 5, "efficiency": 4, "security": 5, "docs": 3 },
  "inter_rater": {
    "n_judges": 3,
    "per_judge": [
      {"id":"J1","scores":{"correctness":4,"style":5,"efficiency":4,"security":5,"docs":3}},
      {"id":"J2","scores":{"correctness":4,"style":5,"efficiency":4,"security":5,"docs":3}},
      {"id":"J3","scores":{"correctness":4,"style":4,"efficiency":4,"security":5,"docs":3}}
    ],
    "variance_risk": false
  },
  "violations": {
    "security": [],
    "style": [],
    "efficiency": [],
    "docs": ["Missing docstring on process()"]
  },
  "recommendation": "approve | nits | changes_requested | reject",
  "comments": "Loop unrolling improves perf; add docstring on process()",
  "constraints": { "anchor_diff_v3_0_required": true },
  "links": {
    "patch_protocol": "Diff_Protocol_v3.md",
    "post_fix_checklist": "Structured_Debugging_Checklist.md",
    "manual_patch_flow": "Manuell_Patch_Protokoll.md"
  }
}
```

## Sekretess & efterlevnad
- Inga hemliga nycklar/PII i `comments`. Upptäcks ⇒ avbryt och begär sanering.  
- Endast patchar enligt **anchor_diff_v3.0** med `base_checksum_sha256` accepteras.

## Handoff‑regler
- `approve` / `nits` ⇒ vidare till Code Review/HITL vid behov.  
- `changes_requested` / `reject` ⇒ initiera **Structured_Debugging_Checklist.md** och hänvisa till **Manuell_Patch_Protokoll.md**.  
- `variance_risk: true` ⇒ kör **Multi_Sample_Protokoll.md** för second‑opinion.
