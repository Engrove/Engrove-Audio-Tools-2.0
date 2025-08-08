#!/usr/bin/env python3
# scripts/process_ai_metrics.py
#
# === SYFTE & ANSVAR ===
# Läser AI-prestandadata och lärdomsdatabas och sammanför dem till ett JSON-objekt.
# Källor: docs/ByggLogg.json och tools/frankensteen_learning_db.json.
# Skriver resultatet till stdout (inte fil).
#
# === API-KONTRAKT ===
# IN: (filer på disk)
#  - docs/ByggLogg.json (valfri; om saknas => tom lista)
#  - tools/frankensteen_learning_db.json (valfri; om saknas => tom lista eller tom dict)
# UT (stdout, application/json):
#  {
#    "performanceLog": <list|dict|[]>,
#    "learningDatabase": <list|dict|[]>
#  }
#
# === HISTORIK ===
# * v1.0 (2025-08-08): Initial skapelse enligt Operation: Metakognition (Fas 5).
#
# === TILLÄMPADE REGLER (Frankensteen v4.x) ===
# - Fullständig kod, alltid (inga platshållare)
# - Ingen gissning: defensiv inläsning med tydliga standardvärden
# - Single Responsibility: endast inläsning och sammanslagning, ingen presentation

import json
import sys
from pathlib import Path
from typing import Any, Union


BYGG_LOGG_PATH = Path("docs/ByggLogg.json")
LEARNING_DB_PATH = Path("tools/frankensteen_learning_db.json")


def load_json_file(path: Path) -> Union[dict, list]:
    """
    Robust inläsning av JSON.
    Vid avvikelse returneras tom lista ([]) för att undvika antaganden.
    Alla fel loggas till stderr.
    """
    try:
        if not path.exists():
            sys.stderr.write(f"[VARNING] Filen saknas: {path}\n")
            return []
        content = path.read_text(encoding="utf-8").strip()
        if not content:
            sys.stderr.write(f"[VARNING] Filen är tom: {path}\n")
            return []
        data = json.loads(content)
        if not isinstance(data, (dict, list)):
            sys.stderr.write(f"[VARNING] Oväntad JSON-rot i {path} (typ {type(data).__name__}); använder tom lista.\n")
            return []
        return data
    except json.JSONDecodeError as e:
        sys.stderr.write(f"[FEL] Ogiltig JSON i {path}: {e}\n")
        return []
    except Exception as e:
        sys.stderr.write(f"[FEL] Kunde inte läsa {path}: {e}\n")
        return []


def main() -> None:
    performance_log: Any = load_json_file(BYGG_LOGG_PATH)
    learning_database: Any = load_json_file(LEARNING_DB_PATH)

    output = {
        "performanceLog": performance_log,
        "learningDatabase": learning_database,
    }

    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
