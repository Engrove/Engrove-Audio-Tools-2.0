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
