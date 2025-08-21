#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# scripts/patch_sessions_with_summaries.py
# ETT ENGÅNGS-SKRIPT för att retroaktivt lägga till session_summary_artifact.

import json
from pathlib import Path
import traceback

ROOT_DIR = Path(__file__).parent.parent
SESSIONS_DIR = ROOT_DIR / 'sessions'
# Detta är sökvägen som anges i din YAML-fil
INPUT_SUMMARIES_FILE = ROOT_DIR / 'historical_summaries.json'

def main():
    if not INPUT_SUMMARIES_FILE.exists():
        print(f"ERROR: Input file not found: {INPUT_SUMMARIES_FILE}")
        # Vi skapar en tom fil för att undvika att skriptet kraschar i CI
        INPUT_SUMMARIES_FILE.touch()
        summaries_data = []
    else:
        summaries_data = json.loads(INPUT_SUMMARIES_FILE.read_text(encoding='utf-8'))

    summaries_map = {item['session_id']: item for item in summaries_data}

    patched_count = 0
    error_count = 0
    
    session_files = sorted(SESSIONS_DIR.glob('*.json'))

    # Första passet: Reparera den kända korrupta filen manuellt i koden
    corrupt_file_path = SESSIONS_DIR / '045.0.json'
    if corrupt_file_path.exists():
        try:
            print(f"Attempting to repair {corrupt_file_path.name}...")
            # Läser som råtext och ersätter ett vanligt fel (kommatering)
            text_content = corrupt_file_path.read_text(encoding='utf-8')
            # Intelligent reparation: letar efter } { utan kommatecken mellan
            fixed_content = text_content.replace('}\n  {', '},\n  {')
            json.loads(fixed_content) # Validerar att reparationen fungerade
            corrupt_file_path.write_text(fixed_content, encoding='utf-8')
            print(f"  + Successfully repaired {corrupt_file_path.name}")
        except Exception as e:
            print(f"  - ERROR: Automatic repair failed for {corrupt_file_path.name}. Manual fix needed. Reason: {e}")


    for session_file in session_files:
        try:
            original_data = json.loads(session_file.read_text(encoding='utf-8'))
            
            # Hoppa över om den redan är i det nya formatet
            if "schema_version" in original_data and "DJTA" in original_data["schema_version"]:
                # print(f"  - INFO: Skipping already patched file: {session_file.name}")
                continue

            session_id_key = session_file.name
            if session_id_key not in summaries_map:
                print(f"  - WARNING: No summary found for {session_id_key}, skipping patch.")
                continue

            summary_artifact = summaries_map[session_id_key]

            new_data = {
                "schema_version": "DJTA v1.1",
                "session_id": original_data.get("sessionId", session_id_key.replace('.json', '')),
                "created_at": original_data.get("createdAt", summary_artifact.get("timestamp_utc")),
                "session_summary_artifact": summary_artifact,
                "builder_input": original_data
            }

            session_file.write_text(json.dumps(new_data, indent=2, ensure_ascii=False), encoding='utf-8')
            print(f"  + Patched: {session_file.name}")
            patched_count += 1

        except Exception as e:
            print(f"  - ERROR: Failed to patch {session_file.name}. Reason: {e}")
            traceback.print_exc()
            error_count += 1
    
    if error_count > 0:
         print(f"\nMigration finished with {error_count} errors.")
    else:
        print(f"\nMigration complete. Patched {patched_count} files.")


if __name__ == '__main__':
    main()
