
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
- **`base_checksum_sha256`**: Är en 64-tecken hex-sträng som representerar SHA-256-hashen av den *kanoniserade* bastexten.

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
    - **`base_checksum_sha256`** (sträng, krävs): SHA-256-hashen av basfilen efter kanonisering.

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

---

### Artefakt 2: `Stalemate_Request.json`

Här är den begärda `Stalemate_Request.json`-artefakten. Den sammanfattar konflikten, listar de motstridiga hypoteserna, presenterar nya alternativa hypoteser och inkluderar all nödvändig bevisning för en extern granskare.

```json
{
  "protocol_id": "Stalemate_Protocol_v1.1",
  "session_timestamp": "2025-08-11T15:10:00Z",
  "stalemate_summary": "Oförmåga att applicera en anchor-baserad patch på filen 'scripts/wrap_json_in_html.py'. Valideringen i Patch Center-verktyget misslyckas upprepade gånger med felet 'Kunde inte hitta instans 1 av ankare', trots flera korrigeringsförsök.",
  "hypotheses": {
    "frankensteen_hypothesis": {
      "statement": "Felet berodde på en textuell artefakt ('9') i början av basfilen som korrumperade ankarmatchningen. En patch med ett mer robust ankare, som undviker filens början, borde fungera.",
      "justification": "Den initiala analysen visade en avvikelse i basfilens text. Logiken var att om ett ankare väljs som garanterat finns i den korrupta texten, så måste matchningen lyckas. Detta visade sig vara felaktigt."
    },
    "engrove_hypothesis": {
      "statement": "Det finns en fundamental, ännu oidentifierad, diskrepans mellan hur AI:n genererar ankare/patchar och hur verktygets JavaScript-logik tolkar dem, eller så är själva valideringslogiken i verktyget felaktig.",
      "justification": "Upprepade misslyckanden med olika, till synes giltiga, ankare pekar på ett systemiskt fel i antingen patch-genereringen eller patch-applikationen, snarare än ett enkelt problem med ett specifikt ankare."
    },
    "hallucinated_hypotheses": [
      {
        "statement": "JavaScript-funktionen `normalizeText` i verktyget är buggig eller implementerad på ett oväntat sätt.",
        "justification": "Om `normalizeText` (som används för `match_mode`) felaktigt tar bort eller ändrar tecken i antingen bastexten eller ankartexten på ett icke-standardiserat sätt, kommer `indexOf` aldrig att hitta en matchning, oavsett hur korrekt ankaret ser ut."
      },
      {
        "statement": "Det finns dolda, icke-utskrivbara tecken i de ankarsträngar jag genererar.",
        "justification": "En subtil skillnad i teckenkodning (t.ex. ett non-breaking space istället för ett vanligt mellanslag) mellan min genererade patch och filens faktiska innehåll skulle vara osynlig för blotta ögat men orsaka att `indexOf` misslyckas."
      },
      {
        "statement": "Ett DOM-timingproblem gör att `findBaseText`-funktionen läser en ofullständig eller tom version av basfilens innehåll.",
        "justification": "Om basfilens innehåll hämtas från `context.file_structure` (som är inbäddat i HTML) och JavaScriptet körs innan den datan är fullt tillgänglig, kan valideringen ske mot en tom sträng, vilket garanterat leder till att inget ankare hittas."
      }
    ]
  },
  "objective_evidence": [
    {
      "type": "error_log",
      "description": "Loggutdata från Patch Center-verktyget vid det senaste misslyckade försöket.",
      "content": "[patch 18:11:42] [INFO] Basfil hittad: scripts/wrap_json_in_html.py (källa: context.file_structure)\n[patch 18:11:42] [ERR] Valideringsfel: Kunde inte hitta instans 1 av ankare. Endast 0 hittades.\n[patch 18:11:42] [ERR] Validering misslyckades. Se logg för detaljer."
    },
    {
      "type": "file_content",
      "file_path": "scripts/wrap_json_in_html.py",
      "file_content": "[Fullständigt innehåll från föregående kontext, inklusive den inledande '9'-artefakten]"
    },
    {
      "type": "file_content",
      "file_path": "docs/ai_protocols/Diff_JSON_Protocol.md",
      "file_content": "[Fullständigt innehåll från föregående kontext, som beskriver det inkompatibla `diff_json_v1`-protokollet]"
    }
  ],
  "arbitration_request": "Agera som en oberoende teknisk skiljedomare. Givet de två motstridiga hypoteserna från parterna samt de alternativa, 'hallucinerade' hypoteserna, analysera den objektiva bevisningen (särskilt källkoden i `wrap_json_in_html.py`) och fastställ den definitiva grundorsaken till det upprepade patch-valideringsfelet. Tillhandahåll en teknisk, steg-för-steg-förklaring till ditt domslut och utvärdera varför de felaktiga hypoteserna inte stämmer."
}
```
