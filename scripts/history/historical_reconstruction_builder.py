#!/usr/bin/env python3
# historical_reconstruction_builder.py (v3, 2025-08-09)
# Läs en mapp med [SESSIONID].json och konsolidera till fyra standardfiler.
#
# v3 UPPGRADERING: Lade till självsanerande logik och hantering av dynamiska protokoll.
#
# OUTPUT:
#   docs/ByggLogg.json                (array)
#   docs/Chatthistorik.json           (array)
#   docs/ai_protocol_performance.json (array)
#   tools/frankensteen_learning_db.json (array, sanerad)
#   docs/ai_protocols/DynamicProtocols.json (array, berikad)
#
# Regler:
# - Sortera kronologiskt utifrån SESSIONID i filnamnet (numerisk).
# - Normalisera talare: säkerställ maskinläsbar model + visningssträngen speaker.
# - Var defensiv: hoppa över trasiga filer men logga stderr.
# - Backcompat: accepterar både objekt (äldre) och array (nya) för frankensteen_learning_db.
#
# Användning:
#   python3 historical_reconstruction_builder.py /path/to/sessions_dir  [/output_root]

import sys
import json
import re
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

# Försök att importera jsonschema, ge ett tydligt felmeddelande om det saknas.
try:
    from jsonschema import validate
    from jsonschema.exceptions import ValidationError
except ImportError:
    print("ERROR: jsonschema is not installed. Please run: pip install jsonschema", file=sys.stderr)
    sys.exit(1)

SPEAKER_PATTERN = re.compile(r'^([^()]+) \(([^:]+):([^@]+)@([^\)]+)\)$')

def normalize_speaker(entry: Dict[str, Any]) -> Dict[str, Any]:
    name = (entry.get("speakerName") or "unknown").strip() or "unknown"
    model = entry.get("model") or {}
    provider = (model.get("provider") or "unknown").strip() or "unknown"
    mname = (model.get("name") or "unknown").strip() or "unknown"
    version = (model.get("version") or "unknown").strip() or "unknown"
    display = f"{name} ({provider}:{mname}@{version})"
    entry["speakerName"] = name
    entry["model"] = {"provider": provider, "name": mname, "version": version}
    entry["speaker"] = display
    return entry

def ensure_chat_schema(chat_obj: Dict[str, Any]) -> Dict[str, Any]:
    interactions = chat_obj.get("interactions") or []
    fixed: List[Dict[str, Any]] = []
    for it in interactions:
        if "speakerName" not in it or "model" not in it:
            speaker = it.get("speaker", "")
            m = SPEAKER_PATTERN.match(speaker) if isinstance(speaker, str) else None
            if m:
                name, provider, mname, version = m.groups()
                it.setdefault("speakerName", name.strip())
                it.setdefault("model", {"provider": provider.strip(), "name": mname.strip(), "version": version.strip()})
            else:
                it.setdefault("speakerName", (speaker or "unknown").strip())
                it.setdefault("model", {"provider": "unknown", "name": "unknown", "version": "unknown"})
        fixed.append(normalize_speaker(it))
    chat_obj["interactions"] = fixed
    return chat_obj

def load_session_file(p: Path) -> Dict[str, Any]:
    try:
        obj = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(obj, dict):
            raise ValueError("Root element is not a JSON object")
        return obj
    except Exception as e:
        sys.stderr.write(f"[SKIP] {p.name}: {e}\n")
        return {}

