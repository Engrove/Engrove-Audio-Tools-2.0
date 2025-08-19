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

## Terminologi & policy
**REFRAKTOR-FLAG:** obligatorisk, när strukturen (inventarium/CLI) medvetet ändras. Utan flagga ⇒ ändringen blockeras av G5/10b.
**Kvantitativ diff-tröskel:** ±10 % som default; projekt kan skärpa i lokal policy.

## Steg G: Hårda grindar (abortvillkor, före Steg 1)
- **G-1. Kontrollsumma-verifiering vid inläsning ⇒ AVBRYT.** Om en fil som ska modifieras har en `base_checksum_sha256` i kontexten, måste min interna minnesbild **och** min beräknade minnesbilds hash matcha den hashen. Vid mismatch, avbryt och begär färsk fil.
- **G0. Kontextintegritet < 99% ⇒ AVBRYT.** Kräv kompletterande källor/sammanfattning och ny körning.
- **G1. Kontext-abort (tvingande):** Om is_content_full == false för målfilen ⇒ AVBRYT omedelbart och begär komplett fil + base_checksum_sha256. Inga patchar/regeneration tillåtna innan kontext = 100%.
- **G2. Anti-placeholder ⇒ AVBRYT.** Kör regex-svit (Bilaga B). Noll träffar krävs.
- **G3. Verifieringsnivå ⇒ AVBRYT.** Simulerad körlogg räcker aldrig ensam; statiska kontroller måste vara PASS.
- **G4. Legacy-sanering ⇒ AVBRYT.** Konflikt/överflödig artefakt måste patchas/arkiveras innan vidare uppdrag.
- **G5. Strukturella invariants (tvingande):**
    Före leverans måste följande PASS:a mot referensversionen, annars AVBRYT:
    - AST-parse (språkets parser)
    - Funktions-/klassinventarium (namn + antal)
    - Publikt CLI-/API-kontrakt (signaturer, argv, flaggor)
    - Kritiska imports (lista och existens)
    - Sentinel-ersättningar (inga platshållare kvar)
    
  **Trunkeringsdetektor:** jämför SHA-256 av tre normerade segment (HEAD/MID/TAIL) före/efter.
    - Om TAIL_AFTER ≠ förväntat vid små diffar eller om TAIL saknas ⇒ AVBRYT (TRUNCATION SUSPECTED).
  **Start/Slut-bevarare:**
    - BEGIN/END FILE-sentineller måste finnas i AFTER och återfinnas i diffens ‘context’.
 
## **Policy:** Förbjud “uppskattad” diff
  - AI får inte rapportera diff utan CI-beräknade värden.
  - Om referensfil saknas eller hash inte matchar ⇒ AVBRYT enligt G-1 och begär base_checksum_sha256.

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


- **1g. Obligatorisk Kod-Dokumentation (P-OKD-1.0):**
 - **Syfte:** Att säkerställa att all ny eller väsentligt modifierad kod är självförklarande, underhållbar och lätt att förstå för både människor och framtida AI-instanser.
- **Tillämpningsområde:** Protokollet gäller för alla .js, .py och .vue-filer som jag skapar eller ändrar.
- **Standarder:**

  JavaScript/Vue (<script>): Alla funktioner, Vue-komponenter (props/emits) och komplexa logikblock ska föregås av en JSDoc-kommentar (/** ... */). Den ska förklara funktionens syfte, dess parametrar (@param) och dess returvärde (@returns). Komplexa enskilda rader förklaras med //.
  
  Python: Alla moduler, klasser och funktioner ska ha en PEP 257-kompatibel docstring ("""..."""). Den ska förklara syfte, argument (:param:) och returvärde (:return:). Komplexa enskilda rader förklaras med #.
- **Definition of Done:** Kod anses inte vara "klar" förrän den uppfyller kraven i P-OKD-1.0. Detta ska vara en del av min interna checklista före varje leverans.


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
 
#### VERIFICATION_LOG (obligatorisk)
- Fil: <relativ väg>
- Statisk syntaktisk verifiering: ast/parse=[PASS|FAIL], linter=[PASS|WARN|FAIL]
- Strukturell diff:
  - **Functions/classes:** <före>=N / <efter>=N  [PASS|FAIL + difflista vid skillnad]
  - **CLI/API-signaturer:** [PASS|FAIL + diff]
  - **Imports (kritiska):** [PASS|FAIL + diff]
