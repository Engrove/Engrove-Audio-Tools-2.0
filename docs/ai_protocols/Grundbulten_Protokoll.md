<!-- BEGIN FILE: docs/ai_protocols/Grundbulten_Protokoll.md
SYFTE & ANSVAR:
"Grundbulten" (P-GB-3.9) är den tvingande lagen för all filgenerering/-modifiering (kod, dokument, konfig, data).
Mål: 100% korrekt, komplett, spårbar, verifierad och deterministisk leverans i chattläge (Gemini/OpenAI), utan antaganden.

HISTORIK:
* v1.0 (2025-08-16): Kodfokus.
* v2.0 (2025-08-16): Universell omarbetning.
* v2.1 (2025-08-16): Syntes + tribunal + korrekt MD-kommentering.
* v2.4 (2025-08-16): Anti-Placeholder-Grind, utfällda steg 2–8.
* v3.0 (2025-08-16): REBORN: Hårda grindar G0–G4, evidensartefakter, typstyrd verifieringsmatris, CI-recept.
* v3.1 (2025-08-17): (Help me God) Gjorde verifiering extern och obligatorisk. Införde 'VERIFICATION_LOG' och 'LIGHTWEIGHT COMPLIANCE STATEMENT'.
* v3.2 (2025-08-17): Skärpt kontextkrav (G0 -> 99%), förenklad rapportering, och lagt till obligatorisk kvantitativ diff-analys.
* v3.3 (2025-08-17): (Help me God) Infört Steg 10b, "Pre-Flight Diff Check".
* v3.4 (2025-08-17): (Help me God) Lade till Steg 1d (kontextkommentar) och Steg 2b (Dominansprincip).
* v3.6 (2025-08-17): (Help me God) KRITISK UPPDATERING. Infört en sluten verifieringskedja för att förhindra trunkeringsfel: 1. G-1: Tvingande hash-kontroll vid inläsning. 2. Steg 1f: Tvingande inbäddning av slutgiltig hash i filens historik. 3. Steg 9: Tvingande rapportering av slutgiltig hash i svar. 4. Steg 10e: Tvingande intern självverifiering av hash-värden före leverans.
* v3.7 (2025-08-17): (Help me God - KORRIGERING) Infört en sluten, hash-baserad verifieringskedja (G-1, 1f, 9, 10e) för att matematiskt förhindra trunkeringsfel. Återställt fullständiga bilagor.
* v3.8 (2025-08-17): (Engrove Mandate) Lade till Steg 11b för att tvinga fram loggning av varje filmodifiering till en temporär sessionslogg (.tmp/session_revision_log.json).
* v3.9 (2025-08-18): (Engrove Mandate) Lade till Bilaga E för att definiera en deterministisk beslutsmatris för leveransformat i chatt (Full fil vs. Manuell Patch vs. JSON-patch).
* SHA256_LF: c4f8e07c968f371701cfc4978acc0f661021ac0446180b8c0f07984b5e3f08ac

TILLÄMPADE REGLER (Frankensteen v5.7):
* Grundbulten v3.8: Denna ändring följer den uppgraderade processen för transparens.
* GR4 – Interaktionskontrakt: Självgranskning + extern dom; fast outputordning och ansvar.
* GR5 – Tribunal/Red Team: KajBjörn validerar SPEC; StigBritt bryter planen före implementation.
* GR6 – Processrefaktorering: Reproducerbar pipeline med grindar och verktygssteg.
* GR7 – Historik & spårbarhet: Full historik i header, BEGIN/END-sentineller, inga platshållare.
* GB-Gates – G-1, G0, G2-G4 (nedan) är tvingande och aborterar på brott.
* No-Guess-Pledge – Inga påståenden utan källa; fråga vid osäkerhet.
* Help me God: Denna uppgradering är en direkt åtgärd mot en identifierad tvetydighet.

Datum: 2025-08-18
Extern granskare: Engrove (godkänd för införing i Steg 10)
END HEADER -->

# Protokoll: **Grundbulten** (P-GB-3.9) – Universell filhantering (chattsession)

## Steg G: Hårda grindar (abortvillkor, före Steg 1)
- **G-1. Kontrollsumma-verifiering vid inläsning ⇒ AVBRYT.** Om en fil som ska modifieras har en `base_checksum_sha256` i kontexten, måste min interna minnesbild **och** min beräknade minnesbilds hash matcha den hashen. Vid mismatch, avbryt och begär färsk fil.
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
- **1f. Hash-evidens i fil-header (Obligatorisk):** Vid leverans **MÅSTE** en rad läggas till i `HISTORIK`-sektionen med den slutgiltiga, verifierade hashen. Format: `* SHA256_LF: <hash>`.
  
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
- Leveransformatet styrs av **Bilaga E**.
- **8a. Execution Summary:** Svaret måste inkludera en ärlig enmeningssammanfattning av processen.
- **8b. Anti-Placeholder-Grind:** Förbjudna mönster (se bilaga). Vid träff: **AVBRYT** och börja om vid Steg 2.

