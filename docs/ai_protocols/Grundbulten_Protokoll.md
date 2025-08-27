<!-- BEGIN FILE: docs/ai_protocols/Grundbulten_Protokoll.md
SYFTE & ANSVAR:
"Grundbulten" (P-GB-3.9) är den tvingande lagen för all filgenerering/-modifiering (kod, dokument, konfig, data).
Mål: 100% korrekt, komplett, spårbar, verifierad och deterministisk leverans i chattläge (Gemini/OpenAI), utan antaganden.

HISTORIK:
* v1.0 (2025-08-16): Kodfokus.
* v2.0 (2025-08-16): Universell omarbetning.
* v2.1 (2025-08-16): Syntes + tribunal + korrekt MD-kommentering.
* v2.4 (2025-08-16): Anti-Placeholder-Grind, utfällda steg 2–8.
* v3.0 (2025-08-16): REBORN: Hårda grindar G0, G1, G2, G3, G4, evidensartefakter, typstyrd verifieringsmatris, CI-recept.
* v3.1 (2025-08-17): (Help me God) Gjorde verifiering extern och obligatorisk. Införde 'VERIFICATION_LOG' och 'LIGHTWEIGHT COMPLIANCE STATEMENT'.
* v3.2 (2025-08-17): Skärpt kontextkrav (G0 -> 99%), förenklad rapportering, och lagt till obligatorisk kvantitativ diff-analys.
* v3.3 (2025-08-17): (Help me God) Infört Steg 10b, "Pre-Flight Diff Check".
* v3.4 (2025-08-17): (Help me God) Lade till Steg 1d (kontextkommentar) och Steg 2b (Dominansprincip).
* v3.6 (2025-08-17): (Help me God) KRITISK UPPDATERING. Infört en sluten verifieringskedja för att förhindra trunkeringsfel: 1. G-1: Tvingande hash-kontroll vid inläsning. 2. Steg 1f: Tvingande inbäddning av slutgiltig hash i filens historik. 3. Steg 9: Tvingande rapportering av slutgiltig hash i svar. 4. Steg 10e: Tvingande intern självverifiering av hash-värden före leverans.
* v3.7 (2025-08-17): (Help me God - KORRIGERING) Infört en sluten, hash-baserad verifieringskedja (G-1, 1f, 9, 10e) för att matematiskt förhindra trunkeringsfel. Återställt fullständiga bilagor.
* v3.8 (2025-08-17): (Engrove Mandate) Lade till Steg 11b för att tvinga fram loggning av varje filmodifiering till en temporär sessionslogg (.tmp/session_revision_log.json).
* v3.9 (2025-08-18): (Engrove Mandate) Lade till Bilaga E för att definiera en deterministisk beslutsmatris för leveransformat i chatt (Full fil vs. Manuell Patch vs. JSON-patch).
* SHA256_LF: c4f8e07c968f371701cfc4978acc0f661021ac0446180b8c0f07984b5e3f08ac
END HEADER -->
```json
{
  "protocolId": "P-GB-3.9",
  "file_path": "docs/ai_protocols/Grundbulten_Protokoll.md",
  "title": "Grundbulten – Universell filhantering (chattsession)",
  "version": "3.9",
  "strict_mode": true,
  "mode": "literal",
  "purpose": "\"Grundbulten\" är den tvingande lagen för all filgenerering/-modifiering (kod, dokument, konfig, data).",
  "goals": "100% korrekt, komplett, spårbar, verifierad och deterministisk leverans i chattläge (Gemini/OpenAI), utan antaganden.",
  "metadata": {
    "date": "2025-08-19",
    "external_reviewer": "Engrove (godkänd för införing i Steg 10)"
  },
  "terminology_and_policy": {
    "refaktor_flag": "Obligatorisk när struktur (inventarium/CLI) medvetet ändras. Utan flagga ⇒ ändringen blockeras av G5/10b.",
    "quantitative_diff_threshold_default": "±10 % (projekt kan skärpa i lokal policy)."
  },
  "gates": [
    {
      "id": "G-1",
      "title": "Kontrollsumma-verifiering vid inläsning",
      "abort_on_violation": true,
      "rule": "Om en fil som ska modifieras har en base_checksum_sha256 i kontexten måste intern minnesbild och beräknad hash matcha bas-hashen. Vid mismatch: avbryt och begär färsk fil."
    },
    {
      "id": "G0",
      "title": "Kontextintegritet",
      "threshold": "99%",
      "abort_on_violation": true,
      "rule": "Kräv kompletterande källor/sammanfattning och ny körning om under tröskel."
    },
    {
      "id": "G1",
      "title": "Kontext-abort (tvingande)",
      "abort_on_violation": true,
      "condition": "is_content_full == false för målfil",
      "action": "AVBRYT omedelbart och begär komplett fil + base_checksum_sha256. Inga patch/regeneration innan kontext=100%."
    },
    {
      "id": "G2",
      "title": "Anti-placeholder",
      "abort_on_violation": true,
      "rule": "Kör regex-svit (Bilaga B). Noll träffar krävs."
    },
    {
      "id": "G3",
      "title": "Verifieringsnivå",
      "abort_on_violation": true,
      "rule": "Simulerad körlogg räcker aldrig ensam; statiska kontroller måste vara PASS."
    },
    {
      "id": "G4",
      "title": "Legacy-sanering",
      "abort_on_violation": true,
      "rule": "Konflikt/överflödig artefakt måste patchas/arkiveras innan vidare uppdrag."
    },
    {
      "id": "G5",
      "title": "Strukturella invariants (tvingande)",
      "abort_on_violation": true,
      "checks": [
        "AST-parse (språkets parser)",
        "Funktions-/klassinventarium (namn + antal)",
        "Publikt CLI-/API-kontrakt (signaturer, argv, flaggor)",
        "Kritiska imports (lista och existens)",
        "Sentinel-ersättningar (inga platshållare kvar)"
      ],
      "policy_forbid_estimated_diff": {
        "rule": "AI får inte rapportera diff utan CI-beräknade värden.",
        "on_missing_reference_or_hash_mismatch": "AVBRYT enligt G-1 och begär base_checksum_sha256."
      },
      "truncation_detector": {
        "method": "Jämför SHA-256 av tre normerade segment (HEAD/MID/TAIL) före/efter.",
        "abort_conditions": [
          "TAIL_AFTER ≠ förväntat vid små diffar",
          "TAIL saknas"
        ]
      },
      "start_end_preserver": {
        "rule": "BEGIN/END FILE-sentineller måste finnas i AFTER och återfinnas i diffens context."
      }
    }
  ],
  "policies": [
    {
      "id": "FORBID_ESTIMATED_DIFF",
      "title": "Förbjud uppskattad diff",
      "rules": [
        "AI får inte rapportera diff utan CI-beräknade värden.",
        "Om referensfil saknas eller hash inte matchar ⇒ AVBRYT enligt G-1 och begär base_checksum_sha256."
      ]
    }
  ],
  "steps": [
    {
      "id": 0,
      "title": "Mål och omfattning",
      "rules": ["Gäller alla filtyper.", "Leverans ska vara självförsörjande (inga dolda referenser)."]
    },
    {
      "id": 1,
      "title": "Dokumentation & metadata",
      "substeps": [
        {"id": "1a", "rule": "Fil-header: SYFTE, HISTORIK (full, inga platshållare), TILLÄMPADE REGLER."},
        {"id": "1b", "rule": "Kommentarspolicy + sentineller: Inkludera BEGIN/END FILE med exakt sökväg."},
        {
          "id": "1c",
          "comment_syntax_table": [
            {"ext": ".md", "syntax": "<!-- ... -->", "status": "Obligatorisk"},
            {"ext": ".py", "syntax": "# ...", "status": "Obligatorisk"},
            {"ext": ".js/.vue/.css", "syntax": "// ... eller /* ... */", "status": "Obligatorisk"},
            {"ext": ".json", "syntax": "Inga kommentarer tillåtna", "status": "Förbjudet"},
            {"ext": ".toml", "syntax": "# ...", "status": "Obligatorisk"},
            {"ext": ".yml/.yaml", "syntax": "# ...", "status": "Obligatorisk"}
          ]
        },
        {
          "id": "1d",
          "rule": "Kontextkommentar (Obligatorisk) – direkt efter filsökväg i headern (1–3 rader). JSON-filer undantas.",
          "example": [
            "# scripts/modules/ui_logic.py",
            "# Denna modul hanterar all generell UI-interaktivitet för det genererade verktyget,",
            "# såsom hantering av modals, resizer och meny-logik."
          ]
        },
        {"id": "1e", "rule": "Kommentarskorrigering: Felaktig kommentar-syntax ska ovillkorligen rättas enligt 1c."},
        {"id": "1f", "rule": "Hash-evidens i fil-header (Obligatorisk): Lägg till rad i HISTORIK med slutgiltig verifierad hash.", "format": "* SHA256_LF: <hash>"},
        {
          "id": "1g",
          "rule": "Obligatorisk Kod-Dokumentation (P-OKD-1.0)",
          "scope": "Alla .js, .py, .vue som skapas/ändras.",
          "standards": {
            "javascript_vue": "JSDoc före alla funktioner/komponenter/komplex logik; förklara syfte, @param, @returns. Komplex rad kommenteras med //.",
            "python": "PEP 257-docstring på moduler/klasser/funktioner; förklara syfte, :param:, :return:. Komplex rad kommenteras med #."
          },
          "definition_of_done": "Kod är inte klar förrän kraven i P-OKD-1.0 uppfylls."
        }
      ]
    },
    {
      "id": 2,
      "title": "SPEC/ANTAGANDEN",
      "substeps": [
        {"id": "2a", "rule": "Beskriv kontrakt, IO, invarianter, fel, typer, tråd/async, prestanda, miljö/beroenden. Märk [Explicit] vs [Härledd]. Tester i Steg 6 binder dessa."},
        {
          "id": "2b",
          "rule": "Kod-i-kod Dominansprincip",
          "priority": [
            "Användarens Prompt – explicit inbäddad kod dominant.",
            "Värdspråket (Host) – vid generella promptar.",
            "Språket med Syntaxfel – dominant om syntaxfel finns."
          ],
          "example": "[Antagande] Dominant kontext är Python. Den inbäddade JS-strängen i `JS_LOGIC` behandlas som literal och ändras endast om det krävs för att korrigera Python-syntax."
        }
      ]
    },
    {
      "id": 3,
      "title": "Tribunalgranskning",
      "roles": [
        {"name": "KajBjörn", "duty": "SPEC bygger endast på given information (No-Guess-Pledge)."},
        {"name": "StigBritt", "duty": "Bryt ÅTGÄRDSPLAN logiskt före implementation."}
      ]
    },
    {
      "id": 4,
      "title": "Fel- och riskkategorier (checklista)",
      "categories": [
        "Syntax/parse; namn/namespace; typer; None/null; index/gränser; edge-fall.",
        "Tillstånd; race; init-ordning; resurser/läckor; I/O (encoding/tidszon).",
        "Säkerhet (injektion, path traversal, osäker deserialisering); prestanda (Big-O).",
        "Beroenden (version/låsning/cirklar); stil/linters."
      ]
    },
    {
      "id": 5,
      "title": "ÅTGÄRDSPLAN",
      "order": ["korrigera", "säkra", "stabilisera", "dokumentera", "städa"],
      "principle": "Minsta nödvändiga ändring; omdesign endast med motivering."
    },
    {
      "id": 6,
      "title": "Testdesign",
      "code": [
        "Enhets- och egenskapstester (seed=42), felvägar, gränsvärden, icke-ASCII, tidszoner."
      ],
      "non_code": [
        "Schema-/formatvalidering (Markdown-länkar, JSON Schema, YAML-schema, TOML-parse)."
      ],
      "general": [
        "Filstorlek, funktionsantal, objektantal, sektionsantal eller annan mätbar differans."
      ]
    },
    {
      "id": 7,
      "title": "Extern Verifiering & Bevisföring",
      "verification_log": {
        "required": true,
        "fields": [
          "Fil: <relativ väg>",
          "Statisk syntaktisk verifiering: ast/parse=[PASS|FAIL], linter=[PASS|WARN|FAIL]",
          "Strukturell diff: Functions/classes, CLI/API-signaturer, Imports (kritiska)",
          "Sentinels/Placeholders: [PASS|FAIL]",
          "Kvantitativ diff: normalisering före diff; metrikpaket och konsistenskontroller",
          "Abortregel: vid konsistensfel eller trunkeringsmisstanke ⇒ AVBRYT (QD-INCONSISTENT)",
          "Hash-kedja: base_sha256 → final_sha256 [PASS|FAIL]"
        ],
        "metrics_table_markdown_template": [
          "| Metric    | Before | After | Added | Deleted | Check              |",
          "| --------- | -----: | ----: | ----: | ------: | ------------------ |",
          "| Lines     |     Lb |    La |    +A |      −D | La == Lb + A − D   |",
          "| Non-empty |     Nb |    Na |     — |       — | Info               |",
          "| Bytes     |     Bb |    Ba |     — |       — | Δ = Ba−Bb          |",
          "| Result    |        |       |       |         | PASS/FAIL          |"
        ]
      }
    },
    {
      "id": 8,
      "title": "Filleverans",
      "rules": [
        "Leveransformatet styrs av Bilaga E.",
        "Execution Summary: Svaret måste inkludera en ärlig enmeningssammanfattning av processen.",
        "Anti-Placeholder-Grind: Förbjudna mönster (se bilaga). Vid träff: AVBRYT och börja om vid Steg 2."
      ]
    },
    {
      "id": 9,
      "title": "Efterlevnadsrapport (Compliance Statement)",
      "required": true,
      "example_markdown": "#### LIGHTWEIGHT COMPLIANCE STATEMENT\\n- **Syntax:** [PASS/NOPASS]\\n- **Kontrakt:** [PASS/NOPASS]\\n- **Placeholders:** [PASS/NOPASS]\\n- **Historik:** [PASS/NOPASS]\\n- **Kvantitativ Diff:** [PASS/NOPASS] - [Ökning/Minskning] av X rader motiverad av nya protokollsteg.\\n- **Base SHA256:** [SHA för filen INNAN ändring]\\n- **Final SHA256:** [SHA för filen EFTER ändring]\\n- **AST/Syntax**: [PASS/NOPASS]\\n- **Strukturell Invarians:**\\n  - **Funktions-/klassinventarium:** [PASS/NOPASS]\\n  - **CLI-/API-signaturer:** [PASS/NOPASS]\\n  - **Imports (kritiska):** [PASS/NOPASS]\\n- **Placeholders/Sentinels:** [PASS/NOPASS]\\n- **Kvantitativ Diff:** [PASS/NOPASS] (motivering krävs > ±10%)\\n- **Base SHA256:** <...>\\n- **Final SHA256:** <...>\\n- **Hash-kedja verifierad (Steg 10e):** [PASS/NOPASS]\\n>  | Metric    | Before | After | Added | Deleted | Check              |\\n>  | --------- | -----: | ----: | ----: | ------: | ------------------ |\\n>  | Lines     |     Lb |    La |    +A |      −D | `La == Lb + A − D` |\\n>  | Non-empty |     Nb |    Na |     — |       — | Info               |\\n>  | Bytes     |     Bb |    Ba |     — |       — | Δ = Ba−Bb          |\\n>  | Result    |        |       |       |         | **PASS/FAIL**      |",
      "abort_on_fail": true
    },
    {
      "id": 10,
      "title": "Självgranskning & extern dom",
      "substeps": [
        {"id": "10a", "rule": "Självgranskning: bekräfta/vederlägg att alla steg följts; annars motivera."},
        {
          "id": "10b",
          "title": "Pre-Flight Diff (tvingande)",
          "checks": {
            "metadata": "HISTORIK uppdaterad + SHA256_LF inbäddad.",
            "integrity": "Ingen borttagen korrekt kod utan REFRAKTOR-FLAG.",
            "fullness": "BEGIN/END FILE stämmer med exakt filsökväg.",
            "structural_diff": [
              "AST-parse",
              "Funktions-/klassinventarium identiskt (eller ändrat med REFRAKTOR-FLAG + motivering)",
              "CLI-/API-kontrakt identiskt (eller explicit ändringsspec)",
              "Kritiska imports kvar",
              "Inga kvarvarande platshållare"
            ],
            "threshold": "Rad-/byte-diff > ±10% kräver REFRAKTOR-FLAG + skriftlig motivering + godkännande."
          }
        },
        {"id": "10c", "rule": "Extern dom (Engrove): Godkännande eller korrigering."},
        {
          "id": "10e",
          "rule": "Slutgiltig Hash-verifiering (Obligatorisk): intern hash på slutgiltig kod måste vara identisk med hashar i 1f & 9. Vid mismatch: AVBRYT."
        }
      ]
    },
    {
      "id": 11,
      "title": "Arkivering",
      "substeps": [
        {"id": "11a", "rule": "Uppdatera HISTORIK. Verifiera BEGIN/END-sentineller och filsökväg."},
        {
          "id": "11b",
          "title": "Temporär Revisionslogg",
          "rule": "Append JSON-post efter varje godkänd filmodifiering.",
          "path": ".tmp/session_revision_log.json",
          "required_fields": ["file_path", "timestamp", "session_id", "commit_sha"]
        }
      ]
    },
    {
      "id": 12,
      "title": "Eskalering",
      "attempt_counter": "Intern räknare per misslyckade försök (ökar vid misslyckande).",
      "forced_escalations": [
        "När räknaren når 1 eller 2: inkrementella fixar förbjudna. Aktivera omedelbart Help_me_God_Protokoll.md.",
        "När räknaren når 3: överväg avslut (bekräftad ändpunkt) och beskriv orsak."
      ],
      "meta_protocol": "Grundbulten Token Counter (GTC)",
      "note_binding": "Vid två misslyckade leveranser för samma fil/fel ⇒ AVBRYT enligt denna Grundbult och eskalera till Help_me_God_Protokoll.md."
    }
  ],
  "appendices": {
    "A": {
      "typed_verification_matrix": [
        {"type": "Vue/JS (.vue/.js)", "rules": ["vue-tsc --noEmit ⇒ PASS", "ESLint ⇒ 0 fel", "Vite build dry-run ⇒ OK"]},
        {"type": "JSON (.json)", "rules": ["Validera mot relevant JSON Schema", "$schema krävs", "Inga kommentarer", "Stabil nyckelordning där norm finns"]},
        {"type": "YAML (.yml/.yaml)", "rules": ["yamllint ⇒ 0 fel", "Schema-validering om tillgänglig"]},
        {"type": "Markdown (.md)", "rules": ["markdownlint ⇒ 0 fel", "Extern/intern länk-check ⇒ 0 brutna"]},
        {"type": "TOML (.toml)", "rules": ["toml-parse ⇒ PASS"]},
        {"type": "GitHub Actions (CI-YAML)", "rules": ["YAML-parse ⇒ PASS", "action-linter/dry-run ⇒ PASS"]},
        {"type": "CSS", "rules": ["Lint ⇒ 0 fel", "Tokens används; inga hårdkodade färger där tokens finns"]},
        {"type": "Python", "rules": ["ast.parse ⇒ PASS", "Inventarium via AST (funktioner/klasser)", "CLI-spec kontroll (argparse/argv)", "Imports jämförs mot referenslista"]},
        {"type": "JS/Vue", "rules": ["vue-tsc --noEmit/ESLint", "Export-inventarium (funktioner/komponenter)", "Publika props/emits/kommandon", "Imports"]}
      ],
      "general": "REFRAKTOR-FLAG krävs när inventarium/CLI ändras; annars AVBRYT."
    },
    "B": {
      "anti_placeholder_regex": "(\\.\\.\\.)|(TODO|FIXME|HACK|WIP)|(resten.oförändrad)|(placeholder|stub|pseudokod|pseudo)|(omitted|truncated)|(implementera senare)|(logik här)|(här ska koden in)|(oförändrad kod)|(samma som (?:ovan|tidigare))|(#\\s\\.\\.\\.)|(\\/\\/\\s*\\.\\.\\.)"
    },
    "C": {
      "chat_mode": [
        "Ingen exekvering garanterad i chatt ⇒ statiska kontroller krävs.",
        "Ingen spekulation; fråga vid osäkerhet.",
        "Determinism: seed=42; inga nätverkskall; inga nya beroenden utan låsta versioner + motivering.",
        "Om faktisk körning krävs: leverera körbart CI-recept (GitHub Actions-jobb) och begär logg för slutligt grönt."
      ]
    },
    "D": {
      "ci_recipe_template_yaml": "name: grundbulten-verify\\non: [workflow_dispatch]\\njobs:\\n  verify:\\n    runs-on: ubuntu-latest\\n    steps:\\n      - uses: actions/checkout@v4\\n      - uses: actions/setup-node@v4\\n        with: { node-version: '20' }\\n      - uses: actions/setup-python@v5\\n        with: { python-version: '3.11' }\\n      - run: npm ci || true\\n      - run: pip install -U ruff mypy pytest || true\\n      - run: npx vue-tsc --noEmit || true\\n      - run: npx eslint . || true\\n      - run: python - <<'PY'\\nimport ast,sys,glob\\n[ast.parse(open(p).read(),p) for p in glob.glob('**/*.py', recursive=True)]\\nprint('PY_AST_OK')\\nPY\\n      - run: echo \"STATIC CHECKS COMPLETE\"\\n      - name: Structural inventory (Python)\\n        run: |\\n           python - <<'PY'\\n           import sys,hashlib\\n           from pathlib import Path\\n           import difflib\\n           def norm_text(p):\\n               s = Path(p).read_text(encoding='utf-8', errors='strict')\\n               s = s.replace('\\r\\n','\\n').replace('\\r','\\n')\\n               s = '\\n'.join(line.rstrip() for line in s.split('\\n'))\\n               return s\\n           before_path = \".tmp/base/files/scripts/engrove_audio_tools_creator.py\"\\n           after_path  = \"scripts/engrove_audio_tools_creator.py\"\\n           sb = norm_text(before_path)\\n           sa = norm_text(after_path)\\n           Lb, La = sb.count('\\n')+1 if sb else 0, sa.count('\\n')+1 if sa else 0\\n           Nb = sum(1 for r in sb.split('\\n') if r.strip() and not r.lstrip().startswith(('#','//','/*','*')))\\n           Na = sum(1 for r in sa.split('\\n') if r.strip() and not r.lstrip().startswith(('#','//','/*','*')))\\n           Bb, Ba = len(sb.encode('utf-8')), len(sa.encode('utf-8'))\\n           added = deleted = 0\\n           for tag,i1,i2,j1,j2 in difflib.SequenceMatcher(a=sb.split('\\n'), b=sa.split('\\n')).get_opcodes():\\n               if tag in ('replace','delete'):\\n                   deleted += (i2 - i1)\\n               if tag in ('replace','insert'):\\n                   added += (j2 - j1)\\n           ok_lines = (La == Lb + added - deleted)\\n           report = {\\n             \"LINES_BEFORE\":Lb,\"LINES_AFTER\":La,\"ADDED\":added,\"DELETED\":deleted,\\n             \"NONEMPTY_BEFORE\":Nb,\"NONEMPTY_AFTER\":Na,\\n             \"BYTES_BEFORE\":Bb,\"BYTES_AFTER\":Ba,\\n             \"CONSISTENT\": ok_lines\\n           }\\n           print(report)\\n           if not ok_lines: sys.exit(2)\\n           import math\\n           def chunk_hash(s, where):\\n               n=len(s); \\n               if n==0: return hashlib.sha256(b'').hexdigest()\\n               span = max(1024, math.ceil(n*0.02))\\n               if where==\"head\": segment=s[:span]\\n               elif where==\"mid\": \\n                   start=max(0,(n//2)-(span//2)); segment=s[start:start+span]\\n               else: segment=s[-span:]\\n               return hashlib.sha256(segment.encode('utf-8')).hexdigest()\\n           sentinels = {\\n             \"HEAD_BEFORE\":chunk_hash(sb,\"head\"), \"HEAD_AFTER\":chunk_hash(sa,\"head\"),\\n             \"MID_BEFORE\":chunk_hash(sb,\"mid\"),   \"MID_AFTER\":chunk_hash(sa,\"mid\"),\\n             \"TAIL_BEFORE\":chunk_hash(sb,\"tail\"), \"TAIL_AFTER\":chunk_hash(sa,\"tail\"),\\n           }\\n           print(sentinels)\\n           PY"
    },
    "E": {
      "delivery_matrix": [
        {"task_type": "Ny fil", "recommended_format": "Fullständig Fil", "rationale": "Icke förhandlingsbart. Enda sättet att garantera fullständighet."},
        {"task_type": "Liten, manuell ändring i befintlig fil", "recommended_format": "Manuell Patch-Instruktion (P-MP-1.0)", "rationale": "Otvetydighet och verifierbarhet för mänsklig operatör."},
        {"task_type": "Medelstor till stor ändring (> 5 rader)", "recommended_format": "Fullständig Fil", "rationale": "Standard. Minimerar risken för manuella fel."},
        {"task_type": "Programmatisk/Automatiserad Patchning", "recommended_format": "Strukturerad JSON-patch (Diff_Protocol_v3.md)", "rationale": "För verktygsapplicering med exakt basinformation."}
      ]
    }
  }
}
```