- **Sentinels/Placeholders:** [PASS|FAIL]
- **Kvantitativ diff:** Normalisering före diff: UTF-8, LF, trim trailing spaces.
   - **Metrikpaket (alla krävs):**
     - LINES_BEFORE/AFTER = exakta radantal.
     - NUMSTAT: added_lines, deleted_lines.
     - BYTES_BEFORE/AFTER.
     - NONEMPTY_BEFORE/AFTER (rader utan endast whitespace/kommentar).
     - **Konsistenskontroll:**
        - LINES_AFTER = LINES_BEFORE + added_lines − deleted_lines (måste hålla).
        - Δbytes = BYTES_AFTER − BYTES_BEFORE (rapporterat).
        - **Tröskel:** |added_lines − deleted_lines| / LINES_BEFORE ≤ 10 % utan REFRAKTOR-FLAG.
  - **Abortregel (tvingande):** Om någon konsistenskontroll faller eller ett tecken på trunkering upptäcks (se D) ⇒ AVBRYT och markera “QD-INCONSISTENT”.
- **Hash-kedja: base_sha256=<...> → final_sha256=<...> [PASS|FAIL]**
- **VERIFICATION_LOG och Compliance ska innehålla tabell:**
  >  | Metric    | Before | After | Added | Deleted | Check              |
  >  | --------- | -----: | ----: | ----: | ------: | ------------------ |
  >  | Lines     |     Lb |    La |    +A |      −D | `La == Lb + A − D` |
  >  | Non-empty |     Nb |    Na |     — |       — | Info               |
  >  | Bytes     |     Bb |    Ba |     — |       — | Δ = Ba−Bb          |
  >  | Result    |        |       |       |         | **PASS/FAIL**      |
  - Fail ⇒ AVBRYT.
 - **Compliance-text – exempelrad:**
   - **Kvantitativ diff:** [PASS] Lb=1234, La=1184, +15/−65 (Δ=−50); Bytes Δ=−3 812; Non-empty: 1021→987; Konsistens=PASS.

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
  - **AST/Syntax**: [PASS/NOPASS]
  - **Strukturell Invarians:**
    - **Funktions-/klassinventarium:** [PASS/NOPASS]
    - **CLI-/API-signaturer:** [PASS/NOPASS]
    - **Imports (kritiska):** [PASS/NOPASS]
  - **Placeholders/Sentinels:** [PASS/NOPASS]
  - **Kvantitativ Diff:** [PASS/NOPASS] (motivering krävs > ±10%)
  - **Base SHA256:** <...>
  - **Final SHA256:** <...>
  - **Hash-kedja verifierad (Steg 10e):** [PASS/NOPASS]
  - **VERIFICATION_LOG och Compliance ska innehålla tabell:**
    >  | Metric    | Before | After | Added | Deleted | Check              |
    >  | --------- | -----: | ----: | ----: | ------: | ------------------ |
    >  | Lines     |     Lb |    La |    +A |      −D | `La == Lb + A − D` |
    >  | Non-empty |     Nb |    Na |     — |       — | Info               |
    >  | Bytes     |     Bb |    Ba |     — |       — | Δ = Ba−Bb          |
    >  | Result    |        |       |       |         | **PASS/FAIL**      |
    - Fail ⇒ AVBRYT.
  - **Compliance-text – exempelrad:**
    - **Kvantitativ diff:** [PASS] Lb=1234, La=1184, +15/−65 (Δ=−50); Bytes Δ=−3 812; Non-empty: 1021→987; Konsistens=PASS.
   
