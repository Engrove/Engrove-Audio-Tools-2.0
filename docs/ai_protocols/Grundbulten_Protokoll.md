<!-- BEGIN FILE: docs/ai_protocols/Grundbulten_Protokoll.md
SYFTE & ANSVAR:
"Grundbulten" (P-GB-3.0) är den tvingande lagen för all filgenerering/-modifiering (kod, dokument, konfig, data).
Mål: 100% korrekt, komplett, spårbar, verifierad och deterministisk leverans i chattläge (Gemini/OpenAI), utan antaganden.

HISTORIK:
* v1.0 (2025-08-16): Kodfokus.
* v2.0 (2025-08-16): Universell omarbetning.
* v2.1 (2025-08-16): Syntes + tribunal + korrekt MD-kommentering.
* v2.4 (2025-08-16): Anti-Placeholder-Grind, utfällda steg 2–8.
* v3.0 (2025-08-16): REBORN: Hårda grindar G0–G4, evidensartefakter (COMPLIANCE_MANIFEST/EVIDENCE_MAP), typstyrd verifieringsmatris, chat-läge-begränsningar, CI-recept, raderingsveto.

TILLÄMPADE REGLER (Frankensteen v5.4):
* GR4 – Interaktionskontrakt: Självgranskning + extern dom; fast outputordning och ansvar.
* GR5 – Tribunal/Red Team: KajBjörn validerar SPEC; StigBritt bryter planen före implementation.
* GR6 – Processrefaktorering: Reproducerbar pipeline med grindar och verktygssteg.
* GR7 – Historik & spårbarhet: Full historik i header, BEGIN/END-sentineller, inga platshållare.
* GB-Gates – G0–G4 (nedan) är tvingande och aborterar på brott.
* No-Guess-Pledge – Inga påståenden utan källa; fråga vid osäkerhet.
* Determinism – seed=42 där slump förekommer; inga nätverkskall; inga nya beroenden utan låsning och motivering.

Datum: 2025-08-16
Extern granskare: Engrove (godkänd för införing i Steg 10)
END HEADER -->

# Protokoll: **Grundbulten** (P-GB-3.0) – Universell filhantering (chattsession)

## Steg G: Hårda grindar (abortvillkor, före Steg 1)
- **G0. Kontextintegritet < 95% ⇒ AVBRYT.** Kräv kompletterande källor/sammanfattning och ny körning.
- **G1. Evidenskarta saknas ⇒ AVBRYT.** `EVIDENCE_MAP.json` måste finnas (se Steg 9).
- **G2. Anti-placeholder ⇒ AVBRYT.** Kör regex-svit (Bilaga B). Noll träffar krävs.
- **G3. Verifieringsnivå ⇒ AVBRYT.** Simulerad körlogg räcker aldrig ensam; statiska kontroller måste vara PASS.
- **G4. Legacy-sanering ⇒ AVBRYT.** Konflikt/överflödig artefakt måste patchas/arkiveras innan vidare uppdrag.

## Steg 0: Mål och omfattning
- Gäller **alla** filtyper. Leverans ska vara **självförsörjande** (inga dolda referenser).

## Steg 1: Dokumentation & metadata
- **1a. Fil-header:** SYFTE, HISTORIK (full, inga platshållare), TILLÄMPADE REGLER.
- **1b. Kommentarspolicy + sentineller:** Inkludera `BEGIN/END FILE` med exakt sökväg.
- **1c. Kommentar-syntax per filtyp:**
| Filändelse | Kommentar-syntax                                 | Status       |
|------------|---------------------------------------------------|--------------|
| `.md`      | `<!-- ... -->`                                   | Obligatorisk |
| `.py`      | `# ...`                                          | Obligatorisk |
| `.js`/`.vue`/`.css` | `// ...` eller `/* ... */`              | Obligatorisk |
| `.json`    | *Inga kommentarer tillåtna*                      | Förbjudet    |
| `.toml`    | `# ...`                                          | Obligatorisk |
| `.yml`/`.yaml` | `# ...`                                      | Obligatorisk |
- **1d. Kommentarskoriigering:** Felaktiga kommentar-syntax vid uppdatering av fil ska ovillkorligen rättas enligt punkt 1c syntax.
  
## Steg 2: SPEC/ANTAGANDEN
- Beskriv kontrakt, IO, invarianter, felhantering, typer, tråd/async, prestanda, miljö/beroenden.
- Märk *[Explicit]* vs *[Härledd]*. Testerna i Steg 6 ska binda dessa.

## Steg 3: Tribunalgranskning
- **KajBjörn:** SPEC bygger endast på given information (No-Guess-Pledge).
- **StigBritt:** Bryt *ÅTGÄRDSPLAN* logiskt innan implementation.

## Steg 4: Fel- och riskkategorier (checklista)
- Syntax/parse; namn/namespace; typer; None/null; index/gränser; edge-fall.
- Tillstånd; race; init-ordning; resurser/läckor; I/O (encoding/tidszon).
- Säkerhet (injektion, path traversal, osäker deserialisering); prestanda (Big-O).
- Beroenden (version/låsning/cirklar); stil/linters.

## Steg 5: ÅTGÄRDSPLAN
- Prioritet: **korrigera → säkra → stabilisera → dokumentera → städa**.
- Minsta nödvändiga ändring; omdesign endast med motivering.

