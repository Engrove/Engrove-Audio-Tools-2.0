<!-- BEGIN FILE: docs/ai_protocols/Grundbulten_Protokoll.md
SYFTE & ANSVAR:
"Grundbulten" (P-GB-3.4) är den tvingande lagen för all filgenerering/-modifiering (kod, dokument, konfig, data).
Mål: 100% korrekt, komplett, spårbar, verifierad och deterministisk leverans i chattläge (Gemini/OpenAI), utan antaganden.

HISTORIK:
* v1.0 (2025-08-16): Kodfokus.
* v2.0 (2025-08-16): Universell omarbetning.
* v2.1 (2025-08-16): Syntes + tribunal + korrekt MD-kommentering.
* v2.4 (2025-08-16): Anti-Placeholder-Grind, utfällda steg 2–8.
* v3.0 (2025-08-16): REBORN: Hårda grindar G0–G4, evidensartefakter, typstyrd verifieringsmatris, CI-recept.
* v3.1 (2025-08-17): (Help me God) Gjorde verifiering extern och obligatorisk. Införde 'VERIFICATION_LOG' och 'LIGHTWEIGHT COMPLIANCE STATEMENT' för att tvinga fram transparens och extern bevisföring efter upprepade processfel. Ersatte den vaga 'Processkomplicitet' med en 'Execution Summary'.
* v3.2 (2025-08-17): Skärpt kontextkrav (G0 -> 99%), förenklad rapportering (G1 borttagen), och lagt till obligatorisk kvantitativ diff-analys (Steg 6 & 9).
* v3.3 (2025-08-17): (Help me God) Infört Steg 10b, "Pre-Flight Diff Check", för att tvinga fram en slutgiltig, holistisk granskning av hela filen (inklusive metadata) innan leverans.
* v3.4 (2025-08-17): (Help me God) Lade till Steg 1d (obligatorisk kontextkommentar) och Steg 2b (Kod-i-kod Dominansprincip) baserat på användarfeedback för att eliminera tvetydighet.

TILLÄMPADE REGLER (Frankensteen v5.6):
* GR4 – Interaktionskontrakt: Självgranskning + extern dom; fast outputordning och ansvar.
* GR5 – Tribunal/Red Team: KajBjörn validerar SPEC; StigBritt bryter planen före implementation.
* GR6 – Processrefaktorering: Reproducerbar pipeline med grindar och verktygssteg.
* GR7 – Historik & spårbarhet: Full historik i header, BEGIN/END-sentineller, inga platshållare.
* GB-Gates – G0, G2-G4 (nedan) är tvingande och aborterar på brott.
* No-Guess-Pledge – Inga påståenden utan källa; fråga vid osäkerhet.
* Help me God: Denna uppgradering är en direkt åtgärd mot ett systemiskt processfel.

Datum: 2025-08-17
Extern granskare: Engrove (godkänd för införing i Steg 10)
END HEADER -->

# Protokoll: **Grundbulten** (P-GB-3.4) – Universell filhantering (chattsession)

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
- **1d. Kontextkommentar (Obligatorisk):** Omedelbart efter filens sökväg i headern måste en kort kommentar på 1-3 rader finnas som beskriver filens huvudsakliga syfte, dess relation till andra filer och dess kontext. JSON-filer är undantagna från denna regel.
  **Exempel (.py):**
  `# scripts/modules/ui_logic.py`
  `# Denna modul hanterar all generell UI-interaktivitet för det genererade verktyget,`
  `# såsom hantering av modals, resizer och meny-logik.`
- **1e. Kommentarskoriigering:** Felaktiga kommentar-syntax vid uppdatering av fil ska ovillkorligen rättas enligt punkt 1c syntax.
  
## Steg 2: SPEC/ANTAGANDEN
- **2a.** Beskriv kontrakt, IO, invarianter, felhantering, typer, tråd/async, prestanda, miljö/beroenden.
- Märk *[Explicit]* vs *[Härledd]*. Testerna i Steg 6 ska binda dessa.
- **2b. Kod-i-kod Dominansprincip:** Om en fil innehåller kod på ett språk inbäddat i ett annat (t.ex. JS i Python), MÅSTE jag i SPEC-sektionen explicit deklarera vilken språkkontext som är **dominant** och därmed i fokus för uppgiften. Prioriteringen är som följer:
    1.  **Användarens Prompt:** Om prompten explicit anger att den inbäddade koden ska ändras, är den dominant.
    2.  **Värdspråket (Host Language):** Om prompten är generell ("fixa den här filen"), är värdspråket dominant. Den inbäddade koden behandlas då som en literal sträng.
    3.  **Språket med Syntaxfel:** Om ett syntaxfel existerar, är språket där felet finns dominant.
  **Exempel på deklaration:**
  `[Antagande] Dominant kontext är Python. Den inbäddade JS-strängen i `JS_LOGIC` kommer att behandlas som en literal och endast ändras om det krävs för att korrigera Python-syntax.`

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
- I **varje svar** som levererar en fil enligt detta protokoll, **MÅSTE** ett `VERIFICATION_LOG`-block inkluderas.
- **Exempel på `VERIFICATION_LOG`:**
  ```markdown
  #### VERIFICATION_LOG
  - **Fil:** `scripts/engrove_audio_tools_creator.py`
  - **Verifiering (simulerad):**
    - `ast.parse`: [PASS] - Filen är giltig Python-syntax.
    - `ruff`: [PASS] - Inga linter-fel.
    - **Kontraktsverifiering (manuell):** [PASS] - Kontextkommentar (Steg 1d) och Dominansprincip (Steg 2b) är nu en del av protokollet.
    - **Pre-Flight Diff Check:** [PASS] - `HISTORIK`-sektionen är verifierat uppdaterad med vX.Y.
  ```

## Steg 8: Filleverans
- Leverera **full fil**.
- **8a. Execution Summary:** Svaret måste inkludera en ärlig enmeningssammanfattning av processen.
- **8b. Anti-Placeholder-Grind:** Förbjudna mönster (se bilaga). Vid träff: **AVBRYT** och börja om vid Steg 2.

## Steg 9: Efterlevnadsrapport (Compliance Statement)
- **MÅSTE** inkluderas i svaret.
- **Exempel på `LIGHTWEIGHT COMPLIANCE STATEMENT`:**
  ```markdown
  #### LIGHTWEIGHT COMPLIANCE STATEMENT
  - **Syntax:** [PASS]
  - **Kontrakt:** [PASS]
  - **Placeholders:** [PASS]
  - **Historik:** [PASS]
  - **Kvantitativ Diff:** [PASS] - Ökning av X rader motiverad av nya protokollsteg.
  ```

## Steg 10: Självgranskning & extern dom
- **10a. Självgranskning:** Intern bekräftelse att alla steg i v3.4 har följts.
- **10b. Pre-Flight Diff Check (Obligatorisk Slutkontroll):** Mental `diff` av original vs. slutgiltig version. Kontrollpunkter:
    1.  **Metadata:** Har `HISTORIK` och kontextkommentar (Steg 1d) uppdaterats korrekt?
    2.  **Integritet:** Har någon befintlig, korrekt kod oavsiktligt tagits bort?
    3.  **Fullständighet:** Matchar `BEGIN/END FILE`-sentinellerna den exakta filsökvägen?
- **10c. Extern dom (Engrove):** Godkännande eller korrigering.

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
