#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# scripts/build_session_manifest.py

import json
from pathlib import Path

# Konfiguration
ROOT_DIR = Path(__file__).parent.parent
SESSIONS_DIR = ROOT_DIR / 'sessions'
OUTPUT_FILE = ROOT_DIR / 'docs' / 'session_manifest.json'

def main():
    print("Building session manifest...")
    manifest_entries = []

    session_files = sorted(SESSIONS_DIR.glob('*.json'))

    for session_file in session_files:
        try:
            content = session_file.read_text(encoding='utf-8')
            # Extrahera det FÖRSTA JSON-objektet, som enligt protokoll ska vara summary
            # Använder en enkel men robust metod för att hitta första '{' och sista '}' i det blocket
            first_brace = content.find('{')
            # Detta är en förenkling; en mer robust parser kan behövas om formatet varierar
            # Men förutsatt att protokollet följs bör detta fungera.
            json_data = json.loads(content) # Läser hela filen som ett JSON-objekt

            # Antag att avslutningsprotokollet skapar en nyckel "final_artifacts"
            # och summary-objektet är det första i den listan.
            # Detta är en robustare design än att bara söka efter första JSON-blocket.
            # **UPPDATERING TILL PROTOKOLLET I STEG 1:** AI:n ska kapsla sina artefakter.
            summary_artifact = json_data.get('session_summary_artifact')

            if summary_artifact and summary_artifact.get('artifact_type') == 'SessionSummaryArtifact':
                manifest_entries.append(summary_artifact)
                print(f"  + Processed: {session_file.name}")
            else:
                 print(f"  - WARNING: No valid summary artifact found in {session_file.name}")


        except (json.JSONDecodeError, KeyError, IndexError) as e:
            print(f"  - ERROR: Could not process {session_file.name}. Reason: {e}")
            continue

    # Sortera manifestet kronologiskt
    manifest_entries.sort(key=lambda x: x.get('timestamp_utc', ''))

    print(f"\nManifest built with {len(manifest_entries)} entries. Writing to {OUTPUT_FILE}...")
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(manifest_entries, indent=2, ensure_ascii=False), encoding='utf-8')
    print("Done.")

if __name__ == '__main__':
    main()