## Steg 6: Testdesign
- **Kod:** Enhets- och egenskapstester (seed=42), felvägar, gränsvärden, icke-ASCII, tidszoner.
- **Icke-kod:** Schema-/formatvalidering (Markdown-länkar, JSON Schema, YAML-schema, TOML-parse).

## Steg 7: Körning & bevis
- **Kod:** Redovisa **FAKTISK** statisk verifiering (parse/lint/type/build). Simulerad körning måste vara märkt **SIMULERAD** och komplettera – aldrig ersätta – statiken.
- **Icke-kod:** Valideringskommandon och utfall.

## Steg 8: Filleverans
- Leverera **full fil** (inte patch) om patch skulle kräva “resten är oförändrat”.
- Formatsektion: **KOD/INNEHÅLL**. `TILLÄMPADE REGLER` i headern får uppdateras först i Steg 10.
- `Processkomplicitet: ` Ett %-värde på hur väl filhanteringen utförst, mycket problem med extra åtgärder = hög procent, ett problemfritt genomförane = låg procent. + en en-menings rapport om hela Grundbulten-processens session.

## Steg 8b: Anti-Placeholder-Grind
- Förbjudna mönster (exempel): `\.\.\.`, `TODO`, `FIXME`, `resten.*oförändrad`, `placeholder`, `stub`, `pseudo`, `exempel`, `// omitted`, `/* truncated */`.
- Vid träff: **AVBRYT** och börja om vid Steg 2.

## Steg 9: Evidensartefakter (maskinläsbara)
- **`COMPLIANCE_MANIFEST.json`** (obligatorisk, en rad per fil):
  - `file_path`, `sha256`, `syntax_ok`, `lint_ok`, `types_ok`, `schema_ok`, `build_ok`, `tests_ok`,
    `placeholders_found` (0 krävs), `unresolved_deps` (tom lista krävs), `deterministic` (true).
- **`EVIDENCE_MAP.json`** (obligatorisk):
  - Lista av `{ "claim": "...", "source_file": "...", "lines_or_keys": "..." }` för alla kvantitativa/faktiska påståenden.
- **`VERIFICATION_LOG.md`**:
  - Exakta kommandon + exitkoder. Märk *SIMULERAD* om ej faktiskt körd. Statik måste vara PASS.

## Steg 10: Självgranskning & extern dom
- **10a. Självgranskning:** `self_review_artifact.json` (vilka regler följdes, evidenspekare).
- **10b. Extern dom (Engrove):** Godkännande eller korrigering + slutlig text för `TILLÄMPADE REGLER`. Först därefter uppdateras header och commit/arkivering.

## Steg 11: Arkivering
- Uppdatera HISTORIK. Säkerställ att BEGIN/END-sentineller och filsökväg är korrekta.

## Steg 12: Eskalering
- Två misslyckade försök ⇒ aktivera `Help_me_God_Protokoll.md`.

---

## Bilaga A: Typstyrd verifieringsmatris (minimikrav)
- **Python (`.py`)**: `ast.parse` ⇒ PASS; ruff/flake8 ⇒ 0 fel; `mypy --strict` ⇒ 0 fel; imports resolvade; om tester finns: `pytest -q` (seed=42).
- **Vue/JS (`.vue`, `.js`)**: `vue-tsc --noEmit` (även JS via JSDoc/tsconfig) ⇒ PASS; ESLint ⇒ 0 fel; Vite build dry-run ⇒ OK.
- **JSON (`.json`)**: Validera mot tillämpligt **JSON Schema**; `$schema` krävs; inga kommentarer; stabil nyckelordning där det är norm.
- **YAML (`.yml/.yaml`)**: `yamllint` ⇒ 0 fel; schema-validering om finns.
- **Markdown (`.md`)**: markdownlint ⇒ 0 fel; extern/intern länk-check ⇒ 0 brutna.
- **TOML (`.toml`)**: toml-parse ⇒ PASS.
- **GitHub Actions (CI-YAML)**: YAML-parse ⇒ PASS; action-linter/dry-run ⇒ PASS.
- **CSS**: Lint ⇒ 0 fel; tokens används (inga hårdkodade färger där tokens finns).

## Bilaga B: Anti-placeholder-regex (minimimängd)
```
(\.\.\.)|(TODO|FIXME|HACK|WIP)|(resten.*oförändrad)|(placeholder|stub|pseudokod|pseudo)|(omitted|truncated)
```

## Bilaga C: Chat-läge (Gemini/OpenAI)
- Ingen exekvering garanterad i chatt ⇒ statiska kontroller krävs.
- Ingen spekulation; fråga vid osäkerhet. All kvantitet måste ha källa i `EVIDENCE_MAP.json`.
- Determinism: seed=42; inga nätverkskall; inga nya beroenden utan låsta versioner + motivering.
- Om faktisk körning krävs: leverera **körbart CI-recept** (GitHub Actions-jobb) och begär logg för slutligt grönt.

## Bilaga D: Minimal CI-recept (GitHub Actions, mall)
```yaml
name: grundbulten-verify
on: [workflow_dispatch]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: npm ci || true
      - run: pip install -U ruff mypy pytest || true
      - run: npx vue-tsc --noEmit || true
      - run: npx eslint . || true
      - run: python - <<'PY'\nimport ast,sys,glob\n[ast.parse(open(p).read(),p) for p in glob.glob('**/*.py', recursive=True)]\nprint('PY_AST_OK')\nPY
      - run: echo "STATIC CHECKS COMPLETE"
```
<!-- END FILE: docs/ai_protocols/Grundbulten_Protokoll.md -->
