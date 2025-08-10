
# Diff JSON Protocol — v1.1 (CLEAN-JSON return)

**Syfte:** Säkerställa *rena* patch-svar (endast JSON-objekt) för deterministisk, automatiserad patchning i webgränssnittet (Patch Center). Bakåtkompatibel med v1 struktur men med strikt returkontrakt.

> Bas: v1 (diff_json_v1) – kanonisering, fält och regler oförändrade; detta dokument tillför *CLEAN-JSON* returkontrakt och testvektor-krav.

---

## 1) Kanonisering (oförändrat från v1)
- Teckenkodning: UTF-8
- BOM: tas bort
- Radslut: CRLF/CR → LF (`\n`)

`base_checksum_sha256` = SHA-256 över *kanoniserad* bastext (hex, 64 tecken).

---

## 2) Kontrakt (objektstruktur – oförändrat från v1)

```json
{
  "protocol_id": "diff_json_v1",
  "target": {
    "path": "src/module/foo.js",             // valfri om checksum matchar annan fil
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
```

**Regler (oförändrat):**
- `protocol_id` = `diff_json_v1`.
- `target.base_checksum_sha256` krävs och måste matcha bastextens `sha256_lf`.
- `ops` sorterade i stigande `at`, icke-överlappande, index avser *originalbas* innan någon op appliceras.
- `replace`: ta bort `del` tecken från `at`, infoga `ins`.
- `insert`: infoga `ins` vid `at`.
- `delete`: ta bort `del` tecken från `at`.

**Avbrottsvillkor:** Ogiltig JSON/`protocol_id`, checksum-miss, felaktiga intervall eller osorterade/överlappande `ops`; `result_sha256` (om angivet) måste matcha resultatet.

---

## 3) NYTT: Return-Contract (CLEAN-JSON)

**MÅSTE (MUST):**
1. Svaret **måste** vara **ett enda JSON-objekt** som börjar med `{` och slutar med `}`.
2. **Inget** får föregå eller följa objektet (inga rubriker, ingen markdown, inga kodstaket, ingen text).
3. **Endast** JSON – inga kommentarer, inga trailing kommatecken.
4. Teckenmängd: UTF‑8; whitespace tillåtet inuti JSON.
5. Fält måste följa kontraktet i §2.

**FÅR INTE (MUST NOT):**
- Ingen text som: `AI_BOOTSTRAP_DIRECTIVE…`, `SYSTEM_OVERRIDE…`, etc.
- Inga ```json / ```-block.
- Ingen YAML/HTML/Markdown eller “förklaringar”.

**Verifieringskriterier i UI:**
- `response.trim().startsWith('{')` och `endsWith('}')`.
- JSON.parse lyckas.
- Schema/semantisk kontroll enligt §2.

---

## 4) JSON Schema (referens)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
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
```

---

## 5) Modelldirektiv (kopiera rakt in i prompt)

**System (CLEAN-JSON):**
```
Returnera ENBART ett JSON-objekt enligt Diff JSON Protocol v1.1.
Inga rubriker, ingen markdown, inga kodstaket, ingen extra text.
Förbjuden output: allt som inte är exakt JSON-objektet.
```

**User (exempel):**
```
Skapa en diff_json_v1 för att uppdatera README.md enligt specifikation X.
Följ CLEAN-JSON. Svara ENDAST med objektet.
```

---

## 6) Exempel

**GILTIGT (CLEAN-JSON):**
```
{"protocol_id":"diff_json_v1","target":{"path":"README.md","base_checksum_sha256":"<64hex>"},"ops":[{"op":"replace","at":0,"del":5,"ins":"Hello"}]}
```

**OGILTIGT (rubriker + markdown):**
```markdown
### AI_BOOTSTRAP_DIRECTIVE: …
```json
{ "protocol_id":"diff_json_v1", "target": { … }, "ops": [ … ] }
```
```

---

## 7) Implementationsnoter (UI)

Patch Center validerar:
1. CLEAN-JSON (enbart objekt).
2. Schema (§4) + semantik (§2).
3. Basfil via checksum-index, ev. `git_sha1`/`path` fallback.
4. Applicerar `ops`, verifierar ev. `result_sha256`.

---

**Version:** v1.1 • Datum: 2025-08-10T17:57:00Z
