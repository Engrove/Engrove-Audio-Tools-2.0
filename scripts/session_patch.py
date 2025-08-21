#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# scripts/session_patch.py
# ETT ENGÅNGS-SKRIPT för att retroaktivt lägga till session_summary_artifact.

import json
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
SESSIONS_DIR = ROOT_DIR / 'sessions'
INPUT_SUMMARIES_FILE = ROOT_DIR / 'logs/session_patch.json'

def main():
    if not INPUT_SUMMARIES_FILE.exists():
        print(f"ERROR: Input file not found: {INPUT_SUMMARIES_FILE}")
        return

    summaries_data = json.loads(INPUT_SUMMARIES_FILE.read_text(encoding='utf-8'))
    summaries_map = {item['session_id']: item for item in summaries_data}

    patched_count = 0
    for session_id, summary_artifact in summaries_map.items():
        session_file = SESSIONS_DIR / session_id
        if not session_file.exists():
            print(f"  - WARNING: Session file not found, skipping: {session_id}")
            continue

        try:
            original_data = json.loads(session_file.read_text(encoding='utf-8'))
            
            # Skapa den nya DJTA-strukturen
            new_data = {
                "schema_version": "DJTA v1.1",
                "session_id": original_data.get("sessionId", session_id.replace('.json', '')),
                "created_at": original_data.get("createdAt", summary_artifact.get("timestamp_utc")),
                "session_summary_artifact": summary_artifact,
                "builder_input": original_data # Kapsla hela det gamla objektet
            }

            # Skriv över den gamla filen
            session_file.write_text(json.dumps(new_data, indent=2, ensure_ascii=False), encoding='utf-8')
            print(f"  + Patched: {session_id}")
            patched_count += 1

        except Exception as e:
            print(f"  - ERROR: Failed to patch {session_id}. Reason: {e}")

    print(f"\nMigration complete. Patched {patched_count} files.")

if __name__ == '__main__':
    main()
