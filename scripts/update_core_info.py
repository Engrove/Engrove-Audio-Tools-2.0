# BEGIN FILE: scripts/update_core_info.py
# scripts/update_core_info.py
#
# === SYFTE & ANSVAR ===
# Detta skript är den centrala mekanismen för att underhålla den levande dokumentationen.
# Det läser den senaste sessionsartefakten och uppdaterar den primära metadatabasen
# (`docs/core_file_info.json`) med ny information om filers syfte och användning.
# Det hanterar även den nya revisionshistoriken.
#
# === HISTORIK ===
# * v1.0 (Initial): Läste senaste sessionen och uppdaterade metadata.
# * v2.0 (2025-08-17): (Engrove Mandate) Utökad med logik för att läsa en temporär
#   revisionslogg (`.tmp/session_revision_log.json`), sammanfoga historiken med
#   den permanenta `core_file_info.json`, och genomföra en atomär skrivoperation
#   för att garantera feltålighet.
# * SHA256_LF: fc5e9d91f868c6d3d63c5aa6a2cc563c639fd5e8843da525287f3b49e5d48259
#
# === TILLÄMPADE REGLER (Frankensteen v5.6) ===
# * Grundbulten v3.8: Denna fil har modifierats enligt det uppdaterade protokollet.
# * GR5 (Tribunal/Red Team): Processen är designad för att vara atomär och feltålig
#   baserat på StigBritts analys.

import json
import sys
import os
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

def main():
    if len(sys.argv) != 4:
        print("Usage: python update_core_info.py <sessions_dir> <core_info_path> <git_commit_sha>")
        sys.exit(1)

    sessions_dir = Path(sys.argv[1])
    core_info_path = Path(sys.argv[2])
    commit_sha = sys.argv[3]
    temp_revision_log_path = Path(".tmp/session_revision_log.json")

    # Läs in den befintliga kunskapsbasen, eller skapa en ny om den inte finns
    if core_info_path.exists():
        with open(core_info_path, 'r', encoding='utf-8') as f:
            core_info = json.load(f)
    else:
        core_info = {}

    # --- Steg 1: Bearbeta metadata-uppdateringar från senaste session ---
    try:
        latest_session_file = max(
            (f for f in sessions_dir.glob("S-*.json") if f.is_file()),
            key=lambda f: f.stat().st_mtime
        )
    except ValueError:
        print("No session files found. Nothing to update.")
        latest_session_file = None

    if latest_session_file:
        with open(latest_session_file, 'r', encoding='utf-8') as f:
            session_data = json.load(f)
        session_id = session_data.get("sessionId", "unknown")
        updates = session_data.get("file_metadata_updates", [])
        
        if updates:
            now_utc = datetime.now(timezone.utc).isoformat()
            for update in updates:
                file_path = update.get("file_path")
                if file_path:
                    if file_path not in core_info:
                        core_info[file_path] = {} # Säkerställ att filposten finns
                    core_info[file_path].update({
                        "purpose_and_responsibility": update.get("purpose_and_responsibility", ""),
                        "usage_context": update.get("usage_context", ""),
                        "last_updated_by_session": session_id,
                        "last_updated_at": now_utc,
                        "last_commit_sha": commit_sha
                    })
            print(f"Processed {len(updates)} metadata updates from session {session_id}.")
        else:
            print(f"No metadata updates found in session {session_id}.")

    # --- Steg 2: Bearbeta och sammanfoga revisionshistorik ---
    if temp_revision_log_path.exists():
        print(f"Found temporary revision log at {temp_revision_log_path}.")
        with open(temp_revision_log_path, 'r', encoding='utf-8') as f:
            try:
                revisions = json.load(f)
                if not isinstance(revisions, list):
                    revisions = []
            except json.JSONDecodeError:
                revisions = []
        
        revisions_by_file = defaultdict(list)
        for rev in revisions:
            if "file_path" in rev:
                revisions_by_file[rev["file_path"]].append(rev)

        for file_path, new_revs in revisions_by_file.items():
            if file_path not in core_info:
                core_info[file_path] = {} # Säkerställ att filposten finns
            
            if "revision_history" not in core_info[file_path]:
                core_info[file_path]["revision_history"] = []
            
            core_info[file_path]["revision_history"].extend(new_revs)
            print(f"Appended {len(new_revs)} revision(s) for {file_path}.")
    else:
        print("No temporary revision log found. Skipping revision history update.")

    # --- Steg 3: Atomär skrivning och städning ---
    temp_output_path = core_info_path.with_suffix(f"{core_info_path.suffix}.tmp")
    try:
        with open(temp_output_path, 'w', encoding='utf-8') as f:
            json.dump(core_info, f, indent=2, ensure_ascii=False)
        
        os.replace(temp_output_path, core_info_path)
        print(f"Successfully updated and wrote to {core_info_path}.")

        # Radera temporär loggfil ENDAST om skrivningen lyckades
        if temp_revision_log_path.exists():
            os.remove(temp_revision_log_path)
            print(f"Successfully removed temporary revision log.")

    except Exception as e:
        print(f"CRITICAL ERROR: Failed to write updates to {core_info_path}. Error: {e}", file=sys.stderr)
        # Ta bort den temporära output-filen vid fel för att undvika skräp
        if temp_output_path.exists():
            os.remove(temp_output_path)
        sys.exit(1)


if __name__ == "__main__":
    main()
# END FILE: scripts/update_core_info.py
