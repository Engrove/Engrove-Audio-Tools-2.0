# Diff JSON Protocol — v1 (diff_json_v1)

## Syfte
Deterministiska textpatchar för filinnehåll i AI-drivet arbetsflöde.

## Kanonisering
All hashing och patchning sker på kanoniserad text:
- Teckenkodning: UTF-8
- BOM: tas bort
- Radslut: CRLF/CR → LF (`\n`)

`base_checksum_sha256` = SHA-256 över kanoniserad bastext (hex, 64 tecken).

## Kontrakt
```json
{
  "protocol_id": "diff_json_v1",
  "target": {
    "path": "src/module/foo.js",             // valfri om checksum träffar annan fil
    "base_checksum_sha256": "<64 hex>",      // krävs
    "git_sha1": "<40 hex>"                   // valfri
  },
  "ops": [
    { "op": "replace", "at": 125, "del": 10, "ins": "new text" },
    { "op": "insert",  "at": 200, "ins": "…" },
    { "op": "delete",  "at": 350, "del": 42 }
  ],
  "result_sha256": "<64 hex, valfri>",
  "meta": { "author": "AI|human", "notes": "valfritt" }
}

Regler

protocol_id = "diff_json_v1".

target.base_checksum_sha256 krävs; måste matcha bastextens sha256_lf.

ops:

sorterade i stigande at

icke-överlappande

index (at) avser originalbasen innan någon op appliceras.


replace: tar bort del tecken från at, infogar ins.

insert: infogar ins vid at.

delete: tar bort del tecken från at.


Fel som ska ge avbrott

Ogiltig JSON eller protocol_id.

base_checksum_sha256 matchar inte någon känd bas (checksum > path > git_sha1).

ops osorterade, överlappande, eller intervall utanför basens längd.

result_sha256 finns men matchar inte resultatet.


Exempel

Bas (kanoniserad):

alpha
beta
gamma

Patch:

{
  "protocol_id": "diff_json_v1",
  "target": { "path": "README.md", "base_checksum_sha256": "…64 hex…" },
  "ops": [
    { "op": "replace", "at": 6, "del": 4, "ins": "BETA" },
    { "op": "insert",  "at": 0, "ins": "# Title\n" }
  ],
  "meta": { "author": "AI" }
}

## tools/schemas/diff_json_v1.schema.json
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://engrove.dev/schemas/diff_json_v1.schema.json",
  "title": "Diff JSON v1",
  "type": "object",
  "additionalProperties": false,
  "required": ["protocol_id", "target", "ops"],
  "properties": {
    "protocol_id": { "const": "diff_json_v1" },
    "target": {
      "type": "object",
      "additionalProperties": false,
      "required": ["base_checksum_sha256"],
      "properties": {
        "path": { "type": "string", "minLength": 1 },
        "base_checksum_sha256": { "type": "string", "pattern": "^[0-9a-fA-F]{64}$" },
        "git_sha1": { "type": "string", "pattern": "^[0-9a-fA-F]{40}$" }
      }
    },
    "ops": {
      "type": "array",
      "minItems": 1,
      "items": {
        "oneOf": [
          {
            "type": "object",
            "additionalProperties": false,
            "required": ["op", "at", "ins"],
            "properties": {
              "op": { "const": "insert" },
              "at": { "type": "integer", "minimum": 0 },
              "ins": { "type": "string" }
            }
          },
          {
            "type": "object",
            "additionalProperties": false,
            "required": ["op", "at", "del"],
            "properties": {
              "op": { "const": "delete" },
              "at": { "type": "integer", "minimum": 0 },
              "del": { "type": "integer", "minimum": 1 }
            }
          },
          {
            "type": "object",
            "additionalProperties": false,
            "required": ["op", "at", "del", "ins"],
            "properties": {
              "op": { "const": "replace" },
              "at": { "type": "integer", "minimum": 0 },
              "del": { "type": "integer", "minimum": 0 },
              "ins": { "type": "string" }
            }
          }
        ]
      }
    },
    "result_sha256": { "type": "string", "pattern": "^[0-9a-fA-F]{64}$" },
    "meta": { "type": "object" }
  }
}
