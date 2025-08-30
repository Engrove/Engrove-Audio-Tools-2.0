# docs/ai_protocols/JSON_Diff_Protocol.md
# v1.0

# === SYFTE & ANSVAR ===
# Detta protokoll definierar "json_diff", en anpassad standard för att applicera
# strukturerade, ankar-baserade ändringar på textbaserade filer av alla typer.
# Till skillnad från traditionella diff-format (som unified diff), använder
# detta format JSON för att garantera spårbarhet, atomicitet och verifierbarhet
# genom att binda varje operation till en specifik checksumma av basfilen.
#
# Protokollet är en "en-fils-lösning" som innehåller både den mänskliga
# beskrivningen och det maskinläsbara JSON-schemat för validering.
#
# === ANVÄNDNING ===
# 1.  **Validering:** Ett `json_diff`-objekt måste först valideras mot det
#     inbäddade schemat.
# 2.  **Basfils-verifiering:** Systemet som applicerar patchen MÅSTE lokalisera
#     originalfilen baserat på `target.base_checksum_sha256` och verifiera att
#     dess checksumma stämmer. Detta är ett absolut krav för att förhindra
#     att en patch appliceras på fel version.
# 3.  **Operation:** Systemet itererar genom `op_groups`, hittar varje `anchor`,
#     och applicerar sedan de specificerade operationerna (`targets`).
# 4.  **Resultat-verifiering (valfritt):** Om `result_sha256` finns, beräknas
#     checksumman på den modifierade filen och jämförs för en sista
#     integritetskontroll.

```json
{
  "protocolId": "P-JDIFF-1.0",
  "title": "JSON Diff Protocol",
  "version": "1.0",
  "description": "Formell definition och schema för det ankar-baserade JSON-patch-formatet 'json_diff'.",
  "strict_mode": true,
  "mode": "literal",
  "schema": {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "JSON Diff Patch Object (json_diff)",
    "description": "En strukturerad instruktion för att modifiera en textfil baserat på en verifierad bas-checksumma och textankare.",
    "type": "object",
    "required": [
      "protocol_id",
      "target",
      "op_groups"
    ],
    "properties": {
      "protocol_id": {
        "type": "string",
        "description": "Identifierare för patch-protokollet. Måste vara 'json_diff'.",
        "enum": [
          "json_diff"
        ]
      },
      "target": {
        "type": "object",
        "description": "Beskriver målfilen som ska patchas.",
        "required": [
          "base_checksum_sha256"
        ],
        "properties": {
          "path": {
            "type": "string",
            "description": "Valfri men starkt rekommenderad sökväg till målfilen. Används som en fallback för att hitta filen."
          },
          "base_checksum_sha256": {
            "type": "string",
            "description": "Den obligatoriska SHA-256-checksumman (LF-normaliserad) av den exakta filversionen som patchen är avsedd för.",
            "pattern": "^[a-f0-9]{64}$"
          }
        }
      },
      "op_groups": {
        "type": "array",
        "description": "En lista av operationsgrupper. Varje grupp är bunden till ett unikt textankare i basfilen.",
        "items": {
          "type": "object",
          "required": [
            "anchor",
            "targets"
          ],
          "properties": {
            "anchor": {
              "type": "object",
              "description": "En unik textsnutt i basfilen som fungerar som startpunkt för operationerna.",
              "required": [
                "text"
              ],
              "properties": {
                "text": {
                  "type": "string",
                  "description": "Ankartexten. Måste finnas i basfilen."
                },
                "match_mode": {
                  "type": "string",
                  "description": "Anger hur ankartexten ska matchas.",
                  "enum": [
                    "exact"
                  ],
                  "default": "exact"
                }
              }
            },
            "targets": {
              "type": "array",
              "description": "En lista av operationer att utföra efter att ankaret har hittats.",
              "items": {
                "type": "object",
                "required": [
                  "op"
                ],
                "properties": {
                  "op": {
                    "type": "string",
                    "description": "Typ av operation.",
                    "enum": [
                      "replace_block",
                      "delete_block",
                      "replace_entire_file"
                    ]
                  },
                  "match_index": {
                    "type": "integer",
                    "description": "Används om samma `old_block` förekommer flera gånger efter samma ankare. 1-baserat.",
                    "minimum": 1,
                    "default": 1
                  },
                  "old_block": {
                    "type": "string",
                    "description": "Det textblock som ska modifieras eller tas bort. Krävs för 'replace_block' och 'delete_block'."
                  },
                  "new_block": {
                    "type": "string",
                    "description": "Det nya textblock som ersätter 'old_block'. Krävs för 'replace_block'."
                  },
                  "new_content": {
                    "type": "string",
                    "description": "Det kompletta nya innehållet för hela filen. Används endast med 'replace_entire_file'."
                  }
                }
              }
            }
          }
        }
      },
      "result_sha256": {
        "type": "string",
        "description": "Valfri men starkt rekommenderad. Den förväntade SHA-256-checksumman av filen EFTER att patchen har applicerats, för en sista integritetskontroll.",
        "pattern": "^[a-f0-9]{64}$"
      }
    }
  }
}
