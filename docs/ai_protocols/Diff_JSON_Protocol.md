
# docs/ai_protocols/Diff_Protocol.md
#
# === SYFTE & ANSVAR ===
# Detta dokument definierar den definitiva version 3.0 av Engrove Diff Protocol.
# Det är den enda, auktoritativa sanningskällan för hur patch-filer ska struktureras.
# Protokollet använder ett text-ankare-baserat system för att säkerställa robusthet
# mot mindre textförskjutningar.
#
# === HISTORIK ===
# * v1.0 (2025-08-10): Initialt protokoll baserat på numeriska index (`diff_json_v1`). Deprekerad.
# * v2.1 (2025-08-11): Intern implementation i verktyg (`anchor_diff_v2.1`), men aldrig formellt dokumenterad.
# * v3.0 (2025-08-11): Detta dokument. Skapat som en del av en "Stalemate Protocol"-upplösning
#   för att skapa en enda, otvetydig sanningskälla. Slår samman och formaliserar
#   den implementerade `anchor_diff_v2.1`-logiken.
#
# === TILLÄMPADE REGLER (Frankensteen v5.0) ===
# - "Help me God": Denna specifikation är resultatet av en grundorsaksanalys.

## 1. Protokoll-ID
- **`protocol_id`**: Måste vara exakt strängen `"anchor_diff_v2.1"`.

## 2. Kanonisering
- **Teckenkodning**: UTF-8
- **BOM**: Måste tas bort.
- **Radslut**: Alla radslut (CRLF/CR) måste normaliseras till LF (`\n`).
- **`base_checksum_sha256`**: Är en 64-tecken hex-sträng som representerar basfilens SHA-256-hash.

## 3. JSON-Struktur
```json
{
  "protocol_id": "anchor_diff_v2.1",
  "target": {
    "path": "sökväg/till/fil.js",
    "base_checksum_sha256": "<64 hex>"
  },
  "op_groups": [
    {
      "anchor": {
        "text": "En unik textsträng i filen",
        "match_mode": "exact"
      },
      "targets": [
        {
          "op": "replace_block",
          "match_index": 1,
          "old_block": "Textblocket som ska ersättas.",
          "new_block": "Det nya textblocket."
        }
      ]
    }
  ],
  "result_sha256": "<64 hex, valfri>",
  "meta": {
    "notes": "Valfri beskrivning av patchen."
  }
}
```

## 4. Fältdefinitioner och Regler

- **`target`** (objekt, krävs):
    - **`path`** (sträng, rekommenderas): Den relativa sökvägen till målfilen.
    - **`base_checksum_sha256`** (sträng, krävs): SHA-256-hashen av basfilen.

- **`op_groups`** (array, krävs): En lista av operationsgrupper. Varje grupp är en logisk operation som utgår från ett ankare.
    - **`anchor`** (objekt, krävs): Definierar en unik referenspunkt i basfilen.
        - **`text`** (sträng, krävs): Den exakta textsträngen att söka efter.
        - **`match_mode`** (sträng, valfri, default: `exact`): Kan vara `exact` eller `ignore_whitespace`.
    - **`targets`** (array, krävs): En lista av operationer att utföra relativt till ankaret.
        - **`op`** (sträng, krävs): Typ av operation. Giltiga värden:
            - `"replace_block"`: Ersätter ett textblock som omedelbart följer ankaret.
            - `"delete_block"`: Raderar ett textblock som omedelbart följer ankaret.
            - `"replace_entire_file"`: Ersätter hela filens innehåll. `anchor` och `old_block` ignoreras.
        - **`match_index`** (heltal, valfri, default: `1`): Om ankaret finns flera gånger, specificerar detta vilken instans som avses (1-baserad).
        - **`old_block`** (sträng, krävs för `replace_block`, `delete_block`): Den exakta texten som ska tas bort/ersättas.
        - **`new_block`** (sträng, krävs för `replace_block`): Den nya texten som ska infogas.
        - **`new_content`** (sträng, krävs för `replace_entire_file`): Det nya, fullständiga filinnehållet.

- **`result_sha256`** (sträng, valfri): SHA-256-hashen av filen *efter* att alla operationer har applicerats. Används för verifiering.

- **`meta`** (objekt, valfri): Innehåller metadata om patchen.
```
