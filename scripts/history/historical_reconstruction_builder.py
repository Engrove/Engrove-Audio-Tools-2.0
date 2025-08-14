#!/usr/bin/env python3
# historical_reconstruction_builder.py (v6.0, 2025-08-14)
# Läs en mapp med [SESSIONID].json och konsolidera till standardfiler.
# v6.0 ARKITEKTURUPPGRADERING: Sorteringslogiken baseras nu uteslutande på 
# 'createdAt'-fältet inuti varje JSON-fil. Detta eliminerar helt det 
# bräckliga beroendet av filnamns-parsing och säkerställer 100% korrekt
# kronologisk ordning baserat på auktoritativ data.

import sys
import json
import re
from pathlib import Path
from typing import Dict, Any, List, Set, Tuple
from datetime import datetime, timezone, timedelta
from collections import OrderedDict

try:
    from jsonschema import validate
    from jsonschema.exceptions import ValidationError
except ImportError:
    print("ERROR: jsonschema is not installed. Please run: pip install jsonschema", file=sys.stderr)
    sys.exit(1)

SPEAKER_PATTERN = re.compile(r'^([^()]+) \(([^:]+):([^@]+)@([^\)]+)\)$')

def normalize_speaker(entry: Dict[str, Any]) -> Dict[str, Any]:
    # ... (oförändrad) ...
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
    # ... (oförändrad) ...
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

def load_json_file(p: Path) -> Any:
    # ... (oförändrad) ...
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        sys.stderr.write(f"[SKIP] {p.name}: {e}\n")
        return None

def main():
    if len(sys.argv) < 2:
        print("Användning: python3 historical_reconstruction_builder.py /path/to/sessions_dir [/output_root]")
        sys.exit(2)
    sessions_dir = Path(sys.argv[1])
    out_root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(".")
    
    docs_dir = out_root / "docs"
    ai_protocols_dir = docs_dir / "ai_protocols"
    tools_dir = out_root / "tools"
    dynamic_protocols_path = ai_protocols_dir / "DynamicProtocols.json"

    for d in [ai_protocols_dir, tools_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # Steg 1: Läs in alla sessionsfiler i minnet
    all_session_data = []
    for p in sessions_dir.glob("*.json"):
        if p.is_file():
            data = load_json_file(p)
            if data and isinstance(data, dict) and "createdAt" in data:
                all_session_data.append(data)
            else:
                sys.stderr.write(f"[WARNING] Skippar fil utan 'createdAt': {p.name}\n")

    # Steg 2: Sortera sessionsdata baserat på 'createdAt'-fältet
    all_session_data.sort(key=lambda s: s.get("createdAt", ""))

    # Steg 3: Bearbeta den sorterade datan
    bygglogg, chathistorik, perf, all_heuristics = [], [], [], []
    
    dynamic_protocols_map = OrderedDict()
    if dynamic_protocols_path.exists():
        protocols_list = load_json_file(dynamic_protocols_path)
        if isinstance(protocols_list, list):
            for proto in protocols_list:
                if isinstance(proto, dict) and 'protocolId' in proto:
                    dynamic_protocols_map[proto['protocolId']] = proto
    
    for data in all_session_data:
        artifacts = data.get("artifacts") or {}
        if isinstance(artifacts.get("ByggLogg"), dict): bygglogg.append(artifacts["ByggLogg"])
        if isinstance(artifacts.get("Chatthistorik"), dict): chathistorik.append(ensure_chat_schema(artifacts["Chatthistorik"]))
        if isinstance(artifacts.get("ai_protocol_performance"), dict): perf.append(artifacts["ai_protocol_performance"])
        
        lg = artifacts.get("frankensteen_learning_db")
        if isinstance(lg, list): all_heuristics.extend([h for h in lg if isinstance(h, dict)])
        elif isinstance(lg, dict): all_heuristics.append(lg)

        approved_protocols = data.get("approvedNewDynamicProtocols")
        if isinstance(approved_protocols, list):
            for proto in approved_protocols:
                if isinstance(proto, dict) and 'protocolId' in proto:
                    dynamic_protocols_map[proto['protocolId']] = proto
                    print(f"[INFO] Iscensatt uppdatering för dynamiskt protokoll: {proto['protocolId']}")
    
    # ... (Resten av logiken för att skriva filer är oförändrad) ...
    (tools_dir / "frankensteen_learning_db.json").write_text(json.dumps(all_heuristics, ensure_ascii=False, indent=2), encoding="utf-8")
    (docs_dir / "ByggLogg.json").write_text(json.dumps(bygglogg, ensure_ascii=False, indent=2), encoding="utf-8")
    (docs_dir / "Chatthistorik.json").write_text(json.dumps(chathistorik, ensure_ascii=False, indent=2), encoding="utf-8")
    (docs_dir / "ai_protocol_performance.json").write_text(json.dumps(perf, ensure_ascii=False, indent=2), encoding="utf-8")
    (ai_protocols_dir / "DynamicProtocols.json").write_text(json.dumps(list(dynamic_protocols_map.values()), ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[OK] Skrev {len(bygglogg)} ByggLogg-poster, {len(chathistorik)} chattposter, {len(perf)} performance-poster.")
    print(f"[OK] {len(all_heuristics)} heuristiker sammanställda.")
    print(f"[UT] {docs_dir / 'ByggLogg.json'}")
    print(f"[UT] {docs_dir / 'Chatthistorik.json'}")
    print(f"[UT] {docs_dir / 'ai_protocol_performance.json'}")
    print(f"[UT] {tools_dir / 'frankensteen_learning_db.json'}")
    print(f"[UT] {ai_protocols_dir / 'DynamicProtocols.json'}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Användning: python3 historical_reconstruction_builder.py <sessions_dir> [/output_root]")
        sys.exit(1)
    main()
