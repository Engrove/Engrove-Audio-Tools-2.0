# scripts/update_core_info.py
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

def main(sessions_dir_path, output_file_path, commit_sha):
    """
    Uppdaterar en central JSON-databas med metadata från den senast tillagda sessionsfilen.
    """
    sessions_dir = Path(sessions_dir_path)
    output_file = Path(output_file_path)

    # Läs in den befintliga kunskapsbasen, eller skapa en ny om den inte finns
    if output_file.exists():
        try:
            core_info = json.loads(output_file.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            core_info = {} # Starta om ifall filen är korrupt
    else:
        core_info = {}

    # Hitta den senast modifierade sessionsfilen (S-*.json)
    try:
        latest_session_file = max(
            sessions_dir.glob('S-*.json'), 
            key=lambda p: p.stat().st_mtime, 
            default=None
        )
    except FileNotFoundError:
        latest_session_file = None

    if not latest_session_file:
        print("Inga sessionsfiler (S-*.json) hittades, avslutar utan ändringar.")
        sys.exit(0)

    print(f"Bearbetar senaste session: {latest_session_file.name}")
    session_data = json.loads(latest_session_file.read_text(encoding='utf-8'))
    
    # Extrahera metadata-uppdateringar från den senaste sessionen
    updates = session_data.get('file_metadata_updates', [])
    
    if not updates:
        print(f"Inga metadata-uppdateringar i {latest_session_file.name}, avslutar.")
        sys.exit(0)
        
    change_made = False
    for update in updates:
        file_path = update.get('file_path')
        if file_path:
            core_info[file_path] = {
                "purpose_and_responsibility": update.get("purpose_and_responsibility"),
                "usage_context": update.get("usage_context"),
                "last_updated_by_session": session_data.get("sessionId"),
                "last_updated_at": datetime.now(timezone.utc).isoformat(),
                "last_commit_sha": commit_sha
            }
            change_made = True
            print(f"Uppdaterade metadata för: {file_path}")

    if change_made:
        output_file.write_text(json.dumps(core_info, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f"'{output_file}' har uppdaterats.")
    else:
        print("Inga ändringar att skriva till core_file_info.json.")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python update_core_info.py <sessions_dir> <output_file> <commit_sha>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