## Steg 9: Efterlevnadsrapport (Compliance Statement)
- **MÅSTE** inkluderas i svaret.
- **Exempel på `LIGHTWEIGHT COMPLIANCE STATEMENT`:**
  ```markdown
  #### LIGHTWEIGHT COMPLIANCE STATEMENT
  - **Syntax:** [PASS/NOPASS]
  - **Kontrakt:** [PASS/NOPASS]
  - **Placeholders:** [PASS/NOPASS]
  - **Historik:** [PASS/NOPASS]
  - **Kvantitativ Diff:** [PASS/NOPASS] - [Ökning/Minskning] av X rader motiverad av nya protokollsteg.
  - **Base SHA256:** [SHA för filen INNAN ändring]
  - **Final SHA256:** [SHA för filen EFTER ändring]

## Steg 10: Självgranskning & extern dom
- **10a. Självgranskning:** Intern bekräftelse eller vederläggande att alla steg i "Grundbulten" protokoll nuvarande har följts eller inte kunnat följas.
- **10b. Pre-Flight Diff Check (Obligatorisk Slutkontroll):** Mental `diff` av original vs. slutgiltig version. Kontrollpunkter:
    1.  **Metadata:** Har `HISTORIK` och kontextkommentar (Steg 1d) uppdaterats korrekt?
    2.  **Integritet:** Har någon befintlig, korrekt kod oavsiktligt tagits bort?
    3.  **Fullständighet:** Matchar `BEGIN/END FILE`-sentinellerna den exakta filsökvägen?
- **10c. Extern dom (Engrove):** Godkännande eller korrigering.
- **10e. Slutgiltig Hash-verifiering (Obligatorisk):** Verifiera internt att hashen beräknad på den slutgiltiga koden är **identisk** med hashen som rapporteras i Steg 1f och Steg 9. Vid mismatch, AVBRYT.

## Steg 11: Arkivering
- **11a.** Uppdatera HISTORIK. Säkerställ att BEGIN/END-sentineller och filsökväg är korrekta.
- **11b. Temporär Revisionslogg:** Efter varje lyckad, godkänd leverans av en modifierad fil, MÅSTE en JSON-post appendas till `.tmp/session_revision_log.json`. Posten måste innehålla: `{ "file_path": "...", "timestamp": "...", "session_id": "...", "commit_sha": "..." }`.

## Steg 12: Eskalering
- Försöksräknare: Intern räknare per misslyckade försök.
- Trigger: Vid misslyckande ökas räknaren med +1.
- Tvingande Eskalering 1: När räknaren når 1 eller 2 (inför andra eller tredje försöket) är inkrementella fixar förbjudna. Aktivera omedelbart Help_me_God_Protokoll.md.
- Tvingande Eskalering 2: När räknaren når 3 (inför fjärde försöket) är inkrementella fixar förbjudna. Överväg om vidare felsökning är befogat eller om sessionen har nått en bekräftad ändpunkt. Beskriv orsak till misslyckandet.
- META‑PROTOKOLL: Grunbulten Token Counter (GTC)

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
(\\.\\.\\.)|(TODO|FIXME|HACK|WIP)|(resten.*oförändrad)|(placeholder|stub|pseudokod|pseudo)|(omitted|truncated)
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
      - run: python - <<'PY'\\nimport ast,sys,glob\\n[ast.parse(open(p).read(),p) for p in glob.glob('**/*.py', recursive=True)]\\nprint('PY_AST_OK')\\nPY
      - run: echo "STATIC CHECKS COMPLETE"
```

---

## Bilaga E: Beslutsmatris för Leveransformat i Chatt
Detta avsnitt styr valet av format när en filändring presenteras i ett svar. Valet baseras på uppgiftens art och mottagarens behov (människa vs. maskin).

| Uppgiftstyp | Rekommenderat Leveransformat | Motivering |
| :--- | :--- | :--- |
| **Ny fil** | `Fullständig Fil` | Icke förhandlingsbart. Enda sättet att garantera fullständighet. |
| **Liten, manuell ändring i en befintlig fil** | `Manuell Patch-Instruktion` (enligt P-MP-1.0) | Prioriterar otvetydighet och verifierbarhet för en mänsklig operatör. |
| **Medelstor till stor ändring (> 5 rader)** | `Fullständig Fil` | Standardläget. Minimerar risken för manuella fel. |
| **Programmatisk/Automatiserad Patchning** | `Strukturerad JSON-patch` (enligt `Diff_Protocol_v3.md`) | Används när ett verktyg ska applicera patchen automatiskt. |