def main():
    if len(sys.argv) < 2:
        print("Användning: python3 historical_reconstruction_builder.py /path/to/sessions_dir [/output_root]")
        sys.exit(2)
    sessions_dir = Path(sys.argv[1])
    out_root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(".")
    docs_dir = out_root / "docs"
    ai_protocols_dir = docs_dir / "ai_protocols"
    tools_dir = out_root / "tools"
    ai_protocols_dir.mkdir(parents=True, exist_ok=True)
    tools_dir.mkdir(parents=True, exist_ok=True)

    files = [p for p in sessions_dir.glob("*.json") if p.is_file()]
    def session_key(p: Path):
        m = re.match(r'^(\d+\.?\d*)\.json$', p.name)
        return float(m.group(1)) if m else float("inf")
    files.sort(key=session_key)

    bygglogg, chathistorik, perf, heuristics = [], [], [], []

    for p in files:
        data = load_session_file(p)
        art = data.get("artifacts") or {}
        if not art: continue

        if isinstance(art.get("ByggLogg"), dict): bygglogg.append(art["ByggLogg"])
        if isinstance(art.get("Chatthistorik"), dict): chathistorik.append(ensure_chat_schema(art["Chatthistorik"]))
        if isinstance(art.get("ai_protocol_performance"), dict): perf.append(art["ai_protocol_performance"])
        
        lg = art.get("frankensteen_learning_db")
        if isinstance(lg, list): heuristics.extend([h for h in lg if isinstance(h, dict)])
        elif isinstance(lg, dict): heuristics.append(lg)
    
    # --- Sanering av Heuristiker ---
    ids_to_deprecate = set()
    for h in heuristics:
        if h.get('metadata', {}).get('deprecates'):
            ids_to_deprecate.update(h['metadata']['deprecates'])
    active_heuristics = [h for h in heuristics if h.get('heuristicId') not in ids_to_deprecate]
    
    # --- Berikning av DynamicProtocols.json ---
    dynamic_protocols_path = ai_protocols_dir / "DynamicProtocols.json"
    master_schema_path = ai_protocols_dir / "DynamicProtocol.schema.json"
    
    try:
        master_schema = json.loads(master_schema_path.read_text(encoding="utf-8")) if master_schema_path.exists() else None
        existing_protocols = json.loads(dynamic_protocols_path.read_text(encoding="utf-8")) if dynamic_protocols_path.exists() else []
    except (FileNotFoundError, json.JSONDecodeError) as e:
        sys.stderr.write(f"[CRITICAL] Kunde inte ladda master schema eller dynamiska protokoll: {e}\n")
        existing_protocols, master_schema = [], None

    if master_schema:
        existing_ids = {p.get('protocolId') for p in existing_protocols}
        new_protocols_added_count = 0
        protocols_to_promote = set()
        protocols_to_deprecate = set() # For future use

        for p in files:
            data = load_session_file(p)
            if not data: continue
            
            # 1. Bearbeta nya, godkända protokoll
            approved = data.get("approvedNewDynamicProtocols", [])
            if isinstance(approved, list):
                for new_protocol in approved:
                    pid = new_protocol.get('protocolId')
                    if isinstance(new_protocol, dict) and pid not in existing_ids:
                        try:
                            validate(instance=new_protocol, schema=master_schema)
                            validate(instance=new_protocol, schema=new_protocol.get("schema", {}))
                            new_protocol['status'] = 'experimental' # Alltid som 'experimental' först
                            existing_protocols.append(new_protocol)
                            existing_ids.add(pid)
                            new_protocols_added_count += 1
                        except ValidationError as e:
                            sys.stderr.write(f"[REJECTED] Nytt protokoll {pid} från {p.name} misslyckades validering: {e.message}\n")
            
            # 2. Samla in instruktioner om att ändra status
            if data.get("promoteProtocols"): protocols_to_promote.update(data["promoteProtocols"])
            # (Här skulle logik för depreciering läggas till om det behövdes)

        # 3. Applicera statusändringar
        for protocol in existing_protocols:
            pid = protocol.get('protocolId')
            if pid in protocols_to_promote:
                protocol['status'] = 'active'
                print(f"[STATUS] Protokoll {pid} promoverat till 'active'.")
        
        # 4. Skriv tillbaka den uppdaterade databasen
        existing_protocols.sort(key=lambda p: p.get('protocolId', ''))
        dynamic_protocols_path.write_text(json.dumps(existing_protocols, ensure_ascii=False, indent=2), encoding="utf-8")
        if new_protocols_added_count > 0: print(f"[OK] Berikade {dynamic_protocols_path.name} med {new_protocols_added_count} nya protokoll.")
        print(f"[UT] {dynamic_protocols_path}")


    # --- Skriv ut konsoliderade filer ---
    (docs_dir / "ByggLogg.json").write_text(json.dumps(bygglogg, ensure_ascii=False, indent=2), encoding="utf-8")
    (docs_dir / "Chatthistorik.json").write_text(json.dumps(chathistorik, ensure_ascii=False, indent=2), encoding="utf-8")
    (docs_dir / "ai_protocol_performance.json").write_text(json.dumps(perf, ensure_ascii=False, indent=2), encoding="utf-8")
    (tools_dir / "frankensteen_learning_db.json").write_text(json.dumps(active_heuristics, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print(f"[OK] Skrev {len(bygglogg)} ByggLogg-poster, {len(chathistorik)} chattposter, {len(perf)} performance-poster.")
    print(f"[OK] Sanerade Learning DB: {len(active_heuristics)} aktiva heuristiker.")
    print(f"[UT] {docs_dir / 'ByggLogg.json'}")
    print(f"[UT] {docs_dir / 'Chatthistorik.json'}")
    print(f"[UT] {docs_dir / 'ai_protocol_performance.json'}")
    print(f"[UT] {tools_dir / 'frankensteen_learning_db.json'}")

if __name__ == "__main__":
    main()
