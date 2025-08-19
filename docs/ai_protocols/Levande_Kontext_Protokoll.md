# docs/ai_protocols/Levande_Kontext_Protokoll.md
#
# === SYFTE & ANSVAR ===
# Sessionsbaserat VCS för kontext: spårbar, deterministisk, lätt att återställa.
# Säkrar att AI arbetar mot rätt filbaslinje och att alla ändringar är loggade.
#
# **Normativ bindning:** Körs under PSV (AI_Core_Instruction.md v5.8).
# Följer Grundbulten P-GB-3.9 (hash/logg) och Diff_Protocol_v3.md (anchor_diff_v3.0).
#
# === HISTORIK ===
# * v2.0 (tidigare): Konceptuell version med ellipser.
# * v2.1 (2025-08-19): Körbar specifikation. Index+blob, hårda triggers, schema, P-KLS, DP-krokar, DJTA-snapshot.

## EXTRA PROTOKOLL: "LEVANDE KONTEXT" (v2.1)

**Mål:** Spårbar, deterministisk filkontext under session. Låg overhead. Inga patchar skrivs här; detta är metadataflöde.

### Register/lagring
- Index: `.tmp/living_context/index.json`
- Innehåll: `.tmp/living_context/blobs/<sha256>` (rått innehåll; filnamn = sha256)
- ISR-event per åtgärd: `{ event:"lk_<op>", file, sha256 }`
- Revisioner: `v0..vN` per fil

### Kommandon (AI-interna steg, ej användarkommando)
1) **LK_INIT(file, content, note?)**
   - Beräkna `sha256(content)`. Spara blob.
   - Lägg i index: `{ file, history:[{ rev:"v0", sha256, note:"init|<note>", ts:"<ISO8601>" }] }`
2) **LK_COMMIT(file, new_content, note)**
   - Kräv **anchor_diff_v3.0** mot senaste `sha256` (base_checksum_sha256 = index.senaste.sha256).
   - Spara blob, bumpa rev `v{n+1}`, uppdatera index (rev, sha256, note, ts).
3) **LK_REVERT(file, target_rev)**
   - Hämta `blob@target_rev`, gör LK_COMMIT med `note:"revert->target_rev"`.
4) **LK_SHOW_HISTORY(file)**
   - Lista `rev, ts, note, sha256` (senaste→äldsta).
5) **LK_VERIFY_BASELINE(file, external_sha256?)**
   - Jämför `index.senaste.sha256` mot angiven. Mismatch ⇒ **STOPPA** och begär uppdaterad fil eller explicit bekräftelse att arbeta mot LK@senaste.

### Efterlevnad
- Endast patchar enligt **Diff_Protocol_v3.md (anchor_diff_v3.0)** accepteras i anslutning till LK_COMMIT.
- Varje LK_COMMIT **måste** inkludera `base_checksum_sha256 = index.senaste.sha256`.
- Logga alla operationer i `.tmp/session_revision_log.json` (P-GB-3.9) och i ISR.

---

## SCHEMA

**index.json**
```json
{
  "version": "LKv2.1",
  "files": [
    {
      "file": "src/App.tsx",
      "history": [
        { "rev": "v0", "sha256": "<64-hex>", "note": "init",         "ts": "<ISO8601>" },
        { "rev": "v1", "sha256": "<64-hex>", "note": "fix header",  "ts": "<ISO8601>" }
      ]
    }
  ]
}
```

**blob**  
- Rått innehåll. Filnamn = sha256.

---

## P-KLS (Kontext‑verifiering vid långa sessioner)

**Trigger:** `(turn_count ≥ 20)` **AND** `intent:"edit_file"` **AND** filen finns i LK-index.  
**Åtgärd:** Kör **LK_VERIFY_BASELINE(file)**. Vid mismatch:
- Säg: “Kontexten för `<fil>` är föråldrad (sha mismatch). Ladda aktuell version eller bekräfta explicit att jag ska arbeta mot LK@senaste.”  
**Fortsättning:** Implementering får endast ske om baseline matchar **eller** användaren explicit bekräftar arbete mot LK@senaste.

---

## DynamicProtocols (krokar för generatorn)

1) **DP-LK-VERIFY-ON-EDIT-01**  
   - `event: "turn_committed"`  
   - `conditions`: `[{ "intent":"edit_file", "file_in_lk_index": true }]`  
   - `steps`:
     - `CHECK_COMPLIANCE`: förvarna om krav på `anchor_diff_v3.0` vid kommande commit
     - `GENERATE_REPORT`: template `LK_VERIFY_NOTICE` → `reports_queue`
     - `APPEND_TO_REGISTER`: `{ event:"lk_verify_candidate", file }`

2) **DP-LK-AUTO-COMMIT-ON-ANSWER-01**  
   - `event: "patch_committed"`  
   - `steps`:
     - `QUERY_FILE`: `.tmp/living_context/index.json` (required)
     - `SANDBOX_EXEC`/`EXEC`: kör LK_COMMIT(file, content, note_from_patch)
     - `APPEND_TO_REGISTER`: `{ event:"lk_commit", file, rev }`

3) **DP-LK-BOOTSTRAP-ON-START-01**  
   - `event: "new_session_start"`  
   - `steps`:
     - Om `.tmp/living_context` saknas men DJTA har `living_context_snapshot`: återskapa index+blobs.
     - `APPEND_TO_REGISTER`: `{ event:"lk_bootstrap", files: <n> }`

---

## Avslut (session_end)

- Bifoga `living_context_snapshot` i **DJTA Block A** (AI_Chatt_Avslutningsprotokoll.md):
```json
{
  "living_context_snapshot": {
    "files": [
      { "file": "src/App.tsx", "latest_rev": "v7", "sha256": "<64-hex>" }
    ]
  }
}
```
- Nästa session kan bootstrap:a från snapshot om `.tmp/living_context` saknas.

---

## Implementationsnoter
- Lågt hinder: index är litet; blobbar dedupliceras via sha256.
- LK används för **kontextspårning**, inte som enda sanning för källkod. Riktig källa = repo/användarfil.
- Om användare laddar ny version utan LK‑koppling: kör **LK_VERIFY_BASELINE** och skapa ny rev.
