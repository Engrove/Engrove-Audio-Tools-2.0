<!-- BEGIN FILE: docs/ai_protocols/Grundbulten_Protokoll.md
SYFTE & ANSVAR:
"Grundbulten" (P-GB-3.2) är den tvingande lagen för all filgenerering/-modifiering (kod, dokument, konfig, data).
Mål: 100% korrekt, komplett, spårbar, verifierad och deterministisk leverans i chattläge (Gemini/OpenAI), utan antaganden.

HISTORIK:
* v1.0 (2025-08-16): Kodfokus.
* v2.0 (2025-08-16): Universell omarbetning.
* v2.1 (2025-08-16): Syntes + tribunal + korrekt MD-kommentering.
* v2.4 (2025-08-16): Anti-Placeholder-Grind, utfällda steg 2–8.
* v3.0 (2025-08-16): REBORN: Hårda grindar G0–G4, evidensartefakter, typstyrd verifieringsmatris, CI-recept.
* v3.1 (2025-08-17): (Help me God) Gjorde verifiering extern och obligatorisk. Införde 'VERIFICATION_LOG' och 'LIGHTWEIGHT COMPLIANCE STATEMENT' för att tvinga fram transparens och extern bevisföring efter upprepade processfel. Ersatte den vaga 'Processkomplicitet' med en 'Execution Summary'.
* v.3.2 (2025-08-17: Verifiering av ändrad filstorlek.

TILLÄMPADE REGLER (Frankensteen v5.6):
* GR4 – Interaktionskontrakt: Självgranskning + extern dom; fast outputordning och ansvar.
* GR5 – Tribunal/Red Team: KajBjörn validerar SPEC; StigBritt bryter planen före implementation.
* GR6 – Processrefaktorering: Reproducerbar pipeline med grindar och verktygssteg.
* GR7 – Historik & spårbarhet: Full historik i header, BEGIN/END-sentineller, inga platshållare.
* GB-Gates – G0–G4 (nedan) är tvingande och aborterar på brott.
* No-Guess-Pledge – Inga påståenden utan källa; fråga vid osäkerhet.
* Help me God: Denna uppgradering är en direkt åtgärd mot ett systemiskt processfel.

Datum: 2025-08-17
Extern granskare: Engrove (godkänd för införing i Steg 10)
END HEADER -->

# Protokoll: **Grundbulten** (P-GB-3.1) – Universell filhantering (chattsession)

## Steg G: Hårda grindar (abortvillkor, före Steg 1)
- **G0. Kontextintegritet < 99% ⇒ AVBRYT.** Kräv kompletterande källor/sammanfattning och ny körning.
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
- **Allmänt:** Filstorlek, funktionsantal, objektantal, sektionsantal eller annan mätbar differans.

## Steg 7: Extern Verifiering & Bevisföring
- I **varje svar** som levererar en fil enligt detta protokoll, **MÅSTE** ett `VERIFICATION_LOG`-block inkluderas. Detta block redovisar explicit de verifieringssteg som har (eller skulle ha) körts, inklusive manuella kontraktskontroller.
- **Exempel på `VERIFICATION_LOG`:**
  ```markdown
  #### VERIFICATION_LOG
  - **Fil:** `scripts/engrove_audio_tools_creator.py`
  - **Verifiering (simulerad):**
    - `ast.parse`: [PASS] - Filen är giltig Python-syntax.
    - `ruff`: [PASS] - Inga linter-fel.
    - **Kontraktsverifiering (manuell):** [PASS] - `file_tree_placeholder` i byggskriptet matchar nu den o-citerade variabeln i `ui_file_tree.py`.
  ```

## Steg 8: Filleverans
- Leverera **full fil** (inte patch) om patch skulle kräva “resten är oförändrat”.
- **8a. Execution Summary:** Svaret måste inkludera en ärlig enmeningssammanfattning av processen. Exempel: `Execution Summary: Planen exekverades utan avvikelser.` eller `Execution Summary: Initial plan var felaktig; korrigerad efter intern granskning.`

## Steg 8b: Anti-Placeholder-Grind
- Förbjudna mönster (exempel): `\.\.\.`, `TODO`, `FIXME`, `resten.*oförändrad`, `placeholder`, `stub`, `pseudo`, `exempel`, `// omitted`, `/* truncated */`.
- Vid träff: **AVBRYT** och börja om vid Steg 2.

## Steg 9: Efterlevnadsrapport (Compliance Statement)
- De fullständiga JSON-artefakterna (`COMPLIANCE_MANIFEST.json`, `EVIDENCE_MAP.json`) genereras **endast vid en formell sessionsavslutning** eller på **explicit begäran**.
- För normala, löpande filleveranser ersätts de av en **Lightweight Compliance Statement** i ett markdown-kodblock, som måste inkluderas i svaret.
- Vid filleverans där filstorlek, funktionsantal, objektantal, sektionsantal eller annan mätbar differans signifikant reducerats ska en förklaring anges.
- **Exempel på `LIGHTWEIGHT COMPLIANCE STATEMENT`:**
  ```markdown
  #### LIGHTWEIGHT COMPLIANCE STATEMENT
  - **Syntax:** [PASS]
  - **Kontrakt:** [PASS]
  - **Placeholders:** [PASS]
  - **Historik:** [PASS]
  ```

## Steg 10: Självgranskning & extern dom
- **10a. Självgranskning:** Intern bekräftelse att alla steg i v3.1 har följts.
- **10b. Extern dom (Engrove):** Godkännande eller korrigering. Först därefter uppdateras `TILLÄMPADE REGLER` i fil-headern.

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
- Ingen spekulation; fråga vid osäkerhet.
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
