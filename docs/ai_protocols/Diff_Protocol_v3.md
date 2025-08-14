# Engrove Diff Protocol v3.0: Boundary Protocol
# docs/ai_protocols/Diff_Protocol_v3.md
#
# === SYFTE & ANSVAR ===
# Detta dokument definierar den definitiva version 3.0 av Engrove Diff Protocol.
# Det är den enda, auktoritativa sanningskällan för hur patch-filer ska struktureras.
# Protokollet använder ett system med dubbla gränsankare ("Boundary Anchors") för att
# eliminera den bräcklighet som fanns i v2.1 och säkerställa robusthet mot
# ändringar i innehållet som ska ersättas.
#
# === HISTORIK ===
# * v1.0 (2025-08-10): Initialt protokoll baserat på numeriska index (`diff_json_v1`). Deprekerad.
# * v2.1 (2025-08-11): Protokoll baserat på ett startankare och ett stort, bräckligt `old_block`. Deprekerad.
# * v3.0 (2025-08-14): Detta dokument. Skapat som en del av en grundorsaksanalys efter upprepade
#   patch-misslyckanden. Införlivar principen "definiera gränser, inte innehåll".
#
# === TILLÄMPADE REGLER (Frankensteen v5.4) ===
# - "Help me God": Denna specifikation är resultatet av en grundorsaksanalys av ett systemiskt fel.
# - Obligatorisk Refaktorisering: Protokollet har omdesignats för fundamental robusthet.

## 1. Protokoll-ID
- **`protocol_id`**: Måste vara exakt strängen `\"anchor_diff_v3.0\"`.

## 2. Kanonisering och Verifiering
- **Teckenkodning**: UTF-8.
- **BOM**: Måste tas bort.
- **Radslut**: Alla radslut (CRLF/CR) måste normaliseras till LF (`\n`).
- **Obligatorisk Checksum-Verifiering**: Innan en patch genereras, måste den exakta `base_checksum_sha256` för målfilen vara känd och verifierad. Att generera en patch mot en okänd eller inaktuell version är ett protokollbrott.

## 3. JSON-Struktur
```json
{
  "protocol_id": "anchor_diff_v3.0",
  "target": {
    "path": "sökväg/till/fil.js",
    "base_checksum_sha256": "<64 hex>"
  },
  "op_groups": [
    {
      "op": "replace_between_anchors",
      "start_anchor": {
        "text": "En unik textsträng som omedelbart föregår blocket som ska ändras.",
        "before_context": [ "Valfri array av rader för fuzzy matching." ]
      },
      "end_anchor": {
        "text": "En unik textsträng som omedelbart följer blocket som ska ändras.",
        "after_context": [ "Valfri array av rader för fuzzy matching." ]
      },
      "new_block": "Det nya textblocket som ska infogas mellan ankarna."
    }
  ],
  "meta": {
    "notes": "Valfri beskrivning av patchen."
  }
}
```

## 4. Fältdefinitioner och Regler

- **`target`** (objekt, krävs):
    - **`path`** (sträng, rekommenderas): Den relativa sökvägen till målfilen.
    - **`base_checksum_sha256`** (sträng, krävs): SHA-256-hashen av den exakta basfilen.

- **`op_groups`** (array, krävs): En lista av operationer.
    - **`op`** (sträng, krävs): Typ av operation. Giltiga värden:
        - `\"replace_between_anchors\"`: Ersätter allt innehåll mellan `start_anchor` och `end_anchor`.
    - **`start_anchor`** (objekt, krävs): Definierar startgränsen.
        - **`text`** (sträng, krävs): Den exakta textsträngen som markerar början. Denna text kommer att bevaras.
        - **`before_context`** (array av strängar, valfri): Används som fallback för att hitta ankaret om exakt matchning misslyckas.
    - **`end_anchor`** (objekt, krävs): Definierar slutgränsen.
        - **`text`** (sträng, krävs): Den exakta textsträngen som markerar slutet. Denna text kommer att bevaras.
        - **`after_context`** (array av strängar, valfri): Fallback för slutankaret.
    - **`new_block`** (sträng, krävs): Den nya texten som ska infogas.