## Steg 10: Självgranskning & extern dom
- **10a. Självgranskning:** Intern bekräftelse eller vederläggande att alla steg i "Grundbulten" protokoll nuvarande har följts eller inte kunnat följas.
- **10b. Pre-Flight Diff (tvingande):**
  1) **Metadata:** HISTORIK uppdaterad + SHA256_LF inbäddad.
  2) **Integritet:** Ingen borttagen korrekt kod utan REFRAKTOR-FLAG.
  3) **Fullständighet:** BEGIN/END FILE stämmer med exakt filsökväg.
  4) **Strukturell diff (måste PASS):**
     - AST-parse
     - Funktions-/klassinventarium identiskt (eller förändrat med REFRAKTOR-FLAG + motivering)
     - CLI-/API-kontrakt identiskt (eller explicit ändringsspec)
     - Kritiska imports kvar
     - Inga kvarvarande platshållare
  5) **Tröskel:** Rad-/byte-diff > ±10% kräver REFRAKTOR-FLAG + skriftlig motivering + godkännande.

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
- Not (bindning till AI_Core_Instruction FL-D): Vid två misslyckade leveranser för samma fil/fel ⇒ AVBRYT enligt denna Grundbult och eskalera till Help_me_God_Protokoll.md. Inkrementella fixar förbjudna tills extern analys slutförd.


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
- **Python:** ast.parse ⇒ PASS; inventarium via AST (funktioner/klasser); CLI-spec kontrolleras (t.ex. argparse/argv-räkning); imports jämförs mot referenslista.
- **JS/Vue:** vue-tsc --noEmit/ESLint; export-inventarium (funktioner/komponenter); publika props/emits/kommandon; imports.
- **Allmänt:** “REFRAKTOR-FLAG” krävs när inventarium/CLI ändras; annars AVBRYT.

## Bilaga B: Anti-placeholder-regex (utökad)
```
(\.\.\.)|(TODO|FIXME|HACK|WIP)|(resten.oförändrad)|(placeholder|stub|pseudokod|pseudo)|(omitted|truncated)|(implementera senare)|(logik här)|(här ska koden in)|(oförändrad kod)|(samma som (?:ovan|tidigare))|(#\s\.\.\.)|(\/\/\s*\.\.\.)
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
      - name: Structural inventory (Python)
        run: |
           python - <<'PY'
           import sys,hashlib
           from pathlib import Path
           import difflib
           def norm_text(p):
               s = Path(p).read_text(encoding='utf-8', errors='strict')
               s = s.replace('\r\n','\n').replace('\r','\n')
               s = '\n'.join(line.rstrip() for line in s.split('\n'))
               return s
           before_path = ".tmp/base/files/scripts/engrove_audio_tools_creator.py"  # referens
           after_path  = "scripts/engrove_audio_tools_creator.py"                  # kandidat
           sb = norm_text(before_path)
           sa = norm_text(after_path)
           Lb, La = sb.count('\n')+1 if sb else 0, sa.count('\n')+1 if sa else 0
           Nb = sum(1 for r in sb.split('\n') if r.strip() and not r.lstrip().startswith(('#','//','/*','*')))
           Na = sum(1 for r in sa.split('\n') if r.strip() and not r.lstrip().startswith(('#','//','/*','*')))
           Bb, Ba = len(sb.encode('utf-8')), len(sa.encode('utf-8'))
           added = deleted = 0
           for tag,i1,i2,j1,j2 in difflib.SequenceMatcher(a=sb.split('\n'), b=sa.split('\n')).get_opcodes():
               if tag in ('replace','delete'):
                   deleted += (i2 - i1)
               if tag in ('replace','insert'):
                   added += (j2 - j1)
           ok_lines = (La == Lb + added - deleted)
           report = {
             "LINES_BEFORE":Lb,"LINES_AFTER":La,"ADDED":added,"DELETED":deleted,
             "NONEMPTY_BEFORE":Nb,"NONEMPTY_AFTER":Na,
             "BYTES_BEFORE":Bb,"BYTES_AFTER":Ba,
             "CONSISTENT": ok_lines
           }
           print(report)
           if not ok_lines: sys.exit(2)
           # 3x sentinel anti-truncation (E)
           import math
           def chunk_hash(s, where):
               n=len(s); 
               if n==0: return hashlib.sha256(b'').hexdigest()
               span = max(1024, math.ceil(n*0.02))
               if where=="head": segment=s[:span]
               elif where=="mid": 
                   start=max(0,(n//2)-(span//2)); segment=s[start:start+span]
               else: segment=s[-span:]
               return hashlib.sha256(segment.encode('utf-8')).hexdigest()
           sentinels = {
             "HEAD_BEFORE":chunk_hash(sb,"head"), "HEAD_AFTER":chunk_hash(sa,"head"),
             "MID_BEFORE":chunk_hash(sb,"mid"),   "MID_AFTER":chunk_hash(sa,"mid"),
             "TAIL_BEFORE":chunk_hash(sb,"tail"), "TAIL_AFTER":chunk_hash(sa,"tail"),
           }
           print(sentinels)
           PY
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
