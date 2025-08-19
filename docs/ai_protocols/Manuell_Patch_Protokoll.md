# docs/ai_protocols/Manuell_Patch_Protokoll.md
#
# === SYFTE & ANSVAR ===
# Strikt, otvetydigt patchflöde för manuella ändringar med full spårbarhet.
#
# === HISTORIK ===
# * v1.0 (2025-08-18): Initial.
# * v2.0 (2025-08-19): Normativ bindning, anchor_diff_v3.0‑kontrakt, regler, HITL/säkerhet, exempel.

## Normativ bindning
- Körs under PSV (AI_Core_Instruction.md v5.8). Följer Grundbulten P‑GB‑3.9 (hash/logg).
- Endast patchformat **anchor_diff_v3.0** (Diff_Protocol_v3.md). “Uppskattade diffar” är förbjudna.

## Patchkontrakt (anchor_diff_v3.0)

```jsonc
{
  "protocol_id": "anchor_diff_v3.0",
  "target": {
    "file_path": "PATH/TO/FILE.ext",
    "base_checksum_sha256": "<64-hex>"     // hash FÖRE ändring (måste stämma)
  },
  "actions": [
    {
      "op": "REPLACE",                      // eller: DELETE | INSERT_AFTER | INSERT_BEFORE
      "anchor": {
        "before": "^# === SYFTE",          // regex (valfritt per op)
        "after": "^## HISTORIK"            // regex (valfritt per op)
      },
      "new_block": "…nytt innehåll…"        // krävs för REPLACE/INSERT_*
    }
  ],
  "final_checksum_sha256": "<64-hex>",      // hash EFTER ändring (verifieras)
  "summary": "Kort orsak till ändring"
}
```

## Regler
- `protocol_id` måste vara exakt `"anchor_diff_v3.0"`.
- `target.base_checksum_sha256` krävs och ska matcha faktisk filhash före skrivning.
- `final_checksum_sha256` krävs; verifieras efter skrivning.
- `old_block` är **förbjudet** i alla patchar.
- `op`‑regler:
  - **REPLACE**: minst ett av `before/after` krävs.
  - **DELETE**: minst ett av `before/after`; inget `new_block`.
  - **INSERT_AFTER/INSERT_BEFORE**: exakt en av `before/after` + `new_block`.
- Ankare som matchar 0 eller >1 ställen ⇒ **avbryt** patchen.
- Regex ska vara enkla och deterministiska (ankra med `^`).

## HITL & säkerhet
- ≥25 rader borttagna eller ändringar i säkerhetskritiska filer ⇒ **HITL Pre‑Commit**.
- Kodpatchar körs i **SANDBOX** + `pytest` enligt Structured_Debugging_Checklist.md.
- Alla åtgärder loggas i `.tmp/session_revision_log.json` (P‑GB‑3.9).

## Exempel (minimalt)
```json
{
  "protocol_id": "anchor_diff_v3.0",
  "target": { "file_path": "docs/README.md", "base_checksum_sha256": "..." },
  "actions": [
    { "op": "INSERT_AFTER", "anchor": { "after": "^# README$" }, "new_block": "\n## Licens\nMIT\n" }
  ],
  "final_checksum_sha256": "...",
  "summary": "Lade till licensavsnitt"
}
```

## DynamicProtocols
- `DP-DIFF-GUARD-01` blockerar patchar utan `base_checksum_sha256`, fel `protocol_id`, eller med `old_block`.
